# 09 · What does "JEV models" mean?

Ömer's brief: *"She asked me to research 'JEV models'. [ÖMER: confirm what this means.]"*

## Most likely meaning (high confidence, not certain)
**JEV is a "decision model" released by TypeSafe AI on 15 September 2026.** It does not generate text. Given a state (text) and typed questions, it returns a probability for each allowed answer in one forward pass. Question types are Noul (yes/no), Choice (one of up to 255 options) and Score (ordinal level). The company calls the class "System One" models. Its slogan: "Jev makes judgments, code makes decisions." Sources: TypeSafe docs and blog (T4, vendor), see `../../Sunum Bilgi Paketi - Saldırılar, Değerlendirme, Savunmalar + JEV (TR-EN).md` §5–6 for quotes checked on 16 Nov 2026.

Why this is most likely:
1. "JEV models" matches TypeSafe's own wording ("decision models", "System One models") and the product name.
2. The timing fits: the model appeared two months before the internship, and several evaluations followed in Sep–Nov 2026.
3. Ömer presented "Agent Security and JEV" to the supervisor this week on this interpretation. If she meant something else, she should have flagged it there — **confirm explicitly** (question 1 in `07_supervisor_questions.md`).

## What is established about JEV as a judge or guard (tiers)
| Claim | Source | Tier | Status |
|---|---|---|---|
| Close to frontier LLM judges where the verdict is visible in the text (RewardBench 92.5 vs 92.5 GPT-6), far behind on JudgeBench (78.6 vs 93.1) | JEV-as-a-Judge, CMU, arXiv 2609.26550 Table 1 | T3 | verified 16 Nov (presentation) |
| A JEV→GPT-6 cascade at confidence threshold 0.9 gains +0.93 points at 41.4% of cost | same, Table 4 | T3 | verified 16 Nov |
| LLM judges repeat 96% of JEV's most confident errors; cascade gains are bounded | Rao & Callison-Burch (UPenn), arXiv 2609.29769 | T3 | verified 16 Nov |
| On 5,219 agent trajectories, JEV positive-class F1 77.8 vs 74.1 for the best generative judge (GLM-5.2); JEV leads on ATBench500 and MCPHunt, GLM on R-Judge and TraceSafe | arXiv 2609.34862 (abstract) | T3 | abstract read 18 Nov |
| A counterfeit policy embedded in the input redefines labels and drops JEV's attack-detection F1 from 90.51% to 7.46% | Datadog Security Labs | T4 (vendor blog) | verified 16 Nov |
| Architecture, weights and training details are unpublished; open reproductions (Kev, Perplexity Decider) use a backbone + per-option scoring head | TypeSafe docs; Hume blog; HF model cards | T4 | verified 16 Nov |

**Correction to earlier material:** the presentation originally said JEV was "not tested on agents yet"; arXiv 2609.34862 tested it on agent traces (fixed on slides 9 and 30 on 18 Nov).

## Alternative readings to rule out (lower confidence)
| Possibility | Why it could be meant | How to tell |
|---|---|---|
| G-Eval (LLM-as-judge with chain-of-thought and form-filling; Liu et al., EMNLP 2023) | "G-Eval" spoken quickly in German ("Geh-Eval") can sound like "JEV"; it is a classic judge method relevant to "build your own metrics" | Ask: "Did you mean the TypeSafe model or G-Eval-style LLM judges?" |
| JEPA (Joint-Embedding Predictive Architecture, LeCun et al.; e.g. I-JEPA, V-JEPA) | the only other "JE…" model family the literature agent found; pronounced close to "JEV"/"JEPA models" | Ask; it would point to world-model / self-supervised vision research, far from agent security, so unlikely in this context |
| Generic "judge/evaluation models" | Supervisor may have used "JEV" loosely for judge models | Same question |
| An internal VW name | Cannot be checked from public sources | Ask; do not search internal systems from outside |

## How JEV should and should not enter the thesis
- **Should:** as one candidate judge in E2 (judge validation against human labels) and one candidate guard in D2 — a sub-question (RQ1a), time-boxed to ≤ 2 weeks.
- **Should:** run the main judge/guard experiments with an open decision model or open LLM as well, because the hosted model may change version and data would leave the company (supervisor question on approval).
- **Should not:** be the final scorer of attack success where a state oracle exists, and should not be trusted on cases that need multi-step reasoning without validation.
- **Should:** be attacked too — the counterfeit-policy result shows the measuring instrument is itself an attack surface ("who measures the measurer?").
