# AGENTS.md

## Project

This repository contains a LaTeX paper on identification of nonignorable missingness using missing IV / shadow variables and latent variable modeling.

## Core editing policy

- Do not delete existing theoretical content unless explicitly instructed.
- Prefer reorganizing, relabeling, and moving material to appendices over removing it.
- Preserve rigorous assumptions, propositions, theorems, proofs, remarks, and appendix discussions from the existing TeX draft.
- If a section seems redundant, mark it for review or move it to an appendix rather than deleting it.
- Keep notation internally consistent. If notation is changed, update all dependent assumptions, theorem statements, proofs, figure captions, and references.

## Main theoretical focus

- The main paper should focus on the IV-type approach:
  $$
  F = g(V) + U.
  $$
- The proxy-type approach:
  $$
  V = g(F) + U
  $$
  should not be deleted. It should be kept as supplementary appendix material unless explicitly instructed otherwise.
- Do not present the proxy-type approach as the main contribution unless the user explicitly changes the paper direction.

## Vector notation rule

- Use vector notation for the main identification result:
  $$
  \bm Y=(Y_1,\ldots,Y_K)'.
  $$
- Treat d'Haultfoeuille's scalar outcome as extended to a vector-valued outcome.
- Replace scalar-by-scalar statements involving \(Y_j\) with vector statements involving \(\bm Y\) when discussing the main result.
- Allow correlation among \(Y_1,\ldots,Y_K\).
- Do not impose product-form missingness unless it is explicitly introduced as a special case.

## Main shadow variable condition

Use the main shadow condition:
$$
R \perp\!\!\!\perp V \mid \bm Y.
$$

Avoid using the older itemwise condition:
$$
D_j \perp\!\!\!\perp V \mid Y_j
$$
as the main assumption, because it can obscure correlation among \(Y_j\) and dependence among itemwise missingness indicators.

## Missingness model

The main missingness model is:
$$
R=\mathbf 1\{R^*>0\},\qquad R^*=k(\bm Y)+\eta.
$$

The missingness probability is:
$$
\pi(\bm Y)=\Pr(R=1\mid \bm Y).
$$

The key identifying moment is:
$$
\mathbb E\{R w(\bm Y)\mid V\}=1,
\qquad
w(\bm Y)=\frac{1}{\pi(\bm Y)}.
$$

The vector shadow completeness condition is:
$$
\mathbb E\{a(\bm Y)\mid V\}=0
\quad\Longrightarrow\quad
a(\bm Y)=0.
$$

## What is identified

Under the IV-type model and the maintained assumptions, the following objects are identified:

- \(\pi(\bm Y)=\Pr(R=1\mid \bm Y)\)
- \(P(\bm Y,V)\)
- \(\mathbb E(\bm Y)\)
- the latent measurement functions \(h_1,\ldots,h_K\)
- the IV function \(g\)

The latent structure is:
$$
\bm Y=\bm h(F)+\bm\varepsilon,
\qquad
F=g(V)+U.
$$

## Important correction

Do not write:
$$
\mathbb E\left[\frac{R}{P(Y)}\mid Z\right]=1.
$$

The correct expression is:
$$
\mathbb E\left[\frac{R}{\pi(Y)}\mid Z\right]=1,
\qquad
\pi(Y)=\Pr(R=1\mid Y).
$$

In the vector version:
$$
\mathbb E\left[\frac{R}{\pi(\bm Y)}\mid V\right]=1.
$$

## Paper structure

Use a d'Haultfoeuille (2010)-style structure:

1. Introduction
2. Identification
3. Estimation
4. Simulation studies
5. Empirical illustration
6. Conclusion
Appendix A. Proofs
Appendix B. Additional measurement error
Appendix C. Empirical Bayes interpretation and completeness
Appendix D. Missingness depending on the latent factor
Appendix E. Proxy-type approach

## Proof placement

- Put technical proofs in `Appendix A. Proofs`.
- Keep theorem, proposition, lemma, and corollary statements in the main text when they are central.
- Move detailed proofs out of the main text unless they are short and necessary for readability.
- When moving proofs, keep labels and cross-references intact.

## Appendix policy

The following topics should be retained in appendices, not deleted:

- additional measurement error and error aggregation;
- empirical Bayes interpretation and completeness;
- missingness depending on the latent factor \(F\);
- proxy-type approach \(V=g(F)+U\).

## Empirical and simulation sections

If data details are unknown, write the sections as templates using placeholders such as:

- `<data_source_name>`
- `<data_Y_name>`
- `<data_V_name>`
- `<sample_period>`
- `<missing_rate>`
- `<estimation_method_name>`
- `<simulation_design_name>`

Do not invent empirical data details.

## Style

- Write in rigorous academic LaTeX.
- Use precise statistical terminology.
- Avoid overclaiming. Use phrases such as "under the maintained assumptions" and "sufficient conditions" where appropriate.
- Distinguish ordinary causal IV from missing-data IV / shadow variable.
- Keep the main text focused and move exploratory material to appendices.
