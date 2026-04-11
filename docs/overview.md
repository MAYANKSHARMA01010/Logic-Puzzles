# 📖 Project Overview

## What is Forecast Audit OpenEnv?

**Forecast Audit OpenEnv** is a software training environment where AI agents learn to perform real-world data quality tasks.

### The Problem It Solves

In companies everywhere, analysts spend time on repetitive tasks:
- Finding missing values in time series data
- Detecting anomalies (corrupted data points)
- Validating forecasts against business rules
- Deciding whether to repair, flag, or escalate issues

This project automates training AI systems to do these jobs correctly.

---

## 🎯 Core Concept

Think of it like a **gym for AI agents**:

```
Real World                          This Project
────────────────────────────────────────────────────────
Analyst reviews data    →    Agent gets observation
Finds problems          →    Agent analyzes data
Takes action            →    Agent chooses operation
Supervisor grades work  →    System calculates reward
Learns from feedback    →    Agent improves
```

---

## 🏆 Key Features

| Feature | Description |
|---------|-------------|
| **3 Difficulty Levels** | Easy, Medium, Hard |
| **Multiple Domains** | Finance, Energy, Operations |
| **Dense Rewards** | Immediate feedback on quality |
| **Interactive API** | REST endpoints for integration |
| **Reproducible** | Deterministic grading |
| **Extensible** | Add custom tasks easily |

---

## 📊 Task Types

### Easy: Missing Value Imputation
```
Given: [120, 125, 130, NULL, 140]
Pattern: Increasing by 5 each hour
Agent Action: Impute NULL with 135
Reward: 1.0 (Perfect!)
```

### Medium: Anomaly Detection & Repair
```
Given: [100, 105, 110, 500, 115]  ← 500 is anomalous
Pattern: All others increase by ~5
Agent Action: Flag 500 as anomaly, repair to 115
Reward: 1.0 (Correct repair)
```

### Hard: Constraint-Based Validation
```
Given: Forecast violates business rule
Constraint: "Energy demand follows 10% rule"
Agent Action: Escalate for human review
Reward: 1.0 (Correct decision)
```

---

## 🎓 Action Space

Agents can take one of 5 actions:

```python
"impute"                 # Fill missing value
"flag_anomaly"          # Mark suspicious point
"accept"                # Data is fine
"repair_and_finalize"   # Fix and complete
"escalate"              # Send to human
```

Each action includes:
- Target index (which data point?)
- Predicted value (what should it be?)
- Severity level (how serious?)
- Constraints violated (which rules?)
- Rationale (why did you choose this?)

---

## 🏅 Reward System

### Grading Criteria

Actions are graded on:

| Criterion | What It Measures |
|-----------|-----------------|
| **Operation Correct** | Is the action type right? |
| **Index Accurate** | Is the target correct? |
| **Value Precision** | How close to correct value? |
| **Severity Match** | Is urgency level appropriate? |
| **Constraint Citation** | Were violations identified? |
| **Rationale Quality** | Is reasoning clear? |

### Reward Range

- **1.0** = Perfect (all criteria met)
- **0.5-0.9** = Good (most criteria met)
- **0.0-0.5** = Poor (many mistakes)
- **0.0** = Wrong (fundamentally incorrect)

---

## 📡 How It Works

### The Workflow

```
1. Initialize Task
   → Client calls POST /reset
   → Server loads task
   → Agent receives observation

2. Agent Analyzes
   → Agent studies data
   → Agent thinks about best action
   → Agent prepares response

3. Execute Action
   → Client calls POST /step
   → Agent sends action
   → Server processes & grades

4. Get Feedback
   → Server calculates reward
   → Agent learns
   → Next task or iteration
```

### Example Request/Response

**Request:**
```bash
POST /reset
{"task_id": "easy_ops_missing_001"}
```

**Response:**
```json
{
  "observation": {
    "values": [120, 125, 130, null, 140],
    "issue_type": "missing_value",
    "constraints": ["Stable +5 ramp"],
    "analyst_note": "Fill missing value"
  },
  "done": false
}
```

**Agent Action:**
```bash
POST /step
{
  "operation": "impute",
  "target_index": 3,
  "predicted_value": 135.0,
  "severity": "low",
  "violated_constraints": [],
  "rationale": "Stable +5 pattern"
}
```

**Server Response:**
```json
{
  "reward": {"score": 1.0},
  "done": true,
  "info": "Perfect imputation!"
}
```

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI (Python) |
| **Server** | Uvicorn |
| **Data Validation** | Pydantic |
| **Containerization** | Docker |
| **Config** | YAML |

---

## 📚 Real-World Applications

### Finance
- Detecting price anomalies
- Validating forecast models
- Quality checking market data

### Energy
- Grid demand forecasting
- Equipment failure detection
- Renewable energy prediction

### Operations
- Warehouse metrics
- Supply chain optimization
- Operational KPIs

---

## 🚀 Getting Started

### 3-Step Quickstart

```bash
# 1. Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run
python -m server.app

# 3. Test
curl http://localhost:7860/docs
```

### Or with Docker

```bash
docker build -t forecast-audit-openenv .
docker run -p 7860:7860 forecast-audit-openenv
```

---

## 👥 Who Should Use This?

### Researchers
- Study reward function design
- Benchmark different agents
- Publish baselines

### Developers
- Build AI agents
- Learn RL/ML concepts
- Practice API integration

### Organizations
- Train AI assistants
- Automate QA workflows
- Research AI capabilities

---

## 💡 Why This Matters

### Current State
- **Manual work**: Analysts spend hours on QA
- **Error-prone**: Humans make mistakes
- **Hard to scale**: Can't process all data

### With AI Training
- **Automation**: Agents do routine work
- **Consistency**: Deterministic grading
- **Scalability**: Process unlimited data
- **Explainability**: Clear reward signals

---

## 📊 Evaluation Metrics

The system measures agent performance via:

- **Average Score**: How well does agent do?
- **Success Rate**: % of tasks completed correctly?
- **Efficiency**: How many steps to solve?
- **Consistency**: Same agent = same results?

---

## 🔐 Features for Production

- ✅ Type-safe (Pydantic validation)
- ✅ Reproducible (deterministic grading)
- ✅ Scalable (stateless design)
- ✅ Extensible (modular task system)
- ✅ Observable (detailed logging)
- ✅ Containerized (Docker ready)

---

## 📖 Learn More

| Topic | Link |
|-------|------|
| Quick Start | [Quick Start](./quick-start.md) |
| Installation | [Installation](./installation.md) |
| API Reference | [API Reference](./api-reference.md) |
| Architecture | [Architecture](./architecture.md) |
| Troubleshooting | [Troubleshooting](./troubleshooting.md) |

---

**Ready to get started?** → [Quick Start](./quick-start.md)
