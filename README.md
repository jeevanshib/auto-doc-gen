# auto-doc-gen

Local AI documentation generator for git commits, powered by FastAPI, React, and Ollama.

## Run locally

Backend:

```bash
cd backend
./venv/bin/uvicorn main:app --reload
```

Frontend:

```bash
cd frontend/dashboard
npm run dev
```

Ollama:

```bash
ollama run llama3
```
