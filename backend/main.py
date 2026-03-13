from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from arch_parser import build_arch_graph
from git_utils import get_git_diff, get_last_commit
from llm_service import summarize_diff
from parser import parse_changes
from storage import get_updates, save_update


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/history")
def history() -> list[dict]:
    try:
        return get_updates()
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.get("/architecture")
def architecture() -> dict:
    try:
        return build_arch_graph("..")
    except Exception as error:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Failed to build architecture graph.") from error


@app.post("/generate")
def generate() -> dict:
    try:
        diff = get_git_diff()
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    if not diff.strip():
        raise HTTPException(status_code=400, detail="Git diff is empty.")

    parsed = parse_changes(diff)
    if not parsed["files"]:
        return {
            "commit": get_last_commit(),
            "summary": "",
            "files": [],
            "apis": [],
            "message": "No meaningful code changes detected",
        }

    try:
        summary = summarize_diff(diff)
        commit = get_last_commit()
        entry = save_update(commit, summary, parsed["files"], parsed["apis"])
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "commit": entry["commit"],
        "summary": entry["summary"],
        "files": entry["files"],
        "apis": entry["apis"],
    }
