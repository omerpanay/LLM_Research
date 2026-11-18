# Evaluation science for agent security: benchmarks, success oracles, LLM judges, metrics, and JEV

*Survey for the thesis "Robustness of agentic AI to adversarial attacks: an adversarial-example pipeline for long-horizon tasks, evaluating in-vehicle LLM agents across agent architectures" (Attack, Evaluate, Defense). Compiled 18 November 2026.*

**How to read this file.**
- **Verification labels.** PRIMARY-READ: I downloaded the full PDF or page, converted it to text, and read the passages that every number below comes from. ABSTRACT-ONLY: I read only the arXiv or OpenReview abstract page. UNVERIFIED: I could not open the primary text.
- **Tiers.** T1: peer-reviewed main track at a top venue. T2: peer-reviewed workshop, journal or standard. T3: arXiv, technical report or official lab research. T4: blog, talk, GitHub or forum. Every venue claim says how I checked it, either through the OpenReview `venue` field, an ACL Anthology page, or the paper's own camera-ready footer. When the only evidence is the author's own statement, the tier is marked "claimed".
- **Inference.** Any line that starts with "Inference:" is my own reasoning, not a claim from the source.
- **Main-session observations.** "Main-session observation" marks a finding the coordinating session made by inspecting a code repository or released data. It is not a literature claim.
- **Untrusted input.** Fetched pages were treated as data. Some papers quote attack payloads. I paraphrase those payloads and never reproduce them.

---

## 1. Area summary

**Solved, or close to it.**
- *Deterministic state oracles work where they can be written.* AgentDojo checks success with a "deterministic binary function" so that an injection cannot also hijack the evaluator [E-03]. AgentHarm, CAR-bench and ASPI use code first and LLM checks only for narrow sub-questions [E-05, E-07, E-19].
- *Statistical correction for an imperfect judge.* The Rogan–Gladen estimator, with an interval covering both test-set and calibration-set uncertainty, has an ICML 2026 treatment for LLM judges [E-25, E-26, E-28].
- *Paired designs with exact tests.* These are established practice [E-30, E-32, E-22].

**Open.**
1. *Is a counted success really an attack?* A large share of reported success comes from the harness or from invalid test cases, not from the agent:
   - On ASB, GPT-4o's attack success rate (ASR) falls from 73.58% to 9.25% once forced attack-tool injection is removed [E-01].
   - AgentDojo injections overwrite task-critical data [E-01].
   - Under an embedding-similarity validity rule, "Mistral appeared vulnerable on all 64 tasks, but only 26 had a successful valid attack" [E-45].
   - Label checks halve JEV's perturbation ASR (69.7 → 36.6) [E-37].
   - Agents are diverted from their task far more often than attacks complete end to end (17–86% vs ≤16%) [E-02].
   - The converse also holds: a low ASR mostly means injections were *ignored* (76–80% of failed attacks), not refused [E-44].
2. *Judges fail under the distribution shift that red-teaming creates.*
   - Judges degrade "to near random chance", and attacks exploit judge weaknesses to inflate their own success [E-16].
   - Benign wrappers flip LLM judges 57–100% of the time [E-46].
   - A change of style alone raises the false-negative rate by 0.24 [E-17].
   - Rubric rewrites flip up to 9.1% of verdicts [E-18].
   - Judges err in the same places, so ensembles and cascades help little [E-36].
3. *Long-horizon and multi-run metrics are immature.*
   - Turns-to-success is averaged over successes only [E-06].
   - Success within N attempts is reported as plain ASR [E-06, main-session observation].
   - pass^k exposes large inconsistency between runs [E-07, E-08].
   - Temperature 0 does not remove judge jitter [E-18].

**Overhyped.**
- *"Human-level" judges.* Their accuracy is measured on in-distribution data [E-15, E-20, E-24].
- *Detector leaderboards.* The best detector on the public BIPIA benchmark catches 2.1% of AgentDojo injections at 1% false-positive rate (FPR) [E-12].
- *JEV as a security judge.* Its cost and accuracy advantages are real on read-off judgments [E-35, E-36, E-40]. But:
  - It is a closed, versioned API.
  - The vendor documents that adversarial content "can move the answer" [E-34].
  - A counterfeit policy cuts its recall from 82.90% to 3.88% [E-41].
  - Injected false evidence reaches up to 100% ASR [E-43].
  - Nobody has tested it inside an agent loop under attack [E-35].

**Consequence for the thesis.** Measure attack success with:
- (a) a state oracle and a pre-run task-validity contract;
- (b) a paired clean/placebo vs attacked design;
- (c) stratified judge-error correction where a judge is unavoidable;
- (d) repeated trials with clustered intervals (Section 3).

---

## 2. Taxonomy of non-attacks

Each row is a way that a case can **look like** a successful attack without being one. For each, the table gives the evidence and a detection method you can implement in your pipeline.

| # | Non-attack type | What happens | Evidence from the literature | Detection method in your pipeline |
|---|---|---|---|---|
| N1 | **Harness-forced action** | The benchmark itself inserts the attacker tool or overrides the plan, so the "malicious" call is not the agent's own choice. | ASB forcibly injects attack tools into each sub-task's tool list. GPT-4o ASR drops from 73.58 ± 2.70 to 9.25 ± 0.25 when this is removed (Table 5, E-01). "most of the original 'attack success' arises from benchmark-induced control-flow manipulation rather than agent vulnerability" (§7.2, E-01). | Provenance check: every attacker-goal action must trace back to an agent-generated tool call, with no harness-inserted options. Diff the tool lists offered in clean and attacked runs. |
| N2 | **Injection destroys task data** | The injection text replaces content the task needs, so a utility drop is data loss, not hijacking. | AgentDojo: "IPIs are implemented by replacing environment content that is essential for completing the task (e.g., overwriting the items and payment amounts in a bill)" (§7.1, App. D.1.1, E-01). After the fix, GPT-4o utility under attack rises from 60.87 to 72.19 (Table 5, E-01). | Placebo control: inject a benign text of the same length at the same position. Assert that every task-critical field survives injection; this is an invariant you can unit-test. |
| N3 | **Brittle oracle** | The success or utility check uses exact state deltas or counters, so a harmless extra event fails a correct run, or an empty run passes. | AgentDojo Slack task checks the inbox has "exactly one more message" (§7.1, E-01). ABC reports "TAU-bench counts empty responses as successful" and over- or underestimation "by up to 100% in relative terms" (abstract, E-09). ASB utility can be gamed by calling all tools (§7.2, E-01). | Audit oracles on clean runs and on hand-built adversarial "should fail" and "should pass" traces. Apply the ABC checklist (E-09). |
| N4 | **Capability failure ("security by incompetence")** | The agent is diverted but cannot complete the attacker's goal. Conversely, a low ASR reflects incompetence, not robustness. | WASP: "between 17-86% ASR-intermediate" vs "ASR-end-to-end of only up to 16%". "the main bottleneck for attack success is not the strength of their attack but rather the capability of the agent" (§4, E-02). | Report diverted, partial and end-to-end success separately. Run the attacker goal as a *legitimate* user task (WASP does this in its utility set) to estimate capability as the upper bound on ASR. |
| N5 | **Ordinary failure counted as attack** | Untargeted ASR (1 − utility under attack, UA) also counts failures that happen without any attack. | AgentDojo defines "the complement of this value as the untargeted attack success rate" (§3.4, E-03). GPT-4o benign utility is 69.0% (Table 5, E-03), so about 31% of tasks fail even with no attack. | Paired clean run per task and seed. Use causal ASR (M1 in Section 3). |
| N6 | **Judge false positive** | The LLM judge labels a benign or unhelpful output as harmful or compliant. | Judges degrade "to near random chance" under victim, attack and category shift. Correcting for precision makes "many attacks prove far less effective" (§4.3, E-16). GPT-4o-mini judge has a 45.7% FPR against human consensus (abstract, E-21). | Human-labelled calibration set stratified by attack × victim. Report corrected ASR (M2). Require more than one positive per behaviour (E-16). |
| N7 | **Attack optimised against the scoring judge** | The attacker's search loss uses the same judge that later scores success, so the attack learns to fool the judge. | "current optimization strategies may be targeting judge-specific noise ... that lack a meaningful correlation with the true adversarial objective" (§4.2, E-16). AgentLAB uses a GPT-5.1 "internal judge" for both refinement and evaluation (§5.1, App., E-06). Main-session observation: the AgentLAB repo's TextGrad loss optimises against the same GPT-5.1 text judge that scores Intent Hijacking. | Keep the optimisation judge separate from the evaluation judge (different model family). Evaluate with a state oracle or humans on a held-out sample. Report the gap between the two. |
| N8 | **Judge hijacked by the trace** | Text inside the trace (injection, counterfeit policy, persuasive framing) changes the judge's verdict. | AgentDojo avoids LLM evaluators because the attack "would also hijack the evaluation model" (§3.3, E-03). Output-level attacks make judges misclassify "100% of harmful generations as safe" (abstract, E-17). Counterfeit policy cuts JEV recall from 82.90% to 3.88% (E-41). TypeSafe: adversarial content "can move the answer" (E-34). | Use a state oracle for the decision. If a judge is unavoidable, red-team the judge with judge-targeted payloads, mask attacker-controlled spans, and report robustness separately. |
| N9 | **Perturbation changed the true label** | An "adversarial" edit changes the correct answer, so the model's changed decision is correct. | DecisionRobust: label checks cut JEV's sample-level combined ASR from 69.7% raw to 36.6% checked (Table 3, E-37). "most raw successes on NevIR and Siim fail them" (§3.2.1). | Label-consistency check: independent models or humans must recover the reference answer on the perturbed input (E-37). |
| N10 | **Legitimate or authorised instruction** | The "attacker" action is also requested or allowed by the user or policy, or the agent rightly asks for confirmation. | From Intent to Action separates 7 pre-action decisions ("execute, refuse, clarify, require confirmation, defer to manual control, trigger an emergency response, or make no tool call") (abstract, E-32). The JEV trace study revised labels to "distinguish resisted injections and signal-only cases from unsafe behavior" and states "encountering an attack does not establish that the agent followed it" (§3.1, §4.1, E-40). | Authorisation oracle: label each attacker-goal action against the user request and policy. In the clean counterfactual, if the same action occurs without injection, it is not attack-caused (M1). |
| N11 | **Harmless deviation** | The agent drifts from the user task, but the resulting action has no security consequence. | WASP's ASR-intermediate only asks whether the agent "has been diverted from its user goal" (§3.4, E-02). Action-Graded Severity shows a binary ASR "discards ... how harmful the resulting action was" (abstract, E-33). | Severity grading (M3). Count only predicates that cross scope, privilege or irreversibility, using an L0–L6 style scale. |
| N12 | **Claimed but not executed** | The agent *says* it did the harmful thing, or the scorer reads intended or parsed actions from a simulated environment. | InjecAgent simulates attacker-tool responses with GPT-4 and scores the parsed next action; ASR-valid drops invalid outputs from the denominator (§4, E-04). AgentHarm's grading functions "can sometimes miss an alternative execution trace" (Limitations, E-05). | Score from tool-execution logs and environment state, never from the agent's narration. Flag runs where narration and state disagree. |
| N13 | **Unrealistic threat model** | The attacker is given powers a real adversary lacks (forced tools, a tool-less chat victim, control of the user channel). | WASP criticises tests "giving the attacker too much power" (abstract, E-02). ASB forced tools (E-01). Main-session observation: AgentLAB's public Intent Hijacking implementation uses a tool-less chat victim scored by a text judge. | Threat-model card per attack: channel, attacker knowledge, query budget, what the attacker controls in a vehicle (POI data, messages, calendar, voice). Reject cases whose channel is not attacker-controllable. |
| N14 | **Denominator and budget artifacts** | ASR is computed on valid outputs only, or as success within N attempts, or on judges' own valid subsets. | InjecAgent ASR-valid (E-04). JEV trace study: DS-V4-Pro's "98.7% ATBench500 accuracy is based on only 151 of 500 trajectories" (§5.2, E-40). Main-session observation: AgentLAB task-injection ASRs equal success within up to 10 attempts (GPT-4o 32.6% at 1 attempt vs 79.9%). | Always report n, coverage, attempts budget k, and ASR@1 alongside ASR@k. Treat missing outputs as failures of the measurement, not as non-successes. |
| N15 | **Nondeterminism and single-run noise** | A single trial "succeeds" by chance. The judge flips on identical input. | Judge jitter at temperature 0: 5.0% (DeepSeek-V3.2), 6.8% (GPT-5.4-mini) (§4, Table, E-18). CAR-bench: "GPT-5 drop from 68% Pass@3 to 36% Pass^3" (E-07). Main-session observation: 12–34% of CAR-bench tasks flip between identical clean trials. Test-retest relabels 3–15% (abstract, E-21). | At least 3 to 5 repeats per (task, attack, defence). Paired tests. Estimate judge jitter by re-scoring identical traces. |
| N16 | **User-simulator error** | The LLM-simulated driver or user misbehaves and causes the failure or "success". | CAR-bench: Base had "12 user errors (2.4%), 6 sole-source (–6% Pass^5)"; Hallucination −9%; Disambiguation −8% (§4, E-07). | Audit simulator turns on all failing runs; mark sole-source simulator failures. |
| N17 | **Evaluation-awareness and eval/production gap** | The model behaves differently because it recognises a test. | OpenAI deployment simulation: traditional evaluations are "generally recognizable as tests"; simulation's "evaluation-awareness point estimates were also much closer to production traffic" (abstract, E-13). | Use realistic, non-templated scenarios. Measure verbalised evaluation awareness. Compare against realistic seeds. |
| N18 | **Detector or monitor false alarms at low base rate** | A detector "detects" an attack in a benign tool output. At realistic attack prevalence most alarms are false. | FPRs on benign tool outputs "range from none to over 90%" (abstract, E-12). Base-rate fallacy (E-29). | Report TPR at fixed low FPR measured on *your own* benign tool outputs. Convert to positive predictive value (PPV) at an assumed prevalence. |
| N19 | **Contamination, or training on the test** | High scores come from training-data overlap with the benchmark. | The BIPIA leader "was trained on full BIPIA inputs" (abstract, E-12). CMU JEV study "cannot rule out that benchmark items were seen in training" (Limitations, E-35). | Audit training data where public. Use fresh, in-house scenarios (the vehicle domain helps). |
| N20 | **Rubric-wording or annotator-panel artifact** | The verdict depends on how the rubric is phrased or which human panel defines truth. | Up to 9.1% verdict flips from content-preserving rewrites (abstract, E-18). One judge correlates 0.43–0.61 with an expert panel but 0.03–0.07 with a crowd panel on the same items (abstract, E-24). | Rubric-paraphrase invariance test (E-18). Name the reference panel. Report agreement per panel. |

| N21 | **Invalid test case: the "attack" edit changed the task itself** | The perturbation alters a fact that defines the task (for example the trusted payee), so the agent's changed action is correct. | Embedding thresholds "allowed 75-100% of edits that changed the task, such as swapping the payee". With a MiniLM threshold, "Mistral appeared vulnerable on all 64 tasks, but only 26 had a successful valid attack" (abstract, E-45). | An executable task contract checked *before* the run: task-defining facts, allowed edit fields, completion predicate (E-45). This is the agent analogue of N9. |
| N22 | **False evidence rather than instruction hijack** | The injected content asserts new "facts", for example that the state is outdated, and the model follows the evidence. The failure is in trust separation, not instruction-following. | The Jev-specific injection "first claims that the original application state is incorrect or outdated, and then adds false information that strongly supports the attacker-chosen target". It reaches 100% ASR on subscription cancellation (§IV-A, Table I, E-43). | Classify every payload as *instruction* vs *evidence* manipulation and report them separately. Check whether a correctly behaving system *could* have known the evidence was untrusted (provenance available?). |

**The inverse problem: things that look like defence success but are not.**
- *The attack was ignored, not resisted.* "most failed attacks are ignored (76-80%) rather than refused". Changing only the system prompt moves InjecAgent ASR "from 0.2% to 43%". In "21.7% of AgentDojo episodes, the agent stayed safe but did not complete the user's task" (abstract, E-44).
- *The low ASR comes from the model or a weak static attack.* "A low static ASR is cheaply earned". On Claude-Haiku-4.5 the static attack succeeds 0.3% of the time with no defence at all. An adaptive attack lifts PIGuard's ASR on GPT-4o-mini "from 0.0% to 28.0%" (§5, E-11).
- *The judge misses the success.* LLM judges show recall of "0.06 to 0.65" against human labels (abstract, E-46).
- **Detection.** Report the attack-outcome × task-outcome matrix (E-44's ATOM), an undefended baseline per model, and adaptive attacks (E-01 §8, E-11).

Inference on grouping:
- N1, N2, N3, N12 and N21 are *benchmark artifacts*.
- N4, N5 and N16 are *ordinary agent or capability failure*.
- N6, N7, N8, N15 and N20 are *measurement (judge) error*.
- N9, N10, N11 and N22 are *non-security or mis-specified behaviour*.

The supervisor's three-way split (real attack / benchmark artifact / ordinary failure) maps onto these four groups. Judge error is a fourth bucket that the thesis should report separately.

---

## 3. Metric catalogue

### 3.1 Existing metrics

| Metric | Definition | Source | Known pitfalls |
|---|---|---|---|
| Benign utility (BU) | Fraction of user tasks solved with no attack | AgentDojo §3.4 (E-03) | Brittle utility oracles (N3). |
| Utility under attack (UA) | Fraction of (user task, injection) pairs solved "without any adversarial side effects" | E-03 | Confounded by injections that overwrite task data (N2, E-01). |
| Untargeted ASR | 1 − UA | E-03 | Includes ordinary failures (N5). |
| Targeted ASR | Fraction of security cases where "the attacker's goal is met" (state oracle) | E-03 | Ignores severity. A collection of attacks counts as successful "if any of the attacks in the collection succeeds" (adaptive max). |
| ASR-valid / ASR-all | Successes among *valid* outputs / among all outputs | InjecAgent §4 (E-04) | ASR-valid drops invalid outputs from the denominator. Tool responses are simulated (N12, N14). |
| ASR-intermediate / ASR-end-to-end | Diverted from user goal (GPT-4o judge) / attacker goal reached (rule-based check of final state) | WASP §3.4 (E-02) | The intermediate score is judge-based. The gap between them is capability-limited (N4). |
| Harm score | Partial credit over "predefined, manually written conditions", with an LLM judge only for narrow semantic checks | AgentHarm §3.1.3 (E-05) | Open-ended criteria mean "perfectly successful runs may sometimes score less than 100%". |
| Refusal rate / non-refusal harm score | Refusal judge applied to all agent messages; harm computed on non-refused runs | E-05 | Refusal judge is itself an LLM. |
| ASR(n_turn), T2S | ASR as a function of the maximum attack turns; "average number of attack turns required for successful attacks" | AgentLAB §5.1, Fig. 7 (E-06) | T2S conditions on success, so it is censoring-biased. The judge also drives the optimisation (N7). |
| pass^k / pass@k | Task counts only if solved in all k trials / in at least one of k trials | τ-bench (E-08); CAR-bench §3.4 (E-07) | Unbiased estimation needs n ≥ k trials per task. |
| Decision Alignment, False Execute | Agreement with a reference pre-action decision (7 classes); executing when the reference is non-execution | From Intent to Action (E-32) | Reference decisions are author-defined. |
| Ordinal severity L0–L6 | Reversibility × cross-scope × privilege expansion of executed actions | Action-Graded Severity (E-33) | Judge panel "shares systematic blind spots", for example escalation chains. |
| TPR at 1% FPR | Detection rate at the threshold that gives 1% FPR on benign outputs | Passing the Test (E-12) | Only meaningful with the threshold set on *in-domain* benign outputs. |
| Precision-corrected ASR | Judge-ASR × P(true positive given judge positive) | Coin Flip §4.3 (E-16) | Precision depends on prevalence. It must be measured on the same mix. |
| Judge Concordance score | S_JC(x) = 1 − H(p_x), where p_x is the fraction of judges saying "harmful" | E-16 | High concordance "does not reliably imply correctness". |
| Δflip, Policy Invariance Score (PIS) | Verdict flips under rubric rewrites, above the identical-rerun jitter; PIS is a weighted composite (0.4, 0.3, 0.3) | E-18 | The composite weights are ad hoc. |
| Rogan–Gladen corrected rate | θ̂ = (p̂ + q̂₀ − 1)/(q̂₀ + q̂₁ − 1), with an adjusted-Wald CI | E-25, E-26, E-28 | Assumes the judge's error rates are the same in calibration and test. Wide intervals with small calibration sets. |
| Coverage / correct-decision yield | Fraction of items with a valid judgment / fraction with a correct judgment | JEV trace study §4.3 (E-40) | Metrics computed on each judge's "own valid responses" are not comparable. |
| Label-consistent ASR; flip vs target ASR | Success counted only if an independent label check passes; "flip" = any wrong decision, "target" = the attacker's chosen answer | DecisionRobust §3.1 (E-37) | Label checkers are themselves LLMs. |
| Paired ΔHCR + McNemar | Change in harmful-compliance rate between paired models, tested with McNemar | Audit the Difference (E-22) | Gives robustness to the choice of instrument, "not ground-truth validity". |
| Agreement statistics | Cohen's κ, Fleiss' κ, Gwet's AC1, Krippendorff's α | E-19, E-20, E-33 | κ is prevalence-sensitive. ASPI's perfect κ on one field "reflects the near-zero attack success rates in that condition". |
| ATOM (attack × task outcome matrix) | Cross-tabulates attack outcome (succeeded / ignored / refused) against user-task outcome (completed / not completed) | Ignored, Not Refused (E-44) | Ignored vs refused is labelled by an LLM judge ("label-blind"). |
| Over-refusal, Clarification Miss, Emergency Miss | Per-class error rates over the 41 EXECUTE, 20 CLARIFY and 16 EMERGENCY scenarios | From Intent to Action §4.2 (E-32) | Small per-class n, so use exact intervals. |
| Contract-valid ASR | Success counted only on perturbed cases that pass an executable task contract | Executable contracts (E-45) | Writing contracts takes manual effort per task family. |
| Clean-row baseline ASR | Rate at which the attacker's target is chosen with no attack | Hidden Risks of Jev Table I (E-43) | Often omitted. Without it, a target that is a plausible answer looks like an attack success. |

### 3.2 Candidate new metrics for the thesis

Notation:
- *i* indexes scenarios (task × attack instance). *r* = 1…R indexes repeated runs. *a* ∈ {0, 1} means clean or attacked.
- **G**(τ) ∈ {0, 1} is the attacker-goal predicate, evaluated by a state oracle on trajectory τ.
- **J**(τ) ∈ {0, 1} is the judge verdict.

**M1. Causal ASR from paired runs (CASR).** For each scenario, run the attacked condition and a *placebo* condition. The placebo has the same injection slot filled with benign text of the same length, which also controls for N2.

$$\mathrm{CASR}=\frac{1}{N}\sum_{i=1}^{N}\left(\bar G_i^{(1)}-\bar G_i^{(0)}\right),\qquad \bar G_i^{(a)}=\frac{1}{R}\sum_{r=1}^{R}G\big(\tau_{ir}^{(a)}\big).$$

- **Estimator.** Plug-in as written. Also report the attributable share $\mathrm{CASR}/\overline{G}^{(1)}$.
- **CI.** Cluster bootstrap over scenarios (resample *i*, keep all runs). With R = 1, use an exact McNemar test on the discordant pairs (n₁₀, n₀₁). With R > 1, use a sign-flip permutation test on the per-scenario differences.
- **Closest prior work.** AgentDojo's untargeted ASR (E-03); differential replay labelling (E-12); paired ΔHCR with McNemar (E-22); WASP's utility-on-attacker-goal control (E-02).
- **What is new.** A placebo arm plus the *same* goal predicate in both arms. This removes N2 and N5 by construction, and it is defined per scenario, so it suits long-horizon runs.

**M2. Judge-error-corrected ASR, stratified (RG-ASR).** Let *s* index strata (attack family × victim architecture). This is required because judge error rates shift across victims and attacks (E-16). From a human-labelled calibration set, estimate the judge's specificity $\hat q_{0s}$ and sensitivity $\hat q_{1s}$:

$$\hat\theta_s=\operatorname{clip}_{[0,1]}\!\left(\frac{\hat p_s+\hat q_{0s}-1}{\hat q_{0s}+\hat q_{1s}-1}\right),\qquad \hat\theta=\sum_s w_s\hat\theta_s .$$

- **CI.** Per stratum, the Lang–Reiczigel adjusted-Wald interval used by Lee et al. (eq. 6–8, E-25), which adds test-set and calibration-set variance. Combine strata by stratified bootstrap that resamples *both* the test and the calibration sets.
- **Alternative.** Prediction-powered inference (PPI/PPI++), which has "strictly smaller" asymptotic variance than Rogan–Gladen (E-26).
- **Validity condition.** Report $\hat q_{0s}+\hat q_{1s}-1$. If it is near 0 the estimator is undefined. This degeneracy is also documented in E-27.
- **Closest prior work.** E-25, E-26, E-16 (precision scaling).
- **What is new.** Stratification by agent architecture and attack family, and using the state oracle as the calibration "human" wherever it exists. For long-horizon traces, also report *where* the judge errs (E-27 shows cross-turn defects are missed).

**M3. Severity-weighted ASR (SW-ASR) and exceedance curve.** Each executed attacked trajectory gets an ordinal severity $L_i\in\{0,\dots,6\}$ (scale in the style of E-33, re-anchored to vehicle harms). Use the clean-arm severity to subtract baseline. Weights $w_\ell$ are fixed *before* the experiment with the safety team:

$$\mathrm{SWASR}=\frac{1}{N}\sum_i w_{L_i},\qquad E(\ell)=\Pr(L\ge \ell)\ \text{for } \ell=1..6 .$$

- **CI.** Cluster bootstrap. Validate the grader with Krippendorff's α (ordinal) against a human or oracle subset, as E-33 does (α = 0.91).
- **Closest prior work.** E-33; AgentHarm partial credit (E-05).
- **What is new.** Vehicle-specific anchors (comfort, privacy, driving-safety-relevant). Reporting the full exceedance curve E(ℓ) rather than one weighted number avoids hiding tail risk.

**M4. Turns-to-compromise survival curve.** Let $T_i$ be the first turn at which the goal predicate *becomes* true, right-censored at the turn budget *B*. Use the Kaplan–Meier estimator:

$$\hat S(t)=\prod_{t_j\le t}\left(1-\frac{d_j}{n_j}\right),\qquad \mathrm{ASR}(t)=1-\hat S(t),\qquad \mathrm{RMST}(B)=\int_0^B\hat S(t)\,dt .$$

- **CI.** Greenwood variance, or cluster bootstrap over scenarios. Compare defences with the log-rank test.
- **Closest prior work.** AgentLAB's ASR vs n_turn curves and T2S (E-06). T2S averages only over successes, which biases it under censoring.
- **What is new.** A censoring-correct estimate and restricted mean survival time (RMST) as a single long-horizon robustness number. Report ASR@1 attempt separately from ASR within *k* attempts (N14).

**M5. Transient unsafe-action rate (TUAR) and exposure.** Final-state oracles miss states that become unsafe and are then reverted. Let $u(s_t)\in\{0,1\}$ be an unsafe-state predicate on the vehicle state (for example a policy-forbidden actuator combination) at step *t*:

$$\mathrm{TUAR}=\frac1N\sum_i \max_t u(s_{it}),\qquad \mathrm{EXP}=\frac1N\sum_i\sum_t u(s_{it})\,\Delta t_{it}.$$

- **CI.** Cluster bootstrap. Pair it with M1 (subtract the clean arm).
- **Detection delay** for a monitor: $D_i=t^{\text{alarm}}_i-t^{\text{first unsafe}}_i$. Report $\Pr(D\le 0)$ (prevented) and the median *D*.
- **Closest prior work.** CAR-bench separates "actions final" from intermediate-state checks (§3.3, E-07). WASP's intermediate/end-to-end split (E-02). Final-state oracles (E-03, E-08).
- **What is new.** Time-in-unsafe-state as a first-class outcome, which matters for driving functions.

**M6. Driver-interaction cost (DIC) and false-block rate.** For benign scenarios, count driver prompts (confirmations, clarifications, refusals) that a defence adds over the undefended agent, and the rate of wrongly blocked benign actions:

$$\mathrm{DIC}=\frac1{N_b}\sum_{i\in\text{benign}}\big(c_i^{\text{def}}-c_i^{\text{none}}\big),\qquad \mathrm{FBR}=\Pr(\text{block}\mid\text{benign}).$$

- **Reporting.** Plot the (CASR, DIC) Pareto front. Use a cluster bootstrap and McNemar for FBR.
- **Closest prior work.** From Intent to Action's confirmation and clarification classes (E-32). ASPI shows that clarification-seeking *raises* injection ASR, for example 1.8% → 34.0% for o3 (abstract, E-19), so the clarifications a defence adds are both a cost *and* an attack surface.
- **What is new.** It turns usability cost in the driver's seat into a measured axis of the security–utility trade-off.

Statistics that apply to all of M1–M6:
- Treat the scenario as the unit of analysis, with cluster bootstrap over scenarios.
- Run R ≥ 3 repeats.
- Fix thresholds and weights before seeing results.
- Report n, coverage and the attempt budget.

Inference: E-30 ("Adding Error Bars") and the CLT position paper (E-31) are the methodological anchors. In particular, use bootstrap or exact intervals instead of CLT intervals for small n.

---

## 4. Entries

### E-01 · Firewalls / benchmark flaws — Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?
- **Authors, year, venue:** Bhagwatkar, Kasa et al. (ServiceNow, Mila), 2025 (v2 March 2026). NeurIPS 2025 Lock-LLM Workshop poster.
- **Tier:** T2. Verified via the OpenReview venue field "NeurIPS Lock-LLM Workshop 2025 Poster". The same record lists it as rejected at ICLR 2026 and under review at TMLR.
- **Link:** https://arxiv.org/abs/2510.05244
- **What it measures / how success is decided:** Re-runs AgentDojo, ASB, InjecAgent and τ-bench with tool-input and tool-output "firewalls", and audits each benchmark's success metrics.
- **Key results:**
  - Table 5 (GPT-4o, no defence): ASB ASR "Original Benchmark 73.58 ±2.70 / Revised Benchmark 9.25 ±0.25". AgentDojo UA under tool_knowledge "60.87 ±2.59 → 72.19 ± 2.79".
  - §7.2: "the ASR drops sharply from 70% to 9.25%, an almost 8× reduction". The text rounds to 70% while Table 5 reports 73.58, so cite the table.
  - §7.1: injections "overwriting the items and payment amounts in a bill to be paid ... makes the task unsolvable regardless of whether the agent disregards the malicious instruction".
  - Table 6 (AgentDojo Slack): a cascade attack lifts ASR against PromptArmor to 75.5 and against their Sanitizer to 30.0.
- **Pitfalls it exposes:** N1, N2, N3. InjecAgent has "no utility metric". Static attacks are saturated. Guidelines in §9 include "Benchmarks should not forcibly inject tools", "Injection vectors should be inserted without overwriting key inputs", and report BU, ASR and UA.
- **Verification:** PRIMARY-READ (§7–9, Appendix D).
- **Inference:** A benchmark audit is a mandatory step before any ASR enters the thesis. The ASB result alone shows the inflation can be about 8×.

### E-02 · WASP — WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks
- **Authors, year, venue:** Evtimov, Zharmagambetov et al. (Meta), 2025. NeurIPS 2025 Datasets and Benchmarks Track (poster). An earlier version was an ICML 2025 WCUA workshop poster.
- **Tier:** T1. Verified via the OpenReview venue field.
- **Link:** https://arxiv.org/abs/2504.18575
- **What it measures / how success is decided:**
  - ASR-end-to-end: a "rule-based evaluator to check if the final state satisfies the specified rule for attacker goal success".
  - ASR-intermediate: a GPT-4o judge decides "whether or not the agent has been diverted from its user goal" (§3.4).
  - Utility: 37 tasks, including the adversarial goals posed as legitimate user goals.
- **Key results:**
  - Abstract: "attacks partially succeed in up to 86% of the case". §4: "between 17-86% ASR-intermediate ... ASR-end-to-end of only up to 16%".
  - Table 2: o1, Tool Calling, system-level instruction hierarchy: 0.857 intermediate vs 0.167 end-to-end. GPT-4o VWA axtree+SOM: 0.429 vs 0.036.
  - §4: "We term this phenomenon 'security through incompetence'".
- **Pitfalls it exposes:** N4, N11, N13. Partial versus full success.
- **Verification:** PRIMARY-READ (§3.4, §4, Tables 2–3).
- **Inference:** As agents become more capable, ASR-end-to-end will rise even with no new attacks. Track it against capability (attacker goal as a legitimate task).

### E-03 · AgentDojo — AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents
- **Authors, year, venue:** Debenedetti, Zhang et al. (ETH Zürich), 2024. NeurIPS 2024 Datasets and Benchmarks Track.
- **Tier:** T1. Verified via the camera-ready footer "38th Conference on Neural Information Processing Systems (NeurIPS 2024) Track on Datasets and Benchmarks".
- **Link:** https://arxiv.org/abs/2406.13352
- **What it measures / how success is decided:** "The utility function is implemented as a deterministic binary function which, given outputs of the model together with the state of the environment before and after execution, determines whether the goal of the task has been accomplished". A security function checks the attacker goal (§3.3). The paper rejects LLM evaluators because the attack "would also hijack the evaluation model".
- **Key results:**
  - 97 tasks and 629 security cases (abstract).
  - GPT-4o, "Important message" attack: targeted ASR 57.7% (Table 4).
  - No defence: BU 69.0%, UA 50.01%, targeted ASR 57.69%. Tool filter: ASR 6.84% (Table 5). All with 95% CIs.
  - Running all 629 security cases on GPT-4o "costs around US$35" (App. D).
- **Pitfalls it exposes:** Untargeted ASR = 1 − UA mixes in ordinary failure (N5). Its own oracles are partly brittle and its injections overwrite task data (N2, N3, via E-01).
- **Verification:** PRIMARY-READ (§3.3–3.4, App. C–D).
- **Inference:** AgentDojo's oracle-first design is the template for an in-vehicle environment. Keep it, and add the placebo arm (M1).

### E-04 · InjecAgent — InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents
- **Authors, year, venue:** Zhan, Liang, Ying, Kang, 2024. Findings of ACL 2024.
- **Tier:** T1 (Findings). Verified via the ACL Anthology page 2024.findings-acl.624.
- **Link:** https://aclanthology.org/2024.findings-acl.624/
- **What it measures / how success is decided:**
  - Agents are not actually run against tools. The user-tool response is fixed, attacker-tool responses are "simulate[d] ... using GPT-4", and the *parsed next action* is scored.
  - "Outputs considered invalid ... are excluded". "ASR-valid as the ratio of successful attacks among valid outputs" (§4).
- **Key results:** 1,054 test cases. "ReAct-prompted GPT-4 vulnerable to attacks 24% of the time", rising to 47% in the enhanced setting (abstract, §4).
- **Pitfalls it exposes:** N12 (intended or parsed action, not an executed state), N14 (denominator excludes invalid outputs), and no utility metric (E-01).
- **Verification:** PRIMARY-READ (§3–4).
- **Inference:** Do not compare InjecAgent ASR-valid with state-oracle ASR from AgentDojo-style environments.

### E-05 · AgentHarm — AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents
- **Authors, year, venue:** Andriushchenko, Souly et al. (Gray Swan, UK AISI), 2024. ICLR 2025 (poster).
- **Tier:** T1. Verified via the OpenReview venue field "ICLR 2025 Poster" and the PDF header.
- **Link:** https://arxiv.org/abs/2410.09024
- **What it measures / how success is decided:** "The majority of our grading criteria checks are predefined, manually written conditions ... A semantic LLM judge is used whenever it is necessary to check the semantics of a portion of an output". LLMs are used "only for narrow and isolated grading tasks". A separate refusal judge is applied "on all messages" (§3.1.3).
- **Key results:** 110 malicious tasks (440 with augmentations). The template attack raises GPT-4o's harm score "from 48.4% to 72.7%" and lowers refusal "from 48.9% to 13.6%" (§4).
- **Pitfalls it exposes:** Grading "can sometimes miss an alternative execution trace that can be considered correct". No multi-turn attacks (Limitations).
- **Verification:** PRIMARY-READ (§3.1.3, §4, Limitations).
- **Inference:** "Rubric + narrow LLM checks" is the best-documented middle ground between pure oracles and holistic judges.

### E-06 · AgentLAB — AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks
- **Authors, year, venue:** Jiang, Wang, Liang, Wang, 2026. ICML 2026.
- **Tier:** T1. Verified via the OpenReview venue field "ICML 2026 regular".
- **Link:** https://arxiv.org/abs/2602.16901
- **What it measures / how success is decided:**
  - 5 long-horizon attack types, 28 environments, 644 cases.
  - Setup: "GPT-5.1 (temperature 0.5) as the planner; Qwen-3-14B-Abliterated ... as the attacker; and GPT-5.1 with greedy decoding (temperature 0) as the internal judge to ensure deterministic and consistent evaluation".
  - Metrics: "ASR reports the fraction of cases where the malicious objectives are fully achieved; and Turn to Success (T2S)" (§5.1).
  - Scenarios were validated so that "attack success can be evaluated programmatically" (§4.3.1), yet the described evaluator is the LLM judge.
- **Key results:**
  - Table 2 overall ASR: Qwen-3 81.5, GPT-4o 78.1, GPT-5.1 69.9, Gemini-3 53.7, Claude-4.5 28.9.
  - Table 3 one-shot vs long-horizon injection: GPT-4o "62.5%" vs "79.9%"; Claude-4.5 "0.0 %" for both.
  - Fig. 7: ASR vs maximum attack turns.
- **Pitfalls it exposes:**
  - The judge is shared between attack refinement and evaluation (N7).
  - I found no judge–human agreement study in the text (Inference from a full-text search for "agreement" and "human").
  - T2S is conditioned on success.
  - Main-session observations: (i) Intent Hijacking in the public repo (commit 36f58e6) uses a tool-less chat victim scored by a GPT-5.1 text judge (score ≥ 4/5), and the attacker's TextGrad loss optimises against that same judge. (ii) Stored task-injection results reproduce the paper's ASRs as success within up to 10 attempts (GPT-4o 32.6% at 1 attempt vs 79.9%).
- **Verification:** PRIMARY-READ (§4–5, App. A).
- **Inference:** The closest benchmark to the thesis. Re-score its released traces with a state oracle and a held-out judge before quoting its numbers. Report ASR@1 alongside ASR within *k* attempts.

### E-07 · CAR-bench — CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty
- **Authors, year, venue:** Kirmayr, Stappen, André, 2026. ACL 2026 (long).
- **Tier:** T1. Verified via the ACL Anthology page 2026.acl-long.1886.
- **Link:** https://aclanthology.org/2026.acl-long.1886/
- **What it measures / how success is decided:**
  - In-car assistant with 58 tools and 19 policies: "Policy compliance is verified automatically for 12 rules via code-based checks and for 7 via LLM-as-a-Judge ... where programmatic validation is infeasible" (§3.1).
  - "A task is considered solved only if all relevant metrics equal 1" (§3.3).
  - Pass^k and Pass@k follow τ-bench.
- **Key results:**
  - Frontier thinking models drop from "68% Pass@3 to 36% Pass^3" (§1).
  - No model exceeds 50% Pass^3 on Disambiguation.
  - User-simulator audit over k = 5 GPT-5 trials: Base "12 user errors (2.4%), 6 sole-source (–6% Pass^5)"; Hallucination −9%; Disambiguation −8% (§4).
- **Pitfalls it exposes:** N15 (inconsistency between runs), N16 (simulator error). The LLM-judged policies have no reported human validation (Inference: none found in a full-text search).
- **Main-session observation:** published clean trajectories show 12–34% of tasks flip between identical clean trials for frontier models.
- **Verification:** PRIMARY-READ (§3–4).
- **Inference:** The natural vehicle environment for the thesis. Its 12 code-checked policies are ready-made state oracles. The 7 LLM-judged ones need the M2 correction.

### E-08 · τ-bench — τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
- **Authors, year, venue:** Yao, Shinn, Razavi, Narasimhan (Sierra), 2024. ICLR 2025 (poster).
- **Tier:** T1. Verified via the OpenReview venue field "ICLR 2025 Poster".
- **Link:** https://arxiv.org/abs/2406.12045
- **What it measures / how success is decided:** "compares the database state at the end of a conversation with the annotated goal state". Introduces pass^k (abstract).
- **Key results:** "pass^8 <25% in retail" (abstract).
- **Pitfalls it exposes:** Empty responses are counted as successful in some tasks (reported by E-09). Final-state comparison misses transient states (M5).
- **Verification:** ABSTRACT-ONLY. The venue was later checked: the OpenReview venue field reads "ICLR 2025 Poster", so the tier is **T1**.

### E-09 · ABC — Establishing Best Practices for Building Rigorous Agentic Benchmarks
- **Authors, year, venue:** Zhu, Jin et al. (25 authors), 2025. NeurIPS 2025 Datasets and Benchmarks Track (poster). The OpenReview title is "Establishing Best Practices in Building Rigorous Agentic Benchmarks".
- **Tier:** T1. Verified via the OpenReview venue field.
- **Link:** https://arxiv.org/abs/2507.02825
- **What it measures:** The Agentic Benchmark Checklist (ABC) for task validity and outcome validity.
- **Key results:** "TAU-bench counts empty responses as successful". Such issues "can lead to under- or overestimation of agents' performance by up to 100% in relative terms". On CVE-Bench, applying ABC "reduces the performance overestimation by 33%" (abstract).
- **Pitfalls it exposes:** N3.
- **Verification:** ABSTRACT-ONLY.
- **Inference:** Run ABC on the thesis's own vehicle benchmark and include the checklist in an appendix.

### E-12 · Detector re-evaluation — Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents
- **Author, year:** Zhuowen Liu, 2026 (arXiv, 2 October 2026).
- **Tier:** T3. arXiv only.
- **Link:** https://arxiv.org/abs/2610.03448
- **What it measures / how success is decided:** Replays the ground-truth tool calls of AgentDojo and τ-bench without an LLM, so that tool outputs are "benign by construction". Labels injected outputs "by differential replay". Evaluates 15 detectors and 2 LLM judges at TPR@1%FPR.
- **Key results:**
  - PIGuard catches "95.1% of BIPIA injections at 1% FPR and 2.1% of AgentDojo injections".
  - Prismor catches "72.2% of AgentDojo injections and 15.2% of τ-bench's".
  - "Between BIPIA and AgentDojo Kendall's τ is 0.01" (§1, §5.2).
  - FPRs on benign tool outputs "range from none to over 90%" (abstract).
- **Pitfalls it exposes:** N18, N19. Detector scores do not transfer across benchmarks.
- **Verification:** PRIMARY-READ (§1, §5, Table 1).
- **Inference:** Differential replay is the detector-side analogue of M1. Reuse it to label which tool outputs carry the injection.

### E-13 · OpenAI deployment simulation — Predicting LLM Safety Before Release by Simulating Deployment
- **Authors, year:** Williams, Sheahan et al. (OpenAI), 2026 (arXiv, 8 July 2026).
- **Tier:** T3 (official lab research).
- **Link:** https://arxiv.org/abs/2607.07184
- **What it measures:** Regenerates the next response of real de-identified conversations with a candidate model to estimate misbehaviour prevalence before release.
- **Key results:** Traditional evaluations "are generally recognizable as tests". Simulation's "evaluation-awareness point estimates were also much closer to production traffic than those from traditional evaluations". "realism of tool resampling" is "a central challenge" (abstract).
- **Pitfalls it exposes:** N17.
- **Note on the OpenAI blog post:** alignment.openai.com ("Sidestepping Evaluation Awareness ... with Production Evaluations") could not be fetched from this environment because the host is blocked by the proxy. Its numbers are UNVERIFIED and are not used here.
- **Verification:** ABSTRACT-ONLY.

### E-14 · R-Judge — R-Judge: Benchmarking Safety Risk Awareness for LLM Agents
- **Authors, year, venue:** Yuan, He et al., 2024. Findings of EMNLP 2024.
- **Tier:** T1 (Findings). Verified via the ACL Anthology page 2024.findings-emnlp.79.
- **Link:** https://aclanthology.org/2024.findings-emnlp.79/
- **What it measures:** Whether LLMs can judge safety risk from 569 multi-turn agent records with human labels. F1 is the main score.
- **Key results:**
  - Abstract: "GPT-4o, achieves 74.42% while no other models significantly exceed the random". The introduction gives "F1 score of 74.45%", a small internal inconsistency.
  - Random baseline F1 51.32 (Table 2).
- **Pitfalls it exposes:** Judging agent risk is hard even without adversarial pressure.
- **Verification:** PRIMARY-READ (abstract, §1, §4 table).

### E-15 · AgentAuditor / ASSEBench — AgentAuditor: Human-Level Safety and Security Evaluation for LLM Agents
- **Authors, year, venue:** Luo, Dai et al., 2025. NeurIPS 2025 (poster).
- **Tier:** T1. Verified via the OpenReview venue field "NeurIPS 2025 poster" and the PDF footer.
- **Link:** https://arxiv.org/abs/2506.00641
- **What it measures:** A memory-augmented retrieval (RAG) judge. ASSEBench has 2,293 records, with "Strict" and "Lenient" label variants for ambiguous cases.
- **Key results:**
  - "up to 96.3% F1 and 96.1% accuracy on R-Judge" (§1).
  - "approaches or surpasses the average performance of a single human annotator (i.e., Acc of 95.7%, 99.3%, and 94.3%)" (§5, Obs. 2).
- **Pitfalls it exposes:** Ambiguity is real: Strict and Lenient labels differ. "Human-level" is measured on in-distribution benchmarks, not under the attack-induced shift of E-16.
- **Verification:** PRIMARY-READ (§1, §4–5).

### E-16 · A Coin Flip for Safety — A Coin Flip for Safety: LLM Judges Fail to Reliably Measure Adversarial Robustness
- **Authors, year, venue:** Schwinn, Ladenburger et al. (TU Munich, Mila), 2026. ICML 2026.
- **Tier:** T1. Verified via the OpenReview venue field "ICML 2026 regular".
- **Link:** https://arxiv.org/abs/2603.06594
- **What it measures:** Audits safety judges with "6642 human-verified labels" across victim models, attacks and harm categories. The number is 6642, not 6,442.
- **Key results:**
  - Judge performance degrades "to near random chance".
  - JailJudge AUROC reaches "a minimum of 0.48 (GCG-R)" (§4.1).
  - "many attacks inflate their success rates by exploiting judge insufficiencies" (abstract).
  - "Once corrected for precision, many attacks prove far less effective" (§4.3).
  - Keeping the 41 most judgeable behaviours "improves accuracy to 70% from 53%" (Fig. 9).
  - Agreement between judges "does not reliably imply correctness" (§4.4).
- **Pitfalls it exposes:** N6, N7. Ensembles are "insufficient to mitigate failures".
- **Verification:** PRIMARY-READ (§1, §4).
- **Inference:** The strongest argument for M2 with stratification. A judge validated on one victim or attack cannot be reused on another without recalibration.

### E-17 · Know Thy Judge — Know Thy Judge: On the Robustness Meta-Evaluation of LLM Safety Judges
- **Authors, year, venue:** Eiras, Zemour, Lin, Mugunthan, 2025. ICLR 2025 ICBINB Workshop.
- **Tier:** T2. Verified via the OpenReview venue field.
- **Link:** https://arxiv.org/abs/2503.04474
- **Key results:**
  - Style change leads "to jumps of up to 0.24 in the false negative rate".
  - Adversarial output modifications "fool some judges into misclassifying 100% of harmful generations as safe" (abstract).
  - Storytelling style raises FNR by 0.24, 0.20 and 0.12 for the HarmBench, ShieldGemma and WildGuard judges (§4).
- **Pitfalls it exposes:** N8, N20. "low attack success under certain judges could create a false sense of security".
- **Verification:** PRIMARY-READ (§3–4).

### E-18 · Policy Invariance — Are LLM Safety Judges Policy-Invariant? A Three-Principle Stress-Test
- **Authors, year, venue:** Weng, Feng, Xie, 2026. NeurIPS 2026, Evaluations and Datasets Track (spotlight).
- **Tier:** T1-claimed. The venue rests on the arXiv v2 comment ("Accepted to NeurIPS 2026 (Spotlight)") and the PDF footer. The OpenReview search did not return the record.
- **Link:** https://arxiv.org/abs/2605.06161
- **What it measures:** Agent-class judges on ASSEBench and R-Judge trajectories. Tests rubric-semantics invariance, rubric-threshold invariance and ambiguity calibration. The estimand is ∆flip = P_flip − P_jitter.
- **Key results:**
  - "Content-preserving policy rewrites flip up to 9.1% of verdicts above baseline jitter, and 18-43% of all observed flips occur on unambiguous cases" (abstract).
  - Jitter at temperature 0: DeepSeek-V3.2 5.0%. GPT-5.4-mini "high baseline jitter (6.8%)" (§4).
- **Pitfalls it exposes:** N15, N20. Temperature 0 is not deterministic. Proposes the Judge Card.
- **Verification:** PRIMARY-READ (§3–4).
- **Inference:** Include a Judge Card (rubric paraphrases, jitter, per-stratum confusion matrix) in the thesis appendix.

### E-19 · ASPI — ASPI: Seeking Ambiguity Clarification Amplifies Prompt Injection Vulnerability in LLM Agents
- **Authors, year, venue:** Sehwag, Shan et al. (Scale AI), 2026. ICML 2026 workshops (FAGEN poster; AIWILD).
- **Tier:** T2. Verified via OpenReview venue fields.
- **Link:** https://arxiv.org/abs/2605.17324
- **What it measures / how success is decided:** 728 matched execution and clarification scenarios. ASR and utility "use deterministic scores". LLM judges are used only for diagnostic behaviour labels (§6, App. F).
- **Key results:**
  - "attack success rises from 1.8% to 34.0% for o3" (abstract).
  - App. F.7, Table 7 (200-sample set, 3 human raters): "LLM–LLM agreement reaches a macro binary κb = 0.942, Human–LLM agreement reaches κb = 0.905, and human IRR reaches κ = 0.775".
  - Perfect κ on one field "reflects the near-zero attack success rates in that condition".
- **Pitfalls it exposes:** κ depends on prevalence. Judge–human agreement can exceed agreement among humans.
- **Verification:** PRIMARY-READ (abstract, App. F.7).
- **Inference:** Relevant to M6, because clarification dialogues with the driver are an attack surface.

### E-20 · Automating Deception — Automating Deception: Scalable Multi-Turn LLM Jailbreaks
- **Authors, year, venue:** Kumarappan, Mujoo, 2025. NeurIPS 2025 Workshop "Multi-Turn Interactions".
- **Tier:** T2-claimed. Verified only via the PDF footer.
- **Link:** https://arxiv.org/abs/2511.19517
- **How success is decided:** Gemini 1.5 Flash judge, "rule-based rubric". The appendix lists "Judge Input Truncation: 2000 characters" and max tokens 8.
- **Key results:** "98.0% agreement (Cohen's κ = 0.82), high precision (0.89), high recall (0.94)" (§3.3). ASR rises by up to 32 percentage points with history (abstract).
- **Pitfalls it exposes:** High raw agreement with lower κ, which is a prevalence effect. Truncating judge input can hide late harmful content.
- **Verification:** PRIMARY-READ (§3.3, App. B).
- **Inference:** With precision 0.89, about 11% of judge-positive successes are false positives. Report M2, not the raw ASR.

### E-21 · Your Judge Is a Confound — Your Judge Is a Confound: Evaluator and Attack Choice Distort Jailbreak-Safety Measurement for Fine-Tuned LLMs
- **Authors, year, venue:** Tamsal, Rusert, 2026. NeurIPS 2026 JUDGe Workshop (oral).
- **Tier:** T2. Verified via the OpenReview venue field.
- **Link:** https://openreview.net/forum?id=IsMm0VavVP
- **Key results:**
  - "Evaluator choice inflates measured black-box Delta ASR roughly threefold".
  - "GPT-4o-mini runs at a 45.7% false-positive rate ... versus 8.6% for a fine-tuned classifier".
  - "test-retest relabeling of 3-15% of identical completions".
  - LoRA "protection" is seed-variable: "mean -30.0, SD 24.1 pp over three seeds" (abstract).
- **Pitfalls it exposes:** N6, N15. The judge is a first-class experimental factor.
- **Verification:** ABSTRACT-ONLY (OpenReview abstract).

### E-22 · Audit the Difference — Audit the Difference, Not the Score: Detecting Safety Regressions in Localized LLMs Despite Unreliable Judges
- **Author, year, venue:** Agrahari, 2026. KDD 2026 SeT-LLM Workshop (poster).
- **Tier:** T2. Verified via the OpenReview venue field.
- **Link:** https://openreview.net/forum?id=ud8sKdplQQ
- **Key results:**
  - Absolute harmful-compliance rate "swings by up to 0.17 across equally-defensible judges".
  - Judges "agree on only 43% of the safety-relevant harmful class". Guard vs committee κ = 0.13.
  - "Yet the paired ΔHCR ... is robust: all four judges agree on the sign of every resolvable effect", with paired McNemar tests (abstract).
- **Pitfalls it exposes:** Absolute rates are fragile, while paired differences are robust to the instrument.
- **Verification:** ABSTRACT-ONLY.
- **Inference:** Direct support for making paired *differences* (M1) the primary estimand.

### E-23 · Measuring the Measurer — Measuring the Measurer: Reliability of LLM Judge Scoring in Petri
- **Authors, year, venue:** Kassler, Ahlqvist, Rivera, Hughes, 2026. NeurIPS 2026 JUDGe Workshop (oral).
- **Tier:** T2. Verified via the OpenReview venue field.
- **Link:** https://openreview.net/forum?id=DeTd5gGgWx
- **Key results:**
  - "Judge models disagree with each other more than with themselves (per-judge ratios 1.8–10.9×, median 2.8×) and the disagreement persists at temperature 0".
  - Per-dimension scoring detects "69.3% vs 62.3%" of planted behaviours, "but at a higher false-positive rate (28.9% vs 18.7%)" (abstract).
- **Verification:** ABSTRACT-ONLY.

### E-24 · Agreement is not a judge property — Agreement With Humans Is Not a Property of the Judge
- **Author, year, venue:** Narayanan, 2026. NeurIPS 2026 JUDGe Workshop (poster).
- **Tier:** T2. Verified via the OpenReview venue field.
- **Link:** https://openreview.net/forum?id=QmrmObszBY
- **Key results:** On SummEval, one judge correlates "0.43 - 0.61 with the expert panel and only 0.03 - 0.07 with the crowd panel, on identical items" (abstract).
- **Pitfalls it exposes:** N20. An agreement figure must name its reference panel.
- **Verification:** ABSTRACT-ONLY.

### E-25 · Lee et al. — How to Correctly Report LLM-as-a-Judge Evaluations
- **Authors, year, venue:** Chungpa Lee, Zeng, Jeong, Sohn, Kangwook Lee, 2025 (v4 May 2026). ICML 2026.
- **Tier:** T1. Verified via the OpenReview venue field "ICML 2026 regular" and the arXiv journal-ref.
- **Link:** https://arxiv.org/abs/2511.21140
- **Method:**
  - Bias-corrected estimator, eq. (5): θ̂ = (p̂ + q̂₀ − 1)/(q̂₀ + q̂₁ − 1), "(Rogan & Gladen, 1978; Lang & Reiczigel, 2014)".
  - The CI, eq. (6)–(8), adds test-set and calibration-set variance using adjusted counts ("add two successes and two failures").
  - Adaptive allocation of calibration labels between the two classes.
- **Key results:**
  - E[p̂] = (q₀ + q₁ − 1)·θ + (1 − q₀), eq. (9), so the naive score is biased unless q₀ = q₁ = 1.
  - With q̂₀ = 0.7, q̂₁ = 0.9 and p̂ = 0.3, "achieving an interval shorter than 0.1 requires m ≈ 200 calibration examples" (§4.2).
  - The estimator "remains unbiased" when the true-label distribution shifts. It assumes Pr(Ẑ|Z) is the same in calibration and test, and App. A relaxes this to covariates ξ (§8).
- **Verification:** PRIMARY-READ (§4–5, §8).
- **Inference:** Robustness to label shift is exactly what ASR estimation needs, because the true ASR differs by defence. Covariate shift (E-16) is not covered unless you stratify, hence M2.

### E-26 · Chen et al. — Efficient Inference for Noisy LLM-as-a-Judge Evaluation
- **Authors, year:** Yiqun T. Chen, Lu et al., 2026 (arXiv).
- **Tier:** T3.
- **Link:** https://arxiv.org/abs/2601.05420
- **Key results:**
  - Unifies Rogan–Gladen and prediction-powered inference via efficient influence functions.
  - "both methods outperform the Rogan–Gladen estimator in terms of finite-sample bias and the efficiency of their confidence intervals". "the asymptotic variance of the PPI estimator is strictly smaller than that of the Rogan–Gladen estimator" (§1).
  - Robustness to covariate and label shift is left as future work (§7).
- **Verification:** PRIMARY-READ (§1–2, §7).
- **Code:** github.com/yiqunchen/debias-llm-as-a-judge

### E-27 · Catching One in Five — Catching One in Five: LLM-as-Judge Blind Spots in Production Multi-Turn Transaction Agents
- **Authors, year:** Zhang, Wang, Lei, 2026 (arXiv).
- **Tier:** T3.
- **Link:** https://arxiv.org/abs/2606.10315
- **Key results:**
  - The judge surfaces "2 of 9 patterns (22%)". Its gate "flagged zero of 100 rounds in a batch where humans confirmed 23 distinct defects".
  - It "catches turn-local issues ... but misses cross-turn state issues".
  - "when the apparent defect rate is zero the Rogan-Gladen correction degenerates" (abstract).
- **Pitfalls it exposes:** Judges miss errors that only appear across turns. These are exactly the long-horizon attacks.
- **Verification:** ABSTRACT-ONLY.

### E-28 · Rogan & Gladen — Estimating prevalence from the results of a screening test
- **Authors, year, venue:** W. J. Rogan, B. Gladen, 1978. American Journal of Epidemiology 107(1):71–76.
- **Tier:** T2 (journal).
- **Verification:** UNVERIFIED primary. The bibliographic data come from the references of E-26 ("Walter J Rogan and Beth Gladen. Estimating prevalence from the results of a screening test. American Journal of Epidemiology, 107(1):71–76, 1978."). The formula is as restated in E-25 and E-26.
- **Companion:** Lang & Reiczigel (2014), "Confidence limits for prevalence of disease adjusted for estimated sensitivity and specificity", *Preventive Veterinary Medicine* 113(1):13–22. Also from E-25's references; also UNVERIFIED primary.

### E-29 · Base-rate fallacy — The base-rate fallacy and the difficulty of intrusion detection
- **Author, year, venue:** S. Axelsson, 2000. ACM TISSEC 3(3):186–205, DOI 10.1145/357830.357849.
- **Tier:** T1/T2 (journal).
- **Verification:** ABSTRACT-ONLY, via a search-engine summary. The ACM DL was not opened.
- **Claim:** The false-alarm rate, not detection rate, is "the limiting factor" for intrusion detection.
- **Inference:** At 1% attack prevalence, a detector with TPR 0.8 and FPR 0.01 has PPV = 0.008/(0.008 + 0.0099) ≈ 0.45. So more than half of its alarms are false.

### E-34 · TypeSafe / JEV vendor sources (launch post, docs, changelog, naming post)
- **Author, year:** TypeSafe AI (founder Diogo Almeida), 2026.
- **Tier:** T4 (vendor).
- **Links:**
  - https://typesafe.ai/blog/introducing-system-one-models-and-jev (15 Sep 2026)
  - https://docs.typesafe.ai/model-jaggedness
  - https://docs.typesafe.ai/changelog
  - https://typesafe.ai/blog/dont-call-it-a-decision-model (3 Nov 2026, Allie Laabs)
- **What it is:** "Our first public model is Jev ... a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out".
  - Training method: "Reinforcement Learning for Calibrated Decisions (RLCD)".
  - Name: "We named Jev after William Stanley Jevons". JEV is not an acronym.
- **Key claims (vendor, not independently verified):**
  - "two orders of magnitude faster and more efficient". "can't hallucinate", in the sense of type safety. Input tokens "$0.042 / MTok".
  - FAQ: "We deliberately chose *not* to publish performance against *public* benchmarks". "Jev is neither small nor an LLM". "We make all the data ourselves".
  - Use cases include "Score, judge, verify, guardrail, and detect jailbreaks".
- **Vendor-admitted limits (jaggedness page, 9 failure modes):**
  - #6: "State is data, and Jev does not treat it as hostile by default. Content written to adversarially steer the model, whether that is an injected instruction, a deliberately misleading framing, or text that argues for its own classification, can move the answer."
  - #8 choice-order bias.
  - #5 "context rot".
- **Version:** Jev 1.14 released "October 14, 2026" (changelog). All academic studies below test 1.13.
- **Verification:** PRIMARY-READ (pages fetched and read).

### E-35 · JEV-as-a-Judge (CMU) — JEV-as-a-Judge: Accept When Confident, Escalate When Unsure
- **Authors, year:** Yubo Li, Miao, Krishnan, Padman (CMU), 2026 (v6, 29 Oct 2026).
- **Tier:** T3. arXiv only.
- **Link:** https://arxiv.org/abs/2609.26550
- **What it measures:** JEV 1.13 against 16 judges on preference, factuality, final answers and selection, with 183 blinded human adjudications. Proposes a confidence-routed cascade to GPT-6.
- **Key results (Table 2, operating envelope, JEV vs comparator):**
  - RewardBench 92.5 vs 92.5 (0.0).
  - JudgeBench 78.6 vs 93.1 (−14.6 [−18.9, −10.3]).
  - RM-Bench hard "style-adversarial" 76.6 vs 90.1 (−13.5).
  - Reference-free prose 53.5 vs 56.0, "Not supported".
  - Abstract: "0.36% of its fee and a 0.15-second median latency". The cascade is "0.9 points more accurate than GPT-6 on 1,610 held-out pairs at 41% of its fee".
  - On reference-free prose, confidence AUROC "is 0.498, and no threshold helps".
- **Pitfalls it exposes:**
  - Limitations: "Whether its decisions and confidence are as useful inside an agent ... is not tested here".
  - "we cannot rule out that benchmark items were seen in training".
  - "Confident errors, including those on style-adversarial pairs, argue against using any automated judge as the sole arbiter of consequential decisions."
- **Verification:** PRIMARY-READ (Table 2, §7–8, Limitations). Appendix A (open alternatives) was not re-read here.

### E-36 · Decision models vs LLM rubric judges (UPenn) — Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places
- **Authors, year:** Rao, Callison-Burch, 2026 (v3, 13 Oct 2026).
- **Tier:** T3.
- **Link:** https://arxiv.org/abs/2609.29769
- **Key results:**
  - LLM judges "cost 16 to 357 times as much and take 5 to 350 times as long". Each decision model "trails them significantly in at most 6 of 27 comparisons" (abstract).
  - On Jev's most confident errors, "242 of the 252 LLM verdicts on these 84 pairs (96.0%) repeat its answer, against 50.3% expected" (§6.1).
  - Cascades "gained a mere 2.7 points at best over the strongest single judge, even with oracle thresholds" (abstract).
  - Jev's confidence AUROC for correctness is "0.57 to 0.70" on ordinal panels and 0.49 on ELLIPSE (§6.1).
- **Pitfalls it exposes:** Errors are correlated across judge families, so neither majority votes nor cascades fix them.
- **Verification:** PRIMARY-READ (abstract, §6, Limitations).

### E-37 · DecisionRobust — DecisionRobust: Benchmarking Robustness for JEV Style Decision Models Across Text and Vision
- **Authors, year:** Lan, Liu et al., 2026 (arXiv, 13 Oct 2026).
- **Tier:** T3.
- **Link:** https://arxiv.org/abs/2610.19118
- **What it measures / how success is decided:** Perturbation and prompt-injection attacks on 30 text and 17 vision model configurations. "For label-consistent ASR, the successful candidate must pass the label check; the denominator is unchanged". Two external LLMs must recover the reference answer on the perturbed input (§2.3.3, §3.1).
- **Key results:**
  - Table 3 (all datasets, 1,332 samples), Jev sample-level combined perturbation ASR "69.7" raw vs "36.6" checked. On the Arm subset it is 79.4 vs 2.9.
  - Table 4: Jev prompt-injection flip/target ASR combined over templates and locations "54.4/49.6". OpenJEV "86.3/82.5".
  - "Target ASR is always below flip ASR, so a wrong decision need not match the attacker target" (§3.2.2).
- **Pitfalls it exposes:** N9. The difference between a flip and a targeted success.
- **Verification:** PRIMARY-READ (§2–3, Tables 3–4).
- **Inference:** About half of JEV's perturbation "failures" were label changes. The same check is needed for any perturbation-style attack on vehicle commands.

### E-40 · JEV on agent traces — JEV as a Judge for Agent Trace Security: An Empirical Comparison with Generative LLM Judges
- **Authors, year:** Zhiqiang Wang, Yichao Gao (USTC), 2026 (arXiv, 28 Sep 2026).
- **Tier:** T3.
- **Link:** https://arxiv.org/abs/2609.34862
- **What it measures / how success is decided:**
  - 5,219 trajectories from R-Judge, ATBench500, a TraceSafe subset and MCPHunt. Risk score 1–5, positive if s ≥ 3.
  - "TraceSafe and MCPHunt use the study's revised labels, which distinguish resisted injections and signal-only cases from unsafe behavior" (§4.1).
- **Key results:**
  - Table 2: JEV mean F1 77.8 (P 77.1, R 79.2, accuracy 82.8, coverage 95.5%). GLM-5.2 mean F1 74.1 (P 91.9, R 64.1, accuracy 86.5, coverage 94.4%).
  - "exploratory paired-bootstrap 95% interval of [0.5, 4.8]" for JEV's 2.7-point advantage on common samples (§5.1).
  - Per dataset (Table 3): R-Judge JEV 88.5 vs GLM 93.4; TraceSafe 67.8 vs 72.4; ATBench500 93.8 vs 85.9; MCPHunt 61.1 vs 44.9.
  - Median latency 0.99 s; "$0.000195 per valid result" (Table 4).
- **Pitfalls it exposes:**
  - JEV wins on F1 but loses on precision and accuracy.
  - The labels were revised by the authors.
  - Single threshold.
  - No attack *on the judge* was tested.
  - Limitations: "Future studies could use independently reviewed labels".
- **Verification:** PRIMARY-READ (full text).
- **Inference:** Supports JEV only as a *screening* signal on traces, not as the ground-truth ASR judge.

### E-41 · Datadog counterfeit policy — Jev as a judge: How counterfeit policy steers Jev
- **Authors, year:** Nick Frichette, Feras Al-Kassar (Datadog Security Labs), 15 Oct 2026.
- **Tier:** T4 (industry security research blog).
- **Link:** https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/
- **What it measures:** JEV as a prompt-injection classifier on four public datasets. A prepended "counterfeit policy" rewrites the label taxonomy inside the untrusted content. Also tests LangChain's tool-risk gating (block if is_risky ≥ 0.5).
- **Key results:**
  - Baseline "99.66% precision" and recall 82.90% (F1 90.51%).
  - With the counterfeit policy, "true positives plummeted from 3,849 to 180", giving recall 3.88% and F1 7.46%.
  - Gating scenario over 40 runs: mean is_risky "dropped from 0.893 to 0.290". A plain prompt-injection payload averaged "0.905, slightly above the baseline".
- **Pitfalls it exposes:** N8. Attacks crafted to fool the judge in its own decision format succeed where generic injections fail.
- **Verification:** PRIMARY-READ.
- **Inference:** A JEV-based judge or guard in the thesis must be red-teamed with policy-shaped payloads, not only generic injections.

### E-42 · LangChain posts on Jev
- **Authors, year:** Sydney Runkle, Hunter Lovell (LangChain), 17 Sep 2026; second post 25 Sep 2026.
- **Tier:** T4.
- **Links:**
  - https://www.langchain.com/blog/building-a-harness-with-jev
  - https://www.langchain.com/blog/building-prod-with-jev-and-langgraph
- **Content:** `AutoModeMiddleware` "uses Jev to check tool calls for risky decisions it may take, and block calls before the tool executes" (17 Sep).
  - The 25 Sep post claims: "In an early Jev-as-a-judge experiment, its scores barely moved across 100 repeated runs, far less than any LLM judge we tested". No data is given.
- **Verification:** PRIMARY-READ (pages). The consistency claim itself is unsupported marketing; do not cite it as evidence.

---

## 5. JEV verdict (draft)

**(a) What "JEV" most likely refers to.**
- Most likely: **Jev, TypeSafe AI's "System One" decision model**, released in early access on 15 Sep 2026 (E-34).
- Confidence: **high (~90%)**. Every 2026 paper that writes "JEV" in an evaluation or judge context means this model (E-35, E-36, E-37, E-40, E-41).
- The name is not an acronym. It comes from William Stanley Jevons (E-34).
- An alternative-meaning search (for example JEPA, "joint embedding") is still pending and will be added below.

**(b) Established vs vendor claims.**
- *Established by independent studies, all on jev-1.13.0:*
  - Near GPT-6 accuracy on read-off judgments at a fraction of the cost and latency (E-35, E-36).
  - Clearly behind where a verdict must be *derived* (JudgeBench −14.6) and on style-adversarial pairs (−13.5) (E-35).
  - Its errors overlap with LLM judges' errors (E-36).
  - On agent traces it is a reasonable screener (mean F1 77.8, but lower precision) (E-40).
  - It is steerable by adversarial content, which the vendor itself documents (E-34). Recall 82.90% → 3.88% under a counterfeit policy (E-41). Label-checked perturbation ASR is 36.6% (E-37).
- *Vendor-only:* "can't hallucinate" (true only in the type-safety sense), calibration claims, workflow-eval speed-ups, architecture claims. There are no public-benchmark numbers by design (E-34).

**(c) Use in the thesis.**
- *Use it* as (i) a cheap *screening* or second judge on traces, calibrated against a human or oracle subset with M2; and (ii) an *attack target*, as a guard whose robustness is itself measured with judge-targeted payloads (E-41).
- *Do not use it* as the sole ground-truth ASR judge. Do not use it without pinning the version (1.13 vs 1.14). Do not claim it is robust or calibrated under attack. Do not judge whole long traces with it without filtering, because the vendor documents context rot (E-34).

---

## 6. Registry rows (draft; extended below as entries are added)

```csv
id,short_name,title,authors_first,year,venue,tier,verification,url,used_for,notes
E-01,Firewalls/benchmark flaws,"Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?",Bhagwatkar,2025,NeurIPS 2025 Lock-LLM Workshop (poster),T2,PRIMARY-READ,https://arxiv.org/abs/2510.05244,"benchmark artifacts N1-N3","ASB 73.58->9.25 Table 5; text says 70%"
E-02,WASP,"WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks",Evtimov,2025,NeurIPS 2025 Datasets & Benchmarks,T1,PRIMARY-READ,https://arxiv.org/abs/2504.18575,"partial vs end-to-end ASR; N4","ASR-intermediate judged by GPT-4o"
E-03,AgentDojo,"AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents",Debenedetti,2024,NeurIPS 2024 Datasets & Benchmarks,T1,PRIMARY-READ,https://arxiv.org/abs/2406.13352,"state oracles; BU/UA/ASR","rejects LLM evaluator to avoid evaluator hijack"
E-04,InjecAgent,"InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents",Zhan,2024,Findings of ACL 2024,T1,PRIMARY-READ,https://aclanthology.org/2024.findings-acl.624/,"ASR-valid; simulated tools; N12/N14",
E-05,AgentHarm,"AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents",Andriushchenko,2024,ICLR 2025,T1,PRIMARY-READ,https://arxiv.org/abs/2410.09024,"rubric + narrow LLM checks; harm score/refusal",
E-06,AgentLAB,"AgentLAB: Benchmarking LLM Agents against Long-Horizon Attacks",Jiang,2026,ICML 2026,T1,PRIMARY-READ,https://arxiv.org/abs/2602.16901,"long-horizon ASR; T2S; turn budget","GPT-5.1 judge temp 0 shared with attack loop; ASR within N attempts (main-session obs.)"
E-07,CAR-bench,"CAR-bench: Evaluating the Consistency and Limit-Awareness of LLM Agents under Real-World Uncertainty",Kirmayr,2026,ACL 2026 (long),T1,PRIMARY-READ,https://aclanthology.org/2026.acl-long.1886/,"in-car env; 12 code + 7 LLM policies; Pass^k","user-simulator errors -6..-9% Pass^5"
E-08,tau-bench,"tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains",Yao,2024,arXiv (venue not yet verified),T3,ABSTRACT-ONLY,https://arxiv.org/abs/2406.12045,"pass^k; final-state oracle",
E-09,ABC checklist,"Establishing Best Practices for Building Rigorous Agentic Benchmarks",Zhu,2025,NeurIPS 2025 Datasets & Benchmarks,T1,ABSTRACT-ONLY,https://arxiv.org/abs/2507.02825,"benchmark validity checklist; N3",
E-12,Detector re-eval,"Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents",Liu,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.03448,"TPR@1%FPR; differential replay; N18/N19",
E-13,Deployment simulation,"Predicting LLM Safety Before Release by Simulating Deployment",Williams,2026,arXiv (OpenAI),T3,ABSTRACT-ONLY,https://arxiv.org/abs/2607.07184,"eval-vs-production gap; N17","alignment.openai.com post not reachable -> UNVERIFIED"
E-14,R-Judge,"R-Judge: Benchmarking Safety Risk Awareness for LLM Agents",Yuan,2024,Findings of EMNLP 2024,T1,PRIMARY-READ,https://aclanthology.org/2024.findings-emnlp.79/,"judge benchmark on agent records","74.42 (abstract) vs 74.45 (intro)"
E-15,AgentAuditor,"AgentAuditor: Human-Level Safety and Security Evaluation for LLM Agents",Luo,2025,NeurIPS 2025,T1,PRIMARY-READ,https://arxiv.org/abs/2506.00641,"judge method; ASSEBench strict/lenient",
E-16,Coin Flip,"A Coin Flip for Safety: LLM Judges Fail to Reliably Measure Adversarial Robustness",Schwinn,2026,ICML 2026,T1,PRIMARY-READ,https://arxiv.org/abs/2603.06594,"judge failure under shift; precision-corrected ASR","6642 labels (not 6,442)"
E-17,Know Thy Judge,"Know Thy Judge: On the Robustness Meta-Evaluation of LLM Safety Judges",Eiras,2025,ICLR 2025 ICBINB Workshop,T2,PRIMARY-READ,https://arxiv.org/abs/2503.04474,"judge style/adversarial robustness",
E-18,Policy Invariance,"Are LLM Safety Judges Policy-Invariant? A Three-Principle Stress-Test",Weng,2026,NeurIPS 2026 E&D Track (claimed),T1-claimed,PRIMARY-READ,https://arxiv.org/abs/2605.06161,"rubric invariance; jitter; Judge Card","venue from arXiv comment + footer only"
E-19,ASPI,"ASPI: Seeking Ambiguity Clarification Amplifies Prompt Injection Vulnerability in LLM Agents",Sehwag,2026,ICML 2026 Workshops (FAGEN; AIWILD),T2,PRIMARY-READ,https://arxiv.org/abs/2605.17324,"judge-human kappa; clarification state",
E-20,Automating Deception,"Automating Deception: Scalable Multi-Turn LLM Jailbreaks",Kumarappan,2025,NeurIPS 2025 Workshop Multi-Turn Interactions (claimed),T2-claimed,PRIMARY-READ,https://arxiv.org/abs/2511.19517,"judge agreement 98%/kappa 0.82","judge input truncated at 2000 chars"
E-21,Your Judge Is a Confound,"Your Judge Is a Confound: Evaluator and Attack Choice Distort Jailbreak-Safety Measurement for Fine-Tuned LLMs",Tamsal,2026,NeurIPS 2026 JUDGe Workshop (oral),T2,ABSTRACT-ONLY,https://openreview.net/forum?id=IsMm0VavVP,"judge FPR; test-retest; seed variance",
E-22,Audit the Difference,"Audit the Difference, Not the Score: Detecting Safety Regressions in Localized LLMs Despite Unreliable Judges",Agrahari,2026,KDD 2026 SeT-LLM Workshop,T2,ABSTRACT-ONLY,https://openreview.net/forum?id=ud8sKdplQQ,"paired differences robust to judge; McNemar",
E-23,Measuring the Measurer,"Measuring the Measurer: Reliability of LLM Judge Scoring in Petri",Kassler,2026,NeurIPS 2026 JUDGe Workshop (oral),T2,ABSTRACT-ONLY,https://openreview.net/forum?id=DeTd5gGgWx,"inter- vs intra-judge disagreement",
E-24,Agreement not judge property,"Agreement With Humans Is Not a Property of the Judge",Narayanan,2026,NeurIPS 2026 JUDGe Workshop (poster),T2,ABSTRACT-ONLY,https://openreview.net/forum?id=QmrmObszBY,"reference-panel dependence of agreement",
E-25,Correct judge reporting,"How to Correctly Report LLM-as-a-Judge Evaluations",Lee,2025,ICML 2026,T1,PRIMARY-READ,https://arxiv.org/abs/2511.21140,"Rogan-Gladen estimator + CI for judges",
E-26,Noisy-judge inference,"Efficient Inference for Noisy LLM-as-a-Judge Evaluation",Chen,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2601.05420,"RG vs PPI vs EIF",
E-27,Catching One in Five,"Catching One in Five: LLM-as-Judge Blind Spots in Production Multi-Turn Transaction Agents",Zhang,2026,arXiv,T3,ABSTRACT-ONLY,https://arxiv.org/abs/2606.10315,"judge misses cross-turn defects; RG degeneracy",
E-28,Rogan-Gladen,"Estimating prevalence from the results of a screening test",Rogan,1978,American Journal of Epidemiology 107(1):71-76,T2,UNVERIFIED,,"misclassification-corrected prevalence","bibliographic data from E-26 references"
E-29,Base-rate fallacy,"The base-rate fallacy and the difficulty of intrusion detection",Axelsson,2000,ACM TISSEC 3(3):186-205,T2,ABSTRACT-ONLY,https://doi.org/10.1145/357830.357849,"detector PPV at low prevalence",
E-34,TypeSafe/Jev docs,"Introducing System One Models & Jev; Model jaggedness; Changelog; Don't Call It a Decision Model",TypeSafe AI (Almeida),2026,vendor blog/docs,T4,PRIMARY-READ,https://typesafe.ai/blog/introducing-system-one-models-and-jev,"what JEV is; vendor-admitted adversarial limits","no public benchmarks by design"
E-35,JEV-as-a-Judge (CMU),"JEV-as-a-Judge: Accept When Confident, Escalate When Unsure",Li,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2609.26550,"JEV judge envelope; cascade","agentic use not tested (Limitations)"
E-36,Decision vs LLM rubric judges,"Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places",Rao,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2609.29769,"correlated judge errors; cascade limits",
E-37,DecisionRobust,"DecisionRobust: Benchmarking Robustness for JEV Style Decision Models Across Text and Vision",Lan,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2610.19118,"label-consistent ASR; JEV robustness","Jev raw 69.7 vs checked 36.6"
E-40,JEV on agent traces,"JEV as a Judge for Agent Trace Security: An Empirical Comparison with Generative LLM Judges",Wang,2026,arXiv,T3,PRIMARY-READ,https://arxiv.org/abs/2609.34862,"JEV as trace screener","F1 77.8 vs 74.1; revised labels"
E-41,Datadog counterfeit policy,"Jev as a judge: How counterfeit policy steers Jev",Frichette,2026,Datadog Security Labs blog,T4,PRIMARY-READ,https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/,"attack on judge/guard","recall 82.90->3.88%"
E-42,LangChain Jev posts,"Building a Harness with Jev; Building Prod with Jev and LangGraph",Runkle,2026,LangChain blog,T4,PRIMARY-READ,https://www.langchain.com/blog/building-a-harness-with-jev,"AutoModeMiddleware tool-risk gating","consistency claim unsupported"
```
