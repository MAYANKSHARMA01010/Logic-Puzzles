# Local Run

Set up Python environment and run the server locally.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate.py
python -m server.app
```

Open API docs at:

```text
http://localhost:7860/docs
```