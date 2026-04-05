"""Server scaffold for your custom API."""

import argparse

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Logic Gates API Scaffold", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run API server. Add your own routes in this module."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(port=args.port)
