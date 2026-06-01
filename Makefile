TEX := manuscript/main.tex
PDF := build/main.pdf
READING_DHAULTFOEUILLE_TEX := notes/reading/dhaultfoeuille2010_annotated_ja.tex
READING_DHAULTFOEUILLE_PDF := build/dhaultfoeuille2010_annotated_ja.pdf
READING_ZHAO_SHAO_TEX := notes/reading/zhao_shao2015_annotated_ja.tex
READING_ZHAO_SHAO_PDF := build/zhao_shao2015_annotated_ja.pdf
READING_KANO_TAKAI_TEX := notes/reading/kano_takai2011_nmar_latent_annotated_ja.tex
READING_KANO_TAKAI_PDF := build/kano_takai2011_nmar_latent_annotated_ja.pdf

.PHONY: pdf reading-dhaultfoeuille2010 reading-zhao-shao2015 reading-kano-takai2011 clean

pdf: $(PDF)

$(PDF): $(TEX) .latexmkrc
	latexmk $(TEX)

reading-dhaultfoeuille2010: $(READING_DHAULTFOEUILLE_PDF)

$(READING_DHAULTFOEUILLE_PDF): $(READING_DHAULTFOEUILLE_TEX) .latexmkrc
	latexmk $(READING_DHAULTFOEUILLE_TEX)

reading-zhao-shao2015: $(READING_ZHAO_SHAO_PDF)

$(READING_ZHAO_SHAO_PDF): $(READING_ZHAO_SHAO_TEX) .latexmkrc
	latexmk $(READING_ZHAO_SHAO_TEX)

reading-kano-takai2011: $(READING_KANO_TAKAI_PDF)

$(READING_KANO_TAKAI_PDF): $(READING_KANO_TAKAI_TEX) .latexmkrc
	latexmk $(READING_KANO_TAKAI_TEX)

clean:
	latexmk -C $(TEX)
	latexmk -C $(READING_DHAULTFOEUILLE_TEX)
	latexmk -C $(READING_ZHAO_SHAO_TEX)
	latexmk -C $(READING_KANO_TAKAI_TEX)
