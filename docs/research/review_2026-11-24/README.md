# 24 Nov 2026 research pass (Turkish)

Partial outputs of six research agents (stopped by a usage limit; A, E1, E3 incomplete). Integrated into the Claude Doc "Tez Araştırması — Açıklamalı Türkçe Rehber" (sections 3.4, 12.6, 15, 16 and the "Sunum hazırlığı" tab).

- A: slide Q&A (slides 1–14)
- B: VehicleWorld vs CAR-bench
- C: JEV good/bad, P/R/F1
- D: Langfuse (+ episode_tracing.py sketch, tested only against a mock endpoint)
- E1: attack numbers + AgentPoison deep dive (partial)
- E3: defences (partial)

## Corrections still to carry into lit notes (from E1/E2)
- A-24 MCPTox 72.8% = mean of 9 cells incl. strengthened prompts; base setting ≈63.5%; denominator = valid outputs.
- A-30 parameter poisoning: result is in Sec. 4.2 / Table 1 (not Sec. 5).
- A-09 AgentDojo: Table 4 57.7% vs Table 3 47.69% (same condition, different runs).
- A-15 AgentPoison: "<0.1% poison" holds for Agent-Driver/ReAct only (EHRAgent ≈0.28%); ">80%" is retrieval.
- E-01 ASB: 73.58 is the delimiters-defended row; undefended 67.50; Llama-3.3-70B 62.58 → 52.92.
- D-30 MELON PI2: 78.6 (Llama-3.3) / 58.9 (Qwen3); 42.1 / 20.7 are 5-attack averages.
