# main.tex 修正案: d'Haultfoeuille (2010) 型欠測IVへの整合

## 目的

指摘「最初の欠測IVが JoE 2011 になっている／識別方法が違う」に対応し、`manuscript/main.tex` が以下の主張として正確に読めるように修正する。

- 基礎文献は Kano and Takai (2011) ではなく、d'Haultfoeuille (2010), Journal of Econometrics 154(1), 1--15。
- 識別の核は、潜在変数に依存するNMARをSEM多母集団分析で処理する方法ではなく、shadow variable / missing IV による
  \[
  R \perp Z \mid Y
  \]
  と積分方程式
  \[
  \mathbb E\{R/\pi(Y)\mid Z\}=1
  \]
  のベクトル拡張。
- 本稿の拡張は、スカラー \(Y\) をベクトル \(\bm Y=(Y_1,\ldots,Y_K)'\) に置き換え、
  \[
  R \perp V \mid \bm Y,\qquad
  \mathbb E\{R/\pi(\bm Y)\mid V\}=1
  \]
  によって \(\pi(\bm Y)\) と \(P(\bm Y,V)\) を識別する、という形で書く。

## 現状評価

`main.tex` はすでに大筋では d'Haultfoeuille (2010) 型になっている。

- `2011`, `Kano`, `Takai` への直接参照は `main.tex` 内にない。
- Abstract と Introduction は d'Haultfoeuille (2010) の shadow variable 識別をベクトル値 \(\bm Y\) に拡張する、と書いている。
- 旧稿の itemwise 条件 \(D_j\perp V\mid Y_j\) と積重み \(\prod_j\pi_j(Y_j)\) は、主仮定ではなく「旧稿からの修正点」として扱われている。
- 中心方程式は正しく
  \[
  w(\bm y)=1/\pi(\bm y),\qquad
  \mathbb E\{Rw(\bm Y)\mid V\}=1
  \]
  と書かれている。

ただし、査読者・共同研究者に「識別方法が違う」と読まれないためには、以下の補強が必要。

## d'Haultfoeuille (2010) との差分整理

| 論点 | d'Haultfoeuille (2010) | 現在の main.tex | 修正方針 |
|---|---|---|---|
| 観測構造 | \(D\) は常時観測、\(D=1\) のとき \(Y,Z\) 観測。\(Z\) の分布は識別済み。 | \(V\) は常時観測、\(R=1\) のとき \(\bm Y\) 観測。 | `Our vector model` 冒頭に「これは d'Haultfoeuille の Assumptions 1--2 のベクトル版」と明記する。 |
| 除外制約 | \(D\perp Z\mid Y\) | \(R\perp V\mid \bm Y\) | 「通常IVではなく、欠測機構からの排除制約」と強調する。 |
| 関連性/ランク | completeness: \(\mathbb E\{a(Y)\mid Z\}=0\Rightarrow a(Y)=0\) | vector completeness: \(\mathbb E\{a(\bm Y)\mid V\}=0\Rightarrow a(\bm Y)=0\) | scalarからvectorへの拡張で仮定が強くなることを明記する。 |
| 識別対象 | \(\pi(Y)\), \(P(Y,Z)\), 関心汎関数 | \(\pi(\bm Y)\), \(P(\bm Y,V)\), \(\mathbb E(\bm Y)\) | 主定理はここまでを d'Haultfoeuille 拡張として書く。 |
| 潜在関数 \(g,h_j\) | 原論文の主対象ではない | \(P(\bm Y,V)\) 復元後に追加仮定で識別 | 二段階目は「d'Haultfoeuille 識別そのもの」ではなく「復元分布に基づく追加的な潜在測定モデル識別」と明確に分離する。 |
| 2011型潜在NMAR | なし | 付録Dで「\(R^*=k(F)+\eta\) では shadow条件が破綻」として扱う | Kano and Takai型の議論は主結果に混ぜない。必要なら参考文献・関連研究でのみ言及。 |

## 具体的修正案

### 1. Abstract を二段階識別として明確化

現状の Abstract は概ね正しいが、潜在測定関数まで d'Haultfoeuille 条件だけで識別されるように読める可能性がある。

修正方針：

- 第1段階：vector shadow condition と completeness により \(\pi(\bm Y)\), \(P(\bm Y,V)\), \(\mathbb E(\bm Y)\) を識別。
- 第2段階：復元された \(P(\bm Y,V)\) に追加の潜在測定モデル識別条件を課して \(g,h_j\) を識別。

差し替え候補：

```tex
本研究では，d'Haultfoeuille (2010) の shadow variable / missing IV 識別を，
スカラーの欠測アウトカムからベクトル値の欠測変数
\(\Y=(Y_1,\ldots,Y_K)'\) へ拡張する。
第一段階では，欠測指標 \(R\) が \(\Y\) に依存しても，
\(\Y\) を条件づけると常時観測変数 \(V\) が欠測機構から排除される
\(R\indep V\mid \Y\) と vector completeness の下で，
\(\pi(\Y)=\Prb(R=1\mid\Y)\)，\(P(\Y,V)\)，および \(\E(\Y)\) が識別される。
第二段階では，復元された \(P(\Y,V)\) に
\(\Y=\bm h(F)+\eps,\ F=g(V)+U\) という潜在測定モデルの識別条件を課すことで，
\(g\) と \(h_1,\ldots,h_K\) の識別を議論する。
```

### 2. Introduction に「2010 JOE が基礎」と明記

現状でも d'Haultfoeuille (2010) を引用しているが、冒頭の「この非識別性に対する解決策」の段落で、Journal of Econometrics 154(1), 1--15 を明示してよい。

追加候補：

```tex
本稿の出発点は，d'Haultfoeuille (2010, Journal of Econometrics)
の ``A new instrumental method for dealing with endogenous selection''
である。同論文の識別戦略は，通常の処置効果IVのように
「操作変数がアウトカムから排除される」ことではなく，
「アウトカムを条件づけたとき，操作変数が選択・欠測指標から排除される」
ことに基づく。
```

### 3. `Existing shadow-variable strategy` に d'Haultfoeuille の仮定対応を追加

現状は要点を説明しているが、原論文との差分比較を本文で明示すると誤解が減る。

追加候補：

```tex
d'Haultfoeuille (2010) では，\(D\) は選択ダミー，
\(Y\) は欠測し得るアウトカム，\(Z\) は操作変数である。
観測構造は，\(D=1\) のとき \(Y\) が観測され，
\(Z\) の分布は本標本または補助情報から識別されている，というものである。
本稿では記号を欠測データ文脈に合わせて \(D\) を \(R\)，
\(Z\) を \(V\)，スカラー \(Y\) をベクトル \(\Y\) に置き換える。
```

### 4. `Our vector model` 冒頭に「d'Haultfoeuilleのベクトル版」を定義

現状は潜在因子モデルから始まるため、読者によっては Kano and Takai 型の「潜在変数依存NMAR」へ見える可能性がある。

修正方針：

`Our vector model` の最初に、まず d'Haultfoeuille の三つ組 \((D,Y,Z)\) と本稿の \((R,\Y,V)\) の対応表を置く。

追加候補：

```tex
本節の主対象は，d'Haultfoeuille (2010) の
\((D,Y,Z)\) を
\[
  D\mapsto R,\qquad
  Y\mapsto \Y,\qquad
  Z\mapsto V
\]
と置き換えたベクトル版である。
ここで \(R\) は完全ケース指標，\(\Y\) は同時分布を復元したい欠測変数ベクトル，
\(V\) は常時観測される shadow variable である。
潜在因子 \(F\) は，\(V\) と \(\Y\) の関連性・completeness を支える構造として導入する。
```

### 5. `潜在測定モデルの識別条件` を「追加仮定」として弱く書く

現状：

```tex
これは，非線形測定誤差モデルまたは Hu--Schennach 型の識別定理に対応する仮定である。
```

これはよいが、d'Haultfoeuille 型識別と混同されやすい。

修正候補：

```tex
この仮定は d'Haultfoeuille (2010) の shadow-variable 識別そのものではなく，
第一段階で復元された \(P(\Y,V)\) に対して潜在測定関数を回復するための
追加的な測定モデル識別条件である。
```

### 6. Theorem を二つに分ける現状は維持し、説明を追加

現状の定理構成は適切：

- Theorem `thm:vector-shadow-identification`: d'Haultfoeuille 型のベクトル拡張。
- Theorem `thm:vector-iv-functions`: 復元分布に基づく追加的な潜在関数識別。

ただし、Theorem 2つの間に以下を追加する。

```tex
定理 \ref{thm:vector-shadow-identification} が本稿における
d'Haultfoeuille (2010) の直接のベクトル拡張である。
次の定理は，この識別結果で得られた \(P(\Y,V)\) を入力として，
潜在測定モデルの関数を回復する第二段階の結果である。
```

### 7. `single always-observed V` の表現を慎重にする

現状では「単一の常時観測IV」と強く書いているが、vector completeness は \(V\) のサポート・次元に強い条件を要求する。スカラー \(V\) で高次元 \(\Y\) を識別できるかはかなり強い仮定になる。

修正方針：

- 「単一の変数」より「一組の常時観測補助変数 \(V\)」を基本表現にする。
- スカラーでもベクトルでもよいが、vector completeness が要求されると書く。

差し替え候補：

```tex
本稿では \(V\) をスカラーまたはベクトル値の常時観測補助変数として扱う。
記法上は単に \(V\) と書くが，ベクトル値 \(\Y\) に対する completeness を満たすには，
\(V\) のサポートと \(\Y\) との関連性が十分に豊かである必要がある。
```

### 8. Appendix D の位置づけを本文で先に予告

指摘された「識別方法が違う」は、潜在因子依存欠測 \(R^*=k(F)+\eta\) と本文の \(\Y\) 依存欠測を混同している可能性がある。

Introduction または Identification に以下を追加する。

```tex
重要な区別として，本稿の主結果は欠測が \(\Y\) に依存する
\(R^*=k(\Y)+\eta\) 場合に関する。
欠測が潜在因子そのものに依存する \(R^*=k(F)+\eta\) 場合には，
一般に \(R\indep V\mid \Y\) は成立せず，d'Haultfoeuille 型の証明は適用できない。
この場合は Appendix \ref{app:latent-factor-missingness} で非識別または別アプローチの問題として扱う。
```

### 9. References に Kano and Takai (2011) を入れるなら「関連研究」に限定

現状 `main.tex` には Kano and Takai (2011) は入っていない。このままでもよい。

もし入れるなら、主識別文献ではなく、関連研究・付録Dの文脈に限定する。

文例：

```tex
潜在変数に依存するNMAR欠測を，欠測機構を明示的に指定せず
SEMの多母集団分析として扱う別方向の研究として
Kano and Takai (2011) がある。
本稿の主結果はこれとは異なり，欠測が \(\Y\) に依存し
\(R\indep V\mid\Y\) が成立する場合の shadow-variable 識別である。
```

## 優先修正順

1. Abstract を二段階識別に書き換える。
2. Introduction に d'Haultfoeuille (2010, JoE 154) が基礎文献であることを明記する。
3. `Our vector model` の冒頭に \((D,Y,Z)\to(R,\Y,V)\) 対応表を入れる。
4. Theorem 2つの間に「第1定理がd'Haultfoeuille拡張、第2定理は追加的潜在測定モデル識別」と書く。
5. \(V\) を「単一の常時観測変数」と強く言い切る箇所を、「スカラーまたはベクトル値の常時観測補助変数」に弱める。
6. 潜在因子依存欠測 \(R^*=k(F)+\eta\) は主結果ではないことを本文で予告する。

## 現時点で main.tex に残してよい部分

- `Existing shadow-variable strategy`
- `Definition and basic equation`
- `Our vector model`
- `Main identification results`
- `旧稿からの修正点`
- Appendix の additional measurement error / empirical Bayes completeness / latent-factor missingness / proxy-type

これらは、指摘への対応として削除する必要はない。むしろ、上記の補強により「主結果は d'Haultfoeuille (2010) のベクトル拡張であり、潜在変数モデルは第2段階または補助構造である」と明確化するのがよい。

## 結論

`main.tex` は現状でも JoE 2011 / Kano--Takai 型を主張してはいない。ただし、潜在因子モデルの説明が前面に出ているため、読者が「潜在変数依存NMARの別識別法」と誤読する余地がある。修正の中心は、本文冒頭と識別節で d'Haultfoeuille (2010) との対応を明示し、shadow-variable 識別と潜在測定モデル識別を二段階に分離して書くことである。
