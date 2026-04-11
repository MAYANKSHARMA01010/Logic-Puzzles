from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class Domain(str, Enum):
    finance = "finance"
    energy = "energy"
    operations = "operations"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Operation(str, Enum):
    impute = "impute"
    flag_anomaly = "flag_anomaly"
    accept = "accept"
    repair_and_finalize = "repair_and_finalize"
    escalate = "escalate"


class ForecastAuditObservation(BaseModel):
    task_id: str
    difficulty: str
    domain: Domain
    metric_name: str
    timestamps: List[str]
    values: List[Optional[float]]
    issue_type: str = Field(description="missing_value, anomaly, or invalid_forecast")
    constraints: List[str]
    analyst_note: str
    step_count: int
    max_steps: int
    history_summary: str


class ForecastAuditAction(BaseModel):
    operation: Operation
    target_index: Optional[int] = None
    predicted_value: Optional[float] = None
    severity: Optional[Severity] = None
    violated_constraints: List[str] = Field(default_factory=list)
    rationale: str = Field(default="")

    @field_validator("rationale")
    @classmethod
    def validate_rationale(cls, value: str) -> str:
        return value.strip()


class RewardModel(BaseModel):
    score: float = Field(gt=0.0, lt=1.0)
    components: Dict[str, float]
    message: str


class ForecastAuditState(BaseModel):
    task_id: str
    difficulty: str
    current_observation: ForecastAuditObservation
    done: bool
    step_count: int
    max_steps: int
    cumulative_score: float
    expected_action: Dict[str, object]
    reward_history: List[RewardModel]