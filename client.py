from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


@dataclass
class ClientStepResult:
    observation: Dict[str, Any]
    reward: Dict[str, Any]
    done: bool
    info: Dict[str, Any]


class ForecastAuditClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.AsyncClient] = None

    @classmethod
    async def from_url(cls, base_url: str) -> "ForecastAuditClient":
        instance = cls(base_url)
        await instance._connect()
        return instance

    async def _connect(self) -> None:
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def reset(self, task_id: Optional[str] = None, difficulty: Optional[str] = None) -> Dict[str, Any]:
        assert self._client is not None, "Client not connected."
        payload: Dict[str, Any] = {}
        if task_id:
            payload["task_id"] = task_id
        if difficulty:
            payload["difficulty"] = difficulty
        response = await self._client.post("/reset", json=payload)
        response.raise_for_status()
        return response.json()

    async def step(self, action: Dict[str, Any]) -> ClientStepResult:
        assert self._client is not None, "Client not connected."
        response = await self._client.post("/step", json=action)
        response.raise_for_status()
        payload = response.json()
        return ClientStepResult(
            observation=payload["observation"],
            reward=payload["reward"],
            done=payload["done"],
            info=payload["info"],
        )

    async def state(self) -> Dict[str, Any]:
        assert self._client is not None, "Client not connected."
        response = await self._client.get("/state")
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()


def run(coro):
    return asyncio.run(coro)