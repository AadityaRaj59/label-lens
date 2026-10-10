from datetime import datetime, timezone
from typing import Any

RULESET_ID = "labellens-packaged-commodities-screening"
RULESET_VERSION = "0.1.0"

# These are screening checks, not a complete legal rulebook.
# Applicability and the current law must be verified by an inspector.
SCREENING_RULES = [
    {
        "id": "LL-SCR-001",
        "field": "mrp",
        "description": "Look for a maximum retail price declaration.",
    },
    {
        "id": "LL-SCR-002",
        "field": "net_quantity",
        "description": "Look for a net quantity or quantity-unit declaration.",
    },
    {
        "id": "LL-SCR-003",
        "field": "manufacturer_or_packer",
        "description": "Look for manufacturer, packer, or marketer details.",
    },
    {
        "id": "LL-SCR-004",
        "field": "manufacturing_or_packing_date",
        "description": "Look for manufacturing or packing date information.",
    },
    {
        "id": "LL-SCR-005",
        "field": "consumer_care",
        "description": "Look for consumer-care contact information.",
    },
]


def run_screening(label_analysis: dict[str, Any]) -> dict[str, Any]:
    fields = label_analysis.get("fields", {})
    results = []

    for rule in SCREENING_RULES:
        field_result = fields.get(rule["field"], {})
        detected = field_result.get("status") == "detected"

        results.append({
            "rule_id": rule["id"],
            "description": rule["description"],
            "field": rule["field"],
            "status": "cue_detected" if detected else "needs_review",
            "evidence": field_result.get("matches", []),
            "finding": (
                "A matching text cue was detected; verify it against the image."
                if detected
                else "No matching cue was detected; inspect the full package image."
            ),
        })

    return {
        "ruleset_id": RULESET_ID,
        "ruleset_version": RULESET_VERSION,
        "results": results,
        "human_review_required": True,
        "legal_violation_confirmed": False,
        "scope_note": (
            "This preliminary screening ruleset is not a complete implementation "
            "of the Legal Metrology (Packaged Commodities) Rules. It does not "
            "evaluate every requirement, exception, product category, declaration "
            "format, or current amendment. A missing cue is not proof of a violation."
        ),
    }


def build_evidence_report(
    filename: str | None,
    extracted_text: str,
    label_analysis: dict[str, Any],
) -> dict[str, Any]:
    from uuid import uuid4

    return {
        "report_id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "filename": filename,
            "method": "image_upload_and_rapidocr",
        },
        "ocr": {
            "text": extracted_text,
            "review_required": True,
        },
        "label_analysis": label_analysis,
        "screening": run_screening(label_analysis),
        "review": {
            "status": "pending",
            "reviewer": None,
            "decision": None,
        },
        "storage_status": "not_persisted",
        "notice": (
            "This report is generated for preliminary inspection support. "
            "It is not a finding of legal non-compliance and has not been "
            "persisted to a database. Preserve the original image separately "
            "if it is needed for later verification."
        ),
    }
