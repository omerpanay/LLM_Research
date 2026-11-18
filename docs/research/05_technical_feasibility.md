# 05 · Technical feasibility

Everything here was checked in this environment on 18 Nov 2026 unless marked *estimate*. Detailed code-level notes: `lit/codebase_audit.md`.

## 1. Codebases to build on
| Codebase | Licence | Role in thesis | Verified here | Extension points |
|---|---|---|---|---|
| AgentDojo (`ethz-spylab/agentdojo`) | MIT | **Integration hub**: suite format, state oracles, built-in attacks/defences | Installed in a venv; `check_suites -s banking --no-check-injectable` passes for 16 user + 9 injection tasks **without any LLM** (the injectability check fails in this setup; to investigate) | `default_suites/v1/<suite>/{task_suite,user_tasks,injection_tasks}.py`, `data/suites/<suite>/{environment,injection_vectors}.yaml`; `BaseInjectionTask.security()` (`base_tasks.py` l. 97–125) |
| CAR-bench (`CAR-bench/car-bench`) | MIT | Source of the in-car domain (tools, JSONL data, tasks, policies) and published trajectories | Cloned; trajectories re-analysed for free (`results/carbench_noise_floor/`) | `car_bench/envs/base.py` (step loop, state hashes), `envs/car_voice_assistant/tools/*/set_apis`, `mock_data/data_manager.py`, `policy_evaluator.py` |
| AgentLAB (`TanqiuJiang/AgentLAB`) | MIT | Attack families and planner/attacker/judge prompts; stored task-injection results | Cloned; stored results re-analysed (`results/agentlab_ti_budget/`); success criteria audited | Family runners at repo root; `Task-Injection/agentdojo/src/agentdojo/attacks/long_horizon_attack.py`; `prompts/*.md` |
| CaMeL (`google-research/camel-prompt-injection`) | Apache-2.0 | System-level defence baseline; policy engine for the own gate | Cloned; policy files read | `src/camel/pipeline_elements/security_policies/<suite>.py` (100–270 lines per suite), `capabilities/`, `interpreter/` |
| carlab_mini (this repo) | — | Free prototype of the measurement pipeline | 14 tests pass; full matrix runs in < 1 min on CPU | `code/carlab_mini/` |

**Recommended architecture.** CarDojo = AgentDojo suite re-implementing ≈20–25 CAR-bench tools on CAR-bench data, plus three additions: driving context + speaker role in the environment, snapshot logging after every state change, and goal-specific injection tasks. This gives AgentDojo defences, CaMeL policies and AgentLAB's long-horizon task injection with no glue code. Size reference: AgentDojo banking ≈ 1,200 lines (tools 178, user tasks 571, injection tasks 418); CaMeL policy set 100–270 lines. *Estimate:* 3–5 weeks for CarDojo v0, 1 week for CaMeL policies.

## 2. What runs where
| Component | Free here (CPU, 4 cores, 15 GB, no GPU) | Needs VW resources |
|---|---|---|
| carlab_mini, metrics, validity filter, statistics | yes | — |
| AgentDojo / CarDojo with ground-truth pipeline (no LLM) | yes | — |
| Re-analysis of stored AgentLAB / CAR-bench results | yes | — |
| Victim agent = open model (e.g. Qwen3-30B-A3B, Llama-3.1-8B, Qwen3-32B) | no (too slow on CPU) | GPU with vLLM. *Estimate:* an 8B model in bf16 needs ~16 GB VRAM plus KV cache; 30B-class models need ~60+ GB in bf16 or ~20 GB quantised |
| AgentLAB attacker (Qwen3-14B abliterated, per README) | no | GPU (*estimate* ~30 GB bf16) + policy approval |
| Victim = API model (GPT/Claude/Gemini) | no (paid) | API budget + data-transfer approval |
| LLM judge / LLM user simulator | no (paid or GPU) | as above |

## 3. Cost model (no money has been spent)
Measured inputs (from CAR-bench's published logs, `info.total_agent_cost` and `info.user_cost`, clean episodes, prices at the authors' run time):

| Agent model in CAR-bench logs | Mean agent cost per clean episode | Median prompt tokens (last call) | Median LLM latency per episode |
|---|---|---|---|
| Claude Sonnet 4.6 | $0.087–0.118 | ≈14.5k | ≈18 s |
| Claude Opus 4.6 (thinking, medium) | $0.138–0.171 | ≈14.4k | ≈17–25 s |
| GPT-5.2 (thinking, medium) | $0.048–0.067 | ≈9.3k | ≈22–29 s |
| Gemini 2.5 Flash as user simulator | ≈$0.0007–0.0014 | — | — |
| Open models (Qwen3-32B, gpt-oss-120b, xLAM-2-32b) | $0 recorded (self-hosted) | 8–14k | 6–340 s (hardware-dependent) |

Formula (*estimate*): $C = N_{ep} \cdot (c_{agent}\, m + c_{user} + c_{att} + c_{judge})$, where $m$ is the episode-length multiplier for attacked runs (multi-turn attacks; *assume* 1.5–3×), $c_{att}$ the attacker LLM per episode and $c_{judge}$ the judge.

Worked example for E3 (*estimate*, to be replaced by a week-1 measurement): 6,480 attacked + 6,480 clean episodes. If one third run on an API model at $0.05–0.17 per clean episode and attacked episodes cost 2× → API agent cost ≈ 2,160 × $0.05–0.17 + 2,160 × 2 × $0.05–0.17 ≈ **$320–1,100**; the open-model two thirds cost GPU time only. Judges/attackers on open models add GPU time; on APIs they add a comparable amount again. **No paid call will be made without your explicit OK and a measured per-episode cost.**

Cheapest credible configuration: open-model victim + open attacker + state oracles (no LLM judge needed for final scoring) on one VW GPU; one API model only for a 300-pair external check.

## 4. Engineering risks
| Risk | Evidence | Mitigation |
|---|---|---|
| AgentDojo injectability check fails in a fresh venv | observed here | investigate before CarDojo (probably data-path/canary handling); not blocking ground-truth checks |
| AgentLAB runners need conda envs, vLLM, GPT-5.1 for planner/judge | README | use only the task-injection path (AgentDojo-based) first; replace GPT-5.1 judge with state oracles where possible |
| CAR-bench needs an LLM user simulator in every run | code + logs | scripted user turns for attack families; LLM user only for external validity |
| Python 3.13 here vs repos targeting 3.10–3.11 | READMEs | pin a 3.11 environment at VW |
| Model drift (API versions) | general | pin model IDs and dates; keep one open model as the reproducible anchor |
