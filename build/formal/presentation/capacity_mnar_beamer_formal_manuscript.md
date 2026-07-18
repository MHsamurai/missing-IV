# 欠測IVと潜在変数モデリングによる非無作為欠測の識別：発表原稿

この原稿は `capacity_mnar_beamer_formal.pptx` の発表者ノートに対応する。

## Slide 01: Title

本日は「欠測IVと潜在変数モデリングによる非無作為欠測の識別」について報告します。オンラインレビューを、有限の公開枠をもつgeneralized Roy型のmultiple selectionとして表し、そこから生じる多変量MNARを扱います。中心は、平均評価や極端評価率をtarget-specific bridgeによりノンパラメトリックに回復し、その性能をoracle評価と比較する実験です。

## Slide 02: 容量制約付きレビューはgeneralized Roy型の多変量MNARである

MNARでは未観測の評価そのものが公開確率を動かすため、公開レビューだけの分布は母集団分布を一般に表しません。d'Haultfoeuilleはshadow variableと完備性によりスカラー欠測アウトカムの分布をノンパラメトリックに識別しました。多変量MNARにはself-censoringとno self-censoringがあります。本研究では、個人が複数の評価を持ちながら有限件しか公開できない状況を扱い、平均評価と極端評価率を直接識別し、容量とランキングの効果を実験的に検証します。

## Slide 03: 選択方程式はgeneralized Roy modelに含まれる

最初に査読上の位置づけを明確にします。各候補に公開効用があり、その上位K件を選ぶ選択方程式は、capacity constraintを伴うgeneralized Roy modelに含まれます。d'Haultfoeuille自身もshadow IVの適用例として未観測部門をもつRoy modelを挙げています。したがって、Roy modelへshadow-variable法を適用すること自体を方法論的新規性とは主張しません。貢献は、レビュー生成をexact top-Kの多変量MNARとして実装し、構造的ゼロ、cross-item crowd-out、oracle/public比較、Kとランキングのランダム化を一つの設計で検証する点です。

## Slide 04: 既知なのは極端性、未解明なのは経験間の競争である

レビューのpolarity self-selectionは既知です。Schoenmueller、Netzer、Stahlは、低頻度レビュアーほど1星と5星が多く、self-selected reviewはforced reviewより極端になることを示しました。本研究が追加するのは、あるレビュー候補の公開確率が、その候補自身の評価だけでなく、同じ個人が持つ他の候補との競争によって変わるというcross-item crowd-outです。Kが小さくなると、より強い経験が有限枠へ集中するという因果比較を行います。

## Slide 05: Strategic sample selectionを欠測パターンへ写像する

Di Tillio、Ottaviani、Sorensenは、k個の候補から上位n個だけを観測するselected experimentを分析しました。本研究ではpresample size kを経験数m、sample size nを公開枠Kに読み替えます。経済モデル上の選択集合を欠測パターンDとして表し、公開されたときだけYが観測される多変量MNARへ写像します。選択そのものの一般理論ではなく、この写像とレビュー実験が本研究の焦点です。

## Slide 06: 既存の多変量MNARはtop-Kの支持集合と両立しない

self-censoringは自己値による欠測を許しますが、識別にはsupported patternのpositivityとupward closureを用います。no self-censoringは自己値が自己の欠測を直接動かさないと仮定し、完全ケースpositivityを置きます。exact top-Kでは全ての観測パターンがK個の1だけを持つため、完全ケースは存在せず、upward closureも成立しません。そこで本文では、full joint lawを狙わず、項目別のtarget-specific bridgeにより平均や裾確率を直接回復します。

## Slide 07: 公開効用はpositive WOMとnegative WOMの二経路をもつ

公開効用は、肯定的経験を共有するpositive word of mouthと、否定的経験を警告するnegative word of mouthの二経路で表します。評価の正側と負側が異なる係数で公開効用へ入るため、対称なU字型の極端性選択と、5星側が厚いJ字型の方向非対称を分けて議論できます。この効用表現は、レビュー文献の極端性とvalence asymmetryをtop-K選択へ接続する役割を持ちます。

## Slide 08: 容量制約が公開集合を決める

個人は公開効用の合計を最大化する集合を、時間・注意・文章化コストの予算内で選びます。exact top-Kは、同順位がなければ公開効用の上位K件を選ぶ特殊ケースです。このとき公開指標Dは評価ベクトル全体に依存し、項目ごとの独立な欠測ではありません。

## Slide 09: 命題1：Top-Kは自己単調性とcrowd-outを生む

他の公開効用を固定すれば、項目jの公開効用が上がるとjの公開指標は弱く増加します。一方、j自身と他の残りの候補を固定して、競合項目lの公開効用だけを上げると、jは弱く公開されにくくなります。後者がexperience-level crowd-outであり、自己値だけに依存するitemwise selectionとの主要な違いです。

## Slide 10: 命題2：公開容量が小さいほど選択効用は高くなる

公開効用を降順に並べると、上位K件の平均はKが小さいほど高くなります。ただし、この結論を評価の極端性へ移すには、公開効用の順位と極端性の順位が整合するという追加条件が必要です。公開効用にノイズがあるだけでは順位一致は従わないため、理論上の選択効用と実証上の極端性を区別します。

## Slide 11: 実験仮説：U字型の裾過剰とJ字型の非対称を区別する

正側と負側のsalienceが対称で、公開効用の順位が極端性順位と整合し、選択が非退化なら、公開レビューは両側の裾を過剰に含みます。これはU字型またはpolarizationです。J字型には、正側の係数が大きい、あるいは母分布自体が正側に偏るという非対称性が必要です。この部分はRoy構造だけから自動的には従わないため、実験仮説として検証します。

## Slide 12: 観測データは完全ケースを含まないpattern dataである

観測データは、常時観測される共変量、容量、shadow signal、公開パターンD、そして公開項目の評価からなります。exact top-KではDの合計がKで固定されるので、Kがmより小さい限り完全ケースは構造的に存在しません。これは標本数を増やしても解消しないsupport restrictionです。

## Slide 13: Supported blockが観測可能な同時分布を定める

項目集合Sの全てが同時に公開された指標をR_Sとします。R_Sが正の確率で1になる集合をsupported blockと呼びます。exact top-KではSの大きさがK以下でなければなりません。supported blockごとにスカラーの観測指標を作れるため、付録ではinverse-selection bridgeによる分布識別も整理します。

## Slide 14: 識別対象は支持される周辺分布と汎関数である

本文の主要対象は各項目の平均評価、1星・5星率、極端性です。Kが2以上ならsupported pairの共分散も候補になります。しかし、Kを超える大きさのブロックは同時観測されないため、追加構造なしにfull joint lawを識別することはできません。この識別境界を最初に明示します。

## Slide 15: 定理1：完全ケース法は構造的ゼロにより適用できない

Kがmより小さいと、完全ケース指標は確率1でゼロです。したがって、完全ケースを選択確率で割った条件付き期待値を1にする通常のmissing-IV momentには解が存在しません。完全ケース法が使えない理由は推定精度ではなく、モーメント自体がデータ生成過程のsupport上で消えていることです。

## Slide 16: 定理1：supported blockを超える結合分布は非識別である

m=2、K=1の反例を示します。Y1とY2を独立にしても、完全相関にしても、毎回どちらか一方しか観測されないなら同じ観測データ法則を作れます。しかし二変量共分散は異なります。したがってfull joint lawは一般に非識別であり、本文で扱う対象を低次元汎関数に限定する必要があります。

## Slide 17: 本文の識別対象は平均・裾確率である

項目jについて、Rを公開指標、Yを私的評価、Vを事前期待などのshadow signalとします。常時観測文脈Cには個人属性、ランダム化容量、他項目の常時観測signalを含めます。対象はtheta_j,tauとして、平均、1星・5星率、中心からの絶対偏差を表すtauに限定します。full-data lawを先に識別せず、必要な汎関数を直接扱います。

## Slide 18: Target-specific representer bridgeを明示する

維持仮定は三つです。第一にitemwise positivity、第二にYとCを条件づけたshadow exclusion、第三にtarget-specific representer deltaの存在です。deltaを回答者のV分布で条件付き平均するとtau(Y,C)になることを要求します。解の存在は必要ですが一意性は不要です。このrange conditionは対象識別の便利な十分条件として用い、一般的な必要十分条件とは主張しません。またpositivityが成立しない場合、対象をoverlap populationへ限定します。

## Slide 19: 定理2：対象汎関数はfull lawなしに識別できる

Rが1の部分では観測されたtauを用い、Rが0の部分では常時観測VとCから計算したdeltaを用います。shadow exclusionにより、回答者で成立するbridgeの条件付き平均は非回答者にも移せます。そのため両部分を足した観測データ汎関数が母集団のthetaに一致します。これが本文の主たるノンパラメトリック識別結果です。

## Slide 20: 5段階評価ではbridge存在条件をrankで確認できる

YとVが有限サポートなら、回答者で観測できるH行列を使います。Hの行はYの5カテゴリー、列はVのカテゴリーです。bridge equationはH delta equal tauです。特定の平均や裾確率にはtauがHのrangeに入ればよく、全ての汎関数を扱うfull row rankは十分条件ですが必要ではありません。これはfull-law識別の完備性より弱い条件です。

## Slide 21: Model 1：top-Kの下ではshadow exclusionを追加仮定する

top-Kでは公開指標が他項目評価と選択ショックに依存するため、shadow exclusionはRoy構造から自動的には従いません。十分条件の一例として、VがY_jと常時観測Cを条件づけた後、他項目評価、選択ショック、個人の公開コストから独立であり、公開効用へ直接入らないことを置きます。事前期待は期待不一致を通じて公開意欲へ直接入り得るので、時間的に先行するだけでは不十分です。二波測定、時点付きログ、複数signal、感度分析で妥当性を補強します。

## Slide 22: 発展：潜在変数はsupported blocksを結ぶ追加構造である

潜在変数は本文のtarget-specific結果に必要ではありません。full-law回復を目指す発展として、三つのanchor itemがjointly supportedで、その結合分布が付録の強い完備性条件により識別される場合を考えます。さらに条件付き独立な測定、作用素のinjectivity、位置尺度の正規化を置きます。

## Slide 23: 定理3：測定モデルはsupported blocksを接続する

三測定識別の条件の下で、潜在因子の条件付き分布と各項目の測定kernelを識別します。これにより、supported blockを横断して潜在構造を接続できます。ただし低ランク因子モデルだけではvector completenessは出ません。anchor support、measurement injectivity、正規化が必要であり、本文の実験的貢献とは分けて扱います。

## Slide 24: 実験1：oracleとpublicを同一標本から取得する

共通候補30から40サービスから、少なくとも約10サービスを利用した参加者をscreeningします。全サービスのprivate ratingと利用情報を先に取得し、回答をlockします。その後、Kを1件または3件へランダム割当し、forced random-3を比較群に置きます。自己選択群は指定件数だけ公開対象を選び、選択対象だけ自由記述を書きます。基本報酬は評価方向や選択対象に依存させません。標本数は三群比較と個人内相関を含む検出力計算で決めます。

## Slide 25: 実験1：shadow測定時点と検証範囲を分ける

回顧的な利用前期待にはrecall biasがあるため、valid shadowと自動的には扱いません。confirmatoryなtarget-specific識別には、二波設計または時点付きログで評価形成前のsignalを得ます。実験が直接検証できるのはcapacity effect、crowd-out、oracleに対する回復性能です。shadow exclusionやbridge existenceそのものはデータだけで証明できません。現行の回顧測定だけなら単調性boundsと感度分析を併記します。

## Slide 26: Oracleとnaiveを同じperson-average targetで比較する

比較対象は、各人についてm項目の汎関数を平均し、その後に個人間で平均するperson-average targetです。oracleもnaiveも個人を同じ重みで扱います。naiveは公開K件の平均ですが、選択が評価に依存するため一般にはoracle targetへ一致しません。ここでestimandの違いによる見かけの差を排除します。

## Slide 27: Representer bridgeの有限標本回復をoracleで評価する

推定量は、公開項目には観測されたtau、非公開項目には推定したrepresenter deltaを代入して全person-itemで平均します。主要対象は平均、1星・5星率、極端性です。representer推定量がnaiveよりoracleに近いかを有限標本上の回復仮説として評価します。項目ごとにbridgeが異なる場合は項目別に推定して平均し、poolingには交換可能性または共通bridgeを別途仮定します。

## Slide 28: 実験2はランキングをランダム化して増幅を識別する

実験1の公開レビューpoolから同数L件のfeedを作り、random order、helpfulness ranking、LLM rankingへ閲覧者をランダム割当します。スコアとtie-breakingは事前固定します。各algorithm feedとrandom feedの差により、投稿後の表示選択が極端性をどこまで増幅するかを因果的に評価します。スコアが極端性に単調という補助命題と、実際のランダム化比較は区別します。

## Slide 29: 結論：Roy型選択の対象汎関数を直接回復する

選択方程式はgeneralized Roy modelに含まれ、shadow-variable法のRoy応用は既知です。本研究の貢献は、exact top-Kレビューを構造的ゼロとcross-item crowd-outをもつ多変量MNARとして実装し、Kをランダム化して検証することです。full joint lawは一般に非識別ですが、target-specific representerが存在すれば平均と裾確率をfull lawなしにノンパラメトリックに識別できます。最後にoracle回復とalgorithmic amplificationを別々に評価します。

## Slide 30: 参考文献

本文で直接用いた文献を示します。d'Haultfoeuilleの欠測IVとRoy応用、Li、Miao、Tchetgen Tchetgenのrepresenter条件、self-censoringとno self-censoring、strategic sample selection、レビューのpolarity self-selectionが中心です。

## Slide 31: 付録A：スカラー欠測IVのノンパラメトリック識別

付録ではまずd'Haultfoeuille型の基準結果を確認します。shadow exclusion、positivity、B-completenessの下で、inverse selection probabilityは条件付きモーメントの唯一解です。これは分布全体を回復する強いbenchmarkです。

## Slide 32: 付録B：Zhao--Shaoのconditional shadow表現

Zhao--Shaoでは常時観測Xを条件づけたshadow conditionを用います。回答者でのV given Y,X分布が母集団と一致することをBayes則で示します。本研究の本文はGLMではなく、target-specific representerを用いたノンパラメトリック汎関数識別へ置き換えています。

## Slide 33: 付録C：完全ケース版の仮定

完全ケース指標が正の確率で1になるbenchmarkでは、ベクトルY全体にshadow exclusion、positivity、completenessを置けます。正の候補関数qが完全ケースモーメントを満たすとします。

## Slide 34: 付録C：完全ケース版の結論と適用範囲

前頁の仮定の下で、qは真の完全ケース確率に一致し、full-data lawが識別されます。ただしexact top-Kでは完全ケース確率がゼロなので、このbenchmarkは本文へ直接適用できません。

## Slide 35: 付録D：完全ケース版の一意性証明

候補解と真の選択確率の比からgを作り、条件付きモーメントを引き算します。gは下有界かつ可積分で、条件付き期待値がゼロになります。B-completenessによりgがゼロとなり、候補解の一意性が従います。

## Slide 36: 付録E：分布全体の識別には強い仮定を置く

supported blockについても、positivity、blockwise shadow exclusion、全ての下有界可積分関数を分離するcompletenessを置けば、分布全体を識別できます。本文のrepresenterは一つのtauに対する解の存在だけを要求するのに対し、ここでは全関数を扱う強い条件を置きます。

## Slide 37: 付録E：inverse-selection bridgeによるfull-law識別

inverse-selection bridgeは選択確率の逆数で、R掛けるomegaのV,C条件付き平均が1になります。completenessによりomegaを一意にし、IPW表現でsupported-block law全体を回復します。本文のrepresenter bridgeは一意性不要のtarget-specific条件、付録のinverse-selection bridgeはfull-law条件です。

## Slide 38: 付録E：supported-block定理の証明

証明は完全ケース版と同じです。真の選択確率と候補解の比からgを作り、shadow exclusionで条件付き期待値をゼロにします。B-completenessでgをゼロにし、最後に反復期待値で回復式を得ます。

## Slide 39: 付録F：有限サポートの完備性はrank条件になる

有限サポートでは、Y given V,Cの条件付き確率行列がfull column rankを持てばcompletenessが成立します。複数signalは分離能力を増やし得ますが、同じ情報を複製してもrankは増えません。これはfull-law用の強いrank条件です。

## Slide 40: 付録G：self-censoringの支持条件まで比較する

self-censoringは自己値依存を許すだけでなく、supported patternのpositivityとupward closureを識別に用います。したがってconditional independenceだけを比べるのでは不十分で、pattern supportの条件を併せて比較する必要があります。

## Slide 41: 付録G：exact top-Kの支持集合との相違

exact top-Kの支持集合はDの合計がKに等しいパターンだけからなります。あるsupported patternに観測項目を追加するとKを超えるため、upward closureは成立しません。既存モデルとの差はcensor relationに加え、positivityとsupport geometryにあります。

## Slide 42: 付録H：個人内ランダム選択帰無

全private ratingを持つので、Yを固定した上で公開集合が一様ランダムに選ばれる帰無を作れます。各人のtail件数Mと公開枠Kを条件づけると、公開tail件数Sはhypergeometric分布に従います。

## Slide 43: 付録H：帰無分布のモーメントとexact test

hypergeometric分布の平均と分散を使い、m=10、K=3なら120通りを列挙してexact testを実施できます。これは分布仮定を置かないcapacity selectionの検定です。

## Slide 44: 付録I：Model 2は単調性による部分識別である

shadow exclusionが疑わしい場合、Vが高いほど公開確率が単調に変わるという制約だけを置きます。同じ観測データ法則と単調性を満たすfull-data lawの集合を作り、その上で対象汎関数のidentified setを定義します。単調性だけでは一般に点識別されません。

## Slide 45: 付録I：有限サポートのboundsを計算する

有限サポートではidentified set上のinfimumとsupremumを計算します。端点が達成されるsharp boundsと呼ぶには、候補集合の閉性、コンパクト性、端点の実現可能性を別途示す必要があります。本文では未証明のsharpnessを主張しません。

## Slide 46: 付録J：Model 3はweak-but-many signalsを用いる

複数の事前signalをベクトルとして用い、joint shadow exclusionとtarget-specific range conditionを置きます。個々のsignalの予測力が弱くても、異質なsignalが対象方向を共同で分離すればrepresenter bridgeが存在し得ます。ただしsignal数や予測精度だけでは十分ではありません。

## Slide 47: 付録J：有限サポートではrankとrangeを区別する

回答者で観測できるH行列を複数signalについて構成します。特定のtauにはtauがHのrangeに入れば十分で、全てのtauを扱うfull rankはより強い条件です。複数signalを一つのF_preへ集約する場合も、集約後のHについてrange conditionを再確認する必要があります。
