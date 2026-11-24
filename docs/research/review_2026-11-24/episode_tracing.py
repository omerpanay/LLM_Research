# Minimal Langfuse instrumentation sketch for one agent episode.
# Tested against: langfuse==5.2.0 (Python SDK v5, needs Python>=3.11 and
# self-hosted Langfuse server >= v4.59.0), openai==3.58.0.
#
# Env vars: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY,
#           LANGFUSE_BASE_URL=http://langfuse.intern:3000  (self-hosted, inside VW network)
import hashlib
import json

from langfuse import get_client, propagate_attributes
from langfuse.openai import OpenAI  # drop-in: every chat.completions call -> "generation"

langfuse = get_client()
llm = OpenAI(base_url="http://vllm.intern:8000/v1", api_key="EMPTY")  # vLLM OpenAI-compatible server


def _sid(*parts: str) -> str:
    """Deterministic score id -> re-uploading the same score overwrites instead of duplicating."""
    return hashlib.sha256(":".join(parts).encode()).hexdigest()[:32]


def run_episode(ep: dict, env, max_steps: int = 10) -> str:
    # 1 episode = 1 trace; trace id derived from OUR episode_id -> 1:1 join with our JSONL
    trace_id = langfuse.create_trace_id(seed=ep["episode_id"])

    with langfuse.start_as_current_observation(
        trace_context={"trace_id": trace_id},
        as_type="agent",
        name=f"episode/{ep['arch']}",
        input={"user_task": ep["user_task"], "task_id": ep["task_id"]},
    ) as root:
        with propagate_attributes(
            session_id=ep.get("session_id"),  # multi-turn / cross-session attack campaign
            trace_name="episode",
            tags=[
                f"arch:{ep['arch']}",            # react | plan_execute | camel
                f"def:{ep['defence']}",          # D0..D5
                f"atk:{ep['attack_family']}",    # or "none" for clean runs
                "attacked" if ep["attacked"] else "clean",
            ],
            metadata={  # each value must be <= 200 chars as JSON
                "episode_id": ep["episode_id"],
                "paired_clean_id": ep.get("paired_clean_id"),
                "model": ep["model"],
                "seed": ep["seed"],
                "benchmark": ep["benchmark"],   # agentdojo | car-bench | vehicleworld
                "git_commit": ep["git_commit"],
            },
        ):
            messages = [{"role": "system", "content": ep["system_prompt"]},
                        {"role": "user", "content": ep["user_task"]}]
            msg = None
            for step in range(max_steps):
                resp = llm.chat.completions.create(   # logged automatically as a generation
                    name=f"llm-step-{step}",          # extra kwarg understood by the Langfuse wrapper
                    model=ep["model"],
                    messages=messages,
                    tools=env.tool_schemas(),
                    temperature=0,
                    seed=ep["seed"],
                )
                msg = resp.choices[0].message
                messages.append(msg.model_dump(exclude_none=True))
                if not msg.tool_calls:
                    break
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments or "{}")
                    with langfuse.start_as_current_observation(
                        as_type="tool", name=tc.function.name, input=args
                    ) as tool_obs:
                        result = env.call_tool(tc.function.name, args)
                        tool_obs.update(output=result,
                                        metadata={"injected_output": env.last_output_injected})
                    messages.append({"role": "tool", "tool_call_id": tc.id,
                                     "content": json.dumps(result)})
            # root observation input/output == trace input/output (v4/v5 semantics)
            root.update(output={"final_answer": msg.content if msg else None,
                                "n_steps": step + 1})
    return trace_id


def log_oracle_scores(trace_id: str, ep: dict, res: dict) -> None:
    """Called AFTER the episode, by our own oracle code (state diff). Langfuse only stores it."""
    e = ep["episode_id"]
    langfuse.create_score(trace_id=trace_id, name="attack_success_oracle",
                          value=1 if res["attack_success"] else 0, data_type="BOOLEAN",
                          score_id=_sid(e, "attack_success_oracle", "oracle-v1"),
                          comment=res["state_diff_summary"][:500])
    langfuse.create_score(trace_id=trace_id, name="validity_label",
                          value=res["validity_label"],  # claimed_only | artifact | legitimate_instruction | ...
                          data_type="CATEGORICAL",
                          score_id=_sid(e, "validity_label", "rules-v1"))
    langfuse.create_score(trace_id=trace_id, name="severity", value=float(res["severity"]),
                          data_type="NUMERIC", score_id=_sid(e, "severity", "v1"))
    langfuse.create_score(trace_id=trace_id, name="task_utility_under_attack",
                          value=1 if res["user_task_done"] else 0, data_type="BOOLEAN",
                          score_id=_sid(e, "tua", "oracle-v1"))
    langfuse.create_score(trace_id=trace_id, name="confirmations_requested",
                          value=float(res["n_confirmations"]), data_type="NUMERIC",
                          score_id=_sid(e, "confirmations", "v1"))
    if ep.get("session_id"):  # campaign-level outcome of a multi-turn attack
        langfuse.create_score(session_id=ep["session_id"], name="campaign_success",
                              value=1 if res["campaign_success"] else 0, data_type="BOOLEAN",
                              score_id=_sid(ep["session_id"], "campaign_success", "v1"))


# At the end of a batch job (short-lived process!):
#   langfuse.flush()
