TEX := manuscript/main.tex
PDF := build/formal/main/main.pdf
ABSTRACT_TEX := notes/onepage/vector_missing_iv_identification_onepage.tex
ABSTRACT_PDF := build/formal/vector_missing_iv_identification_onepage/vector_missing_iv_identification_onepage.pdf
PROOF_TEX := manuscript/vector_missing_iv_identification_proof.tex
PROOF_PDF := build/formal/vector_missing_iv_identification_proof/vector_missing_iv_identification_proof.pdf
TEMPLATE_TEX := notes/onepage/a4_two_column_format_template.tex
TEMPLATE_PDF := build/templates/a4_two_column_format_template/a4_two_column_format_template.pdf
READING_DHAULTFOEUILLE_TEX := notes/reading/dhaultfoeuille2010_annotated_ja.tex
READING_DHAULTFOEUILLE_PDF := build/supplementary_reading/dhaultfoeuille2010/dhaultfoeuille2010_annotated_ja.pdf
READING_ZHAO_SHAO_TEX := notes/reading/zhao_shao2015_annotated_ja.tex
READING_ZHAO_SHAO_PDF := build/supplementary_reading/zhao_shao2015/zhao_shao2015_annotated_ja.pdf
READING_KANO_TAKAI_TEX := notes/reading/kano_takai2011_nmar_latent_annotated_ja.tex
READING_KANO_TAKAI_PDF := build/supplementary_reading/kano_takai2011/kano_takai2011_nmar_latent_annotated_ja.pdf

.PHONY: pdf abstract proof template reading-dhaultfoeuille2010 reading-zhao-shao2015 reading-kano-takai2011 clean

pdf: $(PDF)

$(PDF): $(TEX) .latexmkrc
	latexmk -outdir=build/formal/main $(TEX)

abstract: $(ABSTRACT_PDF)

$(ABSTRACT_PDF): $(ABSTRACT_TEX) .latexmkrc
	latexmk -outdir=build/formal/vector_missing_iv_identification_onepage $(ABSTRACT_TEX)

proof: $(PROOF_PDF)

$(PROOF_PDF): $(PROOF_TEX) .latexmkrc
	latexmk -outdir=build/formal/vector_missing_iv_identification_proof $(PROOF_TEX)

template: $(TEMPLATE_PDF)

$(TEMPLATE_PDF): $(TEMPLATE_TEX) .latexmkrc
	latexmk -outdir=build/templates/a4_two_column_format_template $(TEMPLATE_TEX)

reading-dhaultfoeuille2010: $(READING_DHAULTFOEUILLE_PDF)

$(READING_DHAULTFOEUILLE_PDF): $(READING_DHAULTFOEUILLE_TEX) .latexmkrc
	latexmk -outdir=build/supplementary_reading/dhaultfoeuille2010 $(READING_DHAULTFOEUILLE_TEX)

reading-zhao-shao2015: $(READING_ZHAO_SHAO_PDF)

$(READING_ZHAO_SHAO_PDF): $(READING_ZHAO_SHAO_TEX) .latexmkrc
	latexmk -outdir=build/supplementary_reading/zhao_shao2015 $(READING_ZHAO_SHAO_TEX)

reading-kano-takai2011: $(READING_KANO_TAKAI_PDF)

$(READING_KANO_TAKAI_PDF): $(READING_KANO_TAKAI_TEX) .latexmkrc
	latexmk -outdir=build/supplementary_reading/kano_takai2011 $(READING_KANO_TAKAI_TEX)

clean:
	latexmk -C $(TEX)
	latexmk -C $(ABSTRACT_TEX)
	latexmk -C $(PROOF_TEX)
	latexmk -C $(TEMPLATE_TEX)
	latexmk -C $(READING_DHAULTFOEUILLE_TEX)
	latexmk -C $(READING_ZHAO_SHAO_TEX)
	latexmk -C $(READING_KANO_TAKAI_TEX)
