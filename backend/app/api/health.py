from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    """Return a lightweight health status for local and deployment checks."""
    return {"status": "ok", "service": "labellens-api"}
