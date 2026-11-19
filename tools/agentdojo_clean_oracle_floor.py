"""Do AgentDojo's attack-success oracles fire when there is NO attack?

AgentDojo stores clean runs (`runs/<pipeline>/<suite>/<user_task>/none/none.json`, attack_type None). This script
replays the tool calls of each clean run in a fresh default environment (tools are deterministic), then evaluates
EVERY injection task's security predicate on the resulting state and call trace. A predicate that is true on a clean
run is a false positive of the attack oracle for that (user_task, injection_task) pair: in an attacked run of that
pair, "attack success" could be recorded without the attack having caused it.

Sanity check: the replayed state is also scored with the user task's utility function and compared with the stored
utility; only runs whose replayed utility matches the stored one are counted (replay fidelity).

Usage (needs agentdojo installed):  python tools/agentdojo_clean_oracle_floor.py <agentdojo>/runs <out_dir> [version]
"""
import collections
import copy
import csv
import json
import os
import sys

from agentdojo.functions_runtime import FunctionCall, FunctionsRuntime
from agentdojo.task_suite.load_suites import get_suite


def text_blocks(msg):
    c = msg.get("content")
    if isinstance(c, list):
        return c
    return [{"type": "text", "content": c or ""}]


def replay(suite, run):
    env = suite.load_and_inject_default_environment(suite.get_injection_vector_defaults())
    pre = copy.deepcopy(env)
    rt = FunctionsRuntime(suite.tools)
    trace = []
    for m in run["messages"]:
        for tc in (m.get("tool_calls") or []):
            trace.append(FunctionCall(function=tc["function"], args=tc.get("args", {}), id=tc.get("id")))
            rt.run_function(env, tc["function"], tc.get("args", {}), raise_on_error=False)
    last = next((m for m in reversed(run["messages"]) if m["role"] == "assistant"), {"content": ""})
    return pre, env, trace, text_blocks(last)


def main(runs_dir, out_dir, version="v1"):
    os.makedirs(out_dir, exist_ok=True)
    rows, fp_examples = [], []
    for pipeline in sorted(os.listdir(runs_dir)):
        pdir = os.path.join(runs_dir, pipeline)
        if not os.path.isdir(pdir):
            continue
        for suite_name in ("banking", "slack", "travel", "workspace"):
            sdir = os.path.join(pdir, suite_name)
            if not os.path.isdir(sdir):
                continue
            suite = get_suite(version, suite_name)
            c = collections.Counter()
            for ut in sorted(os.listdir(sdir)):
                f = os.path.join(sdir, ut, "none", "none.json")
                if not ut.startswith("user_task_") or not os.path.exists(f):
                    continue
                run = json.load(open(f, encoding="utf-8"))
                if run.get("error") not in (None, "None"):
                    c["errored"] += 1
                    continue
                try:
                    user_task = suite.get_user_task_by_id(ut)
                    pre, post, trace, out = replay(suite, run)
                    util = suite._check_task_result(user_task, out, pre, post, trace)
                except Exception as e:  # report and skip runs that cannot be replayed
                    c["replay_error"] += 1
                    continue
                c["clean_runs"] += 1
                if bool(util) != bool(run.get("utility")):
                    c["utility_mismatch"] += 1
                    continue
                c["faithful"] += 1
                fired = []
                for it_id, it in suite.injection_tasks.items():
                    try:
                        sec = suite._check_task_result(it, out, pre, post, trace)
                    except Exception:
                        c["security_error"] += 1
                        continue
                    c["pairs"] += 1
                    if sec:
                        c["pairs_fp"] += 1
                        fired.append(it_id)
                if fired:
                    c["runs_with_fp"] += 1
                    if len(fp_examples) < 40:
                        fp_examples.append({"pipeline": pipeline, "suite": suite_name, "user_task": ut,
                                            "injection_tasks_true_without_attack": fired})
            if c["clean_runs"]:
                rows.append({"pipeline": pipeline, "suite": suite_name, **{k: c[k] for k in (
                    "clean_runs", "faithful", "utility_mismatch", "replay_error", "errored", "pairs", "pairs_fp",
                    "runs_with_fp")}})
    with open(os.path.join(out_dir, "clean_oracle_floor.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    json.dump(fp_examples, open(os.path.join(out_dir, "fp_examples.json"), "w"), indent=1)
    tot = collections.Counter()
    for r in rows:
        for k, v in r.items():
            if isinstance(v, int):
                tot[k] += v
    print(json.dumps(dict(tot)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "v1")
