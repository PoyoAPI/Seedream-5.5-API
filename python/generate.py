"""Seedream 5.5 API example for PoYo (Python 3.9+, standard library only).

Usage:
    python python/generate.py                       # default: payloads/seedream-5.5-text-to-image.json
    python python/generate.py payloads/<file>.json
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PAYLOAD = ROOT / "payloads" / "seedream-5.5-text-to-image.json"


def load_env() -> None:
    for env_path in (Path.cwd() / ".env", ROOT / ".env"):
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env()
API_KEY = os.environ.get("POYO_API_KEY", "")
BASE_URL = os.environ.get("POYO_BASE_URL", "https://api.poyo.ai").rstrip("/")
if not API_KEY or API_KEY == "YOUR_POYO_API_KEY_HERE":
    sys.exit("Set POYO_API_KEY in your environment or repo-root .env file.")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "poyo-seedream-5-5-api-example/1.0",
}


def request_json(path: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=HEADERS, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status, text = response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status, text = error.code, error.read().decode("utf-8", "replace")
    try:
        body = json.loads(text) if text else {}
    except ValueError:
        body = {"raw": text}
    api_code = body.get("code") if isinstance(body, dict) else None
    if status >= 400 or (isinstance(api_code, int) and api_code not in (0, 200)):
        raise RuntimeError(f"PoYo request failed: {json.dumps({'http_status': status, 'api_code': api_code, 'body': body}, indent=2)}")
    return body


payload_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PAYLOAD
payload = json.loads(payload_path.read_text(encoding="utf-8"))
if os.environ.get("POYO_CALLBACK_URL"):
    payload["callback_url"] = os.environ["POYO_CALLBACK_URL"]

submitted = request_json("/api/generate/submit", payload)
task_id = (submitted.get("data") or {}).get("task_id")
if not task_id:
    raise RuntimeError(f"Missing data.task_id: {submitted}")
print(f"submitted {payload['model']} task: {task_id}")

for attempt in range(1, 121):
    result = request_json(f"/api/generate/status/{task_id}")
    status = (result.get("data") or {}).get("status")
    print(f"poll {attempt}: {status or 'unknown'}")
    if status in ("finished", "failed"):
        print(json.dumps(result, indent=2))
        sys.exit(0 if status == "finished" else 1)
    time.sleep(5)
raise TimeoutError(f"Timed out waiting for task {task_id}")
