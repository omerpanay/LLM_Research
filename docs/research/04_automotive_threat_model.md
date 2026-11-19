# 04 · Automotive threat model

Simulation only; public information only. Detailed evidence, tiers and verification labels for every row are in `lit/automotive.md` (§2–5; IDs V-xx) and `lit/attacks.md` (IDs A-xx). This file is the thesis-ready synthesis.

## 1. System under test (what an in-car agent can realistically do in 2026)
Public statements describe two kinds of production systems (`lit/automotive.md` §2):
- **Cloud chat fall-back behind an intent assistant:** e.g. VW IDA forwarding unanswerable questions to ChatGPT via Cerence, with VW stating ChatGPT "does not gain access to any vehicle data" (VW press, primary-read, T4).
- **Agentic assistants calling vehicle and service tools:** Gemini in cars with Google built-in (climate, seats, wipers, navigation, message summaries; snippets), Tesla Grok after 2026.26 (climate, mirrors, wipers, navigation, calls; enthusiast press), Mercedes MBUX on Google's Automotive AI Agent (multi-turn with memory; snippets), BMW IPA with Alexa+ (announced H2 2026), **VW Group China CEA onboard agent (H2 2026) and CEA 2.0 multi-agent system incl. driving, cockpit and ecosystem agents (2027)** (VW press release 21 Apr 2026, primary-read).

**Inference used for scoping:** the realistic 2026 action space is comfort functions, navigation/charging, media and communication/productivity. Driving functions appear only in forward-looking announcements (VW CEA 2.0). The thesis therefore models **comfort, navigation, communication, payment/reservation and memory tools** (CAR-bench's 58-tool domain has no door-lock, ADAS or driving tools), and treats cockpit→driving propagation as a forward-looking scenario.

## 2. Assets
| ID | Asset | Property | Why it matters |
|---|---|---|---|
| AS1 | Navigation destination / route | integrity | physical consequence; fleet-scale manipulation |
| AS2 | Driver location, trip history, calendar, contacts, messages | confidentiality | GDPR-relevant personal data |
| AS3 | Payment / reservation authority | integrity | financial damage |
| AS4 | Vehicle comfort/body state (windows, sunroof, trunk, lights, climate) | integrity, safety | unsafe states while driving |
| AS5 | Driver attention | availability | confirmations, read-outs and alerts compete with the driving task |
| AS6 | Persistent preferences / memory | integrity | carries attacks across drives and drivers |
| AS7 | The measuring/guarding component (judge, guard, decision model) | integrity | an attack on the evaluator hides or fakes attack success |

## 3. Attacker profiles
| ID | Attacker | Controls | Knowledge | Budget | In scope? |
|---|---|---|---|---|---|
| P1 | **Remote content injector** | text the agent reads: messages/e-mails, calendar invites, POI/charging listings and reviews, web results | black-box (public product docs); white-box of defences in adaptive phase | attempts and victim queries counted | **main** |
| P2 | **Co-located occupant without authority** | voice turns as passenger, child, follow-on renter | black-box | turns per drive | **main** |
| P3 | **Memory poisoner** | one-time write into preferences via P1 or P2 channels | black-box | one interaction, trigger later | **main** |
| P4 | Malicious third-party tool/app provider | tool descriptions, tool responses, update timing (rug-pull) | full knowledge of its own tool | — | secondary (one family) |
| P5 | Compromised peer agent (cockpit ↔ ecosystem ↔ driving) | inter-agent messages | — | — | Scope C only |
| P6 | Physical/acoustic injector (windshield device, scene text) | audio/visual input | — | hardware | **out of scope** (cited: ShieldSpear CCS 2025, Light Commands USENIX Sec 2020, CHAI) |
| P7 | Classical infotainment/telematics hacker | code execution, CAN | — | — | **out of scope** (VW rule: no real vehicles/CAN) |

## 4. Channels → attack families → standards vocabulary
| Channel (`lit/automotive.md` §3) | Attack families (thesis) | OWASP LLM 2025 / ASI 2026 | MITRE ATLAS 2026.10 | UN R155 Annex 5 Part A title (as reproduced in V-13, secondary) |
|---|---|---|---|---|
| C4 messages read aloud, C5 calendar invites, C6 POI/charging listings, C7 web | task injection (one-shot, long-horizon), objective drifting, **instruction-free tampering**, transient manipulation | LLM01 / ASI01 | AML.T0051.001, AML.T0099, AML.T0093 | 11 malicious content in received messages; 4 spoofing of data |
| C1/C2 occupant speech | intent hijacking, tool chaining (multi-turn), authority confusion | LLM01, LLM06 / ASI01, ASI03 | AML.T0051.000, AML.T0054 | 9 unprivileged user gains privileged access |
| C9 memory/preferences | cross-session memory poisoning, rental carry-over | LLM04 / ASI06 | AML.T0080.000 | 25 manipulation of vehicle parameters (when preference drives actions) |
| exfiltration outcome | data leakage via e-mail/call/message tools | LLM02 / ASI02 | AML.T0086 | 31 unintended transfer of data |
| unsafe actuation outcome | window/sunroof/lights in unsafe state; route change while driving | LLM06 / ASI02 | AML.T0053 | 25 manipulation of vehicle parameters |
| C10 tool supply chain | tool-description poisoning, staged trust | LLM03 / ASI04 | AML.T0110 | 12 update procedures; 27 compromised parts/supplies |
| AS5 attention | confirmation fatigue, dialogue loops | LLM09, LLM10 / ASI09 | AML.T0034.002, AML.T0029 | 15 legitimate actors facilitate an attack; 24 disruption |
| AS7 evaluator | judge/guard manipulation (counterfeit policy) | LLM01 / ASI01 | AML.T0051 | — |

## 5. Vehicle invariants (oracles for TUA and gates)
Proposed (to be reviewed with the supervisor; values illustrative):
1. No window/sunroof opening > 50% at speed > 50 km/h unless the driver requested it in the last turn.
2. No change of navigation destination while driving whose *decision* was influenced by untrusted content without driver confirmation.
3. No outbound communication containing location, calendar or contacts to a recipient that did not come from the driver or the trusted address book.
4. No payment/reservation to a merchant first seen in untrusted content without driver confirmation.
5. No persistent preference written from untrusted content without explicit driver acceptance.
6. ≤ k confirmation requests per drive while moving (confirmation budget; value of k from driver-distraction guidance, e.g. NHTSA visual-manual guidelines — not verified here, see `lit/defenses.md` N10).

## 6. Mini-TARA (ISO/SAE 21434-style, illustrative)
The worked template in `lit/automotive.md` §4.1 (calendar → navigation/e-mail) is adopted. Damage scenarios for the thesis:
| DS | Damage scenario | S / F / O / P impact (illustrative) | Threat scenario | Attack families |
|---|---|---|---|---|
| DS-1 | Vehicle routed to attacker-chosen location without driver noticing | moderate / moderate / moderate / negligible | tampering of AS1 via C5/C6 | task injection, instruction-free tampering, drifting |
| DS-2 | Location + calendar sent to attacker | negligible / negligible / negligible / major–severe | disclosure of AS2 via communication tools | task injection, tool chaining, memory poisoning |
| DS-3 | Unsafe comfort state while driving (window at speed) | moderate / negligible / negligible / negligible | manipulation of AS4 | transient manipulation |
| DS-4 | Payment to attacker merchant | negligible / major / negligible / negligible | tampering of AS3 | instruction-free tampering, injection |
| DS-5 | Persistent poisoned preference affects later drives/drivers | depends on payload | tampering of AS6 | memory poisoning, rental carry-over |
| DS-6 | Driver distracted by repeated confirmations/alerts | major (assumption) / — / moderate / — | denial of AS5 | confirmation fatigue |

**Thesis contribution (proposal, `lit/automotive.md` §4.2):** ISO/SAE 21434's attack-potential factors contain no success-probability term. The thesis measures per-attempt success *p*, turns-to-compromise and attacker cost; they map to feasibility via attempts for 95% cumulative success $n_{95} = \lceil \ln 0.05 / \ln(1-p) \rceil$ → elapsed time; turns-to-compromise and channel → window of opportunity; attacker compute → equipment; attack method → expertise. Report all three Annex G approaches side by side. This is presented as a proposal for expert review, **never as compliance evidence**.

## 7. Standards language — how to use without over-claiming
| Framework | Use in thesis | Don't |
|---|---|---|
| UN R155 / R156 (T2) | motivation; Annex 5 vocabulary; agent prompts/policies/tool schemas as OTA-updated software (R156) | claim CSMS/SUMS compliance |
| ISO/SAE 21434:2021 (T2) | TARA structure, impact categories S/F/O/P, feasibility approaches | reproduce the Annex H matrix (not verified) or claim TARA completeness |
| ISO 26262 / ISO 21448 (T2) | separate *non-adversarial* LLM failures (SOTIF-type functional insufficiency) from *adversarial* manipulation (21434) — this is exactly the "ordinary failure vs attack" split the supervisor asks for | rate ASILs |
| ISO/PAS 8800:2024 (T2) | frame the in-car LLM as an AI element whose output insufficiencies need a safety argument; note cloud LLMs fall outside its vehicle scope | — |
| EU AI Act + Reg. (EU) 2026/1744 (T2) | Art. 15 robustness/cybersecurity vocabulary as motivation; high-risk timeline (Annex III 2 Dec 2027, Annex I 2 Aug 2028 — snippets, verify on EUR-Lex) | classify the assistant as high-risk |
| OWASP LLM 2025, OWASP ASI 2026, ATLAS 2026.10 (T4) | taxonomy labels for every attack family (verified IDs above) | cite as evidence of prevalence |

**Status note.** Most standards texts could not be opened from this environment (unece.org, iso.org, eur-lex returned 403/WAF); their rows are based on secondary sources and search snippets and are marked UNVERIFIED in `lit/automotive.md`. Before citing them in the thesis, obtain the official texts (VW library).
