# Latent MNAR core reading notes

## 読み方

本ノートは、各論文を次の四点で比較する。

1. 何を観測データから識別または推定するか。
2. 欠測機構と潜在構造へ何を仮定するか。
3. complete case、外部IV、completenessをどのように使うか。
4. 本稿のsupported-block latent-class識別とどこが同じで、どこが異なるか。

ページは誌面ページを優先し、誌面ページがないworking paperではPDFページを記す。

## 1. Latent structure and MNAR

### Kuha, Katsikatsou and Moustaki (2018)

- **対象**: latent trait `eta`、latent response propensity `xi`、item responses、
  response indicatorsを含むjoint model。
- **モデル**: joint lawの分解は式(1), p.1171。measurement modelは式(3), p.1172。
  missingnessは式(6), p.1173、finite latent response classは式(7)--(9),
  pp.1175--1176。
- **識別**: structural/measurement modelがignorable caseで識別されることと、`eta`を
  既知としたlatent response class modelが識別されることを要求する。例示条件は
  `p >= 3` および `C <= 2^p/(1+p)`、p.1176。
- **推定**: observed-data likelihoodの直接最大化、式(10), p.1176。
- **限界**: response propensityをfinite classとlogistic regressionsで規定する。
- **本稿との差**: latent structureとMNARの統合自体は既存である。本稿は外部shadow IVで
  supported-block lawsを先に回復し、その後にfinite latent-class decompositionを行う。

### Kano and Takai (2011)

- **対象**: linear latent variate modelのloadings、error variances、pattern-specific latent
  means/covariances。
- **モデル**: confirmatory factor modelは式(2), p.1242。一般化は式(4), p.1243。
- **仮定**: A1は `Y independent R | z`, p.1242。A2--A3によりmissing patternで条件付けても
  共通loadingsとerror varianceを持つモデルが再生される、式(7)--(8), p.1244。
  A4はpattern-specific latent meansのrank型識別条件、p.1246。
- **識別との関係**: covariance structure parameter `theta`は識別済みであると明示的に
  仮定される、p.1243。A4と式(13)--(14)はMSA内のlatent meansの不定性を除く通常の
  正規化・rank条件であり、MNAR観測法則から測定構造を新たに識別する結果ではない。
- **推定**: partial equality constraintsを持つmulti-sample SEM、式(10)--(12),
  pp.1245--1246。漸近分散は式(21), p.1248。
- **本稿との差**: 識別済みの線形測定構造とmissing-pattern invarianceの下で一致推定を
  構成する研究である。external IVからblock lawと潜在測定構造を識別する研究ではない。

### Holman and Glas (2005)

- **対象**: IRT item parametersとlatent response propensity。
- **モデル**: response indicator modelは式(2), p.3。outcome traitとresponse propensityのjoint
  modelは式(4), p.4。GPCM/2PL/Raschは式(7)--(8), p.5。
- **識別**: latent means、loadings、covariancesへ通常のIRT位置・尺度・回転制約を置く。
  Appendix, pp.15--16。
- **推定**: maximum marginal likelihood、式(9), p.5。
- **結果**: traitとpropensityの相関が強いほど、missingnessを無視したitem difficultyの誤差が
  大きくなる、pp.6--10。
- **本稿との差**: parametric IRT joint model内の推定とbias評価が中心で、一般的なfull-law
  identificationやblockwise recoveryは扱わない。

### Muthen, Kaplan and Hollis (1987)

- **対象**: SEMにおけるmissingness ignorabilityとquasi-likelihoodのlarge-sample bias。
- **モデル**: latent factor selectionは式(17), p.436。
- **結論**: latent factorにmissingnessが依存するとselection termがSEM parametersにも依存し、
  MARは一般に成立しない、Section 3.2, pp.436--437。正しいMLにはoutcome/selection modelの
  joint maximizationが必要、p.435。
- **限定**: factorial invarianceにより一部measurement parametersのbiasが0となる特殊構造も
  ある、Section 6.1.3, pp.449--452。
- **本稿との差**: 一般的なlatent distribution/measurement kernelの識別定理ではない。

### Lee and Tang (2006)

- **対象**: nonlinear SEM、latent variables、logistic missingness parametersのjoint Bayesian
  estimation。
- **モデル**: nonlinear measurement/structural equationsとsequential logistic missingness、
  式(1), (2), (5), pp.543--545。
- **識別上の注意**: 通常のSEM normalizationを置く一方、複雑すぎるmissingness modelは
  unidentifiableになり得ると明記する、p.544。
- **推定**: Metropolis--Hastings-within-Gibbs、Section 3, pp.546--549。
- **本稿との差**: 識別定理ではなく、指定したfully parametric model内のBayesian estimation。

### Harel and Schafer (2009)

- **対象**: missingnessの一部だけを無視可能とするpartial ignorabilityとlatent
  ignorability、およびitem nonresponseを伴うlatent-class analysis。
- **定義**: latent ignorabilityはmissing valuesのcoarsened summary `h(Y_mis)`を条件に
  missingnessが残りのmissing valuesへ依存しないこと、Definition 3, Section 4。
- **結論**: `h(Y_mis)`が既知ならmissingness indicatorの情報をlikelihood/Bayes inferenceで
  無視できる、Proposition 3。Section 5でsurvey itemのlatent-class analysisへ適用する。
- **本稿との差**: ignorabilityの分解とmodel-based analysisが中心で、external shadow IV、
  B-completeness、supported-block lawsの回復は扱わない。

### Jung, Schafer and Seo (2011)

- **対象**: arbitrary missing patternsを持つmultivariate dataのlatent-class selection model。
- **モデル**: missingness indicatorsでlatent classを定義し、incomplete itemsとcovariatesから
  class membershipを予測する。missingness modelは式(3.1)、population modelと合わせた
  complete-data likelihoodは式(3.2)、observed-data likelihoodは式(3.3), pp.804--805。
- **識別上の限定**: finite-mixture部分はclass labelsを除いて識別される一方、MNARの
  nonignorable aspectsは観測データだけでは識別できず、追加の検証不能な仮定が必要と明記する、
  Section 8, p.811。本文中にもnearly unidentified parametersへのpriorの役割がある。
- **推定**: joint posteriorのMCMCとmultiple imputation、model checking、simulation、
  実データ分析が中心。著者ら自身が主用途をsensitivity analysisと位置づける、p.811。
- **本稿との差**: multivariate MNARとlatent classの結合自体は既存である。同論文は
  parametric population/selection modelとuntestable missingness assumptionsに依存する。
  shadow-IV/B-completenessでblock lawを識別した後にmeasurement kernelsを分解する
  routeではない。

### Xie, Xue and Wang (2026)

- **対象**: multivariate MNARにおけるmissingness mechanismとground-truth full-data
  distribution `p_gt(x,r)`。
- **仮定**: missingness用latent variableが`X`と独立、Assumption 2, pp.4--5。
  `R_j independent (X_j,R_-j) | (X_-j,Z_tilde)`というconditional no-self-censoring、
  Assumption 3, p.5、およびall-observed patternのpositivityを課す。
- **識別**: Theorem 2がmissingness mechanism、Corollary 3がfull-data distributionを
  nonparametrically identifyする、pp.6--7。
- **推定**: conditional independenceを持つdeep latent working modelとimportance-weighted
  autoencoderを用いる。
- **本稿との差**: latent-variable MNARのfull-law identificationとして重要だが、識別対象は
  observable full-data distributionであり、latent coordinates、class proportions、
  measurement kernelsを個別に識別する定理ではない。またall-observed positivityを置く。

### Allman, Matias and Rhodes (2009)

- **対象**: finite latent-class modelのclass proportionsとclass-specific measurement kernels。
- **モデル**: `r`-class, `p`-feature model、式(1), p.3107。
- **strict result**: Theorem 1とCorollary 2。三modeのKruskal ranksの和が `2r+2`以上なら、
  permutation/scalingを除いて分解が一意で、stochastic normalization後はlabel swappingだけが
  残る、p.3109。
- **generic result**: Corollary 3およびTheorem 4。Theorem 4は多数のobserved variablesを
  三群へまとめるtripartition条件、p.3110。
- **本稿との差**: missingnessを扱わない。本稿はMNAR補正済みpair tensorsにTheorem 1の
  strict uniquenessを適用し、Wを第三modeとする。

### Kanamori, Hirose and Yamamoto (2026)

- **対象**: 共通latent componentsと未知mixing weightsを持つ複数のunlabeled mixtures。
- **識別**: product componentsのsubset-rank条件からaffine span内のindependent distributionを
  componentへ限定するTheorem 1, pp.6--7。Theorem 2とCorollary 1はfull-rank、
  no-cancellation、coordinate-pair marginal independenceの下でcomponentsを回復する、
  pp.8--10。mixing matrix全体の回復にはsquare/invertible caseまたはAppendix Eの
  irreducibility等の追加completion条件が必要である。
- **推定**: affine combinationsに対するProduct-Marginal MMD criterion。
- **本稿との差**: 複数mixturesからcomponentsとmixing matrixを識別する点は本稿の`W` routeに
  近いが、識別信号はmarginal independenceである。MNAR selection、shadow IV、supported
  blocks、anchor overlapは扱わないため、本稿の第一段階とは競合しない。

## 2. Missingness IV and pseudolikelihood

### d'Haultfoeuille (2010)

- **対象**: selection probabilityと `(D,Y,Z)` のjoint distribution。
- **仮定**: `D independent Z | Y`、YのZに対するB-completeness、positivity、Zの分布が
  識別済みであること。Assumptions 1--5, pp.2--3。
- **識別**: integral equation (2.3)の唯一解としてselection probabilityを回復し、
  Theorem 2.3でjoint lawを識別、p.3。
- **推定**: finite-dimensional GMMとregularized inverse problem、Section 3, pp.6--7。
- **本稿との差**: scalar outcomeを全vectorへ置き換えるとglobal complete-case positivityが
  必要になる。本稿はこれをsupported blocksへ分解する。

### Tang, Little and Raghunathan (2003)

- **対象**: multivariate MNAR下のregression parameters。
- **仮定と識別**: `R independent X | Y`の下、complete casesの `[X|Y]` と全標本の `[X]`
  を組み合わせる。式(2), (5), pp.749--750。Lemma 1とPropositionが識別条件を与える、
  pp.750--751。
- **推定**: parametricまたはempirical `[X]` をplug-inするpseudolikelihood。
- **本稿との差**: missingness mechanismやlatent measurement kernelsを識別しない。通常はfull
  outcome vectorのcomplete casesを使う。

### Zhao and Shao (2015)

- **対象**: GLMの有限次元parameters。
- **識別**: `R independent Z | (Y,U)` とcomplete-case identityから `[Z|Y,U]` を利用。
  式(2)--(3), Theorem 1, p.1579。
- **推定構成**: Section 2.3は `[U,Z]` のparametric/empirical/kernel estimateを先に得て
  pseudo-likelihoodへplug-inする、pp.1580--1581。
- **計算**: Section 4のtwo-step iterationは `lambda` と `omega` の交互更新、
  pp.1582--1583。
- **本稿との差**: 本稿はfinite-dimensional GLM rankではなくB-completenessでblock law全体を
  回復する。

### Miao, Liu, Tchetgen Tchetgen and Geng (2019 working paper)

- **対象**: scalar MNARのfull-data lawと各種functionals。
- **仮定**: shadow variable条件 `Z independent R | (X,Y)` とrelevance、Assumption 1,
  PDF p.4。complete-case lawのcompletenessはCondition 1。
- **識別**: odds-ratio integral equationとTheorem 1、PDF pp.8--9。
- **推定**: regression、IPW、doubly robust estimation、式(8)--(14), Theorem 2,
  PDF pp.10--12。
- **近接性**: parametric selection modelを規定せず、shadow variableと観測complete-case
  lawのcompletenessからfull-data joint lawを回復するため、本稿のsupported-block law回復に
  最も近い第一段階の先行研究である。
- **本稿との差**: 基本設定は一つの欠測outcome `Y` と一つの観測指標 `R` であり、複数の
  supported blocksを回復・接続せず、full-data lawをlatent class比率とmeasurement kernelsへ
  分解しない。本稿の候補はこのblockwise extensionとlatent decompositionの接続にある。

### Zhao and Ma (2018)

- **対象**: Tang型pseudolikelihood estimatorsの効率比較。
- **結果**: empirical distribution of Xを使うestimatorの優位性、Theorem 1 and
  Corollary 1, pp.481--482。Section 3はnonresponse instrumentへ拡張、式(5)--(6), p.483。
- **本稿との差**: 新しいlatent identificationではなく、pseudolikelihood efficiencyが中心。

## 3. Multivariate MNAR full-law identification

### Sadinle and Reiter (2017)

- **仮定**: Itemwise Conditionally Independent Nonresponse (ICIN)、Definition 1, p.209。
- **識別**: Theorem 1の再帰式でobserved-data lawからnonparametric saturated full-data lawを
  構成し、Theorem 2でICINを確認、pp.209--210。
- **本稿との差**: external IVを使わない別系統であり、latent class decompositionは対象外。

### Malinsky, Shpitser and Tchetgen Tchetgen (2022)

- **仮定**: no self-censoringとpositivity、Assumptions 1--2, pp.1417--1418。
- **識別・推定**: Theorem 1でresponse mechanism、Corollary 2でfull-data functionalsを
  識別し、Theorems 2--4でefficient influence functionとAIPWを扱う。
- **本稿との差**: semiparametric inferenceが中心で、latent measurement decompositionはない。

### Li, Miao, Shpitser and Tchetgen Tchetgen (2023)

- **仮定**: self-censoring `R_i independent Y_-i | (X,Y_i,R_-i)` とpositivity、
  Assumption 1, p.3205。
- **識別**: 他outcomesをshadow variablesとして使い、completenessからodds-ratio functionsと
  joint lawを識別、Theorems 1--2, pp.3206--3207。
- **推定**: IPW、outcome regression、doubly robust estimation、Theorems 3--5,
  pp.3207--3209。
- **本稿との差**: multivariate/blockwise comparisonとして重要。ただしcomplete-case supportを
  用い、latent class proportionsとmeasurement kernelsの分解は扱わない。

### Li and Shao (2022)

- **仮定**: panel response indicatorsのconditional i.i.d.構造とparametric response
  probability/nonresponse instrument、A1--A2, p.59。
- **推定**: observed component数によるgrouping、modified GMM、generalized regression。
  Theorems 2.1--2.2がconsistencyとasymptotic normalityを与える。
- **本稿との差**: indicator homogeneityとparametric propensityに依存し、latent measurement
  kernelを対象としない。

### Ni and Shao (2023)

- **仮定**: `X=(U,Z)`、`R independent Z | (Y,U)`、item indicatorsのconditional
  independence、parametric propensity、A1--A2, pp.2--3。
- **推定**: complete casesを用いたcomposite IPW、式(1), p.4とmodified GMM。
- **本稿との差**: multivariate outcomesとnonresponse instrumentを直接扱う近接研究だが、
  full-vector complete casesとparametric propensityを使い、latent decompositionは行わない。

### Yang, Ding, Wu and Udell (2021)

- **対象**: MNAR observationsを持つpartially observed tensorのentry completion。
- **仮定・方法**: original tensorとobservation propensity tensorがlow multilinear rankを持つ。
  propensityをconvex relaxationで推定し、inverse-propensity weightingとhigher-order SVDで
  missing entriesを予測する、pp.1--4。
- **結果**: completed tensorに対するfinite-sample error bounds、pp.4--7。
- **本稿との差**: array-valued signalのcompletionであり、joint probability tensorを
  class proportionsとmeasurement kernelsへ一意分解するlatent-model identificationではない。

## 4. Other estimation references

### Kim and Yu (2011)

- respondent/nonrespondent lawsをexponential tiltingで結ぶ、式(6), p.158。
- kernel regressionを含むsemiparametric mean-functional estimationを扱う。
- tilting parameterには既知値またはfollow-up sampleが必要で、外部識別なしには決まらない。

### Kott and Chang (2010)

- finite-population totals/meansに対するcalibration weighting。
- response probabilityをparametricに置き、calibration equationsからweightsを得る、
  pp.1266--1268。
- latent structureやfull-data-law decompositionは対象外。

### Honda (2025)

- 調査・行動データ統合における欠測と測定誤差をMultiple Overimputationで補正する。
- missingnessはMARであり、第3節、PDF pp.8--11でposterior predictive distributionから
  overimputationを行う。
- 本稿のMNAR shadow-IV identificationとは直接競合しない。

## 5. Manuscript positioning

監査した文献から安全に導ける位置づけは次の通りである。

> 本稿は、shadow variableとcompletenessによるMNAR full-law識別、およびKruskal型
> tensor分解によるfinite latent-class modelの識別を、それぞれ新たに提案するものではない。
> 貢献は、global complete caseを仮定せず、supported blocksごとに回復したoverlapping
> lawsをanchor itemsとlatent shifterを通じて接続し、finite latent-class proportionsと
> measurement kernelsを同一のlabelingの下で識別する十分条件を与える点にある。

追加検索したtensor completion、latent class models with missing data、multi-view mixture
identificationを含めても、「初めて」または「従来扱われていない」という網羅的な断定は
支持しない。安全な位置づけは、shadow-IV/B-completenessによるsupported-block law回復と、anchor items、
latent shifter、Kruskal分解によるfinite-class componentsの統合に限定される。
