# Overview

This project is a small OpenEnv environment where an AI agent solves pattern puzzles.

## What the agent does

- Sees a sequence with a missing next value
- Sends a guess through the OpenEnv `step()` API
- Gets feedback and a reward
- Tries again until the episode ends

## Tasks

- Easy: simple arithmetic and number patterns
- Medium: mixed numeric and letter patterns
- Hard: primes, factorials, look-and-say, and other harder rules

## Action Space

- Input: `{ "guess": "10" }`
- The guess must be a string

## Observation Space

- `sequence`: the current puzzle text
- `feedback`: short result message
- `attempts_left`: how many tries remain
- `task_difficulty`: easy, medium, or hard

## Reward

- Easy: base reward 1.0
- Medium: base reward 2.0
- Hard: base reward 3.0
- Faster correct answers earn a bigger bonus
