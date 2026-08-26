"""Allman latent-class benchmark with selection likelihoods and bridge fits."""

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


def _calibrate_intercept(
    linear_part: np.ndarray, target: float, weights: np.ndarray | None = None
) -> float:
    if weights is None:
        weights = np.full(len(linear_part), 1.0 / len(linear_part))
    else:
        weights = np.asarray(weights, dtype=float)
        weights = weights / weights.sum()
    lower, upper = -20.0, 20.0
    for _ in range(80):
        midpoint = (lower + upper) / 2.0
        if np.sum(weights * expit(midpoint + linear_part)) < target:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0


def _categorical_draw(probability: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    cumulative = np.cumsum(probability, axis=1)
    return (rng.uniform(size=(len(probability), 1)) > cumulative).sum(axis=1)


def _pair_cell_probability(config: dict, nonanchor_item: int) -> np.ndarray:
    model = config["model"]
    class_probability = np.asarray(model["class_probability"], dtype=float)
    probabilities = model["bernoulli_probability"]
    y1_probability = np.asarray(probabilities["Y1"], dtype=float)
    yj_probability = np.asarray(
        probabilities[f"Y{nonanchor_item + 1}"], dtype=float
    )
    output = np.zeros(4)
    for y1 in (0, 1):
        for yj in (0, 1):
            cell = 2 * y1 + yj
            output[cell] = np.sum(
                class_probability
                * np.where(y1, y1_probability, 1.0 - y1_probability)
                * np.where(yj, yj_probability, 1.0 - yj_probability)
            )
    return output


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
        shadow_config["probability_given_pair_cell"], dtype=float
    )
    shadows = []
    for pair in config["supported_pairs"]:
        pair_cell = (2 * y[:, pair[0]] + y[:, pair[1]]).astype(int)
        shadows.append(_categorical_draw(shadow_probability[pair_cell], rng))
    shadows = np.column_stack(shadows)

    missingness = config["missingness"]
    target_average = float(missingness["target_average_item_observation_rate"])
    target_nonanchor = (3.0 * target_average - 1.0) / 2.0
    selection_coefficient = missingness["selection_coefficients"]
    beta_y1 = float(selection_coefficient["Y1"])
    beta_yj = float(selection_coefficient["Yj"])
    beta_interaction = float(selection_coefficient["Y1_by_Yj"])
    observed = np.ones((n, 3), dtype=bool)
    pair_propensity = np.ones((n, len(config["supported_pairs"])), dtype=float)
    selection_parameter = []
    for block, pair in enumerate(config["supported_pairs"]):
        y1 = y[:, pair[0]]
        yj = y[:, pair[1]]
        linear_part = beta_y1 * y1 + beta_yj * yj + beta_interaction * y1 * yj
        population_cells = np.array(
            [
                beta_y1 * cell_y1
                + beta_yj * cell_yj
                + beta_interaction * cell_y1 * cell_yj
                for cell_y1, cell_yj in ((0, 0), (0, 1), (1, 0), (1, 1))
            ]
        )
        intercept = _calibrate_intercept(
            population_cells,
            target_nonanchor,
            _pair_cell_probability(config, pair[1]),
        )
        response_probability = expit(intercept + linear_part)
        observed[:, pair[1]] = rng.uniform(size=n) < response_probability
        pair_propensity[:, block] = response_probability
        selection_parameter.append(
            [intercept, beta_y1, beta_yj, beta_interaction]
        )

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


def estimate_saturated_bridge(
    y_pair: np.ndarray,
    response: np.ndarray,
    w: np.ndarray,
    shadow: np.ndarray,
    config: dict,
) -> tuple[np.ndarray, dict]:
    """Estimate a saturated inverse bridge from E[R r(Y_S)|Z_S,W]=1."""
    categories = int(config["shadow"]["categories"])
    instrument_cell = w * categories + shadow
    instrument_cell_count = 2 * categories
    outcome_cell_count = 4
    outcome_cell = (2 * y_pair[:, 0] + y_pair[:, 1]).astype(int)
    observed_index = np.flatnonzero(response)
    instrument_counts = np.bincount(
        instrument_cell, minlength=instrument_cell_count
    )
    design = np.zeros((instrument_cell_count, outcome_cell_count))
    for instrument in range(instrument_cell_count):
        denominator = max(int((instrument_cell == instrument).sum()), 1)
        for outcome in range(outcome_cell_count):
            design[instrument, outcome] = np.sum(
                response
                & (instrument_cell == instrument)
                & (outcome_cell == outcome)
            ) / denominator

    response_rate = np.clip(response.mean(), 0.05, 0.95)
    center = np.full(outcome_cell_count, 1.0 / response_rate)
    ridge = float(config["estimation"]["bridge_ridge"])
    normal_matrix = design.T @ design + ridge * np.eye(outcome_cell_count)
    normal_rhs = design.T @ np.ones(instrument_cell_count) + ridge * center
    unconstrained_bridge = np.linalg.solve(normal_matrix, normal_rhs)
    inverse_bridge = np.clip(
        unconstrained_bridge,
        1.0,
        float(config["estimation"]["maximum_inverse_weight"]),
    )
    moments = design @ inverse_bridge - 1.0
    probability_observed = 1.0 / inverse_bridge[outcome_cell[observed_index]]
    observed_inverse_weight = inverse_bridge[outcome_cell[observed_index]]
    effective_sample_size = (
        observed_inverse_weight.sum() ** 2
        / np.square(observed_inverse_weight).sum()
    )
    singular_values = np.linalg.svd(design, compute_uv=False)
    return probability_observed, {
        **{
            f"inverse_bridge_cell_{cell}": inverse_bridge[cell]
            for cell in range(outcome_cell_count)
        },
        "moment_norm": float(np.linalg.norm(moments)),
        "maximum_absolute_moment": float(np.abs(moments).max()),
        "design_rank": int(np.linalg.matrix_rank(design)),
        "minimum_singular_value": float(singular_values[-1]),
        "condition_number": float(
            singular_values[0] / max(singular_values[-1], EPS)
        ),
        "minimum_instrument_cell_count": int(instrument_counts.min()),
        "lower_constraint_count": int(np.sum(unconstrained_bridge < 1.0)),
        "upper_constraint_count": int(
            np.sum(
                unconstrained_bridge
                > float(config["estimation"]["maximum_inverse_weight"])
            )
        ),
        "mean_inverse_weight": float(observed_inverse_weight.mean()),
        "maximum_inverse_weight": float(observed_inverse_weight.max()),
        "effective_sample_size": float(effective_sample_size),
    }


def _selection_features(
    y1: np.ndarray, yj: np.ndarray, specification: str
) -> np.ndarray:
    if specification == "correct":
        regressors = [y1, yj, y1 * yj]
    elif specification == "misspecified":
        regressors = [yj]
    else:
        raise ValueError(f"Unknown selection specification: {specification}")
    return np.column_stack(
        [np.ones(y1.size), *[regressor.ravel() for regressor in regressors]]
    )


def _weighted_logistic_irls(
    features: np.ndarray,
    outcome: np.ndarray,
    weights: np.ndarray,
    initial: np.ndarray,
    config: dict,
) -> np.ndarray:
    parameter = initial.copy()
    ridge = float(config["estimation"]["selection_ridge"])
    for _ in range(int(config["estimation"]["selection_irls_max_iter"])):
        probability = np.clip(expit(features @ parameter), 1e-6, 1.0 - 1e-6)
        score = features.T @ (weights * (outcome - probability)) - ridge * parameter
        information = features.T @ (
            (weights * probability * (1.0 - probability))[:, None] * features
        ) + ridge * np.eye(features.shape[1])
        step = np.linalg.solve(information, score)
        parameter += step
        if np.linalg.norm(step) < float(config["estimation"]["em_tolerance"]):
            break
    return parameter


def fit_selection_likelihood(
    dataset: dict,
    config: dict,
    specification: str,
    rng: np.random.Generator,
) -> dict:
    """Fit the joint observed-data selection likelihood by EM."""
    y, w, observed = dataset["y"], dataset["w"], dataset["observed"]
    estimation = config["estimation"]
    n = len(y)
    state_f = np.repeat(np.arange(2), 4)
    state_y2 = np.tile(np.repeat(np.arange(2), 2), 2)
    state_y3 = np.tile(np.arange(2), 4)
    state_count = len(state_f)
    y1_state = np.repeat(y[:, [0]], state_count, axis=1)
    y2_state = np.repeat(state_y2[None, :], n, axis=0)
    y3_state = np.repeat(state_y3[None, :], n, axis=0)
    valid = np.ones((n, state_count), dtype=bool)
    valid &= (~observed[:, [1]]) | (y2_state == y[:, [1]])
    valid &= (~observed[:, [2]]) | (y3_state == y[:, [2]])

    def expectation_step(
        measurement: np.ndarray,
        w_kernel: np.ndarray,
        class_probability: np.ndarray,
        selection_parameter: list[np.ndarray],
    ) -> tuple[float, np.ndarray]:
        log_component = np.full((n, state_count), -np.inf)
        for state in range(state_count):
            latent = state_f[state]
            candidate = np.log(class_probability[latent])
            candidate = candidate + _binary_log_kernel(w, w_kernel[latent])
            candidate = candidate + _binary_log_kernel(
                y[:, 0], measurement[0, latent]
            )
            candidate = candidate + _binary_log_kernel(
                y2_state[:, state], measurement[1, latent]
            )
            candidate = candidate + _binary_log_kernel(
                y3_state[:, state], measurement[2, latent]
            )
            for local, item in enumerate((1, 2)):
                yj_state = y2_state[:, state] if item == 1 else y3_state[:, state]
                features = _selection_features(y[:, 0], yj_state, specification)
                probability = expit(features @ selection_parameter[local])
                candidate = candidate + _binary_log_kernel(
                    observed[:, item].astype(float), probability
                )
            log_component[:, state] = np.where(valid[:, state], candidate, -np.inf)

        maximum = log_component.max(axis=1, keepdims=True)
        stabilized = np.exp(log_component - maximum)
        posterior = stabilized / stabilized.sum(axis=1, keepdims=True)
        objective = float(
            np.sum(maximum[:, 0] + np.log(stabilized.sum(axis=1)))
        )
        return objective, posterior

    best = None
    for _ in range(int(estimation["em_starts"])):
        measurement, w_kernel, class_probability = _initial_parameters(y, rng)
        selection_intercept = np.array(
            [
                np.log(
                    observed[:, item].mean()
                    / (1.0 - observed[:, item].mean())
                )
                for item in (1, 2)
            ]
        )
        parameter_size = 4 if specification == "correct" else 2
        selection_parameter = [
            np.concatenate(
                (
                    [selection_intercept[local]],
                    rng.normal(0.0, 0.05, parameter_size - 1),
                )
            )
            for local in range(2)
        ]
        previous_objective = -np.inf
        converged = False
        for iteration in range(int(estimation["em_max_iter"])):
            objective, posterior = expectation_step(
                measurement,
                w_kernel,
                class_probability,
                selection_parameter,
            )

            class_total = np.bincount(
                state_f, weights=posterior.sum(axis=0), minlength=2
            )
            class_probability = class_total / class_total.sum()
            for latent in (0, 1):
                latent_weight = posterior[:, state_f == latent].sum(axis=1)
                w_kernel[latent] = np.sum(latent_weight * w) / class_total[latent]
                measurement[0, latent] = (
                    np.sum(latent_weight * y[:, 0]) / class_total[latent]
                )
                measurement[1, latent] = (
                    np.sum(posterior[:, state_f == latent] * y2_state[:, state_f == latent])
                    / class_total[latent]
                )
                measurement[2, latent] = (
                    np.sum(posterior[:, state_f == latent] * y3_state[:, state_f == latent])
                    / class_total[latent]
                )
            w_kernel = np.clip(w_kernel, 0.01, 0.99)
            measurement = np.clip(measurement, 0.01, 0.99)

            for local, item in enumerate((1, 2)):
                yj_state = y2_state if item == 1 else y3_state
                features = _selection_features(y1_state, yj_state, specification)
                outcomes = np.repeat(observed[:, [item]], state_count, axis=1).ravel()
                selection_parameter[local] = _weighted_logistic_irls(
                    features,
                    outcomes,
                    posterior.ravel(),
                    selection_parameter[local],
                    config,
                )

            if abs(objective - previous_objective) <= float(
                estimation["em_tolerance"]
            ) * (1.0 + abs(objective)):
                converged = True
                break
            previous_objective = objective

        if measurement[0, 0] > measurement[0, 1]:
            measurement = measurement[:, ::-1]
            w_kernel = w_kernel[::-1]
            class_probability = class_probability[::-1]
        objective, _ = expectation_step(
            measurement,
            w_kernel,
            class_probability,
            selection_parameter,
        )
        candidate = {
            "objective": objective,
            "measurement": measurement,
            "w_kernel": w_kernel,
            "class_probability": class_probability,
            "selection_parameter": np.asarray(selection_parameter),
            "iterations": iteration + 1,
            "converged": converged,
            "bridge_diagnostics": [],
        }
        if best is None or candidate["objective"] > best["objective"]:
            best = candidate
    return best


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


def fit_ignorable_latent_model(
    dataset: dict,
    config: dict,
    method: str,
    rng: np.random.Generator,
) -> dict:
    """Fit the complete-data oracle or MAR observed-data likelihood by EM."""
    y, w = dataset["y"], dataset["w"]
    if method == "full_data_oracle":
        item_observed = np.ones_like(dataset["observed"], dtype=bool)
    elif method == "mar":
        item_observed = dataset["observed"]
    else:
        raise ValueError(f"Unknown ignorable method: {method}")
    estimation = config["estimation"]

    def expectation_step(
        measurement: np.ndarray,
        w_kernel: np.ndarray,
        class_probability: np.ndarray,
    ) -> tuple[float, np.ndarray]:
        log_component = np.zeros((len(y), 2))
        for latent in (0, 1):
            log_component[:, latent] = np.log(class_probability[latent])
            log_component[:, latent] += _binary_log_kernel(
                w, w_kernel[latent]
            )
            for item in range(3):
                contribution = _binary_log_kernel(
                    y[:, item], measurement[item, latent]
                )
                log_component[:, latent] += np.where(
                    item_observed[:, item], contribution, 0.0
                )
        maximum = log_component.max(axis=1, keepdims=True)
        stabilized = np.exp(log_component - maximum)
        posterior = stabilized / stabilized.sum(axis=1, keepdims=True)
        objective = float(
            np.sum(maximum[:, 0] + np.log(stabilized.sum(axis=1)))
        )
        return objective, posterior

    best = None
    for _ in range(int(estimation["em_starts"])):
        measurement, w_kernel, class_probability = _initial_parameters(y, rng)
        previous_objective = -np.inf
        converged = False
        for iteration in range(int(estimation["em_max_iter"])):
            objective, posterior = expectation_step(
                measurement, w_kernel, class_probability
            )

            class_total = posterior.sum(axis=0)
            class_probability = class_total / class_total.sum()
            w_kernel = np.clip(
                (posterior * w[:, None]).sum(axis=0) / class_total,
                0.01,
                0.99,
            )
            for item in range(3):
                for latent in (0, 1):
                    effective = posterior[:, latent] * item_observed[:, item]
                    measurement[item, latent] = np.sum(
                        effective * y[:, item]
                    ) / max(effective.sum(), EPS)
            measurement = np.clip(measurement, 0.01, 0.99)
            if abs(objective - previous_objective) <= float(
                estimation["em_tolerance"]
            ) * (1.0 + abs(objective)):
                converged = True
                break
            previous_objective = objective

        if measurement[0, 0] > measurement[0, 1]:
            measurement = measurement[:, ::-1]
            w_kernel = w_kernel[::-1]
            class_probability = class_probability[::-1]
        objective, _ = expectation_step(measurement, w_kernel, class_probability)
        candidate = {
            "objective": objective,
            "measurement": measurement,
            "w_kernel": w_kernel,
            "class_probability": class_probability,
            "iterations": iteration + 1,
            "converged": converged,
            "bridge_diagnostics": [],
        }
        if best is None or candidate["objective"] > best["objective"]:
            best = candidate
    return best


def fit_latent_model(
    dataset: dict,
    config: dict,
    method: str,
    rng: np.random.Generator,
) -> dict:
    """Fit the Allman model by full-data or pairwise composite EM."""
    if method in {"full_data_oracle", "mar"}:
        return fit_ignorable_latent_model(dataset, config, method, rng)
    if method == "selection_likelihood_correct":
        return fit_selection_likelihood(dataset, config, "correct", rng)
    if method == "selection_likelihood_misspecified":
        return fit_selection_likelihood(dataset, config, "misspecified", rng)

    y, w, observed = dataset["y"], dataset["w"], dataset["observed"]
    pairs = [tuple(pair) for pair in config["supported_pairs"]]
    estimation = config["estimation"]
    pair_masks, pair_weights, bridge_diagnostics = [], [], []
    for block, pair in enumerate(pairs):
        mask = observed[:, pair].all(axis=1)
        if method == "proposed_saturated_bridge":
            propensity, diagnostics = estimate_saturated_bridge(
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

    def evaluate_objective(
        measurement: np.ndarray,
        w_kernel: np.ndarray,
        class_probability: np.ndarray,
    ) -> float:
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
            objective += float(
                np.sum(
                    weights
                    * (maximum[:, 0] + np.log(stabilized.sum(axis=1)))
                )
            )
        return objective

    best = None
    for _ in range(int(estimation["em_starts"])):
        measurement, w_kernel, class_probability = _initial_parameters(y, rng)
        previous_objective = -np.inf
        converged = False
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
                converged = True
                break
            previous_objective = objective

        if measurement[0, 0] > measurement[0, 1]:
            measurement = measurement[:, ::-1]
            w_kernel = w_kernel[::-1]
            class_probability = class_probability[::-1]
        objective = evaluate_objective(measurement, w_kernel, class_probability)
        candidate = {
            "objective": objective,
            "measurement": measurement,
            "w_kernel": w_kernel,
            "class_probability": class_probability,
            "iterations": iteration + 1,
            "converged": converged,
        }
        if best is None or candidate["objective"] > best["objective"]:
            best = candidate
    best["bridge_diagnostics"] = bridge_diagnostics
    return best


def run_simulation(
    config: dict,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    master_rng = np.random.default_rng(int(config["seed"]))
    records, overlap_records, bridge_records = [], [], []
    for replication in range(int(config["replications"])):
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
            record = {
                "replication": replication,
                "method": method,
                "M_bias": float(measurement_error.mean()),
                "M_absolute_error": float(np.abs(measurement_error).mean()),
                "M_squared_error": float(np.square(measurement_error).mean()),
                "p_f1_estimate": float(fit["class_probability"][1]),
                "p_f1_error": float(p_error),
                "objective": float(fit["objective"]),
                "iterations": fit["iterations"],
                "converged": fit["converged"],
            }
            for item in range(measurement_error.shape[0]):
                for latent in range(measurement_error.shape[1]):
                    suffix = f"Y{item + 1}_f{latent}"
                    record[f"M_estimate_{suffix}"] = float(
                        fit["measurement"][item, latent]
                    )
                    record[f"M_error_{suffix}"] = float(
                        measurement_error[item, latent]
                    )
            records.append(record)
            for block, diagnostics in enumerate(fit["bridge_diagnostics"]):
                bridge_records.append(
                    {
                        "replication": replication,
                        "method": method,
                        "block": block,
                        **diagnostics,
                    }
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
            convergence_rate=("converged", "mean"),
        )
    )
    summary["M_RMSE"] = np.sqrt(summary.pop("M_mean_squared_error"))
    summary["p_f1_RMSE"] = np.sqrt(summary.pop("p_f1_mean_squared_error"))
    return (
        summary,
        pd.DataFrame.from_records(overlap_records),
        pd.DataFrame.from_records(bridge_records),
        raw,
    )
