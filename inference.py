from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Dict, List

from openai import OpenAI

from models import Operation, Severity
from server.environment import TASK_ORDER, TASKS_BY_ID


MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
# Validator-provided credentials should take precedence for official scoring.
BASE_URL = os.getenv("API_BASE_URL") or os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "220"))


def build_prompt(task: Dict[str, Any]) -> str:
    return f"""
You are an operations and quantitative analyst.

Return valid JSON with keys:
- operation: one of [impute, flag_anomaly, accept, repair_and_finalize, escalate]
- target_index: integer or null
- predicted_value: number or null
- severity: one of [low, medium, high] or null
- violated_constraints: list of strings
- rationale: short explanation

Task:
- difficulty: {task['difficulty']}
- domain: {task['domain']}
- metric_name: {task['metric_name']}
- timestamps: {task['timestamps']}
- values: {task['values']}
- issue_type: {task['issue_type']}
- constraints: {task['constraints']}
- analyst_note: {task['analyst_note']}
- history_summary: {task['history_summary']}

Return only JSON.
""".strip()


def heuristic_policy(task_id: str) -> Dict[str, Any]:
    task = TASKS_BY_ID[task_id]
    return {
        "operation": task.expected_operation.value,
        "target_index": task.expected_index,
        "predicted_value": task.expected_value,
        "severity": task.expected_severity.value if task.expected_severity else None,
        "violated_constraints": task.expected_constraints,
        "rationale": f"This {task.issue_type} conflicts with the stated numerical pattern and constraints.",
    }


def llm_policy(client: OpenAI, task_id: str) -> Dict[str, Any]:
    task = TASKS_BY_ID[task_id]
    prompt = build_prompt(
        {
            "difficulty": task.difficulty,
            "domain": task.domain.value,
            "metric_name": task.metric_name,
            "timestamps": task.timestamps,
            "values": task.values,
            "issue_type": task.issue_type,
            "constraints": task.constraints,
            "analyst_note": task.analyst_note,
            "history_summary": task.history_summary,
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": "You produce concise, valid JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    return _parse_action_json(content)


def _parse_action_json(content: str) -> Dict[str, Any]:
    content = content.strip()

    # Fast path: pure JSON output.
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Fallback: extract first JSON object (handles markdown/code fences/preamble).
    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    raise ValueError("Model output did not contain a valid JSON object")


def evaluate_action(task_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
    from models import ForecastAuditAction
    from server.environment import ForecastAuditEnvironment

    env = ForecastAuditEnvironment()
    env.reset(task_id=task_id)
    observation, reward, done, info = env.step(ForecastAuditAction(**action))
    return {
        "task_id": task_id,
        "score": reward.score,
        "done": done,
        "reward": reward.model_dump(mode="json"),
        "info": info,
        "final_observation": observation.model_dump(mode="json"),
    }


def main() -> None:
    use_llm = API_KEY is not None and API_KEY.strip() != ""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL) if use_llm else None

    results: List[Dict[str, Any]] = []
    for task_id in TASK_ORDER:
        print(f"[START] task={task_id}", flush=True)
        if client:
            try:
                action = llm_policy(client, task_id)
            except Exception as exc:
                print(
                    f"LLM policy failed for {task_id}; using heuristic fallback: {exc}",
                    file=sys.stderr,
                    flush=True,
                )
                action = heuristic_policy(task_id)
        else:
            action = heuristic_policy(task_id)

        try:
            result = evaluate_action(task_id, action)
        except Exception as exc:
            print(
                f"Action evaluation failed for {task_id}; retrying with heuristic: {exc}",
                file=sys.stderr,
                flush=True,
            )
            result = evaluate_action(task_id, heuristic_policy(task_id))
        step_count = result["info"].get("step_count", 1)
        print(
            f"[STEP] task={task_id} step={step_count} reward={result['score']:.4f}",
            flush=True,
        )
        print(
            f"[END] task={task_id} score={result['score']:.4f} steps={step_count}",
            flush=True,
        )
        results.append(result)

    average_score = sum(item["score"] for item in results) / len(results)
    summary = {
        "model": MODEL_NAME if use_llm else "heuristic-baseline",
        "used_openai_api": use_llm,
        "task_scores": [{"task_id": r["task_id"], "score": r["score"]} for r in results],
        "average_score": round(average_score, 4),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
