from __future__ import annotations

import subprocess
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]


def _run_git_command(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def get_last_commit() -> str:
    return _run_git_command(["rev-parse", "--short", "HEAD"]).strip()


def get_git_diff() -> str:
    try:
        commit_count = int(_run_git_command(["rev-list", "--count", "HEAD"]).strip())
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.strip() or "Unable to determine git history.") from error

    try:
        if commit_count <= 1:
            diff = _run_git_command(["show", "--format=", "--unified=0", "HEAD"])
        else:
            diff = _run_git_command(["diff", "--unified=0", "HEAD~1", "HEAD"])
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.strip() or "Unable to read git diff.") from error

    print(f"[git] diff length: {len(diff)}")
    return diff
