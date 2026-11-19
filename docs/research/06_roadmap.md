# 06 · Roadmap to 31 July 2027

Internship: 9 Nov 2026 – 30 Jul 2027 per the internship plan (the brief says 31 Jul; Friday 30 Jul 2027 is the last working day, so both dates give the same plan). 38 working weeks, 35 h/week. Holidays assumed (Lower Saxony, computed): 24–26 Dec, 31 Dec–1 Jan, Good Friday 26 Mar, Easter Monday 29 Mar, 1 May (Saturday), Ascension 6 May, Whit Monday 17 May. Personal leave is not yet planned — subtract it from buffer weeks.

**Rule:** every phase ends with a *gate* (a concrete artefact). If the gate is missed, use the fallback in §4 instead of slipping the whole plan.

## 1. Phases
| Phase | Weeks | Dates | Goal | Gate |
|---|---|---|---|---|
| P0 Orientation & plan | W1–W4 | 9 Nov – 4 Dec | Plan agreed; measurement audit (E0) done | 2-page thesis plan signed off |
| P1 Infrastructure | W5–W12 | 7 Dec – 29 Jan | CarDojo v0; AgentDojo + AgentLAB task injection reproduced (E1); labelling protocol | First end-to-end attacked + clean run on CarDojo with state oracle |
| P2 Attack | W13–W20 | 1 Feb – 26 Mar | 6 families × 3 architectures × 2 models; budget curves (E3) | Dataset v1 + interim presentation |
| P3 Evaluate | W21–W25 | 29 Mar – 30 Apr | Validity filter on E3; judge validation with human labels (E2); metrics frozen | Measurement chapter draft + frozen metric code |
| P4 Defend | W26–W31 | 3 May – 11 Jun | D0–D5, adaptive attacker (E4); external validity on CAR-bench (E5) | Defence results table |
| P5 Write & submit | W32–W38 | 14 Jun – 30 Jul | Full draft 2 Jul; review; final talk | Submission |

## 2. Week by week
| Wk | Dates | Main work | Deliverable / milestone |
|---|---|---|---|
| W1 | 9–13 Nov | Onboarding; first reading | — |
| W2 | 16–20 Nov | Literature presentation to supervisor; **research pass in this repo** (state of field, audits, prototype) | `docs/research/` + presentation |
| W3 | 23–27 Nov | Ask the 10 questions (`07`); read AgentLAB/CAR-bench/AgentDojo code paths named in the audit; run `carlab_mini` and the two free analyses yourself | Answers logged; decision on JEV scope |
| W4 | 30 Nov–4 Dec | Write the 2-page plan from `03_thesis_design.md`; request compute/API access and attacker-model approval | **Gate P0:** plan signed off |
| W5 | 7–11 Dec | Set up VW-approved environment (Python, AgentDojo, vLLM or API); run AgentDojo banking with 1 model (E1a) | first reproduced numbers |
| W6 | 14–18 Dec | Run AgentLAB long-horizon task injection on 1 model; reproduce the budget curve (E1b); email AgentLAB authors with the audit questions | budget-curve reproduction |
| W7 | 21–23 Dec | (short week) CarDojo design doc: tools, data, injection vectors, invariants, oracles | design doc |
| W8 | 28–30 Dec | (holiday week) buffer / reading: CaMeL code, Design Patterns paper | — |
| W9 | 4–8 Jan | CarDojo: tools + environment.yaml from CAR-bench data; snapshot logging | 10 tools running |
| W10 | 11–15 Jan | CarDojo: 15 user tasks with utility checks; driving context, speaker role | `check_suites` passes |
| W11 | 18–22 Jan | CarDojo: 8 injection tasks with goal-specific oracles; injection vectors | first attacked run |
| W12 | 25–29 Jan | Clean baseline K = 3 on 2 models; noise floor on CarDojo; labelling protocol for E2 | **Gate P1:** end-to-end attacked + clean run |
| W13 | 1–5 Feb | Task injection one-shot vs long-horizon at matched budget (H2) | budget-matched table |
| W14 | 8–12 Feb | Instruction-free tampering + transient manipulation families | 2 families running |
| W15 | 15–19 Feb | Tool chaining / intent hijacking with passenger role, scored on executed actions | 2 families running |
| W16 | 22–26 Feb | Cross-session memory poisoning harness | 6 families done |
| W17 | 1–5 Mar | Architectures: plan-then-execute and dual-LLM/CaMeL-style agent | 3 architectures |
| W18 | 8–12 Mar | E3 main runs (model 1) | raw results |
| W19 | 15–19 Mar | E3 main runs (model 2); turn and attempt budget curves | raw results |
| W20 | 22–25 Mar | Interim presentation; dataset v1 with data card | **Gate P2:** dataset v1 + talk |
| W21 | 30 Mar–2 Apr | (short week) Apply validity filter to E3; label distribution per family | validity tables |
| W22 | 5–9 Apr | E2: label 200 traces (2 annotators on 50 for agreement) | gold set |
| W23 | 12–16 Apr | E2: LLM judges + decision model (JEV/open) vs gold; Rogan–Gladen; RQ1a | judge card |
| W24 | 19–23 Apr | Freeze metrics; statistical analysis (mixed-effects, Holm); answer RQ1/RQ2 | frozen metric code |
| W25 | 26–30 Apr | Write measurement chapter + attack chapter drafts | **Gate P3:** 2 chapter drafts |
| W26 | 3–7 May | D1/D2 (prompt, detector incl. decision-model guard) | static defence results |
| W27 | 10–14 May | D4 provenance + vehicle-state gate (own) | gate implemented |
| W28 | 18–21 May | (short week) D5 trajectory monitor; D4+D5 | all defences |
| W29 | 24–28 May | Adaptive attacker per defence, B ∈ {1,5,20} (E4) | adaptive results |
| W30 | 31 May–4 Jun | Driver-interaction cost, latency; external validity on CAR-bench (E5) | E5 numbers |
| W31 | 7–11 Jun | Defence chapter draft; freeze experiments | **Gate P4:** defence table |
| W32 | 14–18 Jun | Write intro, background, related work (reuse `docs/research/01`, `lit/`) | chapters 1–3 |
| W33 | 21–25 Jun | Threat model + discussion + limitations | chapters 4, 9 |
| W34 | 28 Jun–2 Jul | Full draft complete (**2 Jul**) → supervisor + university advisor | full draft |
| W35 | 5–9 Jul | Revisions; reproducibility pass (one command per table) | v2 |
| W36 | 12–16 Jul | Company review (confidentiality), figures, abstract; optional workshop paper | v3 |
| W37 | 19–23 Jul | Final talk; team handover note (1 page + defence recommendations) | talk |
| W38 | 26–30 Jul | Buffer; submission; archive code/data | **Submission** |

## 3. Weekly rhythm
Monday: 3 goals for the week. Friday: log (done / blocked / next) to supervisor. Every second week: 1-hour literature refresh (new arXiv/OpenReview work citing AgentLAB, CAR-bench, CaMeL) and re-check the gaps in `02_gaps_ranked.md`.

## 4. Risks, early signals, fallbacks
| Risk | Early signal | Mitigation | Fallback scope |
|---|---|---|---|
| No GPU / API approval | No access by W6 | Start approval in W4; use AgentDojo with API model on a small subset; continue design work | **Scope A:** measurement study on AgentLAB + AgentDojo artefacts and stored results only (RQ1), small CarDojo demo |
| Attacker model (abliterated) not allowed | Supervisor says no in W3 | Use an approved instruction-tuned model with a red-teaming system prompt; report the difference | same plan, weaker attacker noted as limitation |
| CarDojo takes longer than 4 weeks | `check_suites` not passing by W11 | Cut to 12 tools / 10 tasks / 6 injection tasks | **Scope B (default):** CarDojo small + 4 families + 2 architectures |
| Costs higher than estimated | Week-1 measurement > 2× estimate | Reduce K to 2 for exploratory cells; run main cells only on open model | fewer cells, same RQs |
| LLM user simulator drift | > 10% of clean runs flagged for drift | Scripted user turns for attack families; LLM user only in E5 | — |
| Field moves (a CarDojo-like paper appears) | biweekly refresh finds it | Position as replication + measurement audit; contributions 1, 2, 5 stay new | — |
| Writing late | no chapter draft by W25 | write related work in W32 from `lit/` files | — |
| Ahead of plan in April | gates P2/P3 early | **Scope C:** multi-agent cockpit↔service hand-off (multi-CaMeL finding) or open-model hidden-state probes as guard | workshop paper |

## 5. Milestone summary
- 4 Dec 2026: plan signed off.
- 29 Jan 2027: first attacked + clean CarDojo run.
- 26 Mar 2027: dataset v1, interim talk.
- 30 Apr 2027: metrics frozen; measurement chapter.
- 11 Jun 2027: defence results.
- 2 Jul 2027: full draft.
- 30 Jul 2027: submission.
