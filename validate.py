#!/usr/bin/env python3
from __future__ import annotations

import json

from models import ForecastAuditAction, Operation, Severity
from server.environment import ForecastAuditEnvironment, TASK_ORDER


def assert_reset_and_state() -> None:
    env = ForecastAuditEnvironment()
    obs = env.reset(task_id=TASK_ORDER[0])
    assert obs.task_id == TASK_ORDER[0]
    state = env.state()
    assert state.task_id == TASK_ORDER[0]
    assert state.done is False
    print("✓ reset() and state() are consistent")


def assert_reward_range() -> None:
    env = ForecastAuditEnvironment()
    for task_id in TASK_ORDER:
        env.reset(task_id=task_id)
        action = ForecastAuditAction(
            operation=Operation.accept,
            rationale="Testing penalty path.",
        )
        _, reward, _, _ = env.step(action)
        assert 0.0 <= reward.score <= 1.0
    print("✓ reward range stays within [0.0, 1.0]")


def assert_deterministic_grading() -> None:
    env1 = ForecastAuditEnvironment()
    env2 = ForecastAuditEnvironment()
    task_id = TASK_ORDER[1]
    action = ForecastAuditAction(
        operation=Operation.repair_and_finalize,
        target_index=3,
        predicted_value=105.0,
        severity=Severity.high,
        violated_constraints=["Historical daily P&L usually changes by less than 5k day-to-day."],
        rationale="Thursday is anomalous relative to the stable series, so repair the point.",
    )
    env1.reset(task_id=task_id)
    env2.reset(task_id=task_id)
    _, reward1, _, _ = env1.step(action)
    _, reward2, _, _ = env2.step(action)
    assert reward1.score == reward2.score
    print("✓ grading is deterministic")


def assert_hard_task_is_multi_step_capable() -> None:
    env = ForecastAuditEnvironment()
    obs = env.reset(task_id=TASK_ORDER[2])
    assert obs.max_steps == 3
    print("✓ hard task allows multi-step interaction")


if __name__ == "__main__":
    assert_reset_and_state()
    assert_reward_range()
    assert_deterministic_grading()
    assert_hard_task_is_multi_step_capable()
    print("\nAll local validation checks passed.")