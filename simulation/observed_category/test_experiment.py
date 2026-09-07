import unittest
import numpy as np
from scipy.special import logit
from scipy.optimize._numdiff import approx_derivative
import experiment as e


class CandidateTests(unittest.TestCase):
    def test_population_tensor_recovery(self):
        for mechanism in ['MCAR', 'MAR', 'MNAR']:
            rows = e.population_checks(e.config(), mechanism)
            self.assertTrue(all(r['rank'] == 2 for r in rows))

    def test_gradient(self):
        rng = np.random.default_rng(39)
        for method, n in [('oracle', 10), ('MAR_ignorability', 10),
                          ('selection_misspecified', 14), ('candidate_saturated', 18)]:
            theta = rng.normal(size=n)
            counts = rng.integers(0, 20, 72)
            analytic = e.objective(theta, counts, method)[1]
            numerical = approx_derivative(lambda t: e.objective(t, counts, method)[0], theta).ravel()
            np.testing.assert_allclose(analytic, numerical, atol=1e-7)

    def test_dgp_and_observed_likelihood(self):
        c = e.config()
        c['sample_size'] = 300000
        counts, _, _, rate, _ = e.sample(c, 'MNAR', np.random.default_rng(54))
        m, lam, pi = e.truth(c, 'MNAR')
        theta = np.r_[logit(m.ravel()), logit(lam), logit(pi.ravel())]
        p, _ = e.probability_score(theta, 'candidate_saturated')
        expected = p*np.array(c['v_probability'])[e.V]
        self.assertLess(np.max(np.abs(counts/counts.sum()-expected)), .002)
        self.assertAlmostEqual(rate, .8, places=2)

    def test_population_fit(self):
        c = e.config()
        m, lam, pi = e.truth(c, 'MNAR')
        theta = np.r_[logit(m.ravel()), logit(lam), logit(pi.ravel())]
        pv = np.array(c['v_probability'])
        p, _ = e.probability_score(theta, 'candidate_saturated')
        result, _ = e.fit(100000*p*pv[e.V], 'candidate_saturated', np.random.default_rng(67), starts=4)
        np.testing.assert_allclose(e.targets(result.x, 'candidate_saturated', pv),
                                   e.targets(theta, 'candidate_saturated', pv), atol=2e-4)

    def test_saturated_logistic_equivalence(self):
        _, _, pi = e.truth(e.config(), 'MNAR')
        design = np.array([[1, a, y, a*y] for a in range(2) for y in range(2)])
        for j in range(2):
            beta = np.linalg.solve(design, logit(pi[j].ravel()))
            np.testing.assert_allclose(e.expit(design @ beta), pi[j].ravel())

    def test_rank_negative_controls(self):
        c = e.config()
        pv = np.array(c['v_probability'])
        constant_lambda = np.full(4, .45)
        g = np.column_stack([pv*(1-constant_lambda)/.55, pv*constant_lambda/.45])
        self.assertEqual(np.linalg.matrix_rank(g), 1)
        _, _, pi = e.truth(c, 'MNAR')
        identical_measurement = np.array([.4, .4])
        k = np.vstack([(1-identical_measurement)*pi[0, 0, 0],
                       identical_measurement*pi[0, 0, 1],
                       1-(1-identical_measurement)*pi[0, 0, 0]-identical_measurement*pi[0, 0, 1]])
        self.assertEqual(np.linalg.matrix_rank(k), 1)

    def test_common_complete_data(self):
        c = e.config()
        samples = [e.sample(c, mechanism, np.random.default_rng(43)) for mechanism in c['mechanisms']]
        for other in samples[1:]:
            np.testing.assert_array_equal(samples[0][1], other[1])
            np.testing.assert_array_equal(samples[0][2], other[2])


if __name__ == '__main__':
    unittest.main()
