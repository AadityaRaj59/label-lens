# LabelLens architecture notes

## Current Phase 1

- Static landing page retained without a redesign.
- FastAPI app with `/`, `/api/v1/health`, and interactive OpenAPI docs.
- Environment-backed CORS configuration.
- Automated smoke tests and a GitHub Actions test workflow.

## Next phases

Keep legal rules deterministic and versioned. Use AI for OCR assistance and interpretation, but do not let an LLM invent rule citations or override deterministic checks. Persist original evidence and derived outputs separately. Require authorized human approval before any complaint is submitted.
