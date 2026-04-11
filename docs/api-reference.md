# API Reference

Forecast-Audit exposes a small REST API for task lifecycle management.

## Base URL

```text
http://localhost:7860
```

For local, Docker, and Hugging Face URLs, see [Access URLs and Ports](./access-urls-and-ports.md).

## Authentication

No authentication is required for API routes.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Root service metadata |
| `GET` | `/health` | Health check |
| `GET` | `/metadata` | Task metadata and order |
| `GET` | `/schema` | JSON schemas for action/observation/reward/state |
| `POST` | `/reset` | Start a new task episode |
| `POST` | `/step` | Submit an action and receive reward |
| `GET` | `/state` | Current environment state |

## GET /

Returns service-level metadata.

```bash
curl http://localhost:7860/
```

Example response:

```json
{
  "name": "forecast-audit-openenv",
  "status": "running",
  "docs": "/docs",
  "health": "/health"
}
```

## GET /health

Returns service health.

```bash
curl http://localhost:7860/health
```

Example response:

```json
{
  "status": "healthy"
}
```

## GET /metadata

Returns task order and high-level environment metadata.

```bash
curl http://localhost:7860/metadata
```

## GET /schema

Returns JSON schema definitions for core data models.

```bash
curl http://localhost:7860/schema
```

## POST /reset

Starts a new task episode.

Request body:

```json
{
  "task_id": "easy_ops_missing_001",
  "difficulty": "easy"
}
```

Notes:

- `task_id` is optional.
- `difficulty` is optional and can be `easy`, `medium`, or `hard`.
- If both are omitted, the environment rotates through task order.

Example request:

```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"easy"}'
```

Example response:

```json
{
  "observation": {
    "task_id": "easy_ops_missing_001",
    "difficulty": "easy",
    "domain": "operations",
    "metric_name": "warehouse_orders_per_hour",
    "timestamps": ["09:00", "10:00", "11:00", "12:00", "13:00"],
    "values": [120.0, 125.0, 130.0, null, 140.0],
    "issue_type": "missing_value",
    "constraints": [
      "Weekday ramp is stable at +5 orders/hour.",
      "No promotions or outages were recorded."
    ],
    "analyst_note": "Backfill the missing hour before the report is published.",
    "step_count": 0,
    "max_steps": 2,
    "history_summary": "Recent weekday mornings have shown a steady linear ramp."
  },
  "done": false
}
```

## POST /step

Submits an agent action and returns updated observation plus reward.

Request body:

```json
{
  "operation": "impute",
  "target_index": 3,
  "predicted_value": 135.0,
  "severity": "low",
  "violated_constraints": [],
  "rationale": "Series follows a +5 linear trend."
}
```

Example request:

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation":"impute",
    "target_index":3,
    "predicted_value":135.0,
    "severity":"low",
    "violated_constraints":[],
    "rationale":"Series follows a +5 linear trend."
  }'
```

Example response:

```json
{
  "observation": {
    "task_id": "easy_ops_missing_001",
    "difficulty": "easy",
    "domain": "operations",
    "metric_name": "warehouse_orders_per_hour",
    "timestamps": ["09:00", "10:00", "11:00", "12:00", "13:00"],
    "values": [120.0, 125.0, 130.0, 135.0, 140.0],
    "issue_type": "missing_value",
    "constraints": [
      "Weekday ramp is stable at +5 orders/hour.",
      "No promotions or outages were recorded."
    ],
    "analyst_note": "Previous action: impute. Reward=1.00. Excellent action. The issue was handled correctly and can be finalized.",
    "step_count": 1,
    "max_steps": 2,
    "history_summary": "Recent weekday mornings have shown a steady linear ramp."
  },
  "reward": {
    "score": 1.0,
    "components": {
      "operation": 0.35,
      "index": 0.15,
      "value": 0.2,
      "severity": 0.1,
      "constraints": 0.1,
      "rationale": 0.08,
      "efficiency": 0.05,
      "penalty": 0.0
    },
    "message": "Excellent action. The issue was handled correctly and can be finalized."
  },
  "done": true,
  "info": {
    "task_id": "easy_ops_missing_001",
    "difficulty": "easy",
    "issue_type": "missing_value",
    "max_steps": 2,
    "step_count": 1,
    "expected_operation": "impute"
  }
}
```

## GET /state

Returns current environment state for the active episode.

```bash
curl http://localhost:7860/state
```

## Error Responses

| Status | Meaning |
| --- | --- |
| `400` | Invalid `task_id`, `difficulty`, or action for current state |
| `422` | Request body validation error |

Typical `400` response:

```json
{
  "detail": "Unknown task_id: invalid_task"
}
```

Typical `422` response:

```json
{
  "detail": [
    {
      "loc": ["body", "operation"],
      "msg": "Input should be 'impute', 'flag_anomaly', 'accept', 'repair_and_finalize' or 'escalate'",
      "type": "enum"
    }
  ]
}
```
