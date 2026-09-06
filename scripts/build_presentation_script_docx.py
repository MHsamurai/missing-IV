from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "manuscript" / "vector_missing_iv_presentation_script_ja.docx"


SLIDES = [
    (
        "Slide 1  Title",
        [
            "本報告では、多次元の測定項目がmissing not at random、つまりMNARで欠測する状況において、潜在分布と測定核をどのように識別するかを議論します。",
            "中心となる考え方は二段階です。第一段階でshadow IVとsupported blockを用いて観測変数のblock lawを回復し、第二段階でanchor itemsとlatent shifterを用いて、その法則を有限潜在クラスへ一意に分解します。"
        ],
    ),
    (
        "Slide 2  Nonignorable item nonresponse in latent structure models",
        [
            "多変量データでは、各測定項目の観測確率が、その項目自身を含む未観測の値に依存することがあります。この場合、欠測はMNARであり、観測された回答だけから母集団の分布を推定するとbiasが生じます。",
            "一方、構造方程式モデルや項目反応理論では、関心は観測項目の分布だけではありません。潜在変数の分布Q Fと、各項目が潜在状態をどのように測定するかを表す測定核Q Yの双方が推定対象です。したがって、観測変数のfull-data lawを回復した後に、それを潜在分布と測定核へ分離する問題が残ります。"
        ],
    ),
    (
        "Slide 3  Related identification results",
        [
            "関連研究は、大きく二つの流れに分かれます。第一はMNARの識別です。d’Haultfoeuilleは条件付きmoment equationとcompletenessを用いた識別を示し、Zhao and Shaoは共変量を調整したexclusionへ拡張しています。またMiaoらは、completenessを観測可能なcomplete-case law上の条件として定式化しています。",
            "第二は潜在構造の識別です。Allman、Matias and Rhodesは、三つの条件付き独立なviewから得られるprobability tensorの分解一意性を用いて、latent class比率とclass-specific measurement kernelsを識別しています。ただし、こちらはMNARによる選択が除去されたjoint distributionから出発します。本研究は、この二つの識別段階を接続します。"
        ],
    ),
    (
        "Slide 4  The latent mixture and the additional identification problem",
        [
            "Fを未観測の潜在変数、Yを欠測前に定義される全測定項目、Xを通常共変量、Wを潜在分布を動かす常時観測のlatent shifterとします。局所独立性の下では、Yの条件付き分布は、各測定核の積をQ Fで積分したmixtureとして表されます。",
            "有限潜在クラスの場合、この式はclass比率lambdaと測定行列M jのtensor mixtureになります。missingness IVによって左辺の顕在分布が識別されても、同じ顕在分布を生成する潜在分布と測定核が複数存在し得ます。したがって、潜在構造の識別にはtensor分解の一意性条件が別途必要です。"
        ],
    ),
    (
        "Slide 5  A latent shifter is not a missingness IV",
        [
            "ここで、latent shifter Wとmissingness IV Z Sは区別する必要があります。仮にFまで条件づければDとWが独立であっても、Fを積分すると、Dの条件付き分布にはP of F given Y, W, Xが残ります。WがFを動かすなら、この分布は一般にWへ依存します。",
            "したがって、Wは周辺化後のmissingness IVにはなりません。Z Sは各block lawをMNAR selectionから回復する変数であり、Wは回復後のtensorにthird-mode variationを与える変数です。本研究では、この二つを別々の役割として用います。"
        ],
    ),
    (
        "Slide 6  Stage 1",
        [
            "第一段階では、観測データから各supported-block lawを回復します。必要なのは、blockwise shadow IV、positivity、そしてcomplete-case law上のcompletenessです。この段階では、回復した法則を潜在クラスへ分解しません。"
        ],
    ),
    (
        "Slide 7  Observed data and supported blocks",
        [
            "D jを項目Y jの観測指標とし、観測データOは、常時観測されるX、W、Z、Dと、Dによって選択されたYの成分Y Dから構成されます。",
            "項目集合Sについて、R SをS内の全項目が観測されたことを示すblock indicator、Y Sをblock内の測定値、U SをXとWの組と定義します。R SがゼロならY Sは欠測です。supported blockとは、対象とするsupport上でR Sが1となる条件付き確率pi Sが正であるblockです。必要なのはanchor pairとextension pairsがsupportedであることであり、全項目が同時観測されるglobal complete caseではありません。"
        ],
    ),
    (
        "Slide 8  Single-block data-generating structure",
        [
            "図は一つのsupported blockの構造です。U S、つまりXとWはF、Z S、Y Sへ関連します。Z SはFを通じてY Sを予測しますが、Y SとU Sを条件づけた後にはR Sへ直接影響しないと仮定します。このためZ SからR Sへの矢印はありません。",
            "一方、R Sは未観測となり得るY Sに依存してよく、ここでMNARを許容しています。図の矢印は因果効果を一般に主張するものではなく、本稿で用いる条件付き分布の分解関係を表しています。"
        ],
    ),
    (
        "Slide 9  Stage-1 assumptions",
        [
            "第一の仮定はblockwise covariate-adjusted missingness IVです。各supported blockについて、Y SとU Sを条件づけると、R SとZ Sが独立であるとします。",
            "第二の仮定はcomplete-case completenessです。R Sが1である標本において、Z SとU Sで条件づけたhの期待値がゼロなら、h自体がほとんど確実にゼロであるとします。これは、観測されたcomplete-case conditional operatorの単射性です。positivityはcomplete-case lawとfull lawの零集合を対応させます。"
        ],
    ),
    (
        "Slide 10  Proposition 1",
        [
            "命題1はsupported-block lawの識別です。仮定したexclusion、positivity、complete-case completenessの下で、条件付きmoment equationを満たす正値関数qのうち、pi Sが唯一の解になります。",
            "pi Sが識別されると、R Sをpi Sで割ったinverse probability weightによって、任意のblock関数hのfull-data expectationを再現できます。したがって、P of Y S, Z S, U Sというblock full law全体が識別されます。この段階でparametric selection modelを直接規定する必要はありません。"
        ],
    ),
    (
        "Slide 11  Proof sketch for Proposition 1",
        [
            "証明は四段階です。まずexclusionから、Y S、Z S、U Sを条件づけたR Sの期待値はpi Sになります。このため真のpi Sはbridge momentを満たします。",
            "次に、別の解qがあると仮定すると、complete casesの下でqの逆数とpi Sの逆数の差の条件付き期待値がゼロになります。completenessによって、この差はcomplete-case support上でゼロです。最後にpositivityを用いてfull supportへ拡張し、inverse weighting identityを得ます。"
        ],
    ),
    (
        "Slide 12  Overlapping supported blocks",
        [
            "global complete caseの代わりに、重なりを持つsupported pairsを利用します。S 0は二つのanchor items、Y aとY bを含みます。その他の項目Y jについては、Y jと共通anchor Y aからなるextension pairを用意します。",
            "各pairには、それぞれのshadow IV Z Sとbridgeがあります。第一段階でpair lawを個別に回復し、第二段階で共有されたY aを使って測定核のlabelとscaleを接続します。"
        ],
    ),
    (
        "Slide 13  Stage 2",
        [
            "第二段階では、第一段階で回復したblock lawsを有限潜在クラスへ分解します。二つのanchor itemsとlatent shifter Wを三つのviewとして用い、Kruskal型の一意性を適用します。"
        ],
    ),
    (
        "Slide 14  Finite latent classes and the anchor tensor",
        [
            "Xを固定し、Fがr個の有限状態を取るとします。M jはFとXを条件とする項目jの測定確率、p fはXを条件とするclass比率、GはFとXを条件とするWの分布です。",
            "回復されたY a、Y b、Wのjoint lawは三方向のtensorになります。局所独立性とmeasurement exclusionの下で、このtensorはp f、M a、M b、Gのrank-one tensorの和として表されます。ここでY a、Y b、Wが三つの条件付き独立なviewになります。"
        ],
    ),
    (
        "Slide 15  Anchor-pair identification conditions",
        [
            "anchor-pair identificationには四種類の条件を置きます。class数rは既知とし、anchor pairと全extension pairsがsupportedであること、class比率とWの各support確率が正であることを仮定します。",
            "中心となるrank条件は、M a、M b、Gのcolumn Kruskal rankの和が2rプラス2以上という条件です。さらに、既知のanchor scoreのclass別平均に共通の厳密順序を置きます。Kruskal条件がtensor分解を一意にし、anchor orderingがclass labelを固定します。"
        ],
    ),
    (
        "Slide 16  Theorem 1",
        [
            "定理1は二段階を統合した識別結果です。第一段階の仮定とanchor-pair条件の下で、観測データ法則からp、G、Wごとの潜在class分布Q F、そして全項目の測定核Q Yが共通labelの下で識別されます。",
            "その結果、一度も全てが同時観測されていない項目集合についても、有限潜在クラスの局所独立モデルを通じてjoint distributionを構成できます。ただし、この結論は有限class測定モデルと局所独立性に依存しています。"
        ],
    ),
    (
        "Slide 17  Proof sketch for Theorem 1",
        [
            "まず命題1によりanchor tensorとextension tensorsを回復します。次にAllmanらのKruskal一意性をanchor tensorへ適用し、M a、M b、p、Gをscalingとpermutationを除いて識別します。確率ベクトルとしての列和制約がscalingを固定し、anchor orderingがpermutationを固定します。",
            "pとGからBayes則によりWごとのclass比率lambdaを得ます。最後に、GとM aのKhatri–Rao積がfull column rankになるため、各extension tensorを線形反転して全てのM jを回復します。"
        ],
    ),
    (
        "Slide 18  From observed data to latent parameters",
        [
            "識別の全体像をまとめた図です。出発点はobserved pattern dataです。命題1が各supported blockについて選択確率とfull lawを回復します。その法則を周辺化、条件づけることでanchor tensorとextension tensorsを作ります。",
            "最後に、Wをthird modeとするKruskal分解とextension kernelの線形反転によって、潜在分布Q Fと測定核Q Yを識別します。この順序により、global complete caseを要求しません。"
        ],
    ),
    (
        "Slide 19  Bridge-weighted composite estimation",
        [
            "推定も識別と同じ順序で構成します。まず必要な各pairについてbridge pi Sを推定します。その後、観測されたpairの対数密度への寄与をR S divided by estimated pi Sで重み付けし、全supported pairsについて足し合わせます。",
            "これはfull likelihoodではなく、回復されたoverlapping pair lawsを同時に当てはめるcomposite M-estimatorです。有限次元bridgeが正しく指定され、regularityとseparationが成立すれば、一致性と漸近正規性が得られます。分散にはlatent modelのscoreだけでなく、第一段階のbridge推定誤差も含める必要があります。"
        ],
    ),
    (
        "Slide 20  Computation",
        [
            "計算手順も二段階識別に対応させます。各pairのbridgeを推定した後、weighted anchor tensorとextension tensorsを構成します。anchor tensorをnonnegative CP decompositionで初期化し、確率単体制約で正規化してlabelを固定します。",
            "次にextension tensorsを反転して各M jの初期値を得ます。latent mixtureのcriterionは非凸なので、複数初期値から制約付き更新を行い、criterionが最大の解を採用します。併せてrank gap、anchor gap、propensity overlapを確認します。"
        ],
    ),
    (
        "Slide 21  Simulation design",
        [
            "simulationは、定理1に直接対応するAllman型の二class product mixtureで行います。標本サイズは500、WとY 1、Y 2、Y 3は二値です。Y 1は常時観測、Y 2とY 3は自身の値に依存して欠測するMNARとし、平均item観測率を80パーセントに設定します。",
            "比較は、complete-data oracle、MAR、正しく指定されたselection likelihood、誤指定されたselection likelihood、提案するsaturated finite-cell bridgeの五手法です。評価対象は、各測定核M jとlatent class比率p fのbiasおよびRMSEです。"
        ],
    ),
    (
        "Slide 22  Simulation results",
        [
            "測定核M jについて、提案法の平均biasはマイナス0.0064、RMSEは0.0555です。MARのbiasはマイナス0.0496、RMSEは0.0966であり、誤指定selection likelihoodのbiasは0.0409、RMSEは0.0684です。提案法は、この二手法よりbiasの絶対値とRMSEがともに小さくなっています。",
            "正しく指定されたselection likelihoodのRMSEは0.0544であり、提案法とほぼ同程度です。一方、oracleの0.0351よりは大きく、bridge推定とpairwise composite criterionに伴う効率性の低下が残ります。"
        ],
    ),
    (
        "Slide 23  Interpretation and limits",
        [
            "simulationが示す利点は、特定のparametric selection equationを誤指定した場合のbiasを抑えながら、測定核とclass比率を同時に推定できることです。正しいselection modelを既知として推定できる場合に、それより効率的であると主張するものではありません。",
            "また、頑健性の範囲はselection-link specificationです。shadow-IV exclusion、positivity、complete-case completeness、局所独立性、rank条件、有限latent-class modelの誤指定まで許容するわけではありません。とくにsieve bridgeの漸近推論には、ill-posed inverse problemに対する追加理論が必要です。"
        ],
    ),
    (
        "Slide 24  Conclusion",
        [
            "本研究は、多次元MNARの下で潜在測定モデルを識別する問題を二段階に分けました。第一段階では、shadow IVとcomplete-case completenessにより、parametric selection modelを規定せずにsupported-block lawsを回復します。",
            "第二段階では、anchor itemsでoverlapping blocksを接続し、latent shifter Wをtensorのthird modeとして用いることで、有限潜在class比率と全測定核を共通labelの下で識別します。推定量もこの順序に沿ったbridge-weighted composite estimatorとして構成できます。"
        ],
    ),
    (
        "Slide 25  Selected references",
        [
            "主要な識別の依拠関係は、MNAR側のd’Haultfoeuille、Zhao and Shao、Miaoらと、latent decomposition側のAllman、Matias and Rhodesです。Holman and GlasおよびKuhaらは、IRTやlatent response modelにおいてnonignorable item nonresponseを扱う応用上近接した研究です。質疑では、各論文が識別する対象と、本稿の二段階のどこに対応するかを区別して説明します。"
        ],
    ),
    (
        "Appendix Slide 1  Extension-kernel inversion",
        [
            "extension pairのmode-j unfoldingは、M jと、p、G、M aからなる既知行列の積として表されます。anchor Kruskal条件からGとM aのKhatri–Rao積がfull column rankになるため、Moore–Penrose逆行列を用いてM jを一意に回復できます。これを全extension itemsへ繰り返します。"
        ],
    ),
    (
        "Appendix Slide 2  Empirical diagnostics",
        [
            "候補となるIV、latent shifter、anchor itemsの割当てについて、relevance、有限カテゴリcomplete-case operatorのrank、supported-block positivity、third-mode rank、anchor separationはデータから診断できます。冗長なblocksから回復される測定核の一致はoveridentifying restrictionになります。",
            "ただし、診断に適合することだけでshadow exclusion、measurement exclusion、局所独立性を検証できるわけではありません。不適合は候補設計を反証できますが、適合は全仮定の正しさを保証しません。"
        ],
    ),
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
    fld_char_1 = OxmlElement("w:fldChar")
    fld_char_1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "
    fld_char_2 = OxmlElement("w:fldChar")
    fld_char_2.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char_1, instr_text, fld_char_2])


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
    normal.font.name = "Arial Unicode MS"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial Unicode MS")
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    title_style = styles["Title"]
    title_style.font.name = "Arial Unicode MS"
    title_style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial Unicode MS")
    title_style.font.size = Pt(20)
    title_style.font.bold = True
    title_style.font.color.rgb = RGBColor(0, 0, 0)
    title_style.paragraph_format.space_after = Pt(12)

    for style_name, size in [("Heading 1", 15), ("Heading 2", 12.5)]:
        style = styles[style_name]
        style.font.name = "Arial Unicode MS"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial Unicode MS")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(5)
        style.paragraph_format.keep_with_next = True

    if "Slide Reference" not in styles:
        ref_style = styles.add_style("Slide Reference", WD_STYLE_TYPE.PARAGRAPH)
        ref_style.font.name = "Arial Unicode MS"
        ref_style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial Unicode MS")
        ref_style.font.size = Pt(9)
        ref_style.font.color.rgb = RGBColor(80, 80, 80)
        ref_style.paragraph_format.space_after = Pt(3)

    header = section.header.paragraphs[0]
    header.text = "欠測IVと潜在変数モデリングによる非無作為欠測の識別"
    set_run_font(header.runs[0], "Arial Unicode MS", "Arial Unicode MS", 8.5)
    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_page_number(section.footer.paragraphs[0])

    doc.add_paragraph("欠測IVと潜在変数モデリングによる非無作為欠測の識別", style="Title")
    subtitle = doc.add_paragraph("英語Beamer対応 日本語発表原稿")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in subtitle.runs:
        set_run_font(run, "Arial Unicode MS", "Arial Unicode MS", 12, True)

    opening = doc.add_paragraph()
    opening.add_run(
        "本原稿は、英語Beamerの各スライドに対応する口頭説明用の日本語原稿である。"
        "識別対象、仮定、定理の適用範囲をスライド間で一貫させ、証明は発表時に必要な論理だけを説明する。"
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
            set_run_font(run, "Arial Unicode MS", "Arial Unicode MS", 10, True)
    set_repeat_table_header(table.rows[0])
    rows = [
        ("Slides 1–5", "問題設定、既存研究、潜在分解に残る識別問題"),
        ("Slides 6–12", "Stage 1  supported-block lawの回復"),
        ("Slides 13–18", "Stage 2  有限潜在クラスのtensor分解"),
        ("Slides 19–24", "推定、計算、simulation、結論"),
        ("References and Appendix", "文献関係と質疑用の補足"),
    ]
    for left, right in rows:
        cells = table.add_row().cells
        cells[0].text = left
        cells[1].text = right
        for cell in cells:
            for run in cell.paragraphs[0].runs:
                set_run_font(run, "Arial Unicode MS", "Arial Unicode MS", 10.5)

    doc.add_page_break()

    for index, (heading, paragraphs) in enumerate(SLIDES):
        doc.add_paragraph(heading, style="Heading 1")
        for text in paragraphs:
            p = doc.add_paragraph(text)
            p.paragraph_format.keep_together = True
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
