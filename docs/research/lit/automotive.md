# Automotive context + standards/governance — literature survey

Thesis: *Robustness of agentic AI to adversarial attacks — an adversarial-example pipeline for long-horizon tasks, evaluating in-vehicle LLM agents across agent architectures* (Attack → Evaluate → Defense).
Scope of this file: deployed in-vehicle assistants (public info only), academic work on in-vehicle LLM agents and their security, standards/regulation, industry threat catalogues, automotive security research culture.
Status: compiled 18 Nov 2026. Hard constraint respected: public sources only, no VW-internal data, no real vehicles / CAN — every proposal below is for simulation.

**Verification legend.** Tier: T1 peer-reviewed top venue · T2 peer-reviewed workshop/journal/symposium OR official standard/regulation · T3 arXiv/tech report/official company or lab research publication · T4 blog/press/talk/GitHub/forum. Verification: PRIMARY-READ (full text opened, numbers quoted from it) · ABSTRACT-ONLY · SNIPPET (only search-engine snippets of the primary page were available; treat as UNVERIFIED for exact wording) · UNVERIFIED. "Inference:" marks my own reasoning, not a source claim.

**Hosts that could not be opened from this environment** (so their content is SNIPPET/UNVERIFIED here): unece.org (HTTP 403), iso.org (not attempted beyond search, per instructions), eur-lex.europa.eu (AWS-WAF JavaScript challenge, HTTP 202 with empty body), csrc.nist.gov / nvlpubs.nist.gov, press.bmwgroup.com, group.mercedes-benz.com, cerence.com, stellantis.com, tesla.com, nvidia.com, blog.google / built-in.google, vicone.com, upstream.auto, escar.info, techrxiv.org, indico.un.org, globalautoregs.com, dl.acm.org (403). Opened successfully: arxiv.org, aclanthology.org, api.semanticscholar.org, usenix.org, genai.owasp.org, volkswagen-group.com, GitHub (git clone).

---

## 1. Area summary

**What is deployed.** Production in-car LLM features fall into two groups. (a) *Cloud chat fall-backs* behind a classic intent-based assistant: VW IDA forwards unanswerable questions "anonymously" to ChatGPT via Cerence Chat Pro (standard from Q2 2024; VW states ChatGPT "does not gain access to any vehicle data"), DS/Stellantis ChatGPT via SoundHound (factory-installed from March 2024, snippet), Mercedes ChatGPT "general knowledge" (snippet). (b) *Agentic assistants that call vehicle functions and external services*: Gemini in cars with Google built-in (announced 30 Apr 2026: climate, heated seats, wipers, navigation, message summaries — snippet), Tesla Grok after update 2026.26 (climate, mirrors, wipers, navigation — enthusiast press), Mercedes MBUX Virtual Assistant on Google's Automotive AI Agent (CLA, multi-turn with memory — snippet), BMW IPA with Alexa+ technology (iX3, H2 2026 — snippet), and VW Group China's onboard CEA agent (H2 2026; CEA 2.0 multi-agent incl. driving from 2027 — primary-read press release). Only VW's CEA 2.0 publicly announces unifying *driving* and cockpit agents; everything else publicly exposes comfort, navigation, media and communication tools.

**Realistic threat model.** The best-evidenced attacker is a *remote content injector* (calendar invite, e-mail/message, POI/review text, web result, partner agent) — not a CAN hacker. The closest production evidence is Nassi/Cohen/Yair's Gemini work (14 attacks via calendar invites/e-mails, physical side-effects in a smart home, 73 % "High-Critical" under an ISO/SAE 21434-style TARA). In-cabin occupants (driver, passenger, child; 2609.19630) and out-of-cabin acoustic injection (ShieldSpear, CCS 2025: 90.9 % end-to-end success on five vehicles, abstract) are the next channels. Supply-chain tool poisoning (FuncPoison) and visual prompt injection (CHAI) matter once driving agents are LLM-based.

**Benchmarks.** CAR-bench (ACL 2026; 58 tools, 19 policies; MIT licence) is the natural simulation substrate but contains **no adversary**. 2609.19630 shows LLM-only authorization still produces 1.2–13.7 % false executes. No public benchmark combines in-car tools + multi-turn attacker + vehicle-state context: this is the thesis gap.

**Standards.** Nothing certifies an LLM agent. ISO/SAE 21434 TARA supplies the vocabulary (assets, damage/threat scenarios, S/F/O/P impact, attack-feasibility via attack potential/CVSS/attack vector, risk value 1–5); UN R155/R156 oblige CSMS/SUMS at type approval; ISO/PAS 8800:2024 frames AI safety; the EU AI Act's high-risk obligations were deferred by Reg. (EU) 2026/1744 to 2 Dec 2027 (Annex III) / 2 Aug 2028 (Annex I) (snippets). The thesis should *use* 21434 structure + OWASP/ATLAS IDs as taxonomy, and *propose* (not claim) a mapping from measured ASR / turns-to-compromise / attacker cost to attack feasibility.

---

## 2. What real in-vehicle assistants can do

Status key: **SHIPPED** = publicly stated as available in series vehicles; **ANNOUNCED** = stated for a future date; **DEMO** = supplier/show demo.

| OEM / product | Capabilities / tool calls (public statements) | On-board vs cloud | Status | Source (tier, verification) | Date |
|---|---|---|---|---|---|
| **Volkswagen IDA + ChatGPT via Cerence Chat Pro** (MEB / MQB evo, VW Group brands) | Native IDA: "control the infotainment, navigation, and air conditioning"; IDA "automatically prioritises whether a vehicle function should be executed, a destination searched or the temperature adjusted. If the request cannot be answered by the Volkswagen system, it is forwarded anonymously to AI". Security/privacy statement: "ChatGPT does not gain access to any vehicle data; questions and answers are deleted immediately". Outlook quoted in the same release (Cerence CEO): "together Volkswagen and Cerence will explore collaboration to design a new, large-language-model-based (LLM) user experience as the foundation of Volkswagen's next-generation in-car assistant" — no later launch found (WebSearch, Nov 2026). | Hybrid: native routing in vehicle system; ChatGPT backend in cloud | SHIPPED ("standard feature from the second quarter of 2024") | volkswagen-group.com article 18052 "World premiere at CES: Volkswagen integrates ChatGPT into its vehicles" (T4 official press, PRIMARY-READ) | CES 9–12 Jan 2024 |
| **Volkswagen Group China — CEA onboard AI Agent; CEA 2.0 Multi-Agent** | "onboard AI Agent that incorporates a locally trained large language model (LLM) as its natural language interface … executes complex, multi-system actions, and makes contextual decisions"; CEA 2.0 "Multi-Agent AI system – comprising coordinated agents for driving, cockpit experience, and ecosystem services"; "integrate intelligent driving and cockpit control into a unified system". Privacy statement: "The system runs entirely onboard and ensures that personal information never leaves the vehicle". Partner list (Tencent/Alibaba/Baidu/Horizon) and the restaurant-reservation example appear only in third-party press (SNIPPET, UNVERIFIED). | Stated on-board | ANNOUNCED (H2 2026 for "all vehicles built on the CEA"; CEA 2.0 "to be launched in 2027") | volkswagen-group.com press release 20333 "Auto China 2026: … Agentic AI Roadmap for China" (T4 official press, PRIMARY-READ) | Media night 21 Apr 2026 |
| **Mercedes-Benz MBUX Virtual Assistant (MB.OS, CLA)** | Built on Google Cloud "Automotive AI Agent" (Gemini) with Google Maps Platform data; complex multi-turn dialogue, retains memory of conversations, follow-ups e.g. restaurant reviews; existing ChatGPT/Bing "general knowledge". Pre-history: optional US ChatGPT beta from 16 June 2023 "for over 900,000 vehicles equipped with the MBUX infotainment system", via Azure OpenAI Service, delivered OTA, ~3-month trial (Mercedes press 15 June 2023 via snippets; also ref [9] in 2609.19630). | Cloud (Google Cloud; Azure OpenAI for the 2023 beta) — SNIPPET | ANNOUNCED for CLA in 2025; shipping status not verified here | WebSearch snippets of Google Cloud / press coverage (T4, SNIPPET; group.mercedes-benz.com blocked) | 13 Jan 2025 |
| **BMW Intelligent Personal Assistant + Amazon Alexa+ technology** | "Large Language Model (LLM) … capable of formulating its own responses"; chained requests and follow-ups; Amazon-account linking for music/news; German/English at launch. Vehicle-function scope not stated in snippets. | Not stated in snippets (Inference: cloud LLM) | ANNOUNCED: iX3 customers in Germany and US "starting in the second half of 2026", then BMW OS 9 and X vehicles | BMW press release T0454477EN (CES 2026) via WebSearch snippet (T4, SNIPPET); also cited as ref [1] in 2609.19630 | Jan 2026 |
| **Google Gemini in cars with Google built-in** (replaces Google Assistant) | Natural-language control of "dual-zone climate controls, … heated seats, … windshield wipers"; navigation with Google Maps; summarise incoming messages and hands-free replies; owner's-manual Q&A; EV charge status. One analysis notes it "does not mean Gemini controls safety-critical driving systems". | Not verified (Inference: cloud Gemini + vehicle API) | SHIPPED (rollout start, US/English first) per snippets | Google announcement 30 Apr 2026 via WebSearch snippets (T4, SNIPPET) | 30 Apr 2026 |
| **Gemini on Android Auto** (phone projection, not built-in) | Gemini replaces Google Assistant on the projected phone UI; requires the user to have switched to Gemini on the phone; vehicle-function control not stated. | Phone + cloud | SHIPPED (rollout announced ~20 Nov 2025; uneven availability reported Jan–Apr 2026) | TechCrunch / Android Authority / 9to5Google snippets; blog.google "Gemini is here for Android Auto" (T4, SNIPPET) | Nov 2025 |
| **Tesla Grok** | 2025: chatbot that "does not issue commands to your car"; 2025 Holiday Update: describe destination; update 2026.26 (late July 2026): climate, mirrors, wipers, seat heaters, navigation, Sentry/Dashcam, calls, music; only Ryzen-based cars. | Not verified (Inference: cloud xAI) | SHIPPED per enthusiast press | notateslaapp / electrek / techradar snippets (T4, SNIPPET) | Jul 2025 → Jul 2026 |
| **Stellantis / DS Automobiles** | ChatGPT via "SoundHound AI powered by ChatGPT API" on DS IRIS; pilot from Oct 2023; factory-installed in DS 3/4/7/9 from March 2024. Separate Mistral AI in-car assistant (natural-language user manual, warning lights) "explored/developed". | Cloud (Inference) | ChatGPT SHIPPED; Mistral assistant ANNOUNCED/in development | media.stellantis.com snippets (T4, SNIPPET) | 2023–2026 |
| **Cerence xUI / CaLLM family** (supplier) | "multi-turn, multi-domain conversations with tool calling, planning and execution, and context-aware routing between on-device models and cloud agents, with graceful fallback when connectivity is limited"; CaLLM Edge SLM; demo in a GWM car (Auto Shanghai 2025); Microsoft 365 Copilot orchestration (IAA 2025). | Hybrid edge + cloud | DEMO / platform | Cerence press releases & blog via snippets (T4, SNIPPET) | 2025 |
| **NVIDIA DRIVE AGX (Orin/Thor "AI Box")** (stack supplier) | Speech → NeMo Agent Toolkit orchestration → TensorRT(-Edge)-LLM → TTS; "heavy tasks like trip planning go to cloud agents, while local AI handles immediate and safety-critical responses" (snippet paraphrase). Partners named: Bosch (with Microsoft), PATEO, MediaTek, SoundHound, Cerence (with NeMo Guardrails). | Hybrid | DEMO / platform | NVIDIA developer blog via snippets (T4, SNIPPET) | 2025–2026 |
| **Chinese OEMs** (XPeng, Li Auto, NIO, BYD et al.) | XPeng: natural commands such as parking near a mall entrance; Li Auto CEO: in-car interaction + autonomous driving converge into a "super intelligent agent"; NIO NOMI; DeepSeek integrations reported. No tool lists found. | Not verified | Mixed; mostly ANNOUNCED | Reuters-syndicated coverage (Apr 2026), CnEVPost (Jan 2026) via snippets (T4, SNIPPET) | 2026 |
| **Renault + OpenAI** | "integration of large language models, including ChatGPT-4o, through its partnership with OpenAI" — claim made in the DriveSafe introduction citing "Renault UK, 2026". | Not verified | Not verified | Secondary (V-10, T3) — UNVERIFIED primary | 2026 |

**Reference tool surface in simulation (for comparison):** CAR-bench exposes 58 tools incl. `open_close_window`, `open_close_sunroof`, `open_close_trunk_door`, `set_fog_lights`, `set_head_lights_high_beams`, `set_new_navigation`, `navigation_replace_final_destination`, `get_entries_from_calendar`, `send_email`, `call_phone_by_number`, `search_poi_along_the_route`, `get_user_preferences` (PRIMARY-READ from the cloned repo `car_bench/envs/car_voice_assistant/tools/`). No door-lock, no ADAS/driving tool.

Inference: the realistic action space for 2024–2026 production agents is comfort (climate, seats, windows, lights), navigation/charging, media, and communication/productivity (messages, calls, calendar, e-mail, reservations). Door locks, ADAS settings and driving functions are either absent from public statements or explicitly excluded (Gemini analysis; VW "no vehicle data" for ChatGPT). The thesis' high-impact scenarios should therefore emphasise *navigation integrity, privacy exfiltration via communication tools, distraction, and comfort actuations in unsafe vehicle states* — and treat "driving-function control" as a forward-looking scenario motivated by VW CEA 2.0 / Li Auto "super agent" announcements.

---

## 3. Realistic attacker channels for an in-vehicle agent

| # | Channel | Who controls it | Example | Evidence it is realistic (source) |
|---|---|---|---|---|
| C1 | Direct speech/text by the driver | Owner/driver (malicious, curious, or coerced) | Jailbreak to skip a confirmation; "turn off lane assist" at highway speed | 2609.19630 Table 2 example "Turn off lane assist." Driver, Highway speed → REQUIRE_MANUAL_CONTROL (V-02, PRIMARY-READ); DriveSafe refusal failures (V-10) |
| C2 | Passenger / child / unauthenticated speaker | Co-occupant | "Unlock all doors." by passenger while parked → REQUIRE_CONFIRMATION | 2609.19630 speaker roles "driver, passenger, child, or unknown", authentication status, replay suspicion (V-02) |
| C3 | Inaudible/acoustic injection from outside the cabin | Nearby attacker with a device on the windshield | ShieldSpear: piezo element on windshield exterior acts as speaker+microphone, emulates driver voiceprint | CCS 2025: "90.9% end-to-end success rate in injecting faked voice commands into AVAs", "five mainstream vehicles" (V-07, ABSTRACT-ONLY); Light Commands (USENIX Sec 2020): light-injected voice commands "at distances up to 110 meters" could "unlock and start various vehicles connected to the target's Google account (e.g., Tesla and Ford)" (V-24); inaudible-acoustic study reports success "around 60%" from "over 100 feet" (V-28, arXiv) |
| C4 | Incoming messages read aloud / summarised (SMS, messenger, e-mail) | Any sender | Hidden (invisible-Unicode) instructions executed when driver asks to read the message | VicOne blog May 2025 scenario (V-16, T4 SNIPPET); e-mail-subject injections against Gemini (V-08); Gemini built-in summarises messages (§2, SNIPPET) |
| C5 | Calendar invitations / productivity data | Anyone who knows the victim's address | Injection in invite title → agent changes navigation, calls, e-mails | V-08: attacks "triggered by an indirect prompt injection in the title of a meeting invitation"; CAR-bench pairs calendar, navigation, e-mail and call tools and describes "navigating to a meeting's location from an calender event" (V-01) |
| C6 | POI / charging-station / restaurant listings, reviews | Listing owners, review writers, map-data suppliers | Injected text in POI name/description/review steers route, charger choice or reservation | Mercedes/Gemini follow-ups on restaurant reviews (§2, SNIPPET); CAR-bench POI DB "over 130,000 Points of Interests" with "LLM-generated names" (V-01). Inference: no automotive demonstration found — open scenario (§7) |
| C7 | Web / general-knowledge results | Web authors, SEO spammers | Poisoned answer in a ChatGPT/Bing fall-back | VW ChatGPT fall-back and Mercedes Bing (§2). Inference: standard indirect-injection surface; no in-car demo found |
| C8 | Partner / ecosystem agents (A2A), reservation and payment services | Third-party service providers, compromised agents | A2A `TextPart`/`DataPart` payload carries instructions with same privilege as user input | AgentHeLLM analysis: "no protocol-level distinction exists between human-originated and agent-originated instructions" (V-09, PRIMARY-READ); VW CEA 2.0 "ecosystem services" agent (§2) |
| C9 | Long-term memory / preference store | Earlier sessions, other drivers of a shared/rental car, any channel that can write memory | Persistent poisoned preference ("always route via X", "auto-confirm e-mails") | CarMem preference memory design (V-03); Mercedes assistant "retain memory of conversations" (§2 SNIPPET); V-08 threat class "Permanent Memory Poisoning"; ATLAS AML.T0080.000 |
| C10 | Tool / function library and its updates (supply chain, OTA) | Tier-1 / third-party tool providers, update pipeline | Malicious tool description hijacks tool selection | FuncPoison ASR@3 86.3 % on AgentDriver (V-05); R156 SUMS governs updates (§4) |
| C11 | Visual scene text read by a VLM (signs, screens, other vehicles) | Anyone in the environment | Sign text "Go Onward" makes DriveLM proceed instead of stop | CHAI: 81.8 % on DriveLM (simulation), ≥87 % on a real robotic vehicle (V-06). Relevant only if cockpit and driving agents are unified (VW CEA 2.0) |
| C13 | Paired phone / projection (Android Auto) and cloud-linked accounts | Owner's phone ecosystem; anyone who can reach the phone assistant | Phone-side Gemini on Android Auto ingests the same messages/calendar; home assistant linked to the car account issues vehicle commands | Gemini on Android Auto rollout Nov 2025 (§2, SNIPPET); Light Commands reached "Tesla and Ford" via Google account (V-24) |
| C12 | Classical compromise of infotainment/telematics | Remote attacker | Bluetooth RCE in infotainment, microphone access, persistence | Black Hat Asia 2025 Nissan Leaf; Black Hat Europe 2024 VW MIB3 (V-18, T4 SNIPPET). Outside simulation scope; bounds attacker capability |

---

## 4. Standards & regulation map

| Framework | Type | What it requires (as verified) | How the thesis can use it (without claiming compliance) | Verified via |
|---|---|---|---|---|
| **UN Regulation No. 155** (Cyber security & CSMS) | UNECE regulation under the 1958 Agreement (T2) | Cyber Security Management System + vehicle-type cyber risk assessment; Annex 5 catalogue of threats/mitigations (Part A threats). Dates (snippets): adopted by WP.29 June 2020; "entered into force on January 22, 2021"; in EU/1958-Agreement type approval "from July 2022 … all new vehicle types" and from July 2024 all newly produced vehicles. | Map each thesis threat scenario to an Annex 5 Part A category (as V-13 did: "all 32 UN R155 Annex 5 Part A threat categories"). State explicitly that simulated ASRs are *inputs to* a CSMS risk process, not compliance evidence. | WebSearch snippets only (unece.org 403) — UNVERIFIED primary |
| **UN Regulation No. 156** (Software update & SUMS) | UNECE regulation (T2) | Software Update Management System as type-approval condition; same entry-into-force date (22 Jan 2021) and phase-in as R155 (snippets). Ongoing amendments on software identification (snippet). | Treat model weights, system prompts, policies and tool schemas of an in-car agent as *software that is updated OTA* → FuncPoison-type tool poisoning (C10) and "rollback of guardrail version" scenarios belong under SUMS. | WebSearch snippets — UNVERIFIED primary |
| **ISO/SAE 21434:2021** Road vehicles — Cybersecurity engineering | International standard (T2) | TARA activities: "asset identification, threat scenario identification, impact rating, attack path analysis, attack feasibility rating, risk value determination, and risk treatment decision"; damage scenarios rated in "safety, financial, operational, and privacy (S, F, O, P) on four levels from negligible to severe"; attack feasibility "on four levels from very low to high"; "the risk value, an integer from 1 to 5". Annex G gives three example feasibility approaches (attack-potential, CVSS-based, attack-vector-based); none is mandated (snippet). Revision work item (ISO/SAE AWI 21434) reported by one guide — UNVERIFIED. | Backbone of the thesis threat model and the mini-TARA below. Use the *example* Annex G values only as a documented convention. | Secondary, PRIMARY-READ of Breier & Hou 2026 (V-15, arXiv 2610.09697 §II-A, Table II) which quotes ISO/SAE 21434:2021 Annex G/H/E; WebSearch snippets. Standard text itself not opened. |
| **ISO 26262** (Functional safety) | International standard (T2) | Hazard analysis and risk assessment (HARA) for E/E malfunctions: Severity × Exposure × Controllability → ASIL A–D or QM. Severity classes as quoted by a secondary arXiv paper (2602.05157): "S0: No injuries; S1: Light and moderate injuries; S2: Severe and life-threatening injuries (survival probable); S3: Life-threatening injuries (survival uncertain)"; controllability C0–C3. 21434 safety impact rating is described as referring to ISO 26262 severity (snippet). | Rate the *safety* column of damage scenarios (window/sunroof opened at speed, distraction, wrong route) by analogy to S-classes; joint HARA+TARA as in V-14. | Snippets/secondary — UNVERIFIED wording |
| **ISO 21448:2022** (SOTIF) | International standard (T2) | Scope (snippet of standard preview): "absence of unreasonable risk due to hazards resulting from functional insufficiencies of the intended functionality or by reasonably foreseeable misuse by persons"; excluded: "faults covered by the ISO 26262 series; cybersecurity threats"; "Feature abuse is not in scope of this document". A revision (ISO/WD 21448) is reported in development (snippet). | Clean split for the thesis: *non-adversarial* LLM failures (CAR-bench hallucination/disambiguation errors, ambiguous driver requests) = SOTIF-type "functional insufficiency/foreseeable misuse"; *adversarial* manipulation = explicitly out of SOTIF → ISO/SAE 21434. Use this split to separate "Evaluate" baselines from attack results. | WebSearch snippets of ANSI webstore preview / vendor guides — UNVERIFIED primary |
| **ISO/PAS 8800:2024** Road vehicles — Safety and artificial intelligence | Publicly Available Specification (T2) | "Edition 1 2024-12", 172 pages, ISO/TC 22/SC 32; scope: safety-related E/E systems that use AI in series-production road vehicles; addresses vehicle-level risks from AI "output insufficiencies, systematic errors, and random hardware errors"; "focuses mainly on machine learning"; excludes development of AI elements outside the vehicle (snippets of iso.org/national-body mirrors). | Cite to argue that an actuating in-car LLM agent is an AI element whose output insufficiencies need a safety argument; note gap: cloud LLMs (VW ChatGPT, Gemini) sit outside the vehicle and outside PAS 8800 scope (Inference). | WebSearch snippets — UNVERIFIED primary |
| **ISO/IEC 42001:2023** AI management system | International standard (T2) | Published December 2023; requirements for establishing, operating and improving an AI management system; AI risk assessment (cl. 6.1.2), risk treatment (6.1.3), AI system impact assessment (6.1.4, operational 8.4), Annex A reference controls (snippets of vendor guides/national adoptions). | Context only: organisational wrapper in which an OEM would place AI red-teaming results; thesis does not assess an organisation. | WebSearch snippets — UNVERIFIED primary |
| **EU AI Act** Reg. (EU) 2024/1689, amended by **Reg. (EU) 2026/1744** ("Digital Omnibus on AI") | EU regulation (T2) | 2026/1744 dated 8 July 2026, OJ 24 July 2026, in force 27 July 2026 (snippets). High-risk obligations apply "from 2 December 2027 for stand-alone systems" (Annex III) and "from 2 August 2028" for Annex I product-embedded systems (snippets, multiple law-firm sources + EUR-Lex result titles). Vehicle type-approval acts (Reg. 2018/858, 2019/2144) are listed in Annex I **Section B**; for those, Art. 2(2) limits applicable provisions — consolidated text reportedly "only Article 6(1), Article 60a and Articles 102 to 112 apply" (snippet; wording differs between versions — UNVERIFIED). Art. 15 (for high-risk systems) requires "an appropriate level of accuracy, robustness, and cybersecurity" throughout the lifecycle and names threats incl. "data poisoning", "model poisoning", "adversarial examples or model evasion" (AI Act Service Desk snippet); the paragraph-5 wording "resilient against attempts by unauthorised third parties to alter their use, outputs or performance" is from an unofficial compilation only (UNVERIFIED). | Do **not** classify the in-car assistant as high-risk; say obligations for vehicle AI come mainly through type-approval delegated acts. Use Art. 15 vocabulary only as motivation for robustness/cybersecurity testing evidence. | WebSearch snippets incl. EUR-Lex result titles; EUR-Lex WAF prevented reading — UNVERIFIED primary |
| **UNECE WP.29 IWG on AI; GRVA** | UN working-party documents (T2/T3) | WP.29 adopted revised Terms of Reference for the AI Informal Working Group at session 198 (March 2026); draft "AI Reference Document (AI-09-06/Rev.3)" not finished; IWG requested extension "to deliver the AI Reference Document as a working document no later than June 2027"; GRVA drafts of a UN Regulation and a GTR on Automated Driving Systems (2026) reference ISO PAS 8800 (snippets). | Shows that UN-level AI guidance for vehicles is still draft in Nov 2026 → thesis evidence is timely; do not cite draft content as requirements. | WebSearch snippets — UNVERIFIED primary |
| **NIST AI 100-2 E2025** Adversarial ML taxonomy | Government technical report (T3) | March 2025; authors Vassilev, Oprea, Fordyce, Anderson, Davies, Hamin; DOI 10.6028/NIST.AI.100-2e2025; covers predictive and generative AI incl. direct and indirect prompt injection (§3.4 "Indirect Prompt Injection Attacks and Mitigations") and agent security (snippets). | Terminology for attack classes (evasion/poisoning/privacy/misuse; direct vs indirect injection). | Snippets; NIST hosts blocked — UNVERIFIED primary |
| **OWASP Top 10 for LLM Applications 2025** | Industry catalogue (T4) | LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Supply Chain · LLM04 Data and Model Poisoning · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM08 Vector and Embedding Weaknesses · LLM09 Misinformation · LLM10 Unbounded Consumption | Label each attack class (§5). | PRIMARY-READ genai.owasp.org/llm-top-10/ |
| **OWASP Top 10 for Agentic Applications for 2026** | Industry catalogue (T4) | "Version 2026, December 2025": ASI01 Agent Goal Hijack · ASI02 Tool Misuse and Exploitation · ASI03 Identity and Privilege Abuse · ASI04 Agentic Supply Chain Vulnerabilities · ASI05 Unexpected Code Execution (RCE) · ASI06 Memory & Context Poisoning · ASI07 Insecure Inter-Agent Communication · ASI08 Cascading Failures · ASI09 Human-Agent Trust Exploitation · ASI10 Rogue Agents. Cross-refs: "ASI01 corresponds to T06 Goal Manipulation"; ASI02 "maps to T2 Tool Misuse"; ASI06 "maps to T1 Memory Poisoning". | Primary agent-level taxonomy for attack classes and defenses; ASI02 mitigation 1 reads "Least Agency and Least Privilege for Tools. Define per-tool least-privilege profiles" (PDF) — directly reusable for a vehicle-function permission layer. | PRIMARY-READ (PDF from genai.owasp.org resource page, published 9 Dec 2025) |
| **OWASP Agentic AI – Threats and Mitigations** | Industry guide (T4) | "Version 1.1, December 2025", licence "CC BY-SA 4.0"; threat IDs T1 Memory Poisoning, T2 Tool Misuse, T3 Privilege Compromise, T4 Resource Overload, T5 Cascading Hallucination Attacks, T6 Intent Breaking & Goal Manipulation, T7 Misaligned & Deceptive Behaviors, T8 Repudiation & Untraceability, T9 Identity Spoofing & Impersonation, T10 Overwhelming Human-in-the-Loop, T11 Unexpected RCE and Code Attacks, T12 Agent Communication Poisoning, T13 Rogue Agents in Multi-Agent Systems, T14 Human Attacks on Multi-Agent Systems, T15 Human Manipulation, T16 Insecure Inter-Agent Protocol Abuse, T17 Supply Chain Compromise. (v1.0 was released 17 Feb 2025 per the resource page.) | Threat-model checklist; note AgentHeLLM's critique that these categories mix methods and consequences (V-09). | PRIMARY-READ (PDF from genai.owasp.org) |
| **MITRE ATLAS** (release 2026.10, 28 Oct 2026) | Industry knowledge base (T4) | Technique IDs in §5 verified in the official data file `dist/v6/ATLAS-2026.10.yaml`; case study AML.CS0063 "Prompt-Based Attacks Against Gemini via Calendar Invitations". Note: the legacy `dist/ATLAS.yaml` (v5.6.0) is marked "deprecated"; some old IDs (e.g., AML.T0056, AML.T0104) are not in 2026.10. | Technique IDs for each attack class; case study for the calendar channel. | PRIMARY-READ of github.com/mitre-atlas/atlas-data (commit 2026-10-28); atlas.mitre.org web UI not parsable (SPA) |

### 4.1 Worked mini-TARA template (ISO/SAE 21434-style; simulation only)

Example item: *in-car LLM assistant with calendar, navigation and e-mail tools* (tool names from CAR-bench). Rating scales follow the ISO/SAE 21434:2021 example scales as quoted in V-15; the risk matrix of Annex H is **not reproduced** (not verified).

| TARA step | Content |
|---|---|
| Item / boundary | LLM agent + tools `get_entries_from_calendar`, `set_new_navigation`, `navigation_replace_final_destination`, `send_email` (CAR-bench policy LLM-POL:004 requires explicit confirmation for tools whose description starts with REQUIRES_CONFIRMATION); external data: calendar entries from third parties. |
| Assets (property) | A1 navigation destination/route (integrity); A2 driver location, calendar, contacts (confidentiality); A3 driver attention (availability of safe driving task — cf. AgentHeLLM "Life and Bodily Health"). |
| Damage scenario | DS-1: vehicle is navigated to an attacker-chosen location without the driver noticing; DS-2: driver's meetings and current location are e-mailed to the attacker; DS-3: repeated confirmations/alerts distract the driver while moving. |
| Threat scenario | TS-1: tampering of A1 via indirect prompt injection in a calendar entry processed by the agent (ATLAS AML.T0051.001 → AML.T0053); TS-2: information disclosure of A2 via `send_email` (AML.T0086); TS-3: denial of A3 via induced dialogue loops (AML.T0034.002). |
| Impact rating (per category: negligible / moderate / major / severe) | DS-1: Safety moderate (assumption: unfamiliar route, no direct crash mechanism), Financial minor→moderate, Operational moderate, Privacy negligible. DS-2: Privacy major/severe (location + calendar), others negligible. DS-3: Safety major (assumption, to be justified with distraction literature cited in V-09). *All ratings are illustrative assumptions for the thesis, not OEM ratings.* |
| Attack path | AP-1: attacker learns victim e-mail → sends invite with payload in title/location → invite auto-added (depends on calendar settings, cf. V-08 §4.2.2) → driver asks "What's my next meeting?" → agent calls `get_entries_from_calendar` → payload enters context → agent calls `navigation_replace_final_destination` and/or `send_email` (attempting to obtain or bypass confirmation). |
| Attack feasibility (attack-potential approach, Annex G example values via V-15) | Elapsed time ≤1 day (0); Specialist expertise layman (0) or proficient (3); Knowledge of item public (0) or restricted (3) (needs e-mail address — cf. V-08 "Restricted (2) - a user's email address is required"); Window of opportunity unlimited (0); Equipment standard (0). Sum 0–6 → **High** (scale: "0–13 high (H), 14–19 medium (M), 20–24 low (L), ≥25 very low (VL)"). |
| Risk value | Look up (impact, feasibility) in the Annex H example matrix → integer 1–5. Inference: high feasibility with major/severe privacy impact lands at the upper end; not computed here because the matrix was not verified. |
| Risk treatment | Reduce: (i) deterministic authorization gate outside the LLM ("independently enforced tool permissions, rule-based validators, and vehicle-state safety gates", V-02 §7); (ii) provenance tagging and "no write-tool after untrusted read in the same turn" (cf. V-08 "Agent/Tool Chaining Prevention" and "Control Flow Integrity (CFI)"); (iii) confirmations that display the *source* of the instruction; (iv) memory write-gating. Retain: residual risk documented per DS. Derive cybersecurity goals, e.g., "CG-1: navigation destination changes shall only originate from occupant utterances". |

### 4.2 PROPOSAL (thesis contribution, not part of any standard): feeding measured attack metrics into attack-feasibility rating

ISO/SAE 21434's attack-potential factors (elapsed time, expertise, knowledge, window of opportunity, equipment) contain **no success-probability factor**, while the thesis will measure ASR, turns-to-compromise and attacker cost. Proposed bridge (to be validated with expert review and sensitivity analysis):

1. **ASR → attempts → elapsed time.** For per-attempt success probability *p* (measured ASR with confidence interval over seeds/trials), attempts needed for 95 % cumulative success: n95 = ⌈ln 0.05 / ln(1 − p)⌉. Elapsed time ≈ preparation time (payload search: optimisation queries × time/query) + n95 × (turns-to-compromise × time/turn + waiting time for the trigger, e.g. driver asking about the calendar). Map to Annex G buckets (≤1 day / ≤1 week / ≤1 month / ≤6 months / >6 months).
2. **Turns-to-compromise → window of opportunity.** Remote asynchronous channels (C4–C8) → unlimited; channels requiring the attacker to speak in the cabin over many turns (C1/C2) or to be near a moving vehicle (C3) → moderate/difficult. Long-horizon attacks needing >N turns within one driving session are capped by realistic session length (Inference; needs data).
3. **Attacker cost → equipment.** Commercial API/laptop only → standard; GPU optimisation (e.g., GCG-style suffix search) → specialized; custom hardware (piezo/ultrasonic, V-07) → bespoke.
4. **Attack method → expertise; access level → knowledge.** Template/manual payloads → layman/proficient; gradient-based or learned attacker → expert. Black-box with public docs → public; needs tool schema/system prompt → restricted/confidential; white-box weights → strictly confidential.
5. **CVSS-style alternative.** AV from channel (network for C4–C8; adjacent/physical for C2/C3), AC = High when measured ASR is below a pre-registered threshold, UI = Required when a driver action triggers the payload (V-08 calls this "1/2-click").
6. Report all three Annex G approaches side by side, because V-15 shows they can disagree strongly (attack-vector-based rates every physical path "very low … whatever the asset").
7. Measure ASR under *repeated attempts* and *adaptive* attackers, not single-shot: the US AISI (NIST) agent-hijacking blog lists as an insight that "testing the success of attacks on multiple attempts may yield more realistic evaluation results" (V-29, SNIPPET), and a secondary summary reports adaptive red-teaming raised measured ASR "from 11% to 81%" (UNVERIFIED). Inference: single-shot ASR systematically understates feasibility; pass@k / pass^k-style reporting (as in CAR-bench) maps naturally to "attacker gets k tries".

### 4.4 Mapping the thesis channels to UN R155 Annex 5 Part A threat titles

Threat titles as reproduced in V-13 (Table B.1, "Mapping to UN R 155 Annex 5 Threats"); the UNECE text itself was not opened, so numbering/wording is SECONDARY.

| R155 Annex 5 Part A title (as reproduced in V-13) | Thesis channels / attack classes (Inference) |
|---|---|
| 4. Spoofing of messages or data received by the vehicle | C3 spoofed driver voice; C4–C6 forged message/calendar/POI content |
| 7. Information can be readily disclosed … | Exfiltration of location/calendar/contacts via agent output |
| 9. An unprivileged user is able to gain privileged access to vehicle systems | C2 passenger/child obtains driver-only actions; role confusion |
| 11. Messages received by the vehicle (for example X2V or diagnostic messages), or transmitted within it, contain malicious content | Indirect prompt injection in any ingested content (C4–C8) |
| 12. Misuse or compromise of update procedures | C10 poisoned tool schema / model / guardrail update |
| 15. Legitimate actors are able to take actions that would unwittingly facilitate a cyber-attack | Driver confirms an injected action (S6 confirmation fatigue) |
| 17. Hosted 3rd party software, e.g. entertainment applications, used as a means to attack vehicle systems | C8 third-party/partner agents and apps |
| 24. Disruption of systems or operations | Dialogue loops / resource exhaustion; distraction |
| 25. Manipulation of vehicle parameters | Unsafe comfort actuation (windows, sunroof, lights) or route change via tools |
| 27. Parts or supplies could be compromised to permit vehicles to be attacked | C10 supplier-provided tools/models (FuncPoison) |
| 31. Unintended transfer of data can occur | Agent sends data via e-mail/call/message tools (AML.T0086) |
| 32. Physical manipulation of systems can enable an attack | C3 device on the windshield (V-07) |

### 4.3 Automotive security research culture — what evidence the venues accept

| Venue | What is verified | Evidence norms (quoted) | Source / verification |
|---|---|---|---|
| **USENIX VehicleSec** (4th edition 2026, Baltimore, 10–11 Aug 2026) | Topics explicitly include "AI/ML/DNN/LLM … simulation, digital twin, multi-agent protocol/system design, and human-machine interaction". Regular and SoK papers "at most 18 pages" camera-ready; short/WIP "at most 10 pages". | Ethics: "We expect authors to carefully consider and address the potential harms … Failure to do so may result in the rejection of a submission"; vulnerabilities: authors "should discuss in detail the steps they have already taken or plan to take … (e.g., by disclosing vulnerabilities to the vendors)"; artifact evaluation with a "Distinguished Artifact Award". | usenix.org VehicleSec '26 CFP (T2 venue; PRIMARY-READ) |
| **escar Europe** (24th, Bonn, 17–18 Nov 2026) | Scientific track: full papers up to 15 pages, peer-reviewed, citable DOI; presentation (industry) track: 2–3-page talk description, not anonymised, abstracts in proceedings; "mere product or company presentations are discouraged". 2025 example: STAF (V-25). | Industry-heavy audience; practical relevance to development processes valued (Inference from track design). | EasyChair CFP via WebSearch snippet (escar.info blocked) — UNVERIFIED primary |
| **ACM CSCS** (Computer Science in Cars Symposium) | 2023 edition Darmstadt (5 Dec 2023); a "CSCS '25 Taipei" workshop paper is mentioned in a snippet. | Not verified. | Snippets only — UNVERIFIED |
| **SAE (WCX technical papers)** | Example: V-30 is a "PRE-PRINT FOR SAE WCX 2026 CONFERENCE" arguing safety-process (ISO 26262/SOTIF) for AI features. | Genre: process/framework argumentation by industry authors; acceptance criteria not verified. | arXiv 2602.05157 header (PRIMARY-READ of header) |
| **IEEE VNC** | Not verified in this session. | — | UNVERIFIED |
| **Top-4 security venues** (CCS, USENIX Security, S&P, NDSS) | Automotive voice-assistant work does appear there: V-07 (CCS 2025), V-24 (USENIX Security 2020). | Both demonstrate on real devices/vehicles ("five mainstream vehicles"; Tesla/Ford via Google account). | V-07, V-24 |

**Bridging examples (ML/LLM attacks ↔ vehicle TARA):** V-08 (21434-adapted TARA for LLM assistants, 14 production attacks), V-09 (AgentHeLLM: TARA-style separation of assets and attack paths for in-car LLM agents), V-13 (VehicleSec '26: TARA + ATLAS + OWASP mapped to R155 Annex 5), V-14 (HARA + TARA for DNN limitations).

Inference — implications for a simulation-only thesis: automotive venues accept simulation and digital-twin evidence (explicit VehicleSec topic), but reviewers expect (i) a threat model anchored in real, public product capabilities (§2) and in R155/21434 vocabulary, (ii) an ethics/harm statement and a disclosure position (here: no real products attacked, so state that no vendor disclosure is needed and why), (iii) released artifacts, and (iv) restraint in claims — results are TARA *inputs* and not evidence about any specific vehicle.

---

## 5. OWASP / MITRE mapping

Only IDs verified in OWASP LLM Top 10 2025 (web page), OWASP Agentic Top 10 2026 (PDF), OWASP Agentic T&M v1.1 (PDF) and ATLAS release 2026.10 (official data file).

| Agent-attack class (in-vehicle example) | OWASP LLM 2025 | OWASP ASI 2026 | OWASP Agentic T&M v1.1 | MITRE ATLAS 2026.10 |
|---|---|---|---|---|
| Direct prompt injection / jailbreak by occupant (C1, C2) | LLM01 | ASI01 | T6 | AML.T0051.000 Direct; AML.T0054 LLM Jailbreak |
| Indirect prompt injection via message, calendar, POI, web (C4–C7) | LLM01 | ASI01 | T6 | AML.T0051.001 Indirect; AML.T0099 AI Agent Tool Data Poisoning; AML.T0093 Prompt Infiltration via Public-Facing Application |
| Delayed/triggered payload ("when the user says thanks") | LLM01 | ASI01 | T6 | AML.T0051.002 Triggered |
| Unsafe vehicle-function invocation (window/sunroof/lights in unsafe state; route change) | LLM06 Excessive Agency | ASI02 | T2 | AML.T0053 AI Agent Tool Invocation |
| Exfiltration via e-mail/call/message tools | LLM02 | ASI02 | T2 | AML.T0086 Exfiltration via AI Agent Tool Invocation |
| Speaker/role confusion (passenger acts as driver; agent output treated as user) | — | ASI03 | T3, T9 | — (no specific technique verified) |
| Long-term memory / preference poisoning (C9) | LLM04 | ASI06 | T1 | AML.T0080 AI Agent Context Poisoning; AML.T0080.000 Memory; AML.T0080.001 Thread |
| Knowledge-base / manual / POI-DB poisoning (RAG) | LLM04, LLM08 | ASI06 | T1 | AML.T0070 RAG Poisoning; AML.T0071 False RAG Entry Injection |
| Tool-definition / tool-supply-chain poisoning (C10) | LLM03 | ASI04 | T17 | AML.T0110 AI Agent Tool Poisoning (.000 Definition and Instructions, .002 Runtime Response); AML.T0115.002 Publish Poisoned AI Artifacts: AI Agent Tools |
| Partner-agent / A2A payloads (C8) | LLM01 | ASI07 | T12, T16 | AML.T0118.001 Direct Agent Communication; AML.T0143 LLM Prompt Propagation |
| Cockpit-agent → driving-agent cascade (CEA 2.0-type) | — | ASI08 | T5 | AML.T0143 LLM Prompt Propagation |
| Exploiting driver trust / confirmation fatigue | LLM09 | ASI09 | T10, T15 | AML.T0067 LLM Trusted Output Components Manipulation |
| Physical-channel injection (acoustic C3, visual scene text C11) | LLM01 | ASI01 | T6 | AML.T0041 Physical Environment Access + AML.T0051.001 |
| System-prompt / tool-schema discovery (attacker reconnaissance) | LLM07 | — | — | AML.T0069.002 System Prompt; AML.T0084.001 Tool Definitions |
| Resource exhaustion / dialogue loops (distraction, battery/cost) | LLM10 | — | T4 | AML.T0029 Denial of AI Service; AML.T0034.002 Agentic Resource Consumption |
| Harm outcome labels | — | — | — | AML.T0048.003 User Harm; AML.T0048.000 Financial Harm |

---

## 6. Source entries

### V-01 · CAR-bench — CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty
- Kirmayr (BMW Group Research & Technology / Univ. Augsburg), Stappen (BMW), André (Augsburg), 2026 · ACL 2026 Long Papers, pp. 40599–40618, anthology ID 2026.acl-long.1886 · Tier: T1 (verified via aclanthology.org page: "Pages 40599–40618", "Month July", "Year 2026")
- https://arxiv.org/abs/2601.22027 · https://aclanthology.org/2026.acl-long.1886/ · code https://github.com/CAR-bench/car-bench (+ competition repo https://github.com/CAR-bench/car-bench-ijcai)
- Key content (arXiv v1, 29 Jan 2026): "58 interconnected tools spanning navigation, productivity, charging, and vehicle control" (abstract); Table 3: "100 Base, 90 Hallucination, 50 Disambiguation. Each with 1–9 actions" (= 240 tasks), "58 total → 27 set, 29 get, 2 no-op", "19 total → 12 checked code-based, 7 with LLM-as-a-Judge", "31 dynamic states, 12 context variables", "48 Cities, 130K POIs, 1.7M Routes, 48 Weather, 100 Calendars, 100 Contacts". Results (Table 4): best overall Pass^3 GPT-5 (thinking) .54; "on Disambiguation alone, GPT-5 drops from 68% Pass@3 to 36% Pass^3" (§1). "The codebase builds on τ-bench (MIT License)" (§3.5). Navigation data "48 real European cities (Pareto Software, 2025) (CC BY 4.0)".
- Licence: both repos contain `LICENSE` = "MIT License, Copyright (c) 2026 Johannes Kirmayr" (git clone, car-bench HEAD 2026-10-12, car-bench-ijcai HEAD 2026-08-27). Dataset hosted on HuggingFace `johanneskirmayr/car-bench-dataset`: HF API reports tag `license:mit` and card `license: mit` (lastModified 2026-02-12).
- **Count discrepancy:** car-bench README text says "248 tasks across train/test splits" but its own statistics table says Base 100 / Hallucination 98 / Disambiguation 56 = **254** (train 129, test 125); the IJCAI repo README also says "254 public CAR-bench tasks". The paper says 240. Cite the version you use.
- Policies relevant to safety (wiki.md, PRIMARY-READ): LLM-POL:004 confirmation for REQUIRES_CONFIRMATION tools; AUT-POL:005 sunroof only with sunshade open; LLM-POL:008/AUT-POL:009 weather-dependent confirmations; AUT-POL:014 no high beam with fog lights; "The in-car system will never autonomously or automatically execute any action".
- Use in thesis: primary simulation substrate (tools, policies, user simulator, Pass^k). Attack layer must be added: injected content in calendar entries, POI names, e-mails, preferences; adversarial user simulator. Pass^k is a natural robustness metric (consistency under attack).
- Verification: PRIMARY-READ (paper PDF, README, LICENSE, policy wiki, tool directory)
- Inference: CAR-bench has no door-lock/ADAS tools and no adversary; its POI names are LLM-generated, which makes payload insertion into POI/calendar fields straightforward and keeps the setting synthetic (no real data).

### V-02 · Intent-to-Action — From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization
- Afroze, Zhang, Tu, Hei (Univ. of Louisiana at Lafayette; Auburn Univ.), 2026 · arXiv preprint (cs.AI, v1 17 Sep 2026) · Tier: T3 (verified via arXiv PDF)
- https://arxiv.org/abs/2609.19630
- Key content: "202-scenario benchmark with Reference Decisions under a seven-class taxonomy" (abstract); classes EXECUTE, REFUSE, CLARIFY, REQUIRE_CONFIRMATION, REQUIRE_MANUAL_CONTROL, EMERGENCY_RESPONSE, NO_TOOL_CALL (Table 1); distribution "41 EXECUTE, 57 REFUSE, 20 CLARIFY, 20 REQUIRE_CONFIRMATION, 20 REQUIRE_MANUAL_CONTROL, 16 EMERG-ENCY_RESPONSE, and 28 NO_TOOL_CALL" (§3.1). Models: llama3.2:3b, llama3.1:8b, gpt-4o, gemini-3.1-pro-preview, gemini-3.6-flash (§4.1). Table 3: Decision Alignment 40.1 % (Llama 3.2 3B), 61.4 % (Llama 3.1 8B), 83.2 % (GPT-4o), 89.1 % (Gemini 3.1 Pro Preview), 88.1 % (Gemini Flash); False Execute 3.7 %, 13.7 %, 1.2 %, 1.9 %, 1.2 % "of the 161 non-EXECUTE scenarios". Ablation (Table 4, Llama 3.2 3B): schema only 29.2 %, generic safety 28.2 % (refuses all 41 executable), structured policy 40.1 %. Conclusion: "the LLM should not serve as the final safety authority" (§7). Assumes upstream provides accurate transcription, speaker role, authentication and replay suspicion (§2.3). Limitations: synthetic, single-turn, no acoustic noise (§8). Data/code: "will release … upon acceptance" (not yet available).
- Use in thesis: (1) vehicle-state × speaker-role × tool-availability context schema for scenarios; (2) "False Execute" as safety-specific metric; (3) motivates the Defense chapter's deterministic gate outside the LLM; (4) gap: no adversary, no multi-turn — exactly what the thesis adds.
- Verification: PRIMARY-READ
- Inference: Pairing its context fields with CAR-bench's stateful tools would give a state-aware attack benchmark; the static 1–2 % false-execute rates are a *non-adversarial* floor.

### V-03 · CarMem — CarMem: Enhancing Long-Term Memory in LLM Voice Assistants through Category-Bounding
- Kirmayr, Stappen, Schneider, Matthes, André (BMW Group Research & Technology, Univ. Augsburg, TU Munich), 2025 · COLING 2025 Industry Track, anthology ID 2025.coling-industry.29 · Tier: T2 (industry track; verified via aclanthology.org volume listing)
- https://aclanthology.org/2025.coling-industry.29/ · https://arxiv.org/abs/2501.09645 · code https://github.com/johanneskirmayr/CarMem
- Key content: "F1-score of .78 to .95 in preference extraction, depending on category granularity. Our maintenance strategy reduces redundant preferences by 95% and contradictory ones by 92%, while the accuracy of optimal retrieval is at .87" (abstract). Dataset: "100 user profiles … 1,000 Extraction Conversations, 1,000 Retrieval Utterances, and 3,000 Maintenance Utterances" (§4); categories "Main Category (4) … Subcategory (11) … Detail Category (41)" (Fig. 2). Motivation cites GDPR data minimisation and EU AI Act transparency (§1).
- Use in thesis: realistic design of an in-car preference memory (what an attacker would poison: routing, restaurant, parking, charging, climate, music preferences); target for memory-poisoning attacks (C9) and for the "rental-car carry-over" scenario (§7).
- Licence: the GitHub repo (HEAD a08f8af, 2025-01-21) contains **no LICENSE file** and the README does not mention a licence (git clone). Inference: default copyright applies — reuse of code/data needs the authors' permission; cite the method instead of copying data.
- Verification: PRIMARY-READ (arXiv version + repository tree)
- Inference: no adversarial evaluation in the paper; category-bounding is a partial defense (limits what can be stored) worth testing as a baseline.

### V-04 · AgentPoison — AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases
- Chen, Xiang, Xiao, Song, Li (UChicago, UIUC, UW-Madison, UC Berkeley), 2024 · NeurIPS 2024 · Tier: T1 (venue verified via Semantic Scholar record: venue "Neural Information Processing Systems", DBLP key conf/nips/ChenXXSL24)
- https://arxiv.org/abs/2407.12784 · code https://github.com/BillChan226/AgentPoison
- Key content: attacks "RAG-based autonomous driving agent, knowledge-intensive QA agent, and healthcare EHRAgent"; "average attack success rate of ≥ 80% with minimal impact on benign performance (≤ 1%) with a poison rate < 0.1%" (abstract); driving agent is Agent-Driver (github.com/USC-GVL/Agent-Driver) (§4).
- Use in thesis: canonical memory/RAG backdoor baseline; the driving agent shows the technique transfers to automotive planning; contrast with in-cabin assistant memory (V-03).
- Verification: PRIMARY-READ (arXiv v1); venue via Semantic Scholar/DBLP metadata
- Inference: requires write access to the knowledge base — maps to C9/C10, not to a casual remote sender.

### V-05 · FuncPoison — FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems
- Long, Li (Southeast University), 2025 · arXiv (cs.CR, v2 29 Dec 2025) · Tier: T3
- https://arxiv.org/abs/2509.24408
- Key content: injects "malicious prompts into the function descriptions"; evaluated on AgentDriver and AgentThink with nuScenes; "attack success rates (ASR) exceeding 86%, even under strong defense strategies" (§1); AgentDriver "ASR@3 of 86.3% and ASR@6 of 82.3%", AgentThink "ASR@3 of 84.2% and ASR@6 of 79.5%"; average L2 10.52 and collision rate 4.58 % on AgentDriver (§5); vs AgentPoison "86.3% ± 3.0% … 80.5% ± 2.0%" (Welch t-test p = 0.009) (§5.3.1).
- Use in thesis: supply-chain/tool-definition attack class (C10, ASI04, AML.T0110.000); motivates checking tool-schema integrity under R156-style update governance.
- Verification: PRIMARY-READ (partial: abstract, intro, results)
- Inference: threat model assumes compromised third-party tool provider — higher attacker capability than content injection.

### V-06 · CHAI — CHAI: Command Hijacking against embodied AI
- Burbano, Ortiz, Sun, Yang, Tu, Xie, Cao, Cardenas (UC Santa Cruz, Johns Hopkins), 2025/2026 · IEEE SaTML 2026 (DOI 10.1109/SaTML68715.2026.00055, per Semantic Scholar record); arXiv v2 7 Feb 2026 · Tier: T2 (peer-reviewed IEEE conference; rated conservatively below the top-4 security venues; venue verified via metadata only)
- https://arxiv.org/abs/2510.00181
- Key content: "physical environment indirect prompt injection attack" embedding instructions as signs; "up to 95.5% attack success rate (ASR) on CloudTrack, 81.8% on DriveLM, and 72.8% on drone landing in simulation. In real-world robotic vehicle experiments, CHAI achieves up to ≥ 87% ASR"; "up to 10× more effective" than SceneTAP; generalises across English, Chinese, Spanish, "Spanglish" (§1).
- Use in thesis: visual-channel injection (C11) for future unified driving+cockpit agents; also an example of optimisation-based attacker (expertise = expert in §4.2).
- Verification: PRIMARY-READ (partial)
- Inference: only relevant to the cabin assistant if it ingests camera text (e.g., VLM-based cockpit), which none of the §2 products publicly states.

### V-07 · Threat from Windshield — Threat from Windshield: Vehicle Windows as Involuntary Attack Sources on Automotive Voice Assistants
- Wang, Huai, Cao, Liu, Luo, 2025 · ACM CCS 2025 (DOI 10.1145/3719027.3765171; DBLP conf/ccs/WangHCL025) · Tier: T1 (verified via Semantic Scholar API record)
- https://doi.org/10.1145/3719027.3765171
- Key content (abstract): "ShieldSpear … exploits a tiny piezo-element placed on the exterior of the windshield to convert it into both a speaker and microphone"; covertness "(blended into stickers)", "real-time attacking capability during vehicle motion"; acquires "drivers' voiceprint so as to accurately emulate it"; "Extensive experiments involving five mainstream vehicles have demonstrated … a 90.9% end-to-end success rate in injecting faked voice commands into AVAs". Open-access licence listed as CC BY (Semantic Scholar metadata).
- Use in thesis: evidence that out-of-cabin attackers can produce *driver-voiced* commands → speaker authentication cannot be assumed; justifies C3 and the "replay/voiceprint" fields of V-02.
- Verification: ABSTRACT-ONLY (dl.acm.org returned 403)
- Inference: the thesis simulates this channel as "attacker-controlled utterance with driver identity", no hardware.

### V-08 · Invitation Is All You Need — Invitation Is All You Need! Promptware Attacks Against LLM-Powered Assistants in Production Are Practical and Dangerous
- Nassi (Tel Aviv Univ./Technion), Cohen (Technion), Yair (SafeBreach), 2025 · arXiv (cs.CR, v1 16 Aug 2025); talk at Black Hat USA 2025 (6 Aug) and DEF CON 33 (10 Aug) per press/SafeBreach release snippets · Tier: T3 (paper) / T4 (talks)
- https://arxiv.org/abs/2508.12175 · MITRE ATLAS case study AML.CS0063
- Key content: "We demonstrate 14 attack scenarios … across five identified threat classes: Short-term Context Poisoning, Permanent Memory Poisoning, Tool Misuse, Automatic Agent Invocation, and Automatic App Invocation" (abstract); TARA "adapted from the automotive cybersecurity ISO/SAE 21434 standard" (§1); impact = highest of four factors "(financial, operational, safety, and privacy)" on "negligible, minor, moderate, severe, and critical" (§3.2.1; note: five levels, unlike 21434's four); safety "critical: … the user's car is remotely hijacked during driving"; likelihood = average of six factors (Equipment, Expertise, Window of Opportunity, Knowledge, Elapsed Time, User Interaction) with bands "very unlikely (likelihood < 0.6) … very likely (2.4 ≤ likelihood ≤ 3.0)" (§3.2.2). Results: "Four risks … were classified as critical. Two … very high … Four … high … Three … medium … One … low" (§6) and "73% of the analyzed threats pose High-Critical risk"; after mitigations "Six … medium … Four … low … Four … very low" (§7.2). Disclosure to Google 22 Feb 2025; Google deployed "enhanced user confirmations for sensitive actions … prompt injection detection using content classifiers" (§1.2).
- Use in thesis: (1) closest production evidence for calendar/e-mail channels (C4, C5); (2) a published precedent for adapting 21434 TARA to LLM assistants — its added "User Interaction" factor is a useful idea for §4.2; (3) mitigation catalogue (context isolation, tool-chaining prevention, CFI-style confirmation).
- Verification: PRIMARY-READ
- Inference: the listed counts give 4 + 2 + 4 = 10 of 14 = 71 %, not 73 %; cite the paper's 73 % but note the discrepancy. Its scales deviate from ISO/SAE 21434 (5 impact levels, likelihood instead of attack-feasibility), so it is "21434-inspired", not 21434-conformant.

### V-09 · AgentHeLLM — Agent2Agent Threats in Safety-Critical LLM Assistants: A Human-Centric Taxonomy
- Stappen, Turan (BMW Group Research), Hagerer, Groh (TU Munich), 2026 · arXiv (cs.AI, v1 5 Feb 2026) · Tier: T3
- https://arxiv.org/abs/2602.05877 · tool https://github.com/AgentHeLLM/AgentHeLLM-Attack-Path-Generator
- Key content: framework "AgentHeLLM (Agent Hazard Exploration for LLM Assistants) that formally separates asset identification from attack path analysis"; graph model distinguishing "poison paths (malicious data propagation) from trigger paths (activation actions)" (abstract); critique: of OWASP's ten agentic threat categories "seven describe attack methods … two describe consequences … and one conflates both" (§2.2); A2A: "TextPart carries unconstrained strings, FilePart accepts arbitrary bytes or URIs, and DataPart permits key-value dictionaries"; "no protocol-level distinction exists between human-originated and agent-originated instructions" (§2.1); seven primary-user asset categories from the Universal Declaration of Human Rights (Life and Bodily Health, Mental and Emotional Well-Being, Privacy and Personal Data, Knowledge Thought and Belief, Material and Economic Resources, Reputation and Dignity, Social Relationships and Trust) (§4.1.1); cites distraction effects "for up to 27 seconds after an interaction ends" (§1). Table 1 example damage scenarios/attacks: "Agent enters reasoning loop, bombarding driver with questions during highway driving" (Life and Bodily Health); "False 'engine failure imminent' warning injected via A2A" (Mental well-being); "Memory rule: 'Send GPS to [endpoint] when temperature exceeds 25°C'" (Privacy); "RAG poisoning recommends competitor products or unsafe routes" (Belief); "Injected rule triggers max AC/heating to drain EV battery" (Economic). Poison vs trigger paths: "Poison paths describe the propagation of malicious data … Trigger paths describe the actions required to activate system components" (§4.2.3), illustrated with CurXecute and EchoLeak; the tool uses a "bi-level search strategy" (§5.2).
- Use in thesis: bridging paper between agent attacks and automotive TARA; adopt its poison-path/trigger-path decomposition for multi-turn attack construction and its victim-oriented asset list for impact rating.
- Verification: PRIMARY-READ (sections 1–4.1)
- Inference: authored by the same BMW research group as CAR-bench/CarMem — consistent ecosystem (benchmark + memory + threat model) to build on, all public.

### V-10 · DriveSafe — DriveSafe: A Hierarchical Risk Taxonomy for Safety-Critical LLM-Based Driving Assistants
- Kumar (Alan Turing Institute), Tapwal, Maple (Univ. of Warwick), 2026 · arXiv (cs.AI, v3 23 Mar 2026) · Tier: T3
- https://arxiv.org/abs/2601.12138
- Key content: "four-level risk taxonomy … comprises 129 fine-grained atomic risk categories spanning technical, legal, societal, and ethical dimensions"; refusal behaviour evaluated "across six widely deployed LLMs"; "models often fail to appropriately refuse unsafe or non-compliant driving-related queries" (abstract).
- Use in thesis: harmful-request taxonomy for the *direct* channel (C1) and for judge rubrics.
- Verification: ABSTRACT-ONLY (abstract + intro read)
- Inference: conversational safety only; no tools.

### V-11 · Beyond V2X — Beyond V2X: A Review of Large Language Models in In-Vehicle Autonomous Driving Systems
- Ayan Roy, 2025 · TechRxiv preprint, DOI 10.36227/techrxiv.175571972.28517288/v1 (20 Aug 2025 per listing) · Tier: T3 (not peer-reviewed)
- https://doi.org/10.36227/techrxiv.175571972.28517288/v1
- Key content (snippet only): taxonomy of in-vehicle LLM applications; challenges "latency, determinism, real-time reliability, explainability, and compatibility with legacy automotive protocols"; unsafe in-vehicle LLM behaviour may "propagate into the broader Intelligent Transportation System".
- Use in thesis: background/related-work citation for in-vehicle LLM landscape only.
- Verification: UNVERIFIED (techrxiv.org blocked; search snippets only)
- Inference: none.

### V-12 · LLM-Mobility S&P survey — On the security and privacy of LLMs in Mobility
- Conti, Perinello, Salviati (Univ. of Padova et al.), 2026 · arXiv (cs.CR, v1 22 Sep 2026) · Tier: T3
- https://arxiv.org/abs/2609.26295
- Key content: derives "nine technical classes" from the EU AI Act's high-risk requirements; "research mainly studies GPT and Llama models (over 50% of reviewed works)"; "among 35 reviewed works, only one includes a partial vulnerability assessment and one a partial risk management system" (abstract).
- Use in thesis: quantitative evidence of the security gap in mobility-LLM research; AI-Act-derived requirement classes as an evaluation checklist (without claiming compliance).
- Verification: ABSTRACT-ONLY
- Inference: the abstract states "the European AI Act classifies transportation AI as high risk" — a simplification compared with Art. 2(2)/Annex I Section B (see §4); cite carefully.

### V-13 · Physical-AI TARA (VehicleSec '26) — A Study on Extending the TARA Methodology for Physical AI: A Case Study of ADS
- Woo, Lee (Korea Testing & Research Institute), 2026 · 4th USENIX Symposium on Vehicle Security and Privacy (VehicleSec '26), Baltimore, 10–11 Aug 2026 · Tier: T2 (peer-reviewed symposium; verified via usenix.org proceedings PDF)
- https://www.usenix.org/conference/vehiclesec26/presentation/woo
- Key content: "extended … TARA methodology, compliant with ISO/SAE 21434, that unifies STRIDE, MITRE ATLAS, and OWASP Top 10 for LLMs"; on an NVIDIA Jetson ADS case study "yields 38 security checklists. These outputs cover all 32 UN R155 Annex 5 Part A threat categories, identify 29% more AI-specific risks than a STRIDE-only baseline" (abstract).
- Use in thesis: example of how automotive venues accept ATLAS/OWASP-augmented TARA; precedent for mapping to R155 Annex 5 Part A.
- Verification: PRIMARY-READ (abstract/intro)
- Inference: perception-focused; no LLM-agent tool use.

### V-14 · DNN-limitations HARA+TARA — Towards a Systematic Risk Assessment of Deep Neural Network Limitations in Autonomous Driving Perception
- Pavlitska, Gerking, Zöllner (FZI, KIT), 2026 · arXiv (cs.CR, v1 21 Apr 2026) · Tier: T3
- https://arxiv.org/abs/2604.20895
- Key content: "joint workflow for risk assessment combining the hazard analysis and risk assessment (HARA) following ISO 26262 and threat analysis and risk assessment (TARA) following the ISO/SAE 21434" (abstract); example threat "An adversarial sticker placed on a vehicle causes the DNN to interpret it as an empty road".
- Use in thesis: second bridging example (ML attack → HARA/TARA rows); template for combining safety and security ratings.
- Verification: ABSTRACT-ONLY (+ table rows skimmed)
- Inference: none.

### V-15 · Hardware-aware TARA — Automotive Hardware Attacks: An Architect's Guide to TARA
- Breier, Hou, 2026 · arXiv (cs.CR, v1 7 Oct 2026) · Tier: T3
- https://arxiv.org/abs/2610.09697
- Key content (used as secondary source for ISO/SAE 21434 details): TARA activity list and S/F/O/P four-level impact, four-level feasibility, "risk value, an integer from 1 to 5" (§II-A); "Annex G gives three example approaches" — attack-potential sums "elapsed time, specialist expertise, knowledge of the item or component, window of opportunity, and equipment"; CVSS-based uses "exploitability metrics of CVSS"; attack-vector-based "maps the vector directly to the rating: network to high, adjacent to medium, local to low, and physical to very low" (§II, §III-A); Table II example values: Elapsed time "≤1 day (0), ≤1 week (1), ≤1 month (4), ≤6 months (17), >6 months (19)"; Expertise "layman (0), proficient (3), expert (6), multiple experts (8)"; Knowledge "public (0), restricted (3), confidential (7), strictly confidential (11)"; Window "unlimited (0), easy (1), moderate (4), difficult (10)"; Equipment "standard (0), specialized (4), bespoke (7), multiple bespoke (9)"; rating "0–13 high (H), 14–19 medium (M), 20–24 low (L), ≥25 very low (VL)".
- Use in thesis: citable secondary source for Annex G scales in §4.1–4.2; shows that the three approaches can disagree.
- Verification: PRIMARY-READ (sections I–III)
- Inference: always state "example values of Annex G" — the standard does not mandate them.

### V-16 · VicOne "Invisible Commands" — Invisible Commands, Real Consequences: AI Prompt Injection in Vehicle Systems
- VicOne CyberThreat Research Lab, 2 May 2025 · Company blog · Tier: T4
- https://vicone.com/blog/invisible-commands-real-consequences-ai-prompt-injection-in-vehicle-systems/
- Key content (snippet): driver asks the assistant to read a message aloud, "hears only the benign content … Behind the scenes, the AI interprets and executes the hidden malicious command"; invisible Unicode characters. Companion post "AI Smart Cockpits" (10 Feb 2025) recommends secondary "AI guardians". VicOne says its findings were shared at "RSAC, ESCAR USA, and ELIV" (snippet).
- Use in thesis: industry recognition of the message-read-aloud channel (C4); scenario for §7.
- Verification: UNVERIFIED (vicone.com blocked; snippets only)
- Inference: scenario analysis, no measured attack.

### V-17 · Upstream 2026 Global Automotive & Smart Mobility Cybersecurity Report
- Upstream Security, 2026 · Industry report · Tier: T4
- Link: not opened (upstream.auto blocked)
- Key content (secondary press snippets only): analyses "494 publicly reported automotive and smart-mobility cyber incidents from 2025" from a database of ">2,300 since 2010"; names prompt injection as a key AI threat; "92% … conducted remotely", "67% involved telematics and cloud systems".
- Use in thesis: context sentence that remote/cloud vectors dominate — only after reading the primary report.
- Verification: UNVERIFIED
- Inference: none.

### V-18 · Infotainment exploitation talks (Black Hat Asia 2025 Nissan Leaf; Black Hat Europe 2024 VW MIB3)
- PCAutomotive researchers (Evdokimov et al.), 2024–2025 · Conference talks · Tier: T4
- https://i.blackhat.com/Asia-25/Asia-25-Evdokimov-Remote-Exploitation-of-Nissan-Leaf.pdf ; "Over the Air: Compromise of Modern Volkswagen Group Vehicles" (Black Hat Europe 2024)
- Key content (snippets): Nissan Leaf chain "Bluetooth RCE … persistence and data exfiltration, and CAN communication"; microphone recording reported; MIB3 chain "code execution over Bluetooth, privilege escalation to root"; TechCrunch: researchers "did not find a way past the in-vehicle network gateway to safety-critical controls".
- Use in thesis: bounds attacker capabilities (an attacker with infotainment code execution makes LLM attacks moot) → thesis assumes an *uncompromised* platform and only content-level attacker capabilities.
- Verification: UNVERIFIED (snippets only)
- Inference: these are public talks about public products; cite for context only.

### V-19 · In-car factual benchmarking (Giebisch et al., IEEE IV 2025) and DeepTest 2026 tool competition (Sorokin et al.)
- Giebisch, Friedl, Sorokin, Stocco, "Automated factual benchmarking for in-car conversational systems using large language models", IEEE IV 2025, pp. 1238–1243; Sorokin, Vasilev, Pasini, "DeepTest tool competition 2026: Benchmarking an LLM-based automotive assistant", DeepTest 2026 workshop, pp. 31–34 · Tier: T2 (IV) / T2 (workshop)
- Key content: known only from the reference list of V-02 (refs [3], [13]) — manual-QA correctness and omitted safety warnings.
- Use in thesis: related work for non-adversarial evaluation of in-car assistants.
- Verification: UNVERIFIED (cited by V-02; primaries not opened)

### V-20 · OWASP Top 10 for Agentic Applications for 2026
- OWASP GenAI Security Project – Agentic Security Initiative, Dec 2025 · Industry catalogue · Tier: T4
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- Key content: see §4 table (ASI01–ASI10, "Version 2026, December 2025"); ASI02 "builds on the mitigations of LLM06:2025 (Excessive Agency)".
- Use in thesis: attack-class labels and defense checklist.
- Verification: PRIMARY-READ (PDF)

### V-21 · OWASP Agentic AI – Threats and Mitigations v1.1
- OWASP ASI, Dec 2025 (v1.0 17 Feb 2025) · Industry guide, CC BY-SA 4.0 · Tier: T4
- https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- Key content: T1–T17 (see §4).
- Verification: PRIMARY-READ (PDF)

### V-22 · MITRE ATLAS release 2026.10
- MITRE, 28 Oct 2026 · Knowledge base (data repo) · Tier: T4
- https://atlas.mitre.org ; data https://github.com/mitre-atlas/atlas-data (`dist/v6/ATLAS-2026.10.yaml`)
- Key content: technique IDs in §5; case study AML.CS0063.
- Verification: PRIMARY-READ (official data file)

### V-23 · OWASP Top 10 for LLM Applications 2025
- OWASP GenAI Security Project, 2025 · Tier: T4 · https://genai.owasp.org/llm-top-10/
- Key content: LLM01–LLM10 names (see §4).
- Verification: PRIMARY-READ (web page)

### V-24 · Light Commands — Light Commands: Laser-Based Audio Injection Attacks on Voice-Controllable Systems
- Sugawara et al. (USENIX presentation page "sugawara"), 2020 · USENIX Security 2020 · Tier: T1 (verified via usenix.org presentation page)
- https://www.usenix.org/conference/usenixsecurity20/presentation/sugawara
- Key content (abstract on usenix.org): "inject arbitrary audio signals to a target microphone by aiming an amplitude-modulated light at the microphone's aperture"; control "at distances up to 110 meters and from two separate buildings"; "user authentication on these devices is often lacking"; attacker could "unlock and start various vehicles connected to the target's Google account (e.g., Tesla and Ford)".
- Use in thesis: classic precedent that a *home/phone voice assistant* is already a path to vehicle functions; supports C3 and the need for speaker authentication not to be assumed.
- Verification: ABSTRACT-ONLY (author list beyond first author not extracted)
- Inference: the vehicle actions were reached through cloud-linked accounts, not the in-car microphone — a cross-device channel the in-car agent threat model should list.

### V-25 · STAF (escar Europe 2025) — STAF: Leveraging LLMs for Automated Attack Tree-Based Security Test Generation
- Marksteiner et al., 2025 · 23rd escar Europe (Frankfurt, 5–6 Nov 2025), per arXiv comment "accepted for 23rd escar Europe" · Tier: T2 (escar scientific track is peer-reviewed per escar CFP snippet)
- https://arxiv.org/abs/2509.20190
- Key content (abstract): LLM + "four-step self-corrective Retrieval-Augmented Generation (RAG) framework" that generates "executable security test cases from attack trees".
- Use in thesis: example of what escar's scientific track accepts (method + tool + automotive test integration); LLM used *for* security, not attacked.
- Verification: ABSTRACT-ONLY
- Inference: none.

### V-26 · Typographic attacks on AD Vision-LLMs — Towards Transferable Attacks Against Vision-LLMs in Autonomous Driving with Typography
- Chung, Gao, Vu, Zhang, Liu, Lin, Dong, Guo, 2024 · arXiv 2405.14169 ("work in progress") · Tier: T3
- https://arxiv.org/abs/2405.14169
- Key content (abstract): typographic attacks "against AD systems relying on the decision-making capabilities of Vision-LLMs"; "dataset-agnostic framework for automatically generating false answers"; discusses physical presentation in traffic scenes.
- Use in thesis: DriveLM-style attack precedent (with V-06, V-27) for the visual channel C11.
- Verification: ABSTRACT-ONLY
- Inference: numbers not extracted.

### V-27 · ADvLM — Visual Adversarial Attack on Vision-Language Models for Autonomous Driving
- Zhang, Wang, Zhang, Zhang, Jia, Liang, Hu, Fu, Liu, Liu, 2024 · Machine Intelligence Research (DOI 10.1007/s11633-026-1667-4 per Semantic Scholar) · Tier: T2 (journal)
- https://arxiv.org/abs/2411.18275
- Key content (abstract): "the first visual adversarial attack framework specifically designed for VLMs in AD"; challenges "variability of textual instructions and the time-series nature of visual scenarios"; "Semantic-Invariant Induction".
- Use in thesis: perturbation-based (white/grey-box) attack class on driving VLMs; contrasts with semantic injection (CHAI).
- Verification: ABSTRACT-ONLY
- Inference: none.

### V-28 · Acoustic Cybersecurity — Acoustic Cybersecurity: Exploiting Voice-Activated Systems
- arXiv 2312.00039, 2023 · Tier: T3
- https://arxiv.org/abs/2312.00039
- Key content (abstract): "twelve attack vectors identified include successful manipulation of smart home devices and automotive systems"; "attack success rates hover around 60%, with the ability to activate devices remotely from over 100 feet away".
- Use in thesis: secondary support for C3 only; prefer V-07/V-24.
- Verification: ABSTRACT-ONLY (authors not extracted)
- Inference: not peer-reviewed; methodology unclear from abstract.

### V-30 · Holistic safety evaluation (SAE WCX 2026 preprint) — The Necessity of a Holistic Safety Evaluation Framework for AI-Based Automation Features
- Abbaspour, Mahadevan, Zwirglmaier, Stafford, 2026 · arXiv 2602.05157, header "PRE-PRINT FOR SAE WCX 2026 CONFERENCE" · Tier: T3 (SAE acceptance not verified)
- https://arxiv.org/abs/2602.05157
- Key content: lists ISO 26262 severity classes "S0: No injuries … S3: Life-threatening injuries (survival uncertain)" and discusses how AI components contribute to SOTIF-related hazards.
- Use in thesis: secondary citation for ISO 26262 S-classes in impact rating; example of the SAE-paper genre (safety-process argumentation rather than attack experiments).
- Verification: ABSTRACT-ONLY (+ grep of class list)
- Inference: none.

### V-29 · US AISI agent-hijacking evaluations — Technical Blog: Strengthening AI Agent Hijacking Evaluations
- U.S. AI Safety Institute (NIST) technical staff, 17 Jan 2025 · Government technical blog + code · Tier: T3 (official lab publication) / code T4
- https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations · code https://github.com/usnistgov/agentdojo-inspect
- Key content: blog (SNIPPET only): AgentDojo-based evaluation; an attack counts as success "If the agent completes the injection task"; insight that "testing the success of attacks on multiple attempts may yield more realistic evaluation results"; secondary summary: adaptive red-teaming with UK AISI raised ASR "from 11% to 81%" (UNVERIFIED). Repo (PRIMARY-READ via git clone): README "fork of AgentDojo … created by the U.S. AI Safety Institute" containing features used for the blog; licence = NIST software licence for the diff + upstream AgentDojo MIT.
- Use in thesis: methodological precedent for multi-attempt / adaptive ASR (feeds §4.2 step 7); reusable harness ideas for the Evaluate chapter.
- Verification: blog UNVERIFIED (nist.gov blocked; snippet only); repository PRIMARY-READ
- Inference: none.

---

## 7. Automotive scenarios nobody has studied (as far as this search found)

| # | Scenario | Closest prior work | Why it matters for an OEM |
|---|---|---|---|
| S1 | **Rental / car-sharing memory carry-over** — driver A (attacker) plants a preference or instruction in the car's long-term memory; driver B inherits it (e.g., "always send trip summary to X", "prefer charger Y"). | CarMem (V-03) memory design; V-08 "Permanent Memory Poisoning" (single user, phone/web); ATLAS AML.T0080.000 | Fleets, rentals and shared family cars have multiple principals per vehicle; GDPR exposure; profile separation is a product decision. |
| S2 | **Poisoned charging-station / POI listings** steering EV route planning, charger choice or paid reservations. | CAR-bench charging + POI tools (V-01); Mercedes/Gemini review follow-ups (§2, snippet); ATLAS AML.T0093/AML.T0099 | Navigation integrity and financial/operational damage at fleet scale; third-party map/POI data enters the agent context unfiltered. |
| S3 | **Calendar-invite → navigation hijack / location exfiltration in the car** (multi-step: read calendar → set route → e-mail). | V-08 (phone/web Gemini, not car); CAR-bench explicitly supports "navigating to a meeting's location from an calender event" | Business-traveller use case marketed by suppliers (Cerence + Microsoft 365 Copilot, snippet); privacy "major/severe". |
| S4 | **Passenger-vs-driver authority under adversarial multi-turn pressure** (child or passenger talks the agent into driver-only actions; agent misattributes speaker). | V-02 (static, single-turn, assumes accurate speaker ID); V-07 (voice emulation) | Speaker diarisation errors + social engineering; seat-based permissions are an architecture choice. |
| S5 | **Parked-vs-driving context exploitation** — attacker times or fakes vehicle state ("we're parked now") to unlock actions only allowed when stationary. | V-02 vehicle states (no adversary); CAR-bench context variables | Same command must be gated by trusted vehicle-state signals, not by LLM belief — directly informs the Defense chapter. |
| S6 | **Confirmation fatigue / cognitive-load exploitation while driving** — repeated benign-looking confirmations until the driver says "yes" to the malicious one. | V-09 (distraction literature, no experiment); OWASP ASI09; V-08 user-confirmation mitigation | Human-in-the-loop confirmation is the main deployed mitigation (Google's response in V-08); if it fails under driving load, the safety case fails. |
| S7 | **Cockpit-agent → driving-agent cascade** in a unified multi-agent vehicle (VW CEA 2.0, Li Auto "super agent"). | FuncPoison (V-05) and CHAI (V-06) attack driving agents directly; no cockpit→driving propagation study | Announced architectures merge the two domains; ASI08 cascading failures and ISO 26262/PAS 8800 boundaries become critical. |
| S8 | **TTS/ASR-mediated hidden payloads** — what the driver hears (TTS) differs from what the LLM processes (invisible Unicode, homoglyphs, markup). | V-16 (scenario only) | Driver cannot audit what the agent read; voice-only UI removes the visual check available on phones. |
| S9 | **Connectivity-downgrade attack on hybrid edge/cloud agents** — force fallback from a guarded cloud model to a weaker on-board SLM. | Cerence xUI "graceful fallback" and NVIDIA edge/cloud split (§2, snippets) — Inference, no study found | Hybrid architectures are the supplier default; guardrail parity between edge and cloud is untested. |
| S10 | **Long-horizon delayed triggers across drives** — payload planted on Monday, triggered by a routine ("on the way home") days later. | V-08 "triggered" attacks (same session); ATLAS AML.T0051.002 | Long-horizon persistence is exactly the thesis' "long-horizon tasks" angle; daily-commute routines (Tesla Grok learned routines, snippet) make triggers predictable. |

---

## 8. Registry rows

```csv
id,short_name,title,authors_first,year,venue,tier,verification,url,used_for,notes
V-01,CAR-bench,"CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty",Kirmayr,2026,"ACL 2026 (Long), 2026.acl-long.1886",T1,PRIMARY-READ,https://aclanthology.org/2026.acl-long.1886/,"simulation substrate; tools/policies; Pass^k","MIT licence (repos + HF dataset card); paper 240 tasks vs README table 254 vs README text 248; no adversary"
V-02,IntentToAction,"From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization",Afroze,2026,arXiv 2609.19630,T3,PRIMARY-READ,https://arxiv.org/abs/2609.19630,"vehicle-state/speaker context; False Execute metric; defense motivation","202 scenarios, 7 classes; alignment 40.1-89.1%; data not yet released"
V-03,CarMem,"CarMem: Enhancing Long-Term Memory in LLM Voice Assistants through Category-Bounding",Kirmayr,2025,"COLING 2025 Industry, 2025.coling-industry.29",T2,PRIMARY-READ,https://aclanthology.org/2025.coling-industry.29/,"memory design; memory-poisoning target","F1 .78-.95; repo has no LICENSE file"
V-04,AgentPoison,"AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases",Chen,2024,"NeurIPS 2024; arXiv 2407.12784",T1,PRIMARY-READ,https://arxiv.org/abs/2407.12784,"memory/RAG backdoor baseline; driving agent","ASR>=80%, poison rate <0.1%"
V-05,FuncPoison,"FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems",Long,2025,arXiv 2509.24408,T3,PRIMARY-READ,https://arxiv.org/abs/2509.24408,"tool-definition supply-chain attack class","ASR@3 86.3% AgentDriver"
V-06,CHAI,"CHAI: Command Hijacking against embodied AI",Burbano,2026,"IEEE SaTML 2026; arXiv 2510.00181",T2,PRIMARY-READ,https://arxiv.org/abs/2510.00181,"visual prompt injection channel","81.8% DriveLM sim; >=87% real robotic vehicle; venue via Semantic Scholar metadata"
V-07,ThreatFromWindshield,"Threat from Windshield: Vehicle Windows as Involuntary Attack Sources on Automotive Voice Assistants",Wang,2025,ACM CCS 2025,T1,ABSTRACT-ONLY,https://doi.org/10.1145/3719027.3765171,"acoustic out-of-cabin channel; speaker-auth assumption","ShieldSpear; 90.9% e2e on five vehicles"
V-08,InvitationIsAllYouNeed,"Invitation Is All You Need! Promptware Attacks Against LLM-Powered Assistants in Production Are Practical and Dangerous",Nassi,2025,"arXiv 2508.12175; Black Hat USA 2025; DEF CON 33",T3,PRIMARY-READ,https://arxiv.org/abs/2508.12175,"calendar/e-mail channel; 21434-style TARA precedent; mitigations","14 attacks, 5 classes; 73% High-Critical (listed counts give 10/14=71%); ATLAS AML.CS0063"
V-09,AgentHeLLM,"Agent2Agent Threats in Safety-Critical LLM Assistants: A Human-Centric Taxonomy",Stappen,2026,arXiv 2602.05877,T3,PRIMARY-READ,https://arxiv.org/abs/2602.05877,"asset taxonomy; poison/trigger paths; A2A channel","BMW Research + TUM; open-source attack path generator"
V-10,DriveSafe,"DriveSafe: A Hierarchical Risk Taxonomy for Safety-Critical LLM-Based Driving Assistants",Kumar,2026,arXiv 2601.12138,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2601.12138,"harmful-request taxonomy for direct channel","129 atomic risk categories; 6 LLMs"
V-11,BeyondV2X,"Beyond V2X: A Review of Large Language Models in In-Vehicle Autonomous Driving Systems",Roy,2025,TechRxiv preprint,T3,UNVERIFIED,https://doi.org/10.36227/techrxiv.175571972.28517288/v1,"related-work background","snippet only"
V-12,LLMMobilitySP,"On the security and privacy of LLMs in Mobility",Conti,2026,arXiv 2609.26295,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2609.26295,"gap evidence; AI-Act-derived checklist","35 works reviewed; 1 partial vulnerability assessment"
V-13,PhysicalAI-TARA,"A Study on Extending the TARA Methodology for Physical AI: A Case Study of ADS",Woo,2026,USENIX VehicleSec 2026,T2,PRIMARY-READ,https://www.usenix.org/conference/vehiclesec26/presentation/woo,"TARA + ATLAS + OWASP precedent; R155 Annex 5 mapping","38 checklists; 32 Annex 5 Part A categories; +29% AI risks"
V-14,DNN-HARA-TARA,"Towards a Systematic Risk Assessment of Deep Neural Network Limitations in Autonomous Driving Perception",Pavlitska,2026,arXiv 2604.20895,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2604.20895,"joint HARA+TARA template","ISO 26262 + ISO/SAE 21434"
V-15,HW-TARA,"Automotive Hardware Attacks: An Architect's Guide to TARA",Breier,2026,arXiv 2610.09697,T3,PRIMARY-READ,https://arxiv.org/abs/2610.09697,"secondary source for 21434 Annex G scales","three feasibility approaches disagree"
V-16,VicOne-InvisibleCommands,"Invisible Commands, Real Consequences: AI Prompt Injection in Vehicle Systems",VicOne,2025,Company blog,T4,UNVERIFIED,https://vicone.com/blog/invisible-commands-real-consequences-ai-prompt-injection-in-vehicle-systems/,"message-read-aloud scenario","snippet only"
V-17,Upstream2026,"Upstream 2026 Global Automotive & Smart Mobility Cybersecurity Report",Upstream Security,2026,Industry report,T4,UNVERIFIED,,"context on remote vectors","494 incidents (press summary only)"
V-18,BH-Infotainment,"Remote Exploitation of Nissan Leaf / Over the Air: Compromise of Modern Volkswagen Group Vehicles",Evdokimov,2025,"Black Hat Asia 2025 / Black Hat Europe 2024",T4,UNVERIFIED,https://i.blackhat.com/Asia-25/Asia-25-Evdokimov-Remote-Exploitation-of-Nissan-Leaf.pdf,"bounds attacker capability","snippets only"
V-19,InCarFactual+DeepTest,"Automated factual benchmarking for in-car conversational systems using LLMs; DeepTest tool competition 2026",Giebisch,2025,"IEEE IV 2025; DeepTest 2026",T2,UNVERIFIED,,"related work (non-adversarial)","known via V-02 references"
V-20,OWASP-ASI-Top10,"OWASP Top 10 for Agentic Applications for 2026",OWASP GenAI Security Project,2025,Industry catalogue,T4,PRIMARY-READ,https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/,"attack-class labels","ASI01-ASI10; Dec 2025"
V-21,OWASP-Agentic-TM,"Agentic AI - Threats and Mitigations v1.1",OWASP ASI,2025,Industry guide,T4,PRIMARY-READ,https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/,"threat checklist T1-T17","CC BY-SA 4.0"
V-22,MITRE-ATLAS-2026.10,"MITRE ATLAS (release 2026.10)",MITRE,2026,Knowledge base,T4,PRIMARY-READ,https://github.com/mitre-atlas/atlas-data,"technique IDs","dist/v6/ATLAS-2026.10.yaml"
V-23,OWASP-LLM-Top10-2025,"OWASP Top 10 for LLM Applications 2025",OWASP GenAI Security Project,2025,Industry catalogue,T4,PRIMARY-READ,https://genai.owasp.org/llm-top-10/,"attack-class labels","LLM01-LLM10"
S-01,UN-R155,"UN Regulation No. 155 - Cyber security and cyber security management system",UNECE WP.29,2021,UN Regulation,T2,UNVERIFIED,https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security,"CSMS context; Annex 5 mapping","in force 22 Jan 2021; new types Jul 2022; all new vehicles Jul 2024 (snippets)"
S-02,UN-R156,"UN Regulation No. 156 - Software update and software update management system",UNECE WP.29,2021,UN Regulation,T2,UNVERIFIED,,"SUMS context for model/tool updates","snippets only"
S-03,ISO-SAE-21434,"ISO/SAE 21434:2021 Road vehicles - Cybersecurity engineering",ISO/SAE,2021,International standard,T2,UNVERIFIED,https://www.iso.org/standard/70918.html,"TARA structure","details via V-15 (secondary); URL not opened"
S-04,ISO-PAS-8800,"ISO/PAS 8800:2024 Road vehicles - Safety and artificial intelligence",ISO,2024,Publicly Available Specification,T2,UNVERIFIED,https://www.iso.org/standard/83303.html,"AI safety framing","Edition 1 2024-12, 172 pp (snippets)"
S-05,EU-AI-Act,"Regulation (EU) 2024/1689 (Artificial Intelligence Act)",European Parliament and Council,2024,EU Regulation,T2,UNVERIFIED,https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng,"regulatory context","EUR-Lex WAF blocked reading"
S-06,EU-AI-Omnibus,"Regulation (EU) 2026/1744 (Digital Omnibus on AI)",European Parliament and Council,2026,EU Regulation,T2,UNVERIFIED,https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng,"high-risk deferral dates","2 Dec 2027 (Annex III), 2 Aug 2028 (Annex I); in force 27 Jul 2026 (snippets)"
S-07,NIST-AI-100-2-E2025,"Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations (NIST AI 100-2 E2025)",Vassilev,2025,NIST report,T3,UNVERIFIED,https://doi.org/10.6028/NIST.AI.100-2e2025,"attack terminology","snippets only"
S-08,UNECE-IWG-AI,"WP.29 IWG on Artificial Intelligence - AI Reference Document (draft AI-09-06/Rev.3)",UNECE WP.29,2026,UN working document,T3,UNVERIFIED,,"regulatory status of vehicle AI guidance","draft; delivery requested by June 2027 (snippets)"
V-24,LightCommands,"Light Commands: Laser-Based Audio Injection Attacks on Voice-Controllable Systems",Sugawara,2020,USENIX Security 2020,T1,ABSTRACT-ONLY,https://www.usenix.org/conference/usenixsecurity20/presentation/sugawara,"acoustic/light channel precedent; vehicles via cloud-linked accounts","up to 110 m; Tesla and Ford unlock/start via Google account"
V-25,STAF,"STAF: Leveraging LLMs for Automated Attack Tree-Based Security Test Generation",Marksteiner,2025,escar Europe 2025,T2,ABSTRACT-ONLY,https://arxiv.org/abs/2509.20190,"example of escar scientific-track paper","LLM for security testing"
V-26,TypographyAD,"Towards Transferable Attacks Against Vision-LLMs in Autonomous Driving with Typography",Chung,2024,arXiv 2405.14169,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2405.14169,"visual channel precedent","work in progress"
V-27,ADvLM,"Visual Adversarial Attack on Vision-Language Models for Autonomous Driving",Zhang,2024,Machine Intelligence Research,T2,ABSTRACT-ONLY,https://arxiv.org/abs/2411.18275,"perturbation attacks on driving VLMs","DOI 10.1007/s11633-026-1667-4"
V-28,AcousticCyber,"Acoustic Cybersecurity: Exploiting Voice-Activated Systems",(not extracted),2023,arXiv 2312.00039,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2312.00039,"secondary support for acoustic channel","~60% success, >100 ft"
V-29,USAISI-AgentHijacking,"Technical Blog: Strengthening AI Agent Hijacking Evaluations",U.S. AI Safety Institute (NIST),2025,Government technical blog,T3,UNVERIFIED,https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations,"multi-attempt / adaptive ASR methodology","blog snippet only; repo usnistgov/agentdojo-inspect read (NIST licence + MIT)"
V-30,HolisticSafetyAI,"The Necessity of a Holistic Safety Evaluation Framework for AI-Based Automation Features",Abbaspour,2026,"arXiv 2602.05157 (pre-print for SAE WCX 2026)",T3,ABSTRACT-ONLY,https://arxiv.org/abs/2602.05157,"ISO 26262 S-classes (secondary); SAE genre example","SAE acceptance unverified"
O-01,VW-ChatGPT-IDA,"World premiere at CES: Volkswagen integrates ChatGPT into its vehicles",Volkswagen AG,2024,Official press,T4,PRIMARY-READ,https://www.volkswagen-group.com/en/articles/world-premiere-at-ces-volkswagen-integrates-chatgpt-into-its-vehicles-18052,"deployed capability table","standard from Q2 2024; no vehicle data to ChatGPT"
O-02,VW-AgenticAI-China,"Auto China 2026: Volkswagen Group Unveils Record Product Offensive and Agentic AI Roadmap for China",Volkswagen Group,2026,Official press,T4,PRIMARY-READ,https://www.volkswagen-group.com/en/press-releases/auto-china-2026-volkswagen-group-unveils-record-product-offensive-and-agentic-ai-roadmap-for-china-20333,"deployed capability table; S7","onboard agent H2 2026; CEA 2.0 multi-agent 2027"
```
