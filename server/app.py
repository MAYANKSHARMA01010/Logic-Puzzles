from __future__ import annotations

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models import ForecastAuditAction, RewardModel
from server.environment import ForecastAuditEnvironment, TASK_ORDER


app = FastAPI(
    title="Forecast Audit OpenEnv",
    version="2.0.0",
    description="A mathematically-oriented environment for forecast validation, anomaly handling, and numerical repair.",
)

env = ForecastAuditEnvironment()


class ResetRequest(BaseModel):
    task_id: Optional[str] = None
    difficulty: Optional[str] = None


@app.get("/")
def root() -> dict:
    return {
        "name": "forecast-audit-openenv",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}


@app.get("/metadata")
def metadata() -> dict:
    return {
        "name": "forecast-audit-openenv",
        "task_order": TASK_ORDER,
        "description": "Real-world numerical QA and forecast auditing environment.",
        "reward_range": [0.0, 1.0],
    }


@app.get("/schema")
def schema() -> dict:
    from models import ForecastAuditObservation, ForecastAuditState

    return {
        "action": ForecastAuditAction.model_json_schema(),
        "observation": ForecastAuditObservation.model_json_schema(),
        "reward": RewardModel.model_json_schema(),
        "state": ForecastAuditState.model_json_schema(),
    }


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()) -> JSONResponse:
    try:
        observation = env.reset(task_id=req.task_id, difficulty=req.difficulty)
        return JSONResponse(
            content={
                "observation": observation.model_dump(mode="json"),
                "done": False,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/step")
def step(action: ForecastAuditAction) -> JSONResponse:
    try:
        observation, reward, done, info = env.step(action)
        return JSONResponse(
            content={
                "observation": observation.model_dump(mode="json"),
                "reward": reward.model_dump(mode="json"),
                "done": done,
                "info": info,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/state")
def state() -> JSONResponse:
    try:
        return JSONResponse(content=env.state().model_dump(mode="json"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def main(host: str = "0.0.0.0", port: int = 7860) -> None:
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()