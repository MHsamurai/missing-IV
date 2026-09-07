from pathlib import Path
import re

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "manuscript" / "vector_missing_iv_presentation_script_ja.docx"
BEAMER = ROOT / "manuscript" / "vector_missing_iv_identification_beamer.tex"
LATIN_FONT = "Arial"
JAPANESE_FONT = "BIZ UDPGothic"


SLIDES = [
    ("Slide 1  Title", [
        "本日は、欠測IVと潜在変数モデリングによる非無作為欠測の識別についてお話しします。知りたいのは、欠測した項目の分布だけではありません。その項目の背後にある潜在クラスと、各項目がクラスをどう測っているかも知りたい、という問題です。",
        "考え方は二段階です。まず、Missing IVを使って欠測による偏りを取り除きます。その後、重なりのある項目の組と、潜在分布を動かす変数を使って、潜在クラスの比率と測定核を分けていきます。",
    ]),
    ("Slide 2  Missing-data mechanisms and standard approaches", [
        "まず、欠測を三つに分けます。図のDは、どの項目が観測されたかを表します。Y obsは見えている部分、Y misは欠測している部分です。",
        "MCARは、欠測がYの値と関係しない場合です。MARは、見えている値で条件づければ、欠測した値には依存しない場合です。今回扱うMNARでは、欠測した値そのものにも依存します。このとき、回答者だけを分析すると、母集団とは違う人たちを見てしまうことがあります。Heckmanの選択バイアスの話にもつながります。",
        "そこで使うのが、Missing IV、別名shadow variableです。以後はMissing IVと呼びます。これを使って、欠測した人も含む母集団の分布を回復できるかを考えます。",
    ]),
    ("Slide 3  Usual IV and Missing IV", [
        "左右の図では、Zの役割が違います。左は、欠測への応用で使う通常型のIVです。観測されるかどうかのRには関わる一方、Yのモデルからは除外します。右のMissing IVは逆で、Yとは関連しますが、Yを条件づけた後にはRと独立だと考えます。共変量がある場合は、それも一緒に条件づけます。",
        "式のパイは、Yの値ごとの観測確率です。Missing IVの条件と、観測確率が正であることから、この式が成り立ちます。さらにcompletenessという、Zが識別に十分な情報を持つ条件を置くと、パイが一つに決まります。",
        "この考え方の背景にあるのが、ここに挙げた三つの研究です。d’Haultfoeuilleは、条件付きモーメントの式から母集団の分布を識別します。ZhaoとShaoは共変量を調整した除外制約の下で、GLMのパラメータを識別します。Miaoらはshadow variableによる識別を扱い、観測されたcomplete-caseの分布でcompletenessを考えます。三つとも、識別の対象や条件が全く同じというわけではありません。",
        "あとは、その逆数で観測された人を重み付けします。たとえば観測確率が半分なら、重みは2です。観測されにくい人に大きな重みを付けて、欠測した人も含む母集団全体のYの分布を回復する、という考え方です。",
    ]),
    ("Slide 4  Lemma 2.1", [
        "まず、Missing IVをベクトルYへそのまま広げる方法を、補題2.1として整理します。全項目がそろった人をcomplete caseとし、各D jの積をRとします。UはXとW、P 1はcomplete caseの中でのYとUの分布です。",
        "条件は、YとUを押さえたときのRとZの独立性、対象全体で正の観測確率、それからcomplete-caseでのcompletenessです。正確には、観測確率の逆数と候補の逆数を、P 1の下で二乗平均が有限な関数に限ります。この範囲で、式を満たすパイが一つに決まります。",
        "これは既存のMissing IVの直接の多次元拡張です。ただし、全項目がそろう確率が、対象全体で正である必要があります。そこで次に、この条件を小さなblockごとに置き直します。",
    ]),
    ("Slide 5  Latent measurement model", [
        "次に、項目の背後にある潜在変数を考えます。左の丸が、直接は見えないFです。右の四角が、Fを測る項目Y 1からY mです。構造方程式モデリング、SEMや、項目反応理論、IRTで使う測定モデルの基本形です。",
        "Q Fは、Fがどのように分布しているかを表します。Wはその分布を動かす変数で、latent shifterと呼びます。Q jは、FとXが決まったときに項目jがどう分布するか、つまり測定核です。Xは通常の共変量で、Fにも各項目にも入ります。",
        "下の式では、FとXの下で項目が独立だとして、各測定核を掛けています。それをFの分布で平均すると、Yの分布になります。有限潜在クラスでは、三つのviewに十分なランクがあれば、クラスの入れ替えを除いて分解が一つに決まります。これがAllman、Matias、Rhodesの結果です。連続因子のSEMやIRTまで同じ条件だけで識別できる、という話ではありません。",
        "一方、潜在変数とMNARを一緒に扱うモデルや推定の研究もあります。Muthénら、HolmanとGlas、LeeとTang、HarelとSchafer、Jungら、Kuhaらがこの流れです。KanoとTakaiは、通常のSEMの識別制約を置いた上での線形モデルの推定を扱っています。近年はXieらのように、深層潜在変数モデルを使う研究もあります。なので、潜在変数と欠測を一緒に扱うこと自体が、新しいわけではありません。",
    ]),
    ("Slide 6  Multivariate MNAR and the remaining gap", [
        "もう一つが、複数項目のMNARを扱う研究です。Tangらは、complete-caseの条件付き分布を使って、多変量の回帰パラメータを識別します。SadinleとReiterは、項目ごとの条件付き独立な欠測を考え、外部IVを使わずに多変量のfull-data lawを識別する流れです。",
        "Liらはself-censoringのモデルとcompletenessを、NiとShaoはnonresponse instrumentとパラメトリックな観測確率を使います。研究によって、分布全体、回帰パラメータ、母集団の要約量と、知りたい対象が違います。",
        "もう一つ、欠測モデルをどこまで決めるか、という問題があります。ZhaoとShaoが議論しているように、outcomeと欠測機構を含むモデル全体を正しく指定できれば、パラメトリックな尤度法は効率の面で有力です。ただし、selectionの関数形を間違えるとバイアスが出ます。そこで彼らは、outcomeのモデルを残しつつ、欠測機構は特定しない半パラメトリックな方法を考えています。",
        "本稿でも、selectionの関数形を決めずにノンパラメトリックに分布を回復することを重視します。ただし、何も仮定しなくてよいという意味ではありません。Missing IVやcompletenessは必要です。後半で正指定と誤指定のselection likelihoodを比べるのも、この違いを見るためです。",
        "ここで本稿が考えるのは、その先です。欠測を補正してYの分布が分かっても、それだけでQ Fと各Q jが別々に分かるわけではありません。MNARの下での分布の回復を、潜在クラス比率と測定核の一意な分解へ、どうつなぐか。ここが今回の問題です。",
    ]),
    ("Slide 7  A latent shifter is not a Missing IV", [
        "ここは少し注意が必要です。潜在分布を動かすWと、欠測を補正するZ Sは、同じ役割ではありません。Fまで条件づけるとDとWが独立でも、Fを平均して消すと、Y、W、Xの下でのFの分布が式に残ります。この分布は、一般にはWによって変わります。",
        "つまり、Wがlatent shifterだからといって、そのままMissing IVに使えるわけではありません。Z Sは欠測による偏りを取り除くために使います。Wは、その後の分布を潜在構造に分けるとき、三つ目のviewとして使います。まず回復して、その後で分解する、という順番になります。",
    ]),
    ("Slide 8  Model and assumptions", [
        "ここから第一段階です。まずはMissing IVを使って、小さな項目の組ごとに、欠測した人も含めた分布を回復します。まだ潜在クラスには分けません。そのために何を仮定するかを、順に見ていきます。",
    ]),
    ("Slide 9  Observed data and supported blocks", [
        "D jをY jの観測指標とし、Oを観測変数の集合とします。Oは常時観測されるX、W、Z、Dと、Dによって選択されたYの成分Y Dから構成されます。R Sは集合Sの全項目が観測されたことを示すblock indicatorです。R SがゼロならY Sは欠測であり、観測データには値を持つ変数として現れません。",
        "supported blockとは、対象support上でR Sが1となる条件付き確率pi Sが正のblockです。必要なのはanchor pairとextension pairsがsupportedであることであり、global complete caseではありません。",
    ]),
    ("Slide 10  Single-block data-generating structure", [
        "図は一つのsupported blockの構造です。U SはXとWの組であり、F、Z S、Y Sと関連します。Z SはFを通じてY Sを予測しますが、Y SとU Sを条件づけた後にはR Sへ直接影響しません。そのためZ SからR Sへの直接辺は置きません。",
        "一方、R Sは欠測し得るY Sに依存してよく、MNARを許容します。ここでのDAGは、本稿が用いる条件付き独立性と分布の関係を整理したものです。",
    ]),
    ("Slide 11  Overlapping supported blocks replace global complete cases", [
        "この図のように、全項目がそろう代わりに、重なりのあるペアを使います。最初のS 0は、基準となるY aとY bのペアです。この二つをanchor itemsと呼びます。残りのY jについては、共通のY aと組にしたextension pairを用意します。",
        "各ペアには、それぞれMissing IVとbridgeを置きます。まずペアごとの分布を回復し、その後、共通のanchorを使って測定核とクラスのラベルをそろえていきます。全項目を一度に観測する必要はありません。",
    ]),
    ("Slide 12  Stage-1 assumptions", [
        "仮定6は、先ほどのMissing IVの条件をblockごとに置いたものです。Y Sと共変量U Sが同じなら、Z Sは、そのblockが観測されたかどうかのR Sと独立だとします。",
        "仮定7がcomplete-case completenessです。そのblockが全て見えた人たちの中で考えます。二乗可積分な関数hについて、Z SとU Sのどの条件でも平均がゼロなら、h自体もほとんど確実にゼロだとします。違う関数を条件付き平均だけでは区別できない、ということが起きないための条件です。",
        "ここで使うのは、全項目のcomplete caseではなく、そのblockのcomplete caseです。さらに観測確率が正なので、そこで確率ゼロとなる集合と、母集団で確率ゼロとなる集合を対応させられます。",
    ]),
    ("Slide 13  New Proposition 1", [
        "ここが第一段階の結果です。本文では命題2.1に当たります。真の観測確率の逆数について、blockのcomplete caseでの二乗平均が有限だとします。",
        "その上で、このbridgeの式を満たす候補を考えます。候補は正の関数で、その逆数も同じ二乗可積分な関数の範囲に入るものです。この範囲では、観測確率パイSが一つに決まる、という命題です。真の観測確率が解になるので、ポイントは解の存在より、一意性にあります。",
        "パイSが分かれば、観測された人をその逆数で重み付けできます。すると、blockについての可積分な関数、つまり絶対値の期待値が有限な関数の平均を、母集団の平均に戻せます。平均一つだけでなく、blockの分布全体が識別できるわけです。",
    ]),
    ("Slide 14  Proof sketch the observable bridge is unique", [
        "証明の流れはこの図の通りです。まず、観測過程とsupported block、Missing IVの条件から、真のパイSがbridgeの式を満たすと分かります。次に、別の解もあるとして、二つの逆数の差を取ります。",
        "その差の条件付き平均は、blockのcomplete caseではゼロになります。completenessを使うと、差そのものがゼロです。さらにpositivityを使って、この一致を母集団でもほとんど確実な一致に広げます。あとは逆確率で重み付けすれば、blockの分布が回復できます。",
    ]),
    ("Slide 15  Finite latent-class identification", [
        "ここから第二段階です。blockの分布が分かったとして、それを潜在クラスの比率と測定核に分けられるでしょうか。anchor itemsとWを使って、この分解が一つに決まる条件を考えます。",
    ]),
    ("Slide 16  The remaining decomposition problem", [
        "第一段階で、必要なペアについて、欠測した人も含むY S、W、Xの分布が分かりました。ただ、Fそのものは見えていません。同じペアの分布を作れる潜在構造が、複数あるかもしれません。",
        "ここではXをxに固定します。式のp fがクラスの比率、GがクラスごとのWの分布、M jがクラスごとの測定核です。これらをまとめたものがシータで、ファイxは、シータからペアの確率を並べたテンソルTを作る対応です。同じ観測データの分布を作る値どうしは、Lewbelの言葉でobservationally equivalentと呼びます。第一段階によって、観測データの分布が同じなら、回復したテンソルも同じになります。",
        "ただし、クラス1と2の名前を入れ替えるだけでは、データの分布は変わりません。順序を決めなければ、識別されるのは、この入れ替えを同じものとみなした同値類です。anchorの順序で名前もそろえると、正規化したパラメータ空間で一つの値に決まります。",
    ]),
    ("Slide 17  Identification strategy", [
        "全体の流れを、この図で見ます。まずblockの分布を回復し、それをテンソルに並べます。テンソルは、ここでは確率を並べた多次元の表だと思ってください。",
        "最初に、Y a、Y b、Wからなるanchorのテンソルを分解します。これでp、Gと、二つのanchorの測定核が分かります。次にpとGからWごとのクラス比率を求め、残りの項目はextensionの式を一つずつ解いていきます。全部を一度に分解するのではなく、基準を決めてから広げる順番です。",
    ]),
    ("Slide 18  Lemma 3.1", [
        "この補題は、残りの項目の式を一つに解けることを保証します。使うのはKhatri–Rao積で、対応する列どうしのクロネッカー積を並べたものです。",
        "AとBにはゼロの列がないとします。二つの列Kruskal rankの和がrプラス1以上なら、この積は列フルランクになります。つまり、anchorを分解するときの条件から、extensionを解くためのランクも確保できる、という役割です。",
    ]),
    ("Slide 19  Assumption 3.1", [
        "仮定3.1はcovariate-assisted anchor-pair structureです。class数rは既知です。anchor decompositionには、anchor pairのsupportedness、正のclass比率とWの周辺確率、M a、M b、GのKruskal rank条件を用います。これはAllman、Matias and Rhodesのthree-view conditionと同じです。",
        "既知のanchor scoreの厳密順序で共通labelを固定します。extension propagationでは全extension pairsがsupportedであることと、補題3.1からG Khatri–Rao M aがfull column rankになることを用います。",
    ]),
    ("Slide 20  New Theorem 1", [
        "これが本研究の中心となる定理1で、本文の定理3.1です。第一段階の仮定と仮定3.1の下で、pとG、Wごとの潜在分布Q F、全項目の測定核Q Yが、共通のラベルの下で識別できます。",
        "要するに、必要なペアの分布を回復して、一つのanchorのテンソルを分解し、残りを順に解けばよい、ということです。潜在クラスの比率だけでも、測定核だけでもなく、両方が分かります。さらに、このモデルの下では、一度も同時に観測されていない項目の組合せについても、同時分布を作れます。",
    ]),
    ("Slide 21  Proof map for Theorem 1", [
        "証明で何を使うかを、この一枚にまとめています。出発点は観測データの分布です。命題1で各テンソルを回復し、Allman型の一意性を使って、M a、M b、p、Gを取り出します。確率の和とanchorの順序を使い、大きさとラベルも固定します。",
        "残りは二つの操作です。pとGにはベイズ則を使い、Wごとのクラス比率を求めます。extensionには補題3.1を使い、残りの測定核を一つずつ解きます。詳しい8ステップは、後ろのAppendixに置いています。",
    ]),
    ("Slide 22  Bridge-weighted composite estimation", [
        "推定も、いまの識別と同じ順番で進めます。まずd’Haultfoeuilleの第3節に沿って、blockごとに条件付きモーメントの式を解き、逆確率重み付け、IPWでペアの分布を回復します。次に、重なりのあるペアに共通の潜在モデルを当てはめます。先に補助的な分布を推定してから代入する順序は、ZhaoとShaoに沿っています。",
        "ここで使うのは、一つのfull likelihoodではありません。ペアごとの対数密度をbridgeで重み付けして足す、compositeな基準です。これを最大にするM推定量を使います。分散を求めるときも、最初のbridgeを推定した誤差を含めます。後で示す一致性と漸近正規性は、bridgeの次元を固定した場合の結果です。",
    ]),
    ("Slide 23  Computation", [
        "計算も、回復、分解、更新の順番です。まずbridgeを推定し、重み付きのテンソルを作ります。anchorを分解してラベルをそろえ、残りの測定核の初期値を出します。",
        "その後、確率が非負で和が1になる制約を守りながら、全体を更新します。目的関数は非凸なので、初期値は複数試し、得られた解の中で目的関数が最大のものを採ります。これだけで大域的な最大値を保証するわけではありません。ZhaoとShaoの第2.3節から引き継ぐのはplug-inの順序で、更新法をそのまま移しているわけではありません。",
    ]),
    ("Slide 24  Simulation design", [
        "simulationはAllman、Matias and RhodesのSections 3から5に従い、本文式35のr-class、p-feature product mixtureから出発します。Allmanらに従うのはmodel classであり、数値parameterは本研究固有です。p fはlatent class比率、G fはclass別のWの分布、M j fはclass別の項目jの測定核です。",
        "標本サイズは500、Fは2 class、WとY 1、Y 2、Y 3は二値です。Y 1は常時観測とし、Y 2とY 3は自身の値に依存して欠測するMNAR、平均item response rateは80パーセントです。各pairには4カテゴリでfull-rankのMissing IVを置き、100回反復します。",
        "比較は五手法です。第一は欠測前のfull product-mixture likelihoodを使うcomplete-data oracle、第二はignorabilityを置くMAR full-information likelihood、第三は真のlogistic selection equationを用いてW、Y obs、Dの周辺尤度を最大化するcorrect selection likelihood、第四はY 1のmain effectとinteractionを除くmisspecified selection likelihoodです。第五の提案法は、各blockで固定4-cellのfinite-cell saturated inverse bridgeを推定し、weighted pairwise latent-class criterionを当てはめます。",
    ]),
    ("Slide 25  Evaluation targets", [
        "新しい評価対象の一つ目はmeasurement kernel M jです。二値項目ではM j of 1, fは、latent classがfのときに項目jが1となる確率です。これは項目とlatent classの測定関係を表し、全てのitem-by-class cellsにわたる平均biasと平均RMSEを報告します。",
        "二つ目はlatent class proportion p f、つまり母集団におけるclass fの比率です。本文の結果表に合わせてp 2を評価し、p 1は1 minus p 2で決まります。Biasは系統誤差を、RMSEはbiasとreplication variabilityを合わせた有限標本誤差を表します。",
    ]),
    ("Slide 26  Simulation results", [
        "こちらは、潜在構造まで分けた後の結果です。測定核では、提案法のbiasの絶対値とRMSEが、MARと誤指定したselection likelihoodより小さくなっています。欠測モデルの形を直接決めず、Missing IVからペアの分布を回復していることが効いていると考えられます。",
        "クラス比率のbiasもほぼゼロです。ただし、RMSEがどの手法よりも小さいわけではありません。欠測モデルを正しく指定できれば、パラメトリックな方法も効率の面で有力です。提案法の利点は、常に一番精度が高いことではなく、欠測モデルの形の誤指定を避けられる点にあります。",
    ]),
    ("Slide 27  Contribution & Limitation & Future Work", [
        "最後にまとめます。第一段階では、Missing IVとblockのcomplete-case completenessを使って、欠測モデルの形をパラメトリックに決めずに各blockの分布を回復します。第二段階では、anchor itemsとWを使い、潜在クラス比率と全ての測定核を共通のラベルで識別します。この接続を定理にして、同じ順序で推定量も作りました。",
        "ただし、何にでも頑健というわけではありません。クラス数は既知で、有限潜在クラスの測定モデルが正しいことが前提です。必要なペアが観測されること、Missing IVの除外制約、completeness、局所独立性、ランク条件、anchorの順序も必要です。",
        "効率の面でも、クラス比率のRMSEは、正しく指定したselection likelihoodより大きくなることがあります。常に一番精度が高い、と言っているわけではありません。",
        "今後の課題は、有限次元のbridgeについて示した推測理論を、標本数とともに次元を増やすsieveへ広げることです。そのためには、収束速度や逆問題について追加の理論が必要です。",
    ]),
    ("Slide 28  Selected references", [
        "主に参照した文献はこちらです。第一段階はd’HaultfoeuilleとZhao、Shao、complete-caseでのcompletenessはMiaoらを参照しています。第二段階はAllman、Matias、Rhodesです。識別の言葉遣いはLewbel、欠測の分類はLittleとRubin、選択バイアスはHeckmanに沿っています。",
    ]),
    ("Appendix Slide 29  Steps 1 and 2", [
        "最初の二つのステップです。Step 1では、命題1でanchor pairと全extension pairの分布を回復します。Step 2ではXをxに固定し、Y a、Y b、Wの確率をテンソルに並べます。",
        "仮定した測定モデルから、FとXの下でこの三つは条件付き独立です。そのため、クラスごとの三つの確率ベクトルの積を、クラス比率で重み付けして足す形に書けます。これが分解の出発点です。",
    ]),
    ("Appendix Slide 30  Steps 3 and 4", [
        "Step 3では、Kruskalのランク条件を使います。これで、テンソルの分解は、クラスの入れ替えと列の大きさの調整を除いて一つに決まります。",
        "Step 4では、その二つの曖昧さをなくします。確率ベクトルは和が1なので、列の大きさを固定できます。クラスの名前は、anchorの平均スコアが小さい順にそろえます。",
    ]),
    ("Appendix Slide 31  Steps 5 and 6", [
        "Step 5では補題3.1を使い、GとM aのKhatri–Rao積が列フルランクだと示します。これで、残りの項目の測定核を求める線形の式が、一つに解けます。",
        "Step 6では、既に分かったpとGにベイズ則を使います。クラスごとのWの分布から、今度はWとXが与えられたときのクラス比率を求めます。これがQ Fです。",
    ]),
    ("Appendix Slide 32  Steps 7 and 8", [
        "Step 7では、各extensionのテンソルから、残りのM jを順に解きます。これで全項目の測定核がそろいます。",
        "最後のStep 8では、その測定核と潜在クラスの比率を、局所独立モデルの式に戻します。すると、一度も同時に観測されていない項目の組合せについても、モデルの下で同時分布を作れます。ここまでで、回復と分解がつながります。",
    ]),
    ("Appendix Slide 33  Empirical diagnostics and falsification checks", [
        "応用では、どの変数をMissing IV、W、通常共変量、anchorにするかを決めます。その割当てについて、データで確認できる部分もあります。たとえばZの関連の強さ、有限カテゴリでのcomplete-case行列のランク、必要なblockが観測される確率、Wのviewのランク、anchorの分離です。",
        "余分なblockも回復できれば、別のblockから求めた測定核が一致するかも調べられます。ただし、これらを通過しただけで、Missing IVの除外制約や測定モデルの除外制約、局所独立性まで正しいとは言えません。合わなければ設計を疑えますが、合えば全て証明できる、というものではありません。",
    ]),
]


def _slide_by_title(title):
    for heading, paragraphs in SLIDES:
        if heading.split("  ", 1)[1] == title:
            return title, paragraphs
    raise KeyError(title)


_original_slides = SLIDES
SLIDES = [
    _slide_by_title("Title"),
    _slide_by_title("Missing-data mechanisms and standard approaches"),
    _slide_by_title("Usual IV and Missing IV"),
    ("Latent measurement model", _slide_by_title("Latent measurement model")[1][:3]),
    ("Latent models with nonignorable missingness", _slide_by_title("Latent measurement model")[1][3:]),
    ("Multivariate MNAR and the remaining gap", _slide_by_title("Multivariate MNAR and the remaining gap")[1][:2]),
    ("Why leave the selection model unspecified?", [
        *_slide_by_title("Multivariate MNAR and the remaining gap")[1][2:4],
        _slide_by_title("Multivariate MNAR and the remaining gap")[1][4],
    ]),
    (
        "Motivation and objective",
        [
            "ここで、なぜ二つの識別をつなぐ必要があるのかを見ます。Dはどの項目が見えたか、Wは潜在分布を動かす変数です。仮に、Y、F、Xを条件づけると、DとWは独立だとします。これが上の式です。",
            "でもFは見えないので、平均して消す必要があります。すると下の式の赤い部分、Y、W、Xを見た後のFの分布が残ります。この分布はWによって変わりうるので、積分した後までDとWが独立とは言えません。つまり、latent shifterのWを、そのままMissing IVとしては使えないわけです。",
            "下の二つの欄で役割を分けています。Z SはY Sと関連し、Y Sと共変量を押さえると欠測指標R Sとは独立になる変数です。これを使って、第一段階で欠測による偏りを補正します。一方、WはFの分布を動かし、第二段階で潜在構造を分けるための三つ目のviewを与えます。",
            "逆に、Missing IVでYの分布だけを回復しても、Q Fと各Q jへの分解が一つに決まるとは限りません。そこで、Stage 1の分布の回復と、Stage 2の潜在分解を接続します。selection modelの関数形を決めず、有限潜在クラスの比率と測定核を同時に識別するのが目的です。もちろん、有限クラスの測定モデル、ランクや共通ラベルの条件は置きます。この目的に対して、次のページで具体的な識別戦略を示します。",
        ],
    ),
    (
        "Proposed two-stage identification",
        [
            "この目的に対して、二段階で進めます。第一段階は、欠測した人も含めたblockの分布を回復することです。ZhaoとShaoの除外制約と、d’Haultfoeuilleの条件付きモーメントの式を使います。欠測確率を特定のパラメトリックな形に決める必要はありません。",
            "第二段階は、回復した分布を潜在クラスに分けることです。共通するanchor itemsとWを使い、Allmanらの分解の一意性につなげます。最初のanchorを分けた後、残りの項目を順に解きます。この二段階を接続して、一つの識別定理にするのが今回の提案です。",
        ],
    ),
    _slide_by_title("Model and assumptions"),
    ("Assumption 1", [
        "仮定1では、何が見えているかを決めます。Yが測定項目全体、D jが項目jを観測したかどうかです。D jが1のときだけY jが見えます。X、W、ZとDはいつも見えていますが、潜在変数Fは見えません。",
        "式のOは、一人分の観測データです。いつも見える変数と、その人について実際に見えたYの成分、Y Dをまとめています。Zの中には、各blockで使うMissing IVのZ Sが含まれます。",
    ]),
    ("Assumptions 2 and 3", [
        "仮定2と3は、先ほどの測定モデルを式にしたものです。仮定2のQ Fは、WとXが与えられたときのFの分布です。Xは通常の共変量、Wは潜在分布を動かす変数です。ここではZについて平均を取っており、Zは条件に入っていません。",
        "仮定3のQ jは、FとXが与えられたときのY jの分布です。シータjが、その測定核のパラメータです。クラスの構成を表すのがQ F、各クラスが項目にどう表れるかを示すのがQ j、と分けて考えます。",
    ]),
    ("Assumption 4", [
        "仮定4には二つの内容があります。一つは、FとXを押さえると、項目全体が条件付き独立になることです。二項目ずつ独立というだけではなく、全ての項目の同時分布が、この積に分かれると仮定します。",
        "もう一つは、Wが測定核に直接入らないことです。Wは潜在分布を動かしますが、FとXを決めた後の項目の分布は変えません。これは、Zについて平均を取った測定モデルの条件です。",
        "F、W、Xを条件づけたらYとZも独立、とは言っていません。ZとYには関連があってよいです。Missing IVとしてのZの条件は、欠測指標Rとの独立性として、後の仮定6で別に置きます。",
    ]),
    _slide_by_title("Lemma 2.1"),
    ("Assumption 5", [
        "ここで使うblockは、項目の一部分をまとめたものです。Sがその項目の集合、Y Sがその組の測定値、U SがXとWです。R Sは、その組のD jを全部掛けたものです。1なら、そのblockの項目は全て見えています。0なら、少なくとも一つが欠測しています。",
        "一部だけ見えたblockは、全体が見えたblockとしては使いません。対象となるY SとU Sの値ごとに、block全体が観測される確率パイSが正であることを、supportedと呼びます。後で必要になるのはanchor pairとextension pairで、全項目が同時に見えることではありません。",
    ]),
    ("Two marginal views of the model", [
        "同じモデルを、見る変数を変えて二つに分けた図です。左は、ZとDについて平均した測定モデルです。Fと項目の関係を見ています。U SからY Sへの矢印はXの効果だけで、Wは測定核には入りません。項目間の局所独立性は、仮定4の積の式で置いています。",
        "右は、Fとblock外の項目について平均した図です。Z SからY S、Y SからR Sへ矢印を引いています。Y SとU Sが決まると、Z SとR Sが独立になる関係です。ここでいうfull-data lawは、回答者だけでなく、欠測した人も含む母集団の分布です。図にY Sがあっても、全員で見えているという意味ではありません。",
        "左右を合体させて一つのDAGとして読むものではありません。特に、この図からFとZの追加の独立性を読み取ることはしません。",
    ]),
    ("Overlapping supported blocks", _slide_by_title("Overlapping supported blocks replace global complete cases")[1]),
    ("Assumptions 6 and 7", _slide_by_title("Stage-1 assumptions")[1]),
    _slide_by_title("New Proposition 1"),
    _slide_by_title("Finite latent-class identification"),
    _slide_by_title("The remaining decomposition problem"),
    _slide_by_title("Identification strategy"),
    ("Assumption 3.1: Support and model", [
        "仮定3.1は二枚に分けています。まず、どのモデルを扱うかです。潜在クラス数rは既知で、2以上とします。項目が取る値も、Xで条件づけたWが取る値も有限です。条件は全て、Xについて共通の確率1の集合上で置きます。",
        "仮定2から4の測定モデルが成り立ち、各クラスの比率と、Wのサポート上の確率は正とします。また、anchor pairと全extension pairが仮定1、5から7を満たします。逆観測確率の二乗平均も、blockのcomplete caseで有限です。これで、命題1を必要な全ペアに使えます。",
    ]),
    ("Assumption 3.1: Rank and labels", [
        "次は、分解を一つに決める条件です。M a、M b、Gの列Kruskal rankの和が、2rプラス2以上だとします。三つのviewに対するこのランク条件は、AllmanらのTheorem 1と同じです。",
        "これだけでは、クラスの名前の入れ替えが残ります。そこで、既知のanchor scoreをクラスごとに平均したミューafに、厳密な順序を付けます。先ほどのXの集合上で、同じ順序を使います。ランクで分解を決め、順序で名前をそろえる、という二つの役割です。",
        "なお、GとM aのKhatri–Rao積が列フルランクになることは、別に仮定しません。次の補題で、今の条件から導きます。",
    ]),
    _slide_by_title("Lemma 3.1"),
    _slide_by_title("New Theorem 1"),
    _slide_by_title("Bridge-weighted composite estimation"),
    ("Conditions for estimation", [
        "次に、推定の基準も真値で一つに最大になるかを確認します。ここは本文の命題4.1です。これまでの仮定1から7と3.1に加え、潜在モデルが正しく、全ペアの密度が共通のサポート上で正だとします。母集団の基準には、真のbridgeと、固定した正のblock重みを使います。",
        "IPWによって、ペアの平均を母集団の平均に戻せます。真値との目的関数の差は、分布の違いを測るKLダイバージェンスの正の加重和になります。差がゼロなら、全ペアの分布が同じです。すると定理1から、潜在パラメータも同じだと分かります。",
    ]),
    ("Assumption 5.1: Regularity", [
        "ここからは、標本を増やしたときの推定量の性質です。個人ごとの観測データは独立同分布とします。シータが潜在モデルの母数、イータがbridgeの母数で、この二つをまとめたものがベータです。",
        "確率の和が1という制約を除いた自由な座標で、どちらも有限次元とし、モデルは正しく指定されているとします。パラメータ空間はコンパクトで、真値は境界ではなく内側にあります。第一段階の母集団モーメントがゼロになるのも、真値だけとします。",
        "計算に必要な滑らかさも置きます。目的関数とモーメントは真値の近くで二回連続微分でき、それらを抑える関数は二乗可積分です。また、bridgeとcomposite scoreのヤコビアン、それに対応するGodambe行列は非特異とします。",
    ]),
    ("Assumption 5.1: Uniform convergence", [
        "真値の近くだけが滑らかでも、推定量がそこへ近づくとは限りません。そこで、推定したbridgeを代入した標本の目的関数が、真のbridgeを使う母集団の目的関数に、パラメータ空間全体で一様に近づくと仮定します。",
        "もう一つ、真値から一定以上離れた場所では、母集団の目的関数が最大値より確実に低くなるとします。この一様収束と最大値の分離を使い、argmax定理から一致性を得ます。近所の微分条件と、空間全体の条件を分けている点が大事です。",
    ]),
    ("Assumption 5.1: First stage and separation", [
        "第一段階の誤差も扱います。bridge推定量は正則で、真値からの誤差を、漸近的に影響関数の標本平均で表せると仮定します。その影響関数は平均ゼロで、分散は有限です。",
        "また、識別できるかどうかの境目に近づきすぎない条件を置きます。クラス比率とペアの観測確率は、一様にゼロから離れているとします。anchorのテンソルを、Wが行、Y aとY bが列になる行列に並べ替えたときの、最小の非零特異値も同様です。",
        "Kruskal rankを支える小行列式の絶対値と、anchorの順序で隣り合う平均スコアの差も、一様にゼロから離す必要があります。識別ができることと、安定した推論ができることは別なので、この条件を加えています。",
    ]),
    ("New Theorem 5.1", [
        "以上の命題4.1と仮定5.1の下で、有限次元のbridgeを使う推定量は一致性と漸近正規性を持ちます。標本が増えると真値に近づき、その誤差をルートn倍したものが、漸近的に正規分布に従うという結果です。",
        "分散の式で大事なのは、bridgeを推定した誤差も入ることです。Aはcomposite scoreをシータで微分した期待値、Cはイータで微分した期待値です。Bにはscoreに加え、Cと第一段階の影響関数の積が入ります。bridgeが既知だとして分散を出してはいけません。",
        "個人単位のbootstrapを使うなら、両段階の推定とラベル合わせを毎回やり直します。なお、次元を増やしていくsieveは、この定理の範囲外です。推定速度や逆問題としての追加の条件が必要です。",
    ]),
    _slide_by_title("Computation"),
    (
        "Simulation targets in the model",
        [
            "ここからシミュレーションです。Xは固定し、Fは二つのクラスとします。図は、Z SからY S、Y SからR Sという流れです。FからZ Sへも矢印があります。FとZ Sは関連するので、ここを独立にしてはいけません。Wと三つのYは全て二値です。Y 1はいつも見えているので、ペアが全部見えるかどうかは、もう一方のD jで決まります。",
            "生成するときは、FとWの後に、Zの組を先に、Yの組を後に作ります。AがFの下でのZの分布、BがFとZの下でのYの分布です。最後に、そのYを使ってD 2とD 3を独立に生成します。ここはBayes則で書き直しているだけなので、欠測指標まで含めた同時分布は変わりません。Zについて平均すると、元の測定核の積に戻ります。図はそのうち一つのblockを示しています。",
            "標本サイズは500で、データを作って推定する作業を100回繰り返します。全項目の平均観測率は80パーセントです。この生成モデルは、Zを平均して消した仮定4とMissing IVの条件を満たします。さらに、Y Sの下でR SとF、W、Z Sが独立になる作り方ですが、この追加条件を一般の識別定理にも求めるわけではありません。",
        ],
    ),
    (
        "Outcome and latent parameters",
        [
            "次に、何を評価するかです。第一段階のミューjは、母集団全体でY jが1になる確率です。p S,cは、ペアの00、01、10、11それぞれの確率です。Y 2とY 3、およびY 1とそれぞれを組にしたペアを見ます。",
            "これに対して第二段階のp fはクラスの比率、M jfはクラスfで項目jが1になる確率を表します。M jfは三項目かける二クラスで六つ、クラス比率はp 2を評価します。Yの分布が戻ることと、その背後の潜在構造が分かることを、分けて見ていきます。",
        ],
    ),
    (
        "Simulation design: five estimators",
        [
            "比較するのは五つです。一つ目は、欠測前の全データを使うoracleです。二つ目は、欠測を無視できると考えて観測尤度を使うMARです。三つ目は、欠測のlogisticモデルを正しく指定したselection likelihoodです。四つ目は、そこからY 1の主効果と交互作用を落とした誤指定版です。この二つのselection likelihoodには、どちらもZ Sを入れません。",
            "五つ目が提案法です。各blockのMissing IVの式から、四つのセルに対応する逆観測確率のbridgeを推定します。まず正規化したIPWで分布を回復し、その後、重み付きのペアの基準で潜在モデルを当てはめます。後で見る提案法の項目ごとの確率は、潜在分解をする前の第一段階の結果です。他の四手法は、当てはめたモデルからYの分布を求めています。",
        ],
    ),
    (
        "Simulation evaluation criteria",
        [
            "Yの母数ごとに、四つを見ます。Biasは平均的なずれ、SDは100回の推定値のばらつきです。平均SEは、各データから推定した標準誤差の平均なので、SDと近いかを見ます。95パーセントcoverageは、母数ごとのWald信頼区間が真値を含んだ割合です。区間は推定値プラスマイナス1.96 SEで作ります。",
            "尤度法のSEにはデルタ法とsandwich分散を使います。提案法では、各反復の中で個人単位のbootstrapを200回行い、二つのbridgeを毎回推定し直します。潜在母数はbiasとRMSEで見ます。測定核のRMSEは、100反復と六つの成分の二乗誤差をまとめて平均し、平方根を取ります。成分ごとのRMSEの単純平均ではありません。p 2は別に評価します。",
        ],
    ),
    (
        "Population outcome recovery: bias and SD",
        [
            "まず、潜在構造に分ける前に、Yの分布が戻っているかを見ます。このページでは、ミュー2とミュー3について、五つの手法のbiasとSDを比べます。",
            "提案法は、MARと誤指定したselection likelihoodよりbiasの絶対値が小さくなっています。ミュー2とミュー3の真値は0.475と0.4925で、提案法のbiasはマイナス0.0099とマイナス0.0096です。SDはそれぞれ0.0379と0.0345でした。平均的なずれと、反復ごとのばらつきを分けて見ています。",
        ],
    ),
    (
        "Population outcome recovery: SE and coverage",
        [
            "続いて、不確実性をうまく測れているかを見ます。提案法の平均SEは、ミュー2で0.0365、ミュー3で0.0339です。前のページのSD、0.0379と0.0345に近く、実際の推定値のばらつきをおおむね捉えています。coverageは94パーセントと93パーセントでした。",
            "一方、MARのcoverageは9パーセントと13パーセント、誤指定版は12パーセントと11パーセントです。正指定版のbiasはほぼゼロですが、Y 2のcoverageは86パーセントでした。100反復の結果なので、常にこの被覆率になるとは言えません。ここで言いたいのは、提案法が常に最も効率的ということではなく、欠測モデルの形を決めずに第一段階でYの偏りを補正できた、という点です。",
        ],
    ),
    (
        "Stage-2 full joint law",
        [
            "今度は、三つのYの同時分布を見ます。横軸は0と1の八通りの組合せ、縦軸はそれぞれが起こる確率です。黒い線が母集団の真の分布で、ほかの線は100反復の推定結果を平均しています。",
            "ここでの青い提案法の線は、第二段階まで使った結果です。回復したペアの分布を共通の潜在構造につなぎ、クラス比率と全ての測定核から、三項目の同時分布を作っています。先ほどの項目ごとの確率と違い、今度は項目の組合せまで再現できているかを見ています。",
        ],
    ),
    ("Latent-parameter recovery", _slide_by_title("Simulation results")[1]),
    _slide_by_title("Contribution & Limitation & Future Work"),
    ("Selected references", [
        "主に参照した文献を二枚に分けています。このページのAllman、Matias、Rhodesは潜在分解の一意性、d’HaultfoeuilleはMissing IVを使った分布の回復、Heckmanは選択バイアスの議論に対応します。",
    ]),
    ("Selected references (continued)", [
        "こちらは続きです。識別の言葉遣いはLewbel、欠測の分類はLittleとRubinを参照しています。Miaoらはshadow variableとcomplete-caseでのcompleteness、ZhaoとShaoは共変量を調整した除外制約と半パラメトリックな推定の背景です。",
    ]),
    ("Proof sketch for Proposition 1", _slide_by_title("Proof sketch the observable bridge is unique")[1] + [
        "補題2.1も同じ証明です。全項目を一つのblockと見て、二つのbridgeの逆数の差を取り、complete-case completenessとpositivityで一意性を示します。最後にIPWで全体の分布を回復します。",
    ]),
    _slide_by_title("Proof map for Theorem 1"),
    ("Proof of Theorem 1 (Steps 1--2)", _slide_by_title("Steps 1 and 2")[1]),
    ("Proof of Theorem 1 (Steps 3--4)", _slide_by_title("Steps 3 and 4")[1]),
    ("Proof of Theorem 1 (Steps 5--6)", _slide_by_title("Steps 5 and 6")[1]),
    ("Proof of Theorem 1 (Steps 7--8)", _slide_by_title("Steps 7 and 8")[1]),
    _slide_by_title("Empirical diagnostics and falsification checks"),
    (
        "Simulation calibration",
        [
            "こちらは、シミュレーションの具体的な設定です。WとYのモデルの形は、Allman、Matias、Rhodesの有限クラスのproduct mixtureに沿っています。ただし、数値は本研究で決めています。クラス比率は0.55と0.45です。G fはクラスごとのWの分布で、ラベルはY 1が1となる確率の小さい順にそろえます。",
            "クラス1と2で、Wが1となる確率は0.20と0.80です。Y 1が1となる確率は0.15と0.80、Y 2は0.25と0.75、Y 3は0.20と0.85です。これらの測定核をクラスごとに掛け、クラス比率で平均すると、母集団の分布になります。",
        ],
    ),
    (
        "Selection and shadow calibration",
        [
            "Y 1はいつも観測されます。Y 2とY 3は、自分自身の値、Y 1、その交互作用に依存するlogistic式で観測を決めます。切片を調整し、それぞれの平均観測率を70パーセントにします。Y 1の100パーセントと合わせて、三項目平均で80パーセントです。行列Hは、ペアの値とZ Sの関連を決めるためのものです。そこからBayes則でZを先に作る条件付き分布を計算します。Z Sは常に観測します。",
            "今回掲載している100反復の結果は、同じ同時分布をY先行で生成したものです。Z先行の生成方法へ書き直しても、母集団の分布は変わりません。ただし、同じseedでも出てくる標本は変わるため、数値を完全に再現するための旧生成方法も残しています。生成順序を変えたことだけで、因果効果まで識別したという話ではありません。",
            "取り得る値を全て並べ、母集団で条件も確認しています。各Wの下でcomplete-caseの行列のランクは4、三つのviewのKruskal rankの和は6、extensionを解く行列のランクは2でした。FとWの下でY SとZ Sまで独立にする必要はありません。これは識別条件の確認であって、推定に必要な正則条件を全て数値的に証明した、という意味ではありません。",
        ],
    ),
]


DETAILED_SLIDES = SLIDES
SUMMARY_SLIDES = [
    ("Stage 1 (1): Recover the block law", [
        "まず第一段階です。知りたいのは、回答した人だけでなく、欠測した人も含めたblockの分布です。Sは一緒に扱う項目の組、R Sはその組が全部見えているかを表します。U SにはXとWをまとめています。",
        "ここで使うZ SがMissing IVです。項目の値とは関連しますが、その値とU Sを押さえると、blockが見えるかどうかとは独立になります。この条件から、逆観測確率を重みにした条件付きモーメントの式が出てきます。complete-caseでのcompletenessとpositivityを置くと、bridgeが一つに決まります。",
        "あとは、blockが全部見えた人をその重みで重み付けします。すると、Y S、Z S、U Sの母集団の同時分布が戻ります。一意性は、逆観測確率がcomplete caseで二乗可積分になる、ここで定めたbridgeの範囲での結果です。欠測確率をlogisticなどの形に決めなくてよい、というのが、この段階のポイントです。",
    ]),
    ("Stage 1 (2): Use overlapping pairs", [
        "次に、どのblockを回復するかです。全項目が同時に見える人を集める必要はありません。基準になる二つの項目aとbのペアと、aと残りの項目jを組にしたペアを使います。項目aが共通しているので、ペアどうしが重なっています。",
        "必要なペアごとに、先ほどのMissing IV、completeness、positivityの条件を置いて分布を回復します。得られるのは、各ペアとWの母集団の分布です。まだ潜在クラスや測定核まで分かったわけではないので、それを次の段階で分けます。",
        "ここではZ SとWの役割も分けておきます。Z Sは欠測の偏りを補正するための変数です。Wは潜在構造を分けるための三つ目のviewになります。潜在分布を動かすWを、そのままMissing IVとして使えるとは限りません。",
    ]),
    ("Stage 2 (1): Identify the latent structure", [
        "第二段階では、戻したペアの分布から、その背後の潜在構造を取り出します。クラス数rは既知で有限、項目とWが取り得る値も有限とします。さらに、FとXの下での局所独立性と、Wが測定核に直接入らないことを仮定します。ランク条件は、三つのviewのKruskal rank、k a、k b、k Gの和が2rプラス2以上、というものです。",
        "まずanchorの二項目とWの確率を、三つの方向を持つ表、テンソルに並べます。Kruskalのランク条件があると、この分解はクラスの入れ替えと大きさの調整を除いて一つに決まります。確率の和を1にし、anchorのスコアで順序をそろえると、クラス比率p、Wのクラス別分布G、二つの測定核が分かります。",
        "残りの項目は、共通のanchorを含むペアから線形の式を解いて求めます。これで全ての測定核が同じクラス名でそろい、ベイズ則からWごとのクラス比率も分かります。この測定モデルの下では、全項目の同時分布も組み立てられます。",
    ]),
    ("Stage 2 (2): Connect identification to estimation", [
        "ここまでで分かったWごとのクラス比率と各測定核を使うと、任意の項目集合Aの同時分布を作れます。クラスごとに各項目の確率を掛け、ラムダfで重み付けして足す、という式です。一度も一緒に観測されていない項目にも使えますが、局所独立性など、いまの測定モデルの下での結果です。",
        "推定も、いま説明した順番で進めます。まず各ペアのbridgeを推定して、重み付きの分布を作ります。その後、ペアどうしに共通する潜在クラスモデルを当てはめます。使うのは、ペアごとの対数密度をbridgeで重み付けして足したcompositeな基準です。",
        "識別の結果によって、母集団でどの値を目指すかが決まります。ただ、それだけで標本からの推定が安定するわけではありません。一様収束や真値での最大値の分離、滑らかさ、bridgeの正則性など、推定の条件も必要です。詳しい条件はAppendixに残しています。",
        "次の定理では、固定した有限次元のbridgeについて、一致性と漸近正規性を示します。分散には、最初にbridgeを推定した誤差も入れます。bridgeの次元を増やすsieveの理論まで示しているわけではない、という範囲も押さえておきます。",
    ]),
]
if len(DETAILED_SLIDES) != 53:
    raise ValueError("Expected the original 53 detailed narratives")
SLIDES = (DETAILED_SLIDES[:7] + SUMMARY_SLIDES + DETAILED_SLIDES[31:44]
          + DETAILED_SLIDES[7:31] + DETAILED_SLIDES[44:])
APPENDIX_START = 25


def beamer_frames():
    """Read this deck's frame titles, including its plain section dividers."""
    source = re.sub(r"(?<!\\)%[^\n]*", "", BEAMER.read_text(encoding="utf-8"))
    appendix_offset = source.index(r"\appendix")
    frames = []
    for match in re.finditer(r"\\begin\{frame\}(.*?)\\end\{frame\}", source, re.S):
        body = re.sub(r"^\[[^\]]*\]", "", match.group(1)).lstrip()
        if body.startswith("{"):
            depth = 0
            for end, char in enumerate(body):
                depth += (char == "{") - (char == "}")
                if depth == 0:
                    title = body[1:end]
                    break
            else:
                raise ValueError("Unbalanced Beamer frame title")
            title = title.replace(r"\textcolor{Red}{New!}", "New")
        elif r"\titlepage" in body:
            title = "Title"
        else:
            divider = re.search(r"\\color\{Blue\}\\large\\bfseries ([^}]+)", body)
            if divider is None:
                raise ValueError("Unrecognized untitled Beamer frame")
            title = divider.group(1)
        title = title.removeprefix("Appendix: ").replace(r"\&", "&")
        frames.append((title, match.start() > appendix_offset))
    return frames


def align_with_beamer(slides):
    frames = beamer_frames()
    if len(frames) != len(slides):
        raise ValueError(f"Beamer has {len(frames)} frames; script has {len(slides)}")
    for index, ((title, _), (frame_title, _)) in enumerate(zip(slides, frames), 1):
        if title.casefold() != frame_title.casefold():
            raise ValueError(f"Slide {index}: script {title!r} != Beamer {frame_title!r}")
    if len(slides) != 57 or slides[APPENDIX_START - 1][0] != "Motivation and objective":
        raise ValueError("Expected 57 slides with Motivation and objective at Appendix slide 25")
    expected_appendix = APPENDIX_START - 1
    if [is_appendix for _, is_appendix in frames] != [
        i >= expected_appendix for i in range(len(slides))
    ]:
        raise ValueError("Beamer and script Appendix boundaries differ")
    return [(title, paragraphs) for (title, _), (_, paragraphs) in zip(frames, slides)]


SLIDES = align_with_beamer(SLIDES)
SLIDE_NUMBERS = {title: index for index, (title, _) in enumerate(SLIDES, 1)}
appendix_start = APPENDIX_START
SLIDES = [
    (
        f"{'Appendix ' if index >= appendix_start else ''}Slide {index}  {title}",
        paragraphs,
    )
    for index, (title, paragraphs) in enumerate(SLIDES, start=1)
]


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, end])


def set_run_font(run, latin, east_asia, size=None, bold=None):
    run.font.name = latin
    run._element.rPr.rFonts.set(qn("w:eastAsia"), east_asia)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = LATIN_FONT
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), JAPANESE_FONT)
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    title_style = styles["Title"]
    title_style.font.name = LATIN_FONT
    title_style._element.rPr.rFonts.set(qn("w:eastAsia"), JAPANESE_FONT)
    title_style.font.size = Pt(20)
    title_style.font.bold = True
    title_style.font.color.rgb = RGBColor(0, 0, 0)
    title_style.paragraph_format.space_after = Pt(12)
    for border in list(title_style.element.iter(qn("w:pBdr"))):
        border.getparent().remove(border)

    for style_name, size in [("Heading 1", 15), ("Heading 2", 12.5)]:
        style = styles[style_name]
        style.font.name = LATIN_FONT
        style._element.rPr.rFonts.set(qn("w:eastAsia"), JAPANESE_FONT)
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(5)
        style.paragraph_format.keep_with_next = True

    if "Slide Reference" not in styles:
        ref_style = styles.add_style("Slide Reference", WD_STYLE_TYPE.PARAGRAPH)
        ref_style.font.name = LATIN_FONT
        ref_style._element.rPr.rFonts.set(qn("w:eastAsia"), JAPANESE_FONT)
        ref_style.font.size = Pt(9)
        ref_style.font.color.rgb = RGBColor(80, 80, 80)
        ref_style.paragraph_format.space_after = Pt(3)

    header = section.header.paragraphs[0]
    header.text = "欠測IVと潜在変数モデリングによる非無作為欠測の識別"
    set_run_font(header.runs[0], LATIN_FONT, JAPANESE_FONT, 8.5)
    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_page_number(section.footer.paragraphs[0])

    doc.add_paragraph("欠測IVと潜在変数モデリングによる\n非無作為欠測の識別", style="Title")
    subtitle = doc.add_paragraph("英語Beamer対応 日本語発表原稿")
    for run in subtitle.runs:
        set_run_font(run, LATIN_FONT, JAPANESE_FONT, 12, True)

    doc.add_paragraph(
        f"英語Beamer全{len(SLIDES)}枚に対応した、日本語の発表原稿です。"
        "欠測した人も含む分布をまず回復し、その後で潜在クラスの比率と測定核を分ける、という流れで説明します。"
        "本編24枚では二段階の要約、推定理論と数値結果を説明します。"
        "25枚目からのAppendixには、元の詳細な動機、仮定、識別と推定の議論を残し、その後に証明と数値設定を収めています。"
    )

    doc.add_paragraph("発表の構成", style="Heading 1")
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.autofit = False
    table.columns[0].width = Inches(1.55)
    table.columns[1].width = Inches(5.1)
    hdr = table.rows[0].cells
    hdr[0].text = "範囲"
    hdr[1].text = "内容"
    for cell in hdr:
        set_cell_shading(cell, "D9E7F5")
        for run in cell.paragraphs[0].runs:
            set_run_font(run, LATIN_FONT, JAPANESE_FONT, 10, True)
    set_repeat_table_header(table.rows[0])
    sections = [
        ("Title", "基礎概念、既存研究、問題設定"),
        (SUMMARY_SLIDES[0][0], "二段階の要約 分布の回復、重なるペア、潜在構造の識別、推定への接続"),
        ("New Theorem 5.1", "漸近理論、計算、simulation、結論、参考文献"),
        ("Motivation and objective", "詳細な動機、モデルと仮定、block lawの回復、潜在識別、推定条件"),
        ("Proof sketch for Proposition 1", "証明スケッチ、定理1の8ステップ、empirical diagnostics、数値設定"),
    ]
    starts = [SLIDE_NUMBERS[title] for title, _ in sections]
    ends = [start - 1 for start in starts[1:]] + [len(SLIDES)]
    rows = [
        (f"{'Appendix' if start >= appendix_start else 'Slides'} {start}–{end}", description)
        for start, end, (_, description) in zip(starts, ends, sections)
    ]
    for left, right in rows:
        cells = table.add_row().cells
        cells[0].text = left
        cells[1].text = right
        for cell in cells:
            for run in cell.paragraphs[0].runs:
                set_run_font(run, LATIN_FONT, JAPANESE_FONT, 10.5)

    doc.add_page_break()
    for index, (heading, paragraphs) in enumerate(SLIDES):
        doc.add_paragraph(heading, style="Heading 1")
        for text in paragraphs:
            paragraph = doc.add_paragraph(text)
            paragraph.paragraph_format.keep_together = True
        if index < len(SLIDES) - 1:
            spacer = doc.add_paragraph()
            spacer.paragraph_format.space_after = Pt(1)

    doc.core_properties.title = "欠測IVと潜在変数モデリングによる非無作為欠測の識別 日本語発表原稿"
    doc.core_properties.author = "Masahiro Honda"
    doc.core_properties.subject = "English Beamer presentation script in Japanese"
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
