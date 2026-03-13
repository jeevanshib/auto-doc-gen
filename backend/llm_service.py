from __future__ import annotations

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def summarize_diff(diff: str) -> str:
    prompt = f"""
You are an engineering documentation assistant.

Analyze the git diff and produce short technical documentation.

Rules:
- Ignore configuration files (.gitignore, .DS_Store, lock files)
- Ignore formatting or whitespace-only changes
- Focus only on meaningful code logic changes
- Mention API changes when present

Output format:
New Features:
- ...

Code Changes:
- ...

Affected Modules:
- ...

Git diff:
{diff}
""".strip()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError("Ollama request failed. Ensure `ollama run llama3` is running.") from error

    try:
        payload = response.json()
    except ValueError as error:
        raise RuntimeError("Ollama returned invalid JSON.") from error

    summary = payload.get("response", "").strip()
    print(f"[llm] response: {summary}")

    if not summary:
        raise RuntimeError("Ollama returned an empty response.")

    return summary
