# ❓ Frequently Asked Questions (FAQ)

## Getting Started

### Q: What is this project used for?
**A:** Forecast Audit OpenEnv is a training environment (like a gym) for AI agents to learn data quality tasks - finding missing values, anomalies, and forecast errors in time series data.

### Q: Do I need to be a data scientist to use it?
**A:** No! You just need basic Python knowledge and understanding of REST APIs. We provide simple examples.

### Q: What's the difference between local and Docker?
**A:** 
- **Local**: Runs directly on your machine, faster for development
- **Docker**: Container-based, same everywhere, better for production

Choose local for learning, Docker for deployment.

---

## Setup & Installation

### Q: What Python version do I need?
**A:** Python 3.11 or higher. Check with:
```bash
python --version
```

### Q: Why do I need a virtual environment?
**A:** It isolates project dependencies so they don't conflict with your system Python.

### Q: Can I skip the virtual environment?
**A:** Not recommended. It's small overhead that prevents many issues.

### Q: How do I know if installation worked?
**A:** Run:
```bash
python validate.py
```
If all checks pass, you're good!

---

## Running the Server

### Q: Port 7860 is in use. Can I change it?
**A:** Yes! Edit `server/app.py`:
```python
def main(host: str = "0.0.0.0", port: int = 8000) -> None:  # Change 7860 to 8000
    uvicorn.run(app, host=host, port=port)
```

### Q: How do I stop the server?
**A:** Press `CTRL+C` in the terminal.

### Q: Can I run the server in the background?
**A:** Yes:
```bash
python -m server.app &
```
To stop it:
```bash
jobs  # Find the job number
kill %1  # Kill job 1
```

### Q: Why does validation pass but server doesn't start?
**A:** Usually a port conflict. Try changing the port (see above).

---

## Docker

### Q: Why is Docker build so slow?
**A:** It's downloading Python, all packages, and building the image. This is normal (~5 min first time).

### Q: Can I use Docker on Windows?
**A:** Yes! Install Docker Desktop for Windows.

### Q: How do I debug inside a Docker container?
**A:** 
```bash
# Get container ID
docker ps

# Enter container
docker exec -it <container_id> /bin/bash

# Now you can debug inside
```

### Q: Why Docker if I can run locally?
**A:** Docker ensures identical environment everywhere - great for team/production.

---

## API & Testing

### Q: How do I know if my action is correct?
**A:** The reward score tells you:
- 1.0 = Perfect
- 0.5-0.9 = Partially correct
- 0.0 = Wrong

### Q: Can I have multiple tasks running?
**A:** Not in single server instance. Each task is independent. For concurrency, use multiple server instances.

### Q: What's the max steps per task?
**A:** Set per-task (usually 5-10). Check with:
```bash
curl http://localhost:7860/metadata
```

### Q: Can I modify tasks after reset?
**A:** No, tasks are immutable once loaded. Reset to start new task.

### Q: What happens if I exceed max_steps?
**A:** You can still step, but task is marked `done=true` and no more rewards.

---

## Troubleshooting

### Q: I get "ModuleNotFoundError: No module named 'fastapi'"
**A:** Virtual environment not activated. Run:
```bash
source .venv/bin/activate
```

### Q: Server responds but API returns 422 error
**A:** Invalid JSON format. Check request body:
```json
{
  "operation": "impute",
  "target_index": 3,
  "predicted_value": 135.0,
  "severity": "low",
  "violated_constraints": [],
  "rationale": "explanation"
}
```

### Q: Docker container exits immediately
**A:** Check logs:
```bash
docker logs <container_id>
```
Usually permission or import issues.

### Q: How do I see server debug output?
**A:** 
```bash
# Local
python -m server.app  # Logs to stdout

# Docker
docker logs -f <container_id>
```

---

## Customization

### Q: Can I add my own tasks?
**A:** Yes! Edit `server/environment.py` and add a TaskSpec. See [Custom Tasks](./advanced/custom-tasks.md).

### Q: Can I change the reward function?
**A:** Yes! Modify the `grade_action()` method in `server/environment.py`.

### Q: Can I add authentication?
**A:** Yes! Add FastAPI security middleware. Check FastAPI docs.

### Q: Can I add CORS for browser access?
**A:** Already included! The API accepts requests from any origin.

---

## Performance

### Q: Why is my API slow?
**A:** Typical response time is < 100ms. If slower:
- Check CPU usage: `top`
- Check memory: `free -h`
- Check network latency: `curl -w "@curl-format.txt" ...`

### Q: Can I deploy to the cloud?
**A:** Yes! Works on AWS, Google Cloud, Azure. Use Docker image.

### Q: How many requests/second can it handle?
**A:** Single instance: ~100 req/s. Use load balancer for more.

---

## Data & Privacy

### Q: Are tasks stored in database?
**A:** No! Everything is in-memory. Data lost on restart.

### Q: Can I export results?
**A:** Yes, capture response JSON and save to file.

### Q: Is data secure?
**A:** No authentication by default. Add if needed for production.

---

## Contributing

### Q: Can I contribute to this project?
**A:** Yes! See [Contributing](./contributing.md) guide.

### Q: How do I report bugs?
**A:** Open GitHub issue with:
- Error message
- Steps to reproduce
- Environment info

### Q: Can I suggest new tasks?
**A:** Yes! Open issue with task description.

---

## Learning

### Q: Where do I start?
**A:** 
1. Read [Overview](./overview.md)
2. Follow [Quick Start](./quick-start.md)
3. Try [Basic Tutorial](./tutorials/01-basic-tutorial.md)

### Q: How do I build an AI agent?
**A:** See [Building an Agent](./tutorials/03-building-an-agent.md)

### Q: Where's the code for tasks?
**A:** In `server/environment.py` - search for `TASKS` list.

### Q: How do rewards work mathematically?
**A:** See [Reward System](./advanced/reward-system.md)

---

## Still Have Questions?

1. **Check**: [Troubleshooting Guide](./troubleshooting.md)
2. **Search**: GitHub issues
3. **Read**: Source code comments
4. **Ask**: Open GitHub discussion

---

**Last Updated**: April 11, 2026
