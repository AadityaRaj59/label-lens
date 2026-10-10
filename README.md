# LabelLens

LabelLens is an AI-assisted inspection platform for packaged-commodity declarations under India's Legal Metrology framework. This repository starts with the existing landing page and a small FastAPI backend foundation.

> **Current status:** Phase 1 scaffold. The landing page is preserved as `frontend/index.html`. The API currently provides health and metadata endpoints only. OCR, compliance checks, evidence generation, authentication, database persistence, and complaint submission are not implemented yet.

## Repository layout

```text
label-lens/
├── frontend/
│   └── index.html              # Existing landing page, preserved
├── backend/
│   ├── app/
│   │   ├── api/health.py       # API health endpoint
│   │   ├── core/config.py      # Environment-backed settings
│   │   └── main.py             # FastAPI application
│   ├── tests/test_health.py
│   └── requirements.txt
├── docs/
├── .github/workflows/backend-tests.yml
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.11 or newer (Python 3.12 recommended)
- Git
- A modern browser

The existing landing page uses browser-loaded Three.js/Lenis modules and external visual assets. You can preview it as a static page without Node.js.

## Run the landing page (Windows PowerShell)

From the repository root:

```powershell
Start-Process .\frontend\index.html
```

If your browser restricts module loading from `file://`, use Python's static server instead:

```powershell
py -m http.server 5500 --directory frontend
```

Then open `http://localhost:5500`.

## Run the API (Windows PowerShell)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item ..\.env.example .\.env
uvicorn app.main:app --reload
```

If PowerShell blocks virtual-environment activation, run the executable directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open:

- API welcome: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## Run tests

From `backend/` with the virtual environment active:

```powershell
pytest -q
```

# LabelLens — GitHub Setup

I’ve set up the LabelLens project with its frontend and FastAPI backend and pushed the initial code to my GitHub repository.

**Repository:** https://github.com/AadityaRaj59/label-lens

The repository uses the `main` branch. The project contains the frontend, backend API, tests, documentation, and GitHub Actions workflow.

For local development, I keep environment variables, database files, virtual environments, and backup files out of version control. Only the project files needed to develop and run the application should be committed.

To push future changes, I use:

```bash
git add .
git commit -m "Describe the changes"
git push origin main
```

I’ll continue testing the OCR workflow, inspection reports, and frontend-backend integration as development progresses.
## Planned implementation order

1. Connect frontend actions to backend APIs.
2. Add database models and migrations.
3. Implement secure image upload and OCR extraction.
4. Add a versioned, deterministic compliance rule engine.
5. Generate evidence-backed inspection reports.
6. Add complaint drafts, inspector approval, routing, and status tracking.
7. Add authentication, authorization, observability, deployment configuration, and end-to-end tests.

Actual complaint submission will only be enabled through a supported, authorized channel. A generated draft must never be represented as a submitted complaint.
