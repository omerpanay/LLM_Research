# 07 · The 10 most important questions for the supervisor this week

Ordered by how much the answer changes the plan. Each has a default I will follow if there is no answer by Friday 27 Nov.

| # | Question (ready to ask) | Why it matters | Default if no answer |
|---|---|---|---|
| 1 | "When you asked me to research JEV models, did you mean TypeSafe AI's decision model JEV, or LLM-as-judge methods in general (e.g. G-Eval)? Was this week's presentation what you had in mind?" | Decides whether RQ1a exists | Treat as TypeSafe JEV, time-boxed sub-question (`09`) |
| 2 | "May I centre the thesis on measurement validity — showing which measured attack successes are real — and use it to answer the attack and defence questions? Concretely RQ1–RQ3 in `03_thesis_design.md`." | Reframes the thesis around directive 2 | Proceed with the validity-first design |
| 3 | "AgentLAB's public code scores intent hijacking as harmful text with an LLM judge the attacker also optimises against, and its task-injection ASRs are best-of-up-to-10-attempts. Is it OK if part of my contribution is an audit of AgentLAB's measurement, and may I contact the authors?" | Turns directive 4 ("AgentLAB is important") into a concrete, citable contribution | Contact authors politely with the questions in `lit/codebase_audit.md` |
| 4 | "Which compute can I use: a GPU for open models (vLLM), and/or an API budget? Is sending synthetic benchmark data to an external API allowed?" | Decides model choices and experiment size | Plan for open models on GPU; API only for a small subset |
| 5 | "AgentLAB's attacker is an 'abliterated' open model with safety training removed. Is using such a model allowed at VW? If not, which attacker model is approved?" | Policy/ethics; affects attack strength | Use an approved instruction model with a red-team prompt |
| 6 | "Is building an AgentDojo-format in-car suite from CAR-bench (both MIT) acceptable, and do I need approval for third-party open-source code?" | Engineering path (`05`) | Proceed with CarDojo |
| 7 | "Which agent architectures matter most for the team's work — ReAct-style tool calling, plan-then-execute, CaMeL-style dual LLM, multi-agent?" | Fixes the architecture axis | ReAct, plan-then-execute, CaMeL-style |
| 8 | "Does the team use an ISO/SAE 21434 TARA template or impact scale I could use for severity weights (without any internal data)?" | Severity-weighted ASR and threat model language | Use the public 4×4 impact scheme |
| 9 | "Which peer-reviewed venues count for the final citations, and how should I treat important arXiv-only work (e.g. The Attacker Moves Second, CaMeL)?" | Directive 5 | Cite T3 as motivation only; core claims on T1/T2 + own measurements |
| 10 | "Can parts be published (e.g. a workshop paper on the measurement audit), and what company review does the thesis need before submission?" | Timeline (W36) and possible paper | Plan a review window in W36; no external posting before approval |
