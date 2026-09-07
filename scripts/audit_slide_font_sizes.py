"""Audit transformed PDF font sizes, including text inside vector figures.

Requires pdfminer.six (also installed with pdfplumber). Sizes default to TeX pt;
use --unit pdf for 1/72-inch points. No candidates are automatically exempted.
JSON contains all size groups, optional positional estimates, and body-size
estimates. Raster/outlined text and semantic note exemptions need manual review.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import io
import json
from math import hypot
from pathlib import Path
import re
import sys
import unicodedata

from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


DEFAULT_PDF = (Path(__file__).resolve().parents[1] / "build/formal/"
               "vector_missing_iv_identification_beamer/"
               "vector_missing_iv_identification_beamer.pdf")
MATH_FONT = re.compile(r"(?:CM(?:MI|SY|EX|R)|MS[AB]M|Math|Symbol|STIX|"
                       r"LM(?:Roman|Math)|LatinModernMath)", re.I)


def language_text(text):
    """Latin/Japanese letters; digits and punctuation remain in other groups."""
    return any(unicodedata.category(c).startswith("L") and
               any(name in unicodedata.name(c, "") for name in
                   ("LATIN", "HIRAGANA", "KATAKANA", "CJK")) for c in text)


def union_bbox(chars):
    return [round(fn(c["bbox"][i] for c in chars), 3)
            for i, fn in enumerate((min, min, max, max))]


def sample(chars, limit):
    # Preserve PDF paint order; gaps and baseline changes improve readability
    # without treating the reconstructed sample as authoritative reading order.
    result = ""
    previous = None
    for c in chars:
        if previous:
            if abs(c["baseline"] - previous["baseline"]) > 2:
                result += " | "
            elif c["bbox"][0] - previous["bbox"][2] > 1:
                result += " "
        result += c["text"]
        previous = c
        if len(result) >= limit:
            return result[:limit] + "..."
    return result


class FontCollector(PDFPageAggregator):
    def render_char(self, matrix, font, fontsize, scaling, rise,
                    cid, ncs, graphicstate):
        advance = super().render_char(
            matrix, font, fontsize, scaling, rise, cid, ncs, graphicstate)
        char = self.cur_item._objs[-1]
        if char.get_text().strip():
            name = font.fontname
            if isinstance(name, bytes):
                name = name.decode("latin1")
            self.chars.append({
                "text": char.get_text(), "font": name,
                "size": abs(fontsize) * hypot(matrix[2], matrix[3]) * self.factor,
                "bbox": tuple(v * self.user_unit for v in char.bbox),
                "baseline": (matrix[5] + rise * matrix[3]) * self.user_unit,
                "horizontal": abs(matrix[1]) < 1e-6 and abs(matrix[2]) < 1e-6,
                "math_font_estimate": bool(MATH_FONT.search(name)),
            })
        return advance


def classify(c, chars, bottom, footer_band):
    tags = []
    if c["bbox"][1] < bottom + footer_band:
        tags.append("footer_position_estimate")
    if c["math_font_estimate"]:
        tags.append("math_font_estimate")
    elif language_text(c["text"]):
        tags.append("non_math_latin_japanese_candidate")
    # Nearby larger glyphs suggest scripts, but cannot establish semantics.
    if c["horizontal"]:
        for other in chars:
            if (not other["horizontal"] or
                    not 1.15 * c["size"] <= other["size"] <= 2.2 * c["size"]):
                continue
            gap = max(other["bbox"][0] - c["bbox"][2],
                      c["bbox"][0] - other["bbox"][2], 0)
            delta = c["baseline"] - other["baseline"]
            height = other["bbox"][3] - other["bbox"][1]
            if gap <= 4 and 0.5 < abs(delta) < 0.8 * height:
                direction = "below" if delta < 0 else "above"
                tags.append(f"{direction}_baseline_script_estimate")
                break
    return tags or ["unclassified_candidate"]


def audit(data, args):
    manager = PDFResourceManager()
    device = FontCollector(manager)
    interpreter = PDFPageInterpreter(manager, device)
    pages = []
    for number, page in enumerate(PDFPage.get_pages(io.BytesIO(data)), 1):
        device.chars = []
        device.user_unit = float(page.attrs.get("UserUnit", 1))
        device.factor = device.user_unit * (72.27 / 72 if args.unit == "tex" else 1)
        interpreter.process_page(page)
        chars = device.chars
        page_bbox = [v * device.user_unit for v in device.get_result().bbox]
        grouped = defaultdict(list)
        body = Counter()
        for c in chars:
            c["below_minimum"] = c["size"] < args.minimum - args.tolerance
            c["tags"] = classify(c, chars, page_bbox[1], args.footer_band) if args.classify else []
            grouped[(round(c["size"], args.round_digits), c["font"])].append(c)
            if (not c["math_font_estimate"] and language_text(c["text"]) and
                    c["bbox"][1] >= page_bbox[1] + args.footer_band and
                    c["bbox"][3] <= page_bbox[3] - args.header_band):
                body[round(c["size"], args.round_digits)] += len(c["text"])
        groups = []
        for (size, font), members in sorted(grouped.items()):
            candidates = [c for c in members if c["below_minimum"]]
            group = {
                "size": size, "font": font, "glyph_count": len(members),
                "size_range": [min(c["size"] for c in members), max(c["size"] for c in members)],
                "below_minimum_glyphs": len(candidates),
                "bbox_pdf": union_bbox(members), "sample": sample(members, args.sample_chars),
            }
            if args.classify:
                group["candidate_estimates"] = {
                    tag: {"glyph_count": len(subset), "sample": sample(subset, args.sample_chars),
                          "bbox_pdf": union_bbox(subset)}
                    for tag in sorted({t for c in candidates for t in c["tags"]})
                    if (subset := [c for c in candidates if tag in c["tags"]])
                }
            groups.append(group)
        pages.append({
            "page": number, "bbox_pdf": page_bbox,
            "extracted_glyphs": len(chars),
            "below_minimum_glyphs": sum(c["below_minimum"] for c in chars),
            "body_size_estimates": [{"size": s, "letter_count": n}
                                    for s, n in body.most_common(5)],
            "groups": groups,
        })
    device.close()
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--json", metavar="PATH", help="JSON output path, or - for stdout")
    parser.add_argument("--classify", action="store_true", help="Include overlapping positional/script estimates")
    parser.add_argument("--source", type=Path, help="Compare source mtime with PDF; does not check dependencies")
    parser.add_argument("--minimum", type=float, default=10.5)
    parser.add_argument("--unit", choices=("tex", "pdf"), default="tex")
    parser.add_argument("--tolerance", type=float, default=0.01)
    parser.add_argument("--round-digits", type=int, default=2)
    parser.add_argument("--sample-chars", type=int, default=180)
    parser.add_argument("--footer-band", type=float, default=18, help="Physical PDF points; estimate only")
    parser.add_argument("--header-band", type=float, default=35, help="Exclude from body-size estimate only")
    args = parser.parse_args()
    if (args.minimum <= 0 or not 0 <= args.tolerance < args.minimum or
            args.round_digits < 0 or args.sample_chars < 1 or
            min(args.footer_band, args.header_band) < 0):
        parser.error("Invalid threshold, precision, sample length, or positional band")
    before = args.pdf.stat()
    data = args.pdf.read_bytes()
    pages = audit(data, args)
    after = args.pdf.stat()
    report = {
        "pdf": str(args.pdf.resolve()), "sha256": hashlib.sha256(data).hexdigest(),
        "pdf_mtime_utc": datetime.fromtimestamp(before.st_mtime, timezone.utc).isoformat(),
        "pdf_changed_during_audit": (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size),
        "minimum": args.minimum, "unit": args.unit, "tolerance": args.tolerance,
        "round_digits": args.round_digits,
        "classification_enabled": args.classify,
        "footer_band_pdf_points": args.footer_band, "header_band_pdf_points": args.header_band,
        "limitations": [
            "Candidates are not failures; no math scripts, notes, or footer regions are automatically exempted.",
            "Font and nearby-baseline classifications are estimates, overlap, and require source/visual review.",
            "Body-size estimates count Latin/Japanese letters, not semantic normaltext; notes and labels can dominate.",
            "Bounding boxes use rotated-page coordinates, bottom-left origin, physical 1/72-inch PDF points.",
            "Nominal size uses the transformed font vertical axis, not glyph bounding-box height.",
            "Outlined/rasterized text is not measured; invisible or clipped PDF text may be counted.",
        ],
        "pages": pages,
    }
    if args.source:
        report["source"] = str(args.source.resolve())
        source_stat = args.source.stat()
        report["source_mtime_utc"] = datetime.fromtimestamp(source_stat.st_mtime, timezone.utc).isoformat()
        report["source_newer_than_pdf"] = source_stat.st_mtime_ns > before.st_mtime_ns
    output = sys.stderr if args.json == "-" else sys.stdout
    print(f"{len(pages)} pages; minimum {args.minimum:g} {args.unit} pt; review candidates, not automatic failures", file=output)
    for page in pages:
        print(f"Page {page['page']}: {page['below_minimum_glyphs']} small glyphs; body estimates {page['body_size_estimates']}", file=output)
        for group in page["groups"]:
            if group["below_minimum_glyphs"]:
                print(f"  {group['size']:g} {group['font']} bbox={group['bbox_pdf']} {group['sample']}", file=output)
    if args.json:
        encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.json == "-":
            sys.stdout.write(encoded)
        else:
            target = Path(args.json)
            if target.resolve() in {args.pdf.resolve(), Path(__file__).resolve()} or (args.source and target.resolve() == args.source.resolve()):
                parser.error("JSON output must not overwrite PDF, source, or audit script")
            target.write_text(encoded, encoding="utf-8")
    if report["pdf_changed_during_audit"]:
        print("WARNING: PDF changed during audit; rerun after compilation completes.", file=output)
        return 2
    if report.get("source_newer_than_pdf"):
        print("WARNING: source is newer than PDF; this is not final validation.", file=output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
