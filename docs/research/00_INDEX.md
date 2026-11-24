# 00 · Index and executive summary

Research pass for Ömer's thesis *Robustness of agentic AI to adversarial attacks — long-horizon, in-vehicle agents, across agent architectures* (VW AG, Digital Architecture Concepts, Nov 2026 – Jul 2027). Produced 18–19 Nov 2026. Everything is in English; the summary to Ömer is in Turkish (chat).

## Executive summary (one page)
**The field.** Attacks on tool-using LLM agents are easy and well replicated; defences that ask a model to resist break under adaptive attack; deterministic system-level defences hold on today's benchmarks but cost a lot of utility and have never faced strong adaptive long-horizon attackers. The weakest link is **measurement**: harness artifacts, invalid test cases, judge errors, retries and ordinary agent failure distort reported attack success. No benchmark combines in-car tools, a multi-turn attacker, vehicle state and state-based oracles. (`01_state_of_the_field.md`)

**What we measured ourselves, at zero cost.**
- AgentLAB's task-injection ASRs are success within up to 10–17 attempts: GPT-4o 32.6% at one attempt vs 79.9% reported (`results/agentlab_ti_budget/`).
- AgentLAB's public intent-hijacking code is tool-less and scored by a text judge the attacker optimises against (`lit/codebase_audit.md`).
- CAR-bench clean runs: 12–34% of tasks flip between identical trials; unrequested state changes in up to ~20% of runs, zero unrequested e-mails/calls (`results/carbench_noise_floor/`).
- AgentDojo clean-run replay: attack oracles fire without attack in 13/17,547 pairs, all one goal-collision artifact fixed in v1.1.1 (`results/agentdojo_clean_oracle_floor/`).
- A free prototype (`code/carlab_mini`, 14 tests) shows each proposed metric catching what it should: forced-tool artifacts, claimed-but-not-executed, transient unsafe states, clean-run coincidences, and that a naive provenance gate over-blocks (`results/prototype/`).

**Recommended thesis.** Validity-first measurement (causal/placebo ASR, verified ASR, judge-corrected ASR, budget curves, Kaplan–Meier turns-to-compromise, transient unsafe actions, severity weighting, driver-interaction cost) applied to **CarDojo**, an AgentDojo-format in-car suite built from CAR-bench data; attacks from AgentLAB's families plus instruction-free tampering, cross-session memory and transient manipulation; defences up to a vehicle-state-aware decision-provenance gate under adaptive attack. (`02_gaps_ranked.md`, `03_thesis_design.md`)

**Feasible?** Yes, with one VW GPU or a small API budget; all four codebases are MIT/Apache-2.0; AgentDojo runs LLM-free on CPU here; cost model from real CAR-bench logs ($0.05–0.17 per frontier clean episode). (`05_technical_feasibility.md`)

**Next steps.** Ask the 10 questions (`07`), confirm what "JEV" means (`09`), sign off the plan by 4 Dec (`06`).

## Files
| File | Content |
|---|---|
| `01_state_of_the_field.md` | solved / open / overhyped per stage; where the framing needs updating |
| `02_gaps_ranked.md` | 5 gaps scored novelty × feasibility × VW fit |
| `03_thesis_design.md` | RQs, hypotheses, threat model summary, CarDojo, attacks, **formal metrics**, validity filter, defences, experiments, statistics |
| `04_automotive_threat_model.md` | assets, attacker profiles, channels → OWASP/ATLAS/R155, vehicle invariants, mini-TARA, standards use |
| `05_technical_feasibility.md` | codebases, extension points, compute split, cost model |
| `06_roadmap.md` | week-by-week to 30 Jul 2027, gates, risks, fallback scopes |
| `07_supervisor_questions.md` | 10 questions with defaults |
| `08_discoveries_and_ideas.md` | 13 discoveries, framing challenges, 11 original ideas with publishability |
| `09_jev_clarification.md` | what "JEV models" most likely means; evidence; alternatives |
| `lit/attacks.md` · `lit/evaluation.md` · `lit/defenses.md` · `lit/automotive.md` | verified literature notes (≈200 entries; summaries, taxonomies, registry rows) |
| `lit/codebase_audit.md` | AgentLAB / CAR-bench / AgentDojo / CaMeL code audit |
| `sources.csv` · `sources_check.md` | 243-row source registry with tiers; arXiv titles checked live (174 ok, 0 mismatch) |
| `../../code/carlab_mini/` · `../../results/` · `../../tools/` | prototype, measurements, scripts |

## Source quality
- Registry: 243 rows — T1 79, T2 41, T3 104, T4 18, 1 untiered (title-only); verification: 107 primary-read, 103 abstract-only, 33 unverified (`tools/build_registry.py`).
- `tools/verify_sources.py`: every arXiv-backed URL resolves to a matching title (174/174).
- Standards texts (UNECE, ISO, EUR-Lex) and most OEM sites were blocked from this environment; those rows are snippet-based and marked UNVERIFIED — obtain official texts before citing.

## 10-claim audit (main session re-checked literature-agent claims against primary sources, 19 Nov 2026)
| # | Claim | Checked against | Result |
|---|---|---|---|
| 1 | The Attacker Moves Second was rejected at ICLR 2026 (update 24 Nov: later accepted at USENIX Security 2026, usenix.org checked) | OpenReview API venueid `ICLR.cc/2026/Conference/Rejected_Submission` | ✔ |
| 2 | STAC appears at the REALM workshop | ACL Anthology page 2026.realm-1.17 | ✔ |
| 3 | AgentPoison ">80%" is retrieval; end-to-end lower | PDF abstract ("82% retrieval … 63% end-to-end") + Table 1 (Agent-Driver ASR-r 80.0, ASR-t 56.8) | ✔ (also exposes slide 7 error) |
| 4 | ROPE Table 3: Progent 8.7/8.3/15.1, up to 43.5; DRIFT up to 25.4 | ROPE PDF Table 3 + §4.4 text | ✔ |
| 5 | AutoDojo: CaMeL clean utility 26.3 / 40.4 | AutoDojo PDF tables | ✔ |
| 6 | AlignmentCheck precision 0.096 at 2% attack rate | Detectors-of-Hijacked-Agents abstract | ✔ |
| 7 | Rogan–Gladen judge paper is ICML 2026 | PDF footer "Proceedings of the 43rd International Conference on Machine Learning" | ✔ |
| 8 | "Mistral vulnerable on all 64 tasks, only 26 valid" | task-contracts PDF abstract | ✔ |
| 9 | PIGuard = InjecGuard (renamed) | arXiv 2410.22770 title + ACL 2025 title | ✔ |
| 10 | arXiv ids in registry match titles | `sources_check.md` (174/174) | ✔ |

## Reproduce the free analyses
```bash
git clone --depth 1 https://github.com/TanqiuJiang/AgentLAB third_party/AgentLAB
git clone --depth 1 https://github.com/CAR-bench/car-bench third_party/car-bench
git clone --depth 1 https://github.com/ethz-spylab/agentdojo third_party/agentdojo
python3 -I tools/agentlab_ti_attempts.py third_party/AgentLAB/Task-Injection/agentdojo/res/long_horizon results/agentlab_ti_budget
python3 -I tools/carbench_noise_floor.py third_party/car-bench/results results/carbench_noise_floor
pip install -e third_party/agentdojo && python tools/agentdojo_clean_oracle_floor.py third_party/agentdojo/runs results/agentdojo_clean_oracle_floor v1
PYTHONPATH=code python3 -m pytest -q -p no:cacheprovider code/carlab_mini && PYTHONPATH=code python3 -m carlab_mini.run results/prototype
python3 -I tools/build_registry.py && python3 -I tools/verify_sources.py docs/research/sources.csv
```
