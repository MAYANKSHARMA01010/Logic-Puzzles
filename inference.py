import asyncio
import os
import textwrap
from typing import List, Optional
from openai import OpenAI

API_KEY       = os.getenv("HF_TOKEN")
API_BASE_URL  = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME    = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
IMAGE_NAME    = os.getenv("IMAGE_NAME")   # your Docker image name

TASK_NAME     = os.getenv("PATTERN_TASK",      "sequence_guess")
BENCHMARK     = os.getenv("PATTERN_BENCHMARK", "my_pattern_env")
MAX_STEPS     = int(float(os.getenv("MAX_STEPS",   "3")))
TEMPERATURE   = float(os.getenv("TEMPERATURE",     "0.3"))
MAX_TOKENS    = int(float(os.getenv("MAX_TOKENS",  "50")))


# -----------------------------------------------
# Scoring constants
# -----------------------------------------------
# Max possible reward: hard task (3.0) + full efficiency on attempt 1 of 2 (0.5) = 3.5
MAX_TOTAL_REWARD        = float(os.getenv("MAX_TOTAL_REWARD",        "3.5"))
SUCCESS_SCORE_THRESHOLD = float(os.getenv("SUCCESS_SCORE_THRESHOLD", "0.1"))


# -----------------------------------------------
# LOGGING HELPERS — the only things that print to stdout
# -----------------------------------------------

def log_start(task: str, env: str, model: str) -> None:
    # Exactly one space between fields, no extra characters
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float,
             done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()          # Python True → "true"
    print(
        f"[STEP] step={step} action={action} "
        f"reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int,
            score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.3f} rewards={rewards_str}",
        flush=True,
    )