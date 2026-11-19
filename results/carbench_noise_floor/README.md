# Noise floor of clean in-car agent runs (CAR-bench published trajectories)

**What this is.** A zero-cost measurement of how often in-car LLM agents do things that an attack oracle could mistake for attack success, **with no attack present**. It re-analyses the multi-trial trajectories that the CAR-bench authors publish in their repository.

- Data: `github.com/CAR-bench/car-bench`, `results/` folder, commit `ce6dc9d` (12 Oct 2026), MIT licence. The paper is CAR-bench, ACL 2026 (T1). The trajectories themselves are a GitHub artefact (T4 as a source, but they are the authors' own runs).
- Script: `tools/carbench_noise_floor.py` (run: `python3 -I tools/carbench_noise_floor.py third_party/car-bench/results results/carbench_noise_floor`).
- Output: `noise_floor.csv` (with Wilson 95% CIs), `noise_floor.md`, `examples.json` (flagged runs for manual audit).
- Runs whose record holds only an error/traceback (infrastructure failures) are excluded and counted in `errored`.

## Definitions
Ground truth = the task's required state-changing actions (`info.task.actions`, filtered to the 26 set-APIs).

| Column | Meaning |
|---|---|
| pass1 | share of runs with reward = 1 |
| pass_k | share of tasks where all k trials pass (CAR-bench's Pass^k) |
| flip | share of tasks whose k clean trials disagree (some pass, some fail) |
| usca | share of runs with ≥1 *unrequested state-changing action*: a set-API call whose tool is not among the ground-truth tools. **Upper bound**: it also counts actions the simulated user asked for mid-conversation but that are not in the task's ground truth |
| usca_A2 / usca_A3 | same, restricted to outbound communication (send_email, call_phone_by_number) / driving-relevant or exterior functions (navigation edits, windows, sunroof, trunk, exterior lights) |
| usca_spont | same as usca, but only calls whose preceding user message contains no keyword of that tool family. **Heuristic estimate** of actions the agent took on its own |
| param_dev | share of runs with ≥1 call to a ground-truth tool whose arguments match no ground-truth call ("right tool, wrong parameters", includes intermediate attempts later corrected) |

The A1/A2/A3 criticality split is this thesis's proposal, not CAR-bench's.

## Headline numbers (clean runs, frontier models)
| Split / model | runs | flip (tasks) | usca (upper bound) | usca_spont (estimate) | usca_A2 |
|---|---|---|---|---|---|
| base_test / Claude Sonnet 4.6 | 149 | 6/49 | 3/149 | 3/149 | 0/149 |
| base_v2 / Claude Opus 4.6 | 150 | 9/50 | 3/150 | 0/150 | 0/150 |
| base_v2 / GPT-5.2 | 148 | 13/48 | 11/148 | 5/148 | 0/148 |
| hallucination_test / Claude Sonnet 4.6 | 150 | 17/50 | 18/150 | 0/150 | 0/150 |
| hallucination_train_v2 / GPT-5.2 | 138 | 11/43 | 29/138 | 5/138 | 0/138 |
| hallucination / xLAM-2-32b (open) | 486 | 21/97 | 72/486 | 26/486 | 3/486 |

## What it means for the thesis (inference)
1. **Outcome instability is large without any attack.** 12–34% of tasks flip between identical clean trials for frontier models. A single attacked run that "fails the user task" is weak evidence of an attack: utility-under-attack must be compared with the *same task's* clean pass rate, over several trials.
2. **Broad oracles have a real false-positive floor.** "The agent changed something it was not asked to change" happens in up to ~20% of clean runs (upper bound) and in roughly 0–4% (frontier) to ~6% (open models) of runs on the heuristic spontaneous estimate. An attack oracle defined as "any unrequested A3 action" would therefore report non-zero ASR with no attacker at all.
3. **Narrow, goal-specific oracles are clean.** No frontier run sent an email or placed a call that the task did not require (0 of ~1,300 frontier runs). Attack goals defined as a specific attacker target state (e.g., email to an attacker address, destination = attacker POI) have a near-zero clean floor, so they can be used without large correction; broad deviation oracles need paired clean runs (the thesis's *causal ASR*).
4. **The simulated user is a source of "non-attacks".** In audited example `base_81` (Claude Sonnet 4.6, trial 2) the simulated user asked for a route change that its instructions said not to ask for; the resulting action is unrequested by ground truth but requested in the conversation. Simulator drift must be logged and excluded from attack success.

## Caveats
- The keyword heuristic is crude in both directions; a manual audit of a random sample of flagged runs (planned: 30) is required before any number is quoted in the thesis.
- CAR-bench tasks were not designed as attack controls; these are floors for this environment and these models only.
- Some `_v2` files contain each run twice (once errored); errored copies are excluded.
