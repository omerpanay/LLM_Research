"""Turn the Turkish guide (Markdown) into a readable HTML page (for PDF printing) and a Word file.

Usage (needs the `markdown` package and pandoc):
    python tools/build_guide.py "Tez Araştırması - Tam Rehber (TR).md"
Then print the HTML to PDF:
    node tools/print_pdf_portrait.js "<name>.html" "<name>.pdf"
"""
import html
import os
import re
import subprocess
import sys

import markdown

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10.3pt; line-height: 1.55; color: #1d1d1f; margin: 0; }
main { max-width: 820px; margin: 0 auto; padding: 0 4px; }
h1, h2, h3, h4, h5 { line-height: 1.25; color: #10243e; break-after: avoid; }
h2 { font-size: 19pt; border-bottom: 3px solid #b4002d; padding-bottom: 6px; margin: 0 0 14px; break-before: page; }
h3 { font-size: 14pt; margin: 22px 0 8px; color: #b4002d; }
h4 { font-size: 12pt; margin: 18px 0 6px; }
h5, h6 { font-size: 10.8pt; margin: 14px 0 4px; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0 6px 0; padding-left: 22px; }
li { margin: 2px 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px; font-size: 8.8pt; line-height: 1.4; }
th, td { border: 1px solid #c9ced6; padding: 5px 6px; vertical-align: top; text-align: left; overflow-wrap: break-word; hyphens: auto; }
th { background: #eef1f6; font-weight: 600; }
tr { break-inside: avoid; }
tbody tr:nth-child(even) td { background: #fafbfc; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; background: #f2f3f5; padding: 1px 3px; border-radius: 3px; overflow-wrap: anywhere; }
pre { background: #f2f3f5; padding: 8px 10px; border-radius: 4px; white-space: pre-wrap; font-size: 8.4pt; break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { margin: 8px 0; padding: 6px 12px; border-left: 4px solid #b4002d; background: #fff6f8; }
hr { border: 0; border-top: 1px solid #d9dde3; margin: 18px 0; }
strong { color: #0d1b2e; }
a { color: #10243e; text-decoration: none; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .kicker { font-size: 11pt; letter-spacing: .12em; text-transform: uppercase; color: #b4002d; font-weight: 600; }
.cover h1 { font-size: 30pt; margin: 10px 0 8px; border: 0; }
.cover .sub { font-size: 13pt; color: #3c4858; max-width: 150mm; }
.cover .meta { margin-top: 26px; font-size: 10.5pt; color: #5a6472; }
.cover .box { margin-top: 30px; border: 1px solid #d9dde3; border-radius: 6px; padding: 12px 16px; font-size: 10pt; max-width: 160mm; }
.toc { break-before: page; }
.toc h2 { break-before: avoid; }
.toc ul { list-style: none; padding-left: 0; }
.toc > ul > li { margin: 8px 0 2px; font-weight: 600; }
.toc ul ul { padding-left: 16px; font-weight: 400; }
.toc ul ul li { margin: 1px 0; font-size: 9.6pt; }
.toc ul ul ul { display: none; }
"""

SYMBOLS = {"✅": "✔", "⚠️": "⚠", "❌": "✘", "‌": ""}


def main(src):
    base = os.path.splitext(src)[0]
    text = open(src, encoding="utf-8").read()
    for a, b in SYMBOLS.items():
        text = text.replace(a, b)
    lines = text.split("\n")
    title = lines[0].lstrip("# ").strip()
    body_md = "\n".join(lines[1:])

    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                           extension_configs={"toc": {"toc_depth": "2-3", "title": ""}})
    body = md.convert(body_md)
    toc = md.toc

    cover = (
        '<section class="cover">'
        '<div class="kicker">Tez araştırması · Volkswagen AG staj tezi</div>'
        f'<h1>{html.escape(title)}</h1>'
        '<div class="sub">Araç içi LLM ajanlarının uzun soluklu saldırılara dayanıklılığı: '
        'Saldırı → Değerlendirme → Savunma</div>'
        '<div class="meta">Hazırlayan: Ömer · Kasım 2026</div>'
        '<div class="box"><b>Nasıl okunur?</b> Önce <b>A</b> (tez planına eklenecekler), sonra '
        '<b>B</b> (düzeltmeler) ve <b>C</b> (açık işler). D–G başvuru bölümleri. '
        'T1 = hakemli büyük konferans/dergi, T2 = hakemli çalıştay/standart, T3 = ön baskı, T4 = blog/şirket. '
        '"Çıkarım:" = kaynağın değil bizim yorumumuz.</div>'
        '</section>'
    )
    page = (f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f'<style>{CSS}</style></head><body><main>{cover}'
            f'<nav class="toc"><h2>İçindekiler</h2>{toc}</nav>{body}</main></body></html>')
    open(base + ".html", "w", encoding="utf-8").write(page)

    # Word: pandoc with a table of contents (headings stay editable; comments and track changes work in Word)
    clean_md = base + ".pandoc.md"
    open(clean_md, "w", encoding="utf-8").write(text)
    subprocess.run(["pandoc", clean_md, "-f", "gfm", "-o", base + ".docx", "--toc", "--toc-depth=2",
                    "-M", f"title={title}", "-M", "lang=tr-TR"], check=True)
    os.remove(clean_md)
    print("written:", base + ".html", base + ".docx")


if __name__ == "__main__":
    main(sys.argv[1])
