# Presentation-only figures

These assets preserve the research model and saved simulation results while
making labels readable at their native size in Beamer. Do not use `resizebox`
or shrink the chart PDFs when including them.

- TikZ labels and slide prose use 10.6 TeX pt. With the current XeLaTeX font
  conversion, the final Latin text measures approximately 10.52 PDF pt.
- Chart PDFs are 14 x 5 cm, with 11 PDF pt text. The outcome inference chart
  has separate bias/SD and SE/coverage pages.
- Mathematical subscripts/superscripts retain conventional typesetting.
  Citation-only notes, explanatory footnotes, and the footer use 8 TeX pt.
- Paper figures in `notes/figures` and simulation data are unchanged.

Rebuild charts from the saved CSV results:

```sh
simulation/.venv/bin/python scripts/build_readable_slide_charts.py
make beamer
```

Audit transformed font sizes, including embedded PDF figures:

```sh
python scripts/audit_slide_font_sizes.py --classify --json /tmp/slide-font-audit.json
```

The audit reports candidates, not automatic failures. Review genuine math
scripts and note regions separately, and visually inspect rendered pages for
overlap. The Word script builder checks slide titles, order, and Appendix
boundaries against the Beamer source before generating the speaking script.
