LabelLens
LabelLens is a prototype for reviewing packaged-product labels against common Legal Metrology declaration requirements. It combines OCR-based text extraction with a review checklist so that a person can quickly identify details that may need a closer look.
The current MVP focuses on image upload, OCR extraction, preliminary screening, and saving inspection reports locally. It is a decision-support tool—not an official compliance determination or an automated complaint-submission service.
Repository: https://github.com/AadityaRaj59/label-lens
What it does today
- Accepts a product-label image through the API.
- Extracts visible text using the backend OCR pipeline.
- Screens the extracted text for common declaration cues:
  - Maximum Retail Price (MRP)
  - Net quantity
  - Manufacturer or packer details
  - Manufacturing or packing date
  - Consumer-care details
  - Importer details
- Presents findings as a preliminary checklist for human review.
- Stores inspection reports in a local SQLite database.
- Provides endpoints to check API health and retrieve saved inspection reports.
- Includes a browser-based frontend and a FastAPI backend.
A missing OCR match does not prove that a declaration is absent from the package. Text recognition can be affected by image quality, orientation, glare, small print, and packaging design. Always compare the result with the original label.
Project layout
label-lens/
├── .github/
│   └── workflows/
│       └── backend-tests.yml
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── health.py
│   │   │   ├── inspections.py
│   │   │   └── ocr.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── services/
│   │   │   ├── compliance.py
│   │   │   ├── label_analysis.py
│   │   │   └── storage.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── pytest.ini
├── docs/
│   └── ARCHITECTURE.md
├── frontend/
│   └── index.html
├── .gitignore
└── README.md
Tech stack
- Frontend: HTML, CSS, and JavaScript
- Backend: Python and FastAPI
- OCR: RapidOCR
- Local persistence: SQLite
- API documentation: OpenAPI / Swagger UI
- Tests and automation: pytest and GitHub Actions
Run locally on Windows
You need Python 3.12 installed. Run the commands below from the project root.
1. Install backend dependencies
cd backend
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install --upgrade pip
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
cd ..
If Python 3.12 is not available through the py launcher, install Python 3.12 or use the Python version supported by the dependencies in backend/requirements.txt.
2. Start the API
Open a PowerShell terminal in the project root:
& ".\backend\.venv312\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --app-dir backend
The API will be available at:
- Health check: http://127.0.0.1:8000/api/v1/health
- Interactive API docs: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json
Keep this terminal running while using the frontend.
3. Start the frontend
Open a second PowerShell terminal in the project root:
py -m http.server 5500 --directory frontend
Open http://127.0.0.1:5500 in your browser.
The inspection workspace calls the local API at http://127.0.0.1:8000/api/v1. If you change the backend address or port, update the frontend API base URL accordingly.
API endpoints
Method	Endpoint	Purpose
GET	/api/v1/health	Check whether the API is running
POST	/api/v1/ocr/extract	Upload a label image and receive OCR and preliminary screening results
GET	/api/v1/inspections?limit=20	List recent saved inspection reports
GET	/api/v1/inspections/{report_id}	Retrieve a saved report


The OCR endpoint accepts an image as multipart/form-data using the file field. Supported formats in the current implementation are JPEG, PNG, and WebP, with a 10 MB upload limit.
Example request:
curl -X POST "http://127.0.0.1:8000/api/v1/ocr/extract" \
  -H "accept: application/json" \
  -F "file=@product-label.jpg"
You can also upload an image from the interactive documentation at /docs.
Inspection results and storage
The API returns the extracted text, preliminary label-analysis results, and review items. The current checklist is a screening aid based on detected text cues; it is not a complete legal rules engine and does not replace an inspector's judgment.
Inspection reports are stored locally in SQLite at:
backend/data/labellens.sqlite3
The database is generated during local use and should not be committed to Git. The repository's ignore rules exclude local database files, virtual environments, environment files, and backup files.
Configuration and secrets
The backend reads settings through Pydantic Settings and can load values from a .env file. Keep real credentials in local environment configuration or your hosting provider's secret settings—not in source code, README examples, screenshots, or Git commits.
The database_url setting defaults to an empty value in the current configuration. Local inspection persistence uses SQLite. A production database connection must be configured and tested before relying on hosted persistence.
Run tests
From the project root:
.\backend\.venv312\Scripts\python.exe -m pytest backend
The repository also includes a GitHub Actions workflow for backend tests. Check the Actions tab on GitHub to see the latest workflow result.
Current scope and limitations
This is an MVP under active development. At present:
- OCR quality depends on the clarity and framing of the uploaded image.
- Declaration checks are preliminary text-cue checks; they do not establish a legal violation.
- A reviewer should verify every finding against the original package and the applicable rules.
- Reports are stored locally in SQLite by default.
- Automatic complaint filing, marketplace crawling, live enforcement integrations, and production authentication should not be considered available unless separately implemented, configured, and tested.
- The project has not been described here as production-deployed.
Next development steps
- Improve image preprocessing and OCR handling for small or rotated packaging text.
- Add test images with manually verified expected OCR output.
- Expand versioned, deterministic rule checks and include rule references in findings.
- Make report evidence and reviewer decisions easier to audit.
- Configure and test secure hosted storage, authentication, and deployment before using real inspection data.
- Keep complaint drafting and any eventual submission behind explicit human review.
Contributing
For a change, create a branch, make the update, run the backend tests, and open a pull request with a short explanation of what changed and how it was tested.
git checkout -b feat/describe-change
git add .
git commit -m "Describe the change"
git push -u origin feat/describe-change
Disclaimer
LabelLens provides preliminary technical screening to assist review. It does not issue official legal findings, provide legal advice, or guarantee that a product complies with or violates applicable law. OCR output may be incomplete or incorrect. Confirm all findings against the original label and current legal requirements before taking action.
