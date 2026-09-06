# Allman latent-class MNAR simulation

The simulation uses only the finite latent-class model of Allman, Matias and
Rhodes (2009, Sections 3-5). For latent class `F` and observed finite-state
features `(W, Y1, Y2, Y3)`, the complete-data distribution is

```text
P = sum_f pi_f (p_fW tensor p_f1 tensor p_f2 tensor p_f3).
```

Allman et al. provide the model class and identification conditions, but no
Monte Carlo DGP, numerical parameter values, estimator, bias table, or coverage
table. The probabilities in `config.yml` are therefore explicitly study-specific
interior calibration values, not values copied from that paper.

The comparison uses five estimators:

1. `full_data_oracle`: the Allman model fitted before missingness.
2. `mar`: observed-data FIML using every observed item under ignorability.
3. `selection_likelihood_correct`: the likelihood for `(W, Y_obs, R)` with the
   correctly specified main effects and `Y1 * Yj` interaction; it marginalizes
   over latent classes and missing items and deliberately does not use `Z`.
4. `selection_likelihood_misspecified`: the same joint likelihood with the
   `Y1` main effect and interaction omitted from the selection index while
   retaining MNAR dependence on the missing `Yj`.
5. `proposed_saturated_bridge`: a ridge-regularized, constrained inverse bridge
   with one parameter for each binary pair-outcome cell, estimated from the
   conditional bridge moments and followed by bridge-weighted latent-model
   fitting.

The two selection-likelihood methods integrate over both the latent class and
the missing item values. The saturated bridge does not posit a parametric link
for the selection probability. Its robustness comparison is therefore about
parametric selection-model misspecification; it still requires the shadow-IV
exclusion, positivity, B-completeness, and the finite latent-class model.
The selection IRLS uses a `1e-6` ridge only as numerical stabilization.

Primary outputs are bias and RMSE for the measurement kernels `M_j` and for the
latent class proportion `p_f`. The replication-level output retains each
`M_jf`, the selection coefficients, convergence status, and objective value;
the summary also reports Monte Carlo standard errors for bias and RMSE.

Observed-law inference is separated from latent decomposition. The headline
results report parameter-specific bias, empirical Monte Carlo standard
deviation, mean estimated standard error, and pointwise 95% Wald coverage for
the population marginals `P(Y2=1)` and `P(Y3=1)` and for every cell of the
supported pairs `(Y1,Y2)` and `(Y1,Y3)`. The first four methods use the laws
implied by their fitted models. The proposed observed-law estimator is the
direct normalized-IPW Stage-1 bridge, before latent decomposition.

Likelihood-based standard errors use a delta-method sandwich covariance based
on the observed likelihood. Proposed Stage-1 standard errors use 200
individual-level nonparametric bootstrap samples per Monte Carlo replication;
each bootstrap sample re-estimates both bridges. The complete eight-cell law
`P(Y1,Y2,Y3)` remains a supporting Stage-2 diagnostic because the two missing
items need not be observed together. These outputs distinguish population
marginal recovery, direct supported-block recovery, and full joint-law recovery
after latent decomposition.

## Run

```bash
uv venv simulation/.venv
uv pip install --python simulation/.venv/bin/python -r simulation/requirements.txt
simulation/.venv/bin/python -m jupyter nbconvert --execute --to notebook \
  --inplace simulation/allman_latent_mnar_simulation.ipynb
```

## Test

```bash
simulation/.venv/bin/python -m unittest simulation.test_latent_mnar_sim
```
