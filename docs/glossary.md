# 📚 Glossary

Technical terms and abbreviations explained.

## A

### Action
The decision an agent makes about what to do with problematic data. Examples: impute, flag anomaly, accept.

*Related: Operation*

### Anomaly
An outlier or suspicious data point that doesn't fit the pattern.

*Example: Temperature spike of 500°C in normal data*

### API
Application Programming Interface - set of rules for software to communicate.

*In this project: REST API with endpoints like /reset, /step*

---

## B

### Baseline
A simple solution to a problem, used as reference point for comparison.

*In this project: Heuristic baseline in inference.py*

### Batch
A group of tasks or samples processed together.

---

## C

### Constraint
A business rule or mathematical boundary that data should follow.

*Example: "Daily temperature change must be < 10°C"*

### Container
Lightweight package containing application + dependencies (Docker).

---

## D

### Data Quality
How accurate, complete, and consistent data is.

*Domain: Finance, Energy, Operations*

### Dense Reward
Immediate feedback on every action (not just end result).

*This project uses dense rewards for learning*

### Difficulty
Level of task complexity: easy, medium, hard.

---

## E

### Episode
One complete run of a task from reset to done.

*Similar to "game" in game playing*

### Environment
The system that presents tasks and evaluates actions.

*Our ForecastAuditEnvironment class*

---

## F

### FastAPI
Modern Python web framework for building APIs.

*Framework we use for server*

### Forecast
Predicted future values based on historical data.

*Example: Weather forecast, sales forecast*

---

## G

### Grading
Process of evaluating if an action is correct.

*Compare to expected solution, assign reward*

### Gym
Training environment for agents (like fitness gym for humans).

*This project is conceptually a "gym" for AI*

---

## H

### Health Check
API endpoint that verifies server is running.

*GET /health returns {"status": "healthy"}*

### Heuristic
Simple rule-based approach without machine learning.

*Our baseline solver uses heuristics*

---

## I

### Imputation
Filling in missing values using estimated guesses.

*Example: Missing temperature → estimate from neighbors*

### Inference
Using a trained model to make predictions.

*inference.py tests agents on tasks*

---

## J

### JSON
JavaScript Object Notation - data format for API communication.

*{"task_id": "easy_ops_missing_001", "done": false}*

---

## K

---

## L

### Learning Rate
Speed at which AI agent learns (not used here, but common ML term).

---

## M

### Metric
Measured value being tracked over time.

*Example: warehouse_orders_per_hour, stock_price_usd*

### Missing Value
Absent/null data point in a dataset.

*Example: [100, 105, NULL, 115]*

### Model
Mathematical representation of a system or trained AI.

*In this project: Pydantic models for data validation*

---

## O

### Observation
What the agent sees/learns about the task.

*Contains: values, constraints, issue type*

### OpenAPI
Standard format for describing REST APIs.

*Available at GET /openapi.json*

### Operation
What action to take: impute, flag_anomaly, accept, repair_and_finalize, escalate.

---

## P

### Pydantic
Python library for data validation using type hints.

*We use for all request/response validation*

### Production
Live, customer-facing system (not development).

---

## Q

### Quality Assurance (QA)
Testing to ensure data/systems meet quality standards.

*This project helps automate data QA*

---

## R

### Reinforcement Learning (RL)
Machine learning where agents learn by reward/punishment.

*Similar concept to this project*

### Repair
Fix problematic data (e.g., replace with correct value).

### Reward
Score indicating how well agent performed (0.0-1.0).

*1.0 = perfect, 0.0 = completely wrong*

### REST
Representational State Transfer - API design style.

*Uses HTTP methods: GET, POST, PUT, DELETE*

---

## S

### Schema
Structure/format definition for data.

*GET /schema shows all data structures*

### Server
Computer running the application.

*Our FastAPI server on port 7860*

### Severity
How serious a problem is: low, medium, high.

### State
Current status of an environment/task.

*task_id, done flag, step count, observation*

### Step
One action/decision in a task.

*POST /step = take one step*

---

## T

### Task
Training scenario with specific problem to solve.

*3 types: missing_value, anomaly, invalid_forecast*

### Threshold
Boundary value for decision making.

*Example: value_tolerance = 0.01 (1% allowed difference)*

### Time Series
Data points ordered by time.

*Examples: stock prices, temperature readings*

### Type Hints
Python syntax specifying variable types.

```python
def my_func(name: str, count: int) -> float:
```

---

## U

### Uvicorn
Python ASGI server (runs our FastAPI).

*The "U" in "Unicorn"*

---

## V

### Validation
Checking data is correct/acceptable.

*Pydantic validates all API requests*

### Value Tolerance
Allowed accuracy range when comparing numbers.

*tolerance=0.01 means within 1%*

---

## W

---

## X

---

## Y

---

## Z

---

## Acronyms

| Acronym | Full Form | Meaning |
|---------|-----------|---------|
| AI | Artificial Intelligence | Intelligent computer systems |
| API | Application Programming Interface | Communication between programs |
| ASGI | Asynchronous Server Gateway Interface | Python server standard |
| CSV | Comma-Separated Values | Data file format |
| GPU | Graphics Processing Unit | Fast computation hardware |
| HTTP | HyperText Transfer Protocol | Web protocol |
| JSON | JavaScript Object Notation | Data format |
| ML | Machine Learning | Learning from data |
| QA | Quality Assurance | Testing/validation |
| RL | Reinforcement Learning | Learning from rewards |
| REST | Representational State Transfer | API style |
| URL | Uniform Resource Locator | Web address |
| YAML | YAML Ain't Markup Language | Config file format |

---

## Related Documentation

- [API Reference](./api-reference.md) - Technical details
- [Architecture](./architecture.md) - System design
- [Task Format](./task-format.md) - Task definitions

---

**Glossary Complete** ✅

Don't see a term? [Open an issue](https://github.com/MAYANKSHARMA01010/Forecast-Audit/issues)!
