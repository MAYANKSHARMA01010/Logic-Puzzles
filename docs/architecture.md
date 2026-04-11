# 🏗️ System Architecture

This document explains the internal structure and design of Forecast Audit OpenEnv.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Client/User                            │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Server                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /reset       (POST)  - Initialize environment      │   │
│  │  /step        (POST)  - Execute action              │   │
│  │  /state       (GET)   - Get current state           │   │
│  │  /metadata    (GET)   - Task metadata               │   │
│  │  /health      (GET)   - Health check                │   │
│  │  /schema      (GET)   - Data schemas                │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ Python Calls
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ForecastAuditEnvironment                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  - Manages task state                                │   │
│  │  - Processes actions                                 │   │
│  │  - Calculates rewards                                │   │
│  │  - Handles grading logic                             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ TASKS  │  │ MODELS │  │ REWARD │
    │ SPECS  │  │ DATA   │  │ LOGIC  │
    └────────┘  └────────┘  └────────┘
```

---

## 📁 Project Structure

### Core Files

```
forecast-audit-env/
├── server/
│   ├── app.py                    # FastAPI application & routes
│   └── environment.py            # Task manager & grading logic
│
├── models.py                     # Pydantic data models
├── client.py                     # HTTP client helper
├── inference.py                  # AI agent testing script
├── validate.py                   # Validation checks
│
└── docs/                         # Documentation
```

### Key Components

#### 1. **app.py** (FastAPI Server)
- Defines HTTP endpoints
- Handles requests/responses
- Manages CORS and middleware

```python
@app.post("/reset")      # Initialize new task
@app.post("/step")       # Execute action
@app.get("/state")       # Get current state
```

#### 2. **environment.py** (Task Engine)
- Stores task specifications
- Manages environment state
- Implements reward calculation
- Grades agent actions

```python
class ForecastAuditEnvironment:
    def reset(task_id, difficulty)  # Start new task
    def step(action)                 # Process action
    def state()                      # Get current state
    def grade_action()               # Calculate reward
```

#### 3. **models.py** (Data Structures)
- Pydantic models for type safety
- Request/response schemas
- Data validation

```python
class ForecastAuditAction          # Agent's action
class ForecastAuditObservation     # Environment observation
class RewardModel                  # Reward breakdown
class ForecastAuditState          # Environment state
```

---

## 🔄 Request/Response Flow

### Example: Complete Workflow

```
1. CLIENT REQUEST (POST /reset)
   ├─ Input: {"task_id": "easy_ops_missing_001"}
   └─ Server receives, validates

2. SERVER PROCESSES
   ├─ Create environment
   ├─ Load task specification
   ├─ Initialize state
   └─ Generate observation

3. SERVER RESPONDS
   ├─ Status: 200 OK
   ├─ Body: {
   │    "observation": {...},
   │    "done": false
   │  }
   └─ Client receives

4. CLIENT SENDS ACTION (POST /step)
   ├─ Input: {"operation": "impute", "target_index": 3, ...}
   └─ Server receives, validates

5. SERVER PROCESSES
   ├─ Execute action
   ├─ Update state
   ├─ Grade correctness
   ├─ Calculate reward
   └─ Determine if done

6. SERVER RESPONDS
   ├─ Status: 200 OK
   ├─ Body: {
   │    "observation": {...},
   │    "reward": {...},
   │    "done": true,
   │    "info": {...}
   │  }
   └─ Client receives

7. CLIENT CHECKS STATE (GET /state)
   ├─ No input needed
   └─ Server responds with current state
```

---

## 📊 Task Specification Format

Each task is defined as:

```python
@dataclass
class TaskSpec:
    task_id: str                      # Unique identifier
    difficulty: str                   # easy, medium, hard
    domain: Domain                    # finance, energy, operations
    metric_name: str                  # Description
    timestamps: List[str]             # Time points
    values: List[Optional[float]]      # Data values
    issue_type: str                   # missing_value, anomaly, etc.
    constraints: List[str]            # Business rules
    analyst_note: str                 # Context
    expected_operation: Operation     # Correct action
    expected_index: Optional[int]      # Target index
    expected_value: Optional[float]    # Correct value
    value_tolerance: float            # Accuracy threshold
```

---

## 🎯 Task Workflow

```
TASK LIFECYCLE:

┌─────────────────────────┐
│  1. RESET RECEIVED      │
│  - Create environment   │
│  - Load task spec       │
│  - Generate observation │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  2. OBSERVATION SENT    │
│  - Data with issue      │
│  - Constraints          │
│  - Context hints        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. AGENT DECIDES       │
│  - Analyzes data        │
│  - Chooses operation    │
│  - Sends action         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  4. ACTION PROCESSED    │
│  - Validate syntax      │
│  - Check logic          │
│  - Update state         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  5. GRADING             │
│  - Compare to expected  │
│  - Calculate reward     │
│  - Generate feedback    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  6. RESPONSE SENT       │
│  - New observation      │
│  - Reward score         │
│  - Done flag            │
└─────────────────────────┘
```

---

## 🏆 Reward System

### Scoring Components

```python
class RewardBreakdown:
    operation_correct: float         # Is operation right? (1.0 or 0.0)
    index_correct: float             # Is target index right? (1.0 or 0.0)
    value_accuracy: float            # How close is predicted value? (0.0-1.0)
    severity_alignment: float        # Is severity appropriate? (0.0-1.0)
    constraints_cited: float         # Are violations cited? (0.0-1.0)
    rationale_quality: float         # Is reasoning clear? (0.0-1.0)

Total Score = Average of all components (0.0 to 1.0)
```

### Example Scoring

```
Perfect Imputation:
├─ operation_correct: 1.0 ✓ (impute is correct)
├─ index_correct: 1.0 ✓ (index 3 is correct)
├─ value_accuracy: 1.0 ✓ (135.0 is perfect)
├─ severity_alignment: 1.0 ✓ (low is appropriate)
├─ constraints_cited: 1.0 ✓ (cited ramp rule)
└─ rationale_quality: 1.0 ✓ (clear explanation)

Final Score: 1.0 (Perfect!)
```

---

## 🔗 Data Flow Diagram

```
Client Application
      │
      │ JSON Request
      ▼
┌──────────────────┐
│  FastAPI Layers  │
├──────────────────┤
│ 1. Router        │ - Route to handler
│ 2. Validator     │ - Validate schema
│ 3. Handler       │ - Business logic
│ 4. Serializer    │ - Convert to JSON
└────────┬─────────┘
         │
         │ Python Objects
         ▼
┌──────────────────────────┐
│ ForecastAuditEnvironment │
├──────────────────────────┤
│ - Load task              │
│ - Execute action         │
│ - Grade response         │
│ - Calculate reward       │
└────────┬─────────────────┘
         │
         │ Updated State Objects
         ▼
┌──────────────────┐
│  Serializer      │
├──────────────────┤
│ - Convert to dict│
│ - JSON encoding  │
└────────┬─────────┘
         │
         │ JSON Response
         ▼
Client Application
```

---

## 🔐 Validation Layers

```
Request Flow:

Raw Request
    ▼
HTTP Parser
    ▼
Pydantic Validation (Type checking)
    ▼
Business Logic Validation
    ▼
Correctness Grading
    ▼
Response Serialization
    ▼
JSON Response
```

---

## 📈 Scalability Considerations

### Current Architecture
- **Single instance** per deployment
- **In-memory state** (task per request)
- **Synchronous processing**

### For Production Scale
```
Load Balancer
    ▼
┌─────────────────────────────────┐
│ Multiple Server Instances       │
├─────────────────────────────────┤
│ Instance 1 │ Instance 2 │ ... │
└──────┬──────────────┬────────────┘
       │              │
       └──────┬───────┘
              ▼
        Shared Database
        (Session State)
```

---

## 🚀 Performance Characteristics

| Operation | Time | Scaling |
|-----------|------|---------|
| Reset task | < 100ms | O(1) |
| Step action | < 50ms | O(1) |
| Grading | < 10ms | O(1) |
| State retrieval | < 10ms | O(1) |

---

## 📝 Key Design Decisions

1. **Stateful per Request**: Each request is independent
2. **Synchronous**: No async/await for simplicity
3. **In-Memory**: Fast, no database overhead
4. **Type-Safe**: Pydantic validates all data
5. **Modular**: Easy to extend with new tasks

---

**Architecture Documentation Complete** ✅
