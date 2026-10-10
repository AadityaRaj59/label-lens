from io import BytesIO
from functools import lru_cache

import numpy as np
from app.services.storage import save_report
from app.services.label_analysis import analyze_label_text
from app.services.compliance import build_evidence_report
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, File, HTTPException, UploadFile
from rapidocr_onnxruntime import RapidOCR

router = APIRouter(prefix="/ocr", tags=["OCR"])

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


@lru_cache(maxsize=1)
def get_ocr_engine():
    return RapidOCR()


@router.post("/extract", summary="Extract text from a product label")
def extract_text(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Upload a JPEG, PNG, or WebP image."
        )

    content = file.file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds the 10 MB upload limit."
        )

    try:
        with Image.open(BytesIO(content)) as image:
            image.verify()

        with Image.open(BytesIO(content)) as image:
            image = image.convert("RGB")
            image_array = np.asarray(image)

    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise HTTPException(
            status_code=400,
            detail="The file is not a valid or supported image."
        )

    try:
        result, _ = get_ocr_engine()(image_array)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="OCR processing failed. Try a clearer image."
        )

    detections = []

    if result:
        for item in result:
            if not item or len(item) < 3:
                continue

            box, text, confidence = item
            detections.append({
                "text": str(text),
                "confidence": round(float(confidence), 4),
                "bounding_box": box.tolist() if hasattr(box, "tolist") else box,
            })


    extracted_text = "\n".join(
        item["text"] for item in detections if item["text"].strip()
    )

    label_analysis = analyze_label_text(extracted_text)


    evidence_report = build_evidence_report(
        filename=file.filename,
        extracted_text=extracted_text,
        label_analysis=label_analysis,
    )

    try:
        evidence_report["storage_status"] = "persisted"
        evidence_report["notice"] = (
            "This report supports preliminary inspection only. "
            "It is not a finding of legal non-compliance. "
            "Preserve the original image separately for verification."
        )
        save_report(evidence_report)
    except Exception:
        import logging
        logging.exception("Failed to persist evidence report")
        evidence_report["storage_status"] = "failed"


    return {
        "filename": file.filename,
        "status": "completed",
        "text": extracted_text,
        "label_analysis": label_analysis,
        "evidence_report": evidence_report,
        "detections": detections,
        "detection_count": len(detections),
        "note": (
            "OCR output is machine-extracted text. It is not, by itself, "
            "a legal compliance determination."
        ),
    }
