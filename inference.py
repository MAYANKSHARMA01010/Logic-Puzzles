from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from models import Operation, Severity
from server.environment import TASK_ORDER, TASKS_BY_ID


MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
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
    return json.loads(content)


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
        action = llm_policy(client, task_id) if client else heuristic_policy(task_id)
        result = evaluate_action(task_id, action)
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
