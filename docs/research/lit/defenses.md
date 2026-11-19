# Defences for LLM agents + transferable ideas from neighbouring fields

Survey for the thesis "Robustness of agentic AI to adversarial attacks — an adversarial-example pipeline for long-horizon tasks, evaluating in-vehicle LLM agents across agent architectures" (Attack → Evaluate → **Defense**).
Compiled 18 Nov 2026. Status: v1 (written incrementally; sections marked *pending* are still being verified).

**How to read the labels.**
- Tier: T1 = peer-reviewed top venue; T2 = peer-reviewed workshop / journal / standard / second-tier conference; T3 = arXiv / tech report / official lab research; T4 = blog / talk / GitHub. "(claimed)" = acceptance stated only by the authors (arXiv comment or camera-ready header), not confirmed on the venue's own site.
- Verification: PRIMARY-READ = I downloaded the PDF (`pdftotext -layout`) and read the passages the numbers come from; ABSTRACT-ONLY = arXiv abstract page (or OpenReview/ACL abstract) only; UNVERIFIED = I could not open a primary text.
- "Inference:" = my reasoning, not a claim of the source.
- Adaptive? = was the defence evaluated against an attacker that optimises against *this* defence (yes / partial / no). Long-horizon? = evaluated against attacks spread over many turns/steps or staged across tool outputs (yes / partial / no). "Self" vs "third-party" says who ran the evaluation.
- All arXiv metadata (title, authors, dates, comments) was read from the arXiv abstract pages on 18 Nov 2026. Several 2026 papers cite fictional-sounding model names (e.g., "GPT-5.6-Luna", "Claude Fable 5", "Qwen3.6-27B"); these are reproduced exactly as printed in the papers.

---

## 1. Area summary (≤400 words)

**Solved (in a narrow sense).** For *instruction injection that must create a new tool call*, deterministic out-of-band enforcement works on today's benchmarks: CaMeL (D-01), FIDES (D-06), SPIDES (D-07), ROPE (D-09), SPILLWAY (D-10) and Progent (D-08) all drive static ASR to ≈0–3%, and the only independent black-box adaptive attack run against several of them (AutoDojo, D-19) barely moved CaMeL/ROPE/Progent. Detectors and fine-tuned models do *not* have this property: every one tested adaptively was broken (D-44: >90% ASR on most of 12 defences; MELON 95%, Meta-SecAlign 96%, PIGuard 71%).

**Open.** (1) *Utility*: the security comes from refusing data-dependent tasks. CaMeL's own 77% vs 84% (D-01) becomes 26–53% clean utility vs 63–90% undefended in third-party AutoDojo runs (D-19, Table 5); LeanGuard's read-only deployment drops benign success 53.1%→12.5% (D-22). (2) *Residual attack classes outside the threat model*: side channels (D-01 §7), branch steering of pre-approved branches (D-03, D-05), parameter poisoning with legitimate values (D-11), agent-data injection that spoofs trusted metadata (D-46), composition across agents (D-04), errors at the provenance/extraction step (D-06/D-45). (3) *Long horizon*: only ShadowMem (D-36), ROPE (D-09) and PAA (D-38) evaluate staged/multi-turn attacks; ROPE's replay of AgentLAB shows Progent admitting 8–15% (up to 43.5%) and DRIFT up to 25.4% (D-09 Table 3) — "near-zero" single-turn defences leak over long horizons. (4) *Human-in-the-loop cost*: every deterministic system escalates to user approval; only SPIDES/Kolluri (D-07, D-20) measure approvals (1.84 per completed task), nobody measures it under driving workload.

**Overhyped.** (a) Benchmark scores of injection detectors: AgentDojo-vs-BIPIA rankings do not transfer (D-33), base-rate effects make AUROC 0.88–0.93 detectors mostly false alarms at 2% attack prevalence (D-32). (b) "Provable" model-level defences: Meta-SecAlign 1.9% static → 78.8–96% adaptive (D-39, D-41, D-44); SecPO/SecOPD (D-41/D-42) are the first to stay ≈9% under adaptive attack, but only on short-horizon tasks. (c) "No adaptive evaluation needed for system-level defences": AMS explicitly *skipped* CaMeL/Tool Filter/IPIGuard (D-44 App.), so the claim rests on AutoDojo (black-box, success-bit feedback) and a one-template reproduction on Progent (D-18) — no white-box, human red-team or long-horizon adaptive test of CaMeL exists in what I found.

**Automotive reading.** The neighbouring fields (Section 3) all say the same thing: the learned component must never be the last safety authority — a simple, verified monitor (reference monitor / shield / Simplex / ASIL-decomposed checker) gates every actuation. The thesis gap is to test such a gate against *adaptive, long-horizon* attacks *and* to price its confirmations in driver-distraction terms.

---

## 2. Defence matrix

Layer: P = prompt, D = detection, M = model, S = system/architecture, T = trajectory. Det.? = is the final allow/deny decision deterministic (not an LLM/classifier)? Utility numbers are clean or under-attack task success as reported; "self" = authors' own numbers.

| ID | Defence | Layer | Det.? | Adaptive-evaluated? | Long-horizon-evaluated? | Utility cost (number + source) | Residual weakness |
|---|---|---|---|---|---|---|---|
| D-01 | CaMeL | S | yes (interpreter + capability policies) | partial — third-party black-box AutoDojo: ASR ≤1.8% (D-19 T5); AMS skipped it (D-44 App.) | no | self 77% vs 84% (abstract); third-party clean util. 66.7→26.3 (GPT-4o-mini), 70.2→40.4 (Claude-Haiku-4.5) (D-19 T5); −21.6 pts avg in MultiAgentDojo (D-04); parameter poisoning BU 90.28→43.75 at 0.69% ASR (D-11 T1) | side channels (§7); "data requires action" tasks unsolvable; policies hand-written; confirmations on violation |
| D-02 | Design Patterns (6 patterns) | S | yes (by construction) | no (design paper) | no | qualitative only (case studies) | restricts generality by design |
| D-03 | NOVA / CaMeL-NOVA (CUA) | S | yes (single-shot branching plan) | partial — branch-steering attacks by authors | no | "retain up to 57%" of frontier performance (abstract); 1.88× tokens (§4) | branch steering: pixel attack evades strongest redundancy defence (§4) |
| D-04 | multi-CaMeL | S | yes | no (one constructed attack) | no (multi-agent, not multi-turn) | +3.2 pts over individual CaMeL; CaMeL itself −21.6 pts avg (results §) | provenance only as good as protocol adoption by every agent |
| D-05 | COBRA (branch-steering defence) | S | yes (ahead-of-time capability bounds) | partial (STEER-Bench attacks) | no | 97% benign utility retained (abstract) | bounded by plan coverage; workshop paper |
| D-06 | FIDES (MSR IFC planner) | S | yes (label checks at sinks) | no | no | with policies: drop "up to 24.5 %" (o3, o4-mini) (§8.2) | text-to-text attacks not covered; labels default to trusted if forgotten (D-18 §8.2) |
| D-07 | SPIDES (IFC for browser agents) | S | yes | partial — Byzantine model-output adversary (worst case), not optimisation | no | 1.84 HITL approvals per completed task (§6); TCR@k metric | needs operator element labels; same-origin reader granularity (§7) |
| D-08 | Progent | S | yes (symbolic rules; LLM writes policy) | partial — self: 3 templates + AgentVigil (App. E, max 4.2%); third-party AutoDojo ≤7.7% (D-19); D-18 repro 2.6% | yes, third-party: AgentLAB replay 8.7/8.3/15.1% overall, up to 43.5% (D-09 T3) | AutoDojo: "up to 7 points" (D-19 §4.2); SPILLWAY grid BU .540→.437 (D-10 T2) | LLM-generated policy is the attack surface; expansion approvals |
| D-09 | ROPE | S | yes (origin check) | yes (self, AutoDojo) | yes (self, AgentLAB Task-Injection: 0.0%) | retains 82–100% of clean utility (abstract) | self-evaluated only; audited parameter set must be complete |
| D-10 | SPILLWAY | S | yes (typed-target floor) + LLM judge | partial — PISmith replayed open-loop .005; AutoDojo replay | no | BU .539 vs .540 undefended (T2) | only identity targets; legitimate-identity steering left to judge (§7) |
| D-11 | AuthorityFlow | S/D | mixed (LLM trust hierarchy + flow tracing) | no | no | 90.28%→82.64% benign utility (abstract, T1) | trust hierarchy itself LLM-built; 9.03% residual ASR |
| D-12 | IsolateGPT | S | yes (hub/spoke isolation) | no | no | overhead "<30% for three-quarters of tested queries" (abstract) | ACE (D-14) shows planning-integrity attacks on it |
| D-13 | f-secure LLM | S | yes (IFC security monitor) | no | no | not quantified in abstract | — (ABSTRACT-ONLY) |
| D-14 | RTBAS / ACE / PFI / IPIGuard / DRIFT (cluster) | S | mixed | DRIFT: third-party AutoDojo doubles ASR (D-19) | DRIFT/PFI: third-party AgentLAB replay — DRIFT up to 25.4%, PFI 0–9.1% at CU 36.8–47.4 (D-09 T3) | DRIFT CU −18/−25 pts (D-19); IPIGuard BU −5.4/−8.1 pts (D-36 T5); RTBAS "2% loss" (abstract) | learned judges inside the loop (DRIFT, RTBAS) are adaptive-attack surface |
| D-15 | Tool filter (AgentDojo baseline) | S | yes (tool allow-list per task) | no | yes, third-party (D-09 T3: 0–4.8%) | Gemini clean util. 13.2 in D-09 T3 | coarse: blocks whole tools |
| D-18 | (Evaluation) out-of-band adaptive protocol | — | — | yes (Progent only, 1 template, Qwen2.5-7B) | no | — | single weak model |
| D-19 | (Evaluation) AutoDojo | — | — | yes (black-box, success-bit) on 10 defences | no | — | no white-box / human attacker |
| D-20 | Autonomy metric / PRUDENTIA (Kolluri et al.) | S | yes (IFC base) | no | no | HITL load 48.2 → 32.4 (Basic-IFC) → 18.8 (FIDES), o3-mini (§4) | ideal-approver assumption; no driver workload |
| D-21 | MiniScope | S | yes (permission hierarchy) | no | no | confirmations −43.4% to −89.4% (abstract) | simulated personas |
| D-22 | LeanGuard (Lean4 tool-call policies) | S | yes (proved-equivalent past-time LTL check) | no | partial (temporal rules over history; multi-turn attack "not yet reproduced", T6) | τ²: 72.7→68.9 (70.9 w/ feedback); DTap read-only: benign 53.1→12.5 (T1) | policy completeness; read-only deployment blocks benign writes |
| D-23 | NOMOS (policy compiler) | S | yes | no | no | "domain-dependent benign-utility cost" (abstract) | ABSTRACT-ONLY |
| D-24 | AgentSpec (runtime DSL; AV domain) | S | yes | no | no | "overheads in milliseconds" (abstract) | rules hand-written / LLM-generated (recall 70.96%) |
| D-25 | ShieldAgent | D/T | partly (rule circuits + LLM) | no | partial (action trajectories) | n/a | probabilistic rule circuits |
| D-26 | Llama Guard | D | no (LLM classifier) | no | no | n/a | content-safety, not injection |
| D-27 | LlamaFirewall (PromptGuard 2, AlignmentCheck) | D/T | no | third-party: PromptGuard >90% ASR (D-44); AlignmentCheck precision 0.096 at 2% prevalence (D-32) | no | n/a | AlignmentCheck "still experimental" (abstract) |
| D-28 | PIGuard / InjecGuard | D | no | third-party: 71% ASR (D-44); 0.0→28.0% (D-19) | no | AutoDojo CU 66.7→43.9 on GPT-4o-mini (D-19 T5) | over-defence vs. under-detection trade |
| D-29 | DataSentinel | D | no | self (minimax-trained); third-party broken (D-44: "In every case, the defense was bypassed") | no | n/a | task-redefinition attacks |
| D-30 | MELON | D/T | no (re-execution + similarity) | third-party: 76% / 95% ASR (D-44) | third-party: PI2 multi-turn avg ASR 42.1% on Llama-3.3 (D-36 T5); AgentLAB 0–0.4% but UA 13.9–26.8 (D-09 T3) | BU −5.4/−9.8 pts (D-36 T5); 2 runs per step | conditional ("if summarising…") injections |
| D-31 | Task Shield | D/T | no (LLM alignment check) | no (authors list "susceptibility to adaptive attacks") | no | UA 69.79% vs 50.08% undefended, GPT-4o (T1) | LLM checker reads attacker text |
| D-32 | (Evaluation) Detectors of hijacked agents | — | — | — | — | — | base-rate, unseen tools, benchmark transfer |
| D-33 | (Evaluation) Passing the Test You Trained On | — | — | — | — | FPR on clean tool outputs "from none to over 90%" | rankings do not transfer |
| D-34 | Hidden-state probes + probe-gated reasoning | D (white-box) | no | yes (self: search-based + anti-encoding, AUROC ≥0.956) | partial (multi-turn agent traces) | "better preserves clean-task utility than the baselines" (abstract) | needs activations; open models only |
| D-35 | Guardrail DoS (attack on D-layer) | — | — | — | — | 13–63× token, up to 148× latency amplification | availability of reasoning guards |
| D-36 | ShadowMem (v1 title: MAGE) | T | no (trained memory + judge) | yes (self: up to 25.0% with frontier harness reading memory+feedback, T4) | yes (PI2, STAC; avg 4.43 turns) | "below 3%" BU loss; ≈3K tokens/task (T5) | claims the trajectory cannot contradict |
| D-37 | TRACE | T | no | no | yes (offline detection on long trajectories) | n/a (detector) | offline judge only |
| D-38 | PAA / Blocking at the Boundary | T | no (LLM attribution, verbatim-quote checks) | no ("we do not study online-adaptive or auditor-targeted attacks") | yes (staged injection in Claude Code/Codex) | 6–8% false-block rate at 86% recall (abstract) | model stages read attacker text |
| D-39 | Meta-SecAlign | M | no | third-party broken: 96% (D-44), 78.8% ASR@800 (D-42 T2) | no | AgentDojo util. 59.8%→84.5% (T4) | DPO anchored on insecure reference (D-42) |
| D-40 | StruQ / SecAlign / Instruction Hierarchy | M | no | StruQ broken "in every case we tested" (D-44); IH: GPT-4o-mini vulnerable to 276 AgentDojo attacks (D-01 §6.3) | no | SecAlign "significant utility degradation" in agentic tasks (D-39 abstract) | train-test attack gap |
| D-41 | SecOPD | M | no | yes (self, PISmith: 9.0%) | no | not in abstract | single-turn-trained |
| D-42 | SecPO + adversarial training | M | no | yes (self: Genetic/TAP/PISmith/AMS; 8.8% ASR@800 AgentDojo) | no | AgentDojo util. 90.7% vs 89.7% undefended (T2) | still ~9–13% adaptive ASR |
| D-43 | ASIDE | M | no | no | no | "without performance loss" (abstract) | ABSTRACT-ONLY |
| D-45 | Signed requirement manifests (multi-agent handoff) | S | yes (verifier) | partial (pre-signing injection test) | no | "no detectable utility loss" vs structured (Qwen3-8B) | extraction before signing is the trust boundary |
| D-47 | Stateful cooperative defenders (EMRA) | T (chat) | no | partial ("evolving" multi-turn attacks) | yes (multi-turn chat, not tool agents) | n/a | evaluates jailbreak-style chat, not tool use |

*Rows D-16/D-17 are folded into D-14 (cluster).*

---

## 3. Transferable ideas from neighbouring fields

Verification key for this section: **V-DBLP** = bibliographic record confirmed via Semantic Scholar API (which returns the DBLP key / journal volume and pages); **V-site** = confirmed on the publisher/venue site; **V-arXiv** = arXiv abstract page read; **V-catalog** = only library/standards catalogue entries seen via web search (full text not opened); **UNVERIFIED** = details from my own knowledge, not confirmed in this session. dl.acm.org, iso.org, nhtsa.gov and regulations.justia.com were not reachable from this environment (Cloudflare challenge / proxy refusal), so ISO and NHTSA texts could not be opened.

| # | Idea (one line) | Canonical source · tier · verification | Concrete in-vehicle agent design | Experiment that would test it |
|---|---|---|---|---|
| N1 | **Confused deputy**: a program holding authority A is tricked by a caller into using A for the caller's purpose; the cure is to make authority travel with the request (capabilities) instead of being ambient. | Hardy, N. 1988, "The Confused Deputy: (or why capabilities might have been invented)", ACM SIGOPS Operating Systems Review 22, pp. 36–38 · T2 (non-refereed newsletter, canonical) · V-DBLP (`journals/sigops/Hardy88`). | The assistant holds ambient vehicle authority (unlock, route, pay, call). An inbound SMS/e-mail/POI review is a "caller". Bind every consequential call to the *originator* of each argument: a value that originated in an inbound message cannot by itself authorise an action on the driver's behalf. | Attack set where injected content requests actions the driver *could* legitimately do (navigate, call, pay). Compare ASR of ambient-authority agent vs originator-bound gate (O1). |
| N2 | **Capabilities / object capabilities**: authority = an unforgeable reference passed explicitly; no ambient authority. | Dennis & Van Horn 1966, "Programming semantics for multiprogrammed computations", CACM 9(3) · T1 · *V-DBLP pending*; Miller, M.S. 2006, "Robust Composition" (PhD thesis, Johns Hopkins) · T3 · UNVERIFIED. | Tools take capability handles minted only by trusted components: `call(contact_handle)` where the handle comes from the address book; `navigate(poi_handle)` from the OEM POI service. Strings from untrusted text cannot be turned into handles. This is the mechanism under CaMeL (D-01), ROPE (D-09), SPILLWAY (D-10). | Agent-data-injection (D-46)-style spoofing: forged "[Contacts]" blocks in a message. Compare string-argument gate vs handle-based gate. |
| N3 | **Reference monitor / complete mediation**: every access is checked by a mechanism that is always invoked, tamper-proof and small enough to verify; plus least privilege, fail-safe defaults, economy of mechanism. | Anderson, J.P. 1972, "Computer Security Technology Planning Study", ESD-TR-73-51 (2 vols, DTIC AD-758 206 / AD-772 806) · T3 · V-catalog (DTIC listing via web search); Saltzer & Schroeder 1975, "The Protection of Information in Computer Systems", Proc. IEEE 63(9) · T1 · *V-DBLP pending*. | One gate between LLM and the vehicle API gateway; no tool reaches the bus except through it; gate is a few hundred lines of rule code, separately tested, outside the LLM process; default deny for unknown tools (fail-safe defaults). | Coverage audit (share of vehicle-API calls that bypass the gate) + fault injection on the gate + attempts to reach actuation through "convenience" tools (e.g., a scripting tool). |
| N4 | **Information-flow control, lattice labels, decentralized labels; integrity (Biba) as the dual of confidentiality.** | Denning, D. 1976, "A lattice model of secure information flow", CACM 19, pp. 236–243 · T1 · V-DBLP (`journals/cacm/Denning76`); Myers & Liskov 1997, "A decentralized model for information flow control", SOSP '97 · T1 · V-DBLP (`conf/sosp/MyersL97`); Biba 1977 integrity model (MITRE TR) · T3 · UNVERIFIED (its use for agents is summarised in D-18 Fig. 2, PRIMARY-READ). | Integrity labels: `driver_voice` > `oem_trusted` > `third_party_typed` > `free_text_untrusted`. Low-integrity data may be *read out* but may not choose a consequential action or its target without endorsement (driver utterance or trusted channel). Confidentiality labels protect location/contacts from flowing to third-party tools. | Measure the share of in-vehicle tasks that are *data-dependent* (need low-integrity data in control flow); that share predicts the utility loss of IFC (cf. "data requires action", D-01; DI/DIQ task taxonomy, D-06). |
| N5 | **Enforceable security policies = safety properties over execution traces (security automata); past-time temporal-logic monitors.** | Schneider, F.B. 2000, "Enforceable security policies", ACM TISSEC 3(1) · T1 · *V-DBLP pending*; Bauer, Leucker, Schallhart 2011, "Runtime verification for LTL and TLTL", ACM TOSEM · T1 · *V-DBLP pending*. LLM-agent instance: LeanGuard (D-22, PRIMARY-READ) checks past-time temporal rules over the tool history. | Write hazards as past-time rules over the agent's trace and vehicle signals: "`unlock_doors` only if the most recent driver utterance requested it ∧ speed = 0 ∧ no inbound message mentioned unlocking in the last N turns". | Port 20–30 STPA-derived rules (N8) to a monitor; measure blocked-benign rate on replayed benign drives and ASR on staged attacks; latency per decision. |
| N6 | **Safety shield for learning agents; runtime assurance (Simplex)**: a synthesized, verified component either restricts the learner's action set ("preemptive shield") or corrects only unsafe actions ("post-posed shield"); Simplex switches to a verified simple controller. | Alshiekh, M. et al. "Safe Reinforcement Learning via Shielding", AAAI 2018 (arXiv 1708.08611) · T1 · V-arXiv (abstract read: shield "monitors the actions from the learner and corrects them only if the chosen action causes a violation of the specification"); AAAI venue: ojs.aaai.org page reached a bot wall → *venue V-DBLP pending*. Sha, L. 2001, "Using simplicity to control complexity", IEEE Software · T2 · *V-DBLP pending*. | Preemptive shield = the gate exposes only actions that are safe in the current vehicle state (the LLM never sees "open trunk" at 80 km/h). Post-posed shield = the gate corrects (e.g., clamps window opening). Simplex = fallback to a fixed voice-command grammar if the LLM stack misbehaves or its guard is DoS'd (D-35). | Compare preemptive vs post-posed shielding on task success and ASR; availability test under guard-DoS payloads with/without Simplex fallback. |
| N7 | **Control barrier functions**: a minimally invasive safety filter projects a nominal command onto the safe set instead of rejecting it. | Ames, A.D. et al. 2019, "Control Barrier Functions: Theory and Applications" (arXiv 1903.11199; published at ECC 2019 — venue *UNVERIFIED*) · T2 · V-arXiv. | For continuous comfort actuators (windows, sunroof, seat motion, volume, HVAC), "project" the LLM's request to the nearest safe value given speed/occupancy rather than deny, reducing confirmations. | Block-vs-project comparison: task success, number of driver confirmations, and whether attackers can exploit projection (e.g., many small steps). |
| N8 | **STPA**: hazards arise from unsafe control actions (UCAs) in a control structure, not only from component failures; UCAs are "provided", "not provided", "wrong timing/order", "too long/too short". | Leveson, N.G. 2011, "Engineering a Safer World: Systems Thinking Applied to Safety", MIT Press (open access, DOI 10.7551/mitpress/8179.001.0001; ch. 8 "STPA") · T2 (book) · V-catalog (DOAB/OAPEN records). Automotive application: Abdulkhaleq, A. et al. 2017, "Using STPA in Compliance with ISO 26262 for Developing a Safe Architecture for Fully Automated Vehicles" (arXiv 1703.03657; "24 system-level accidents, 176 hazards, 27 unsafe control actions") · T2 (claimed proceedings) · V-arXiv. LLM-agent application: Doshi, A. et al. 2026, "Towards Verifiably Safe Tool Use for LLM Agents", ICSE NIER 2026 (claimed) · T2 · V-arXiv (2601.08012: STPA → "enforceable specifications on data flows and tool sequences"). | Model the agent as a controller over vehicle subsystems (HVAC, body, infotainment, navigation, charging/payment) and the driver; derive UCAs; compile to gate rules (O5). | Coverage: fraction of thesis attack goals that violate ≥1 UCA-derived rule; compare with benchmark-derived policies (Progent/NOMOS). |
| N9 | **ASIL decomposition / freedom from interference**: a safety requirement can be split over sufficiently independent elements so a lower-integrity element is never the sole safety authority. | ISO 26262-9:2018 (Road vehicles — Functional safety — Part 9: ASIL-oriented and safety-oriented analyses; clause 5 "requirements decomposition with respect to ASIL tailoring") · T2 (standard) · V-catalog (iso.org standard 68391 listing via web search; full text not opened). ISO/PAS 8800:2024 (Road vehicles — Safety and artificial intelligence, Dec 2024) · T2 · V-catalog (iso.org 83303 listing via web search). | LLM planner developed as QM; the deterministic gate (O1) and vehicle-state source carry the safety requirement; independence argued (separate process/ECU, no shared labels produced by the LLM). The LLM is never the last safety authority. | Dependent-failure analysis: inject faults where the gate consumes LLM-produced labels (the "extraction is the trust boundary" failure of D-45) and show whether independence holds. |
| N10 | **Warning/confirmation fatigue and driver-distraction budgets**: users click through many warnings; in cars, visual-manual interaction has hard glance limits. | Akhawe, D., Porter Felt, A. 2013, "Alice in Warningland: A Large-Scale Field Study of Browser Security Warning Effectiveness", USENIX Security 2013 · T1 · V-site (usenix.org; abstract: "users continued through 70.2% of Google Chrome’s SSL warnings"). NHTSA 2013, "Visual-Manual NHTSA Driver Distraction Guidelines for In-Vehicle Electronic Devices", Federal Register notice 2013-09883 (78 FR 24817–24890), non-binding · T2 (government guideline) · UNVERIFIED primary (not reachable); web-search snippets report single glances ≤2 s and total eyes-off-road ≤12 s per testable task. | Confirmation budget (O3): no visual confirmations in motion; voice-only, at most k per drive for non-urgent actions; defer to stops; design so that a confirmation never requires reading attacker-controlled text. | Driving-simulator or desk study: approvals per 10 min, approval accuracy when one of the approval requests is malicious, glance metrics against the NHTSA criteria. |

---

## 4. Entries

### D-01 · CaMeL — Defeating Prompt Injections by Design
- Debenedetti, E. et al. (Google DeepMind, ETH), 2025 · IEEE SaTML 2026 · Tier: T2 (peer-reviewed IEEE conference; arguably T1) — verified via Semantic Scholar record: DBLP key `conf/satml/DebenedettiSFHCFKSTT26`, DOI 10.1109/SaTML68715.2026.00040.
- https://arxiv.org/abs/2503.18813 (v2, 24 Jun 2025)
- Mechanism: A privileged LLM (P-LLM) sees only the trusted user query and writes a program in a Python subset; a quarantined LLM (Q-LLM) parses untrusted data but cannot call tools. A custom interpreter tracks data-flow dependencies and capabilities on every value and checks security policies before each tool call.
- Results: "solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo" (abstract). Tokens: "CaMeL requires only 2.82× more input and 2.73× more output tokens than native tool-calling" (Fig. 13). Policy violations in deployment "will not be blocked, but they will require user confirmation" (§5). Limitation: "We find that CaMeL is vulnerable to side-channel attacks" (§7); "No, prompt injection attacks are not fully solved." (§9.3). Failure mode "Data requires action": the P-LLM "cannot write a plan based on data it can’t read" (§6.1.2).
- Third-party utility cost (D-19, AutoDojo Table 5, clean utility undefended → CaMeL): GPT-4o-mini 66.7→26.3; GPT-5.4-mini 77.2→52.6; Gemini-2.5-Flash 63.2→28.1; DeepSeek-v4-Flash 89.5→38.6; Claude-Haiku-4.5 70.2→40.4. "CaMeL, being the most effective defense overall, incurs the largest clean utility cost on four of the five models." (D-19 §4.2). In MultiAgentDojo, "individual CaMeL reduces utility relative to the no-CaMeL baseline for every model, with an average reduction of 21.6 points" (D-04).
- Adaptive attacker? partial. AMS (D-44) explicitly skipped it: "We skip “plan-then-execute” defenses, such as Tool Filter, CaMeL ..., IPIGuard ..., because the attack is guaranteed to fail in most of the selected scenarios" (D-44 App.). AutoDojo's black-box adaptive attack left CaMeL ASR at 0.0–1.8% (D-19 Table 5). No white-box or human red-team evaluation found. Long-horizon? no (AgentDojo only; not run in ROPE's AgentLAB replay).
- Automotive fit: strong conceptual fit for actuation (unlock/route/pay) because the control flow is fixed by the driver's utterance. Poor fit for "read my messages and do what they say" style tasks (data-requires-action) and for latency (two LLMs, ≈2.8× tokens).
- Verification: PRIMARY-READ (abstract, §5–7, §9.3, Fig. 9/13).
- Third-party on parameter poisoning (D-11 Table 1, Qwen3.6-27B): CaMeL (policies) BU 43.75% vs 90.28% undefended, ASR 0.69% vs 93.06%.
- Inference: the 77-vs-84 headline understates utility loss with smaller/cheaper models that an embedded car stack would use (third-party 26–53%).

### D-02 · Design Patterns — Design Patterns for Securing LLM Agents against Prompt Injections
- Beurer-Kellner, L. et al. (incl. Debenedetti, Tramèr), 2025 · arXiv · Tier: T3 (Semantic Scholar lists venue arXiv.org; no proceedings found).
- https://arxiv.org/abs/2506.08837
- Mechanism: Six patterns that trade generality for provable resistance: action-selector (no feedback from tools), plan-then-execute (fixed action list), LLM map-reduce (isolated per-document sub-LLMs), dual LLM (privileged vs quarantined), code-then-execute (CaMeL-style program), context-minimization (drop the user prompt before answering from untrusted data). Ten case studies (OS assistant, SQL agent, email/calendar, booking, …).
- Results: no numbers; key principle quote (§3): "once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions". Plan-then-execute "acts as a form of “control flow integrity” protection" but "does not prevent all prompt injections" (§3.1).
- Adaptive? no (design paper). Long-horizon? no.
- Automotive fit: very high as a vocabulary. In-car commands are mostly action-selector or plan-then-execute; message summarisation fits map-reduce; route-from-email fits dual LLM.
- Verification: PRIMARY-READ (§3, §4 headings, Table 1 case-study list).
- Inference: a thesis can classify each in-vehicle tool into one pattern and report what share of the task suite each pattern can solve.

### D-03 · NOVA — CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents
- Foerster, H. et al. (incl. Shumailov, Papernot, Tramèr), 2026 · arXiv (v3 4 Jun 2026) · Tier: T3.
- https://arxiv.org/abs/2601.09923
- Mechanism: Single-shot planning: a trusted planner emits a complete *branching* plan up front; a perception model (Q-VLM) only resolves runtime values (coordinates, which branch). Gives control-flow integrity for GUI agents.
- Results: "retain up to 57% of the performance of frontier models while improving performance for smaller open-source models by up to 19%" (abstract). "CaMeL-NOVA adds 1.88× tokens over the undefended agent, while Fides-NOVA adds 29.6×" (§4). Branch steering: "even under our strongest redundancy defense (Multi-Modal Consensus) ... the pixel attack evades both screenshot-based and DOM-enhanced Q-VLM verification" (§4).
- Adaptive? partial (authors' own branch-steering attacks). Long-horizon? no.
- Automotive fit: in-car UIs (HMI screens, apps) are structurally predictable like OSWorld; branch steering maps to spoofed POI/charging-station data choosing a pre-approved but attacker-preferred branch.
- Verification: PRIMARY-READ (abstract, §4, §5).
- Inference: branch steering is the CaMeL analogue of ROP (D-01 §9.3 makes that analogy itself).

### D-04 · multi-CaMeL — Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks
- Peters-Gill, J. et al. (incl. Shumailov, Schroeder de Witt), 2026 · arXiv preprint · Tier: T3.
- https://arxiv.org/abs/2610.05640
- Mechanism: Shows CaMeL is not compositional when agents call agents as tools ("boundary laundering": untrusted data returned by a sub-agent becomes trusted input of the parent). multi-CaMeL adds a separate data channel that carries provenance across agent boundaries.
- Results: "We find that CaMeL's guarantees do not compose." (abstract). "multi-CaMeL reduces attack success rate (ASR) to 0.0%, compared with 0.2% for individual-agent CaMeL and 12.9% with no CaMeL" (abstract). Utility: individual CaMeL "average reduction of 21.6 points across all models and 13.4 points across the two strongest models"; multi-CaMeL adds "3.2 points on average across all models and 0.85 points across the two strongest models" (results §, MultiAgentDojo).
- Adaptive? no. Long-horizon? no (hierarchical, not multi-turn).
- Automotive fit: in-vehicle stacks are becoming multi-agent (OEM assistant → third-party app agents → cloud agents); provenance must survive each hop.
- Verification: PRIMARY-READ (abstract, contributions, utility results).
- Inference: any thesis architecture comparison (single vs multi-agent) must test composition explicitly.

### D-05 · COBRA — Securing Computer-Use Agents Against Branch Steering Attacks
- Zingrillo, G. et al. (incl. Foerster, Shumailov), 2026 · NeurIPS 2026 "Agents in the Wild" workshop (claimed, arXiv comment) · Tier: T2 (claimed).
- https://arxiv.org/abs/2610.03089
- Mechanism: Pairs trusted branching plans with ahead-of-time capability constraints that bound the parameters and destinations each branch may use.
- Results: STEER-Bench (101 tasks, 9 domains): "high attack success against both standard (94.4%) and vanilla Dual-LLM (89.5%) CUAs"; "COBRA reduces attack success to 0% while retaining 97% benign utility" (abstract).
- Adaptive? partial (benchmark of branch-steering attacks; no optimisation against COBRA reported in abstract). Long-horizon? no.
- Automotive fit: bounding destinations per branch = whitelisting navigation targets/payees per plan step.
- Verification: ABSTRACT-ONLY.

### D-06 · FIDES — Securing AI Agents with Information-Flow Control
- Costa, M. et al. (Microsoft Research), 2025 · arXiv · Tier: T3.
- https://arxiv.org/abs/2505.23643
- Mechanism: Formal model of agent planners; dynamic taint tracking of confidentiality and integrity labels; deterministic policy checks at tool sinks; primitives to hide information from the planner (query-LLM on hidden variables). Characterises which properties dynamic taint tracking can enforce.
- Results: "Without policy enforcement, many attacks succeed against the Basic planner, for instance 156 using gpt-4o. In comparison, FIDES only allows 23 injections" (§8.1); "With policy checks, it blocks all attacks that violate P" (Finding 1). Utility: Basic planner drops "by up to 40 % for gpt-4o"; FIDES drop "mainly affects the reasoning models, by up to 24.5 % for o3 and o4-mini" (§8.2). Text-to-text attacks are not stopped: "Since we only enforce policies upon tool calls, our planners do not stop these text-to-text attacks" (§8.1).
- Adaptive? no. Long-horizon? no.
- Automotive fit: label lattice maps well to driver-voice (high integrity) vs. messages/web (low). Text-to-text gap matters in a car: a spoken misleading answer ("the bridge is closed, take exit 12") is a safety issue even without a tool call.
- Verification: PRIMARY-READ (§8.1–8.2).

### D-07 · SPIDES — Information-Flow Control for Browser Agents
- Zverev, E. et al. (Microsoft; Köpf, Zanella-Béguelin), 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2610.24277
- Mechanism: Gates primitive browser actions (type, click, navigate) on labels propagated from element-level HTML confidentiality/integrity annotations; untrusted/confidential content is masked from the agent; a revealed value taints the context and triggers approval for consequential actions.
- Results: 0% ASR "by design" on MicroNet (28 sites) under a Byzantine adversary (abstract, §6). Confirmation metric: "TCR@k, the fraction of benign tasks completed with at most k approvals" (§6); "SPIDES and SOPGuard averaged 1.84 and 0.22 HITL approvals per successfully completed task, respectively" (§6). Limitation: "SPIDES assumes operator-provided element-level labels" (§7). The ideal human in the autonomy evaluation "can distinguish benign approval requests from unsafe ones" (§6).
- Adaptive? partial — the Byzantine model treats any model output that saw attacker content as attacker-controlled (strong, but it is a worst-case model, not an optimiser against the policy). Long-horizon? no.
- Automotive fit: TCR@k is directly the "confirmation budget" metric a car needs; but the assumption of an ideal approver is exactly what a distracted driver violates.
- Verification: PRIMARY-READ (§6–7, App. D).
- Inference: 1.84 approvals per completed task would be unacceptable while driving for frequent tasks; the metric must be combined with distraction budgets (N10).

### D-08 · Progent — Securing AI Agents with Privilege Control
- Shi, T. et al. (incl. Dawn Song), 2025 (v3 14 May 2026) · arXiv · Tier: T3 (Semantic Scholar: no venue).
- https://arxiv.org/abs/2504.11703
- Mechanism: Privilege policies = symbolic rules over tool names and arguments, checked deterministically on every call (least privilege). An LLM drafts the initial policy from the user task and proposes updates; an SMT solver classifies updates as narrowing (auto) or expansion (needs approval) — "monotonic confinement".
- Results: "reduces the attack success rate (ASR) from 39.9% to 1.0% on AgentDojo, and from 70.3% to 3.9% on ASB" (§1). Evaluation assumes the approver will "always accept policy-expansion requests" (§7 setup). Adaptive (App. E, Fig. 10): ASR under three adaptive attacks 0.5 / 4.2 / 0.9 (vs 1.0 normal); "the adaptive attacks can only marginally increase the ASR".
- Third-party: AutoDojo ASR ≤7.7% (GPT-4o-mini), CU cost "up to 7 points" (D-19); 2606.26479 reproduction 25.8%→4.2%, adaptive 2.6% (D-18); SPILLWAY grid BU .437 vs .540 undefended, ASR .031 (D-10 Table 2); **long-horizon**: AgentLAB Task-Injection replay overall ASR 8.7% (GPT-4o-mini), 8.3% (Gemini-2.5-Flash), 15.1% (Qwen3-235B), "up to 43.5 for Progent on Qwen travel" (D-09 Table 3).
- Adaptive? partial (hand-written templates, AgentVigil; third-party black-box). Long-horizon? yes (third-party) — and it leaks.
- Automotive fit: high — a proxy between agent and vehicle API needs no agent rewrite; "expansion requires approval" maps to driving-mode-aware privilege.
- Verification: PRIMARY-READ (§1, §7, App. E).
- Inference: the long-horizon leak (≈1% → 8–15%) is the clearest evidence in the literature that single-turn privilege policies do not carry over to staged attacks.

### D-09 · ROPE — Routed Origin Policy Enforcement against Indirect Prompt Injection
- Ma, X. et al. (Vorobeychik group, incl. C. Xiao), 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2608.27496
- Mechanism: A value may reach a state-changing tool parameter only if it traces unforgeably to the user, a source the user named, or the user's own authoritative records; an LLM reads only the trusted request to route which sources count. Enforcement is a deterministic origin check.
- Results: "ROPE holds attack success rate to 1.6--2.6% while retaining 82--100% of undefended clean utility" (abstract). Long-horizon (Table 3, AgentLAB Task-Injection replay): ROPE overall ASR 0.0 on all three models with UA 40.9 vs 44.0 undefended (GPT-4o-mini); comparison rows: Progent 8.7/8.3/15.1, DRIFT 10.7/6.7/25.4, PFI 0.0/0.0/9.1 at CU 47.4/42.1/36.8, MELON 0.0/0.4/0.0 at UA 13.9/26.8/15.5, Tool Filter 4.0/0.0/4.8 (CU 13.2 on Gemini).
- Adaptive? yes (self, AutoDojo optimiser; "optimizing the injection against ROPE is largely ineffective", abstract). Long-horizon? yes (self).
- Automotive fit: high — "the user's own authoritative records" = car's contact book, home/work addresses, saved payees.
- Verification: PRIMARY-READ (abstract, §4.3–4.4, Table 3).
- Inference: strongest current evidence on the long-horizon axis, but it is the authors' own evaluation; needs third-party replication.

### D-10 · SPILLWAY — Separating Target Admission from Sanitization to Defend Tool-Using Agents against Prompt Injection
- Lim, W., Chang, Y., Lee, J., 2026 · earlier version accepted at NeurIPS 2026 "Agents in the Wild" workshop (claimed, arXiv comment; a neurips.cc virtual-site listing appeared in web search) · Tier: T2 (claimed).
- https://arxiv.org/abs/2611.07222
- Mechanism: Deterministic "target floor": a call is admitted only if every target value (recipient, account) that appears in tool output but not in the user's task came from a *typed field* of a read-only tool, or is covered by a fixed delegation rule. A rule-based sanitizer strips instruction-like spans; a small local judge may restore a refused call but never one whose target came from removed text.
- Results (Table 2, AgentDojo, 12 backbone×suite cells): SPILLWAY BU .539 / UAU .489 / ASR .000 vs undefended .540 / .417 / .305; MELON .526/.314/.094; Progent .437/.371/.031; DRIFT .460/.453/.016. "holds in-scope attack success at .000 under a forged chat template and at .005 on average under a frontier reinforcement-learning attacker (PISmith)" (§6). Limitation: "an injection that steers an effect to a legitimate identity ... is left to the sanitizer and the judge" (§7).
- Adaptive? partial (PISmith replayed open-loop; AutoDojo injections optimised against Progent replayed). Long-horizon? no.
- Automotive fit: very high and cheap ("almost no added model call"): phone numbers, navigation targets and payees must come from typed fields (contacts, OEM POI DB), never from free text in a message.
- Verification: PRIMARY-READ (Tables 1–2, §5–7).

### D-11 · AuthorityFlow — Right Tool, Wrong Parameters: Defending LLM Agents Against Parameter Poisoning
- Wang, Y. et al., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2611.04673
- Mechanism: Targets *parameter poisoning* (right tool, attacker-chosen argument). Builds a task-specific trust hierarchy over information fields from the user query, traces which field produced each argument, accepts only values from fields trusted for that parameter.
- Results: "Without defense, the attack success rate reaches 93.06%. AuthorityFlow reduces it to 9.03%, while retaining 82.64% benign task utility compared with 90.28% without defense" (abstract; FactAuthBench, authors' own benchmark). Table 1 also re-runs other defences on parameter poisoning (Qwen3.6-27B, BU / UA / ASR): CaMeL (policies) 43.75% / 29.17% / 0.69%; MELON 86.81% / 2.78% / 79.17%; IPIGuard 70.83% / 16.67% / 47.92%; DRIFT 86.11% / 44.44% / 39.58%; Spotlighting 92.36% / 25.69% / 69.44%. GPT-4o: CaMeL 39.58% BU / 2.08% ASR vs no defence 81.94% / 57.64%.
- Adaptive? no (adaptive payloads named only as related/future work). Long-horizon? no.
- Automotive fit: parameter poisoning is the most plausible in-car attack (agent *should* navigate/call; attacker changes *where/whom*).
- Verification: PRIMARY-READ (abstract, §1, Table 1).
- Inference: on the attack class most relevant to a car, detectors/planners that check *which tool* is called (MELON, IPIGuard, DRIFT) mostly fail, while CaMeL holds but halves benign utility — the gap AuthorityFlow, ROPE and SPILLWAY target.

### D-12 · IsolateGPT — An Execution Isolation Architecture for LLM-Based Agentic Systems
- Wu, Y. et al. (Iqbal, Kohno, Roesner), 2024/2025 · NDSS 2025 · Tier: T1 (verified on ndss-symposium.org paper page).
- https://arxiv.org/abs/2403.04960
- Mechanism: Hub-and-spoke isolation of third-party LLM apps; apps run in separate spokes and interact only via a trusted hub with user mediation.
- Results: "protects against many security, privacy, and safety issues ... without any loss of functionality. The performance overhead ... is under 30% for three-quarters of tested queries" (abstract).
- Adaptive? no. Long-horizon? no. Note: ACE (NDSS 2026, claimed) "demonstrate[s]" new planning-integrity attacks "against IsolateGPT" (ACE abstract, arXiv 2504.20984).
- Automotive fit: in-car app ecosystems (third-party skills) = exactly the LLM-app setting.
- Verification: ABSTRACT-ONLY.

### D-13 · f-secure — System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective
- Wu, F., Cecchetti, E., Xiao, C., 2024 · arXiv · Tier: T3.
- https://arxiv.org/abs/2409.19091
- Mechanism: Disaggregates the LLM system into a context-aware pipeline with dynamically generated structured plans; a security monitor filters untrusted input out of planning; formal model of guarantees.
- Results: qualitative in abstract ("robust security while preserving functionality and efficiency").
- Adaptive? no. Long-horizon? no.
- Verification: ABSTRACT-ONLY.

### D-14 · Planner/IFC cluster — RTBAS, ACE, PFI, IPIGuard, DRIFT
- RTBAS: Zhong, P.Y. et al., 2025, arXiv 2502.08966, T3 — IFC with LM-judge and attention-saliency dependency screeners; "prevents all targeted attacks with only a 2% loss of task utility when under attack" (abstract). Also argues per-call confirmation is "onerous". ABSTRACT-ONLY.
- ACE: Li, E. et al., 2025, arXiv 2504.20984, NDSS 2026 (claimed, arXiv comment), T1 (claimed) — abstract plan from trusted info, then concrete plan; static IFC check on plan. ABSTRACT-ONLY.
- PFI (Prompt Flow Integrity): Kim, J. et al., 2025, arXiv 2503.15547, T3 — agent isolation + untrusted-data processing + privilege-escalation guardrails. Third-party long-horizon (D-09 Table 3): ASR 0.0/0.0/9.1 but clean completion 47.4 vs 73.7 (GPT-4o-mini). ABSTRACT-ONLY (own paper).
- IPIGuard: An, H. et al., EMNLP 2025 main (verified: ACL Anthology `2025.emnlp-main.53`), T1 — plans a Tool Dependency Graph before reading external data. Third-party (D-36 Table 5): avg ASR 0.7/1.1/0.7 with BU loss 5.4 and 8.1 pts on two models. ABSTRACT-ONLY (own paper).
- DRIFT: Li, H. et al., NeurIPS 2025 poster (verified: OpenReview forum oY1Xnt83oJ, venue "NeurIPS 2025 poster"), T1 — secure planner + JSON-schema parameter checklist + dynamic validator + injection isolator for memory. Third-party: AutoDojo "DRIFT gives up 18 points on GPT-4o-mini and 25 on Claude-Haiku-4.5 (70.2%→45.6%)" and adaptive attack "more than doubles the static ASR (2.6% → 6.4% on GPT-4o-mini ...)" (D-19 §4.2); long-horizon AgentLAB replay 10.7/6.7/25.4% (D-09 Table 3). ABSTRACT-ONLY (own paper).
- Adaptive? DRIFT yes (third-party, degrades); others no. Long-horizon? DRIFT, PFI yes (third-party).
- Inference: defences with an LLM in the runtime decision (DRIFT validator, RTBAS LM-judge) are where adaptive attacks gain; purely structural ones (PFI, Tool Filter) hold ASR but lose utility.

### D-15 · Tool filter (AgentDojo baseline) — AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
- Debenedetti, E. et al., 2024 · NeurIPS 2024 Datasets & Benchmarks · Tier: T1 (verified on proceedings.neurips.cc, D&B track listing).
- https://arxiv.org/abs/2406.13352
- Mechanism (tool filter): before execution an LLM restricts the available tools to those needed for the user task. AgentDojo itself: 97 tasks, 629 security test cases (abstract).
- Results: third-party, MELON paper: tool filter's 0.00% ASR on o3-mini/Llama-3.3-70B "results from blocking nearly all tool usage, rendering the system non-functional" (D-30 §4); CaMeL paper: next-best defence "(tool filter) is 8" successful attacks vs 0 for CaMeL (D-01 §6.3).
- Adaptive? no. Long-horizon? yes (third-party D-09 Table 3: 4.0/0.0/4.8%).
- Verification: ABSTRACT-ONLY (AgentDojo); tool-filter numbers PRIMARY-READ in D-01/D-30/D-09.

### D-18 · Out-of-band adaptive evaluation — Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents
- Narisetty, P. et al., 2026 · arXiv (12 pp.) · Tier: T3.
- https://arxiv.org/abs/2606.26479
- Mechanism (evaluation paper): systematises CaMeL, FIDES, Progent, Conseca, RTBAS, FORGE as Biba integrity + reference monitor + least privilege (Table 2, D1–D8); specifies an adaptive-evaluation protocol; runs it on Progent.
- Results: "every one of them is validated only on static benchmarks"; "Progent cut mean attack success roughly sixfold (25.8% to 4.2%), and a hand-crafted adaptive attack did not raise it (2.6%)" (abstract; Qwen2.5-7B, three runs). §7: open question is "does the reference monitor hold when the attacker optimizes against it” (unknown)". §8.2: "Provenance assignment is the trusted base, and it is under-specified".
- Adaptive? yes, but one black-box template on one weak model. Long-horizon? no.
- Automotive fit: directly reusable as the thesis' evaluation protocol skeleton.
- Verification: PRIMARY-READ (abstract, Table 2, §7–8).

### D-19 · AutoDojo — A Generative Benchmark for Evaluating Prompt Injection Defenses in LLM Agents
- Ma, X. et al., 2026 (v3 28 Sep 2026) · arXiv · Tier: T3.
- https://arxiv.org/abs/2606.15057
- Mechanism (evaluation): black-box adaptive injection generator ("observing only whether a candidate injection succeeds") over AgentDojo + AgentDyn; ten defences × five models.
- Results: "static benchmarks often significantly overestimate defense efficacy" (abstract). "on GPT-4o-mini, AutoDojo lifts PIGuard’s ASR from 0.0% to 28.0%, DataFilter’s from 12.6% to 33.4% ... and ProtectAI’s from 7.2% to 15.4%" (§4.2). CaMeL/ROPE "structurally immune to surface-level paraphrased injection strings whenever their policies are correctly specified" (§4.2). Table 5 gives clean utility and ASR per defence/model (CaMeL rows quoted in D-01; Progent ASR 7.7/1.5/3.6/4.6/0.5 under AutoDojo). Under-specified user tasks are more vulnerable (abstract).
- Adaptive? this *is* the adaptive evaluation (black-box). Long-horizon? no.
- Automotive fit: "under-specified tasks particularly vulnerable" matters for voice commands, which are typically under-specified ("call him back", "take me there").
- Verification: PRIMARY-READ (§1, §4.2, Table 5).

### D-20 · Autonomy metric — Optimizing Agent Planning for Security and Autonomy
- Kolluri, A. et al. (Microsoft; Köpf, Zanella-Béguelin), 2026 · ICLR 2026 poster · Tier: T1 (verified via OpenReview API: forum g0aVCDY3gS, venue "ICLR 2026 Poster"); arXiv 2602.11416.
- https://arxiv.org/abs/2602.11416
- Mechanism: Introduces "autonomy metrics ... the fraction of consequential actions an agent can execute without human-in-the-loop (HITL) approval while preserving security"; a security-aware planner that plans for policy compliance and uses richer HITL interactions, built atop an IFC defence (FIDES lineage).
- Results: metrics defined in §3: "(i) HITL load, the total number of HITL interventions on tasks successfully completed, and (ii) Task Completion Rate under at most k HITL interventions (TCR@k)". §1 motivation: deterministic defences show "a reduction in task completion rate of up to 30 % on the AgentDojo benchmark". §4 (o3-mini, AgentDojo): "the HITL load of Basic-IFC is 1.5× lower (32.4) than that of a Basic agent (48.2)"; FIDES (their PRUDENTIA design builds on it) reaches "a HITL load of 18.8"; "Basic-IFC achieves 9.7 % higher TCR@0 than Basic"; on WASP (data-independent tasks) the agent "achieves full autonomy, i.e. an ideal HITL load of 0". Endorsement of untrusted *data* (one interaction) instead of approving each tool call is a key design lever (§3).
- Adaptive? no. Long-horizon? no.
- Automotive fit: this is the right *metric family* for a car; it needs to be weighted by driving context (Section 5, idea O3). Endorse-data-once maps to "confirm this address once, then navigate/call/message without further prompts".
- Verification: PRIMARY-READ (abstract, §1, §3, §4 first results paragraph).

### D-21 · MiniScope — Authorizing Agents with Least-Privilege Permissions
- Zhu, J. et al. (Popa group), 2025 (v2 Oct 2026) · arXiv · Tier: T3.
- https://arxiv.org/abs/2512.11147
- Mechanism: task-centric hierarchical permission model (agent as delegate in a task role) instead of per-call prompts.
- Results: "reduces simulated permission confirmations by 43.4%-89.4% for cautious and typical personas relative to per-tool prompting and mitigates all privilege-escalation attacks with negligible impact on utility and runtime" (abstract). Motivation: "fine-grained confirmation induces user fatigue".
- Adaptive? no. Long-horizon? no.
- Automotive fit: task roles ("navigation session", "charging session") with pre-granted scoped permissions = confirmation budget design.
- Verification: ABSTRACT-ONLY.

### D-22 · LeanGuard (Lean-verified) — LEANGUARD: Lean-Verified Guardrails for Tool-Using Agents
- Sankar, S. et al., 2026 (2 Nov 2026) · arXiv · Tier: T3. **Name collision:** an unrelated "LeanGuard" (Na, D., arXiv 2606.26686, a 395M encoder moderation guard) exists — see D-48.
- https://arxiv.org/abs/2611.02332
- Mechanism: Every proposed tool call is checked, fail-closed, against a Lean4 policy combining state predicates with scoped *past-time temporal operators* over the execution history; the decision procedure "is proved equivalent to a LeanLTL semantics" (abstract). Denials return the violated rule; proof-guided repair searches for a nearby admissible call.
- Results (Table 1): τ²-bench task success 72.7 (none) → 68.9 (LG) → 70.9 (LG+feedback); judge-flagged 9.7→5.6/6.5. DTap (read-only deployment): direct attack 57.9→5.9, indirect 22.3→3.8, **benign success 53.1→12.5** ("the read-only deployment also stops benign writes", RQ3 text). Telecom: benign unchanged (75.1% vs 75.3%) while direct attack 55.1%→2.4%. Repair: 88 of 252 argument-value denials repaired (RQ4).
- Adaptive? no. Long-horizon? partial (temporal rules over full history; but Table 6 notes "multi-turn attack not yet reproduced (5)").
- Automotive fit: very high for the deterministic gate: past-time rules ("unlock only if the driver asked within the last turn and speed = 0") are exactly what ISO 26262-style requirements look like; "median of 2 ms" repair (abstract).
- Verification: PRIMARY-READ (abstract, Table 1, RQ3–4, Table 6).
- Inference: the 53.1→12.5 drop is a clean illustration that a fail-closed formal gate with an incomplete policy pays in utility, not security.

### D-23 · NOMOS — Compiling Written Policies into Statically Verified Tool-Call Gates for LLM Agents
- Yu, M.-Y. et al., 2026 · arXiv (submitted to IEEE Access) · Tier: T3.
- https://arxiv.org/abs/2610.11030
- Mechanism: four-pass compiler from natural-language policy to a deterministic tool-call gate; static checks against tool schemas repair/reject rules.
- Results: "On τ²-bench the gate cuts violations ... from 66.3% to 2.6% (airline) and 30.8% to 6.9% (retail)"; "zero attack success rate (ASR) on banking"; "Decisions take microseconds without an LLM call, at a domain-dependent benign-utility cost" (abstract).
- Adaptive? no. Long-horizon? no.
- Automotive fit: OEM policies (owner's manual, legal rules) → compiled gate; on-premise compilation with an open 26B model (abstract).
- Verification: ABSTRACT-ONLY.

### D-24 · AgentSpec — Customizable Runtime Enforcement for Safe and Reliable LLM Agents
- Wang, H., Poskitt, C.M., Sun, J., 2025 · ICSE 2026 (claimed, arXiv comment) · Tier: T1 (claimed).
- https://arxiv.org/abs/2503.18666
- Mechanism: DSL of rules = trigger + predicates + enforcement action, evaluated at runtime on agent actions; includes an autonomous-driving domain.
- Results: "prevents unsafe executions in over 90% of code agent cases, eliminates all hazardous actions in embodied agent tasks, and enforces 100% compliance by autonomous vehicles (AVs)"; "overheads in milliseconds"; LLM-generated rules (o1) "precision of 95.56% and recall of 70.96%" (abstract).
- Adaptive? no. Long-horizon? no.
- Automotive fit: the only defence paper found that already includes an AV domain; useful precedent for rule format.
- Verification: ABSTRACT-ONLY.

### D-25 · ShieldAgent — Shielding Agents via Verifiable Safety Policy Reasoning
- Chen, Z., Kang, M., Li, B., 2025 · ICML 2025 · Tier: T1 (verified: PMLR v267 `chen25ae`).
- https://arxiv.org/abs/2503.22738
- Mechanism: extracts verifiable rules from policy documents into probabilistic rule circuits; a guardrail agent checks the protected agent's action trajectory with formal-verification tools.
- Results: "outperforming prior methods by 11.3% on average with a high recall of 90.1%"; "reduces API queries by 64.7% and inference time by 58.2%" (abstract; ShieldAgent-Bench).
- Adaptive? no. Long-horizon? partial (trajectories, web environments).
- Verification: ABSTRACT-ONLY.

### D-26 · Llama Guard — LLM-based Input-Output Safeguard for Human-AI Conversations
- Inan, H. et al. (Meta), 2023 · arXiv · Tier: T3.
- https://arxiv.org/abs/2312.06674
- Mechanism: Llama2-7B fine-tuned to classify prompts/responses against a safety-risk taxonomy.
- Results: matches or exceeds moderation tools on OpenAI Moderation and ToxicChat (abstract).
- Adaptive? no. Long-horizon? no. Note: a content-safety classifier, not an injection defence — it cannot tell a benign-looking "navigate to X" from an injected one.
- Verification: ABSTRACT-ONLY.

### D-27 · LlamaFirewall (PromptGuard 2, AlignmentCheck, CodeShield)
- Chennabasappa, S. et al. (Meta), 2025 · arXiv · Tier: T3.
- https://arxiv.org/abs/2505.03574
- Mechanism: PromptGuard 2 (small jailbreak/injection classifier), Agent Alignment Checks (chain-of-thought auditor of the agent's reasoning for goal misalignment), CodeShield (static analysis).
- Results (own): AlignmentCheck is "still experimental" (abstract). Third-party: PromptGuard adaptive ASR "> 90%" (D-44 §5); AlignmentCheck as monitor: AUROC 0.930 on AgentDojo but "its released decision rule would still mostly raise false alerts at a 2% attack rate (precision 0.096)" (D-32 abstract).
- Adaptive? third-party yes (broken / impractical). Long-horizon? no.
- Verification: ABSTRACT-ONLY (own paper); third-party numbers PRIMARY-READ.

### D-28 · PIGuard / InjecGuard — Prompt Injection Guardrail via Mitigating Overdefense for Free
- Li, H., Liu, X. (et al.), 2025 · ACL 2025 long (verified: ACL Anthology `2025.acl-long.1468`, titled "PIGuard"; arXiv 2410.22770 titled "InjecGuard") · Tier: T1.
- https://aclanthology.org/2025.acl-long.1468/
- Mechanism: injection classifier trained with "Mitigating Over-defense for Free" to reduce trigger-word bias; NotInject benchmark (339 benign trigger-word samples).
- Results: own: over-defence of SOTA guards drops accuracy "close to random guessing levels (60%)"; InjecGuard surpasses best model "by 30.8%" on NotInject (arXiv abstract). Third-party: adaptive "PIGuard is somewhat more resistant but still reaches 71% ASR" (D-44 §5); AutoDojo 0.0%→28.0% on GPT-4o-mini with clean utility 66.7→43.9 (D-19 Table 5).
- Adaptive? third-party, broken. Long-horizon? no.
- Verification: ABSTRACT-ONLY (own); third-party PRIMARY-READ.

### D-29 · DataSentinel — A Game-Theoretic Detection of Prompt Injection Attacks
- Liu, Y. et al. (Gong group), 2025 · IEEE S&P 2025, Distinguished Paper (claimed in arXiv comment; corroborated by citations "2025 IEEE Symposium on Security and Privacy (SP), pp. 2190–2208" in other PDFs) · Tier: T1 (claimed + corroborated).
- https://arxiv.org/abs/2504.11358
- Mechanism: known-answer detection (can the detector LLM still repeat a secret key?) fine-tuned with a minimax objective against adaptive injections.
- Results: own: detects "both existing and adaptive prompt injection attacks" (abstract). Third-party: RL attack redirected the task with "over 80% accuracy on both tasks—comparable to an undefended model. In every case, the defense was bypassed." (D-44 §5). In Progent's AgentDojo comparison, detectors (incl. DataSentinel) "fail to generalize to AgentDojo, exhibiting high rates of false" positives (D-08 §7).
- Adaptive? self yes (minimax), third-party broken. Long-horizon? no.
- Verification: ABSTRACT-ONLY (own); third-party PRIMARY-READ.

### D-30 · MELON — Provable Defense Against Indirect Prompt Injection Attacks in AI Agents
- Zhu, K. et al., 2025 · ICML 2025 · Tier: T1 (verified: PMLR v267 `zhu25z`).
- https://arxiv.org/abs/2502.05174
- Mechanism: re-executes the trajectory with a masked user prompt (a "summarise the tool outputs" task); if the masked run produces the same tool calls as the real run, the calls are driven by tool output → attack.
- Results (own, AgentDojo): "For GPT-4o, MELON achieves the average ASR of 0.24%" (§4); MELON-Aug "ASR to 0.32% while maintaining 68.72% utility on GPT-4o" (§1). No adaptive section in the paper (no match for "adaptive" in text).
- Third-party: "Our search-based attack reaches a 76% ASR against MELON on Llama-3.3-70B even without explicit knowledge of the defense"; with full knowledge "This yields a 95% ASR." (D-44 §5). Long-horizon PI2: avg ASR 0.7% (GPT-4o-mini) but 42.1% (Llama-3.3) and 20.7% (Qwen3); BU loss 5.4/9.8 pts (D-36 §6.2, Table 5). AgentLAB replay: ASR ≈0 but UA 13.9/26.8/15.5 (D-09 Table 3).
- Adaptive? no (self); third-party broken. Long-horizon? third-party yes — model-dependent.
- Automotive fit: doubles LLM calls per step (latency) and fails against conditional injections; weak fit.
- Verification: PRIMARY-READ (§1, §4).

### D-31 · Task Shield — Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents
- Jia, F. et al., 2025 · ACL 2025 long · Tier: T1 (verified: ACL Anthology `2025.acl-long.1435`).
- https://arxiv.org/abs/2412.16682
- Mechanism: test-time LLM checker that verifies whether each instruction and tool call contributes to user-specified goals.
- Results (Table 1, GPT-4o, Important-Instructions attack, overall): Task Shield utility-under-attack 69.79 / ASR 2.07 vs no defence 50.08 / 47.69. Limitations section names "susceptibility to adaptive attacks".
- Adaptive? no. Long-horizon? no.
- Automotive fit: goal-consistency checking is the right *idea* for long-horizon monitoring (O4), but an LLM checker reading attacker text inherits AMS-style breaks.
- Verification: PRIMARY-READ (abstract, Table 1, limitations).

### D-32 · Detectors of hijacked agents — What Standard Evaluations Hide About Detectors of Hijacked LLM Agents: Rare Attacks, Unseen Tools and Benchmark Transfer
- Abbasi, M. et al., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2610.41803
- Mechanism (evaluation): audits 11 trace-detector evaluations; tests trained detectors and AlignmentCheck on AgentDrift and AgentDojo at realistic prevalence.
- Results: "attacks or anomalies make up 16% to 86% of the test samples, no evaluation varies that share"; "at a 2% attack rate a detector with an area under the receiver operating characteristic curve (AUROC) of 0.879 reaches a precision of 0.076"; "no detector trained on AgentDrift ranks AgentDojo traces better than chance (AUROC 0.47 to 0.52), including one that reaches 0.996 within AgentDojo"; AlignmentCheck "reaches 0.930 ... (precision 0.096)" (abstract). Gives a checklist.
- Automotive fit: in a car, attacks are rare; a monitor that alarms the driver at precision ≈0.08 means >90% false alarms → confirmation fatigue.
- Verification: PRIMARY-READ (abstract, tables around the 0.076/0.930 values).

### D-33 · Passing the Test You Trained On — Re-evaluating Prompt-Injection Detectors for LLM Agents
- Liu, Z., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2610.03448
- Mechanism (evaluation): replays ground-truth tool calls of AgentDojo and τ-bench to get benign-by-construction tool outputs; 15 detectors incl. Prompt Guard 2 and two task-aware LLM judges.
- Results: "the best detector on BIPIA catches 2% of AgentDojo injections at a 1% false-positive rate, and a detector that catches 72% of AgentDojo injections catches 15% on tau-bench"; "False-positive rates on tool outputs, which range from none to over 90%, do transfer" (abstract).
- Verification: ABSTRACT-ONLY.
- Inference: detector choice for a car must be made on the car's own tool-output distribution (CAN-derived status strings, POI JSON), not public benchmarks.

### D-34 · Hidden-state probes — Your Agentic LLMs Secretly Encode Indirect Prompt-Injection Exposure in Hidden States
- Dong, J. et al., 2026 (v2 24 Aug 2026) · arXiv · Tier: T3.
- https://arxiv.org/abs/2608.02657
- Mechanism: linear probes on pre-generation hidden states predict IPI exposure; a probe-gated reasoning defence triggers safety reasoning when the probe fires.
- Results: probes "achieve 0.90+ AUROC on unseen attacks, agent instructions, and task suites"; defence "from 34.6% to 0% on Qwen3.5-27B" (abstract). Adaptive (§3): "the probes ... reach AUROCs of 0.999 and 0.992 under the search-based attack, and 1.000 and 0.956 under anti-encoding" (Qwen3-8B, Gemma-4-31B).
- Adaptive? yes (self; black-box rewriting + a naive anti-encoding instruction — not a white-box attack on the probe). Long-horizon? partial (multi-turn agent traces; intervention kept "for the next three assistant turns").
- Automotive fit: an on-board open-weight model gives activation access; the probe is cheap. Needs white-box adaptive testing before trust.
- Verification: PRIMARY-READ (abstract, §3 adaptive paragraph).

### D-35 · Guardrail DoS — From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails
- Zhou, Y. et al., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2606.14517
- Mechanism (attack on the defence layer): payloads that trap reasoning guardrails in long reasoning loops.
- Results: "13--63× token amplification"; end-to-end "up to a 148× latency amplification"; "a single poisoned document can saturate shared guardrail infrastructures" (abstract).
- Automotive fit: critical — an in-car assistant has hard latency budgets; any LLM-based guard is an availability risk → motivates Simplex fallback (N6) and cost-bounded, non-reasoning guards (cf. D-48).
- Verification: ABSTRACT-ONLY.

### D-36 · ShadowMem (v1 title "MAGE") — Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory
- Wang, Y., Jiang, T., Liang, J., Fleming, C., Wang, T. (same group as AgentLAB), 2026 · ACM CCS 2026 (claimed: arXiv comment "Accepted to ACM CCS 2026"; PDF carries the header "CCS ’26, November 15–19, 2026, The Hague, Netherlands") · Tier: T1 (claimed).
- https://arxiv.org/abs/2605.03228 — **Note:** v1 (4 May 2026) was titled "MAGE: Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory" (secondary indexes, e.g. arxivexplorer); v2 (23 Sep 2026) is titled ShadowMem. MAGE and ShadowMem are the same paper, not two defences.
- Mechanism: inspired by the shadow stack; a dedicated safety memory manager (M) distils safety-critical context across the whole trajectory; a judge (J) uses it to assess each pending action before execution; both trained with turn-wise GRPO.
- Results (Table 5, AgentDojo Banking+Slack, "average of 4.43 interaction turns"): PI2 long-horizon attack ASR — GPT-4o-mini: no defence 98.2, Spotlighting 98.2, MELON 0.0, IPIGuard 0.0, ShadowMem 0.0; Llama-3.3 average ASR: MELON 42.1 vs ShadowMem 0.4. "ShadowMem incurs only marginal utility loss (below 3%)" (§6.2.2); overhead ≈2.7–3.5K tokens/task (Table 5). Adaptive (Table 4): "the agentic harness reaches 16.7% ASR when it reads e, and 25.0% when it also sees m"; bypass works only when the attacker supplies "claims the trajectory cannot contradict" (§5.2).
- Adaptive? yes (self; incl. a frontier agentic attack harness with access to memory and feedback). Long-horizon? yes (PI2: avg 3.5 attack turns, max 6; STAC tool chaining) — but horizons are short (≈4–6 turns).
- Automotive fit: high for trip-length interactions (a drive = many turns); trained judge is still an LLM → adaptive-attack and DoS surface; pair with a deterministic gate.
- Verification: PRIMARY-READ (§5.2, §6.1–6.2, Tables 3–5).

### D-37 · TRACE — Trajectory Risk-Aware Compression for Long-Horizon Agent Safety
- Hong, Z. et al., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2606.00611
- Mechanism: Compressor encodes the full trajectory into a latent evidence state; Reader judges the raw trajectory with this state as reference.
- Results: "best accuracy on all evaluated backbones, improving over strong baselines by up to 12.6 percentage points" on ASSEBench, Pre-Ex-Bench, R-Judge; "smaller performance degradation as context length grows" on LongSafety (abstract).
- Adaptive? no. Long-horizon? yes (offline trajectory classification, not live attacks).
- Verification: ABSTRACT-ONLY (PDF downloaded, only abstract/intro checked).

### D-38 · PAA — Blocking at the Boundary: Auditing Long-Horizon Agents against Staged Prompt Injection
- Liu, J. et al., 2026 · arXiv (29 pp.) · Tier: T3.
- https://arxiv.org/abs/2610.05163
- Mechanism: formulates "boundary action auditing": given a trajectory prefix and the fully specified pending action, predict Pass/Block. Path-Aligned Attribution decomposes the action into operative elements and traces which source supplied each value; blocks unwarranted material influence from attacker-reachable sources.
- Results: staged attacks confirmed against Claude Code and Codex "span eight workflow scenarios, seven attack goals, and six injection surfaces"; benchmark 479 pairs / 3,112 units; "PAA reaches 86% Block recall at a 6-8% false-block rate (FBR), whereas ARGUS reaches 44-47% recall at 16-33% FBR" (abstract). Limitation: "we do not study online-adaptive or auditor-targeted attacks" (§6).
- Adaptive? no (explicit). Long-horizon? yes (staged injection).
- Automotive fit: the pre-action boundary is exactly where a vehicle gate sits; PAA's per-element attribution is the learned complement to a deterministic provenance gate.
- Verification: PRIMARY-READ (abstract, limitations).

### D-39 · Meta-SecAlign — Training LLMs against Prompt Injection for Robust Agents
- Chen, S. et al. (Meta FAIR, Berkeley), 2025 (v4 28 Sep 2026) · arXiv · Tier: T3.
- https://arxiv.org/abs/2507.02735
- Mechanism: SecAlign-style DPO with randomized injection position and self-generated labels; open 8B/70B models.
- Results (Table 4, Llama-3.3-70B): AgentDojo utility 59.8%→84.5%, ASR 14.7%→1.9%; InjecAgent ASR 53.8%→0.5%. Abstract: SecAlign "actually suffers from significant utility degradation, especially in agentic tasks".
- Third-party / later: AMS "reports an attack success rate (ASR) of 2% on the static AgentDojo benchmark ... achieved a 96% ASR" (D-44 §5); SecPO paper: 78.8% AgentDojo ASR@800 under Genetic adaptive attack (D-42 Table 2); SecOPD: 94.0% against PISmith (D-41 abstract).
- Adaptive? self: GCG only (Table 5); third-party: broken. Long-horizon? no.
- Verification: PRIMARY-READ (abstract, Tables 4–5).

### D-40 · StruQ, SecAlign, Instruction Hierarchy (first-generation model-level defences)
- StruQ: Chen, S. et al., USENIX Security 2025 — T1 (verified: usenix.org presentation page). Separate prompt/data channels + structured instruction tuning. Third-party: RL attacker "succeeds in every case we tested" (D-44 §5). ABSTRACT-ONLY (own).
- SecAlign: Chen, S. et al., ACM CCS 2025 (claimed, arXiv comment; corroborated by citations) — T1 (claimed). Preference optimization; claims "<10%" ASR even for stronger unseen attacks (abstract). Later shown to degrade agentic utility (D-39 Table 4: AgentDojo utility 6.2% for SecAlign-70B vs 59.8% undefended). ABSTRACT-ONLY (own).
- Instruction Hierarchy: Wallace, E. et al. (OpenAI), 2024, arXiv 2404.13208 — T3. Training to prioritise privileged instructions. Third-party: "GPT-4o-mini with the tool calling API (which implements the instruction hierarchy by default) is vulnerable to 276 attacks" in AgentDojo (D-01 §6.3). ABSTRACT-ONLY (own).
- Adaptive? third-party broken (StruQ); IH not adaptively tested in what I read. Long-horizon? no.

### D-41 · SecOPD — Mitigating Adaptive Prompt Injections by On-Policy Distillation
- Peng, Y., Lian, L., Wagner, D., Chen, S., 2026 · EMNLP 2026 main · Tier: T1 (verified: ACL Anthology `2026.emnlp-main.1102`).
- https://aclanthology.org/2026.emnlp-main.1102/ (arXiv 2608.21500)
- Mechanism: token-level feedback: the policy's rollout on an injected input is scored token-by-token by the initial model given the clean input (teacher secure by construction).
- Results: "our defended Qwen3.6-27B achieves a 9.0% ASR against the SoTA PISmith adaptive prompt injections, compared to 94.0% for the prior SoTA, Meta-SecAlign"; "in agentic tool calling, SecOPD achieves a 4.7% ASR compared to 5.5% for Meta-SecAlign" (abstract).
- Adaptive? yes (self). Long-horizon? no.
- Verification: ABSTRACT-ONLY.

### D-42 · SecPO — Principled Adversarial Training for Prompt Injection Security
- Chen, S., Peng, Y., Chang, J., Sitawarin, C., Wagner, D., 2026 (30 Oct 2026) · arXiv · Tier: T3.
- https://arxiv.org/abs/2610.41998
- Mechanism: replaces DPO's insecure reference model with an approximated injection-invariant oracle (SecPO loss) and adds adversarial training on optimised injections (best@240).
- Results: "our SecPO + AT Qwen3.6-27B is much more secure than Meta-SecAlign: 8.8% vs. 78.8% AgentDojo ASR@800 under the AttackerMovesSecond attack" (abstract). Table 2 (Qwen3.6-27B, undefended / Meta-SecAlign / SecPO+AT): AgentDojo utility 89.7 / 87.6 / 90.7; AgentDojo static ASR 26.9 / 2.2 / 0.0; Genetic adaptive ASR@800 81.3 / 78.8 / 8.8; DTaP ASR 50.8 / 45.9 / 7.6. Llama-3.1-8B: mean adaptive ASR "from 89.6% to 10.5%" (§4.2).
- Adaptive? yes (self: Genetic, TAP, PISmith, AMS-style). Long-horizon? no.
- Automotive fit: model-level hardening is a cheap *inner* layer for an on-board open model; ≈9% residual ASR means it cannot be the last authority.
- Verification: PRIMARY-READ (abstract, §4.2–4.3, Table 2).

### D-43 · ASIDE — Architectural Separation of Instructions and Data in Language Models
- Zverev, E. et al., 2025 · ICLR 2026 poster · Tier: T1 (verified via OpenReview API: forum C81TnwHiRM, venue "ICLR 2026 Poster").
- https://arxiv.org/abs/2503.10566
- Mechanism: orthogonal rotation of data-token embeddings so instructions and data have distinct representations, with no extra parameters.
- Results: "substantially higher instruction-data separation without performance loss" and more robust on prompt-injection benchmarks "even without dedicated safety training" (abstract).
- Adaptive? no (per abstract). Long-horizon? no.
- Verification: ABSTRACT-ONLY.

### D-44 · AMS — The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections
- Nasr, M., Carlini, N. et al. (incl. Tramèr), 2025 · USENIX Security 2026 · Tier: T1 (verified: usenix.org presentation page `usenixsecurity26/presentation/nasr`; OpenReview shows it was a rejected ICLR 2026 submission before).
- https://arxiv.org/abs/2510.09023
- Mechanism (attack/evaluation): gradient, RL, search-based and human red-team attacks tuned per defence.
- Results: "we bypass 12 recent defenses ... with attack success rate above 90% for most; importantly, the majority of defenses originally reported near-zero attack success rates" (abstract). Spotlighting/Prompt Sandwiching: static ASR "as low as 1%" but adaptive "above 95% for both" (§5.1); StruQ: "succeeds in every case we tested"; MetaSecAlign 2% static → 96% (§5.2); detectors: "> 90% against Protect AI, PromptGuard, and Model Armor ... PIGuard ... 71% ASR" (§5.3); DataSentinel "In every case, the defense was bypassed"; MELON 76% / 95% (§5.4). Lesson 3: "the search attack succeeds 69% of the time whereas the red-teaming humans collectively succeeds 100% of the time".
- Scope gap: plan-then-execute defences (Tool Filter, CaMeL, IPIGuard) skipped (App., quoted in D-01).
- Verification: PRIMARY-READ (abstract, §5, §6, App.).

### D-45 · Signed requirement manifests — Signed but Not Safe: Requirement Integrity in Multi-Agent LLM Handoffs
- Chen, X. et al., 2026 (v2 17 Nov 2026) · arXiv (preregistered) · Tier: T3.
- https://arxiv.org/abs/2611.07483
- Mechanism: the orchestrator extracts each requirement as a verbatim quote + checkable predicate; code signs it; a deterministic verifier checks the merger's decision.
- Results: Qwen3-8B "signed manifests cut unsafe commits under attack from 69.4% to 9.0%"; "the deterministic verifier caught 78.7% of violating decisions versus 59.0% for an LLM checker"; but "one adversarial line raised signed-manifest unsafe commits from 14.6% to 37.5% (Qwen3-8B), 11.1% to 63.9% (gpt-oss-20b) and 16.7% to 97.2% (gemma-4-12b)"; "Signing protects transit; extraction is the trust boundary." (abstract).
- Adaptive? partial (preregistered pre-signing injection). Long-horizon? no.
- Automotive fit: OEM → supplier agent handoffs; the lesson generalises to any provenance gate: the labeller is the TCB.
- Verification: ABSTRACT-ONLY.

### D-46 · Agent data injection — Agent Data Injection Attacks are Realistic Threats to AI Agents
- Choi, W. et al. (Byoungyoung Lee group, same as PFI), 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2607.05120
- Mechanism (attack class relevant to all provenance defences): inject data disguised as trusted metadata (resource identifiers, data origins, tool-call formats).
- Results: real vulnerabilities in Claude in Chrome, Antigravity, Nanobrowser, Claude Code, Codex, Gemini CLI; ADI "easily bypasses existing IPI defenses" (abstract). SPILLWAY reports ADI "succeeds against most defenses it tests except CaMeL’s strict policy" (D-10 §6, secondary).
- Automotive fit: spoofed vehicle-status or sender fields in a message ("[OEM-SERVICE] ...") are the in-car analogue.
- Verification: ABSTRACT-ONLY.

### D-47 · Stateful cooperative defenders — Stateful Cooperative Agents Safeguarding LLMs Against Evolving Multi-Turn Attacks
- Li, S. et al., 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2608.00134
- Mechanism: multi-agent defender with response pacing, strategic ambiguity (misdirection) and forensic log analysis, coordinated adaptively across turns; EMRA dataset (5,200 samples, 8 attack types).
- Results: "reduces ASR by 69% on average relative to evaluated state-of-the-art baselines"; attacker-token consumption +198.83% (abstract).
- Adaptive? partial (attacks "evolve" across turns; not optimised against this defence per abstract). Long-horizon? yes (multi-turn chat), but no tool use.
- Automotive fit: deception/misdirection is inappropriate for a driver-facing assistant; pacing conflicts with latency. Low fit.
- Verification: ABSTRACT-ONLY.

### D-48 · LeanGuard (moderation encoder) — Do Safety Guardrails Need to Reason? LeanGuard: A Fast and Light Approach for Robust Moderation
- Na, D., 2026 · arXiv · Tier: T3. (Different paper from D-22.)
- https://arxiv.org/abs/2606.26686
- Mechanism: 395M label-only bidirectional encoder vs. a reasoning guard trained on the same corpus.
- Results: "average F1 of 82.90 ± 0.26"; "about a ~100x reduction in inference compute"; "retains far more recall at a strict false-positive rate than the reasoning guard" (abstract). Mentions on-device deployment (robots).
- Automotive fit: evidence that an on-board, single-forward-pass content guard is viable (latency, DoS resistance vs D-35); still a classifier → not an injection authority.
- Verification: ABSTRACT-ONLY.

### D-49 · Adaptive-attack toolbox used to evaluate defences (Zhan et al.; PISmith; Hofer et al.; Climbing the Hill)
- Zhan, Q. et al., "Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents", NAACL 2025 Findings — T2 (verified: ACL Anthology `2025.findings-naacl.395`). "we evaluate eight different defenses and bypass all of them using adaptive attacks, consistently achieving an attack success rate of over 50%" (abstract). ABSTRACT-ONLY.
- PISmith (Yin, C. et al., arXiv 2603.13026, COLM 2026 claimed — T2 claimed): RL red-teaming with adaptive entropy regularisation; "state-of-the-art prompt injection defenses remain vulnerable to adaptive attacks" (abstract). ABSTRACT-ONLY.
- Hofer, D., Debenedetti, E., Tramèr, F., "Assessing Automated Prompt Injection Attacks in Agentic Environments", arXiv 2606.10525 — T3. "black-box optimization substantially outperforms gradient-based methods"; attacks optimised on small open models "do not transfer to frontier models like GPT-5" (abstract). ABSTRACT-ONLY.
- Climbing the Hill (Yin, C. et al., arXiv 2609.33628, T3): curriculum RL attacker; "ASR@10 of 93.8% and 45.0% against GPT-5.6-Luna and GPT-5.6-Terra on AgentDyn, whereas ... RL-Hammer and PISmith achieve 0% ASR under the same setting" (abstract). ABSTRACT-ONLY.
- Use for the thesis: these are the attackers a defence evaluation must include (black-box search, RL, curriculum RL, human red-team).

### D-50 · AgentLAB — Benchmarking LLM Agents against Long-Horizon Attacks
- Jiang, T. et al. (Ting Wang group), 2026 · arXiv · Tier: T3.
- https://arxiv.org/abs/2602.16901
- Mechanism (benchmark): five long-horizon attack types (intent hijacking, tool chaining, task injection, objective drifting, memory poisoning), 28 environments, 644 test cases.
- Results: "defenses designed for single-turn interactions fail to reliably mitigate long-horizon threats" (abstract) — confirmed third-party by ROPE's replay (D-09 Table 3).
- Verification: ABSTRACT-ONLY.

---

## 5. Original defence ideas for an in-vehicle agent

Each idea is my proposal (Inference throughout); "closest prior work" cites entries above.

**O1 · Provenance-typed action gate with vehicle-state context ("VSG").**
A deterministic gate between the LLM and the vehicle API gateway. Every argument of a consequential call (destination, phone number, payee, door/window/seat command) carries a provenance type: `driver_voice`, `oem_trusted` (vehicle state, OEM POI DB, owner's contacts), `third_party_typed` (typed field of a read-only tool), `free_text_untrusted`. The policy is a function of (action, argument provenance, *vehicle state*: speed, gear, driving mode, occupancy). Example: `open_window(pos)` admitted from `driver_voice` at any speed but clamped by a barrier-function-style projection above 100 km/h (N7); `navigate(dest)` admitted only if `dest` has provenance `driver_voice`/`oem_trusted`/`third_party_typed`, never `free_text_untrusted`.
- Closest prior work: CaMeL (D-01), ROPE (D-09), SPILLWAY (D-10), AgentSpec AV rules (D-24), FIDES labels (D-06).
- What's new: vehicle state as a first-class policy input; the gate is designed to be ASIL-decomposable from the QM LLM (N9) and to fail operational (O6).
- Evaluate: an in-vehicle AgentDojo-style suite (navigation, messaging, calls, climate, charging/payment, locks); static + AutoDojo-style black-box adaptive + AgentLAB-style staged attacks; report ASR, clean and under-attack utility, p95 gate latency.
- Publishability: good for a security workshop (NeurIPS/ICML "Agents in the Wild", escar) and plausible main-track (SaTML/ACSAC) if the adaptive + long-horizon evaluation is thorough.

**O2 · Driving-mode-aware privilege lattice with monotone confinement.**
Privileges form a lattice indexed by driving context (parked < manual driving < assisted driving (L2) < conditional automation (L3) per the vehicle's own mode, ordered by how much attention the driver can spare). Within a drive the agent's effective privilege can only *narrow* automatically (Progent's monotonic confinement, D-08); *expansion* requires a confirmation that is only offered when the context allows it (e.g., parked, or via a physical control).
- Closest prior work: Progent (D-08), MiniScope task roles (D-21), Conseca contextual policies (HotOS 2025 workshop, arXiv 2501.17070, ABSTRACT-ONLY).
- What's new: context = vehicle mode, not task; ties privilege expansion to driver workload.
- Evaluate: replay long-horizon attacks that try to trigger expansions mid-drive; count expansion requests per drive; compare with a flat per-task policy.
- Publishability: workshop-level alone; strong as part of O1.

**O3 · Confirmation budget metric (TCR@k weighted by driving workload).**
Extend SPIDES' TCR@k (D-07) and Kolluri's autonomy (D-20) with a *workload-weighted* budget: each approval costs w(context) (e.g., 0 when parked, high in motion), and the system must complete tasks under a budget B per drive while keeping ASR ≈0. Approvals in motion must be voice-only and must not require reading.
- Closest prior work: D-07, D-20, D-21, Aegis OS (arXiv 2611.08516: confirmations "interrupt workflows on 45%-57% of tool calls", ABSTRACT-ONLY), SA-CUA (arXiv 2610.18508, ABSTRACT-ONLY), driver-distraction guidance (N10).
- What's new: the first security–utility–*distraction* frontier for agents.
- Evaluate: offline with an ideal approver first (as SPIDES does), then a small driving-simulator study measuring approval accuracy under attack and glance behaviour.
- Publishability: high novelty; HCI+security venues (SOUPS, CHI late-breaking, AutomotiveUI) or as the evaluation chapter of the thesis.

**O4 · Hybrid trajectory monitor: past-time temporal rules + shadow memory.**
A two-tier long-horizon monitor: tier 1 = deterministic past-time temporal rules over the action/utterance history (LeanGuard-style, D-22), e.g., "a payment to a payee first seen in an inbound message within the last N turns requires a driver utterance naming that payee"; tier 2 = a learned shadow memory + judge (ShadowMem, D-36) that only *escalates* (can add confirmations/blocks, never admit what tier 1 denied).
- Closest prior work: D-22, D-36, PAA (D-38), Task Shield (D-31).
- What's new: monotone composition (learned part can only tighten) gives the deterministic guarantee of tier 1 plus the recall of tier 2 on staged attacks; test whether tier 2 alarms stay useful at realistic prevalence (D-32).
- Evaluate: AgentLAB-style staged attacks adapted to the car; report Block recall / false-block rate at 1–2% attack prevalence (precision, not only AUROC).
- Publishability: medium–high (long-horizon defence is under-explored; adaptive evaluation would be the differentiator).

**O5 · STPA-to-policy compilation.**
Run STPA on the agent-in-the-vehicle control structure, derive unsafe control actions (UCAs: provided when unsafe, not provided, wrong timing/order, too long/short), and compile them into gate rules (NOMOS-style compiler, D-23; AgentSpec DSL, D-24). Measure coverage: what fraction of the thesis' attack goals map to at least one UCA-derived rule.
- Closest prior work: D-23, D-24; STPA itself (N8); LLM-assisted STPA (arXiv 2304.01246, 2503.12043 — titles from arXiv search, not read).
- What's new: hazard-analysis-derived (not benchmark-derived) policies; gives an argument a safety assessor recognises.
- Publishability: good for a safety-engineering venue (SAFECOMP/ISSRE workshops) or as the thesis' "Defense" chapter design rationale.

**O6 · Simplex fallback for availability.**
When the gate denies, the guard is slow (D-35 DoS), or the monitor's confidence collapses, switch to a verified *simple* controller: a fixed voice-command grammar for core functions (call contact, climate, navigation to saved places) with no LLM in the loop.
- Closest prior work: Simplex/runtime assurance (N6), LeanGuard feedback/repair (D-22).
- What's new: treats LLM-guard availability as a safety requirement; measures degradation instead of only ASR.
- Evaluate: inject guard-DoS payloads; measure task completion and latency of core functions with/without fallback.
- Publishability: workshop; strong demo value.

---

## 6. Registry rows

```csv
id,short_name,title,authors_first,year,venue,tier,verification,url,used_for,notes
D-01,CaMeL,Defeating Prompt Injections by Design,Debenedetti,2025,IEEE SaTML 2026,T2,PRIMARY-READ,https://arxiv.org/abs/2503.18813,"system defence; utility cost","77% vs 84% AgentDojo; venue via Semantic Scholar DBLP key + DOI 10.1109/SaTML68715.2026.00040; AMS skipped it"
D-02,DesignPatterns,Design Patterns for Securing LLM Agents against Prompt Injections,Beurer-Kellner,2025,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2506.08837,"architecture vocabulary",six patterns
D-03,NOVA,CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents,Foerster,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2601.09923,"CaMeL for GUI agents; branch steering",retains up to 57%
D-04,multi-CaMeL,Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks,Peters-Gill,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.05640,"composition across agents","guarantees do not compose; CaMeL -21.6 pts utility"
D-05,COBRA,Securing Computer-Use Agents Against Branch Steering Attacks,Zingrillo,2026,NeurIPS 2026 AitW workshop (claimed),T2,ABSTRACT-ONLY,https://arxiv.org/abs/2610.03089,"branch steering defence",0% ASR 97% utility
D-06,FIDES,Securing AI Agents with Information-Flow Control,Costa,2025,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2505.23643,"IFC planner",utility drop up to 24.5% with policies
D-07,SPIDES,SPIDES: Information-Flow Control for Browser Agents,Zverev,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.24277,"IFC; TCR@k confirmation metric",1.84 approvals per completed task
D-08,Progent,Progent: Securing AI Agents with Privilege Control,Shi,2025,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2504.11703,"privilege control","39.9->1.0% static; leaks 8.7-15.1% long-horizon (ROPE T3)"
D-09,ROPE,ROPE: Routed Origin Policy Enforcement against Indirect Prompt Injection,Ma,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2608.27496,"origin check; long-horizon evidence",AgentLAB replay table for 6 defences
D-10,SPILLWAY,SPILLWAY: Separating Target Admission from Sanitization to Defend Tool-Using Agents against Prompt Injection,Lim,2026,NeurIPS 2026 AitW workshop (claimed),T2,PRIMARY-READ,https://arxiv.org/abs/2611.07222,"typed-target floor; third-party grid",BU .539 vs .540
D-11,AuthorityFlow,Right Tool Wrong Parameters: Defending LLM Agents Against Parameter Poisoning,Wang,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2611.04673,"parameter poisoning",93.06->9.03% ASR
D-12,IsolateGPT,IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems,Wu,2025,NDSS 2025,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2403.04960,"app isolation",verified on ndss-symposium.org
D-13,f-secure,System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective,Wu,2024,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2409.19091,IFC,
D-14a,RTBAS,RTBAS: Defending LLM Agents Against Prompt Injection and Privacy Leakage,Zhong,2025,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2502.08966,"IFC + screeners",2% utility loss
D-14b,ACE,ACE: A Security Architecture for LLM-Integrated App Systems,Li,2025,NDSS 2026 (claimed),T1,ABSTRACT-ONLY,https://arxiv.org/abs/2504.20984,"abstract-concrete planning",attacks IsolateGPT
D-14c,PFI,Prompt Flow Integrity to Prevent Privilege Escalation in LLM Agents,Kim,2025,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2503.15547,"privilege escalation",third-party LH numbers in ROPE
D-14d,IPIGuard,IPIGuard: A Novel Tool Dependency Graph-Based Defense Against Indirect Prompt Injection in LLM Agents,An,2025,EMNLP 2025,T1,ABSTRACT-ONLY,https://aclanthology.org/2025.emnlp-main.53/,"plan graph",ACL Anthology verified
D-14e,DRIFT,DRIFT: Dynamic Rule-Based Defense with Injection Isolation for Securing LLM Agents,Li,2025,NeurIPS 2025,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2506.12104,"dynamic rules","OpenReview verified; AutoDojo doubles ASR; CU -18/-25 pts"
D-15,AgentDojo/ToolFilter,AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents,Debenedetti,2024,NeurIPS 2024 D&B,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2406.13352,"benchmark; tool filter baseline",proceedings.neurips.cc verified
D-18,OOB-adaptive,Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents,Narisetty,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2606.26479,"evaluation protocol",Progent 25.8->4.2%; adaptive 2.6%
D-19,AutoDojo,AutoDojo: A Generative Benchmark for Evaluating Prompt Injection Defenses in LLM Agents,Ma,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2606.15057,"third-party adaptive eval incl. CaMeL",Table 5 utility costs
D-20,Autonomy,Optimizing Agent Planning for Security and Autonomy,Kolluri,2026,ICLR 2026,T1,PRIMARY-READ,https://arxiv.org/abs/2602.11416,"HITL autonomy metric",OpenReview g0aVCDY3gS
D-21,MiniScope,MiniScope: Authorizing Agents with Least-Privilege Permissions,Zhu,2025,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2512.11147,"confirmation fatigue",-43.4% to -89.4% confirmations
D-22,LeanGuard-Lean,LEANGUARD: Lean-Verified Guardrails for Tool-Using Agents,Sankar,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2611.02332,"formal tool-call policy; past-time LTL",benign 53.1->12.5 read-only
D-23,NOMOS,NOMOS: Compiling Written Policies into Statically Verified Tool-Call Gates for LLM Agents,Yu,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2610.11030,"policy compilation",
D-24,AgentSpec,AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents,Wang,2025,ICSE 2026 (claimed),T1,ABSTRACT-ONLY,https://arxiv.org/abs/2503.18666,"runtime DSL incl. AV",
D-25,ShieldAgent,ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning,Chen,2025,ICML 2025,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2503.22738,"policy-reasoning guard",PMLR v267 chen25ae
D-26,LlamaGuard,Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations,Inan,2023,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2312.06674,"content classifier",
D-27,LlamaFirewall,LlamaFirewall: An open source guardrail system for building secure AI agents,Chennabasappa,2025,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2505.03574,"PromptGuard 2; AlignmentCheck",AlignmentCheck precision 0.096 at 2% (D-32)
D-28,PIGuard,PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free,Li,2025,ACL 2025,T1,ABSTRACT-ONLY,https://aclanthology.org/2025.acl-long.1468/,"detector","arXiv 2410.22770 (InjecGuard); 71% adaptive ASR (AMS)"
D-29,DataSentinel,DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks,Liu,2025,IEEE S&P 2025 (claimed),T1,ABSTRACT-ONLY,https://arxiv.org/abs/2504.11358,"detector",bypassed by AMS
D-30,MELON,MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents,Zhu,2025,ICML 2025,T1,PRIMARY-READ,https://arxiv.org/abs/2502.05174,"re-execution detector","PMLR v267 zhu25z; 95% adaptive ASR (AMS)"
D-31,TaskShield,The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents,Jia,2025,ACL 2025,T1,PRIMARY-READ,https://aclanthology.org/2025.acl-long.1435/,"goal-alignment check",ASR 2.07% UA 69.79%
D-32,HijackDetectors,What Standard Evaluations Hide About Detectors of Hijacked LLM Agents: Rare Attacks Unseen Tools and Benchmark Transfer,Abbasi,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.41803,"base-rate evaluation",precision 0.076 at 2%
D-33,PassingTheTest,Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents,Liu,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2610.03448,"detector transfer",2% at 1% FPR
D-34,HiddenStateProbes,Your Agentic LLMs Secretly Encode Indirect Prompt-Injection Exposure in Hidden States,Dong,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2608.02657,"white-box detector",34.6->0% Qwen3.5-27B
D-35,GuardDoS,From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails,Zhou,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2606.14517,"availability attack on guards",up to 148x latency
D-36,ShadowMem(MAGE),Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory,Wang,2026,ACM CCS 2026 (claimed),T1,PRIMARY-READ,https://arxiv.org/abs/2605.03228,"long-horizon monitor","v1 titled MAGE; same paper"
D-37,TRACE,TRACE: Trajectory Risk-Aware Compression for Long-Horizon Agent Safety,Hong,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2606.00611,"trajectory detector",+12.6 pp
D-38,PAA,Blocking at the Boundary: Auditing Long-Horizon Agents against Staged Prompt Injection,Liu,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.05163,"pre-action auditor",86% recall at 6-8% FBR
D-39,Meta-SecAlign,Meta-SecAlign: Training LLMs against Prompt Injection for Robust Agents,Chen,2025,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2507.02735,"model-level","1.9% static; 96% adaptive (AMS)"
D-40a,StruQ,StruQ: Defending Against Prompt Injection with Structured Queries,Chen,2025,USENIX Security 2025,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2402.06363,"model-level",usenix.org verified
D-40b,SecAlign,SecAlign: Defending Against Prompt Injection with Preference Optimization,Chen,2025,ACM CCS 2025 (claimed),T1,ABSTRACT-ONLY,https://arxiv.org/abs/2410.05451,"model-level",
D-40c,InstructionHierarchy,The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions,Wallace,2024,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2404.13208,"model-level",276 AgentDojo attacks on GPT-4o-mini (CaMeL paper)
D-41,SecOPD,SecOPD: Mitigating Adaptive Prompt Injections by On-Policy Distillation,Peng,2026,EMNLP 2026,T1,ABSTRACT-ONLY,https://aclanthology.org/2026.emnlp-main.1102/,"model-level adaptive-robust",9.0% vs 94.0% PISmith
D-42,SecPO,SecPO: Principled Adversarial Training for Prompt Injection Security,Chen,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.41998,"model-level adaptive-robust",8.8% vs 78.8% ASR@800
D-43,ASIDE,ASIDE: Architectural Separation of Instructions and Data in Language Models,Zverev,2025,ICLR 2026,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2503.10566,"model architecture",OpenReview C81TnwHiRM
D-44,AMS,The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections,Nasr,2025,USENIX Security 2026,T1,PRIMARY-READ,https://arxiv.org/abs/2510.09023,"adaptive evaluation","usenix.org verified; skipped CaMeL/ToolFilter/IPIGuard"
D-45,SignedManifests,Signed but Not Safe: Requirement Integrity in Multi-Agent LLM Handoffs,Chen,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2611.07483,"multi-agent provenance",extraction is trust boundary
D-46,ADI,Agent Data Injection Attacks are Realistic Threats to AI Agents,Choi,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2607.05120,"attack on provenance defences",
D-47,StatefulCoop,Stateful Cooperative Agents Safeguarding LLMs Against Evolving Multi-Turn Attacks,Li,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2608.00134,"multi-turn chat defence",-69% ASR
D-48,LeanGuard-Mod,Do Safety Guardrails Need to Reason? LeanGuard: A Fast and Light Approach for Robust Moderation,Na,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2606.26686,"on-device guard","name collision with D-22"
D-49a,ZhanAdaptive,Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents,Zhan,2025,NAACL 2025 Findings,T2,ABSTRACT-ONLY,https://aclanthology.org/2025.findings-naacl.395/,"adaptive attack",8 defences >50% ASR
D-49b,PISmith,PISmith: Reinforcement Learning-based Red Teaming for Prompt Injection Defenses,Yin,2026,COLM 2026 (claimed),T2,ABSTRACT-ONLY,https://arxiv.org/abs/2603.13026,"adaptive attack",
D-49c,HoferAutoPI,Assessing Automated Prompt Injection Attacks in Agentic Environments,Hofer,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2606.10525,"adaptive attack",TAP > GCG
D-49d,ClimbingTheHill,Climbing the Hill: Prompt Injection Red-Teaming Against Frontier Models with Curriculum Reinforcement Learning,Yin,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2609.33628,"adaptive attack",93.8% ASR@10 AgentDyn
D-50,AgentLAB,AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks,Jiang,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2602.16901,"long-horizon benchmark",
```
