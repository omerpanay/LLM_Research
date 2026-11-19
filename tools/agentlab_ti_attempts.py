"""How much of AgentLAB's task-injection ASR comes from attacker retries?

AgentLAB (ICML 2026) publishes per-attempt results of its long-horizon task-injection attack (built on AgentDojo,
whose security check reads the environment state). Each user_task x injection_task pair has several attempts
(snippet iterations/variants); a pair counts as compromised if ANY attempt succeeds. This script measures ASR as a
function of the attacker's attempt budget, at zero cost.

Usage: python3 -I tools/agentlab_ti_attempts.py <AgentLAB>/Task-Injection/agentdojo/res/long_horizon <out_dir>
"""
import collections
import csv
import json
import os
import sys


def load_pairs(model_dir):
    pairs = {}
    for root, _, files in os.walk(model_dir):
        if "results.jsonl" in files and os.path.basename(root).startswith("user_task_"):
            rows = [json.loads(l) for l in open(os.path.join(root, "results.jsonl"), encoding="utf-8") if l.strip()]
            pairs[os.path.relpath(root, model_dir)] = rows
    return pairs


def main(base, out):
    os.makedirs(out, exist_ok=True)
    table = []
    for model in sorted(os.listdir(base)):
        mdir = os.path.join(base, model)
        if not os.path.isdir(mdir):
            continue
        pairs = load_pairs(mdir)
        if len(pairs) < 20:
            continue
        n = len(pairs)
        attempts = [len(v) for v in pairs.values()]
        first = sum(bool(v and v[0]["security_passed"]) for v in pairs.values())
        anyok = sum(any(r["security_passed"] for r in v) for v in pairs.values())
        stealth = sum(any(r["security_passed"] and r["utility_passed"] for r in v) for v in pairs.values())
        # ASR as a function of budget b: success within the first b attempts
        maxb = max(attempts)
        curve = []
        for b in (1, 2, 3, 5, 10, 20, maxb):
            if b > maxb:
                continue
            curve.append((b, sum(any(r["security_passed"] for r in v[:b]) for v in pairs.values())))
        first_success = [next((i + 1 for i, r in enumerate(v) if r["security_passed"]), None) for v in pairs.values()]
        fs = sorted(x for x in first_success if x)
        med = fs[len(fs) // 2] if fs else None
        table.append({
            "model": model, "suites": ",".join(sorted({p.split(os.sep)[0] for p in pairs})), "pairs": n,
            "attempts_min": min(attempts), "attempts_median": sorted(attempts)[n // 2], "attempts_max": maxb,
            "asr_first_attempt": f"{first}/{n} ({first / n:.1%})", "asr_any_attempt": f"{anyok}/{n} ({anyok / n:.1%})",
            "asr_any_with_user_task_done": f"{stealth}/{n} ({stealth / n:.1%})",
            "median_attempt_of_first_success": med,
            "curve": "; ".join(f"b={b}: {k / n:.1%}" for b, k in curve),
        })
    with open(os.path.join(out, "ti_attempt_budget.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader()
        w.writerows(table)
    for r in table:
        print(json.dumps(r))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
