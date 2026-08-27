# Citation claim audit

監査対象は `notes/vector_missing_iv_identification_working.tex` と、
`resources/latent_multivariate`、`resources/shadow variable`、`resources/missing`
に保存された25 PDF（24論文）、ならびに出版社・著者公開本文で確認した1論文である。
Kano and Takai (2011) は二つの配布版があるが、抽出本文とDOIが一致するため
一論文として扱う。

## 判定基準

- **確認済み**: 本文の主張が原文の対象、仮定、結論の範囲内にある。
- **限定が必要**: 中心内容は支持されるが、識別対象または仮定の限定が欠ける。
- **引用箇所誤り**: 文献は適切だが、節・定理・式の参照が誤っている。
- **根拠不足**: ローカル原文から当該主張を直接確認できない。
- **本文未使用**: PDFまたは参考文献は存在するが、本文の主張に使われていない。

## 重要な監査結論

1. Allman, Matias and Rhodes (2009) の Corollary 2 は Section 4, p.3109である。
   Theorem 1/Corollary 2の実現Kruskal rankによる一意性と、Section 5,
   Theorem 4のgeneric identificationを分ける。
2. Zhao and Shao (2015) の Section 2.3は周辺法則を先に推定するplug-in
   pseudo-likelihoodである。Section 4のtwo-step iterationは回帰パラメータ
   `lambda` とdispersion `omega` の交互更新であり、別の手順である。
3. Kuha et al. (2018) はlatent traitとlatent response classのjoint modelを提案する
   だけでなく、その識別条件も述べる。latent structureとMNARの統合自体を新規性と
   してはならない。
4. 本稿の安全な貢献候補は、parametric selection modelを正しく指定する代わりに、
   shadow IVとblockwise complete-case completenessでoverlapping supported-block lawsを回復し、anchor itemsと
   latent shifterを通じて同一のclass labelingの下で潜在class比率と測定核を識別する
   二段階の十分条件である。

## 本文主張の監査

| 本文位置 | 引用・主張 | 原文根拠 | 判定 | 修正方針 |
|---|---|---|---|---|
| 63--74 | 医学・疫学・心理学の具体例 | 本稿の動機としては自然だが、列挙した各応用を直接裏付ける実証文献は今回のPDF集合にない。 | 根拠不足 | 「本稿が想定する例」として例示であることを明記する。 |
| 79--81 | latent factor依存欠測ではMARが一般に成立せず、quasi-likelihoodにbiasが生じ得る | Muthen et al. (1987), Section 3.2, pp.436--437; Section 6.1.3, pp.449--452. | 確認済み | 「一部の構造パラメータ」という限定を維持する。 |
| 82--83 | 非線形SEMとlogistic selection modelのjoint Bayesian推定 | Lee and Tang (2006), eqs. (1), (2), (5), pp.543--545; Section 3, pp.546--549. | 確認済み | 識別定理ではなくfully parametric estimation routeとして引用する。 |
| 83--85 | IRTにlatent response propensityを導入し、無視した場合のbiasを検討 | Holman and Glas (2005), eqs. (2), (4), (7)--(9), pp.3--10. | 確認済み | parametric joint IRT model内の結果であることを維持する。 |
| 86--88 | latent response classとlatent traitの関連でMNARを表現 | Kuha et al. (2018), eqs. (1), (6)--(9), pp.1171--1176. | 限定が必要 | 同論文がjoint modelの識別条件も与えることを追記する。 |
| 96--104 | 識別済みの線形latent structureの下でmissingness mechanismを指定しないMSA推定 | Kano and Takai (2011), covariance parameterの識別済み仮定, p.1243; A2--A4, eqs. (7)--(15), pp.1244--1246; conclusion, p.1251. | 確認済み | 潜在測定構造の識別結果として引用せず、通常のSEM識別制約を置いた後の一致推定として記す。 |
| 118--119 | B-completenessとpositivityによる `(D,Y,Z)` joint lawの識別 | d'Haultfoeuille (2010), Assumptions 1--5, eqs. (2.2)--(2.3), Theorem 2.3, p.3. | 確認済み | Assumption 2としてZの分布が識別済みである点を落とさない。 |
| 119--123 | 共変量調整済みexclusionによるGLMパラメータの識別 | Zhao and Shao (2015), eqs. (2)--(3), Theorem 1, p.1579. | 確認済み | full nonparametric lawではなく有限次元GLMパラメータの識別とする。 |
| 123--130 | shadow variableと観測complete-case lawのcompletenessによるfull-data joint lawの識別 | Miao et al. (2019), Assumption 1, p.4; Condition 1 and Theorem 1, pp.8--9. | 確認済み | 本稿の第一段階に最も近い。基本設定は一つの欠測outcomeと一つの観測指標であり、supported blocksの接続とlatent decompositionは扱わない。仮定7と命題2.1ではcomplete-case conditional operatorの単射性としてblockwiseに継承する。 |
| 136--138 | marginal mixture lawが識別されてもlatent分解は一意でない | Allman et al. (2009), Sections 3--4, pp.3106--3109. | 限定が必要 | 「追加の分解一意性条件なしには一意でない」とする。 |
| 140--146 | Allmanの3-view tensorによるlatent-class識別 | Allman et al. (2009), Section 4, Theorem 1 and Corollary 2, p.3109. | 引用箇所誤り | `Section 3, Corollary 2`を`Section 4, Theorem 1 and Corollary 2`へ修正し、Theorem 4を外す。 |
| 76--104 | 既存latent-MNAR modelと本稿の差 | Kuha et al. (2018), Holman and Glas (2005), Lee and Tang (2006); Kano and Takai (2011). | 限定が必要 | joint model内の識別と、Kano--Takaiの識別済み線形構造の下での推定を分ける。本稿の差はsupported-block recoveryとlatent decompositionの接続に限定する。 |
| 179--188 | Zhao--Shao、d'Haultfoeuille、Allmanの三原理 | 各文献の上記箇所。 | 確認済み | AllmanをSection 3のmodelとSection 4のTheorem 1/Corollary 2に具体化する。 |
| 264--267 | Zhao--Shaoの `(Y,U,Z,R)` のblockwise置換 | Zhao and Shao (2015), Section 2.1, pp.1578--1579. | 確認済み | WをUへ含める部分は本稿の拡張として記す。 |
| 270--278 | full vector routeはglobal complete caseを必要とする | d'Haultfoeuille (2010), Assumption 1 and Theorem 2.3をvector Yへ適用した含意。 | 確認済み | 原論文の定理そのものではなく、本稿によるvectorizationの含意と明記する。 |
| 299--300 | complete-case identity | Zhao and Shao (2015), eq. (3), p.1579. | 確認済み | blockwise analogueという表現を維持する。 |
| 310--313 | Zhao--Shaoの有限次元rank条件とB-completenessの差 | Zhao and Shao (2015), Theorem 1 and Appendix. | 確認済み | 有限次元/無限次元の区別を維持する。 |
| 345--347 | block law回復はZhao--Shao型exclusionとd'Haultfoeuille型一意性の拡張 | 上記両文献。 | 確認済み | 「型」「blockへの条件付き適用」という限定を維持する。 |
| 392--399 | finite latent classの3-view route | Allman et al. (2009), Section 3, pp.3106--3107; Section 4, pp.3108--3109. | 確認済み | MNAR結果ではないことを明記する。 |
| 525--533 | Theorem 1によるCP分解のpermutation/scaling一意性 | Allman et al. (2009), Theorem 1, p.3109. | 確認済み | 本稿のcolumn conventionが原論文のrow conventionの転置である点に注意する。 |
| 602--605 | inverse problem推定とIPWへの接続 | d'Haultfoeuille (2010), Section 3, pp.6--7, Theorem 3.1 and Corollary 3.2. | 確認済み | bridge estimationの先例として引用する。 |
| 606--608 | complete-case lawからpseudo-likelihoodへの接続 | Zhao and Shao (2015), Section 2.3, pp.1580--1581. | 限定が必要 | 同論文のnuisanceは `[U,Z]` 等でありmissingness mechanismそのものではないため、「同様」ではなく「推定構成上の先例」とする。 |
| 711--714 | Zhao--Shaoのtwo-step algorithm | Zhao and Shao (2015), Section 4, pp.1582--1583. | 引用箇所誤り | Section 2.3のplug-in構造とSection 4の `lambda`/`omega` 交互更新を分ける。 |
| 750--774 | Allman型simulation modelとAllmanに数値実験がないこと | Allman et al. (2009), Section 3, eq. (1), p.3107. | 確認済み | 数値parameterは本稿固有という脚注を維持する。 |

## 二担当の相互検証

### 読解担当から指摘担当への応答

- Allmanの中心根拠はTheorem 1/Corollary 2であり、Theorem 4を本稿のstrict
  identificationへ直接使わない点に同意した。
- Zhao--Shaoについて、Section 2.3をcriterion構築、Section 4を数値最適化の先例として
  分けるべきとの指摘に同意した。
- Kuha et al.の識別条件を正面から認め、latent-MNAR自体を新規性としない点に同意した。
- multivariate MNARの本文追加候補としてMiao et al. (2019)、Sadinle and Reiter
  (2017)、Li et al. (2023)を挙げ、Tang et al. (2003)を本文引用へ昇格させる案を示した。

### 指摘担当から読解担当への反対検証

- 「parametric modelを置かない」は広すぎる。本稿もknown class数、local independence、
  Kruskal rank、anchor orderingを課すため、「parametric selection modelを直接規定しない」
  と限定する必要がある。
- shadow IV、B-completeness、complete-case completeness自体はd'HaultfoeuilleやMiao et al.に既にあり、
  tensor分解自体もAllman et al.にある。新規性は両段階の接続に置く。
- Li et al. (2023)にはcompletenessを用いるmultivariate self-censoringとblockwise extensionが
  あるため、「初のblockwise MNAR識別」とは書かない。
- Ni and Shao (2023)はmultivariate outcomes、item nonresponse、nonresponse instrumentを
  直接扱うため、第一段階の比較に含める。
- 「初めて」という断定には今回の19論文だけでなく、tensor completionやlatent class with
  missing dataの追加検索が必要である。本稿ではその断定を避ける。

## 本文に追加する比較文献

| 文献 | 本文での役割 |
|---|---|
| Tang, Little and Raghunathan (2003) | multivariate MNARに対するcomplete-case conditional likelihoodとpseudo-likelihoodの先例 |
| Miao et al. (2019 working-paper version) | shadow variableとcompletenessによるfull-data-law識別の直接比較 |
| Sadinle and Reiter (2017) | 外部IVを使わないICINによるmultivariate full-law識別の別系統 |
| Li et al. (2023) | self-censoring、completeness、multivariate/blockwise識別の近接比較 |
| Ni and Shao (2023) | multivariate item nonresponseとnonresponse instrumentを用いるIPWの近接比較 |

## 追加新規性監査

| 文献 | 原文根拠 | 本稿との重なり | 判定・本文上の扱い |
|---|---|---|---|
| Harel and Schafer (2009) | Definition 3, Proposition 3, Section 4; latent-class application in Section 5 | latent ignorabilityを定義し、item nonresponseを伴うlatent-class analysisへ適用する。 | **限定が必要**: latent classとnonignorable missingnessの組合せ自体は既存。ただし本稿のshadow-IV/B-completeness routeではない。 |
| Jung, Schafer and Seo (2011) | eqs. (3.1)--(3.3), pp.804--805; Section 8, p.811 | missingness indicatorsで定義されるlatent response classを介してmultivariate MNARを表すlatent-class selection model。population modelとmissingness modelをjoint likelihoodとして規定する。 | **限定が必要**: multivariate MNAR latent-class model自体は既存。ただし非無視部分には検証不能な仮定が必要で、主眼はsensitivity analysisとmultiple imputationである。本稿と同じshadow-IV/B-completenessによるblock-law識別ではない。 |
| Yang et al. (2021) | abstract; low-rank propensity model and finite-sample bounds, pp.1--7 | MNAR下でlow-multilinear-rank tensorの欠測entryをIPW/HOSVDで補完する。 | **区別可能**: 対象はarray entryのcompletionであり、probability tensorのlatent-class decompositionやclass labelingの接続ではない。 |
| Xie, Xue and Wang (2026) | Assumptions 2--4, Theorem 2 and Corollary 3, pp.4--6 | latent variableを条件とするno-self-censoringからmissingness mechanismとfull-data distributionを識別する。 | **重要な近接研究**: latent-variable MNARに識別定理があることを認める。ただし識別対象はground-truth full-data distributionであり、working modelのlatent coordinatesや測定核の個別識別ではない。 |
| Kanamori, Hirose and Yamamoto (2026) | Theorems 1--2 and Corollary 1, pp.6--10; completion results in Appendix E | 共通componentを持つ複数unlabeled mixturesから、marginal independenceによりcomponent distributionsを回復する。mixing matrix全体にはsquare/invertible caseまたはirreducibility等の追加条件が要る。 | **近接する第二段階**: 複数mixturesからcomponentを回復する別routeであり、MNAR、shadow IV、supported blocksは扱わない。Wをthird modeとする本稿のKruskal routeとは識別信号が異なる。 |

追加検索後も「初めて」という断定は避ける。本文では、第一段階の
shadow-IV/complete-case-completenessによるblock-law回復と、第二段階のanchor/latent-shifterを用いる
finite-class decompositionを一体として比較する。

## 参考文献の必要十分性

本文未使用だった8件のうちTang et al. (2003)は本文へ追加して残す。次の7件は、今回の
本文に対応する主張がないため削除する。

- Little and Rubin (2002)
- Robins and Ritov (1997)
- Greenlees, Reece and Zieschang (1982)
- Ibrahim, Chen and Lipsitz (2001)
- Qin, Leung and Shao (2002)
- Kott and Chang (2010)
- Kim and Yu (2011)

Miao et al.についてはローカルPDFが2019年working-paper版であるため、その版を引用する。
2024年の刊行版は著者と題名が異なり、同一書誌として扱わない。
