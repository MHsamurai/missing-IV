"""Deterministic checks for the observed-law inference helpers."""

from __future__ import annotations

import unittest

import numpy as np

from simulation.latent_mnar_sim import (
    _finite_difference_hessian,
    _observed_law_target_from_components,
    _pack_likelihood_parameters,
    _pair_cell_probability,
    _population_y_probability,
    _unpack_likelihood_parameters,
    load_config,
)


class ObservedLawInferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config("simulation/config.yml")
        model = cls.config["model"]
        cls.measurement = np.asarray(
            [
                model["bernoulli_probability"][name]
                for name in ("Y1", "Y2", "Y3")
            ],
            dtype=float,
        )
        cls.class_probability = np.asarray(model["class_probability"], dtype=float)
        cls.w_kernel = np.asarray(model["bernoulli_probability"]["W"], dtype=float)

    def test_parameter_transforms_round_trip(self) -> None:
        selection_shape = {
            "full_data_oracle": None,
            "mar": None,
            "selection_likelihood_correct": (2, 4),
            "selection_likelihood_misspecified": (2, 2),
        }
        for method, shape in selection_shape.items():
            selection_parameter = None if shape is None else np.arange(np.prod(shape)).reshape(shape) / 10
            fit = {
                "measurement": self.measurement,
                "w_kernel": self.w_kernel,
                "class_probability": self.class_probability,
                "selection_parameter": selection_parameter,
            }
            packed = _pack_likelihood_parameters(fit, method)
            measurement, w_kernel, class_probability, selection = (
                _unpack_likelihood_parameters(packed, method)
            )
            np.testing.assert_allclose(measurement, self.measurement)
            np.testing.assert_allclose(w_kernel, self.w_kernel)
            np.testing.assert_allclose(class_probability, self.class_probability)
            if selection_parameter is None:
                self.assertIsNone(selection)
            else:
                np.testing.assert_allclose(selection, selection_parameter)

    def test_block_cells_and_marginals_are_consistent(self) -> None:
        target = _observed_law_target_from_components(
            self.measurement, self.class_probability, self.config
        )
        population_marginal = _population_y_probability(self.config)
        np.testing.assert_allclose(target[:2], population_marginal[1:])
        for block, pair in enumerate(self.config["supported_pairs"]):
            cells = target[2 + 4 * block : 6 + 4 * block]
            np.testing.assert_allclose(cells, _pair_cell_probability(self.config, pair[1]))
            self.assertAlmostEqual(float(cells.sum()), 1.0)
            self.assertAlmostEqual(float(cells[1] + cells[3]), target[block])

    def test_finite_difference_hessian_is_step_stable_on_quadratic(self) -> None:
        matrix = np.asarray([[3.0, 0.4, -0.2], [0.4, 2.0, 0.1], [-0.2, 0.1, 1.5]])
        center = np.asarray([0.3, -0.8, 1.2])

        def quadratic(value: np.ndarray) -> float:
            return float(0.5 * value @ matrix @ value)

        coarse = _finite_difference_hessian(quadratic, center, 1e-4)
        fine = _finite_difference_hessian(quadratic, center, 5e-5)
        np.testing.assert_allclose(coarse, matrix, atol=2e-7)
        np.testing.assert_allclose(fine, matrix, atol=5e-7)
        np.testing.assert_allclose(coarse, fine, atol=5e-7)


if __name__ == "__main__":
    unittest.main()
