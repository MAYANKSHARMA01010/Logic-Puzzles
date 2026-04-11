from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from models import (
    Domain,
    ForecastAuditAction,
    ForecastAuditObservation,
    ForecastAuditState,
    Operation,
    RewardModel,
    Severity,
)


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    difficulty: str
    domain: Domain
    metric_name: str
    timestamps: List[str]
    values: List[Optional[float]]
    issue_type: str
    constraints: List[str]
    analyst_note: str
    history_summary: str
    max_steps: int
    expected_operation: Operation
    expected_index: Optional[int]
    expected_value: Optional[float]
    expected_severity: Optional[Severity]
    expected_constraints: List[str]
    value_tolerance: float


TASKS: List[TaskSpec] = [
    TaskSpec(
        task_id="easy_ops_missing_001",
        difficulty="easy",
        domain=Domain.operations,
        metric_name="warehouse_orders_per_hour",
        timestamps=["09:00", "10:00", "11:00", "12:00", "13:00"],
        values=[120.0, 125.0, 130.0, None, 140.0],
        issue_type="missing_value",
        constraints=[
            "Weekday ramp is stable at +5 orders/hour.",
            "No promotions or outages were recorded.",
        ],
        analyst_note="Backfill the missing hour before the report is published.",
        history_summary="Recent weekday mornings have shown a steady linear ramp.",
        max_steps=2,
        expected_operation=Operation.impute,
        expected_index=3,
        expected_value=135.0,
        expected_severity=Severity.low,
        expected_constraints=[],
        value_tolerance=0.25,
    ),
    TaskSpec(
        task_id="medium_finance_anomaly_001",
        difficulty="medium",
        domain=Domain.finance,
        metric_name="daily_strategy_pnl_usd_k",
        timestamps=["Mon", "Tue", "Wed", "Thu", "Fri"],
        values=[101.0, 103.0, 104.0, 980.0, 106.0],
        issue_type="anomaly",
        constraints=[
            "Historical daily P&L usually changes by less than 5k day-to-day.",
            "No major event, rebalance, or macro release occurred on Thu.",
        ],
        analyst_note="Decide whether Thursday should be accepted, repaired, or escalated.",
        history_summary="The desk has been running low-volatility market-neutral intraday strategies.",
        max_steps=2,
        expected_operation=Operation.repair_and_finalize,
        expected_index=3,
        expected_value=105.0,
        expected_severity=Severity.high,
        expected_constraints=["Historical daily P&L usually changes by less than 5k day-to-day."],
        value_tolerance=2.0,
    ),
    TaskSpec(
        task_id="hard_energy_forecast_001",
        difficulty="hard",
        domain=Domain.energy,
        metric_name="hourly_grid_demand_forecast_mw",
        timestamps=["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
        values=[950.0, 990.0, 1030.0, 1205.0, 1110.0, 1080.0],
        issue_type="invalid_forecast",
        constraints=[
            "Peak-hour demand should rise smoothly by about 30-50 MW/hour from 18:00 to 21:00.",
            "At 21:00, forecast demand must stay below 1100 MW because feeder maintenance limits transfer capacity.",
            "After the peak, demand should decline, not jump upward again.",
        ],
        analyst_note="Validate the forecast against physical and operational constraints.",
        history_summary="This is an evening peak forecast for a balancing area under a temporary transfer-cap limit.",
        max_steps=3,
        expected_operation=Operation.escalate,
        expected_index=3,
        expected_value=1080.0,
        expected_severity=Severity.high,
        expected_constraints=[
            "At 21:00, forecast demand must stay below 1100 MW because feeder maintenance limits transfer capacity.",
        ],
        value_tolerance=10.0,
    ),
]

TASKS_BY_ID = {task.task_id: task for task in TASKS}
TASK_ORDER = [task.task_id for task in TASKS]


class ForecastAuditEnvironment:
    """Deterministic OpenEnv-style environment for mathematical forecast auditing."""

    def __init__(self) -> None:
        self._task_index = -1
        self._task: Optional[TaskSpec] = None
        self._observation: Optional[ForecastAuditObservation] = None
        self._done = False
        self._step_count = 0
        self._cumulative_score = 0.0
        self._reward_history: List[RewardModel] = []

    def reset(self, task_id: Optional[str] = None, difficulty: Optional[str] = None) -> ForecastAuditObservation:
        if task_id is not None:
            if task_id not in TASKS_BY_ID:
                raise ValueError(f"Unknown task_id: {task_id}")
            task = TASKS_BY_ID[task_id]
        elif difficulty is not None:
            matches = [task for task in TASKS if task.difficulty == difficulty]
            if not matches:
                raise ValueError(f"Unknown difficulty: {difficulty}")
            task = matches[0]
        else:
            self._task_index = (self._task_index + 1) % len(TASKS)
            task = TASKS[self._task_index]

        self._task = task
        self._done = False
        self._step_count = 0
        self._cumulative_score = 0.0
        self._reward_history = []
        self._observation = self._build_observation(task)
        return self._observation

    def state(self) -> ForecastAuditState:
        if self._task is None or self._observation is None:
            raise RuntimeError("Environment has not been reset yet.")
        return ForecastAuditState(
            task_id=self._task.task_id,
            difficulty=self._task.difficulty,
            current_observation=self._observation,
            done=self._done,
            step_count=self._step_count,
            max_steps=self._task.max_steps,
            cumulative_score=round(self._cumulative_score, 4),
            expected_action={
                "operation": self._task.expected_operation.value,
                "target_index": self._task.expected_index,
                "predicted_value": self._task.expected_value,
                "severity": self._task.expected_severity.value if self._task.expected_severity else None,
                "violated_constraints": self._task.expected_constraints,
            },
            reward_history=self._reward_history,
        )

    def step(
        self, action: ForecastAuditAction
    ) -> Tuple[ForecastAuditObservation, RewardModel, bool, Dict[str, Any]]:
        if self._task is None or self._observation is None:
            raise RuntimeError("Call reset() before step().")
        if self._done:
            raise RuntimeError("Episode already completed. Call reset() to start a new one.")

        self._step_count += 1
        reward = self._grade_action(self._task, action, self._step_count)
        self._reward_history.append(reward)
        self._cumulative_score += reward.score

        if reward.score >= 0.95:
            self._done = True
        elif self._step_count >= self._task.max_steps:
            self._done = True

        self._observation = self._advance_observation(action, reward)
        info = {
            "task_id": self._task.task_id,
            "difficulty": self._task.difficulty,
            "issue_type": self._task.issue_type,
            "max_steps": self._task.max_steps,
            "step_count": self._step_count,
            "expected_operation": self._task.expected_operation.value,
        }
        return self._observation, reward, self._done, info

    def _build_observation(self, task: TaskSpec) -> ForecastAuditObservation:
        return ForecastAuditObservation(
            task_id=task.task_id,
            difficulty=task.difficulty,
            domain=task.domain,
            metric_name=task.metric_name,
            timestamps=copy.deepcopy(task.timestamps),
            values=copy.deepcopy(task.values),
            issue_type=task.issue_type,
            constraints=copy.deepcopy(task.constraints),
            analyst_note=task.analyst_note,
            step_count=0,
            max_steps=task.max_steps,
            history_summary=task.history_summary,
        )

    def _advance_observation(
        self, action: ForecastAuditAction, reward: RewardModel
    ) -> ForecastAuditObservation:
        assert self._task is not None
        values = copy.deepcopy(self._observation.values if self._observation else self._task.values)
        if action.target_index is not None and action.predicted_value is not None:
            if 0 <= action.target_index < len(values):
                values[action.target_index] = float(action.predicted_value)

        analyst_note = (
            f"Previous action: {action.operation.value}. "
            f"Reward={reward.score:.2f}. {reward.message}"
        )
        return ForecastAuditObservation(
            task_id=self._task.task_id,
            difficulty=self._task.difficulty,
            domain=self._task.domain,
            metric_name=self._task.metric_name,
            timestamps=copy.deepcopy(self._task.timestamps),
            values=values,
            issue_type=self._task.issue_type,
            constraints=copy.deepcopy(self._task.constraints),
            analyst_note=analyst_note,
            step_count=self._step_count,
            max_steps=self._task.max_steps,
            history_summary=self._task.history_summary,
        )

    def _grade_action(self, task: TaskSpec, action: ForecastAuditAction, step_count: int) -> RewardModel:
        components: Dict[str, float] = {
            "operation": 0.0,
            "index": 0.0,
            "value": 0.0,
            "severity": 0.0,
            "constraints": 0.0,
            "rationale": 0.0,
            "efficiency": 0.0,
            "penalty": 0.0,
        }

        if action.operation == task.expected_operation:
            components["operation"] = 0.35
        elif task.issue_type == "anomaly" and action.operation == Operation.flag_anomaly:
            components["operation"] = 0.2
        elif task.issue_type == "invalid_forecast" and action.operation == Operation.repair_and_finalize:
            components["operation"] = 0.15

        if action.target_index == task.expected_index:
            components["index"] = 0.15

        if task.expected_value is not None and action.predicted_value is not None:
            error = abs(action.predicted_value - task.expected_value)
            if error <= task.value_tolerance:
                components["value"] = 0.2
            elif error <= task.value_tolerance * 2:
                components["value"] = 0.1

        if task.expected_severity is not None and action.severity == task.expected_severity:
            components["severity"] = 0.1

        if task.expected_constraints:
            matched_constraints = set(action.violated_constraints).intersection(task.expected_constraints)
            if matched_constraints:
                components["constraints"] = min(0.1, 0.1 * len(matched_constraints) / len(task.expected_constraints))
        else:
            if not action.violated_constraints:
                components["constraints"] = 0.1

        rationale_lower = action.rationale.lower()
        if len(action.rationale.split()) >= 5:
            components["rationale"] = 0.05
        if any(keyword in rationale_lower for keyword in ["missing", "anomaly", "capacity", "linear", "trend", "repair", "escalate"]):
            components["rationale"] = max(components["rationale"], 0.08)

        components["efficiency"] = max(0.0, 0.05 - (step_count - 1) * 0.02)

        penalty = 0.0
        if action.operation == Operation.accept and task.issue_type != "missing_value":
            penalty += 0.15
        if action.operation == Operation.accept and task.issue_type == "missing_value":
            penalty += 0.25
        if action.operation == Operation.impute and action.predicted_value is None:
            penalty += 0.2
        if action.operation in (Operation.repair_and_finalize, Operation.impute) and action.target_index is None:
            penalty += 0.15
        if not action.rationale:
            penalty += 0.05
        components["penalty"] = -penalty

        raw_score = sum(value for key, value in components.items() if key != "penalty") - penalty
        final_score = max(0.0, min(1.0, round(raw_score, 4)))

        message = self._build_feedback_message(task, action, final_score)
        return RewardModel(score=final_score, components=components, message=message)

    @staticmethod
    def _build_feedback_message(task: TaskSpec, action: ForecastAuditAction, final_score: float) -> str:
        if final_score >= 0.95:
            return "Excellent action. The issue was handled correctly and can be finalized."
        if action.operation == Operation.accept:
            return "Accepting this record leaves a known issue unresolved."
        if task.issue_type == "missing_value" and action.operation != Operation.impute:
            return "This task primarily requires imputing the missing point."
        if task.issue_type == "anomaly" and action.operation not in (Operation.flag_anomaly, Operation.repair_and_finalize):
            return "The core challenge is spotting and handling the anomalous point."
        if task.issue_type == "invalid_forecast" and action.operation != Operation.escalate:
            return "This forecast violates an operational constraint and should likely be escalated."
        return "Partial progress. Tighten the operation choice, index, value, or constraints cited."
