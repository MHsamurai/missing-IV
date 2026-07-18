# ver2: active presentation workspace

This directory is the editable successor to `../ver1/`. It was initialized as
an exact copy of the 2026-07-18 interim presentation.

## Working rule

- Make all future presentation changes in this directory.
- Keep the TeX source, manuscript, bibliography, PDF, and PPTX synchronized.
- Do not apply later edits back to `../ver1/`.

## Build

Run from this directory:

```bash
latexmk -norc -lualatex -interaction=nonstopmode capacity_mnar_beamer_formal.tex
```

The copied PDF and PPTX are the ver1 baseline and should be regenerated when
the ver2 source changes.

## Economic Letters core model

- `economic_letters_core_model.tex`: formal model separating item-level posting costs from a shared time budget, defining the experienced-user population, and stating target-specific nonparametric identification.
- `economic_letters_core_model.pdf`: compiled research note for review and later conversion into the paper or slides.
