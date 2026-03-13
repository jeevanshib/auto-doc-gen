# auto-doc-gen

`auto-doc-gen` is a local AI documentation generator for code changes.

It reads your latest git diff, detects changed source files and API routes, sends the diff to Ollama using `llama3`, stores the result in JSON, and shows the generated documentation in a React dashboard.

## Features

- Reads local git diffs for the latest commit
- Handles both first-commit and later-commit diff flows
- Detects modified code files only
- Supports code extensions:
  - `.py`
  - `.js`
  - `.ts`
  - `.jsx`
  - `.java`
  - `.go`
- Detects Python functions and API routes
- Generates summaries through Ollama at `http://localhost:11434/api/generate`
- Stores generated updates in `docs/updates.json`
- Displays results in a local React dashboard

## Project Structure

```text
auto-doc-gen
├── backend
│   ├── main.py
│   ├── git_utils.py
│   ├── parser.py
│   ├── llm_service.py
│   ├── storage.py
│   ├── doc_writer.py
│   └── requirements.txt
├── frontend
│   └── dashboard
│       └── src
├── docs
│   └── updates.json
└── scripts
    └── run_generation.py
```

## Tech Stack

- Backend: FastAPI
- Frontend: React + Vite
- LLM: Ollama + Llama 3
- Storage: JSON file

## Requirements

Make sure these are available locally:

- Python 3.11+
- Node.js + npm
- Git
- [Ollama](https://ollama.com/)

You also need the `llama3` model available in Ollama.

## Backend Setup

From the project root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Frontend Setup

From the project root:

```bash
cd frontend/dashboard
npm install
npm run dev
```

Frontend will be available at:

```text
http://127.0.0.1:5173
```

## Ollama Setup

Start Ollama with:

```bash
ollama run llama3
```

The backend uses this endpoint:

```text
http://localhost:11434/api/generate
```

Request format:

```json
{
  "model": "llama3",
  "prompt": "...",
  "stream": false
}
```

## Local Workflow

This project does not require GitHub to generate documentation. It works from your local git history.

Typical local flow:

1. Make a code change.
2. Commit the change locally.
3. Run Ollama.
4. Run the backend.
5. Run the frontend.
6. Open the dashboard.
7. Click `Analyze Latest Commit`.

Result:

- backend reads the latest local git diff
- parser extracts changed files and routes
- Ollama generates a short technical summary
- backend stores the result in `docs/updates.json`
- frontend displays the summary, files changed, and APIs detected

## API Endpoints

### `POST /generate`

Runs the documentation generation flow:

1. reads git diff
2. parses changes
3. skips if no meaningful code changes exist
4. sends diff to Ollama
5. stores the output
6. returns JSON response

Example response:

```json
{
  "commit": "abc123",
  "summary": "...",
  "files": ["backend/main.py"],
  "apis": ["POST /generate"]
}
```

### `GET /history`

Returns saved entries from `docs/updates.json`.

## Stored JSON Format

Entries in `docs/updates.json` follow this shape:

```json
{
  "commit": "...",
  "summary": "...",
  "files": [],
  "apis": [],
  "timestamp": "..."
}
```

## Supported Parser Detection

The parser currently detects:

- modified code files
- Python functions
- API routes from common patterns such as:
  - FastAPI decorators
  - Express-style route declarations
  - inline `GET /path` style matches in diffs

## Debug Logging

The backend prints debug information for:

- detected files
- git diff length
- parsed API routes
- LLM response

## Troubleshooting

### Blank frontend page

If the dashboard is blank:

- make sure the frontend dev server is running
- open browser console and check for runtime errors
- confirm you are using `http://127.0.0.1:5173`

### Ollama not running

If generation fails, start:

```bash
ollama run llama3
```

### No documentation generated

Check:

- you made a real code change
- the change was committed locally
- the changed file has a supported code extension

### Invalid JSON in `updates.json`

If `docs/updates.json` becomes invalid, reset it to:

```json
[]
```

## Example End-to-End Run

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

```bash
cd frontend/dashboard
npm install
npm run dev
```

```bash
ollama run llama3
```

Then:

1. make a small code change
2. commit it locally
3. open the dashboard
4. click `Analyze Latest Commit`

## Status

This project is designed for local developer workflows:

```text
git commit -> POST /generate -> AI summary appears in dashboard
```
