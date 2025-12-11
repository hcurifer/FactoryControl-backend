# app/routers/health_router.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/", summary="Health check")
def health_check():
    return {
        "status": "ok",
        "message": "FactoryControl backend running"
    }
