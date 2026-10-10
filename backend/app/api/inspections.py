from fastapi import APIRouter, HTTPException, Query

from app.services.storage import get_report, list_reports

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.get("", summary="List recent inspection reports")
def get_inspections(limit: int = Query(default=20, ge=1, le=100)):
    reports = list_reports(limit)
    return {
        "count": len(reports),
        "reports": reports,
    }


@router.get("/{report_id}", summary="Get an inspection report")
def get_inspection(report_id: str):
    report = get_report(report_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection report not found.",
        )

    return report
