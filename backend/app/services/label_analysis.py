import re
from typing import Any


PATTERNS = {
    "mrp": [
        r"\b(?:MRP|M\.R\.P\.?)\s*(?:RS\.?|INR|₹)?\s*[:\-]?\s*(?:₹|Rs\.?)?\s*\d+(?:[.,]\d{1,2})?",
        r"\b(?:maximum retail price)\b",
    ],
    "net_quantity": [
        r"\b(?:net\s+(?:quantity|weight|contents?)|net\s+qty\.?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:kg|g|gm|mg|ml|l|litre|liter|litres|liters)\b",
    ],
    "manufacturer_or_packer": [
        r"\b(?:manufactured|manufactured by|manufactured for|marketed by|packed by|packer)\b",
    ],
    "manufacturing_or_packing_date": [
        r"\b(?:date of manufacture|mfg\.?\s*date|manufacturing date|packed on|packing date|pkd\.?)\b",
    ],
    "consumer_care": [
        r"\b(?:consumer care|customer care|consumer complaints?|customer service|helpline|toll[- ]free)\b",
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
    ],
    "importer": [
        r"\b(?:imported by|importer)\b",
    ],
}


def analyze_label_text(text: str) -> dict[str, Any]:
    """Identify declaration cues in OCR text; do not make legal conclusions."""
    normalized = re.sub(r"\s+", " ", text or "").strip()
    fields: dict[str, dict[str, Any]] = {}

    for field_name, patterns in PATTERNS.items():
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, normalized, re.IGNORECASE):
                value = match.group(0).strip()
                if value not in matches:
                    matches.append(value)

        fields[field_name] = {
            "status": "detected" if matches else "not_detected",
            "matches": matches[:10],
        }

    review_items = [
        {
            "field": name,
            "reason": "Declaration cue was not detected in OCR text; check the original package image.",
        }
        for name, field in fields.items()
        if field["status"] == "not_detected"
    ]

    return {
        "fields": fields,
        "review_items": review_items,
        "review_required": True,
        "assessment": "preliminary_screening_only",
        "disclaimer": (
            "A missing OCR cue is not proof of a legal violation. "
            "Verify the complete label, image quality, product category, "
            "applicable exemptions, and current rules before any decision."
        ),
    }
