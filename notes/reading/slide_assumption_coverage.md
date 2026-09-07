# Slide Assumption Coverage

Updated 2026-09-07. Source: `notes/vector_missing_iv_identification_working.tex`.
Slide numbers refer to the 46-page English Beamer deck. The Japanese Word script
has one matching section per slide. The Japanese title and English subtitle are unchanged.

| Manuscript condition | Slide | Coverage |
|---|---:|---|
| Assumption 1 | 9 | Item response indicators; always-observed X,W,Z,D; latent F; O and Y_D defined |
| Assumption 2 | 10 | F given W,X; Q_F defined with Z marginalized |
| Assumption 3 | 10 | Item kernels Q_j and parameters theta_j |
| Assumption 4 | 11 | Joint product law after marginalizing Z; W excluded from measurement; no Y-Z exclusion given F,W,X |
| Assumption 5 | 13 | S,Y_S,U_S,R_S; block observation process; positivity on target support |
| Assumption 6 | 16 | Blockwise Missing IV conditional on Y_S,U_S |
| Assumption 7 | 16 | Complete-case L2 function class, injectivity, almost-sure domain |
| Proposition 2.1 side conditions | 17 | True and candidate inverse propensities in the stated L2 class; integrable targets |
| Finite model domains / Assumption 3.1 | 22 | Known r>=2; finite item and W supports; common full-probability X set; positive class/W probabilities |
| Assumption 3.1 first-stage inheritance | 22 | Assumptions 1,2--4,5--7; every required anchor/extension pair and W value; inverse-L2 condition |
| Assumption 3.1 rank / label constraints | 23 | Kruskal sum; known score and score expectation; same strict ordering across X |
| Lemma 3.1 premise | 24 | r nonzero columns of A,B, with column Kruskal ranks; Khatri--Rao bound |
| Proposition 4.1 side conditions | 28 | Correct latent specification; positive density on common support; true bridge; fixed positive block weights |
| Assumption 5.1 sampling / parameterization | 29 | I.i.d. individuals; finite-dimensional correctly specified parameters; free simplex coordinates; compact spaces, interior truth |
| Assumption 5.1 local regularity | 29 | Unique first-stage moment zero; C2 criterion/moments; L2 envelopes; nonsingular Jacobians and Godambe matrix |
| Assumption 5.1 global consistency conditions | 30 | Uniform convergence of plug-in criterion; separated population maximum |
| Assumption 5.1 first-stage estimator | 31 | Regular asymptotic linearity; mean-zero finite-variance influence function |
| Assumption 5.1 quantitative separation | 31 | Positive class/response probabilities; smallest nonzero singular value of named W-mode unfolding; Kruskal minors; ordering gaps |
| Theorem 5.1 scope and inference | 32 | Finite-dimensional bridge; first-stage contribution to sandwich; full bootstrap re-estimation; no unsupported growing-sieve claim |
| Simulation-specific restrictions | 34,46 | Fixed X, two classes, binary outcomes; Z from pair law; extra DGP response independence; numeric calibration |

## Dependency Review

- The independent reviewer confirmed that weakening Assumption 4 does not change
  the Stage-1 proof or the three-view Stage-2 decomposition.
- Proposition 2.1's inverse-L2 premise is explicitly inherited by Assumption 3.1.
- The general Khatri--Rao lemma now states its nonzero-column premise; the latent
  probability columns already satisfy it.
- Assumption 5.1 now states the global uniform convergence and separation used by
  its consistency proof. The singular-value condition names the W-mode unfolding
  and its smallest nonzero singular value, not an undefined tensor singular value.
- Figures distinguish marginal models from the full joint DGP. Their arrows do
  not introduce additional latent-shadow exclusion or independence across blocks.
- The continuous-factor footnote is a limitation, not an additional assumption
  of the finite-class theorem. It is summarized in the scope discussion rather
  than presented as a sufficient continuous-factor identification condition.

## Validation

The exact-population DGP checks and negative controls are documented in
`simulation_dag_alignment_check.md`. They validate model/rank restrictions, not
all estimator regularity conditions. Stored simulation results remain unchanged.

- Both `make -B working-paper` and `make -B beamer` succeed: 11 manuscript pages
  and 46 slides. No overfull boxes or undefined references remain in the logs.
- All PDF pages and all 13 rendered Japanese Word pages were visually checked.
  The supported-block set diagram now uses the anchor pair `{a,b}` and extension
  pair `{j,a}`; the diagram footer and vertical ellipsis are clear of block borders.
- Extracted PDF headings match the Word script's 46 sections in order.
- The independent source review confirmed complete numbered-assumption coverage
  and the mathematical changes; the final diagram-border issue was corrected
  and re-rendered before delivery.
