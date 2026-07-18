# 容量制約付きレビュー研究と潜在因子 Shadow-IV 研究

## 査読者評価・論文分割・優先順位

**作成日:** 2026-07-18
**目的:** 二つの研究方向を混同せず、識別主張の成立範囲、既存研究との差、投稿可能性、次の作業順序を固定する。

## 1. 結論

二つの研究は分割するべきである。現時点で一方を優先するなら、**容量制約付きレビュー研究を先行**させる方が、独自の観察可能な現象、実験可能性、早期投稿可能性の点で優位である。

潜在因子 Shadow-IV 研究は博論との整合性と理論的な上限が高い一方、現在の主張はそのままでは論文の定理にならない。特に、

1. shadow exclusion と relevance / completeness の混同、
2. 項目別周辺分布と多変量同時分布の混同、
3. 「三つの測定値があれば非線形測定モデルが識別される」という過大な一般化、
4. 潜在尺度の正規化不足、
5. 既存の self-censoring と非線形測定誤差モデルを逐次適用しただけに見える新規性、

を解消する必要がある。

したがって推奨する研究ポートフォリオは次の通りである。

- **論文A:** Capacity-constrained review generation and competitive underreporting
- **論文B:** Nonparametric identification of latent measurement models with itemwise MNAR outcomes and a common shadow variable
- **将来の論文C:** Platform ranking / generative-AI amplification

## 2. 二つの研究の欠測構造

### 2.1 論文A: 容量制約付きレビュー

個人 \(i\) は \(J\) 個の私的評価 \(\bm Y_i=(Y_{i1},\ldots,Y_{iJ})\) を持ち、公開効用

\[
A_{ij}=b(Y_{ij},X_{ij})+\varepsilon^D_{ij}
\]

の上位 \(K_i\) 件を公開する。

\[
S_i(K_i)\in
\arg\max_{S\subseteq\{1,\ldots,J\}}
\sum_{j\in S}A_{ij}
\quad\text{s.t.}\quad |S|\le K_i,
\qquad
R_{ij}=\mathbf 1\{j\in S_i(K_i)\}.
\]

したがって \(R_{ij}\) は \(Y_{ij}\) だけでなく \(\bm Y_{i,-j}\) にも依存し、欠測指標間には容量制約による依存が生じる。exact top-\(K\) なら

\[
\sum_{j=1}^J R_{ij}=K_i
\]

であり、\(K_i<J\) のとき完全ケースは構造的に存在しない。

### 2.2 論文B: 潜在因子と項目別 self-censoring

測定モデルを

\[
Y_{ij}=h_j(F_i)+\varepsilon_{ij},
\qquad j=1,\ldots,J
\]

とする。常時観測変数 \(V_i\) との関係には二つの型がある。

\[
\text{IV型:}\quad F_i=g_{\mathrm{IV}}(V_i)+U_i,
\]

\[
\text{proxy型:}\quad V_i=g_{\mathrm P}(F_i)+U_i.
\]

項目別欠測を

\[
D_{ij}=\mathbf 1\{k_j(Y_{ij})+\eta_{ij}>0\}
\]

とする。このモデルは、各項目の欠測が自己の値だけに依存する strict self-censoring の特殊ケースである。

## 3. 潜在因子案の識別監査

### 3.1 shadow exclusion は成立し得る

\(\eta_{ij}\) が \((V_i,F_i,\bm\varepsilon_i)\) から独立なら、IV型・proxy型のいずれでも

\[
\Pr(D_{ij}=1\mid Y_{ij},V_i)
=\Pr\{\eta_{ij}>-k_j(Y_{ij})\mid Y_{ij}\}
=:\pi_j(Y_{ij}),
\]

したがって

\[
D_{ij}\perp\!\!\!\perp V_i\mid Y_{ij}
\tag{SV-j}
\]

が成立する。これは因果方向 \(V\to F\) または \(F\to V\) ではなく、\(V\) が欠測効用に直接入らないことから従う。

ただし、(SV-j) だけで \(V\) が有効な shadow variable になるわけではない。少なくとも relevance と、識別対象に応じた completeness または representer 条件が必要である。

### 3.2 relevance と completeness は自動的ではない

各項目について full-law identification を行う典型的な条件は

\[
E\{a(Y_{ij})\mid V_i\}=0
\quad\Longrightarrow\quad
a(Y_{ij})=0\quad\text{a.s.}
\tag{C-j}
\]

である。\(V_i\) が \(F_i\) と関連すること、\(g\) が非定数であること、または \(g\) が非線形であることだけでは (C-j) は従わない。

反例として、\(g\) が定数なら \(V_i\) と \(Y_{ij}\) は関連せず、shadow relevance が失われる。また、\(V_i\) と \(Y_{ij}\) が相関していても条件付き期待値作用素が非自明なヌル空間を持つ場合、completeness は成立しない。

### 3.3 各周辺平均の識別

(SV-j)、positivity \(\pi_j(Y_{ij})>0\)、(C-j) の下では

\[
E\{D_{ij}w_j(Y_{ij})\mid V_i\}=1,
\qquad
w_j(y)=\frac{1}{\pi_j(y)},
\]

から \(\pi_j\) を識別できる。したがって

\[
E(Y_{ij})
=E\{D_{ij}w_j(Y_{ij})Y_{ij}\}
\]

が識別される。

これは項目ごとのスカラー shadow-variable 識別を同じ \(V_i\) に対して反復した結果であり、ここだけでは共通潜在因子を必要としない。

### 3.4 同時分布の回復には追加仮定が必要

\(P(Y_{i1},Y_{i2},V_i)\) などを回復するには、項目別識別だけでは足りない。例えば任意の \(S\subseteq\{1,\ldots,J\}\) について

\[
\Pr(D_{ij}=1,\ j\in S\mid\bm Y_i,V_i)
=\prod_{j\in S}\pi_j(Y_{ij})
\tag{PF}
\]

と、同時観測positivityが必要である。(PF) は \(\eta_{i1},\ldots,\eta_{iJ}\) の条件付き独立性と、各欠測式が自己の \(Y_{ij}\) だけに依存するという強い仮定である。

このときのみ

\[
E\!\left[
\left\{\prod_{j\in S}D_{ij}w_j(Y_{ij})\right\}
\varphi(\bm Y_{iS},V_i)
\right]
=E\{\varphi(\bm Y_{iS},V_i)\}
\]

により \(P(\bm Y_{iS},V_i)\) を回復できる。

### 3.5 非線形潜在測定モデルの識別は別の定理である

復元された \(P(Y_{i1},Y_{i2},V_i)\) から \(F_i\)、\(h_2\)、\(g\) を識別するには、Hu--Schennach型の条件を明示する必要がある。「三つの条件付き独立な測定値がある」という記述だけでは不十分である。

必要となり得る条件には、以下が含まれる。

- 潜在変数を条件とした測定値の条件付き独立性
- 関連する積分作用素の単射性または bounded completeness
- 固有値・固有関数分解を一意にラベル付けするlocation条件
- 誤差分布と測定関数に関する正則性
- 潜在尺度と向きを固定する正規化

したがって、論文では「既存定理を仮定する」のか、「本モデルについてprimitive conditionsから証明する」のかを分ける必要がある。前者なら方法論的新規性は限定的である。

### 3.6 潜在尺度の正規化

\(E(F)=0\)、\(\operatorname{Var}(F)=1\)、\(h_1\) が単調増加、だけでは一般に非線形な再パラメータ化を排除できない。単調な一対一変換 \(T\) により

\[
F^*=T(F),
\qquad
h_j^*(f^*)=h_j\{T^{-1}(f^*)\}
\]

と書き換えても観測分布が同じになる可能性がある。標準化後にも複数の単調変換が残り得るため、例えば

\[
h_1(f)=f
\]

を固定する、潜在分布全体を既知とする、または既存識別定理のlocation normalizationを厳密に採用する必要がある。

### 3.7 \(g\) の非線形性と completeness

IV型シフトモデル \(F=g_{\mathrm{IV}}(V)+U\) では

\[
E\{a(F)\mid V=v\}
=\int a(f)p_U\{f-g_{\mathrm{IV}}(v)\}\,df
=(a*\check p_U)\{g_{\mathrm{IV}}(v)\}.
\]

例えば \(g_{\mathrm{IV}}(\mathcal V)=\mathbb R\) かつ \(U\) の特性関数が全域で非零なら、適切な関数空間においてcompletenessを示せる。しかし、\(g\) の非線形性それ自体は必要条件でも十分条件でもない。像が開区間を含むだけの場合、畳み込みの解析性などを追加しない限り、区間上の零から全域の零は従わない。

### 3.8 測定誤差と欠測の概念は識別可能性で分けない

測定誤差は観測値が真値とノイズから生成される観測方程式であり、欠測は観測指標によって値が記録されない観測過程である。「誤差分布を設定できるなら測定誤差、できないなら欠測」という分類は採用しない。特性関数の零点や逆問題のill-posednessは識別・推定の難しさを表すが、測定誤差と欠測の定義上の境界ではない。

## 4. 既存研究との境界

### 4.1 Shadow-variable文献

d'Haultfoeuille (2010) 以降のshadow-variable文献は、条件付き排除とcompletenessによりMNAR full-data lawをノンパラメトリックに識別する一般論を与えている。Miao et al. (2024) は一般的な識別条件、効率影響関数、二重ロバスト推定まで提示している。

### 4.2 多変量 self-censoring

Li, Miao, Shpitser and Tchetgen Tchetgen (2023) は、各欠測指標が自己のアウトカムに依存し、他のアウトカムには条件付きで依存しない多変量 self-censoring modelを提示し、full-data lawの識別、IPW、回帰型、二重ロバスト推定、感度分析まで与えている。現在の項目別欠測式は、そのstrict self-censoring特殊ケースに近い。

### 4.3 非線形測定誤差

Hu and Schennach (2008) は、操作変数を利用した非古典的・非線形測定誤差モデルについて、作用素の固有値・固有関数分解による識別とsieve推定を提示している。

### 4.4 現在の潜在因子案が受ける査読評価

現在のままでは

\[
\text{既存の項目別shadow識別}
+\text{strict self-censoring}
+\text{既存の非線形測定モデル識別}
\]

の逐次適用と評価される可能性が高い。「一つの \(V\) を複数項目に反復利用できる」だけでは、共通潜在因子に固有の新定理とはならない。

## 5. 査読者としての比較

| 観点 | 論文A: 容量制約レビュー | 論文B: 潜在因子 Shadow-IV |
|---|---|---|
| 現在の新規性 | randomized \(K\)、cross-item crowd-out、oracle/public比較が明確 | 既存結果の合成に見える |
| 欠測構造 | dependent multivariate MNAR、構造的零 | strict itemwise self-censoring、積型欠測 |
| 理論リスク | 中 | 高 |
| 実証可能性 | 倫理審査後に直接実験可能 | 適切な実証設定が別途必要 |
| 短期投稿 | Economics Letters、Journal of Interactive Marketing、ECRA | 現状では難しい |
| 理論的上限 | 新推定理論を加えれば高い | 真に新しい識別定理ができれば高い |
| 博論との整合 | 中 | 高 |

## 6. 二本を統合しない理由

論文Bのjoint recoveryは (PF) と同時観測positivityに依存する。一方、論文Aのexact top-\(K\)選択では

\[
\sum_jR_{ij}=K_i<J
\]

であり、欠測指標は負に依存し、完全ケース確率は零である。したがって、論文Bの積重み識別をレビュー設定に適用できない。

この差は単なる応用上の違いではなく、識別仮定の違いである。一つの論文に統合すると、前半のproduct-form self-censoringと後半のcapacity-constrained dependent missingnessが矛盾して見える。

## 7. 推奨する作業順序

### 7.1 論文Aを先行する

1. \(K_i\) をランダム化したExperiment 1を確定する。
2. 自己評価効果、cross-item crowd-out、容量効果を事前登録する。
3. oracleとpublicについて平均、裾確率、極端性を比較する。
4. 事前期待等を用いたtarget-specific representer bridgeを推定する。
5. 排除制約違反への感度分析を行う。
6. 最初はExperiment 2と潜在因子を切り離す。

### 7.2 論文Bは短期間の定理監査を行う

最初に、有限離散モデルで観測分布から構造対象への写像のrankを確認し、識別と反例を明示する。その後、次の候補定理が既存研究の単純な逐次適用を超えるか判定する。

> すべての測定項目がitemwise MNARであっても、単一の常時観測proxy \(V\) と部分観測パターンから、潜在分布、測定関数、母集団平均をノンパラメトリックに識別できる。

Go条件は、少なくとも次の一つを示せることである。

- Li et al. (2023) のcross-outcome completenessを弱める。
- 完全ケースを必要としない。
- 高次元vector completenessを低次元latent completenessへ置き換える。
- 各項目に別々のshadow variableを必要とせず、単一proxyについてprimitiveな十分条件を与える。
- 潜在関数推定誤差を含む新しい推定・推論理論を与える。

これらを示せず、既存定理を順番に適用するだけなら、独立した方法論論文ではなく博論の補助章または応用上の構造拡張として扱う。

## 8. 投稿先の見立て

### 論文A

- 短報: **Economics Letters**
- レビュー行動・プラットフォーム中心: **Journal of Interactive Marketing**、**Electronic Commerce Research and Applications**
- 新しい推定・漸近理論まで含む場合: **The Econometrics Journal**

### 論文B

- 新しい識別定理、推定量、漸近理論、simulationが揃う場合: **The Econometrics Journal**、**Journal of Multivariate Analysis**、**Statistica Sinica**
- 潜在特性・測定モデルを中心とする場合: **Psychometrika**、**Multivariate Behavioral Research**
- 現在の逐次適用だけの場合: 独立した上位方法論誌への投稿は推奨しない。

### 上位目標

Journal of Econometricsを目標にするには、top-\(K\) dependent MNARまたはlatent-proxy MNARに固有の新しい識別・推論理論が必要である。既存representerまたはHu--Schennach定理の応用だけでは不足する。

## 9. 最終判断

期待採択確率と完成可能性を重視するなら、論文Aを先に完成させる。論文Bは放棄せず、博論の理論章候補として、まず識別定理の成立範囲と既存研究との差を監査する。

両者の関係は「同じ論文の理論と応用」ではなく、次のように整理する。

\[
\boxed{
\begin{array}{c}
\text{論文A: dependent top-}K\text{ MNARを実験で発見・補正}\[1mm]
\text{論文B: itemwise MNAR下の潜在測定モデルを理論的に識別}
\end{array}}
\]

## 参考文献

- d'Haultfoeuille, X. (2010). A new instrumental method for dealing with endogenous selection. *Journal of Econometrics*, 154(1), 1--15. <https://doi.org/10.1016/j.jeconom.2009.06.005>
- Hu, Y., & Schennach, S. M. (2008). Instrumental variable treatment of nonclassical measurement error models. *Econometrica*, 76(1), 195--216. <https://doi.org/10.1111/j.0012-9682.2008.00823.x>
- Li, Y., Miao, W., Shpitser, I., & Tchetgen Tchetgen, E. J. (2023). A self-censoring model for multivariate nonignorable nonmonotone missing data. *Biometrics*, 79(4), 3203--3214. <https://doi.org/10.1111/biom.13916>
- Miao, W., Liu, L., Li, Y., Tchetgen Tchetgen, E. J., & Geng, Z. (2024). Identification and semiparametric efficiency theory of nonignorable missing data with a shadow variable. *ACM/IMS Journal of Data Science*, 1(2), Article 5. <https://doi.org/10.1145/3592389>
