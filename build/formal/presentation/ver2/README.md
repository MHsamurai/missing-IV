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
