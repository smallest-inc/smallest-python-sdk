"""Shared helper for Velocity SDK smoke tests (4.4.7 shipped client).

Reads SMALLEST_API_KEY + base from the repo .env and builds a SmallestAI
client pointed at the Velocity dev stack. NOT for CI — live target only.
"""
import os
import pathlib

_ROOT = pathlib.Path(__file__).resolve().parents[2]


def _load_dotenv():
    env = _ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()  # .env wins for tests


def client():
    _load_dotenv()
    from smallestai import SmallestAI
    from smallestai.environment import SmallestAIEnvironment

    base = os.environ["SMALLEST_BASE_URL"].rstrip("/")
    ws = base.replace("https://", "wss://").replace("http://", "ws://")
    env = SmallestAIEnvironment(atoms=f"{base}/atoms/v1", waves=base, waves_ws=ws)
    return SmallestAI(api_key=os.environ["SMALLEST_API_KEY"], environment=env)
