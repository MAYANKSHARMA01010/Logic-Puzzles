# Installation

## 1. Create the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Create the env file

```bash
cp .env.example .env
nano .env
```

Add your Hugging Face token and API values.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Validate the setup

```bash
python validate.py
```
