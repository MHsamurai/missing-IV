# Model DAG and Simulation Alignment

Status: resolved on 2026-09-07 by the approved revision of Assumption 4.
The measurement restriction is now
`P(Y | F,W,X) = product_j Q_j(Y_j | F,X)`, with Z marginalized.
The DGP, configuration, estimator, and stored Monte Carlo results are unchanged.
The original finding below is retained as a record of why the assumption and
diagrams had to change, not as a description of the current manuscript.

## Current model and validation

- Keep joint local independence across **all** items and W's measurement exclusion.
  Pairwise independence alone would not justify the full-joint-law conclusion.
- Do not impose `Y independent of Z given (F,W,X)`. Retain the separate restriction
  `R_S independent of Z_S given (Y_S,U_S)` and complete-case completeness.
- Proposition 2.1 only uses Assumptions 1 and 5--7 plus inverse-propensity L2
  integrability. Assumption 3.1 now explicitly inherits all of these premises.
- Stage-2 Step 2 uses the marginal product law to factor the three views
  `(Y_a,Y_b,W)` given F and X; Steps 3--8 and their conclusions are unchanged.
- Figure 1 now shows two separately marginalized models. Figure 2 shows full-data
  marginals over manifest variables, with F marginalized. Blocks are marginals
  of the same underlying law and are not asserted to be independent.
- The simulation diagram shows its actual generation scheme `F -> (W,Y)` and
  `Y_S -> (Z_S,R_S)`. This is a particular DGP, not a complete characterization
  of the theorem's model class.

Reproduce the population validation with:

```sh
simulation/.venv/bin/python -m simulation.dgp_validation
simulation/.venv/bin/python -m unittest simulation.test_dgp_validation simulation.test_latent_mnar_sim
```

All 13 population checks and 21 tests (18 new, 3 existing) pass. Finite-support
enumeration uses 2,048 population cells and tolerance 1e-10, with no Monte Carlo.

| Check | Result |
|---|---|
| Marginal product measurement and W exclusion | Maximum error 1.11e-16 |
| Missing-IV exclusion in both pairs, conditional on W | Maximum error 2.22e-16 |
| Pair propensities | Minimum 0.37147; maximum 0.88595 |
| Item response probabilities | 1.00, 0.70, 0.70; overall mean 0.80 |
| Complete-case operator, each pair and each W stratum | Rank 4 in all four cases |
| Anchor Kruskal-rank sum | 6 = 2r+2 |
| Shared Khatri--Rao / extension inversion | Rank 2 |
| Recovered measurement kernels under common labels | Maximum error 6.66e-16 |
| Recovered class probabilities | Maximum error 0 to floating-point precision |
| Negative control: class-only shadow | Strong exclusion holds, but operator rank 2 |

These checks establish the specified DGP's finite-support identification
conditions. They do not prove regularity of the finite-sample optimizer,
Assumption 5.1 in its entirety, or new bias/coverage results. No new Monte Carlo
run is needed to retain the existing numerical results because the DGP did not change.

## Original Model Diagram (Historical Finding)

Before this revision, `notes/figures/latent_mnar_dag.tex`, also used on Beamer p17, had edges
`Z_S -> F`, `U_S -> F`, `U_S -> Z_S`, `U_S -> Y_S`, `F -> Y_S`,
and `Y_S -> R_S`. At fixed X, its factorization imposes
`Y_S independent of Z_S given (F,W)`.
This was also part of Assumption 4 in
`notes/vector_missing_iv_identification_working.tex`.

The prior p25 revision preserved those edges and annotated the outcome and latent
parameters. It is explicitly a model diagram, not a claim that the current
simulation factors according to that graph.

## Implemented simulation

`simulate_allman_dataset` in `simulation/latent_mnar_sim.py` draws the class,
then W and the Y items conditionally on the class, then draws each Z_S
conditionally on its Y pair using the matrix H in `simulation/config.yml`.
For example, `P(Z_S=0 | Y_S=00)=0.70`, whereas
`P(Z_S=0 | Y_S=10)=0.05`, including after conditioning on F and W.
All pair cells have positive probability. Thus the **old strong** measurement exclusion fails.

The implemented selection equation depends only on the pair outcomes and
does satisfy the Missing IV exclusion `R_S independent of Z_S given (Y_S,W)`.
The product-mixture representation of (W,Y) also remains valid after
marginalizing Z. These facts do not establish the stronger measurement
exclusion imposed by the original diagram.

## Rank obstruction

Under the original diagram, a pair with four positive-probability cells and
two latent classes has a 4-by-2 measurement matrix M_S. For fixed W,
the columns of `P(Y_S | Z_S,W)` are mixtures of those two columns.
Their rank is therefore at most 2. Positive selection multiplies rows by
the pair propensities and normalizes columns, so
`P(Y_S | Z_S,W,R_S=1)` still has rank at most 2.

Consequently the original finite two-class diagram cannot satisfy
unrestricted four-cell complete-case completeness. The configured H is
full rank 4, and the current simulation instead supplies a rank-4 observed
operator. Reversing only the arrows cannot reconcile these conditions.

## Original Follow-up Boundary (Now Resolved)

A separate theoretical decision was needed about the measurement exclusion
and the function class on which completeness is required. Only after that
decision can the model, numerical DGP, and theorem verification be aligned.
The current revision takes the weaker marginal-model route described above;
it does not claim to satisfy all assumptions of the original strong model.

## Review

The independent reviewer confirmed the conditional-independence conflict
and rank obstruction by inspecting the code and enumerating the configured
population distribution. Evaluation checks retained bias, empirical SD,
mean estimated SE, pointwise Wald coverage, and the distinction between
direct Stage-1 IPW and model-implied outcome laws. Measurement-kernel RMSE
is pooled over replications and item-by-class cells, not a mean of cell RMSEs.
