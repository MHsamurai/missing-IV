"""Pilot DGPs and pairwise latent-class estimators.

The pilot isolates latent-model recoverability. It uses the true block
propensities for the oracle bridge; estimated bridge methods are intentionally
left for the next implementation stage.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


EPS = 1e-10


def load_config(path: str | Path) -> dict:
    """Load the JSON-compatible YAML configuration without extra dependencies."""
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def expit(value: np.ndarray) -> np.ndarray:
    value = np.asarray(value, dtype=float)
    output = np.empty_like(value)
    positive = value >= 0
    output[positive] = 1.0 / (1.0 + np.exp(-value[positive]))
    exponential = np.exp(value[~positive])
    output[~positive] = exponential / (1.0 + exponential)
    return output


def _calibrate_intercept(linear_part: np.ndarray, target: float) -> float:
    lower, upper = -20.0, 20.0
    for _ in range(80):
        midpoint = (lower + upper) / 2.0
        if expit(midpoint + linear_part).mean() < target:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0


def simulate_dataset(config: dict, profile_name: str, rng: np.random.Generator) -> dict:
    profile = config["profiles"][profile_name]
    n = int(config["sample_size"])
    m = int(config["items"])
    family = profile["family"]
    measurement = np.asarray(profile["measurement_parameter"], dtype=float)

    w = rng.binomial(1, 0.5, size=n)
    x = rng.normal(size=(n, 2))
    latent_shift = config["latent_shift"]
    lambda_by_w = np.array([
        latent_shift["p_f1_given_w0"],
        latent_shift["p_f1_given_w1"],
    ])
    latent_probability = lambda_by_w[w]
    latent_class = rng.binomial(1, latent_probability)

    proxy = config["shadow_proxy"]
    proxy_probability = np.where(
        latent_class[:, None] == 1,
        proxy["p_z1_given_f1"],
        proxy["p_z1_given_f0"],
    )
    z = rng.binomial(1, np.repeat(proxy_probability, m, axis=1))

    item_parameter = measurement[np.arange(m)[None, :], latent_class[:, None]]
    if family == "binary":
        y = rng.binomial(1, item_parameter).astype(float)
    elif family == "normal":
        y = rng.normal(item_parameter, float(profile.get("normal_sd", 1.0)))
    elif family == "poisson":
        y = rng.poisson(item_parameter).astype(float)
    else:
        raise ValueError(f"Unsupported family: {family}")

    missingness = config["missingness"]
    centered_y = (y - y.mean(axis=0)) / np.maximum(y.std(axis=0), 0.25)
    linear_part = (
        missingness["outcome_slope"] * centered_y
        + missingness["x_slope"] * x[:, [0]]
        + missingness["w_slope"] * w[:, None]
    )
    target_rate = float(config["target_item_observation_rate"])
    intercepts = np.array([
        _calibrate_intercept(linear_part[:, j], target_rate) for j in range(m)
    ])
    item_propensity = expit(linear_part + intercepts)
    observed = rng.uniform(size=(n, m)) < item_propensity

    return {
        "profile": profile_name,
        "family": family,
        "y": y,
        "observed": observed,
        "item_propensity": item_propensity,
        "w": w,
        "x": x,
        "z": z,
        "latent_class": latent_class,
        "lambda_by_w_true": lambda_by_w,
        "p_f1_true": float(lambda_by_w.mean()),
        "measurement_true": measurement,
    }


def _log_measurement(y: np.ndarray, parameter: np.ndarray, family: str, normal_sd: float) -> np.ndarray:
    parameter = np.clip(parameter, EPS, None) if family == "poisson" else parameter
    if family == "binary":
        probability = np.clip(parameter, EPS, 1.0 - EPS)
        return y * np.log(probability) + (1.0 - y) * np.log(1.0 - probability)
    if family == "normal":
        return -0.5 * ((y - parameter) / normal_sd) ** 2 - np.log(normal_sd)
    if family == "poisson":
        return y * np.log(parameter) - parameter
    raise ValueError(f"Unsupported family: {family}")


def _initial_measurement(y: np.ndarray, family: str, rng: np.random.Generator) -> np.ndarray:
    m = y.shape[1]
    center = np.nanmean(y, axis=0)
    spread = np.maximum(np.nanstd(y, axis=0), 0.20)
    if family == "binary":
        lower = np.clip(center - 0.18 - rng.uniform(0.0, 0.08, m), 0.03, 0.90)
        upper = np.clip(center + 0.18 + rng.uniform(0.0, 0.08, m), 0.10, 0.97)
    elif family == "normal":
        lower = center - 0.65 * spread - rng.uniform(0.0, 0.20, m)
        upper = center + 0.65 * spread + rng.uniform(0.0, 0.20, m)
    else:
        lower = np.clip(center * rng.uniform(0.45, 0.75, m), 0.05, None)
        upper = np.clip(center * rng.uniform(1.20, 1.65, m), 0.10, None)
    return np.column_stack([lower, upper])


def fit_pairwise_latent_model(
    dataset: dict,
    config: dict,
    method: str,
    rng: np.random.Generator,
) -> dict:
    """Fit a two-class model to anchor and extension pair composite laws."""
    y_full = dataset["y"]
    observed = dataset["observed"]
    propensity = dataset["item_propensity"]
    w = dataset["w"]
    family = dataset["family"]
    profile = config["profiles"][dataset["profile"]]
    normal_sd = float(profile.get("normal_sd", 1.0))
    pairs = [tuple(pair) for pair in config["supported_pairs"]]
    em = config["em"]

    best = None
    for _ in range(int(em["starts"])):
        measurement = _initial_measurement(y_full, family, rng)
        lambda_by_w = np.clip(np.array([0.35, 0.65]) + rng.normal(0, 0.04, 2), 0.08, 0.92)
        previous_objective = -np.inf

        for iteration in range(int(em["max_iter"])):
            numerator_f1 = np.zeros(2)
            denominator_lambda = np.zeros(2)
            numerator_measurement = np.zeros_like(measurement)
            denominator_measurement = np.zeros_like(measurement)
            objective = 0.0

            for pair in pairs:
                pair_index = np.asarray(pair)
                if method == "full_data_oracle":
                    mask = np.ones(len(y_full), dtype=bool)
                    weights = np.ones(len(y_full))
                else:
                    mask = observed[:, pair_index].all(axis=1)
                    weights = np.ones(mask.sum())
                    if method == "oracle_bridge":
                        pair_propensity = propensity[:, pair_index].prod(axis=1)
                        weights = 1.0 / np.maximum(pair_propensity[mask], EPS)
                        weights = np.minimum(weights, float(em["max_weight"]))

                y_pair = y_full[mask][:, pair_index]
                w_pair = w[mask]
                if len(y_pair) == 0:
                    continue

                log_component = np.empty((len(y_pair), 2))
                for latent in (0, 1):
                    prior = np.where(w_pair == 1, lambda_by_w[1], lambda_by_w[0])
                    log_prior = np.log(np.clip(prior if latent == 1 else 1.0 - prior, EPS, 1.0))
                    log_kernel = np.zeros(len(y_pair))
                    for local_index, item in enumerate(pair_index):
                        log_kernel += _log_measurement(
                            y_pair[:, local_index], measurement[item, latent], family, normal_sd
                        )
                    log_component[:, latent] = log_prior + log_kernel

                maximum = log_component.max(axis=1, keepdims=True)
                stabilized = np.exp(log_component - maximum)
                posterior = stabilized[:, 1] / stabilized.sum(axis=1)
                log_mixture = maximum[:, 0] + np.log(stabilized.sum(axis=1))
                objective += float(np.sum(weights * log_mixture))

                for w_value in (0, 1):
                    in_group = w_pair == w_value
                    numerator_f1[w_value] += np.sum(weights[in_group] * posterior[in_group])
                    denominator_lambda[w_value] += np.sum(weights[in_group])

                for local_index, item in enumerate(pair_index):
                    response = y_pair[:, local_index]
                    for latent, responsibility in ((0, 1.0 - posterior), (1, posterior)):
                        effective_weight = weights * responsibility
                        numerator_measurement[item, latent] += np.sum(effective_weight * response)
                        denominator_measurement[item, latent] += np.sum(effective_weight)

            lambda_by_w = np.clip(
                numerator_f1 / np.maximum(denominator_lambda, EPS), 0.01, 0.99
            )
            measurement = numerator_measurement / np.maximum(denominator_measurement, EPS)
            if family == "binary":
                measurement = np.clip(measurement, 0.01, 0.99)
            elif family == "poisson":
                measurement = np.clip(measurement, 0.02, None)

            if abs(objective - previous_objective) <= float(em["tolerance"]) * (1.0 + abs(objective)):
                break
            previous_objective = objective

        if measurement[0, 0] > measurement[0, 1]:
            measurement = measurement[:, ::-1]
            lambda_by_w = 1.0 - lambda_by_w

        candidate = {
            "objective": objective,
            "measurement": measurement,
            "lambda_by_w": lambda_by_w,
            "iterations": iteration + 1,
        }
        if best is None or candidate["objective"] > best["objective"]:
            best = candidate

    w_probability = np.array([(w == 0).mean(), (w == 1).mean()])
    best["p_f1"] = float(np.dot(w_probability, best["lambda_by_w"]))
    return best


def run_pilot(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    master_rng = np.random.default_rng(int(config["seed"]))
    methods = [
        name for name, settings in config["methods"].items() if settings["pilot_enabled"]
    ]
    records = []
    diagnostics = []

    for profile_name in config["profiles"]:
        for replication in range(int(config["pilot_replications"])):
            dataset_seed = int(master_rng.integers(0, 2**32 - 1))
            dataset = simulate_dataset(config, profile_name, np.random.default_rng(dataset_seed))
            observed = dataset["observed"]
            diagnostics.append({
                "profile": profile_name,
                "replication": replication,
                "item_observation_rate": observed.mean(),
                "anchor_pair_rate": observed[:, [0, 1]].all(axis=1).mean(),
                "extension_pair_rate": observed[:, [0, 2]].all(axis=1).mean(),
                "complete_case_rate": observed.all(axis=1).mean(),
                "minimum_item_propensity": dataset["item_propensity"].min(),
            })
            for method in methods:
                fit_seed = int(master_rng.integers(0, 2**32 - 1))
                fit = fit_pairwise_latent_model(
                    dataset, config, method, np.random.default_rng(fit_seed)
                )
                measurement_error = fit["measurement"] - dataset["measurement_true"]
                mean_class_gap = float(
                    np.mean(np.abs(np.diff(dataset["measurement_true"], axis=1)))
                )
                records.append({
                    "profile": profile_name,
                    "family": dataset["family"],
                    "method": method,
                    "replication": replication,
                    "M_signed_error": float(measurement_error.mean()),
                    "M_absolute_error": float(np.abs(measurement_error).mean()),
                    "M_squared_error": float(np.square(measurement_error).mean()),
                    "M_normalized_squared_error": float(
                        np.square(measurement_error).mean() / mean_class_gap**2
                    ),
                    "p_f1_error": fit["p_f1"] - dataset["p_f1_true"],
                    "iterations": fit["iterations"],
                })

    raw = pd.DataFrame.from_records(records)
    summary = (
        raw.groupby(["profile", "family", "method"], as_index=False)
        .agg(
            M_bias=("M_signed_error", "mean"),
            M_mean_absolute_error=("M_absolute_error", "mean"),
            M_mean_squared_error=("M_squared_error", "mean"),
            M_normalized_mean_squared_error=("M_normalized_squared_error", "mean"),
            p_f1_bias=("p_f1_error", "mean"),
            p_f1_mean_squared_error=("p_f1_error", lambda value: np.mean(np.square(value))),
            mean_iterations=("iterations", "mean"),
        )
    )
    summary["M_RMSE"] = np.sqrt(summary.pop("M_mean_squared_error"))
    summary["M_normalized_RMSE"] = np.sqrt(
        summary.pop("M_normalized_mean_squared_error")
    )
    summary["p_f1_RMSE"] = np.sqrt(summary.pop("p_f1_mean_squared_error"))
    return summary, pd.DataFrame.from_records(diagnostics)
