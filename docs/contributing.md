# 🤝 Contributing Guide

Guidelines for contributing to Forecast Audit OpenEnv.

## Welcome Contributors! 👋

We welcome contributions from everyone! Whether you're fixing bugs, adding features, improving docs, or creating new tasks.

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/MAYANKSHARMA01010/Forecast-Audit
cd Forecast-Audit
```

### 2. Create a Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-bug
```

**Branch naming:**
- `feature/` - New feature
- `fix/` - Bug fix
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Tests

### 3. Make Changes

Edit files and test locally.

### 4. Commit

```bash
git add .
git commit -m "Clear, descriptive message"
```

**Commit message format:**
```
type: description

Optional longer explanation
```

Examples:
```
feat: add custom task support
fix: resolve port binding issue
docs: update API reference
test: add unit tests for grading
refactor: simplify reward calculation
```

### 5. Push & Create PR

```bash
git push origin feature/my-feature
```

Then on GitHub:
- Click "Compare & pull request"
- Fill in PR description
- Submit!

---

## 📝 Types of Contributions

### 🐛 Bug Reports

Found a bug? Open an issue:

**Template:**
```markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: macOS/Linux/Windows
- Python: 3.11/3.12
- How running: Local/Docker

## Error Message
(if applicable)
```

### ✨ New Features

Want to add a feature?

**Discussion:**
1. Open issue describing feature
2. Wait for feedback
3. Get approval before coding

**Implementation:**
1. Fork and create branch
2. Add feature with tests
3. Update documentation
4. Submit PR

### 📚 Documentation

Spotted a typo or want to improve docs?

1. Fork repository
2. Edit `.md` files in `docs/`
3. Submit PR

### ➕ New Tasks

Want to add a training task?

**Template:**
```python
TaskSpec(
    task_id="domain_type_###",           # domain_finance_001, etc
    difficulty="easy|medium|hard",
    domain=Domain.finance,              # finance, energy, operations
    metric_name="human_readable_name",
    timestamps=[...],
    values=[...],
    issue_type="missing_value|anomaly|invalid_forecast",
    constraints=[...],
    analyst_note="context",
    expected_operation=Operation.,
    expected_index=...,
    expected_value=...,
    value_tolerance=0.01,
    max_steps=10,
    history_summary="description"
)
```

See: [Task Format](./task-format.md)

---

## 💾 Code Style

### Python Style

We follow **PEP 8**:

```bash
# Format code
black server/ models.py client.py

# Check style
flake8 server/ models.py client.py

# Type check
mypy server/ models.py client.py
```

### Key Rules

- ✅ Type hints on all functions
- ✅ Docstrings for functions/classes
- ✅ 80 character line limit
- ✅ 2 blank lines between classes
- ✅ Snake_case for variables/functions

### Example

```python
def calculate_reward(action: ForecastAuditAction, expected: TaskSpec) -> float:
    """
    Calculate reward score for an action.
    
    Args:
        action: Agent's action
        expected: Expected solution
        
    Returns:
        Reward score (0.0-1.0)
    """
    components = []
    
    # Check operation correctness
    if action.operation == expected.expected_operation:
        components.append(1.0)
    else:
        components.append(0.0)
    
    return sum(components) / len(components)
```

---

## ✅ Testing

### Run Local Tests

```bash
python validate.py
python inference.py
```

### Add Tests

Create `test_*.py`:

```python
def test_reset():
    """Test reset functionality"""
    env = ForecastAuditEnvironment()
    obs = env.reset(task_id="easy_ops_missing_001")
    assert obs.task_id == "easy_ops_missing_001"
    assert not obs.done

def test_step():
    """Test step functionality"""
    env = ForecastAuditEnvironment()
    env.reset(task_id="easy_ops_missing_001")
    
    action = ForecastAuditAction(
        operation=Operation.impute,
        target_index=3,
        predicted_value=135.0,
        severity=Severity.low,
        violated_constraints=[],
        rationale="Test"
    )
    
    obs, reward, done, info = env.step(action)
    assert reward.score > 0.9
    assert done
```

### Run Tests

```bash
pytest test_*.py -v
```

---

## 📋 PR Checklist

Before submitting PR:

- [ ] Code follows style guide
- [ ] Added tests for changes
- [ ] All tests pass
- [ ] Updated documentation
- [ ] Commit messages are clear
- [ ] No breaking changes (or documented)
- [ ] Works locally
- [ ] Works with Docker

---

## 🔍 Code Review Process

1. **Automated Checks**
   - Linting ✓
   - Type checking ✓
   - Tests ✓

2. **Human Review**
   - Code quality
   - Design decisions
   - Documentation

3. **Approval**
   - Need 1 approval for small changes
   - Need 2 approvals for large changes

4. **Merge**
   - "Squash and merge" for cleaner history

---

## 🎯 Contribution Ideas

### Beginner-Friendly

- [ ] Fix typos in documentation
- [ ] Add code examples
- [ ] Improve error messages
- [ ] Add docstrings

### Intermediate

- [ ] Add new task types
- [ ] Improve test coverage
- [ ] Optimize performance
- [ ] Add logging

### Advanced

- [ ] Refactor reward system
- [ ] Add new deployment targets
- [ ] Build integration examples
- [ ] Create CLI tools

---

## 🚫 What NOT to Do

- ❌ Don't commit debugging code
- ❌ Don't modify .gitignore unnecessarily
- ❌ Don't add large binary files
- ❌ Don't remove tests
- ❌ Don't force push to main
- ❌ Don't mix unrelated changes

---

## 📞 Need Help?

- **Questions?** Open discussion
- **Confused?** Ask in PR comments
- **Found issue?** Tag maintainers
- **Want to pair code?** Schedule meeting

---

## 🎉 Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md`
- Release notes
- GitHub contributors graph

Thank you for contributing! 🙏

---

**Happy Contributing!**
