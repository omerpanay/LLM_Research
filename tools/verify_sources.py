"""Check every arXiv-backed row of the source registry against the live arXiv abstract page.

Usage: python3 -I tools/verify_sources.py docs/research/sources.csv [--out docs/research/sources_check.md]

For each row whose url or id contains an arXiv id (NNNN.NNNNN), fetch https://arxiv.org/abs/<id>, read the
citation_title meta tag, and compare it with the registry title (normalised token overlap). Rows without an arXiv id
are listed as "not checked automatically" (venue/standard/blog sources need a manual check).
Never edits the registry; writes a report.
"""
import csv
import html
import re
import sys
import time
import urllib.request

ARXIV = re.compile(r"(\d{4}\.\d{4,5})")


def norm(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"a", "an", "the", "of", "for", "and", "in", "on", "to", "with"}


def fetch_title(aid):
    req = urllib.request.Request(f"https://arxiv.org/abs/{aid}", headers={"User-Agent": "source-checker/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        page = r.read().decode("utf-8", "ignore")
    m = re.search(r'citation_title" content="([^"]+)', page)
    d = re.search(r'citation_date" content="([^"]+)', page)
    return (html.unescape(m.group(1)) if m else None), (d.group(1) if d else None)


def main(path, out):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    lines = ["| id | registry title | arXiv title | overlap | status |", "|---|---|---|---|---|"]
    stats = {"ok": 0, "mismatch": 0, "unchecked": 0, "error": 0}
    cache = {}
    for r in rows:
        m = ARXIV.search((r.get("url") or "") + " " + (r.get("notes") or ""))
        if not m:
            stats["unchecked"] += 1
            lines.append(f"| {r['id']} | {r['title'][:70]} | — | — | not checked automatically |")
            continue
        aid = m.group(1)
        try:
            if aid not in cache:
                cache[aid] = fetch_title(aid)
                time.sleep(1.0)
            t, date = cache[aid]
        except Exception as e:  # network errors are reported, not hidden
            stats["error"] += 1
            lines.append(f"| {r['id']} | {r['title'][:70]} | error: {type(e).__name__} | — | ERROR |")
            continue
        a, b = norm(r["title"]), norm(t or "")
        ov = len(a & b) / max(1, min(len(a), len(b)))
        status = "ok" if t and ov >= 0.6 else "MISMATCH"
        stats["ok" if status == "ok" else "mismatch"] += 1
        lines.append(f"| {r['id']} | {r['title'][:70]} | {(t or '')[:70]} ({aid}, {date}) | {ov:.2f} | {status} |")
    head = [f"# Source check ({time.strftime('%Y-%m-%d')})", "",
            f"arXiv ids checked against live abstract pages: {stats['ok']} ok, {stats['mismatch']} mismatch, "
            f"{stats['error']} errors; {stats['unchecked']} rows without an arXiv id (venue/standard/blog; manual check).", ""]
    open(out, "w", encoding="utf-8").write("\n".join(head + lines) + "\n")
    print(head[2])


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "docs/research/sources_check.md"
    main(sys.argv[1], out)
