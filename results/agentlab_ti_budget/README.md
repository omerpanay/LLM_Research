# AgentLAB task injection: how much of the ASR is attacker retries?

**Data.** AgentLAB's public repository (`github.com/TanqiuJiang/AgentLAB`, commit `36f58e6`, 31 May 2026, MIT) ships per-attempt results of its long-horizon task-injection attack under `Task-Injection/agentdojo/res/long_horizon/`. The attack runs on AgentDojo, whose `security` check reads the **environment state** (an oracle, not an LLM judge). Each line of `results.jsonl` is one attempt (an injection snippet iteration/variant) for one user_task × injection_task pair, with `security_passed` (attacker goal reached in the environment) and `utility_passed`.

**Script.** `python3 -I tools/agentlab_ti_attempts.py third_party/AgentLAB/Task-Injection/agentdojo/res/long_horizon results/agentlab_ti_budget` → `ti_attempt_budget.csv`.

A pair counts as compromised within budget *b* if any of its first *b* stored attempts succeeded (attempts taken in stored order).

## Result (banking suite, 144 pairs, as stored in the repo)
| Model folder | attempts per pair (median / max) | ASR at 1 attempt | ASR at 3 | ASR at 5 | ASR, any attempt | AgentLAB paper value |
|---|---|---|---|---|---|---|
| gpt-4o | 3 / 10 | 32.6% | 59.0% | 70.1% | **79.9%** | 79.9% (Tables 2–3, long-horizon) |
| meta-llama_Llama-3.3-70B-Instruct | 1 / 15 | **50.7%** | 75.0% | 81.9% | **86.8%** | 86.8% long-horizon; 50.7% one-shot (Table 3) |
| Qwen3-235B-A22B | 1 / 10 | 72.2% | 85.4% | 90.3% | **93.1%** | 93.1% (Table 3) |
| gpt-5.1 | 12 / 13 | 0.7% | 6.9% | 9.7% | 22.9% | 21.5% (Table 2) |
| gpt-5.1 + repeat_user_prompt | 10 / 12 | 1.4% | 6.2% | 12.5% | **20.8%** | 20.8% (Table 4, RP) |
| gpt-5.1 + transformers_pi_detector | 10 / 10 | 0.0% | 0.0% | 0.7% | **2.8%** | 2.8% (Table 4, DD) |
| claude-sonnet-4-5 | 12 / 17 | 0.0% | 0.0% | 0.0% | **0.0%** | 0.0% (Table 2) |

Bold any-attempt values match the paper's reported numbers exactly; the GPT-5.1 any-attempt value (22.9%) is close to, but not identical with, the paper's 21.5%. The gpt-4o `summary_results.txt` also states that 111 of the 115 successful pairs were carried over ("skipped") from previous runs, so the final number aggregates several runs.

## What it shows (observation vs. inference)
- **Observation:** the published long-horizon task-injection ASRs are **any-success-within-N-attempts** rates, with N up to 10–17 attempts per pair, aggregated across runs.
- **Observation:** at a budget of one attempt, GPT-4o's long-horizon ASR in these files is 32.6%, below the paper's one-shot baseline for GPT-4o (62.5%, Table 3). It passes 62.5% only between 3 and 5 attempts.
- **Observation:** for Llama-3.3-70B, the paper's "one-shot" value (50.7%) equals the long-horizon attack's first-attempt ASR in these files, which suggests (Inference) that the paper's one-shot vs long-horizon comparison is a 1-attempt vs N-attempt comparison for that model.
- **Inference:** part of the "long-horizon attacks are stronger" effect may be an **attack-budget** effect. Budget-matched comparison (same number of attempts, or same number of victim queries) is needed before attributing the gain to multi-step structure. This is a direct instance of the supervisor's "is this really an attack?" question, and it is measurable for free from the authors' own files.
- **Not a criticism of the oracle:** success here is read from environment state, which is the most reliable kind of measurement. The issue is how attempts are aggregated, not how a single attempt is judged.

## Caveats
- Stored order is assumed to be chronological (snippet `iter_i_vj`). Pairs carried over from earlier runs may have their history truncated; the curve is therefore a lower bound on early-budget ASR only if earlier attempts are missing. Confirm with the authors.
- Folders `gpt-4o-backip`, `gpt-4o-backup-0120`, and suite-named folders (`banking`, `slack`, `travel`, `workspace`) are other runs/backups whose model is not stated; they are listed in the CSV but not interpreted.
- One-shot baseline numbers are from the paper (Table 3), not from these files.
