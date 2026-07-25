# Shadow-IV と潜在変数モデル: Annals of Statistics 向け理論監査

作成日: 2026-07-25

## 0. 対象資料

本メモは次の資料を順に比較して作成した。

1. `mnar_latent_iv_memo.pdf`（12頁、初期草案）
2. `mnar_latent_iv_memo_revised.tex` / PDF（18頁、中間改稿）
3. `shadow_iv_latent_joint_aos_memo_ja_v6.tex` / PDF（83頁、統合版）

資料の発展は次のように整理できる。

- 12頁版: blockwise shadow recovery の後に有限潜在クラスまたは連続潜在モデルを識別する二段階案
- 18頁版: mixture shifter \(W\) と block-specific shadow \(Z_S\) を分離し、target-specific recovery、pair-\(W\) tensor、\(K=1\) の限界を追加
- 83頁版: 非一意 bridge と潜在構造の共同識別、有限・連続理論、因子分析、Rasch、推定、minimax、weak identification を一冊に統合

83頁版は内容が不足しているのではなく、少なくとも三本の論文に相当する内容を一稿へ積み過ぎている。

## 1. 星野先生の問いへの現時点の回答

星野先生の問いは、潜在変数 MNAR モデルを次の三層に分け、各層をどこまでパラメトリックにせず識別できるか、というものである。

\[
\begin{aligned}
\text{層1: }&P(D\mid Y,F,X)
&&\text{欠測機構},\\
\text{層2: }&P(Y\mid F,X;\beta)
&&\text{測定モデル},\\
\text{層3: }&P(F\mid X)
&&\text{潜在分布}.
\end{aligned}
\]

結論は次のとおりである。

### 1.1 潜在変数を積分消去しただけでは十分でない

顕在変数の完全データ分布 \(P_Y\) が shadow-IV により回復されても、

\[
P_Y(y)=\int P(y\mid f;\beta)\,dG(f)
\]

という潜在分解 \((\beta,G)\) が一意とは限らない。したがって、

> 「顕在分布の識別」と「測定母数・潜在分布の識別」は別問題である

という星野先生の指摘は正しい。

一方、pure shadow が \(F\) に追加的な情報を持たず、選択も latent representation ではなく \(Y\) のみに依存する場合、shadow-IV は完全データでも残る latent label、位置・尺度、符号、回転、mixture aliasing を解消できない。よって、潜在母数の識別には complete-data manifest map の一意性または追加 proxy/shifter 構造が必要である。

### 1.2 三層ごとの現時点の答え

| 層 | shadow-IV がある場合に外せる指定 | なお必要な条件 |
|---|---|---|
| 1. 欠測機構 | logistic/probit 等の link を指定せず、nonparametric selection を許せる | shadow exclusion、positivity、full-law completeness、target range、または共同識別条件 |
| 2. 測定モデル | 識別対象によっては有限次元構造だけを残し、誤差分布を unspecified にできる | 完全データでの因子負荷・IRT母数の一意性、正規化、rank/graph/tensor 条件 |
| 3. 潜在分布 | 因子負荷や Rasch difficulty のように \(G\) を消去できる母数では \(G\) を unspecified にできる | \(G\) 自体を識別するなら multi-view measurements、proxy/shifter、作用素単射性が必要 |

したがって、現時点の理論的主張は、

> shadow-IV により層1を nonparametric に保ったまま、層2・層3のうち完全データ統計で分離できる部分を識別できる

である。三層すべてを同時に unrestricted nonparametric にして常に識別できる、という結果ではない。

## 2. \(Z\)-\(F\)-\(X_j\)-\(R_j\) 案

星野先生との議論から生じた候補モデルを、

\[
Z\longrightarrow F\longrightarrow X_j,\qquad
X_j\longrightarrow R_j
\]

とする。次の原始条件を置く。

\[
X_j\perp Z\mid(F,C),
\tag{A1}
\]

\[
R_j\perp F\mid(X_j,C),
\tag{A2}
\]

\[
R_j\perp Z\mid(F,X_j,C).
\tag{A3}
\]

このとき、

\[
R_j\perp Z\mid(X_j,C)
\]

が成立する。実際、

\[
\begin{aligned}
P(R_j=r\mid X_j=x,Z=z,C=c)
&=\int P(R_j=r\mid x,f,z,c)\,dP(f\mid x,z,c)\\
&=\int P(R_j=r\mid x,f,c)\,dP(f\mid x,z,c)\\
&=\int P(R_j=r\mid x,c)\,dP(f\mid x,z,c)\\
&=P(R_j=r\mid x,c).
\end{aligned}
\]

したがって、観測される \(Z\) は \(X_j\) に対する通常の shadow variable になる。ここで \(F\) は「欠測IV」そのものというより、\(Z\) と \(X_j\) の relevance を生成する潜在媒介変数である。

### 2.1 合成完備性

作用素

\[
(A_jg)(f,c)=E\{g(X_j,C)\mid F=f,C=c\},
\]

\[
(Bh)(z,c)=E\{h(F,C)\mid Z=z,C=c\}
\]

を定義する。(A1) の下で、

\[
E\{g(X_j,C)\mid Z,C\}=(BA_jg)(Z,C).
\]

従って、

1. \(A_j\) が単射
2. \(B\) が少なくとも \(\operatorname{Range}(A_j)\) 上で単射

なら、合成作用素 \(BA_j\) は単射である。この条件は \(B\) が潜在空間全体で完全であることより弱い。

これは「weak IV」というより、

> range-restricted compositional completeness

と呼ぶ方が正確である。単射だが最小特異値が小さい場合には、点識別は成立するものの弱識別・ill-posedness が生じる。

### 2.2 この結果の限界

この短い継承定理は itemwise MNAR には使えるが、exact top-\(K\) 選択には一般にそのまま使えない。top-\(K\) では、

\[
R_j=r_j(X_1,\ldots,X_J)
\]

であり、\(X_j\) を固定しても \(F\) が \(X_{-j}\) を通じて \(R_j\) を予測し得るため、

\[
R_j\not\perp F\mid X_j
\]

となり得る。レビュー研究では supported block \(X_S\)、block-specific shadow \(Z_S\)、mixture shifter \(W\) を分ける必要がある。

したがって、潜在変数理論とオンラインレビュー実験は、現段階では別研究として扱うのが安全である。

## 3. 83頁版の査読判定

### 総合判定

現状は Annals of Statistics 投稿稿ではなく、研究プログラムを集積した technical compendium である。AoSへ進めるには、主定理を二本程度へ削り、実際の観測データモデル上の識別集合として証明し直す必要がある。

### 3.1 重大な問題

#### (a) 商空間 fiber は緩和モーメントモデルの解集合である

現行の

\[
\Psi(\lambda)-\Psi(\lambda_0)\in B\Null(T)
\]

は、定義した conditional moment system については exact である。しかし、任意の null direction から作る bridge が、

- 正値性を満たす
- 単一の選択機構から生成される
- 重複 block 間で整合する
- 同じ full-data law と observed-data law を生成する

ことまでは保証していない。

従って、現行定理は「緩和モーメントモデルの exact fiber」と呼ぶべきである。実際の MNAR モデルの identified set とするには、

\[
\Omega_{\mathrm{adm}}
=
\{\omega:\omega>0,\ \omega\text{ が単一の選択機構と整合する}\}
\]

との交差を明示した model-level theorem が必要である。

#### (b) 共同識別を示す実質的な latent model 例がない

有限潜在クラス、連続 anchor、因子分析、Rasch の多くは、

1. shadow 法で block law または protected moments を回復
2. 既知の complete-data identification を適用

という逐次結果である。

これは重要な統合結果だが、「bridge が非一意でも潜在構造との共同制約により母数が識別される」という中心メッセージそのものではない。

AoS向けには、次を満たす一つの完全な確率モデル例が必要である。

1. 各 block の shadow completeness は失敗する
2. bridge は実際に複数存在する
3. それでも共有 latent restriction により対象母数が一意になる
4. admissibility と observed-law compatibility を満たす

#### (c) 連続理論の多くは一次線形化上の結果である

continuous totality の中心は、

\[
\Null(CJ)=\{0\}
\iff
\overline{\operatorname{Range}(J^*C^*)}=\mathcal H
\]

という Hilbert 空間の双対性である。これは derivative の単射性を与えるが、無限次元非線形写像の局所単射性を自動的には与えない。

また、\(\pi>0\) だけから構成した tangent direction が正の propensity path に実現可能かを示す必要がある。現行版は linear relaxation と実際の tangent cone を区別できていない。

#### (d) minimax・one-step・weak-ID は元の MNAR 実験へ未接続

minimax 節は Gaussian sequence experiment 上の標準上下界であり、元の observed-data experiment からの LAN embedding または asymptotic equivalence が未証明である。

one-step 節は必要な remainder 条件を仮定に置いた高水準 CLT、weak-ID 節は一般的な test inversion である。これらを現段階で「本モデルの推論理論」として主貢献に数えるべきではない。

### 3.2 最も有望な結果

有限 support の selection cancellation と Rado--Hall capacity condition が最も有望である。

\[
\mathsf T_S(z,y)
=P(R_S=1,Y_S=y\mid Z_S=z),
\]

\[
\mathsf D_S
=\operatorname{diag}\{P(R_S=1,Y_S=y)\},
\]

に対して、

\[
\mathsf H_S=\mathsf T_S\mathsf D_S^{-1}
=\frac{P(Y_S=y\mid Z_S=z)}{P(Y_S=y)}
\]

となり、local rank condition から selection probability が消える。この cancellation はモデル固有であり、stagewise completeness より弱い joint rank condition を与える。

さらに各 block の latent tangent row space \(V_S\) と shadow contrast capacity \(r_S=q_S-1\) に対し、

\[
\dim\left(\sum_{S\in\mathcal I}V_S\right)
+\sum_{S\notin\mathcal I}r_S
\ge p
\quad\text{for all }\mathcal I
\]

という Rado--Hall 型条件は、blockwise information をどう組み合わせれば全 latent direction を識別できるかを sharp に表す。

ただし、one-witness から genericity を導くには、shadow table と latent law を analytic family 内で独立に摂動できる variation-independence を追加する必要がある。

## 4. Annals向けに一本へ絞る場合

### 推奨する中心テーマ

> Joint identification of latent measurement models under nonunique MNAR bridges

### 主定理候補

#### 主定理1: model-level quotient identified set

正値性、admissibility、単一選択機構、重複 block の global compatibility を含む実際の observed-data model について、latent parameter の identified set を特徴付ける。

#### 主定理2: finite-support sharp identification

selection cancellation と Rado--Hall condition により、block shadow capacity が latent tangent space を識別するための必要十分条件を与える。

### Corollary / worked example

- finite latent class の pair-\(W\) tensor
- \(K=1\) の非識別
- 線形一因子または Rasch のうち一つ

factor と Rasch を両方主応用にすると焦点がぼける。星野先生への応用上の返答としては両方を整理してよいが、AoS本文では一つを完全な worked example とし、他方は supplement または別稿とする。

### 本文から外す候補

- continuous spectral/Baire genericity
- 一般 PSMD
- abstract Gaussian sequence minimax
- DQM/LAN の一般論
- oracle weak-ID projection

これらは別稿または supplement の研究課題とする。

## 5. 既存研究との境界

以下は新規性として単独では主張できない。

- latent variable model と MNAR mechanism の同時推定
- 因子負荷または Rasch difficulty の推定
- bridge が非一意でも線形 functional が識別され得ること
- weakly identified nuisance の下で strongly identified target を推定する一般論
- deep latent MNAR model の識別

本研究の防御可能な新規性候補は、次の組合せである。

\[
\boxed{
\begin{gathered}
\text{非一意な blockwise MNAR bridges}\\
+\text{共有 latent measurement restrictions}\\
+\text{selection cancellation}\\
+\text{sharp block-capacity condition}
\end{gathered}}
\]

ただし、この主張は model-level identified set と strict-extension example を完成させて初めて成立する。

## 6. オンラインレビュー研究との切り分け

星野先生への返信で、潜在変数理論とオンラインレビュー実験を別研究として整理したことは妥当である。

レビュー研究の中心は、

\[
\max_{\boldsymbol R_i}
\sum_{j=1}^J R_{ij}U_{ij}
\quad\text{s.t.}\quad
\sum_{j=1}^J R_{ij}\le K_i
\]

が生む capacity-constrained multivariate MNAR である。

ただし、これを現段階で単純に

> Roy model への多変量 shadow-IV の応用

と呼ぶのは強すぎる。exact top-\(K\) は complete case を構造的に消し、blockwise shadow exclusion も自動ではないためである。

安全な説明は次である。

> オンラインレビューを、複数経験が有限の開示予算を競う capacity-constrained selective disclosure model として定式化し、oracle と public の分布差を実験で測定する。shadow-IV による回復は、supported block、overlap、block-specific exclusion を確認した上で追加分析とする。

この整理なら、倫理申請を先行させても理論論文の未解決点と衝突しない。

## 7. 次の証明作業

優先順位は次のとおりである。

1. 実際の observed-data model と admissible bridge class を定義する
2. model-level identified set theorem を証明する
3. 非一意 bridge でも latent parameter が識別される完全な finite-support DGP を構成する
4. Rado--Hall genericity に必要な variation-independence を定式化する
5. 星野先生の三層表を本文導入へ移し、定理が答える範囲を明示する
6. factor または Rasch の一方で完全な応用節を作る
7. ここまで完成してから日本語 AoS 構成へ再編集する
8. 日本語稿の論理を固定した後、英語稿と AoS 書式を作る

## 8. 現時点の判定

星野先生の問題提起には研究価値がある。特に、

> 顕在分布の回復後に潜在変数を単に当てはめる

だけでなく、

> 非一意な MNAR bridge と潜在測定構造を同時に課すことで、個別には識別不能なものを共同で識別する

ところまで到達できれば、強い理論論文になる。

しかし83頁版は、その主張を完全な確率モデル上でまだ証明していない。現段階では「多くの条件付き解法を含む研究プログラム」であり、AoS投稿稿へ進むには finite-support の主定理へ焦点を絞る必要がある。
