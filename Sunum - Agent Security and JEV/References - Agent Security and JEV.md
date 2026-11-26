# Sources behind my presentation "Agent Security and JEV"

Dear Ms. Navruz,

here are the sources I used to prepare the slides, in the same order as the presentation. For each one I wrote in a sentence or two what I took from it, where it was published, and on which slides it appears, so you can find the source of any number quickly.

A short note on how much weight each source carries. Most of them are **peer-reviewed** papers from conferences such as ICML, NeurIPS, ICLR, ACL or USENIX Security. Some are **preprints**: papers on arXiv that have not been reviewed yet. A few, mostly in the JEV part, are **company documentation or blog posts**. I mark this for every source, because I think it matters how much we can trust each number. JEV is very new (September 2026), so almost all the evidence about it is still preprints or company material.

All arXiv links follow the pattern arxiv.org/abs/NUMBER, so every paper can also be found by its number alone.

## 1. The problem and the attacks

**AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks.** Jiang et al. · *ICML 2026, peer-reviewed.*
This is the main paper my presentation builds on. I used its five attack types (intent hijacking, tool chaining, task injection, objective drifting, memory poisoning), its main results (one-message attack 62.5% vs many-step attack 79.9% on GPT-4o; tool chaining 73–96%), its Table 4 on how standard defences do against long attacks, and the fact that it uses an LLM judge (GPT-5.1).
Link: https://arxiv.org/abs/2602.16901 · Code: https://github.com/TanqiuJiang/AgentLAB
Slides: 5, 7, 9, 10, 11, 13, 21, 29, 30, 31

**AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.** Debenedetti et al. · *NeurIPS 2024 (Datasets & Benchmarks), peer-reviewed.*
The standard test environment for attacks hidden in data. I took the example attack text word for word from it, the 47.7% success of that simple attack on GPT-4o, its way of deciding success with code instead of an LLM, and its three numbers (benign utility, utility under attack, targeted ASR).
Link: https://arxiv.org/abs/2406.13352 · Code: https://github.com/ethz-spylab/agentdojo
Slides: 3, 6, 9, 10, 13, 16, 19, 20

**AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents.** Andriushchenko et al. · *ICLR 2025, peer-reviewed.*
Shows the attack through the user's own request: GPT-4o did 48.4% of harmful tasks just because it was asked, 72.7% with a simple trick. Also my example of an evaluator built on written rules with only small LLM checks.
Link: https://arxiv.org/abs/2410.09024
Slides: 3, 9, 10

**MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers.** Wang et al. · *AAAI 2026, peer-reviewed.*
The attack through an app's description: 1,348 tests on real apps, o1-mini tricked 72.8% of the time, and models almost never refused.
Link: https://arxiv.org/abs/2508.14925
Slide: 3

**AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases.** Chen et al. · *NeurIPS 2024, peer-reviewed.*
The memory attack on a driving agent. One correction to my slide 7: the "more than 80%" is how often the poisoned memory was *retrieved*; the agent actually carried out the attacker's goal in 56.8% of cases (Table 1). Still high, but I want to say it precisely.
Link: https://arxiv.org/abs/2407.12784 · Code: https://github.com/BillChan226/AgentPoison
Slides: 3, 7, 30

## 2. Evaluators: who decides that an attack worked?

**Agent Security Bench (ASB).** Zhang et al. · *ICLR 2025, peer-reviewed.*
**Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** Bhagwatkar et al. · *NeurIPS 2025 Lock-LLM Workshop, peer-reviewed workshop.*
I use these two together as my main warning example. In ASB the attacker's tool was always added to the agent's tool list. When the second team let the agent choose its own tools, the success rate on GPT-4o fell from 73.58% to 9.25%. This is also where my fifth question ("could a real attacker reach the agent this way?") comes from.
Links: https://arxiv.org/abs/2410.02644 · https://arxiv.org/abs/2510.05244
Slides: 8, 14

**InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents.** Zhan et al. · *Findings of ACL 2024, peer-reviewed.*
An example of a benchmark that decides success with code (did the agent call the attacker's tool?), 1,054 test cases.
Link: https://arxiv.org/abs/2403.02691
Slides: 9, 10

**CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty.** Kirmayr et al. (BMW Group Research) · *ACL 2026, peer-reviewed.*
The closest in-car benchmark: 58 car tools, 19 rules, 240 tasks, but no attacks. It is the base for my planned environment. I also used its finding that even the best model gets only about half of the tasks right in all three tries, which is why I want to run every task once without an attack.
Link: https://arxiv.org/abs/2601.22027 · Code: https://github.com/CAR-bench/car-bench
Slides: 10, 29, 31

**A Coin Flip for Safety: LLM Judges Fail to Reliably Measure Adversarial Robustness.** Schwinn et al. · *ICML 2026, peer-reviewed.*
The reason I want human-labelled data: compared with 6,642 human labels, LLM judges in attack tests were close to guessing.
Link: https://arxiv.org/abs/2603.06594
Slide: 11

**R-Judge: Benchmarking Safety Risk Awareness for LLM Agents.** Yuan et al. · *Findings of EMNLP 2024, peer-reviewed.*
**AgentAuditor: Human-Level Safety and Security Evaluation for LLM Agents.** Luo et al. · *NeurIPS 2025, peer-reviewed.*
Together they show that judges can be checked against humans and can get better: the best judge in R-Judge reached 74.45; AgentAuditor reached up to 96.3 on the same test.
Links: https://arxiv.org/abs/2401.10019 · https://arxiv.org/abs/2506.00641
Slide: 12

**WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks.** Evtimov et al. · *NeurIPS 2025 (Datasets & Benchmarks), peer-reviewed.*
Why one number is not enough: agents started following the attack in up to 86% of cases but finished it only 0–17% of the time ("security by incompetence").
Link: https://arxiv.org/abs/2504.18575
Slide: 13

## 3. Defences

**Design Patterns for Securing LLM Agents against Prompt Injections.** Beurer-Kellner et al. · *arXiv preprint.*
Background for how I split defences into two kinds (asking a model to notice the attack vs fixed rules in code). It is not named on a slide itself.
Link: https://arxiv.org/abs/2506.08837
Slide: 15 (background)

**The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections.** Nasr, Carlini et al. · *USENIX Security 2026, peer-reviewed.*
The "smart attacker" column on slide 16 and the first row on slide 18: when the attacker knows the defence, 12 prompt- and model-based defences were broken most of the time. On the slide I wrote "2025" (the arXiv year); it has since been accepted at USENIX Security 2026. An earlier version had been rejected at ICLR 2026.
Link: https://arxiv.org/abs/2510.09023 · Conference page: https://www.usenix.org/conference/usenixsecurity26/presentation/nasr
Slides: 6, 16, 18

**Defeating Prompt Injections by Design (CaMeL).** Debenedetti et al. (Google DeepMind, ETH Zurich) · *IEEE SaTML 2026, peer-reviewed.*
The system-design defence: how it works (the figure on slide 17 is the paper's Figure 5) and its cost, 77% of tasks done safely vs 84% without defence. This 77/84 is for one model (o3), not an average.
Link: https://arxiv.org/abs/2503.18813 · Code: https://github.com/google-research/camel-prompt-injection
Slides: 16, 17, 18, 30

**MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents.** Zhu et al. · *ICML 2025, peer-reviewed.*
Its Table 1 is the whole of slide 19: fewer attacks can also mean less work done (the LLM checker stops every attack but also every task).
Link: https://arxiv.org/abs/2502.05174
Slides: 16, 19

**Right Tool, Wrong Parameters: Defending LLM Agents Against Parameter Poisoning (AuthorityFlow).** Wang et al. · *arXiv preprint.*
Checking where each tool input came from: attack success 93% → 9%, finished tasks 90% → 83%.
Link: https://arxiv.org/abs/2611.04673
Slide: 18

**Signed but Not Safe: Requirement Integrity in Multi-Agent LLM Handoffs.** Chen et al. · *arXiv preprint.*
Rules in code vs an LLM checker on the same traces: 79% vs 59% of problems caught, 7% vs 50% false alarms.
Link: https://arxiv.org/abs/2611.07483
Slide: 18

**PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free.** Li et al. · *ACL 2025, peer-reviewed.* (On arXiv under its earlier name, InjecGuard.)
A checker model; one of the examples on slide 16 and the detector on slide 20.
Links: https://aclanthology.org/2025.acl-long.1468/ · https://arxiv.org/abs/2410.22770
Slides: 16, 20

**Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents.** Liu et al. · *arXiv preprint.*
This is where the PIGuard numbers on slide 20 come from (95.1% of attacks found on BIPIA, only 2.1% on AgentDojo). I forgot to put it on the reference slide, so I add it here.
Link: https://arxiv.org/abs/2610.03448
Slide: 20

**Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.** Inan et al. (Meta) · *arXiv technical report.*
The checker model that helps very little against long attacks, because no single message looks bad (AgentLAB Table 4).
Link: https://arxiv.org/abs/2312.06674
Slides: 20, 21

**Zhaokun's thesis** (slide 20). *I still need to add the full reference: author, title, year and university.*

## 4. JEV

**TypeSafe AI documentation and launch blog.** *Company documentation.*
What JEV is, its three question types (Noul, Choice, Score), the quote "Jev makes judgments, code makes decisions", the release date and version, and its claim that its confidence is calibrated. This is the company's own description, not an independent test.
Links: https://typesafe.ai/blog/introducing-system-one-models-and-jev · https://docs.typesafe.ai/concepts/system-one · https://docs.typesafe.ai/models · https://docs.typesafe.ai/changelog · https://docs.typesafe.ai/model-jaggedness
Slides: 22, 23, 24, 25, 28

**Jev's Architecture Unmasked.** Hume · *Independent blog post.*
The outside test with about 10,000 requests: each question sees the shared information but not the other questions, and 200 options take as long as 2.
Link: https://archerhume.com/posts/jevs-architecture-unmasked
Slides: 23, 24

**Open copies of the idea: Kev and Perplexity Decider.** *Model cards on Hugging Face.*
They show that a normal open model plus one small scoring layer gets close to JEV.
Links: https://huggingface.co/Terom/kev-0.5b · https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b
Slides: 23, 24

TypeSafe has not published how JEV works inside. Slides 23 and 24 put the picture together from these three kinds of sources, so they are my best reconstruction, not confirmed facts.

**JEV-as-a-Judge: Accept When Confident, Escalate When Unsure.** Li et al. (CMU) · *arXiv preprint.*
The biggest comparison: JEV against 16 other judges (Table 1 on slide 26), the two-step "cascade" that gives +0.9 points over GPT-6 at 41% of the cost, the advice to set the threshold with about 100 labelled examples, and the finding that six open models reach about the same accuracy.
Link: https://arxiv.org/abs/2609.26550
Slides: 26, 27, 28

**Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places.** Rao, Callison-Burch (UPenn) · *arXiv preprint.*
LLM judges cost 16 to 357 times more but were significantly better in at most 6 of 27 comparisons, and they repeated 96% of JEV's most confident mistakes.
Link: https://arxiv.org/abs/2609.29769
Slide: 28

**Jev as a judge: How counterfeit policy steers Jev.** Frichette, Al-Kassar (Datadog Security Labs) · *Industry blog.*
A fake rule hidden in the input changed the meaning of "attack", and JEV's detection score fell from 90.51% to 7.46%. This is the most important weakness for my topic.
Link: https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/
Slide: 28

## 5. Newer work I used to check that the gaps are really open

Before slide 30 I searched again for anything that might already fill my gaps. These are the closest works I found. Most are still preprints, and some made a gap smaller than I first thought.

**From Intent to Action: Benchmarking LLM Safety in Vehicle Voice Command Authorization.** Afroze et al. · *arXiv preprint.*
The closest in-car work: 202 voice-command scenarios, but each is a single command, not a many-step attack (gap 1).
Link: https://arxiv.org/abs/2609.19630

**FuncPoison: Poisoning Function Library to Hijack Multi-agent Autonomous Driving Systems.** Long et al. · *arXiv preprint.*
**CHAI: Command Hijacking against Embodied AI.** Burbano et al. · *IEEE SaTML 2026, peer-reviewed.*
Attacks on driving agents, not on an in-car assistant (gap 1).
Links: https://arxiv.org/abs/2509.24408 · https://arxiv.org/abs/2510.00181

**Adaptive Adversaries: A Multi-Turn, Multi-LLM Benchmark for LLM Agent Security.** Jain et al. · *NeurIPS 2026 Evaluations & Datasets Track, peer-reviewed.*
A smart attacker over 15 rounds, but the defending model sees each round fresh, so it is not one long agent task (gap 3). On the slide notes I called it a workshop paper; it has since been accepted at NeurIPS 2026.
Link: https://arxiv.org/abs/2607.18063

**CaMeLs Can Use Computers Too (NOVA).** Foerster et al. · *arXiv preprint.*
**Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks.** Peters-Gill et al. · *arXiv preprint.*
CaMeL moved to computer use and to teams of agents, but not tested against long attacks (gap 4).
Links: https://arxiv.org/abs/2601.09923 · https://arxiv.org/abs/2610.05640

**JEV as a Judge for Agent Trace Security: An Empirical Comparison with Generative LLM Judges.** Wang, Gao (USTC) · *arXiv preprint.*
JEV tested on 5,219 agent traces, but not on long attacks or in a car (gap 5). Also the "one study" on slide 9.
Link: https://arxiv.org/abs/2609.34862
Slides: 9, 30

**Beyond Attack-Success Rate: Action-Graded Severity Scale for Tool-Using AI Agents.** Owiredu-Ashley et al. · *arXiv preprint.*
A harm scale for tool calls (L0–L6), but not for physical car actions (gap 6).
Link: https://arxiv.org/abs/2607.07474

All of the above are on slide 30 (FuncPoison, CHAI and AgentPoison in the speaker notes).

## 6. What is my own work

Some points in the presentation are my own analysis of the public code and data of AgentLAB, CAR-bench and AgentDojo (all open source under the MIT licence), for example how much AgentLAB's numbers depend on the number of attempts allowed. The five questions on slide 14 and "Checked ASR" are my own proposal. None of this is peer-reviewed. I am happy to share the scripts and results.

## 7. Updates since the slides were made

- *The Attacker Moves Second* is now **USENIX Security 2026** (slide 16 says 2025).
- *CaMeL* is now published at **IEEE SaTML 2026** (the reference slide only gives the arXiv number).
- *Adaptive Adversaries* is now **NeurIPS 2026**, not only a workshop paper.
- *AgentPoison* on slide 7: "more than 80%" is retrieval; end-to-end it is 56.8%.
- *Passing the Test You Trained On* was missing from the reference slide and is added above.
