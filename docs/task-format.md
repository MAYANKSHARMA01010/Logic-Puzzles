# 📋 Task Format Specification

Complete specification for task definitions in Forecast Audit OpenEnv.

## Task Structure

Every task is defined as a `TaskSpec` dataclass:

```python
@dataclass(frozen=True)
class TaskSpec:
    # Identification
    task_id: str
    difficulty: str
    domain: Domain
    
    # Task Data
    metric_name: str
    timestamps: List[str]
    values: List[Optional[float]]
    
    # Issue Description
    issue_type: str
    constraints: List[str]
    analyst_note: str
    
    # Expected Solution
    expected_operation: Operation
    expected_index: Optional[int]
    expected_value: Optional[float]
    expected_severity: Optional[Severity]
    expected_constraints: List[str]
    
    # Evaluation
    value_tolerance: float
    max_steps: int
    history_summary: str
```

---

## Field Descriptions

### Identification Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `task_id` | str | Unique identifier | `"easy_ops_missing_001"` |
| `difficulty` | str | easy\|medium\|hard | `"easy"` |
| `domain` | Domain | finance\|energy\|operations | `Domain.operations` |

### Task Data Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `metric_name` | str | What metric? | `"warehouse_orders_per_hour"` |
| `timestamps` | List[str] | Time points | `["09:00", "10:00", "11:00"]` |
| `values` | List[Optional[float]] | Data with issue | `[120, 125, 130, None, 140]` |

### Issue Description Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `issue_type` | str | Type of problem | `"missing_value"` |
| `constraints` | List[str] | Business rules | `["Stable +5 ramp", "No outages"]` |
| `analyst_note` | str | Context/hint | `"Fill missing value"` |

### Expected Solution Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `expected_operation` | Operation | Correct action | `Operation.impute` |
| `expected_index` | Optional[int] | Target location | `3` |
| `expected_value` | Optional[float] | Correct value | `135.0` |
| `expected_severity` | Optional[Severity] | Risk level | `Severity.low` |
| `expected_constraints` | List[str] | Violated rules | `[]` |

### Evaluation Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `value_tolerance` | float | Accuracy threshold | `0.01` (1% tolerance) |
| `max_steps` | int | Step limit | `10` |
| `history_summary` | str | Context | `"Steady linear ramp"` |

---

## Issue Types

### Missing Value

```python
TaskSpec(
    issue_type="missing_value",
    values=[120, 125, 130, None, 140],  # None = missing
    expected_operation=Operation.impute,
    expected_value=135.0
)
```

### Anomaly

```python
TaskSpec(
    issue_type="anomaly",
    values=[100, 105, 110, 500, 115],  # 500 is anomalous
    expected_operation=Operation.flag_anomaly,
    expected_index=3
)
```

### Invalid Forecast

```python
TaskSpec(
    issue_type="invalid_forecast",
    constraints=["Rule violated"],
    expected_operation=Operation.escalate,
    expected_constraints=["Rule violated"]
)
```

---

## Difficulty Levels

### Easy

- **Characteristics**: Single obvious issue
- **Complexity**: Low
- **Time**: < 1 minute
- **Example**: Simple missing value with clear pattern

```python
TaskSpec(
    difficulty="easy",
    issue_type="missing_value",
    max_steps=10,
    value_tolerance=0.01
)
```

### Medium

- **Characteristics**: Subtle issue, multiple steps
- **Complexity**: Medium
- **Time**: 2-5 minutes
- **Example**: Anomaly detection with multiple options

```python
TaskSpec(
    difficulty="medium",
    issue_type="anomaly",
    max_steps=10,
    value_tolerance=0.05
)
```

### Hard

- **Characteristics**: Complex, requires reasoning
- **Complexity**: High
- **Time**: 5-10 minutes
- **Example**: Constraint validation with escalation

```python
TaskSpec(
    difficulty="hard",
    issue_type="invalid_forecast",
    max_steps=15,
    value_tolerance=0.1
)
```

---

## Domains

### Finance

```python
Domain.finance
```

Examples:
- Stock price anomalies
- Trading volume spikes
- Forecast validation

### Energy

```python
Domain.energy
```

Examples:
- Grid demand forecasting
- Equipment failure detection
- Consumption patterns

### Operations

```python
Domain.operations
```

Examples:
- Warehouse metrics
- Supply chain KPIs
- Operational efficiency

---

## Operations

### Impute

Fill missing value.

```python
Operation.impute
# Requires: target_index, predicted_value
# Optional: severity
# Example: Fill None with calculated value
```

### Flag Anomaly

Mark suspicious point.

```python
Operation.flag_anomaly
# Requires: target_index, severity
# Example: Mark extreme outlier
```

### Accept

Data is valid.

```python
Operation.accept
# Requires: Nothing
# Example: All data checks pass
```

### Repair and Finalize

Fix and complete.

```python
Operation.repair_and_finalize
# Requires: target_index, predicted_value, severity
# Example: Repair and submit final result
```

### Escalate

Send to human review.

```python
Operation.escalate
# Requires: violated_constraints
# Example: Pattern violates business rule
```

---

## Severity Levels

| Level | Meaning | When |
|-------|---------|------|
| `low` | Minor issue | Missing value |
| `medium` | Notable issue | Unexpected spike |
| `high` | Critical issue | Rule violation |

---

## Example Task: Easy

```python
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
        "No promotions or outages were recorded."
    ],
    analyst_note="Backfill the missing hour before the report.",
    
    expected_operation=Operation.impute,
    expected_index=3,
    expected_value=135.0,
    expected_severity=Severity.low,
    expected_constraints=[],
    
    value_tolerance=0.01,
    max_steps=10,
    history_summary="Recent weekday mornings show steady +5 ramp."
)
```

---

## Example Task: Medium

```python
TaskSpec(
    task_id="medium_finance_anomaly_001",
    difficulty="medium",
    domain=Domain.finance,
    
    metric_name="stock_price_usd",
    timestamps=["2024-01-01", "2024-01-02", "2024-01-03"],
    values=[150.0, 155.0, 500.0],  # 500 is anomaly
    
    issue_type="anomaly",
    constraints=[
        "Daily moves generally < 5%",
        "No major announcements on date"
    ],
    analyst_note="One spike - likely data error",
    
    expected_operation=Operation.flag_anomaly,
    expected_index=2,
    expected_value=None,
    expected_severity=Severity.high,
    expected_constraints=["Daily moves generally < 5%"],
    
    value_tolerance=None,
    max_steps=15,
    history_summary="Stable prices with one anomalous spike."
)
```

---

## Example Task: Hard

```python
TaskSpec(
    task_id="hard_energy_forecast_001",
    difficulty="hard",
    domain=Domain.energy,
    
    metric_name="grid_demand_mw",
    timestamps=["Hour1", "Hour2", "Hour3", "Hour4"],
    values=[500.0, 510.0, 520.0, 450.0],
    
    issue_type="invalid_forecast",
    constraints=[
        "Hourly demand must be within 95-105% of hourly average",
        "No sudden drops > 50MW allowed"
    ],
    analyst_note="Forecast violates demand stability rule",
    
    expected_operation=Operation.escalate,
    expected_index=None,
    expected_value=None,
    expected_severity=None,
    expected_constraints=[
        "No sudden drops > 50MW allowed"
    ],
    
    value_tolerance=None,
    max_steps=10,
    history_summary="Mostly stable with final hour violating rules."
)
```

---

## Validation Rules

### Required Fields
- `task_id` - Must be unique
- `difficulty` - Must be easy|medium|hard
- `domain` - Must be valid Domain
- `metric_name` - Non-empty string
- `timestamps` - List, length > 0
- `values` - List, same length as timestamps

### Constraints
- At least one value must have issue
- `value_tolerance` required for value-based grading
- `expected_operation` must be valid
- `max_steps > 0`

---

## Creating Custom Tasks

### Step 1: Define TaskSpec

```python
from server.environment import TaskSpec
from models import Domain, Operation, Severity

new_task = TaskSpec(
    task_id="custom_test_001",
    difficulty="easy",
    domain=Domain.finance,
    metric_name="my_metric",
    timestamps=["t1", "t2", "t3"],
    values=[1.0, None, 3.0],
    issue_type="missing_value",
    constraints=["Increases by 1 each step"],
    analyst_note="Fill the missing value",
    expected_operation=Operation.impute,
    expected_index=1,
    expected_value=2.0,
    expected_severity=Severity.low,
    expected_constraints=[],
    value_tolerance=0.01,
    max_steps=10,
    history_summary="Simple linear sequence"
)
```

### Step 2: Add to TASKS List

Edit `server/environment.py`:

```python
TASKS: List[TaskSpec] = [
    # ... existing tasks ...
    new_task,  # Add your task
]
```

### Step 3: Update TASK_ORDER

```python
TASK_ORDER = [
    "easy_ops_missing_001",
    "medium_finance_anomaly_001",
    "hard_energy_forecast_001",
    "custom_test_001",  # Add here
]
```

### Step 4: Test

```bash
python validate.py
curl http://localhost:7860/metadata  # See task listed
```

---

**Task Format Documentation Complete** ✅
