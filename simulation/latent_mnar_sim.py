"""Allman latent-class benchmark with MAR and estimated-bridge fits."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


EPS = 1e-10


def load_config(path: str | Path) -> dict:
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


def _categorical_draw(probability: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    cumulative = np.cumsum(probability, axis=1)
    return (rng.uniform(size=(len(probability), 1)) > cumulative).sum(axis=1)


def simulate_allman_dataset(config: dict, rng: np.random.Generator) -> dict:
    """Generate the Allman product mixture P=sum_f pi_f tensor_j p_fj."""
    n = int(config["sample_size"])
    model = config["model"]
    class_probability = np.asarray(model["class_probability"], dtype=float)
    latent_class = rng.choice(2, size=n, p=class_probability)

    feature_probability = model["bernoulli_probability"]
    w_kernel = np.asarray(feature_probability["W"], dtype=float)
    measurement = np.asarray(
        [feature_probability[name] for name in ("Y1", "Y2", "Y3")], dtype=float
    )
    w = rng.binomial(1, w_kernel[latent_class])
    y_probability = measurement[np.arange(3)[None, :], latent_class[:, None]]
    y = rng.binomial(1, y_probability).astype(float)

    shadow_config = config["shadow"]
    shadow_probability = np.asarray(
        [
            shadow_config["probability_given_f0"],
            shadow_config["probability_given_f1"],
        ],
        dtype=float,
    )
    shadows = np.column_stack(
        [
            _categorical_draw(shadow_probability[latent_class], rng)
            for _ in config["supported_pairs"]
        ]
    )

    missingness = config["missingness"]
    target_average = float(missingness["target_average_item_observation_rate"])
    target_nonanchor = (3.0 * target_average - 1.0) / 2.0
    selection_slope = float(missingness["selection_slope_on_pair_sum"])
    observed = np.ones((n, 3), dtype=bool)
    pair_propensity = np.ones((n, len(config["supported_pairs"])), dtype=float)
    selection_parameter = []
    for block, pair in enumerate(config["supported_pairs"]):
        pair_sum = y[:, pair].sum(axis=1)
        intercept = _calibrate_intercept(selection_slope * pair_sum, target_nonanchor)
        response_probability = expit(intercept + selection_slope * pair_sum)
        observed[:, pair[1]] = rng.uniform(size=n) < response_probability
        pair_propensity[:, block] = response_probability
        selection_parameter.append([intercept, selection_slope])

    return {
        "y": y,
        "w": w,
        "observed": observed,
        "shadows": shadows,
        "pair_propensity_true": pair_propensity,
        "measurement_true": measurement,
        "w_kernel_true": w_kernel,
        "class_probability_true": class_probability,
        "selection_parameter_true": np.asarray(selection_parameter),
    }


def estimate_block_bridge(
    y_pair: np.ndarray,
    response: np.ndarray,
    w: np.ndarray,
    shadow: np.ndarray,
    config: dict,
) -> tuple[np.ndarray, dict]:
    """Estimate logit pi_S(y_S) from E[R/pi_S(Y_S)|Z_S,W]=1."""
    categories = int(config["shadow"]["categories"])
    cell = w * categories + shadow
    cell_count = 2 * categories
    observed_index = np.flatnonzero(response)
    design = np.column_stack(
        [np.ones(len(observed_index)), y_pair[observed_index].sum(axis=1)]
    )
    response_rate = np.clip(response.mean(), 0.01, 0.99)
    parameter = np.array([np.log(response_rate / (1.0 - response_rate)), 0.0])

    def evaluate(candidate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        probability = expit(design @ candidate)
        inverse = 1.0 / np.maximum(probability, EPS)
        moments = np.zeros(cell_count)
        jacobian = np.zeros((cell_count, 2))
        for category in range(cell_count):
            denominator = max(int((cell == category).sum()), 1)
            in_observed_cell = cell[observed_index] == category
            moments[category] = -1.0
            if in_observed_cell.any():
                moments[category] += inverse[in_observed_cell].sum() / denominator
                derivative = -(
                    (1.0 - probability[in_observed_cell]) * inverse[in_observed_cell]
                )[:, None] * design[in_observed_cell]
                jacobian[category] = derivative.sum(axis=0) / denominator
        return moments, jacobian

    converged = False
    for iteration in range(int(config["estimation"]["bridge_max_iter"])):
        moments, jacobian = evaluate(parameter)
        step = np.linalg.solve(
            jacobian.T @ jacobian + 1e-8 * np.eye(2), jacobian.T @ moments
        )
        objective = float(moments @ moments)
        scale = 1.0
        while scale > 1e-5:
            candidate = parameter - scale * step
            candidate_moments, _ = evaluate(candidate)
            if float(candidate_moments @ candidate_moments) < objective:
                parameter = candidate
                break
            scale *= 0.5
        if np.linalg.norm(scale * step) < float(
            config["estimation"]["bridge_tolerance"]
        ):
            converged = True
            break

    moments, jacobian = evaluate(parameter)
    probability_observed = expit(design @ parameter)
    return probability_observed, {
        "parameter_0": parameter[0],
        "parameter_1": parameter[1],
        "iterations": iteration + 1,
        "converged": converged,
        "moment_norm": float(np.linalg.norm(moments)),
        "minimum_information_eigenvalue": float(
            np.linalg.eigvalsh(jacobian.T @ jacobian).min()
        ),
    }


def _initial_parameters(
    y: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    center = y.mean(axis=0)
    measurement = np.column_stack(
        [
            np.clip(center - rng.uniform(0.15, 0.25, 3), 0.03, 0.90),
            np.clip(center + rng.uniform(0.15, 0.25, 3), 0.10, 0.97),
        ]
    )
    w_kernel = np.clip(
        np.array([0.25, 0.75]) + rng.normal(0, 0.03, 2), 0.03, 0.97
    )
    class_probability = np.clip(
        np.array([0.55, 0.45]) + rng.normal(0, 0.03, 2), 0.05, None
    )
    class_probability /= class_probability.sum()
    return measurement, w_kernel, class_probability


def _binary_log_kernel(value: np.ndarray, probability: float) -> np.ndarray:
    probability = np.clip(probability, EPS, 1.0 - EPS)
    return value * np.log(probability) + (1.0 - value) * np.log(1.0 - probability)


def fit_latent_model(
    dataset: dict,
    config: dict,
    method: str,
    rng: np.random.Generator,
) -> dict:
    """Fit the Allman model by full-data or pairwise composite EM."""
    y, w, observed = dataset["y"], dataset["w"], dataset["observed"]
    pairs = [tuple(pair) for pair in config["supported_pairs"]]
    estimation = config["estimation"]
    pair_masks, pair_weights, bridge_diagnostics = [], [], []
    for block, pair in enumerate(pairs):
        if method == "full_data_oracle":
            mask = np.ones(len(y), dtype=bool)
            weights = np.ones(len(y))
        else:
            mask = observed[:, pair].all(axis=1)
            if method == "mar":
                weights = np.ones(mask.sum())
            elif method == "proposed_bridge":
                propensity, diagnostics = estimate_block_bridge(
                    y[:, pair], mask, w, dataset["shadows"][:, block], config
                )
                weights = np.minimum(
                    1.0 / np.maximum(propensity, EPS),
                    float(estimation["maximum_inverse_weight"]),
                )
                bridge_diagnostics.append(diagnostics)
            else:
                raise ValueError(f"Unknown method: {method}")
        pair_masks.append(mask)
        pair_weights.append(weights)

    best = None
    for _ in range(int(estimation["em_starts"])):
        measurement, w_kernel, class_probability = _initial_parameters(y, rng)
        previous_objective = -np.inf
        for iteration in range(int(estimation["em_max_iter"])):
            class_total = np.zeros(2)
            w_total = np.zeros(2)
            y_total = np.zeros((3, 2))
            y_weight = np.zeros((3, 2))
            objective = 0.0
            for pair, mask, weights in zip(pairs, pair_masks, pair_weights):
                y_pair, w_pair = y[mask][:, pair], w[mask]
                log_component = np.zeros((len(y_pair), 2))
                for latent in (0, 1):
                    log_component[:, latent] = np.log(class_probability[latent])
                    log_component[:, latent] += _binary_log_kernel(
                        w_pair, w_kernel[latent]
                    )
                    for local, item in enumerate(pair):
                        log_component[:, latent] += _binary_log_kernel(
                            y_pair[:, local], measurement[item, latent]
                        )
                maximum = log_component.max(axis=1, keepdims=True)
                stabilized = np.exp(log_component - maximum)
                posterior = stabilized / stabilized.sum(axis=1, keepdims=True)
                objective += float(
                    np.sum(weights * (maximum[:, 0] + np.log(stabilized.sum(axis=1))))
                )
                for latent in (0, 1):
                    effective = weights * posterior[:, latent]
                    class_total[latent] += effective.sum()
                    w_total[latent] += np.sum(effective * w_pair)
                    for local, item in enumerate(pair):
                        y_total[item, latent] += np.sum(effective * y_pair[:, local])
                        y_weight[item, latent] += effective.sum()
            class_probability = class_total / class_total.sum()
            w_kernel = np.clip(w_total / np.maximum(class_total, EPS), 0.01, 0.99)
            measurement = np.clip(y_total / np.maximum(y_weight, EPS), 0.01, 0.99)
            if abs(objective - previous_objective) <= float(
                estimation["em_tolerance"]
            ) * (1.0 + abs(objective)):
                break
            previous_objective = objective

        if measurement[0, 0] > measurement[0, 1]:
            measurement = measurement[:, ::-1]
            w_kernel = w_kernel[::-1]
            class_probability = class_probability[::-1]
        candidate = {
            "objective": objective,
            "measurement": measurement,
            "w_kernel": w_kernel,
            "class_probability": class_probability,
            "iterations": iteration + 1,
        }
        if best is None or candidate["objective"] > best["objective"]:
            best = candidate
    best["bridge_diagnostics"] = bridge_diagnostics
    return best


def run_simulation(config: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    master_rng = np.random.default_rng(int(config["seed"]))
    records, overlap_records, bridge_records = [], [], []
    for replication in range(int(config["pilot_replications"])):
        dataset = simulate_allman_dataset(
            config, np.random.default_rng(int(master_rng.integers(0, 2**32 - 1)))
        )
        observed = dataset["observed"]
        overlap_records.append(
            {
                "replication": replication,
                "item_observation_rate": observed.mean(),
                "anchor_pair_rate": observed[:, [0, 1]].all(axis=1).mean(),
                "extension_pair_rate": observed[:, [0, 2]].all(axis=1).mean(),
                "complete_case_rate": observed.all(axis=1).mean(),
                "minimum_true_pair_propensity": dataset["pair_propensity_true"].min(),
            }
        )
        for method in config["estimation"]["methods"]:
            fit = fit_latent_model(
                dataset,
                config,
                method,
                np.random.default_rng(int(master_rng.integers(0, 2**32 - 1))),
            )
            measurement_error = fit["measurement"] - dataset["measurement_true"]
            p_error = (
                fit["class_probability"][1]
                - dataset["class_probability_true"][1]
            )
            records.append(
                {
                    "replication": replication,
                    "method": method,
                    "M_bias": float(measurement_error.mean()),
                    "M_absolute_error": float(np.abs(measurement_error).mean()),
                    "M_squared_error": float(np.square(measurement_error).mean()),
                    "p_f1_error": float(p_error),
                    "iterations": fit["iterations"],
                }
            )
            for block, diagnostics in enumerate(fit["bridge_diagnostics"]):
                bridge_records.append(
                    {"replication": replication, "block": block, **diagnostics}
                )

    raw = pd.DataFrame.from_records(records)
    summary = (
        raw.groupby("method", as_index=False)
        .agg(
            M_bias=("M_bias", "mean"),
            M_mean_absolute_error=("M_absolute_error", "mean"),
            M_mean_squared_error=("M_squared_error", "mean"),
            p_f1_bias=("p_f1_error", "mean"),
            p_f1_mean_squared_error=(
                "p_f1_error",
                lambda value: np.mean(np.square(value)),
            ),
            mean_iterations=("iterations", "mean"),
        )
    )
    summary["M_RMSE"] = np.sqrt(summary.pop("M_mean_squared_error"))
    summary["p_f1_RMSE"] = np.sqrt(summary.pop("p_f1_mean_squared_error"))
    return (
        summary,
        pd.DataFrame.from_records(overlap_records),
        pd.DataFrame.from_records(bridge_records),
    )
