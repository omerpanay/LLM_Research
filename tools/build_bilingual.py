"""Build side-by-side English | Turkish HTML pages (and a print layout for PDF) from line-aligned Markdown pairs.

Each Turkish file in "Tez Araştırması (TR-EN)/turkce-md/" has exactly the same lines as its English source
(line i translates line i). Lines are grouped into blocks (paragraph, list, table, fenced code); each block is shown
as one row: English left, Turkish right. Identical blocks (code) span both columns.

Usage: python tools/build_bilingual.py      (needs the `markdown` package)
"""
import html
import os
import re

import markdown

ROOT = "Tez Araştırması (TR-EN)"
TR_DIR = os.path.join(ROOT, "turkce-md")
OUT_DIR = os.path.join(ROOT, "yan-yana-html")

DOCS = [  # (english source, turkish file, Turkish title)
    ("docs/research/00_INDEX.md", "00_INDEX.md", "00 · İndeks ve yönetici özeti"),
    ("docs/research/01_state_of_the_field.md", "01_state_of_the_field.md", "01 · Alanın durumu"),
    ("docs/research/02_gaps_ranked.md", "02_gaps_ranked.md", "02 · Sıralanmış araştırma boşlukları"),
    ("docs/research/03_thesis_design.md", "03_thesis_design.md", "03 · Tez tasarımı"),
    ("docs/research/04_automotive_threat_model.md", "04_automotive_threat_model.md", "04 · Otomotiv tehdit modeli"),
    ("docs/research/05_technical_feasibility.md", "05_technical_feasibility.md", "05 · Teknik fizibilite"),
    ("docs/research/06_roadmap.md", "06_roadmap.md", "06 · Haftalık yol haritası"),
    ("docs/research/07_supervisor_questions.md", "07_supervisor_questions.md", "07 · Hocaya sorulacak 10 soru"),
    ("docs/research/08_discoveries_and_ideas.md", "08_discoveries_and_ideas.md", "08 · Keşifler ve özgün fikirler"),
    ("docs/research/09_jev_clarification.md", "09_jev_clarification.md", "09 · JEV ne demek?"),
    ("docs/research/lit/codebase_audit.md", "10_codebase_audit.md", "10 · Kod denetimi (AgentLAB, CAR-bench, AgentDojo, CaMeL)"),
    ("results/agentlab_ti_budget/README.md", "R1_agentlab_ti_budget.md", "R1 · Ölçüm: AgentLAB deneme bütçesi"),
    ("results/agentdojo_clean_oracle_floor/README.md", "R2_agentdojo_clean_oracle_floor.md", "R2 · Ölçüm: AgentDojo temiz koşu tekrar oynatma"),
    ("results/carbench_noise_floor/README.md", "R3_carbench_noise_floor.md", "R3 · Ölçüm: CAR-bench gürültü tabanı"),
    ("results/prototype/README.md", "R4_prototype.md", "R4 · Prototip (carlab_mini) sonuçları"),
]

CSS = """
:root{--bg:#fff;--fg:#1d1d1f;--muted:#666;--line:#e3e3e3;--en:#f7f8fa;--tr:#fffaf2;--accent:#b4002d}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151515;--fg:#eaeaea;--muted:#aaa;--line:#333;--en:#1d2026;--tr:#26221a;--accent:#ff6b8b}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 "DejaVu Sans","Noto Sans",Arial,sans-serif}
main{max-width:1500px;margin:0 auto;padding:16px}
h1.doc{font-size:22px;border-bottom:3px solid var(--accent);padding-bottom:6px;margin:8px 0 12px}
.legend{display:grid;grid-template-columns:1fr 1fr;gap:12px;font-weight:bold;color:var(--muted);font-size:12px;
  position:sticky;top:0;background:var(--bg);padding:4px 0;z-index:2}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px;border-top:1px solid var(--line);padding:4px 0;break-inside:avoid}
.row.long{break-inside:auto}
.cell{min-width:0;overflow-wrap:break-word;padding:2px 8px;border-radius:4px}
.cell.en{background:var(--en)} .cell.tr{background:var(--tr)}
.row.same .cell{grid-column:1/-1;background:transparent}
table{border-collapse:collapse;width:100%;font-size:11.5px}
th,td{border:1px solid var(--line);padding:3px 5px;vertical-align:top;text-align:left;overflow-wrap:break-word;hyphens:auto}
td:first-child,th:first-child{min-width:4.5em}
pre{white-space:pre-wrap;font-size:11px;background:var(--en);padding:6px;border-radius:4px}
code{font-size:0.92em}
h1,h2,h3,h4{margin:6px 0 4px;line-height:1.25} h1{font-size:19px} h2{font-size:17px} h3{font-size:15px}
p,ul,ol{margin:4px 0} ul,ol{padding-left:20px}
.nav{font-size:13px;margin:6px 0 14px} .nav a{color:var(--accent)}
.cover{padding:30px 0} .cover h1{font-size:30px;border:0} .cover li{margin:3px 0}
@media (max-width:760px){.row,.legend{grid-template-columns:1fr}.legend{display:none}
  .cell.en::before{content:"EN";font-size:10px;color:var(--muted);display:block}
  .cell.tr::before{content:"TR";font-size:10px;color:var(--muted);display:block}}
@media print{body{font-size:10.5px}main{max-width:none;padding:0}.legend{position:static}
  .doc-sec{break-before:page} .nav{display:none} a{color:inherit;text-decoration:none}
  table{font-size:9px} pre{font-size:8.5px}}
@page{size:A4 landscape;margin:10mm}
"""


def blocks(lines):
    """Group line indices into blocks: fenced code, table, heading, or paragraph/list run."""
    out, i, n = [], 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        j = i
        if lines[i].lstrip().startswith("```"):
            j += 1
            while j < n and not lines[j].lstrip().startswith("```"):
                j += 1
            j += 1
        elif lines[i].lstrip().startswith("#"):
            j += 1
        else:
            is_table = lines[i].lstrip().startswith("|")
            while j < n and lines[j].strip() and lines[j].lstrip().startswith("|") == is_table \
                    and not lines[j].lstrip().startswith(("#", "```")):
                j += 1
        out.append((i, min(j, n)))
        i = j
    return out


def md(text):
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def render_pair(en_lines, tr_lines):
    rows = []
    for a, b in blocks(en_lines):
        e = "\n".join(en_lines[a:b])
        t = "\n".join(tr_lines[a:b])
        long = " long" if b - a > 14 else ""
        if e.strip() == t.strip():
            rows.append(f'<div class="row same{long}"><div class="cell">{md(e)}</div></div>')
        else:
            rows.append(f'<div class="row{long}"><div class="cell en" lang="en">{md(e)}</div>'
                        f'<div class="cell tr" lang="tr">{md(t)}</div></div>')
    return "\n".join(rows)


def page(title, body):
    return (f'<!doctype html><html lang="tr"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>'
            f'<style>{CSS}</style></head><body><main>{body}</main></body></html>')


def check(en, tr, name):
    problems = []
    if len(en) != len(tr):
        problems.append(f"{name}: {len(en)} EN lines vs {len(tr)} TR lines")
    for k, (x, y) in enumerate(zip(en, tr)):
        if (x.strip() == "") != (y.strip() == "") or x.count("|") != y.count("|"):
            problems.append(f"{name}: line {k + 1} structure differs")
    return problems


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    legend = '<div class="legend"><div>ENGLISH (original)</div><div>TÜRKÇE (çeviri)</div></div>'
    sections, toc, problems = [], [], []
    for k, (src, trf, title) in enumerate(DOCS):
        en = open(src, encoding="utf-8").read().rstrip("\n").split("\n")
        tr = open(os.path.join(TR_DIR, trf), encoding="utf-8").read().rstrip("\n").split("\n")
        problems += check(en, tr, trf)
        body = render_pair(en, tr)
        slug = os.path.splitext(trf)[0]
        prev = f'<a href="{os.path.splitext(DOCS[k - 1][1])[0]}.html">← önceki</a> · ' if k else ""
        nxt = f' · <a href="{os.path.splitext(DOCS[k + 1][1])[0]}.html">sonraki →</a>' if k + 1 < len(DOCS) else ""
        nav = f'<div class="nav">{prev}<a href="index.html">içindekiler</a>{nxt} · kaynak: <code>{src}</code></div>'
        open(os.path.join(OUT_DIR, slug + ".html"), "w", encoding="utf-8").write(
            page(title, f'<h1 class="doc">{html.escape(title)}</h1>{nav}{legend}{body}'))
        sections.append(f'<section class="doc-sec" id="{slug}"><h1 class="doc">{html.escape(title)}</h1>'
                        f'<div class="nav">kaynak: <code>{src}</code></div>{legend}{body}</section>')
        toc.append((slug, title, src))
    cover = ('<div class="cover"><h1>Tez Araştırması — İngilizce | Türkçe yan yana</h1>'
             '<p>Robustness of in-vehicle LLM agents to long-horizon adversarial attacks · araştırma paketi, Kasım 2026.</p>'
             '<p>Sol sütun: İngilizce orijinal. Sağ sütun: Türkçe çeviri. Sayılar, kaynak kimlikleri (A-15, D-09 …) '
             've kod aynen korunmuştur. Bir çelişki görürsen <b>İngilizce orijinal geçerlidir</b>.</p><ol>'
             + "".join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for s, t, _ in toc) + "</ol></div>")
    open(os.path.join(OUT_DIR, "hepsi-tek-sayfada.html"), "w", encoding="utf-8").write(page("Tez Araştırması TR-EN", cover + "\n".join(sections)))
    index = ('<div class="cover"><h1>Tez Araştırması — İngilizce | Türkçe yan yana</h1><p>Okuma sırası:</p><ol>'
             + "".join(f'<li><a href="{s}.html">{html.escape(t)}</a></li>' for s, t, _ in toc) + "</ol></div>")
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page("İçindekiler", index))
    print(f"{len(DOCS)} documents built")
    for p in problems:
        print("PROBLEM:", p)


if __name__ == "__main__":
    main()
