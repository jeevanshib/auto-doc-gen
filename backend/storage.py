from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


FILE = Path(__file__).resolve().parents[1] / "docs" / "updates.json"


def _load_updates() -> list[dict]:
    if not FILE.exists():
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text("[]", encoding="utf-8")
        return []

    try:
        with FILE.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON in {FILE}.") from error

    if not isinstance(data, list):
        raise RuntimeError(f"Expected a list in {FILE}.")

    return data


def save_update(commit: str, summary: str, files: list[str], apis: list[str]) -> dict:
    data = _load_updates()

    entry = {
        "commit": commit,
        "summary": summary,
        "files": files,
        "apis": apis,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    data.append(entry)

    with FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)

    return entry


def get_updates() -> list[dict]:
    return _load_updates()
