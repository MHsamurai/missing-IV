# Latent MNAR simulation

This folder contains the pilot simulation used to choose the main data-generating
process before implementing the full 3 outcome families x 6 estimators design.

## Files

- `config.yml`: all pilot and final-run settings. It is valid YAML and JSON.
- `latent_mnar_sim.py`: DGPs, pairwise latent-class EM, and metrics.
- `latent_mnar_dgp_pilot.ipynb`: executed comparison of the candidate DGPs.
- `requirements.txt`: optional local Jupyter environment.

## Current scope

The pilot compares three diagnostic estimators:

1. `full_data_oracle`
2. `mar_naive`
3. `oracle_bridge`, using the true supported-pair propensities

The remaining three methods are listed in `config.yml` but intentionally marked
as planned. The oracle bridge tests whether the DGP and latent-class fitting are
stable before estimated bridge error is introduced.

The primary outputs are bias and RMSE for the class-specific measurement
parameters representing each `M_j`, and bias and RMSE for `p_f=P(F=1)`.

## Run

```bash
uv venv simulation/.venv
uv pip install --python simulation/.venv/bin/python -r simulation/requirements.txt
simulation/.venv/bin/python -m jupyter nbconvert --execute --to notebook \
  --inplace simulation/latent_mnar_dgp_pilot.ipynb
```
