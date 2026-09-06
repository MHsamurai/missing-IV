# Model DAG and Simulation Alignment

Status: unresolved model/DGP mismatch, identified while revising Beamer p25.
No simulation code, numerical result, or manuscript theorem was changed in this revision.

## Model diagram

`notes/figures/latent_mnar_dag.tex`, also used on Beamer p17, has edges
`Z_S -> F`, `U_S -> F`, `U_S -> Z_S`, `U_S -> Y_S`, `F -> Y_S`,
and `Y_S -> R_S`. At fixed X, its factorization imposes
`Y_S independent of Z_S given (F,W)`.
This is also part of Assumption 4 in
`notes/vector_missing_iv_identification_working.tex`.

The revised p25 preserves those edges and annotates the outcome and latent
parameters. It is explicitly a model diagram, not a claim that the current
simulation factors according to that graph.

## Implemented simulation

`simulate_allman_dataset` in `simulation/latent_mnar_sim.py` draws the class,
then W and the Y items conditionally on the class, then draws each Z_S
conditionally on its Y pair using the matrix H in `simulation/config.yml`.
For example, `P(Z_S=0 | Y_S=00)=0.70`, whereas
`P(Z_S=0 | Y_S=10)=0.05`, including after conditioning on F and W.
All pair cells have positive probability. Thus measurement exclusion fails.

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

## Follow-up boundary

A separate theoretical decision is needed about the measurement exclusion
and the function class on which completeness is required. Only after that
decision can the model, numerical DGP, and theorem verification be aligned.
The present graphs describe the existing numerical benchmark; they must not
be presented as verification of all assumptions of the original model.

## Review

The independent reviewer confirmed the conditional-independence conflict
and rank obstruction by inspecting the code and enumerating the configured
population distribution. Evaluation checks retained bias, empirical SD,
mean estimated SE, pointwise Wald coverage, and the distinction between
direct Stage-1 IPW and model-implied outcome laws. Measurement-kernel RMSE
is pooled over replications and item-by-class cells, not a mean of cell RMSEs.
