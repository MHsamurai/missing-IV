"""Deterministic population identities and counterexamples; no Monte Carlo."""

from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from unittest import TestCase, main, mock

import numpy as np

from simulation import dgp_validation as validation
from simulation.latent_mnar_sim import load_config, simulate_allman_dataset


class PopulationValidationTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(validation.DEFAULT_CONFIG)
        cls.report = validation.validate_dgp(cls.config)

    def test_current_population_passes_weak_model_but_violates_old_strong_exclusion(self) -> None:
        self.assertTrue(self.report["passed"], self.report)
        self.assertEqual(self.report["failed_checks"], [])
        diagnostic = self.report["diagnostics"]["old_strong_y_z_exclusion"]
        self.assertFalse(diagnostic["holds"])
        self.assertFalse(diagnostic["required_for_weak_model"])
        self.assertGreater(diagnostic["max_absolute_difference"], 0.1)
        self.assertNotIn("old_strong_y_z_exclusion", self.report["checks"])
        json.dumps(self.report, allow_nan=False)

    def test_enumeration_shape_support_and_normalization(self) -> None:
        population = validation.enumerate_population(self.config)
        self.assertEqual(population.joint.shape, (2, 2, 2, 2, 2, 4, 4, 2, 2))
        self.assertEqual(population.joint.size, 2048)
        self.assertTrue((population.joint > 0).all())
        self.assertAlmostEqual(float(population.joint.sum()), 1)
        self.assertEqual(population.propensities.shape, (2, 4))
        self.assertTrue(((population.propensities > 0) & (population.propensities < 1)).all())
        self.assertEqual(population.intercepts.shape, (2,))

    def test_population_measurement_marginalizes_z_and_excludes_w(self) -> None:
        population = validation.enumerate_population(self.config)
        joint_fwy = population.joint.sum(axis=(5, 6, 7, 8))
        kernels = self.config["model"]["bernoulli_probability"]
        for f in range(2):
            for w in range(2):
                conditional = joint_fwy[f, w] / joint_fwy[f, w].sum()
                expected = np.einsum(
                    "a,b,c->abc",
                    [1 - kernels["Y1"][f], kernels["Y1"][f]],
                    [1 - kernels["Y2"][f], kernels["Y2"][f]],
                    [1 - kernels["Y3"][f], kernels["Y3"][f]],
                )
                np.testing.assert_allclose(conditional, expected, atol=1e-14, rtol=0)

    def test_population_response_calibration_is_global_not_within_w(self) -> None:
        calibration = self.report["checks"]["response_calibration"]
        np.testing.assert_allclose(calibration["item_rates"], [1, 0.70, 0.70], atol=1e-14, rtol=0)
        self.assertAlmostEqual(calibration["mean_all_items"], 0.80)
        for block in self.report["pairs"]:
            self.assertGreater(abs(block["response_rates_given_w"][0] - 0.7), 0.01)

    def test_selection_exclusion_and_both_operators_in_every_w_stratum(self) -> None:
        self.assertEqual(len(self.report["pairs"]), 2)
        for block in self.report["pairs"]:
            self.assertLess(block["selection_exclusion_error"], 1e-14)
            self.assertLess(block["selection_equation_error"], 1e-14)
            self.assertLess(block["pair_law_recovery_error"], 1e-14)
            self.assertGreater(block["minimum_pair_w_mass"], 0)
            self.assertGreater(block["minimum_instrument_w_mass"], 0)
            self.assertEqual([entry["w"] for entry in block["operators"]], [0, 1])
            for entry in block["operators"]:
                self.assertLess(entry["inverse_bridge_moment_error"], 1e-14)
                for name in ("bridge_design", "complete_case"):
                    matrix = np.asarray(entry[name]["matrix"])
                    self.assertEqual(matrix.shape, (4, 4))
                    self.assertEqual(entry[name]["rank"], 4)
                    self.assertTrue(((matrix > 0) & (matrix < 1)).all())
                np.testing.assert_allclose(np.asarray(entry["complete_case"]["matrix"]).sum(axis=1), 1)
                self.assertTrue((np.asarray(entry["bridge_design"]["matrix"]).sum(axis=1) < 1).all())

    def test_anchor_and_extension_recover_in_shared_labels(self) -> None:
        latent = self.report["latent"]
        self.assertEqual(latent["anchor_kruskal_sum"], 6)
        self.assertEqual(latent["extension_kruskal_sum"], 6)
        self.assertEqual(latent["shared_khatri_rao"]["rank"], 2)
        self.assertEqual(latent["weighted_inversion"]["rank"], 2)
        recovered = latent["recovery"]
        self.assertTrue(recovered["passed"])
        np.testing.assert_allclose(recovered["class_probability"], [0.55, 0.45], atol=1e-13, rtol=0)
        for name, truth in self.config["model"]["bernoulli_probability"].items():
            np.testing.assert_allclose(recovered["bernoulli_probability"][name], truth, atol=1e-13, rtol=0)
        expected_posterior = np.asarray([[0.55 * 0.8, 0.45 * 0.2], [0.55 * 0.2, 0.45 * 0.8]])
        expected_posterior /= expected_posterior.sum(axis=1, keepdims=True)
        np.testing.assert_allclose(recovered["class_probability_given_w"], expected_posterior, atol=1e-13, rtol=0)

    def test_common_class_permutation_has_same_population_and_canonical_recovery(self) -> None:
        changed = deepcopy(self.config)
        changed["model"]["class_probability"].reverse()
        for kernel in changed["model"]["bernoulli_probability"].values():
            kernel.reverse()
        report = validation.validate_dgp(changed)
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["latent"]["recovery"]["configured_class_order"], [1, 0])
        for name, probability in self.report["latent"]["recovery"]["bernoulli_probability"].items():
            np.testing.assert_allclose(
                report["latent"]["recovery"]["bernoulli_probability"][name], probability, atol=1e-13, rtol=0,
            )
        original = validation.enumerate_population(self.config).joint.sum(axis=0)
        permuted = validation.enumerate_population(changed).joint.sum(axis=0)
        np.testing.assert_allclose(original, permuted, atol=1e-15, rtol=0)

    def test_configured_target_and_supported_pair_order_are_used(self) -> None:
        changed = deepcopy(self.config)
        changed["missingness"]["target_average_item_observation_rate"] = 0.75
        changed["supported_pairs"].reverse()
        report = validation.validate_dgp(changed)
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["pairs"][0]["pair"], ["Y1", "Y3"])
        np.testing.assert_allclose(
            report["checks"]["response_calibration"]["item_rates"], [1, 0.625, 0.625], atol=1e-14, rtol=0,
        )

    def test_extension_needs_shared_inversion_not_its_own_kruskal_bound(self) -> None:
        changed = deepcopy(self.config)
        changed["model"]["bernoulli_probability"]["Y3"] = [0.4, 0.4]
        report = validation.validate_dgp(changed)
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["latent"]["extension_kruskal_sum"], 5)
        np.testing.assert_allclose(report["latent"]["recovery"]["bernoulli_probability"]["Y3"], [0.4, 0.4])

    def test_class_only_shadows_restore_strong_exclusion_but_rank_is_at_most_two(self) -> None:
        diagnostic = validation.class_only_shadow_diagnostic(self.config)
        self.assertTrue(diagnostic["old_strong_y_z_exclusion"]["holds"])
        self.assertTrue(diagnostic["rank_at_most_two"])
        self.assertEqual(diagnostic["maximum_complete_case_rank"], 2)
        self.assertFalse(diagnostic["passes_rank_four"])
        for block in diagnostic["pairs"]:
            self.assertLess(block["selection_exclusion_error"], 1e-14)
            for entry in block["operators"]:
                self.assertEqual(entry["complete_case"]["rank"], 2)
                self.assertEqual(entry["bridge_design"]["rank"], 2)

    def test_rank_deficient_shadow_fails_without_being_misclassified_as_invalid_probability(self) -> None:
        changed = deepcopy(self.config)
        changed["shadow"]["probability_given_pair_cell"] = [[0.25] * 4 for _ in range(4)]
        report = validation.validate_dgp(changed)
        self.assertFalse(report["passed"])
        self.assertTrue(report["checks"]["configuration"]["passed"])
        self.assertIn("shadow_kernel_rank", report["failed_checks"])
        self.assertIn("complete_case_rank_each_w", report["failed_checks"])
        for block in report["pairs"]:
            for entry in block["operators"]:
                self.assertEqual(entry["complete_case"]["rank"], 1)

    def test_degenerate_anchor_and_inversion_ranks_fail(self) -> None:
        for names in (("W",), ("Y1",), ("W", "Y1")):
            with self.subTest(names=names):
                changed = deepcopy(self.config)
                for name in names:
                    changed["model"]["bernoulli_probability"][name] = [0.5, 0.5]
                report = validation.validate_dgp(changed)
                self.assertFalse(report["passed"])
                self.assertIn("anchor_kruskal", report["failed_checks"])
                self.assertIn("shared_label_recovery", report["failed_checks"])
                if len(names) == 2:
                    self.assertIn("extension_inversion_rank", report["failed_checks"])

    def test_bad_parameter_shapes_ranges_and_nonfinite_values_fail(self) -> None:
        cases = [
            (("model", "latent_classes"), 3),
            (("model", "class_probability"), [1.0, 0.0]),
            (("model", "class_probability"), [0.55, 0.40]),
            (("model", "class_probability"), [0.55, 0.45, 0.0]),
            (("model", "bernoulli_probability", "W"), [0, 0.8]),
            (("model", "bernoulli_probability", "Y1"), [-0.1, 0.8]),
            (("model", "bernoulli_probability", "Y2"), [0.2, float("nan")]),
            (("model", "bernoulli_probability", "Y3"), [0.2]),
            (("model", "state_cardinality"), [2, 2, 2, 3]),
            (("model", "observed_features"), ["Y1", "Y2", "Y3"]),
            (("shadow", "categories"), 3),
            (("shadow", "probability_given_pair_cell"), [[0.25] * 4] * 3),
            (("shadow", "probability_given_pair_cell"), [[0.2] * 4] * 4),
            (("shadow", "probability_given_pair_cell"), [[1, 0, 0, 0]] * 4),
            (("shadow", "probability_given_pair_cell"), [[0.25], [0.25, 0.75]]),
            (("supported_pairs",), [[0, 1], [0, 1]]),
            (("supported_pairs",), [[1, 0], [0, 2]]),
            (("missingness", "always_observed_anchor"), "Y2"),
            (("missingness", "target_average_item_observation_rate"), 1 / 3),
            (("missingness", "target_average_item_observation_rate"), 1.0),
            (("missingness", "target_average_item_observation_rate"), float("inf")),
            (("missingness", "selection_coefficients", "Yj"), float("nan")),
            (("missingness", "selection_coefficients", "Y1"), "not numeric"),
        ]
        for path, value in cases:
            with self.subTest(path=path, value=value):
                changed = deepcopy(self.config)
                parent = changed
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                report = validation.validate_dgp(changed)
                self.assertFalse(report["passed"])
                self.assertEqual(report["failed_checks"], ["configuration"])
                json.dumps(report, allow_nan=False)
                with self.assertRaises(ValueError):
                    validation.enumerate_population(changed)
        for malformed in (None, [], {}, {"model": None}):
            self.assertFalse(validation.validate_dgp(malformed)["passed"])

    def test_class_only_shadow_requires_valid_two_by_four_kernel(self) -> None:
        for kernel in ([[0.25] * 4], [[0.2] * 4] * 2, [[1, 0, 0, 0]] * 2):
            with self.subTest(kernel=kernel), self.assertRaises(ValueError):
                validation.class_only_shadow_diagnostic(self.config, kernel)

    def test_extreme_selection_parameters_cannot_silently_pass_calibration(self) -> None:
        changed = deepcopy(self.config)
        changed["missingness"]["selection_coefficients"]["Y1"] = 1000
        report = validation.validate_dgp(changed)
        self.assertFalse(report["passed"])
        self.assertFalse(report["checks"]["positive_pair_propensities"]["passed"])
        json.dumps(report, allow_nan=False)

    def test_population_equations_match_simulator_on_deterministic_support_grid(self) -> None:
        # A stub supplies every (F,W,Y) state; no sampling or frequency estimates.
        cells = np.indices((2,) * 5).reshape(5, -1).T
        config = deepcopy(self.config)
        config["sample_size"] = len(cells)
        rng = mock.Mock()
        rng.choice.return_value = cells[:, 0]
        rng.binomial.side_effect = [cells[:, 1], cells[:, 2:5]]
        rng.uniform.side_effect = lambda size: np.full(size, 0.5)
        dataset = simulate_allman_dataset(config, rng)
        self.assertEqual(rng.choice.call_count, 1)
        self.assertEqual(rng.choice.call_args.args, (2,))
        self.assertEqual(rng.choice.call_args.kwargs["size"], len(cells))
        np.testing.assert_array_equal(rng.choice.call_args.kwargs["p"], config["model"]["class_probability"])
        kernels = config["model"]["bernoulli_probability"]
        np.testing.assert_array_equal(
            rng.binomial.call_args_list[0].args[1], np.asarray(kernels["W"])[cells[:, 0]],
        )
        y_probability = np.asarray([kernels[name] for name in ("Y1", "Y2", "Y3")])
        np.testing.assert_array_equal(rng.binomial.call_args_list[1].args[1], y_probability[:, cells[:, 0]].T)
        population = validation.enumerate_population(config)
        np.testing.assert_allclose(dataset["selection_parameter_true"][:, 0], population.intercepts, atol=1e-14, rtol=0)
        shadow = np.asarray(config["shadow"]["probability_given_pair_cell"])
        for block, pair in enumerate(config["supported_pairs"]):
            cell = 2 * cells[:, 2 + pair[0]] + cells[:, 2 + pair[1]]
            np.testing.assert_allclose(
                dataset["pair_propensity_true"][:, block], population.propensities[block, cell], atol=1e-14, rtol=0,
            )
            np.testing.assert_array_equal(dataset["shadows"][:, block], (0.5 > shadow[cell].cumsum(axis=1)).sum(axis=1))

    def test_report_is_deterministic_and_ignores_sampling_and_estimator_settings(self) -> None:
        changed = deepcopy(self.config)
        for name in ("seed", "sample_size", "replications", "estimation", "inference"):
            changed.pop(name)
        with mock.patch.object(np.random, "default_rng", side_effect=AssertionError("no sampling")):
            self.assertEqual(validation.validate_dgp(changed), self.report)

    def test_cli_prints_json_and_uses_config_option_and_exit_status(self) -> None:
        for arguments, config, expected in (([], self.config, 0), (["--config", "custom.json"], {}, 1)):
            stream = StringIO()
            with mock.patch.object(validation, "load_config", return_value=config) as loader, redirect_stdout(stream):
                status = validation.main(arguments)
            self.assertEqual(status, expected)
            report = json.loads(stream.getvalue())
            self.assertEqual(report["passed"], expected == 0)
            self.assertEqual(
                str(loader.call_args.args[0]), str(validation.DEFAULT_CONFIG) if not arguments else "custom.json",
            )
        for error in (OSError("missing configuration"), ValueError("invalid JSON")):
            stream = StringIO()
            with mock.patch.object(validation, "load_config", side_effect=error), redirect_stdout(stream):
                self.assertEqual(validation.main(["--config", "missing.json"]), 1)
            self.assertFalse(json.loads(stream.getvalue())["passed"])


if __name__ == "__main__":
    main()
