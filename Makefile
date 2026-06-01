TEX := manuscript/main.tex
PDF := build/main.pdf

.PHONY: pdf clean

pdf: $(PDF)

$(PDF): $(TEX) .latexmkrc
	latexmk $(TEX)

clean:
	latexmk -C $(TEX)
