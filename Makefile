TEX := manuscript/main.tex
PDF := build/main.pdf
READING_DHAULTFOEUILLE_TEX := notes/reading/dhaultfoeuille2010_annotated_ja.tex
READING_DHAULTFOEUILLE_PDF := build/dhaultfoeuille2010_annotated_ja.pdf

.PHONY: pdf reading-dhaultfoeuille2010 clean

pdf: $(PDF)

$(PDF): $(TEX) .latexmkrc
	latexmk $(TEX)

reading-dhaultfoeuille2010: $(READING_DHAULTFOEUILLE_PDF)

$(READING_DHAULTFOEUILLE_PDF): $(READING_DHAULTFOEUILLE_TEX) .latexmkrc
	latexmk $(READING_DHAULTFOEUILLE_TEX)

clean:
	latexmk -C $(TEX)
	latexmk -C $(READING_DHAULTFOEUILLE_TEX)
