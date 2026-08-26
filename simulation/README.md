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

Primary outputs are bias and RMSE for the measurement kernels `M_j` and for the
latent class proportion `p_f`.

## Run

```bash
uv venv simulation/.venv
uv pip install --python simulation/.venv/bin/python -r simulation/requirements.txt
simulation/.venv/bin/python -m jupyter nbconvert --execute --to notebook \
  --inplace simulation/allman_latent_mnar_simulation.ipynb
```
