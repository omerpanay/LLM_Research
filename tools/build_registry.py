"""Merge the fenced CSV 'Registry rows' blocks of docs/research/lit/*.md (+ own artefacts) into docs/research/sources.csv.

Usage: python3 -I tools/build_registry.py
Checks: required columns, duplicate ids, tier values; prints a summary. Never invents rows: own artefacts are listed
explicitly below.
"""
import csv
import glob
import io
import re

COLS = ["id", "short_name", "title", "authors_first", "year", "venue", "tier", "verification", "url", "used_for", "notes"]

OWN = [
    ["R-01", "AgentLAB repo", "TanqiuJiang/AgentLAB (code + stored task-injection results)", "Jiang", "2026", "GitHub", "T4",
     "PRIMARY-READ (cloned, commit 36f58e6)", "https://github.com/TanqiuJiang/AgentLAB", "codebase audit; ASR-vs-budget analysis",
     "artefact of the ICML 2026 paper; analysed in results/agentlab_ti_budget"],
    ["R-02", "CAR-bench repo", "CAR-bench/car-bench (code + published trajectories)", "Kirmayr", "2026", "GitHub", "T4",
     "PRIMARY-READ (cloned, commit ce6dc9d)", "https://github.com/CAR-bench/car-bench", "environment basis; noise-floor analysis; cost model",
     "artefact of the ACL 2026 paper; analysed in results/carbench_noise_floor"],
    ["R-03", "AgentDojo repo", "ethz-spylab/agentdojo (code + stored runs)", "Debenedetti", "2024", "GitHub", "T4",
     "PRIMARY-READ (cloned; ground-truth suite check run)", "https://github.com/ethz-spylab/agentdojo",
     "integration hub; clean-run oracle replay", "analysed in results/agentdojo_clean_oracle_floor"],
    ["R-04", "CaMeL repo", "google-research/camel-prompt-injection", "Debenedetti", "2025", "GitHub", "T4",
     "PRIMARY-READ (cloned, commit f083b6b)", "https://github.com/google-research/camel-prompt-injection",
     "defence baseline; policy engine", ""],
    ["R-05", "CAR-bench IJCAI harness", "CAR-bench/car-bench-ijcai (competition harness)", "Kirmayr", "2026", "GitHub", "T4",
     "PRIMARY-READ (cloned)", "https://github.com/CAR-bench/car-bench-ijcai", "task counts; A2A harness", ""],
    ["R-06", "VW CEA press release", "Auto China 2026: Volkswagen Group unveils record product offensive and Agentic AI roadmap for China",
     "Volkswagen Group", "2026", "press release", "T4", "PRIMARY-READ",
     "https://www.volkswagen-group.com/en/press-releases/auto-china-2026-volkswagen-group-unveils-record-product-offensive-and-agentic-ai-roadmap-for-china-20333",
     "deployment context", "also in lit/automotive.md"],
]


def blocks(path):
    text = open(path, encoding="utf-8").read()
    i = text.find("Registry rows")
    if i < 0:
        return []
    out = []
    for m in re.finditer(r"```(?:csv)?\n(.*?)```", text[i:], re.S):
        out.extend(csv.reader(io.StringIO(m.group(1))))
    return out


def main():
    rows, seen, problems = [], {}, []
    for path in sorted(glob.glob("docs/research/lit/*.md")):
        for r in blocks(path):
            if not r or r[0].strip() in ("id", ""):
                continue
            if len(r) != len(COLS):
                problems.append(f"{path}: {r[0]} has {len(r)} columns")
                r = (r + [""] * len(COLS))[:len(COLS)]
            d = dict(zip(COLS, (x.strip() for x in r)))
            d["notes"] = (d["notes"] + f" [from {path.split('/')[-1]}]").strip()
            if d["id"] in seen:
                problems.append(f"duplicate id {d['id']} in {path} (first in {seen[d['id']]})")
                continue
            seen[d["id"]] = path
            rows.append(d)
    for r in OWN:
        rows.append(dict(zip(COLS, r)))
    with open("docs/research/sources.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    tiers = {}
    for r in rows:
        t = re.match(r"T\d", r["tier"])
        tiers[t.group(0) if t else "?"] = tiers.get(t.group(0) if t else "?", 0) + 1
    ver = {}
    for r in rows:
        k = "PRIMARY" if "PRIMARY" in r["verification"].upper() else ("ABSTRACT" if "ABSTRACT" in r["verification"].upper()
                                                                        else ("UNVERIFIED" if "UNVERIFIED" in r["verification"].upper() else "other"))
        ver[k] = ver.get(k, 0) + 1
    print(f"{len(rows)} rows; tiers {dict(sorted(tiers.items()))}; verification {ver}")
    for p in problems:
        print("PROBLEM:", p)


if __name__ == "__main__":
    main()
