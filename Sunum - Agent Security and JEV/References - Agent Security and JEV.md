# Sources — Agent Security and JEV

## Attacks

**AgentLAB** — Peer-reviewed (ICML 2026)
The main benchmark for long, many-step attacks on agents: five attack types, 644 test cases.
Link: https://arxiv.org/abs/2602.16901
Code: https://github.com/TanqiuJiang/AgentLAB

**AgentDojo** — Peer-reviewed (NeurIPS 2024)
Standard test environment for attacks hidden in data (emails, reviews). Success is checked by code, not by an LLM.
Link: https://arxiv.org/abs/2406.13352
Code: https://github.com/ethz-spylab/agentdojo

**AgentHarm** — Peer-reviewed (ICLR 2025)
Tests whether agents carry out harmful tasks when the user simply asks.
Link: https://arxiv.org/abs/2410.09024

**InjecAgent** — Peer-reviewed (Findings of ACL 2024)
1,054 attacks hidden in tool outputs; success is checked by code.
Link: https://arxiv.org/abs/2403.02691

**MCPTox** — Peer-reviewed (AAAI 2026)
Attacks hidden in the descriptions of real connected apps (MCP servers).
Link: https://arxiv.org/abs/2508.14925

**AgentPoison** — Peer-reviewed (NeurIPS 2024)
Poisons an agent's memory, including a driving agent.
Link: https://arxiv.org/abs/2407.12784
Code: https://github.com/BillChan226/AgentPoison

## Evaluation

**Agent Security Bench (ASB)** — Peer-reviewed (ICLR 2025)
Large attack benchmark; its high success rates partly came from how the test was built.
Link: https://arxiv.org/abs/2410.02644

**Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** — Peer-reviewed workshop (NeurIPS 2025 Lock-LLM)
Re-ran ASB fairly: attack success on GPT-4o fell from 73.58% to 9.25%.
Link: https://arxiv.org/abs/2510.05244

**CAR-bench** — Peer-reviewed (ACL 2026)
In-car agent benchmark (BMW Group Research): 58 car tools, 240 tasks, no attacks. Base for my environment.
Link: https://arxiv.org/abs/2601.22027
Code: https://github.com/CAR-bench/car-bench

**WASP** — Peer-reviewed (NeurIPS 2025)
Web-agent attacks; shows that agents often start an attack but rarely finish it.
Link: https://arxiv.org/abs/2504.18575

**A Coin Flip for Safety** — Peer-reviewed (ICML 2026)
Compared with human labels, LLM judges in attack tests are close to guessing.
Link: https://arxiv.org/abs/2603.06594

**R-Judge** — Peer-reviewed (Findings of EMNLP 2024)
Tests how well LLMs judge whether agent conversations are safe; the best scored 74.45%.
Link: https://arxiv.org/abs/2401.10019

**AgentAuditor** — Peer-reviewed (NeurIPS 2025)
Gives the judge memory of labelled examples; reaches near-human accuracy.
Link: https://arxiv.org/abs/2506.00641

## Defences

**The Attacker Moves Second** — Peer-reviewed (USENIX Security 2026)
An attacker who knows the defence broke 12 published defences most of the time.
Link: https://arxiv.org/abs/2510.09023

**CaMeL (Defeating Prompt Injections by Design)** — Peer-reviewed (IEEE SaTML 2026)
Defence by system design: untrusted data can never change the agent's plan. 77% of tasks done safely vs 84% with no defence.
Link: https://arxiv.org/abs/2503.18813
Code: https://github.com/google-research/camel-prompt-injection

**MELON** — Peer-reviewed (ICML 2025)
Runs the agent twice and compares; its table shows defences also cost finished tasks.
Link: https://arxiv.org/abs/2502.05174

**PIGuard (InjecGuard)** — Peer-reviewed (ACL 2025)
A small model that detects attack text before the agent reads it.
Link: https://aclanthology.org/2025.acl-long.1468/

**Llama Guard** — Not peer-reviewed (Meta technical report)
Checker model for unsafe messages; helps little against many-step attacks.
Link: https://arxiv.org/abs/2312.06674

**Design Patterns for Securing LLM Agents against Prompt Injections** — Not peer-reviewed (arXiv)
Overview of system-design defences; background for "two kinds of defences".
Link: https://arxiv.org/abs/2506.08837

**AuthorityFlow (Right Tool, Wrong Parameters)** — Not peer-reviewed (arXiv)
Checks where each tool input came from: attack success 93% → 9%.
Link: https://arxiv.org/abs/2611.04673

**Signed but Not Safe** — Not peer-reviewed (arXiv)
Rules in code catch more problems with fewer false alarms than an LLM checker.
Link: https://arxiv.org/abs/2611.07483

**Passing the Test You Trained On** — Not peer-reviewed (arXiv)
Attack detectors work on data like their training data but fail on new tests (PIGuard 95.1% vs 2.1%).
Link: https://arxiv.org/abs/2610.03448

## JEV

**TypeSafe AI documentation** — Company documentation
What JEV is and how to use it, from the company that makes it.
Link: https://typesafe.ai/blog/introducing-system-one-models-and-jev
Docs: https://docs.typesafe.ai/concepts/system-one

**JEV-as-a-Judge (CMU)** — Not peer-reviewed (arXiv)
Compares JEV with 16 other judges; JEV is very cheap and good on easy decisions, weaker when reasoning is needed.
Link: https://arxiv.org/abs/2609.26550

**Decision Models vs. LLMs as Rubric Judges (UPenn)** — Not peer-reviewed (arXiv)
LLM judges cost much more than JEV but rarely do better, and they make the same mistakes.
Link: https://arxiv.org/abs/2609.29769

**Jev as a judge: How counterfeit policy steers Jev (Datadog)** — Company blog
A fake rule hidden in the text made JEV's attack detection drop from 90.51% to 7.46%.
Link: https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/

**Jev's Architecture Unmasked (Hume)** — Blog
Outside test with about 10,000 requests to work out how JEV is built.
Link: https://archerhume.com/posts/jevs-architecture-unmasked

**Kev and Perplexity Decider** — Open models (Hugging Face)
Open copies of the JEV idea that we can run ourselves.
Links: https://huggingface.co/Terom/kev-0.5b · https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b

## Newer work used to check the research gaps

**From Intent to Action** — Not peer-reviewed (arXiv)
In-car voice command safety test; single commands only, no many-step attacks.
Link: https://arxiv.org/abs/2609.19630

**Adaptive Adversaries** — Peer-reviewed (NeurIPS 2026)
An attacker that adapts over 15 rounds, but not inside one long agent task.
Link: https://arxiv.org/abs/2607.18063

**CaMeLs Can Use Computers Too** — Not peer-reviewed (arXiv)
CaMeL applied to computer-use agents.
Link: https://arxiv.org/abs/2601.09923

**Can CaMeLs Talk?** — Not peer-reviewed (arXiv)
CaMeL applied to teams of agents.
Link: https://arxiv.org/abs/2610.05640

**JEV as a Judge for Agent Trace Security (USTC)** — Not peer-reviewed (arXiv)
JEV tested on 5,219 agent traces, but not on long attacks or in a car.
Link: https://arxiv.org/abs/2609.34862

**Beyond Attack-Success Rate (Severity Scale)** — Not peer-reviewed (arXiv)
A harm scale (L0–L6) for agent tool calls; nothing similar for car actions.
Link: https://arxiv.org/abs/2607.07474

**FuncPoison** — Not peer-reviewed (arXiv)
Attack on multi-agent autonomous driving systems through their function library.
Link: https://arxiv.org/abs/2509.24408

**CHAI** — Peer-reviewed (IEEE SaTML 2026)
Hijacks embodied AI (e.g. drones, cars) with text placed in the camera view.
Link: https://arxiv.org/abs/2510.00181
