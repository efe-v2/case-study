
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "I am standing..."}
