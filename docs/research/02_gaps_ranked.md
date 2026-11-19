# 02 · The strongest gaps the thesis can fill (ranked)

Scoring: Novelty (N), Feasibility within 8 months on VW resources (F), Fit with VW's automotive focus (V), each 1–5; score = N × F × V (max 125). "Closest work" = newest work found that narrows the gap (checked 18–19 Nov 2026). Every gap must be re-searched every two weeks (`06_roadmap.md`).

| Rank | Gap | N | F | V | Score | Closest existing work (why it does not close the gap) |
|---|---|---|---|---|---|---|
| **1** | **Long-horizon attacks on an in-vehicle agent with state/snapshot oracles** (CarDojo) — incl. instruction-free POI tampering, cross-session memory, transient unsafe states, passenger authority | 5 | 4 | 5 | **100** | CAR-bench (no attacker, V-01); From Intent to Action (single-turn, V-02); AgentLAB (no vehicle, A-01); Gemini calendar attacks (phone/web, V-08). Highest score but depends on CarDojo engineering (P1 gate). |
| **2** | **Validity-first measurement of agent attacks** — a protocol (paired/placebo controls, task contracts, budget matching, judge correction, snapshot oracles) plus an audit showing how much of published long-horizon ASR survives it | 4 | 5 | 4 | **80** | ASB re-analysis (E-01, one benchmark, one artifact); executable task contracts (E-45, perturbation tasks); Rogan–Gladen for judges (E-25, ICML 2026, chatbot judgments); Coin Flip (E-16, jailbreak judges). None audits AgentLAB, none combines these controls for multi-turn agent attacks. Own measurements already show the effect (`results/`). |
| **3** | **Budget-matched comparison of one-shot vs long-horizon attacks** (attempts, turns, queries) and session semantics (fresh vs persistent) | 4 | 5 | 3 | **60** | Adaptive Adversaries (A-05: fresh-session defender, 15 rounds); AgentLAB (A-01: turn curves, but N-attempt aggregation). Can be done partly for free from AgentLAB's stored results; full version needs runs. |
| **4** | **Vehicle-state-aware provenance gate under adaptive + long-horizon attack, priced in driver interaction** | 4 | 3 | 5 | **60** | CaMeL/ROPE/Progent (no vehicle state; no strong adaptive long-horizon test, D-01/D-09/D-19); AgentSpec AV rules (D-24, no attacks); SPIDES approvals with ideal approver (D-07). Novel combination: vehicle state + decision provenance + confirmation budget. |
| **5** | **Judge and guard reliability on long agent traces — including decision models (JEV)** and attacks on the judge itself | 3 | 5 | 3 | **45** | JEV trace study (E-40: retrospective classification, not inside an attacked loop); Datadog counterfeit policy (E-41, vendor); R-Judge/AgentAuditor (short traces). Small, well-bounded sub-question (RQ1a). |

## Recommendation
Build the thesis on **ranks 1 + 2** as the core (the validity-first measurement protocol applied to a new in-car long-horizon attack suite), with **rank 4** (vehicle-state-aware gate) as the Defense chapter and **ranks 3 and 5** (budget matching; judge/JEV reliability) as bounded sub-questions inside the Evaluate chapter. This is robust to the main risk: if CarDojo slips (rank 1), the measurement protocol (rank 2) and budget matching (rank 3) still deliver a publishable measurement study on existing artefacts (Scope A in `06_roadmap.md`). Ties are ordered by feasibility.

## Gaps considered and deprioritised
| Gap | Why not (now) |
|---|---|
| Physical/acoustic injection into in-car agents | out of scope (no real vehicles); simulation would be unconvincing (V-07, A-48 are hardware results) |
| Cockpit → driving agent cascades (VW CEA 2.0) | highly relevant for VW but needs a credible two-domain testbed; Scope C extension |
| Model-level training defences (SecAlign-style) | requires GPU training budget; repeatedly broken adaptively (D-39–D-42) |
| New jailbreak techniques | crowded; not agent-specific |
| Hidden-state probes as guards (D-34) | open models only; good optional extension if GPUs are available |
