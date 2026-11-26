# References — "Agent Security and JEV"

Sources used in the presentation, grouped as in the deck. For each source: title, first author, venue, peer-review status, link, and the slides where it is used. Venues were checked on 24–26 November 2026 (OpenReview, ACL Anthology, USENIX, proceedings pages or citing papers).

**Peer-review status:** *Peer-reviewed* = published at a reviewed conference or journal. *Workshop* = peer-reviewed workshop. *Preprint* = arXiv only, not (yet) peer-reviewed. *Vendor / blog* = company documentation or blog post.

## 1. Attacks and benchmarks

| # | Source | Venue · status | Link | Slides |
|---|---|---|---|---|
| 1 | **AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks.** T. Jiang et al. | ICML 2026 (PMLR 306) · Peer-reviewed | [arXiv 2602.16901](https://arxiv.org/abs/2602.16901) · [code](https://github.com/TanqiuJiang/AgentLAB) | 5, 7, 10, 11, 21, 29 |
| 2 | **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.** E. Debenedetti et al. | NeurIPS 2024 Datasets & Benchmarks · Peer-reviewed | [arXiv 2406.13352](https://arxiv.org/abs/2406.13352) · [code](https://github.com/ethz-spylab/agentdojo) | 3, 6, 10, 13 |
| 3 | **InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents.** Q. Zhan et al. | Findings of ACL 2024 · Peer-reviewed | [arXiv 2403.02691](https://arxiv.org/abs/2403.02691) | 9, 10 |
| 4 | **AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents.** M. Andriushchenko et al. | ICLR 2025 · Peer-reviewed | [arXiv 2410.09024](https://arxiv.org/abs/2410.09024) | 3, 9, 10 |
| 5 | **Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents.** H. Zhang et al. | ICLR 2025 (poster) · Peer-reviewed | [arXiv 2410.02644](https://arxiv.org/abs/2410.02644) | 8 |
| 6 | **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** (ASB re-analysis). R. Bhagwatkar et al. | NeurIPS 2025 Lock-LLM Workshop · Workshop | [arXiv 2510.05244](https://arxiv.org/abs/2510.05244) | 8 |
| 7 | **AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases.** Z. Chen et al. | NeurIPS 2024 · Peer-reviewed | [arXiv 2407.12784](https://arxiv.org/abs/2407.12784) · [code](https://github.com/BillChan226/AgentPoison) | 3, 7 |
| 8 | **MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers.** Z. Wang et al. | AAAI 2026 (Proc. AAAI 40(42), 35811–35819) · Peer-reviewed | [arXiv 2508.14925](https://arxiv.org/abs/2508.14925) | 3 |
| 9 | **WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks.** I. Evtimov et al. | NeurIPS 2025 Datasets & Benchmarks · Peer-reviewed | [arXiv 2504.18575](https://arxiv.org/abs/2504.18575) | 13 |
| 10 | **CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty.** J. Kirmayr et al. | ACL 2026 · Peer-reviewed | [arXiv 2601.22027](https://arxiv.org/abs/2601.22027) · [code](https://github.com/CAR-bench/car-bench) | 10, 29, 31 |

## 2. Judges and evaluation

| # | Source | Venue · status | Link | Slides |
|---|---|---|---|---|
| 11 | **R-Judge: Benchmarking Safety Risk Awareness for LLM Agents.** T. Yuan et al. | Findings of EMNLP 2024 · Peer-reviewed | [arXiv 2401.10019](https://arxiv.org/abs/2401.10019) | 12 |
| 12 | **AgentAuditor: Human-Level Safety and Security Evaluation for LLM Agents.** H. Luo et al. | NeurIPS 2025 · Peer-reviewed | [arXiv 2506.00641](https://arxiv.org/abs/2506.00641) | 12 |
| 13 | **A Coin Flip for Safety: LLM Judges Fail to Reliably Measure Adversarial Robustness.** L. Schwinn et al. | ICML 2026 · Peer-reviewed | [arXiv 2603.06594](https://arxiv.org/abs/2603.06594) | 11 |

## 3. Defences

| # | Source | Venue · status | Link | Slides |
|---|---|---|---|---|
| 14 | **The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections.** M. Nasr, N. Carlini et al. | USENIX Security 2026 · Peer-reviewed (an earlier version was rejected at ICLR 2026) | [arXiv 2510.09023](https://arxiv.org/abs/2510.09023) · [USENIX page](https://www.usenix.org/conference/usenixsecurity26/presentation/nasr) | 6, 16, 18 |
| 15 | **Defeating Prompt Injections by Design** (CaMeL). E. Debenedetti et al. | IEEE SaTML 2026, pp. 587–618, DOI 10.1109/SaTML68715.2026.00040 · Peer-reviewed | [arXiv 2503.18813](https://arxiv.org/abs/2503.18813) · [code](https://github.com/google-research/camel-prompt-injection) | 17, 18 |
| 16 | **MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents.** K. Zhu et al. | ICML 2025 · Peer-reviewed | [arXiv 2502.05174](https://arxiv.org/abs/2502.05174) | 16, 19 |
| 17 | **Design Patterns for Securing LLM Agents against Prompt Injections.** L. Beurer-Kellner et al. | arXiv · Preprint | [arXiv 2506.08837](https://arxiv.org/abs/2506.08837) | 15 |
| 18 | **Right Tool, Wrong Parameters: Defending LLM Agents Against Parameter Poisoning** (AuthorityFlow). Y. Wang et al. | arXiv · Preprint | [arXiv 2611.04673](https://arxiv.org/abs/2611.04673) | 18 |
| 19 | **Signed but Not Safe: Requirement Integrity in Multi-Agent LLM Handoffs.** Chen et al. | arXiv · Preprint | [arXiv 2611.07483](https://arxiv.org/abs/2611.07483) | 18 |
| 20 | **PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free** (arXiv title: *InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models*). H. Li et al. | ACL 2025 (long) · Peer-reviewed | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468/) · [arXiv 2410.22770](https://arxiv.org/abs/2410.22770) | 16, 20 |
| 21 | **Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents.** Liu et al. *(source of the PIGuard 95.1% vs 2.1% numbers; not on the reference slide yet)* | arXiv · Preprint | [arXiv 2610.03448](https://arxiv.org/abs/2610.03448) | 20 |
| 22 | **Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.** H. Inan et al. (Meta) | arXiv · Preprint (technical report) | [arXiv 2312.06674](https://arxiv.org/abs/2312.06674) | 20, 21 |

## 4. JEV (decision models)

| # | Source | Venue · status | Link | Slides |
|---|---|---|---|---|
| 23 | **TypeSafe AI documentation and blog** (JEV launch, System One models, confidence, model jaggedness, changelog) | Vendor documentation | [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) · [Docs: System One](https://docs.typesafe.ai/concepts/system-one) · [Models](https://docs.typesafe.ai/models) · [Confidence](https://docs.typesafe.ai/confidence) · [Model jaggedness](https://docs.typesafe.ai/model-jaggedness) · [Changelog](https://docs.typesafe.ai/changelog) | 22–25, 28 |
| 24 | **JEV-as-a-Judge: Accept When Confident, Escalate When Unsure.** Li et al. (CMU) | arXiv · Preprint | [arXiv 2609.26550](https://arxiv.org/abs/2609.26550) | 26, 27, 28 |
| 25 | **Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places.** Rao, Callison-Burch (UPenn) | arXiv · Preprint | [arXiv 2609.29769](https://arxiv.org/abs/2609.29769) | 28 |
| 26 | **Jev as a judge: How counterfeit policy steers Jev.** N. Frichette, F. Al-Kassar (Datadog Security Labs), 15 Oct 2026 | Industry blog | [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/) | 9, 28 |
| 27 | **Jev's Architecture Unmasked** (independent test with about 10,000 requests). A. Hume | Blog | [archerhume.com](https://archerhume.com/posts/jevs-architecture-unmasked) | 23, 24 |
| 28 | **Open decision-model replicas:** Kev; Perplexity Decider | Model cards | [Kev (Hugging Face)](https://huggingface.co/Terom/kev-0.5b) · [Perplexity Decider v1.1](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b) | 23, 28 |

## 5. Newer work used to check the research gaps

| # | Source | Venue · status | Link | Slides |
|---|---|---|---|---|
| 29 | **From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization.** D. Afroze et al. | arXiv · Preprint | [arXiv 2609.19630](https://arxiv.org/abs/2609.19630) | 30 |
| 30 | **Adaptive Adversaries: A Multi-Turn, Multi-LLM Benchmark for LLM Agent Security.** D. Jain et al. | NeurIPS 2026 Evaluations & Datasets Track (also ICML 2026 AIWILD workshop) · Peer-reviewed | [arXiv 2607.18063](https://arxiv.org/abs/2607.18063) · [OpenReview](https://openreview.net/forum?id=TwAO2rViBV) | 30 |
| 31 | **CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents** (NOVA). Foerster et al. | arXiv · Preprint | [arXiv 2601.09923](https://arxiv.org/abs/2601.09923) | 30 |
| 32 | **Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.** J. Peters-Gill et al. | arXiv · Preprint | [arXiv 2610.05640](https://arxiv.org/abs/2610.05640) | 30 |
| 33 | **JEV as a Judge for Agent Trace Security: An Empirical Comparison with Generative LLM Judges.** Wang, Gao (USTC) | arXiv · Preprint | [arXiv 2609.34862](https://arxiv.org/abs/2609.34862) | 9, 30 |
| 34 | **Beyond Attack-Success Rate: Action-Graded Severity Scale for Tool-Using AI Agents.** Owiredu-Ashley et al. | arXiv · Preprint | [arXiv 2607.07474](https://arxiv.org/abs/2607.07474) | 14, 30 |
| 35 | **FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems.** Y. Long et al. | arXiv · Preprint | [arXiv 2509.24408](https://arxiv.org/abs/2509.24408) | 2, 30 |
| 36 | **CHAI: Command Hijacking against Embodied AI.** L. Burbano et al. | IEEE SaTML 2026 · Peer-reviewed | [arXiv 2510.00181](https://arxiv.org/abs/2510.00181) | 2, 30 |

## 6. Other

- **Zhaokun's thesis** (slide 20, Llama Guard result) — please add author, title, year and university.
- **Own re-analyses of public artefacts** (slides 5, 7, 8, 14): attempt-budget analysis of AgentLAB's published task-injection results, clean-run noise of CAR-bench's published trajectories, and a replay of AgentDojo's stored clean runs against all attack checks. These are my own analyses of the authors' public code and data (AgentLAB, CAR-bench, AgentDojo; all MIT-licensed), not peer-reviewed results. Scripts and outputs available on request.

## Notes on venue status

- Peer-reviewed (main venues): 1–5, 7–16, 20, 30, 36. Workshop: 6. Preprints: 17–19, 21, 22, 24, 25, 29, 31–35. Vendor or blog: 23, 26–28.
- **Corrections compared with the slide version of the reference list:**
  - #14 The Attacker Moves Second is now **USENIX Security 2026**; it was rejected at ICLR 2026 (both shown on OpenReview and usenix.org).
  - #15 CaMeL is **IEEE SaTML 2026**; the slide lists only the arXiv number.
  - #30 Adaptive Adversaries is now **NeurIPS 2026 E&D**.
  - #11 R-Judge is **Findings of EMNLP 2024**.
  - #21 is added; it is the source of the PIGuard numbers on slide 20.
- arXiv numbers were checked against the arXiv titles. The CaMeL page numbers come from Semantic Scholar/DBLP and two citing papers; the IEEE Xplore page itself could not be opened from my environment.
