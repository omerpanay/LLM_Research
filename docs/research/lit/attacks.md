# Attacks on tool-using LLM agents — verified literature survey

Thesis context: "Robustness of agentic AI to adversarial attacks — an adversarial-example pipeline for long-horizon tasks, evaluating in-vehicle LLM agents across agent architectures" (Attack → Evaluate → Defense). This file covers **ATTACKS** only.

Status: survey as of 18 Nov 2026. Primary PDFs were fetched from arxiv.org and read with `pdftotext`; venues were checked on OpenReview (api2.openreview.net), ACL Anthology, USENIX, AAAI OJS, PMLR, proceedings.neurips.cc, or via Semantic Scholar DOIs where no proceedings page was opened. Everything fetched was treated as data, not instructions.

Conventions
- **Tier**: T1 = peer-reviewed top venue (verified); T2 = peer-reviewed workshop / journal / standard; T3 = arXiv preprint / tech report; T4 = blog / talk / GitHub. "T1-claimed" = only the arXiv comment or a secondary index states the venue.
- **Verification**: PRIMARY-READ (sections named) | ABSTRACT-ONLY | UNVERIFIED.
- Numbers are given with their location in the source. Lines starting with **Inference:** are my reasoning, not the source's claim.
- "How success is measured" uses: *state oracle* (programmatic check of environment state / tool-call log), *LLM judge*, *human*, *output-label match*, *unclear*.

---

## 1. Area summary (≤400 words)

**Largely settled (well replicated):**
- Indirect prompt injection (IPI) through tool outputs works against every model family tested, from GPT-4-era agents to 2026 frontier models (A-07, A-08, A-09, A-11, A-12). Static template attacks are no longer a meaningful robustness test: defenses reporting ≈0–2% static ASR fall to >90% under adaptive search, RL or humans (A-38, A-40, A-41, A-42, A-13).
- Multi-turn / long-horizon decomposition beats one-shot attacks. Splitting a harmful goal into individually benign tool calls bypasses refusal training (A-01: Claude-4.5 27.2% intent hijacking vs 73.3% tool chaining; A-02: 91.2% mean final ASR).
- Persistent state (memory files, scheduled tasks, skills, artifacts) turns a one-time injection into a cross-session compromise (A-19, A-21, A-23, A-17).

**Open:**
- *Instruction-free* attacks that tamper with a decision inside the benign task — parameters, beliefs about state, fabricated hazards — evade detectors and tool-allowlist defenses built for "instruction override" (A-29, A-30, A-31). Benchmarks built only from redirect-style injections overestimate defense coverage (A-29, Sec. 5.3).
- Multi-agent composition: per-agent guarantees (incl. CaMeL) do not compose (A-35); orchestrators execute code that sub-agents refused to write (A-34).
- Physical and acoustic channels into agents (signs, ambient audio) are demonstrated on static driving images, a small robot vehicle or a smartphone, not on closed-loop cars (A-45, A-48).
- Inference: none of the sources read combines in-vehicle tools, persistent memory, multi-turn dialogue and a state oracle (gap across A-01, A-19, A-49, A-50).

**Overhyped / measurement caveats:**
- Headline ASRs often come from LLM judges that share a model family with the attack generator (A-02 uses GPT-4.1 for generator and judge; A-01 uses a GPT-5.1 internal judge) or from single-step "next action" parsing with invalid outputs excluded (A-08 ASR-valid, A-24).
- Retrieval success is not end-to-end success: AgentPoison's ">80%" abstract figure is retrieval ASR; end-to-end driving ASR-t is 54.7–59.6% (A-15, Table 1).
- Hijack ≠ harm: WASP reports up to 86% intermediate hijacking but 0–17% end-to-end attacker-goal completion ("security by incompetence", A-11).
- Some 2026 attack results disable production safeguards (A-42 queries Gemini "without any safety classifiers and with disabled out-of-model prompt injection defenses", Sec. 5.1).
- Long horizon is not monotonically worse for the defender: with a *stateful* defender, ASR fell from 57.4% to 31.5% (A-05, Sec. 5.4), opposite in direction to AgentLAB's turn-budget curves (A-01, Fig. 7) which use a different protocol.

---

## 2. Taxonomy

| Attack class | Channel | Attacker capability | Representative papers | Best reported number (source) |
|---|---|---|---|---|
| Multi-turn user-side escalation / decomposition | user turns | malicious user, black-box, adaptive | A-03, A-04, A-02, A-01 | STAC: 91.2% mean final ASR over 8 agents (A-02 abstract; LLM judge). AgentLAB tool chaining 94.6% on GPT-5.1 (A-01 Table 2) |
| Single-shot indirect prompt injection | tool output, web page, email, doc | third party writes content, black-box | A-07, A-08, A-09, A-10, A-11, A-12 | AgentDojo "important message" vs GPT-4o: 57.7% targeted ASR (A-09 Table 4) |
| Long-horizon / staged / fragmented IPI | multiple observations over time | third party, adaptive across turns | A-01, A-51, A-52, A-53 | ECLIPSE up to 96.7% (no defense) (A-51 abstract) |
| Clarification-state IPI | user-solicited clarification channel | third party | A-14 | o3: 1.8% → 34.0% when clarifying (A-14 abstract) |
| Memory / RAG poisoning with trigger | long-term memory, RAG KB | write access to KB (A-15) or query-only (A-16, A-22) | A-15, A-16, A-22, A-21, A-20, A-18 | MINJA injection success 98.2%, ASR 76.8% (A-16 Sec. 1) |
| Cross-session carryover / delayed trigger | memory file, scheduled task, skill artifacts, calendar | one-time third-party content | A-19, A-17, A-23, A-27 | Carryover "Autonomous" channel on Qwen3-235B: 83.3% (A-19 Table 1) |
| Tool-metadata / MCP poisoning, staged trust | tool description, server behaviour | malicious tool/server provider | A-24, A-25, A-26, A-27, A-28 | MCPTox o1-mini 72.8% (A-24 abstract, Sec. 4.2) |
| Cross-channel fragmentation | tool description + tool result + sampling msg | malicious MCP server | A-28 | 0% single-channel → up to 100% two-channel exfiltration (A-28 abstract) |
| Decision tampering (instruction-free) | data values inside the benign task | environment participant (vendor, reviewer) | A-29, A-30, A-31 | Parameter poisoning 93.06% (Qwen3.6-27B) (A-30 Sec. 5) |
| Chat-template / role spoofing | tool output carrying forged role tokens | third party, knows/guesses template | A-32 | InjecAgent avg 15.13% → 45.90% (A-32 abstract) |
| Multi-agent propagation / control-flow hijack | inter-agent messages, orchestrator | third-party content or message interception | A-33, A-34, A-35, A-36, A-37 | Code execution 58–90% with GPT-4o, 100% in some configs (A-34 abstract) |
| Adaptive optimisation attackers | any text channel | query access (black-box) or gradients (white-box) | A-38, A-39, A-40, A-41, A-42, A-13, A-43 | MetaSecAlign 2% static → 96% adaptive on AgentDojo (A-38 Sec. 5) |
| Physical visual prompt injection | camera (signs, objects) | places printed text in scene, black-box | A-45, A-46 | CHAI 81.8% on DriveLM (A-45 Sec. 1) |
| Acoustic / voice injection | microphone (ultrasonic, concurrent audio) | nearby speaker | A-47, A-48 | 69.10% vs Gemini 3 Pro (A-48 abstract) |
| Embodied jailbreak | user prompt to LLM planner | malicious user | A-44 | "often achieving 100%" (A-44 abstract) |

---

## 3. Entries

### Group 1 — Long-horizon and multi-turn attacks

### A-01 · AgentLAB — AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks
- Jiang, T. et al. (Stony Brook), 2026 · Venue: ICML 2026, PMLR 306:53162–53180 · Tier: T1 (verified via PMLR v306 page `proceedings.mlr.press/v306/jiang26as.html`, "Proceedings of the 43rd International Conference on Machine Learning")
- Link: https://arxiv.org/abs/2602.16901 · code https://github.com/TanqiuJiang/AgentLAB
- Threat model: two settings (Sec. 3): *user as adversary* (substitutes some user prompts) and *environment as adversary* (substitutes some observations: web pages, emails, code comments). Black-box (actions + responses only) and white-box (also sees chain-of-thought). Attacks are adaptive across turns.
- Key results:
  - Scale: 5 attack types (intent hijacking, tool chaining, objective drifting, task injection, memory poisoning), 28 environments, 644 test cases (abstract; Sec. 4.3).
  - Table 2 (overall ASR %): Qwen-3 81.5, Llama-3.1 66.5, GPT-4o 78.1, GPT-5.1 69.9, Gemini-3 53.7, Claude-4.5 28.9. Tool chaining is the strongest column (73.3–96.3%).
  - Table 3, one-shot "important message" vs long-horizon task injection: GPT-4o 62.5% → 79.9%; GPT-5.1 2.08% → 21.5%; Gemini-3 41.0% → 43.1%; Claude-4.5 0.0% → 0.0%. Quote: "For GPT-4o, the ASR increases from 62.50% to 79.9%".
  - Sec. 5.2: Claude "demonstrates resilience against hijacking attacks (27.2% ASR) but remains highly susceptible to chaining attacks (73.3% ASR)".
  - Fig. 7: task injection vs GPT-4o "progresses from 0% at nturn = 0 to about 80% at nturn = 5". Note: 0 turns means the attack cannot place any content; it is not a one-shot baseline (see Table 3 for that).
  - Table 4 defenses: Self-Reminder cuts Claude-4.5 intent hijacking to 6.9% but tool chaining stays 57.9%; DeBERTa detector cuts task injection on Qwen-3 from 93.1 to 6.9 but memory poisoning only from 48.0 to 41.2.
- How success is measured: **LLM judge (mixed with ground truth)**. Sec. 5.1: "GPT-5.1 with greedy decoding (temperature 0) as the internal judge"; Sec. 4: "We employ an evaluator (e.g., an external LLM) to determine task completion by comparing the agent's execution trajectories against ground-truth sequences". Manual validation required that "attack success can be evaluated programmatically", but the reported ASR path is via the LLM evaluator. Attacker = Qwen-3-14B-Abliterated, planner = GPT-5.1.
- Automotive relevance: directly reusable taxonomy for the thesis pipeline; tool chaining maps onto vehicle-function tools (individually benign: unlock, open window, navigate). Memory poisoning uses Mem0.
- Verification: PRIMARY-READ (Abstract, Sec. 1–3, 4.1–4.3, 5.1–5.4, Tables 1–4, Fig. 7–8, App. A threat models).
- Inference: GPT-5.1 is both attack planner and judge, and Qwen-3 is both target and (abliterated) attacker family; a state-oracle re-scoring of the AgentDojo-derived subset would show how much judge leniency contributes. The 0.0% Claude task-injection cell vs 73.3% chaining is the strongest single argument in the literature that refusal training alone does not cover decomposed attacks.

### A-02 · STAC — STAC: When Innocent Tools Form Dangerous Chains for LLM Agents
- Li, J.-J. et al., 2025 (v3 Jul 2026) · Venue: REALM 2026 workshop (ACL Anthology `2026.realm-1.17`); earlier ICLR 2026 submission withdrawn (OpenReview venueid `ICLR.cc/2026/Conference/Withdrawn_Submission`) · Tier: T2 (verified via ACL Anthology page title)
- Link: https://arxiv.org/abs/2509.25624
- Threat model: malicious user drives the agent over ≤3 user turns (each with ≤10 agent turns); pipeline generator → verifier (executes chain in environment) → prompt writer → planner. Black-box w.r.t. the target agent. Environments: 4 SHADE-Arena (Banking, Travel, Workspace, Spam Filter) + 62 Agent-SafetyBench.
- Key results:
  - 483 cases, 1,352 interaction sets, 10 failure modes (abstract).
  - Sec. 3.2: "Against all eight evaluated agents it reaches a mean final attack success rate (ASR) of 91.2% (>90% for seven of the eight; Table 2), while staying near-undetectable ... (prompt harmfulness <2%, refusal <4%)".
  - Baselines on SHADE-Arena cases: "95.1% versus 53.2% (MT-AgentRisk) and 61.5% (X-Teaming) ... in fewer turns (2.8 vs. 3.9 and 4.2; Table 3)".
  - Defense: reasoning prompt cuts ASR "by up to ∆ASR=28.8% (ASR ≥ 58.6%)"; erodes under adaptive attacks; ToolShield more durable (Sec. 1, 3.5).
  - Pilot: "ASR plateaued after 3 turns" (Sec. 3.1).
- How success is measured: **LLM judge**. "A Judge model assesses three metrics after each turn" (Sec. 2.2); ASR = "Attack Goal Progress = 3". Generator, Verifier, Planner and Judge are all GPT-4.1 (Sec. 3.1); authors acknowledge "a single-model-family dependency". X-Teaming baseline is scored by the X-Teaming judge, not the STAC judge.
- Automotive relevance: the chain idea fits vehicle APIs (e.g., disable alert → change route → share location). Verifier-executed chains guarantee executability, a good design for the thesis pipeline.
- Verification: PRIMARY-READ (Abstract, Sec. 1–3.2, metric definitions, defense setup).
- Inference: the comparison with baselines mixes judges (STAC judge vs X-Teaming judge), so the 95.1 vs 61.5 gap is not apples-to-apples. The tool chains are verified in the environment, but final success is still judge-scored.

### A-03 · Crescendo — Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack
- Russinovich, M. et al. (Microsoft, per PDF header), 2024 · Venue: USENIX Security 2025 · Tier: T1 (verified via usenix.org presentation page `usenixsecurity25/presentation/russinovich`)
- Link: https://arxiv.org/abs/2404.01833
- Threat model: malicious user, black-box chat access; starts benign and escalates "by referencing the model's replies".
- Key results (abstract): Crescendomation "achieving 29-61% higher performance on GPT-4 and 49-71% on Gemini-Pro" on an AdvBench subset vs other jailbreaks.
- How success is measured: **LLM judge + external classifiers** — "the Judge, a self-evaluation" by GPT-4, a "Secondary Judge that evaluates the Judge's output", plus Google Perspective API and Azure Content Filters (Sec. 1); manual Crescendo runs were evaluated by hand (Sec. 3).
- Automotive relevance: the escalation pattern is the conversational analogue of objective drifting; a driver/passenger can escalate over a drive.
- Verification: PRIMARY-READ (Abstract, Sec. 1 evaluation description only; venue page opened).
- Inference: chat jailbreak, not tool-use; included as the root of the multi-turn line that STAC/AgentLAB extend to tools.

### A-04 · X-Teaming — X-Teaming: Multi-Turn Jailbreaks and Defenses with Adaptive Multi-Agents
- Rahman, S. et al., 2025 · Venue: COLM 2025 · Tier: T1 (OpenReview venueid `colmweb.org/COLM/2025/Conference`)
- Link: https://arxiv.org/abs/2504.13203
- Threat model: malicious user with planner/attacker/verifier/optimizer agents (TextGrad) over many turns; black-box.
- Key results (abstract): "success rates up to 98.1%"; "96.2% attack success rate against the latest Claude 3.7 Sonnet". Releases XGuard-Train (30K multi-turn jailbreaks).
- How success is measured: **classifier/LLM judge** — headline ASR "under HarmBench evaluation" (Sec. 1); an in-loop Verifier scores each turn 1–5 (Sec. 3, Table 2 area). Table 2: Claude 3.7 Sonnet 96.2%, GPT-4o, Llama-3-IT, Gemini 2.0-Flash, DeepSeek V3 100% on HarmBench validation.
- Automotive relevance: attacker architecture template for the thesis pipeline (planner + attacker + judge), already re-used by AgentLAB (A-01).
- Verification: PRIMARY-READ (Sec. 1, metric description; Table 2 text).

### A-05 · Adaptive Adversaries — Adaptive Adversaries: A Multi-Turn, Multi-LLM Benchmark for LLM Agent Security
- Jain, D. et al. (Lambda), 2026 · Venue: ICML 2026 workshop "Agents in the Wild" (AIWILD), per OpenReview venueid `ICML.cc/2026/Workshop/AIWILD` · Tier: T2
- Link: https://arxiv.org/abs/2607.18063
- Threat model: autonomous LLM attacker observes prior defender responses and scorer feedback and pivots; each defender response is a **fresh session** (cross-session adaptive search). 21 scenarios, 3×3 attacker–defender matrix, 945 battles; plus a competition with 18,422 held-out battles on gpt-oss-20b.
- Key results:
  - Sec. 5: "round-1-only scoring gives 0.0% / 0.0% / 1.0% for Opus / GPT-5.4 / Gemini. Scoring through round 15 gives 7.9% / 9.5% / 16.8%".
  - History control: with attacker history 13/36 battles succeed vs 0/36 without (p = 6.52×10⁻⁵) (Sec. 5.4).
  - Defender-state control: "defender memory reduces ASR by 25.9 percentage points: from 57.4% (31/54) with a fresh-session defender to 31.5% (17/54 ...) with a stateful defender" (Sec. 5.4).
  - Provenance paragraph: 110/270 → 70/270 on six scenarios (abstract).
  - Pooling three attacker LLMs finds 1.7–2.2× more unique successful inputs (abstract).
- How success is measured: **state/rule oracle** — "scenario-specific checks to the defender output" (e.g., vendor score ≥70); infrastructure failures not counted (Sec. 3). Benign over-refusal uses an LLM judge.
- Automotive relevance: an in-car assistant session per drive is a "fresh-session defender"; the result says single-round scoring would report ~0% and miss real risk.
- Verification: PRIMARY-READ (Abstract, Sec. 2–3 protocol, Sec. 5.4 controls).
- Inference: this partly contradicts the reading of AgentLAB as "longer = always worse". Adaptivity across attempts helps the attacker; defender-side memory of the same conversation helps the defender. The thesis should report both fresh-session and persistent-session numbers.

### A-06 · ShadowMem (v1 title "MAGE") — Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory
- Wang, Y. et al. (same group as AgentLAB), 2026 · Venue: ACM CCS 2026 (arXiv comment "Accepted to ACM CCS 2026"; Semantic Scholar DOI 10.1145/3830454.3846601) · Tier: T1 (via S2 DOI; ACM DL not opened)
- Link: https://arxiv.org/abs/2605.03228
- Note: **the seed list described arXiv 2605.03228 as the "MAGE" attack. It is a defense.** v1 was titled "MAGE: Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory" (seen in third-party arXiv mirrors via web search); v2 is "ShadowMem". No attack paper named MAGE was found.
- Key results (abstract): "substantially outperforms existing defenses ... achieves early-stage detection for the majority of attacks" — no numbers in abstract.
- How success is measured: not read.
- Automotive relevance: belongs in the Defense survey; listed here only to correct the seed.
- Verification: ABSTRACT-ONLY.

### Group 2 — Indirect prompt injection: foundations and channels

### A-07 · Greshake et al. — Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- Greshake, K. et al., 2023 · Venue: AISec '23 (ACM workshop co-located with CCS), DOI 10.1145/3605764.3623985 (via Semantic Scholar) · Tier: T2 (workshop)
- Link: https://arxiv.org/abs/2302.12173
- Threat model: remote attacker with no direct interface plants prompts in data likely to be retrieved. Injection methods (Sec. 3, Fig. 2): passive (retrieval, SEO), active (e.g., emails), user-driven, hidden (multi-stage; encoded).
- Key results: qualitative demonstrations on Bing Chat (GPT-4) and code-completion engines; taxonomy of impacts: data theft, worming, information-ecosystem contamination, persistence. Already anticipates "persistence across sessions by copying the injection into memory" (Sec. 4).
- How success is measured: demonstrations (human inspection); no ASR.
- Automotive relevance: passive retrieval (POI reviews, web search) and active (emails/calendar synced to the car) channels both exist in connected cockpits.
- Verification: PRIMARY-READ (Sec. 1–4 skimmed for taxonomy).

### A-08 · InjecAgent — InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents
- Zhan, Q. et al., 2024 · Venue: Findings of ACL 2024 (ACL Anthology `2024.findings-acl.624`) · Tier: T1 (ACL Findings; anthology page verified)
- Link: https://arxiv.org/abs/2403.02691
- Threat model: attacker controls content returned by a user tool (e.g., a product review); goals: direct harm or data stealing. 1,054 cases, 17 user tools, 62 attacker tools, 30 agents.
- Key results: "the prompted GPT-4 demonstrates a high ASR of 24% in the base setting and a higher ASR of 47% in the enhanced setting" (Sec. 3.2); fine-tuned GPT-4 3.8%, GPT-3.5 6.6%; prompted Llama2-70B ">80% in both settings".
- How success is measured: **single next-action parse on simulated tool outputs**. "we assume that the LLM agent can accurately execute the user tool ... This hypothetical state ... is then used as a basis" (Sec. 3.1); data-stealing second step uses a GPT-4-simulated tool response. Main metric **ASR-valid** excludes invalid outputs (Sec. 3.1).
- Automotive relevance: cheap single-step screening set; not a long-horizon test.
- Verification: PRIMARY-READ (Sec. 1, 3.1–3.2).
- Inference: ASR-valid inflates vulnerability of weak models and deflates nothing for strong ones; the thesis should report ASR-all alongside.

### A-09 · AgentDojo — AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
- Debenedetti, E. et al. (ETH), 2024 · Venue: NeurIPS 2024 Datasets & Benchmarks · Tier: T1 (OpenReview venueid `NeurIPS.cc/2024/Datasets_and_Benchmarks_Track`; proceedings.neurips.cc page title verified)
- Link: https://arxiv.org/abs/2406.13352 · code https://github.com/ethz-spylab/agentdojo
- Threat model: attacker controls placeholders inside tool outputs (emails, web pages, Slack messages). 97 user tasks, 629 security cases, suites workspace/travel/banking/slack.
- Key results:
  - App. C Table 4 (GPT-4o): targeted ASR TODO 3.66%, Ignore previous 5.41%, InjecAgent 5.72%, **Important message 57.7%**.
  - App. C Table 3 (same attack across models): GPT-4o 47.69%, Claude 3.5 Sonnet 33.86%, Claude 3 Opus 11.29%, Llama 3 70b 20.03%.
  - Table 5 defenses (GPT-4o): tool filter 6.84%, PI detector 7.95% (but benign utility 41.49%), repeat prompt 27.82%, delimiting 41.65%. Text says tool filter lowers ASR "to 7.5%" (Sec. 4.3).
  - Sec. 4.1: "more capable models tend to be easier to attack, a form of inverse scaling law"; Slack suite "92% success rate".
  - Sec. 4.3: tool filter fails when tools for task suffice for attack — "true for 17% of our test cases"; also names the multi-task "wait until it receives a task that requires the right tools" scenario as not covered.
- How success is measured: **state oracle** — "The utility function is implemented as a deterministic binary function which, given outputs of the model together with the state of the environment before and after execution, determines..." (Sec. 3).
- Automotive relevance: the de-facto harness; the "wait for the right tool" scenario is exactly a delayed-trigger attack for an in-car agent that gains vehicle-control tools later in a drive.
- Verification: PRIMARY-READ (Sec. 3, 4.1, 4.3, App. C–D).
- Inference: two GPT-4o targeted ASRs coexist in the paper (47.69% Table 3 vs 57.69% Table 5) and two tool-filter values (7.5% text vs 6.84% Table 5); likely different runs/versions (v3 fixed a Llama bug and updated travel suite). Cite the table you use.

### A-10 · Formalizing PI — Formalizing and Benchmarking Prompt Injection Attacks and Defenses
- Liu, Y. et al., 2023 · Venue: USENIX Security 2024 · Tier: T1 (usenix.org page `usenixsecurity24/presentation/liu-yupei`)
- Link: https://arxiv.org/abs/2310.12815
- Threat model: attacker injects instruction/data into the data of an LLM-integrated application; formal framework where earlier attacks are special cases; "Combined Attack".
- Key results (abstract): systematic evaluation of "5 prompt injection attacks and 10 defenses with 10 LLMs and 7 tasks".
- How success is measured: task-level metrics on NLP tasks (not agentic) — details not read.
- Automotive relevance: vocabulary (target task vs injected task) for the thesis formal section.
- Verification: ABSTRACT-ONLY.

### A-11 · WASP — WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks
- Evtimov, I. et al. (Meta), 2025 · Venue: NeurIPS 2025 Datasets & Benchmarks (OpenReview `NeurIPS.cc/2025/Datasets_and_Benchmarks_Track`) · Tier: T1
- Link: https://arxiv.org/abs/2504.18575
- Threat model: realistic, weak attacker: can only post content (e.g., comments/issues) on GitLab/Reddit clones, cannot alter layout or pop-ups; black-box.
- Key results: "while attacks partially succeed in up to 86% of cases, the agents often struggle to fully carry out the malicious tasks, with attacker task completion rates ranging from 0 to 17%" (Sec. 1); Sec. 4: "between 17-86% ASR-intermediate ... ASR-end-to-end of only up to 16%". Agents: Claude Computer Use, GPT-4o VisualWebArena, o1, GPT-4o-mini.
- How success is measured: **state oracle** for ASR-end-to-end ("rule-based evaluator to check if the final state satisfies the specified rule"); **LLM judge (GPT-4o)** for ASR-intermediate (Sec. 3.4).
- Automotive relevance: the intermediate-vs-end-to-end split should be adopted; in a car, "intermediate" deviation (agent distracted, asks confusing questions) is itself a safety hazard.
- Verification: PRIMARY-READ (Sec. 1, 3.3–3.4, 4 intro).
- Inference: "security by incompetence" decays as agents get more capable — a moving baseline.

### A-12 · INFUSE — INFUSE: A Unified Surface Benchmark for Indirect Prompt Injection in Agentic Systems
- Nguyen, T. D. et al. (Vanderbilt), 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2610.20776
- Threat model: IPI injected through realistic interaction surfaces across long-horizon workflows (shell, code, dependency install, remote services); 40 tasks, 56 attack scenarios, 5 threat categories, 19 LLMs, 41,824 adversarial trajectories.
- Key results (abstract): "mean attack success reaches 19.6% under LLM-based evaluation and 15.4% under heuristic verification, with per-model ASR-L ranging from 3.2% to 41.9%"; prompt hardening "reduces mean attack success from 58.2% to 14.3%".
- How success is measured: **both** — ASR-L by a GPT-4o-mini judge that is itself an evaluated model (validated with a cross-family committee, App. A.4) and ASR-H by "heuristic checks for concrete artifacts such as attacker-controlled commits, exfiltrated files, or modified credentials" (Sec. 3, Phase 4). Reports the gap (19.6% vs 15.4%).
- Automotive relevance: methodological precedent for reporting judge-vs-oracle disagreement.
- Resolved from full text (Sec. 4.3): defenses are evaluated on "a controlled subset of 20 attacks (IDs 101–120) and up to 10 tasks ... on which agents are most vulnerable"; "This stress-test subset has an undefended ASR-L of 58.2%, compared with the 19.6% full-benchmark average ... absolute reductions should not be extrapolated to the full benchmark." The abstract's "58.2% to 14.3%" therefore refers to the stress subset only.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 3 scoring, 4.3 defense analysis, App. D.3 protocol).

### A-13 · AutoDojo — AutoDojo: A Generative Benchmark for Evaluating Prompt Injection Defenses in LLM Agents
- Ma, X. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2606.15057
- Threat model: strict black-box; optimizer observes only whether a candidate injection succeeds; built on AgentDojo and AgentDyn, six suites.
- Key results (abstract): "Across ten defenses and five target models, AutoDojo demonstrates that standard static benchmarks often significantly overestimate defense efficacy"; "under-specified tasks particularly vulnerable". No numbers in abstract.
- How success is measured: inherits AgentDojo state checks (inference from "built on AgentDojo"; not read).
- Automotive relevance: in-car requests are often under-specified ("take me somewhere to charge") — the vulnerable regime.
- Verification: ABSTRACT-ONLY.

### A-14 · ASPI — ASPI: Seeking Ambiguity Clarification Amplifies Prompt Injection Vulnerability in LLM Agents
- Sehwag, U. M. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2605.17324
- Threat model: injected content arrives either via tool output (execution setting) or during a clarification exchange the agent itself initiates. 728 task-attack scenarios, 10 frontier LLMs.
- Key results (abstract): "attack success rises from 1.8% to 34.0% for o3 and from 2.2% to 35.7% for Gemini-3-Flash".
- How success is measured: **state oracle (AgentDojo-based)** — ASPI "builds on AgentDojo" and ASR "measures how often the attacker goal I is achieved" (Sec. 5). Injection channels: task-tool output, the `ask_user` tool return (clarif_ask_user) or a user message (clarif_user) (Sec. 4).
- Automotive relevance: high — CAR-bench (A-50) rewards clarification ("Disambiguation tasks"); in-car clarification answers can come from passengers or ambient audio.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 4–5 definitions).

### Group 3 — Memory / knowledge poisoning, delayed triggers, cross-session

### A-15 · AgentPoison — AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases
- Chen, Z. et al., 2024 · Venue: NeurIPS 2024 (OpenReview `NeurIPS.cc/2024/Conference` poster) · Tier: T1
- Link: https://arxiv.org/abs/2407.12784
- Threat model (Sec. 3): attacker can inject a few instances into the agent's memory/RAG KB and has **white-box access to the RAG embedder** for trigger optimisation (transfer to black-box ADA shown). The trigger must appear in the victim's query.
- Key results:
  - Abstract: "average attack success rate higher than 80% with minimal impact on benign performance (less than 1%) with a poison rate less than 0.1%".
  - Table 1, Agent-Driver (autonomous driving, target action "SUDDEN STOP"), AgentPoison rows: ASR-r 78.0–84.4%, ASR-a 64.9–94.7%, **ASR-t (end-to-end) 54.7–59.6%**, ACC 82.4–92.0%.
  - Sec. 1: "82% retrieval success rate and 63% end-to-end attack success rate".
- How success is measured: **output-label / offline target-action match**. ASR-t = "percentage of test instances where the agent achieves the final adversarial impact on the environment (e.g., collision)" (Sec. 4.1); Agent-Driver is run on its released (nuScenes-based) dataset, i.e., open-loop.
- Automotive relevance: the only top-venue poisoning attack with a driving agent; but trigger-in-query assumption is strong for a cockpit assistant.
- Verification: PRIMARY-READ (Sec. 1, 3 threat model, 4.1 metrics, Table 1).
- Inference: the ">80%" headline is retrieval success (ASR-r), not end-to-end; cite ASR-t when talking about harm. Open-loop "collision" is not closed-loop driving.

### A-16 · MINJA — Memory Injection Attacks on LLM Agents via Query-Only Interaction
- Dong, S. et al. (MSU), 2025 · Venue: NeurIPS 2025 (OpenReview `NeurIPS.cc/2025/Conference` poster; S2 DOI 10.52202/085713-1554) · Tier: T1
- Link: https://arxiv.org/abs/2503.03704
- Threat model (Sec. 3): attacker is a regular user, no direct memory access, cannot touch victim queries; **assumes a shared memory bank across users** and that records are stored after execution. Uses bridging steps, indication prompt, progressive shortening.
- Key results (Sec. 1): "MINJA achieves a high average success rate of 98.2% for injecting malicious records into the memory, and a high average attack success rate of 76.8%". Agents: RAP (WebShop), EHRAgent (MIMIC-III, eICU), QA agent (MMLU).
- How success is measured: ISR (record stored) and ASR (agent produces target reasoning steps for the victim query) — target-match; scoring method details not read.
- Automotive relevance: fleet-shared memory (OEM backend learning from many drivers) is exactly the shared-memory assumption; a single malicious driver could poison suggestions to others.
- Verification: PRIMARY-READ (Sec. 1, 3, 4.1 setup).
- Inference: in a per-vehicle private memory, MINJA's threat model collapses to self-poisoning; it only bites with shared/fleet memory.

### A-17 · Promptware — Invitation Is All You Need! Promptware Attacks Against LLM-Powered Assistants in Production Are Practical and Dangerous
- Nassi, B. et al., 2025 · Venue: arXiv only (arXiv comment links only the project site sites.google.com/view/invitation-is-all-you-need; no peer-reviewed venue found) · Tier: T3
- Link: https://arxiv.org/abs/2508.12175
- Threat model: attacker sends email / calendar invitation / shared doc; user asks Gemini assistant about meetings; context poisoned. 14 scenarios, 5 threat classes incl. "Permanent Memory Poisoning", "Automatic Agent Invocation", "Automatic App Invocation".
- Key results: "73% of the analyzed threats pose High-Critical risk" (abstract) using a TARA "adapting ISO/SAE 21434 for automotive cybersecurity" (Sec. 1). Delayed trigger demo: invitation title poisons context; "When the user thanked the assistant, it replied with a recommendation" (Sec. 5.1.2). Physical effects: opening windows, activating boiler via Google Home; text names "the user's car is remotely ..." as a critical-severity example (Sec. 4).
- How success is measured: demonstrations (videos); risk scored by TARA, not ASR.
- Automotive relevance: very high — calendar/email sync is in production cockpits; the TARA is ISO/SAE 21434-based, directly reusable at VW. Disclosed to Google, mitigations deployed (abstract).
- Verification: PRIMARY-READ (Sec. 1, 4, 5.1–5.3 partially).

### A-18 · MemHarm (counterfactual memory attacks) — From Attack Success to Attack Severity: Counterfactual Memory Attacks on LLM Agents
- Zou, M. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2609.34132
- Threat model: attacker writes to persistent memory through the normal interface; optimises *severity* (counterfactual memory regret, CMR = paired increase in expected downstream loss vs clean memory), not success.
- Key results (abstract): "CMR-guided selection produces substantially larger downstream loss while retaining most of the success-rate gain"; verifies "write-to-fresh-process attack path". No numbers in abstract.
- How success is measured: paired downstream loss (counterfactual), offline.
- Automotive relevance: severity-weighted metrics fit ISO 26262 / 21434 thinking better than binary ASR.
- Verification: ABSTRACT-ONLY.

### A-19 · CarryoverBench — After the Attacker Leaves: Benchmarking Carryover Attacks on LLM Agents
- Xu, Z. et al. (CASIA), 2026 · Venue: EMNLP 2026 Main (ACL Anthology `2026.emnlp-main.1996`) · Tier: T1 (anthology page verified)
- Link: https://arxiv.org/abs/2610.28425
- Threat model: one-time IPI; payload committed to (a) a memory file prepended to the system prompt (Latent) or (b) a scheduled task / HEARTBEAT (Autonomous); fires in later sessions "long after the attacker leaves". 12 scenarios, 101 attack tasks (35 Instant, 30 Autonomous, 36 Latent); harness Nanobot (OpenClaw-like).
- Key results:
  - Table 1 overall ASR: GPT-5.4 11.9%, Claude-Sonnet-4.6 18.8%, Gemini-3.1-Pro 51.5%, GLM-5 27.7%, Qwen3-235B 63.4%. Autonomous column for Qwen3: 83.3%.
  - Decomposition ASR = Pr(Plant)·Pr(Trig|Plant) (Eq. 7). Sec. 4.2: "Autonomous, Pr(trig | plant) ≈ 1 on all 5 models".
  - "Persistence does not decay": across 5 follow-up sessions no monotonic decay (Sec. 4.3, Table 2).
  - Defenses act at the plant stage and leave "the trigger gate largely" open (Sec. 5).
- How success is measured: **state/rule oracle** — "Rule-based rather than LLM-as-judge. Under adversarial traces, a judge prompt is itself an injection surface" (Sec. 3.2).
- Automotive relevance: maps 1:1 to drive cycles (each ignition = fresh session; persistent profile/memory = Latent; scheduled pre-conditioning / reminders = Autonomous).
- Verification: PRIMARY-READ (Abstract, Sec. 3.1–3.3, 4.1–4.3, Table 1, Sec. 5 summary).

### A-20 · MemoryDojo — MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory
- Yang, D. H. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2611.09721
- Threat model: malicious instructions in one session stored by the memory system and acted on in later sessions; 155 multi-session trajectories, 4 domains, 5 memory systems; memory-aware poison optimisation.
- Key results (abstract): "all memory systems are susceptible to memory poisoning, with substantial variation in downstream effects". No numbers in abstract.
- How success is measured: not read.
- Automotive relevance: memory architecture is a design variable for in-vehicle agents; this lets you compare them.
- Verification: ABSTRACT-ONLY.

### A-21 · MemGhost / WhisperBench — When Claws Remember but Do Not Tell: Stealthy Memory Injection in Persistent Personal Agents
- Zhang, Y. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2607.05189
- Threat model: remote black-box adversary sends **one email**; must make the agent write poisoned memory, stay hidden from the user, and affect future behaviour. Attacker policy trained with SFT + RL using proxy environments. 108-case benchmark on real IMAP/SMTP.
- Key results (abstract): "MemGhost achieves 87.5% end-to-end success on OpenClaw with GPT-5.4 and 71.4% on Claude Code SDK with Sonnet 4.6"; transfers to NanoClaw, Hermes Agent, Mem0.
- How success is measured: not read (rubric-based rewards used for training; final metric unclear).
- Automotive relevance: a single email synced to the car profile could plant a preference ("always route via X") silently.
- Verification: ABSTRACT-ONLY.

### A-22 · MemPoison — MemPoison: Bypassing Selective Memory Mechanisms to Plant Backdoors in LLM Agents
- Wang, H. et al., 2026 · Venue: ACM CCS 2026 (arXiv comment "Accepted by ACM CCS 2026"; S2 lists CCS proceedings) · Tier: T1-claimed (no DOI seen)
- Link: https://arxiv.org/abs/2605.29960
- Threat model: dialogue-only attacker plants a triggerable backdoor that survives **selective extraction and rewriting** stages of modern memory pipelines (semantic relational bridge, entity masquerading, joint embedding optimisation).
- Key results (abstract): "attack success rates up to 0.95".
- How success is measured: not read.
- Automotive relevance: in-car memory will be selective (summarised preferences), the regime this targets.
- Verification: ABSTRACT-ONLY.

### A-23 · SkillRelayBench — Understanding and Mitigating Cross-Session Attacks via Persistent Artifacts in Agent Skill Composition
- Liao, D. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2610.13227
- Threat model: artifacts (files, configs, caches) written by one skill in one session are consumed by another skill later: Instruction Propagation, Data Boundary Violation, Evidence Poisoning. 270 cases, 30 scenarios; Codex CLI, Gemini CLI, Claude Code.
- Key results (abstract): "ASR ranging from 46.7% to 77.4% and attack chain success rates (ACSR) ranging from 35.6% to 61.1%"; SkillRelayGuard 69.5% → 10.9% ASR.
- How success is measured: not read.
- Automotive relevance: OEM app/skill ecosystems with shared cached state (e.g., trip logs) form the same relay.
- Verification: ABSTRACT-ONLY.

### Group 4 — Tool / MCP poisoning and supply chain

### A-24 · MCPTox — MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers
- Wang, Z. et al., 2025 · Venue: AAAI 2026, Proc. AAAI 40(42) 35811–35819 · Tier: T1 (verified on AAAI OJS article 40895; also OpenReview archive record)
- Link: https://arxiv.org/abs/2508.14925
- Threat model: malicious MCP server whose **tool description** carries instructions; poisoned tool is never executed; malicious action done via legitimate tools. Paradigms: explicit-trigger function hijacking, implicit-trigger function hijacking, implicit-trigger **parameter tampering** (Sec. 3.1). 45 servers, 353 tools, 1,348 cases, 20 model settings.
- Key results: "o1mini and Phi-4 exhibited the highest vulnerability, with extremely high average ASRs of 72.8% and 70.2%"; GPT-4o-mini 61.8% (Sec. 4.2); highest refusal "Claude-3.7-Sonnet less than 3%" (abstract); "more capable models are often more susceptible" (abstract).
- How success is measured: **tool-call output classification** (single turn): Success / Ignored / Direct Execution / Refused (Sec. 3.4). ASR = successes / **valid outputs** (following InjecAgent). Who/what assigns labels is not stated in the parts read → *unclear*.
- Automotive relevance: third-party connectors (parking, charging, music) as MCP-like servers; parameter tampering paradigm = A-30.
- Verification: PRIMARY-READ (Sec. 1, 3.1, 3.4, 4.1–4.2).

### A-25 · FuncPoison — FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems
- Long, Y. & Li, S., 2025 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2509.24408
- Threat model: attacker injects malicious tools with deceptive instructions into the **shared function library** of LLM multi-agent driving systems; exploits text-based tool selection and replicable command formats; errors cascade across agents.
- Key results (abstract): "significantly degrade trajectory accuracy", targets specific agents, evades defenses — no numbers in abstract.
- How success is measured: trajectory accuracy degradation (offline planning metrics; inference from abstract).
- Automotive relevance: the most direct driving-stack supply-chain attack; tied to multi-agent hand-offs.
- Verification: ABSTRACT-ONLY.

### A-26 · MCP-SafetyBench — MCP-SafetyBench: A Benchmark for Safety Evaluation of Large Language Models with Real-World MCP Servers
- Zong, X. et al., 2025 · Venue: ICLR 2026 (OpenReview `ICLR.cc/2026/Conference` poster) · Tier: T1
- Link: https://arxiv.org/abs/2512.15163
- Threat model: 20 MCP attack types spanning server, host and user sides; multi-turn; 5 domains incl. location navigation.
- Key results (abstract): "all models remain vulnerable to MCP attacks, with a notable safety-utility trade-off". No numbers in abstract.
- How success is measured: not read.
- Automotive relevance: has a location-navigation domain.
- Verification: ABSTRACT-ONLY.

### A-27 · TrustShiftProbe — TrustShiftProbe: Characterizing, Benchmarking, and Defending Staged Trust Attacks on MCP Servers
- Rostamzadeh, M. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2608.23763
- Threat model: compromised MCP server behaves benignly during a conditioning phase, then defects at an interaction threshold ("temporal, not syntactic" evasion); invisible to pre-deployment static analysis.
- Key results (abstract): "TrustShift attacks achieve a 69.5% mean attack success rate that SHIELD mitigates to 42.7%".
- How success is measured: not read.
- Automotive relevance: OEM certification of third-party connectors is a pre-deployment snapshot — exactly what this evades.
- Verification: ABSTRACT-ONLY.

### A-28 · Cross-channel fragmentation — Measuring and Exploiting Implicit Trust in LLM Tool-Calling Pipelines
- Ediga, M. & Chattopadhyay, S., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2609.18217
- Threat model: malicious MCP server spreads benign-looking fragments over tool descriptions, tool results and sampling messages; no single channel holds a full injection.
- Key results (abstract): "models that fully resist single-channel injection (0% compliance) exfiltrate sensitive data at up to 100% under two-channel fragmentation"; 12 models, 3 clients, >15,000 trials; all 7 third-party MCP security tools failed to detect fragmented payloads.
- How success is measured: **graded rubric** — 5-point scale per trial; "scores of 4 or 5 are classified as COMPLY (the attacker obtained the requested data)" (Sec. 5). Who assigns the score was not checked.
- Automotive relevance: in-vehicle agents merge many channels (calendar, POI, voice, OEM backend) in one context window.
- Verification: ABSTRACT-ONLY.

### Group 5 — Instruction-free / decision-tampering attacks

### A-29 · Task tampering — Beyond Instruction Override: Benchmarking Indirect Prompt Injection with Task-Tampering Attacks
- Zhang, R. et al. (Amazon), 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2611.07640
- Threat model (Sec. 3): attacker is "a legitimate participant in the environment, such as a vendor, repository contributor"; cannot intercept tool calls; planted content tampers with a decision required by the benign task. IPI defined "by authority rather than instruction-like wording". 90 cases, 3 environments (productivity, DevOps, marketplace), 1,343 single-primitive attacks; six primitives: objective b(U), decision rules b(π), actions b(A), consequences b(T), observations b(O), state b(s).
- Key results (Table 3, mean over 5 LLMs): no defense 17.0% ASR; b(π) 21.2, b(A) 19.0, b(s) 18.6 vs b(U) 15.0. DRIFT-isolation: b(U) **2.4%** vs b(O) **9.5%**, b(s) **12.1%**. Progent "remains near the undefended ASR (15.4% versus 17.0%)". CaMeL 1.3% ASR but 13.3% benign task success.
- How success is measured: **state oracle + narrow LLM judge**: "Exact values, bounds, recipients, tool usage ... are checked programmatically. When a free-form outcome requires semantic interpretation, code extracts the relevant field and an LLM judge evaluates a case-specific binary predicate on that field"; human agreement 97.2% (Sec. 4).
- Automotive relevance: high — e.g., a fake charger-status note changing which station the agent picks, without any instruction.
- Verification: PRIMARY-READ (Abstract, Sec. 3–4, Table 3, Sec. 5.2–5.3).

### A-30 · Parameter poisoning / AuthorityFlow — Right Tool, Wrong Parameters: Defending LLM Agents Against Parameter Poisoning
- Wang, Y. et al. (USTC), 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2611.04673
- Threat model: attacker manipulates external content so that the intended tool is called but an argument (recipient, amount, location) is changed. FactAuthBench: 144 paired benign–attack cases on AgentDojo suites.
- Key results (Sec. 5): "Without defense, ASR reaches 93.06% on Qwen3.6-27B and 57.64% on GPT-4o"; Sandwiching 72.22%, Spotlighting 69.44%, MELON 79.17% on Qwen3.6-27B; AuthorityFlow → 9.03% ASR with 82.64% benign utility (abstract).
- How success is measured: **state oracle** — "attacker-intended parameter value to appear in the executed tool call" (Sec. 5.1).
- Automotive relevance: destination coordinates, cabin temperature, charge limit, contact to call — all parameter slots.
- Verification: PRIMARY-READ (Sec. 1, 5.1 metrics, 5.2 results).

### A-31 · Voluntary servitude — Voluntary Servitude: Weaponized Safety Warning Mechanisms for Controlling AI Agents
- Zendel, I. et al. (Technion), 2026 · Venue: NeurIPS 2026 Main Track (arXiv comment; OpenReview venue "NeurIPS 2026 poster") · Tier: T1
- Link: https://arxiv.org/abs/2611.04393
- Threat model (Sec. 3): attacker posts ordinary reviews containing a fabricated hazard on public pages; "needs no access to the model, its prompt, its retriever or its detectors". Agent's own harm-avoidance disqualifies legitimate options.
- Key results: generation-stage steering "60.4% vs. 66.0%" (safety payload vs instruction injection); behind ProtectAI / Lakera detectors "1.7 to 4.4 times as effective as instruction injection" (Table 1); browser agents: "Edge selected the attacker's listing in every trial against 20% for instruction injection, Comet in 60% against none" (Sec. 5); corroboration requirement removes "roughly 95% of the exposure against a non-adaptive attacker" (abstract).
- How success is measured: **LLM judge** (Llama-3.3-70B, temp 0) labelling recommendation status; human relabel of 100 answers, "Agreement on the success category is 90.0%, κ = 0.742" (Sec. 4). Browser trials: 20 per attack per agent.
- Automotive relevance: very high — a car agent weighting safety warnings ("road closed due to flooding", "charger fire hazard") is the ideal victim; this is an instruction-free POI/route tampering primitive.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 3, 4 measurement, browser-agent results).

### A-32 · ChatInject — ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents
- Chang, H. et al., 2025 · Venue: ICLR 2026 (OpenReview `ICLR.cc/2026/Conference` poster) · Tier: T1
- Link: https://arxiv.org/abs/2509.22830
- Threat model: third party formats payload with forged chat-template role tokens; Multi-turn variant embeds a fake persuasive dialogue inside one tool output (Sec. 1, 3).
- Key results (abstract): "improving from 5.18% to 32.05% on AgentDojo and from 15.13% to 45.90% on InjecAgent, with multi-turn dialogues showing particularly strong performance at average 52.33% success rate on InjecAgent"; transfers to closed models.
- How success is measured: inherits AgentDojo (state) and InjecAgent (next-action parse) metrics.
- Automotive relevance: on-board open-weight models with known templates are the easiest targets.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 3 method overview).
- Inference: "simulated multi-turn inside a single observation" lets a one-shot channel emulate a long-horizon attack — relevant for the thesis's adversarial-example pipeline.

### Group 6 — Multi-agent

### A-33 · Prompt Infection — Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems
- Lee, D. & Tiwari, M., 2024 · Venue: arXiv; ICLR 2025 submission **rejected** (OpenReview `ICLR.cc/2025/Conference/Rejected_Submission`) · Tier: T3
- Link: https://arxiv.org/abs/2410.07283
- Threat model: malicious prompt self-replicates across interconnected agents.
- Key results (abstract): "multi-agent systems are highly susceptible, even when agents do not publicly share all communications"; LLM Tagging defense. No numbers in abstract.
- How success is measured: not read.
- Automotive relevance: cockpit agents passing messages (navigation ↔ media ↔ vehicle-function agent).
- Verification: ABSTRACT-ONLY.

### A-34 · MAS control-flow hijacking — Multi-Agent Systems Execute Arbitrary Malicious Code
- Triedman, H. et al. (Cornell Tech), 2025 · Venue: COLM 2025 (OpenReview `colmweb.org/COLM/2025/Conference`) · Tier: T1
- Link: https://arxiv.org/abs/2503.12188
- Threat model: adversarial web content / files hijack orchestrator control flow ("metadata transmission" via fake error messages) in AutoGen (Magentic-One, Selector, Round-Robin), CrewAI, MetaGPT.
- Key results: "Web-based attacks successfully cause the multi-agent system execute arbitrary malicious code in 58-90% of trials (depending on the orchestrator). In some model-orchestrator configurations, the attack success rate is 100%" (abstract); "Magentic-One orchestrator ... executes ... code 88% of the time" (Sec. 1); attacks succeed "even when sub-agents refuse" (Sec. 1, App. J–K).
- How success is measured: **real system oracle** — modified executor + "a lightweight cloud server to monitor incoming reverse shell connections" (Sec. 5). 10 runs per configuration.
- Automotive relevance: orchestrator-level trust is the cockpit↔backend hand-off; refusals by one agent do not stop another.
- Verification: PRIMARY-READ (Abstract, Sec. 1, threat model, Sec. 5 setup).

### A-35 · Can CaMeLs Talk? — Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks
- Peters-Gill, J. et al. (Oxford et al.), 2026 · Venue: arXiv (preprint) · Tier: T3
- Link: https://arxiv.org/abs/2610.05640
- Threat model: hierarchical agents-as-tools each running CaMeL; untrusted data from one agent is "reinterpreted as trusted input by a downstream agent".
- Key results (abstract): "CaMeL's guarantees do not compose"; on MultiAgentDojo ASR 12.9% (no CaMeL), 0.2% (individual CaMeL), 0.0% (multi-CaMeL).
- How success is measured: AgentDojo-derived state checks for security; utility partly by an LLM judge with privileged information (Sec. on AssetOpsBench).
- Automotive relevance: provenance must survive cockpit-agent → vehicle-agent boundaries.
- Verification: PRIMARY-READ (Abstract, Sec. 1, MultiAgentDojo description).
- Inference: 0.2% vs 0.0% is a small absolute gap; the composition break is shown by a constructed attack, i.e., a possibility result rather than a high measured rate.

### A-36 · AiTM — Red-Teaming LLM Multi-Agent Systems via Communication Attacks
- He, P. et al., 2025 · Venue: Findings of ACL 2025 (ACL Anthology `2025.findings-acl.349`) · Tier: T1 (Findings; anthology page verified)
- Link: https://arxiv.org/abs/2502.14847
- Threat model: Agent-in-the-Middle intercepts and rewrites inter-agent messages; LLM adversarial agent with reflection.
- Key results (abstract): "LLM-MAS is vulnerable to communication-based attacks" — numeric claims seen only in a search snippet, not verified → omitted.
- How success is measured: not read.
- Automotive relevance: in-vehicle bus/IPC between agents (if messages are not authenticated).
- Verification: ABSTRACT-ONLY.

### A-37 · Agent Smith — Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast
- Gu, X. et al., 2024 · Venue: ICML 2024, PMLR v235 · Tier: T1 (title found on proceedings.mlr.press/v235 index)
- Link: https://arxiv.org/abs/2402.08567
- Threat model: adversarial image placed in one agent's memory spreads through pairwise chats ("infectious jailbreak"); simulated up to one million LLaVA-1.5 agents.
- Key results (abstract): "(almost) all agents will become infected exponentially fast".
- How success is measured: simulation; harmful-output rate.
- Automotive relevance: V2X / fleet agent-to-agent messaging is a future propagation path.
- Verification: ABSTRACT-ONLY.

### Group 7 — Attack generation methods and adaptive attackers

### A-38 · The Attacker Moves Second — The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections
- Nasr, M., Carlini, N. et al. (Google DeepMind, OpenAI, Anthropic et al.), 2025 · Venue: arXiv; ICLR 2026 submission **rejected** (OpenReview `ICLR.cc/2026/Conference/Rejected_Submission`); PDF header "Preprint. Under review." · Tier: T3
- Link: https://arxiv.org/abs/2510.09023
- Threat model: adaptive attacker who knows the defense; four families: gradient, RL, search (LLM mutator), human red-teaming (online competition, ">500 participants", "$20,000 in prizes", App. F).
- Key results (Sec. 5): Spotlighting / Prompt Sandwiching on AgentDojo: static ASR "as low as 1%", search attack ">95% for both"; MetaSecAlign "reports ... 2% on the static AgentDojo benchmark ... achieved a 96% ASR"; detectors: ">90% against Protect AI, PromptGuard, and Model Armor", PIGuard 71%; MELON 76% without knowledge, 95% with; Circuit Breakers 100% (RL, HarmBench). Lesson #3: "the search attack succeeds 69% of the time whereas the red-teaming humans collectively succeeds 100%" on a subset.
- How success is measured: AgentDojo **state oracle** for PI; HarmBench-style classifiers for jailbreak; Lesson #4 warns "Model-based auto-raters can be unreliable".
- Automotive relevance: sets the bar — any defense in the thesis must be tested with an adaptive attacker that knows it.
- Verification: PRIMARY-READ (Sec. 3–6, App. F excerpt).
- Inference: the rejection does not undercut the empirical results, but cite it as a preprint (T3), not as ICLR.

### A-39 · Hofer et al. — Assessing Automated Prompt Injection Attacks in Agentic Environments
- Hofer, D., Debenedetti, E., Tramèr, F. (ETH), 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2606.10525
- Threat model: white-box GCG and black-box TAP adapted to AgentDojo; single-task and task-universal; 80 task pairs; targets Qwen3-4B, Gemma3-4B, GPT-5.
- Key results: "TAP substantially outperforms gradient-based GCG (45.2% vs. 24.1% ASR on Qwen3-4B)" (Sec. 1); GPT-5 "remains vulnerable to TAP (∼5% ASR, 30% S@N)" (Fig. caption); GCG suffixes from small open models "do not transfer to frontier models like GPT-5" (abstract); safety-tuned attackers can refuse.
- How success is measured: **state oracle** (AgentDojo checks; "avoiding the unreliability of LLM-based evaluation"); TAP's internal search scoring uses GPT-5-mini as judge.
- Automotive relevance: on-board small open models are the GCG-friendly regime; cloud frontier models need black-box search.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 5 setup, Fig. 1 caption).

### A-40 · AutoInject — Learning to Inject: Automated Prompt Injection via Reinforcement Learning
- Chen, X., Zhang, J., Tramèr, F., 2026 · Venue: NeurIPS 2026 (OpenReview `NeurIPS.cc/2026/Conference` poster) · Tier: T1
- Link: https://arxiv.org/abs/2602.05746
- Threat model: black-box RL learns adversarial suffixes; comparison-based reward turns binary success into dense signal; online or offline transferable.
- Key results (abstract): outperforms template, GCG, TAP and adaptive attack on AgentDojo "with statistically significant improvements under McNemar's test with p<0.05"; breaks Meta-SecAlign-70B "where template attacks fail outright".
- How success is measured: AgentDojo state oracle (inference from benchmark).
- Automotive relevance: offline-trained transferable suffixes fit a realistic attacker who cannot query the car.
- Verification: ABSTRACT-ONLY.

### A-41 · RL-Hammer — RL Is a Hammer and LLMs Are Nails: A Simple Reinforcement Learning Recipe for Strong Prompt Injection
- Wen, Y. et al., 2025 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2510.04885
- Threat model: attacker model trained from scratch with RL; universal injections.
- Key results (abstract): "98% ASR against GPT-4o and a 72% ASR against GPT-5 with the Instruction Hierarchy defense"; attackers "reward-hack diversity objectives"; evades detectors.
- How success is measured: not read.
- Automotive relevance: generator for the thesis attack pipeline.
- Verification: ABSTRACT-ONLY.

### A-42 · Agent swarms — Scaling Adaptive Prompt Injection Attacks with Agent Swarms
- Kurakin, A. et al. (Google DeepMind), 2026 · Venue: arXiv technical report · Tier: T3
- Link: https://arxiv.org/abs/2611.11861
- Threat model: "Agentic Optimizer" = 8 teams × 2 agents, ≤320 evaluation calls, shared strategy database; synthetic dataset with **random non-malicious actions** as adversarial goals (isolates instruction-hierarchy compliance from harm knowledge).
- Key results (Table 1, attacker Gemini 4 Argon): attack-resisted rate (ARR) — Gemini 3.6 Flash 1.0%, Gemini 3.8 Flash 10.0%, Gemini 4 Argon 66.0% (87.0% at 150 queries), Kimi K3 1.0%. Quote: "No defender is fully robust" (Sec. 5.2). Context: "human red-teaming may be nearing saturation, especially on the Gemini family" (abstract).
- How success is measured: **state oracle** on tool calls — success if score >0.99: target function called with arguments at >96% Jaccard similarity (Sec. 3).
- Automotive relevance: shows the attacker's capability, not the target's, drives success — attacker strength must be a reported variable.
- Verification: PRIMARY-READ (Abstract, Sec. 1, 3, 5.1–5.2).
- Inference / caveat: "All Gemini models ... were queried without any safety classifiers and with disabled out-of-model prompt injection defenses" (Sec. 5.1) — results bound the model, not the deployed product.

### A-43 · TAP / PAIR / GCG (attack-generation baselines)
- TAP: Mehrotra, A. et al., "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically", NeurIPS 2024 (OpenReview `NeurIPS.cc/2024/Conference` poster) · T1 · https://arxiv.org/abs/2312.02119
- PAIR: Chao, P. et al., "Jailbreaking Black Box Large Language Models in Twenty Queries", IEEE SaTML 2025 (Semantic Scholar DOI 10.1109/SaTML64287.2025.00010; ICLR 2024 submission rejected per OpenReview) · T1 (via S2 DOI)
- GCG: Zou, A. et al., "Universal and Transferable Adversarial Attacks on Aligned Language Models", 2023, arXiv only (no venue in arXiv record; S2 venue "arXiv.org") · T3 · https://arxiv.org/abs/2307.15043
- Threat model: TAP/PAIR black-box attacker-LLM search with judge scoring; GCG white-box greedy coordinate gradient suffixes with transfer.
- Key results: GCG abstract — suffixes trained on Vicuna-7B/13B "induce objectionable content in the public interfaces to ChatGPT, Bard, and Claude". For agents see A-39 (TAP > GCG; no GCG transfer to GPT-5).
- How success is measured: TAP/PAIR use an LLM judge during search; GCG uses refusal-prefix matching (from my knowledge, not re-read).
- Automotive relevance: building blocks of the thesis attack generator.
- Verification: ABSTRACT-ONLY (venues checked).

### Group 8 — Physical, perception and voice channels

### A-44 · RoboPAIR — Jailbreaking LLM-Controlled Robots
- Robey, A. et al., 2024 · Venue: ICRA 2025 (Semantic Scholar DOI 10.1109/ICRA55743.2025.11128119) · Tier: T1 (via S2 DOI)
- Link: https://arxiv.org/abs/2410.13691
- Threat model: white-box (NVIDIA Dolphins self-driving LLM), gray-box (Jackal UGV with GPT-4o planner), black-box (Unitree Go2).
- Key results (abstract): "often achieving 100% attack success rates"; "first successful jailbreak of a deployed commercial robotic system".
- How success is measured: not read (judge-based in PAIR lineage — inference).
- Automotive relevance: includes a self-driving LLM (Dolphins) as a target.
- Verification: ABSTRACT-ONLY.

### A-45 · CHAI — CHAI: Command Hijacking against embodied AI
- Burbano, L. et al. (UC Santa Cruz et al.), 2025 · Venue: IEEE SaTML 2026 (arXiv comment; S2 DOI 10.1109/SaTML68715.2026.00055) · Tier: T1 (via S2 DOI)
- Link: https://arxiv.org/abs/2510.00181
- Threat model (Sec. 3): attacker places deceptive text (e.g., signs) in the scene; "cannot physically contact the vehicle"; black-box; optimiser builds a prompt dictionary and generates Visual Attack Prompts.
- Key results (Sec. 1): "up to 95.5% attack success rate (ASR) on CloudTrack, 81.8% on DriveLM, and 72.8% on drone landing in simulation. In real-world robotic vehicle experiments, CHAI achieves up to ≥ 87%". Sec. 6.A: "in all applications and LVLMs, CHAI yields an ASR over 54%"; outperforms SceneTAP up to 10×. Targets: GPT-4o, InternVL2.5-8B.
- How success is measured: **output-label match** — "an attack is successful if, as a consequence of the attack, the LVLM outputs the target label" (Sec. 5.B); no-attack baseline also reported (DriveLM no-attack ASR 6.22% ± 2.93, Table IV) because of stochasticity.
- Automotive relevance: highest-relevance physical attack; but DriveLM numbers are image-level decisions (open-loop), not closed-loop driving.
- Verification: PRIMARY-READ (Sec. 1, 3 threat model, 5.B metric, 6.A, Table IV header).

### A-46 · Typographic attacks on AD Vision-LLMs — Towards Transferable Attacks Against Vision-LLMs in Autonomous Driving with Typography
- Chung, N. et al., 2024 · Venue: arXiv ("work in progress") · Tier: T3
- Link: https://arxiv.org/abs/2405.14169
- Threat model: typographic text in traffic scenes misleads Vision-LLM reasoning; studies physical realisability.
- Key results (abstract): "particular harmfulness ... against existing Vision-LLMs (e.g., LLaVA, Qwen-VL, VILA, and Imp)". No numbers in abstract.
- How success is measured: not read.
- Automotive relevance: precursor of A-45 in driving scenes.
- Verification: ABSTRACT-ONLY.

### A-47 · DolphinAttack — DolphinAttack: Inaudible Voice Commands
- Zhang, G. et al., 2017 · Venue: ACM CCS 2017 (arXiv journal-ref) · Tier: T1 (via arXiv JREF; ACM DL not opened)
- Link: https://arxiv.org/abs/1708.09537
- Threat model: ultrasonic carrier (>20 kHz) exploits microphone non-linearity; attacker near the device.
- Key results (abstract): proof-of-concept incl. "manipulating the navigation system in an Audi automobile".
- How success is measured: recognition/command execution on devices.
- Automotive relevance: physical channel into any voice-fronted in-car agent; pre-LLM but still the acoustic baseline.
- Verification: ABSTRACT-ONLY.

### A-48 · Concurrent audio prompt injection — Piggybacking on Perception: Stealthy Concurrent Audio Prompt Injections against Multimodal LLM Agents
- Liu, M. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2607.28165
- Threat model: malicious audio instructions "piggyback" onto user speech in continuous-audio agents (instruction augmentation, scenario concealment); AudioAgentSecurity benchmark: 8 scenarios, 10 attack patterns, 11 agents.
- Key results (abstract): "average Attack Success Rate (ASR) of 69.10% against the advanced Gemini 3 Pro"; CADV defense "up to 96% detection accuracy"; real-world tests on Doubao AI Smartphone.
- How success is measured: **LLM judge as aid** — "We employ Qwen-Max as an auxiliary Judge to audit the agent's thought process and tool invocation traces, while recognizing that judge-model decisions can introduce semantic bias" in a sandboxed tool-trace environment (Sec. 5).
- Automotive relevance: cabin audio (radio, passengers, phone calls) is a concurrent-audio environment; the low-intelligibility attacks (Pulse, Spectral Inversion, Spectral Scramble, Noise Texture, Whisper) "are intended to model noisy outdoor or in-car environments" (Sec. 3); no vehicle deployment.
- Verification: PRIMARY-READ (Abstract, Sec. 3 attack families, Sec. 5 ASR definition).

### A-49 · Vehicle voice-command authorization — From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization
- Afroze, D. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2609.19630
- Threat model: not an attack paper; benchmark of the pre-action decision (execute / refuse / clarify / confirm / defer to manual / emergency / no tool) across speaker role, authentication, vehicle state. 202 scenarios.
- Key results (abstract): "Alignment ranges from 40.1% for Llama 3.2 3B to 89.1% for Gemini 3.1 Pro Preview"; "Even these models produce two to three False Executes among 161 non-execution scenarios".
- How success is measured: Decision Alignment against reference decisions (label match).
- Automotive relevance: defines the in-vehicle "unsafe action" target set an attack should aim at (False Execute).
- Verification: ABSTRACT-ONLY.

### A-50 · CAR-bench — CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty
- Kirmayr, J. et al., 2026 · Venue: ACL 2026 (Semantic Scholar venue; ACL Anthology `2026.acl-long.1886` per this repo's 16 Nov 2026 source audit) · Tier: T1
- Link: https://arxiv.org/abs/2601.22027
- Threat model: none (benign benchmark); 58 tools (navigation, productivity, charging, vehicle control), LLM-simulated user, policies.
- Key results (abstract): frontier models "less than 50% consistent pass rate on Disambiguation tasks".
- How success is measured: task completion with policy checks (not read here).
- Automotive relevance: the most suitable host environment for in-vehicle attack injection (add attacker-controlled fields to tool outputs).
- Verification: ABSTRACT-ONLY.

### Group 9 — Newer long-horizon IPI work found via forward citations of AgentLAB (Semantic Scholar)

### A-51 · ECLIPSE — ECLIPSE: Self-Evolving Stealthy Prompt Injection Attack against Long-Horizon Agentic Systems
- Zhao, S. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2608.30441
- Threat model: combines direct user-prompt injection with tool-side injection: sandbox-verified tool chains rendered as a natural one-shot prompt + Static Workflow Encoding in tool descriptions + Dynamic Trajectory Correction. LASE-Bench: 120 malicious tasks, 198 tools; "96.7% of its tasks make at least five tool calls".
- Key results (abstract): "up to 96.7% attack success without defense and 69.2% under the common safety filter, exceeding the strongest baseline by 27.5%".
- How success is measured: not read.
- Automotive relevance: hybrid user+tool attacker is plausible when a malicious app is installed and the user is socially engineered.
- Verification: ABSTRACT-ONLY.

### A-52 · Divide and Inject (AdaLCPI) — Divide and Inject: Can Agents Reconstruct an Indirect Prompt Injection from Fragments?
- Lee, M. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2609.36576
- Threat model: attack objective split into incomplete fragments across retrieved content + a reconstruction cue; refined with OpenEvolve using execution feedback.
- Key results (abstract): "61.4% macro-average ASR compared with 32.8% for Trojan Hippo-style and 30.0% for AgentVigil".
- How success is measured: not read ("graded scoring" used in search).
- Automotive relevance: fragments across several POI descriptions / messages over a drive.
- Verification: ABSTRACT-ONLY.

### A-53 · Staged prompt injection — Blocking at the Boundary: Auditing Long-Horizon Agents against Staged Prompt Injection
- Liu, J. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2610.05163
- Threat model: IPI that propagates across causally connected workflow stages and alters a consequential action while the workflow continues; automated feedback-guided generation against Claude Code and Codex in native runtimes; 8 scenarios, 7 goals, 6 surfaces.
- Key results (abstract): production agents "are vulnerable"; benchmark 479 pairs / 3,112 units; PAA auditor "86% Block recall at a 6-8% false-block rate" (defense side).
- How success is measured: confirmed attacks in native runtimes (details not read).
- Automotive relevance: frames the defense question as "audit before each consequential action", matching vehicle-function gating.
- Verification: ABSTRACT-ONLY.

### A-54 · Trust region effect — Where You Inject Matters: The Trust Region Effect in LLM Agents
- Guo, C. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2610.38867
- Threat model: same injection content, different placements across environment surfaces; learning-based attacker chooses content and placement.
- Key results (abstract): GPT-5.4 agent "follows an unsafe injection instruction placed in a repository documentation file (i.e., a README or TODO file) 2.6 times more often on average than the same instruction placed in a code or data file".
- How success is measured: not read.
- Automotive relevance: placement is an attack parameter: OEM-signed manual text vs user calendar vs third-party POI review likely receive different implicit trust.
- Verification: ABSTRACT-ONLY.

### A-55 · Delayed derived-action trap — Can agents whose sole duty is to keep humans alive be hijacked to kill? Delayed multi-turn derived-action trap attacks in simulated high-stakes environments
- Habdank, J. A., 2026 · Venue: arXiv (single author) · Tier: T3
- Link: https://arxiv.org/abs/2610.15153
- Threat model: delayed prompt injection appended to truthful telemetry in a NASA-derived BioSim lunar-habitat simulator; attacker cannot falsify sensors; must persuade and persist.
- Key results (abstract): qualitative per family: "Claude configurations mostly refuse life-support shutdown"; "Grok configurations, given the packet framed as a trusted commission, more often ... cut the life-support systems"; framing (trusted commission / peer / untrusted) changes potency.
- How success is measured: simulator state (life-support shutdown held) — inference from abstract.
- Automotive relevance: closest analogue to safety-critical vehicle control with telemetry-borne injection; small study.
- Verification: ABSTRACT-ONLY.

### Group 10 — Additional sources found during citation trails

### A-56 · MINJA under realistic memory — Memory Poisoning Attack and Defense on Memory Based LLM-Agents
- Sunil, B. D. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2601.05504
- Threat model: re-runs MINJA-style query-only memory injection on an EHR agent (MIMIC-III) while varying initial memory state, number of indication prompts and retrieval parameters; GPT-4o-mini, Gemini-2.0-Flash, Llama-3.1-8B.
- Key results (abstract): "realistic conditions with pre-existing legitimate memories dramatically reduce attack effectiveness"; restates MINJA as "over 95 % injection success rate and 70 % attack success rate under idealized conditions". Magnitude of the drop not in abstract.
- How success is measured: not read.
- Automotive relevance: an in-car memory after months of use is full of legitimate entries — the regime where this paper says MINJA weakens.
- Verification: ABSTRACT-ONLY.
- Inference: a direct counter-weight to A-16; cite both together.

### A-57 · Provider-side IPI in proactive agents — Who Is Your Agent Serving? Provider-Side Indirect Prompt Injection in Proactive Agents
- Wang, R. et al., 2026 · Venue: arXiv · Tier: T3
- Link: https://arxiv.org/abs/2610.05266
- Threat model: an external provider controls only content about its own target (e.g., its listing); no access to private user context, no extra permissions; strategies Target Control, Private Binding, Prospective Support.
- Key results (abstract): the full attack "increases target authorization in all tested environment-user-model combinations, with a macro gain of up to 77.4 percentage points" (3 environments, 6 simulated user models).
- How success is measured: target authorization by simulated users (details not read).
- Automotive relevance: very high — proactive in-car suggestions (charging stops, restaurants, parking) are provider-supplied; this is the commercial-manipulation variant of A-31.
- Verification: ABSTRACT-ONLY.

### A-58 · AgentVigil — AgentVigil: Generic Black-Box Red-teaming for Indirect Prompt Injection against LLM Agents
- Wang, Z. et al., 2025 · Venue: Findings of EMNLP 2025 (OpenReview record mirrors dblp `conf/EMNLP/2025`, title "AGENTVIGIL: Automatic Black-Box Red-teaming ..."; earlier name AgentFuzzer) · Tier: T1-claimed (ACL Anthology page not opened)
- Link: https://arxiv.org/abs/2505.05849
- Threat model: black-box fuzzing with seed corpus + MCTS seed selection.
- Key results (abstract): "71% and 70% success rates against agents based on o3-mini and GPT-4o" on AgentDojo and VWA-adv; real-world redirection of agents "to navigate to arbitrary URLs".
- How success is measured: AgentDojo / VWA-adv checks (inference from benchmark).
- Automotive relevance: baseline adaptive attacker used by later work (A-52 compares against it).
- Verification: ABSTRACT-ONLY.

### A-59 · BadRobot — BadRobot: Jailbreaking Embodied LLM Agents in the Physical World
- Zhang, H. et al., 2024 · Venue: ICLR 2025 (OpenReview `ICLR.cc/2025/Conference` poster; arXiv journal-ref) · Tier: T1
- Link: https://arxiv.org/abs/2407.20242
- Threat model: malicious user via "typical voice-based user-system interactions"; exploits (i) LLM manipulation, (ii) misalignment between linguistic outputs and physical actions, (iii) world-knowledge flaws.
- Key results (abstract): effective against Voxposer, Code as Policies, ProgPrompt; no numbers in abstract.
- How success is measured: not read.
- Automotive relevance: point (ii) — the model refuses in words but the action still executes — is a known failure mode to test in vehicle-function calls.
- Verification: ABSTRACT-ONLY.

### A-60 · Embodied-AI security survey — Towards Robust and Secure Embodied AI: A Survey on Vulnerabilities and Attacks
- Xing, W. et al., 2025 · Venue: ACM Computing Surveys (Semantic Scholar DOI 10.1145/3806048) · Tier: T2 (journal, via S2 DOI)
- Link: https://arxiv.org/abs/2502.13175
- Content (abstract): exogenous vs endogenous vulnerabilities in robots and autonomous vehicles; attacks on LVLM/LLM components "such as jailbreak attacks and instruction misinterpretation".
- How success is measured: n/a (survey).
- Automotive relevance: background framing for perception-channel attacks.
- Verification: ABSTRACT-ONLY.

---

## 4. Open problems & original ideas

Each idea names the closest existing work and why it is not yet covered. "Publishability" is my guess (Inference throughout this section).

1. **Ignition-cycle delayed-trigger memory poisoning conditioned on vehicle state.** Plant via a synced calendar invite, email or POI review in drive N; the payload fires only when a *vehicle-state* predicate holds (battery < 20%, highway, child seat occupied, night), not when a text trigger appears. Closest: CarryoverBench (A-19: Latent/Autonomous channels, text-triggered, desktop agent), MemGhost (A-21: one email, stealthy memory write), AgentPoison (A-15: trigger must be in the user query), Promptware (A-17: "thanks"-triggered tool call). New: the trigger lives in the physical/vehicle context, so text-level memory sanitisers and query-trigger detectors cannot see it; evaluation needs a state oracle over multiple sessions. Publishability: high (main-track security/NLP venue if the benchmark is released with rule-based verifiers).

2. **Instruction-free POI / charging-station tampering via safety framing.** Fabricated hazards ("charger at station X caught fire last week", "bridge closed for flooding") planted in reviews or provider feeds steer route and charger choice without any command. Closest: Voluntary Servitude (A-31: consumer-service recommendations, browser agents), task tampering (A-29: b(s)/b(O) primitives), provider-side IPI (A-57). New: the car agent's harm-avoidance is stronger and safety warnings have legitimate regulatory weight, and the effect is a physical route, measurable by a state oracle on the chosen destination. Publishability: high (strong automotive story, cheap to build on CAR-bench A-50).

3. **Parameter poisoning of vehicle-function arguments under physical bounds.** Keep the right tool (set climate, set charge limit, navigate, call contact) but move the argument within its legal range (e.g., charge limit 100% daily, destination 300 m off, contact swapped). Closest: Right Tool, Wrong Parameters (A-30), MCPTox P3 "parameter tampering" (A-24), task tampering b(A) (A-29). New: argument values that are individually valid and in-range defeat both allowlists and range checks; requires authority-flow reasoning tied to vehicle state. Publishability: medium-high (workshop quickly; main track with a defense comparison).

4. **Cockpit ↔ driving-domain hand-off hijack (multi-agent).** Untrusted text processed by an infotainment agent is summarised and handed to a planning/ADAS-adjacent agent (route advisory, ODD hints, comfort-vs-safety arbitration) where it is treated as trusted. Closest: Can CaMeLs Talk? (A-35: guarantees do not compose), MAS control-flow hijacking (A-34), FuncPoison (A-25: shared function library in driving MAS), AiTM (A-36). New: a domain boundary that is also a safety-integrity boundary (ASIL vs QM); provenance must survive summarisation. Publishability: high, but needs a credible two-domain testbed.

5. **Clarification-channel injection in multi-speaker cabins.** When the agent asks "Which charging station?" the answer can come from a passenger, a phone call on the speakers, or injected audio. Closest: ASPI (A-14: `ask_user` channel amplifies ASR, 1.8% → 34.0% for o3), concurrent audio injection (A-48: in-car-like noise), CAR-bench disambiguation tasks (A-50), From Intent to Action (A-49: speaker role/authentication). New: speaker identity and clarification state together; tests whether agents bind clarification answers to the authorised speaker. Publishability: medium-high.

6. **Staged-trust (rug-pull) third-party vehicle apps.** A connector (parking, charging, music) behaves benignly for N drives and defects after building reliance. Closest: TrustShiftProbe (A-27: MCP servers), MCPTox (A-24: static metadata), SkillRelayBench (A-23: cross-session artifacts). New: OEM app certification is a pre-deployment snapshot; temporal defection measured across ignition cycles with fleet-scale exposure. Publishability: medium (strong for an industry track or VehicleSec-type venue).

7. **Cross-modal fragmentation.** Split the payload across modalities that the agent fuses: half in a calendar entry, half on a roadside sign (camera), with a reconstruction cue in a POI description. Closest: cross-channel fragmentation (A-28: text channels of MCP), Divide and Inject (A-52: text fragments), CHAI (A-45: sign-only). New: no single modality contains an injection, so per-channel detectors (text classifiers, sign-text filters) are blind by construction. Publishability: high novelty; evaluation hard (needs a multimodal simulator or recorded drives).

8. **Fresh-session vs persistent-session robustness — resolving the protocol contradiction.** AgentLAB (A-01) shows ASR rising with turns; Adaptive Adversaries (A-05) shows a stateful defender lowering ASR (57.4% → 31.5%) and single-round scoring hiding risk (0–1% vs 7.9–16.8%). In cars, a "session" may be a drive, a day or a profile lifetime. A controlled study that varies session semantics while holding attacker budget fixed would settle which protocol the thesis should report. Publishability: medium-high as a measurement paper; directly useful for the Evaluate chapter.

9. **Untargeted distraction / denial-of-service measured in driver-attention terms.** An injection that makes the agent repeatedly ask for confirmation, read long text aloud or raise false warnings is harmless in AgentDojo terms (untargeted ASR, A-09 App. D) but hazardous while driving. Closest: AgentDojo untargeted DoS (A-09), WASP intermediate hijack (A-11). New: severity weighted by driving context (cf. counterfactual severity, A-18). Publishability: medium (strong human-factors angle; needs a driver-distraction proxy).

10. **Judge-independent scoring as an attack target.** Several headline numbers rely on LLM judges (A-01, A-02, A-31, A-48). An attack payload that also manipulates the judge (Carryover's warning that "a judge prompt is itself an injection surface", A-19 Sec. 3.2; A-38 Lesson #4) inflates or hides ASR. Measuring judge-vs-oracle disagreement under adversarial traces on an in-vehicle benchmark is both an attack and an evaluation contribution. Publishability: medium-high; links the Attack and Evaluate chapters.

---

## 5. Registry rows

(Pending — written at the end of the survey.)
