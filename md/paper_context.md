# Paper context: Missing IV and latent variable modeling

## Purpose of this file

This file summarizes the current paper state and the decisions made in the ChatGPT discussion, so that Codex can continue editing the LaTeX paper without losing context.

## Working title

欠測IVと潜在変数モデリングによる非無作為欠測の識別

English working title:

Identification of Nonignorable Missingness via Missing Instruments and Latent Variable Modeling

## Authors

Current authors:

- Masahiro Honda
- Takahiro Hoshino
- Taisuke Otsu
  - Department of Economics, London School of Economics
  - Houghton Street, London WC2A 2AE, UK
  - Email: t.otsu@lse.ac.uk
  - URL: http://econ.lse.ac.uk/staff/otsu_taisuke/

## Recent meeting decisions

A meeting with Taisuke Otsu led to two main changes.

### Change 1: Add one author

Add Taisuke Otsu as a coauthor with the LSE affiliation and contact details above.

### Change 2: Replace scalar/itemwise notation with vector notation

The previous draft used \(Y_j\) and itemwise statements such as:
$$
D_j \perp\!\!\!\perp V\mid Y_j.
$$

The revised paper should treat the d'Haultfoeuille outcome \(Y\) as vector-valued:
$$
\bm Y=(Y_1,\ldots,Y_K)'.
$$

The main condition should be:
$$
R \perp\!\!\!\perp V\mid \bm Y.
$$

This is important because the components \(Y_1,\ldots,Y_K\) may be correlated. The paper should not imply that the \(Y_j\) are independent or that the missingness indicators factorize across \(j\), unless explicitly introduced as a special case.

The old product-form expression:
$$
\Pr(D_j=1, j\in S\mid Y_1,Y_2,Y_3,V)
=
\prod_{j\in S}\pi_j(Y_j)
$$
should not be used in the main theory.

## Main research idea

The paper extends d'Haultfoeuille (2010)'s shadow variable / missing IV identification strategy from a scalar missing outcome to a vector-valued missing variable and links it to a latent variable model.

The original d'Haultfoeuille condition is:
$$
R \perp\!\!\!\perp Z\mid Y.
$$

The paper's vector version is:
$$
R \perp\!\!\!\perp V\mid \bm Y.
$$

The novelty is that a single always-observed variable \(V\) may identify the joint distribution of multiple potentially missing variables \(\bm Y\), through a common latent factor.

## Main model

Let:
$$
\bm Y=(Y_1,\ldots,Y_K)'.
$$

Latent measurement model:
$$
\bm Y=\bm h(F)+\bm\varepsilon.
$$

IV-type latent structure:
$$
F=g(V)+U.
$$

Missingness:
$$
R=\mathbf 1\{R^*>0\},
\qquad
R^*=k(\bm Y)+\eta.
$$

Missingness probability:
$$
\pi(\bm y)=\Pr(R=1\mid \bm Y=\bm y).
$$

Observed data:
$$
\mathcal O=\{V,R,R\bm Y,\bm D\},
$$
where \(\bm D=(D_1,\ldots,D_K)'\) can describe itemwise observation patterns and \(R=\prod_jD_j\) denotes a complete-case indicator.

## Assumptions

### Exogeneity

\(V,U,\bm\varepsilon,\eta\) are mutually independent, and:
$$
F=g(V)+U,
\qquad
\bm Y=\bm h(F)+\bm\varepsilon,
\qquad
R^*=k(\bm Y)+\eta.
$$

### Positivity

There exists \(c>0\) such that:
$$
\pi(\bm Y)\ge c
\quad\text{a.s.}
$$

### Vector shadow completeness

For any integrable function \(a:\mathbb R^K\to\mathbb R\):
$$
\mathbb E\{a(\bm Y)\mid V\}=0
\quad\text{a.s.}
\quad\Longrightarrow
a(\bm Y)=0
\quad\text{a.s.}
$$

### Latent measurement identification

The recovered joint distribution \(P(\bm Y,V)\) should identify:
$$
\bm Y=\bm h(F)+\bm\varepsilon,
\qquad
F=g(V)+U
$$
under the chosen normalization.

A convenient normalization is:
$$
h_1(f)=f.
$$

Alternatively, use:
$$
\mathbb E(F)=0,\qquad \operatorname{Var}(F)=1,
$$
and require \(h_1\) to be monotone increasing to resolve sign indeterminacy.

## Key results to preserve

### Current theorem order for the vector d'Haultfoeuille extension

Use the following order when rewriting the identification section in the
d'Haultfoeuille (2010) style. This block uses the local vector JoE-style
notation \(D,\bm Y,\bm Z\). The scalar-\(Z\) case should be presented later
as a rank-based special case, not as the main notation.

1. Theorem 2.1' gives the vector version of Proposition 2.1:
   $$
   \bm Y=\varphi(\bm Z,\bm\varepsilon),\qquad
   \bm D=\psi(\bm Y,\bm\eta),\qquad
   \bm\eta\perp\!\!\!\perp (\bm Z,\bm\varepsilon)
   \quad\Longrightarrow\quad
   \bm D\perp\!\!\!\perp \bm Z\mid \bm Y.
   $$
   This is a one-way implication, matching the original JoE proposition.

2. Main Theorem 2.3' should use vector \(\bm Z\). It should impose
   Assumption 4' as vector \(B_{\bm Y}\)-completeness:
   $$
   \bm Y\text{ is }B_{\bm Y}\text{-complete for }\bm Z,
   $$
   meaning that for every real-valued \(g\in B_{\bm Y}\),
   $$
   \mathbb E\{g(\bm Y)\mid \bm Z\}=0\quad\text{a.s.}
   \quad\Longrightarrow\quad
   g(\bm Y)=0\quad\text{a.s.}
   $$
   Here \(B_{\bm Y}\) is the class of functions such that \(g(\bm Y)\) is
   bounded below almost surely and integrable.

3. Proposition 2.2' gives sufficient conditions for Assumption 4'. First
   prove the case where
   $$
   \bm\nu(\bm Z)
   $$
   has sufficiently rich support in \(\mathbb R^K\). What matters is not only
   \(q=\dim(\bm Z)\), but whether the transformed index \(\bm\nu(\bm Z)\) has
   full \(K\)-dimensional variation.

4. Lemma 2.2.1 records that the finite-support case can be weakened to scalar
   \(Z\). Under:
   - \(Z\) is scalar and \(\bm\nu(Z):\mathbb R\to\mathbb R^K\);
   - scalar \(Z\) and \(\bm Y\) are both discrete with finite supports;
   - the matrix
     $$
     M_{ij}=\Pr(\bm Y=\bm y_i\mid Z=z_j)
     $$
     has full row rank, i.e.,
     \(\operatorname{rank}(M)=|\operatorname{supp}(\bm Y)|\);
   vector \(B_{\bm Y}\)-completeness holds even with scalar \(Z\).

5. The main vector identification theorem should preserve the original
   d'Haultfoeuille Assumption 2 logic: with only the marginal distribution
   \(P(\bm Z)\) identified, Assumptions 1'--5' identify
   \((R,\bm Y,\bm Z)\), where \(R=\mathbf 1\{\bm D=\bm 1\}\). This is enough for
   the paper's main target, namely recovery of the global distribution
   \(P(\bm Y,\bm Z)\) and \(P(\bm Y)\). Write the numerator as an indicator of the
   event \(\bm D=\bm 1\), not as the vector \(\bm D\) divided by a scalar:
   $$
   \pi(\bm y)=\Pr(\bm D=\bm 1\mid \bm Y=\bm y),\qquad
   \mathbb E\left\{
   \frac{\mathbf 1\{\bm D=\bm 1\}}{\pi(\bm Y)}
   \,\middle|\, \bm Z
   \right\}=1.
   $$

6. Do not make identification of the full missingness-pattern distribution
   \((\bm D,\bm Y,\bm Z)\) a main claim. Mention only in a note or remark that full
   pattern identification would require additional pattern-specific information,
   such as \(P(\bm D=\bm d,\bm Z)\) for every pattern \(\bm d\). This is not needed
   for recovering the global distribution of \(\bm Y\).

### Conditional independence

Under the main model:
$$
R \perp\!\!\!\perp V\mid \bm Y.
$$

Reason: \(R\) is a function only of \(\bm Y\) and \(\eta\), and \(\eta\) is independent of \(V\).

### Identification moment

Define:
$$
w(\bm Y)=\frac{1}{\pi(\bm Y)}.
$$

Then:
$$
\mathbb E\{R w(\bm Y)\mid V\}=1.
$$

This is the main inverse-problem equation.

### Uniqueness

If \(w\) and \(\widetilde w\) both solve:
$$
\mathbb E\{R w(\bm Y)\mid V\}=1,
$$
then:
$$
\mathbb E\{\pi(\bm Y)[w(\bm Y)-\widetilde w(\bm Y)]\mid V\}=0.
$$

By vector shadow completeness and positivity:
$$
w(\bm Y)=\widetilde w(\bm Y).
$$

Thus \(\pi(\bm Y)\) is identified.

### Joint distribution recovery

For any bounded measurable function \(\varphi\):
$$
\mathbb E\{\varphi(\bm Y,V)\}
=
\mathbb E\{R w(\bm Y)\varphi(\bm Y,V)\}.
$$

Thus \(P(\bm Y,V)\) and \(\mathbb E(\bm Y)\) are identified.

### Latent function identification

Once \(P(\bm Y,V)\) is recovered, the latent IV model gives:
$$
p(\bm y\mid v)
=
\int
\left\{\prod_{j=1}^Kp_{\varepsilon_j}(y_j-h_j(f))\right\}
p_U\{f-g(v)\}\,df.
$$

Under the latent measurement model identification condition, \(g\) and \(h_1,\ldots,h_K\) are identified.

## Important correction from earlier drafts

A previous draft incorrectly wrote:
$$
\mathbb E\left[\frac{R}{P(Y)}\mid Z\right]=1.
$$

This should be:
$$
\mathbb E\left[\frac{R}{\pi(Y)}\mid Z\right]=1,
\qquad
\pi(Y)=\Pr(R=1\mid Y).
$$

In the vector version:
$$
\mathbb E\left[\frac{R}{\pi(\bm Y)}\mid V\right]=1.
$$

## Paper structure to use

The user wants the paper to follow the structure of d'Haultfoeuille (2010). The current target structure is:

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
References

## Proofs

A major comment was that it was unclear where the proofs were.

Therefore:

- Put all proofs in `Appendix A. Proofs`.
- Main text should contain theorem/proposition/lemma statements but not long proofs.
- Use labels such as:
  - `Proof of Proposition ...`
  - `Proof of Lemma ...`
  - `Proof of Theorem ...`
  - `Proof of Corollary ...`

## What not to delete

Do not casually delete the rigorous content from the previous TeX draft. In particular, preserve:

- the shadow variable definition;
- the explanation that shadow variable is not MAR;
- MCAR/MAR/NI/MNAR distinctions if present;
- NI nonidentification argument using selected density;
- vector shadow completeness;
- the old-to-new correction explaining why itemwise \(Y_j\) notation was replaced by vector \(\bm Y\);
- additional measurement error appendix;
- empirical Bayes / Fourier completeness appendix;
- latent-factor-dependent missingness appendix;
- proxy-type appendix;
- references to d'Haultfoeuille (2010), Zhao and Shao (2015), Wang, Shao and Kim (2014), Shao and Wang (2016), Miao and Tchetgen Tchetgen, and Li, Miao and Tchetgen Tchetgen (2023).

## Proxy-type approach

The proxy-type approach:
$$
V=g(F)+U
$$
was discussed earlier.

Current decision:

- Do not make it the main result.
- Do not delete it.
- Place it in an appendix as supplementary identification discussion.
- State clearly that it requires additional multiple-indicator identification assumptions and is not the main contribution.

Typical proxy-type appendix structure:

$$
\bm Y=\bm h(F)+\bm\varepsilon,
\qquad
V=g(F)+U.
$$

If:
$$
R^*=k(\bm Y)+\eta,
$$
then:
$$
R\perp\!\!\!\perp V\mid \bm Y.
$$

With positivity, vector shadow completeness, and multiple-indicator identification, one may identify:
$$
P(\bm Y,V),\quad \mathbb E(\bm Y),\quad g,\quad h_1,\ldots,h_K.
$$

But this should remain supplementary.

## Missingness depending on latent factor

The paper should distinguish the case:
$$
R^*=k(F)+\eta.
$$

In this case, generally:
$$
R\not\perp\!\!\!\perp V\mid \bm Y.
$$

Reason:
$$
\Pr(R=1\mid \bm Y=\bm y,V=v)
=
\mathbb E\{\rho(F)\mid \bm Y=\bm y,V=v\},
$$
which generally depends on \(v\).

This means the shadow variable proof does not apply. This is important and should remain in an appendix.

## Additional measurement error

If:
$$
Y_j^*=h_j(F)+e_j,
\qquad
Y_j=Y_j^*+Q_j,
$$
and \(e_j\) and \(Q_j\) are independent, then define:
$$
\varepsilon_j=e_j+Q_j.
$$

The model reduces to:
$$
Y_j=h_j(F)+\varepsilon_j.
$$

This should remain as an appendix proposition.

## Empirical Bayes interpretation and completeness

The previous draft included a useful interpretation:

- measurement error corresponds to smoothing / convolution;
- missingness corresponds to truncation / information loss;
- completeness corresponds to the relevant operator having no nontrivial null space.

For the shift model:
$$
F=g(V)+U,
$$
if \(U\) has density \(p_U\), \(U\perp V\), \(g(\mathcal V)=\mathbb R\), and the characteristic function:
$$
\phi_U(t)\ne 0
$$
for all \(t\), then:
$$
\mathbb E\{a(F)\mid V\}=0
\quad\Longrightarrow\quad
a(F)=0.
$$

The proof uses convolution and Fourier transform:
$$
(a*\check p_U)(x)=0
\quad\Rightarrow\quad
\widehat a(t)\overline{\phi_U(t)}=0
\quad\Rightarrow\quad
a=0.
$$

This should remain in the appendix.

## Estimation section

The estimation section should be developed but can remain partly schematic.

Possible contents:

- finite-dimensional sieve approximation for \(w(\bm Y)\);
- conditional moment estimator based on:
  $$
  \mathbb E\{Rw(\bm Y)\mid V\}=1;
  $$
- regularized minimum distance:
  $$
  \widehat w
  \in
  \arg\min_w
  \|\widehat T w -1\|^2+\lambda_n\mathcal J(w);
  $$
- IPW estimator:
  $$
  \widehat\theta_\varphi
  =
  \frac1n\sum_i R_i\widehat w(\bm Y_i)\varphi(\bm Y_i,V_i).
  $$

Do not overclaim asymptotic normality unless proved.

## Simulation section

Simulation can be a template. Use placeholders if details are unknown.

Suggested design:

- Generate \(V\).
- Generate \(F=g(V)+U\).
- Generate \(\bm Y=\bm h(F)+\bm\varepsilon\).
- Generate \(R=1\{k(\bm Y)+\eta>0\}\).
- Compare complete-case, MAR-style imputation/IPW, and proposed shadow-IV estimator.
- Evaluate bias/RMSE for \(\mathbb E(\bm Y)\) and recovery of selected functionals.

## Empirical illustration section

This should be a template for now.

Use placeholders:
- `<data_source_name>`
- `<data_Y_name>`
- `<data_V_name>`
- `<sample_period>`
- `<missing_rate>`
- `<estimation_method_name>`

Do not invent a real dataset.

Potential empirical framing:

- \(V\): leading economic indicator;
- \(F\): latent business-cycle or recession factor;
- \(\bm Y\): multiple firm, market, or macro indicators subject to missingness or selection.

The user mentioned that a pseudo-empirical illustration using full data with artificially introduced NI missingness is acceptable.

## Category / presentation context

The user is preparing a conference submission. The likely categories discussed were:

- 統計調査法・標本調査論
- 統計理論一般
- 因果推論
- 経済・経営統計
- ノンパラメトリック解析
- ベイズ統計

The most natural category from a session-audience perspective is probably:
1. 統計調査法・標本調査論
2. 統計理論一般
3. 因果推論

But if economic/marketing application is emphasized, use:
1. 経済・経営統計
2. 統計調査法・標本調査論
3. 因果推論

## User preference for future edits

The user explicitly said that the previous d'Haultfoeuille-style rewrite improved the structure but deleted too much of the original TeX content. Future edits should preserve content more carefully.

Preferred approach:

- Reorder, relabel, and move material.
- Do not simplify by deleting rigorous content.
- If a block is not central, move it to Appendix.
- Keep the theory explicit and mathematically rigorous.
