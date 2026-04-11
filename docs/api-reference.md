# 📡 API Reference

Complete documentation of all REST API endpoints.

## Base URL

```
http://localhost:7860
```

## Authentication

No authentication required (can be added if needed).

---

## Endpoints Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API root info |
| GET | `/health` | Health check |
| GET | `/metadata` | Task metadata |
| GET | `/schema` | Data schemas |
| POST | `/reset` | Initialize task |
| POST | `/step` | Execute action |
| GET | `/state` | Current state |

---

## ✅ Detailed Endpoint Documentation

### 1. GET / (Root)

Returns basic API information.

**Request:**
```bash
curl http://localhost:7860/
```

**Response (200 OK):**
```json
{
  "name": "forecast-audit-openenv",
  "status": "running",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. GET /health (Health Check)

Checks if server is operational.

**Request:**
```bash
curl http://localhost:7860/health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

**Use Cases:**
- Load balancer health checks
- Monitoring/uptime detection
- Readiness probes

---

### 3. GET /metadata (Task Metadata)

Returns available tasks and environment info.

**Request:**
```bash
curl http://localhost:7860/metadata
```

**Response (200 OK):**
```json
{
  "name": "forecast-audit-openenv",
  "task_order": [
    "easy_ops_missing_001",
    "medium_finance_anomaly_001",
    "hard_energy_forecast_001"
  ],
  "description": "Real-world numerical QA and forecast auditing environment.",
  "reward_range": [0.0, 1.0]
}
```

**Fields:**
- `name`: Project identifier
- `task_order`: Available task IDs
- `description`: Brief description
- `reward_range`: Min/max possible rewards

---

### 4. GET /schema (Data Schemas)

Returns JSON schemas for all data structures.

**Request:**
```bash
curl http://localhost:7860/schema
```

**Response (200 OK):**
```json
{
  "action": {...},           // ForecastAuditAction schema
  "observation": {...},      // ForecastAuditObservation schema
  "reward": {...},           // RewardModel schema
  "state": {...}             // ForecastAuditState schema
}
```

**Use Cases:**
- API client code generation
- Validation rule extraction
- Documentation generation

---

### 5. POST /reset (Initialize Task)

Initializes a new task/episode.

**Request:**
```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_ops_missing_001"}'
```

**Request Body:**
```json
{
  "task_id": "easy_ops_missing_001",    // Optional: specific task
  "difficulty": "easy"                   // Optional: easy|medium|hard
}
```

**Response (200 OK):**
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
    "max_steps": 10,
    "history_summary": "Recent weekday mornings have shown a steady linear ramp."
  },
  "done": false
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `observation` | Object | Initial task observation |
| `done` | Boolean | Task completion status |

**Errors:**

| Code | Description |
|------|-------------|
| 400 | Invalid task_id or difficulty |
| 500 | Server error |

**Example:**
```python
import requests

response = requests.post(
    'http://localhost:7860/reset',
    json={'task_id': 'medium_finance_anomaly_001'}
)
print(response.json())
```

---

### 6. POST /step (Execute Action)

Executes an agent action and returns observation + reward.

**Request:**
```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "impute",
    "target_index": 3,
    "predicted_value": 135.0,
    "severity": "low",
    "violated_constraints": [],
    "rationale": "The sequence rises by 5 each hour, so index 3 should be 135."
  }'
```

**Request Body:**
```json
{
  "operation": "impute|flag_anomaly|accept|repair_and_finalize|escalate",
  "target_index": null|integer,        // Index of problematic value
  "predicted_value": null|float,       // Repaired/imputed value
  "severity": null|"low"|"medium"|"high",
  "violated_constraints": [],          // List of violated constraint indices
  "rationale": "string"                // Explanation of action
}
```

**Response (200 OK):**
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
    "constraints": [...],
    "analyst_note": "Your imputation was correct! The pattern is +5/hour.",
    "step_count": 1,
    "max_steps": 10,
    "history_summary": "Imputed missing value at 12:00 with 135.0 (correct)."
  },
  "reward": {
    "score": 1.0,
    "breakdown": {
      "operation_correct": 1.0,
      "index_correct": 1.0,
      "value_accuracy": 1.0,
      "severity_alignment": 1.0,
      "constraints_cited": 1.0,
      "rationale_quality": 1.0
    }
  },
  "done": true,
  "info": {
    "grading_notes": "Perfect imputation! Correctly identified pattern and filled missing value."
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `observation` | Object | Updated task state |
| `reward.score` | Float | Overall reward (0.0-1.0) |
| `reward.breakdown` | Object | Reward component scores |
| `done` | Boolean | Is episode finished? |
| `info` | Object | Feedback/grading notes |

**Reward Breakdown:**
- `operation_correct`: (0 or 1) Is operation type correct?
- `index_correct`: (0 or 1) Is target index correct?
- `value_accuracy`: (0-1) How accurate is predicted value?
- `severity_alignment`: (0-1) Is severity appropriate?
- `constraints_cited`: (0-1) Are violated constraints identified?
- `rationale_quality`: (0-1) Is explanation clear?

**Operations Allowed:**

```
operation: "impute"
  → Use when: Missing value in data
  → Requires: target_index, predicted_value
  → Example: Fill in null with 135

operation: "flag_anomaly"
  → Use when: Corrupted/outlier value
  → Requires: target_index, severity
  → Example: Mark suspicious spike

operation: "accept"
  → Use when: Data is valid as-is
  → Requires: None
  → Example: No action needed

operation: "repair_and_finalize"
  → Use when: Fix AND complete
  → Requires: target_index, predicted_value, severity
  → Example: Repair and submit

operation: "escalate"
  → Use when: Needs human review
  → Requires: violated_constraints
  → Example: Pattern violation
```

**Errors:**

| Code | Description |
|------|-------------|
| 400 | Invalid action format or values |
| 422 | Validation error |
| 500 | Server error |

**Example:**
```python
import requests

action = {
    "operation": "impute",
    "target_index": 3,
    "predicted_value": 135.0,
    "severity": "low",
    "violated_constraints": [],
    "rationale": "Stable +5 pattern"
}

response = requests.post(
    'http://localhost:7860/step',
    json=action
)

result = response.json()
print(f"Reward: {result['reward']['score']}")
print(f"Done: {result['done']}")
```

---

### 7. GET /state (Current State)

Returns current environment state.

**Request:**
```bash
curl http://localhost:7860/state
```

**Response (200 OK):**
```json
{
  "task_id": "easy_ops_missing_001",
  "done": true,
  "step_count": 1,
  "observation": {
    "task_id": "easy_ops_missing_001",
    "difficulty": "easy",
    "domain": "operations",
    "metric_name": "warehouse_orders_per_hour",
    "timestamps": ["09:00", "10:00", "11:00", "12:00", "13:00"],
    "values": [120.0, 125.0, 130.0, 135.0, 140.0],
    "issue_type": "missing_value",
    "constraints": [...],
    "analyst_note": "...",
    "step_count": 1,
    "max_steps": 10,
    "history_summary": "..."
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | String | Current task ID |
| `done` | Boolean | Is task finished? |
| `step_count` | Integer | Steps taken so far |
| `observation` | Object | Task observation |

**Use Cases:**
- Query state without taking action
- Monitor episode progress
- Verify state after action

---

## 🔄 Typical Workflow

### Complete Task Flow

```
1. Reset
POST /reset
└─ Get initial observation
   
2. Analyze
(Process observation offline)

3. Step
POST /step (action)
└─ Get reward + new observation
   
4. Check Result
GET /state
└─ Verify final state
```

### Code Example

```python
import requests

BASE_URL = "http://localhost:7860"

# 1. Reset
reset_resp = requests.post(
    f"{BASE_URL}/reset",
    json={"task_id": "easy_ops_missing_001"}
)
obs = reset_resp.json()["observation"]
print(f"Task: {obs['task_id']}")
print(f"Issue: {obs['issue_type']}")
print(f"Values: {obs['values']}")

# 2. Think & prepare action
action = {
    "operation": "impute",
    "target_index": 3,
    "predicted_value": 135.0,
    "severity": "low",
    "violated_constraints": [],
    "rationale": "Pattern is +5 per hour"
}

# 3. Execute
step_resp = requests.post(
    f"{BASE_URL}/step",
    json=action
)
result = step_resp.json()
print(f"Reward: {result['reward']['score']}")
print(f"Done: {result['done']}")

# 4. Check state
state_resp = requests.get(f"{BASE_URL}/state")
final_state = state_resp.json()
print(f"Final values: {final_state['observation']['values']}")
```

---

## 🎯 Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid task_id: unknown_task"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "target_index"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📊 Rate Limiting

Currently: **No rate limiting**

Recommended for production: Add rate limiting middleware

---

## 🔗 Interactive Documentation

Visit Swagger UI for interactive testing:
```
http://localhost:7860/docs
```

---

**API Reference Complete** ✅
