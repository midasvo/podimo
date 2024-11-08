from fastapi import APIRouter
from services.health_service import HealthService

router = APIRouter()
health_service = HealthService()

@router.get("/health/check")
async def check_health():
    results = await health_service.check_all_feeds()
    return [result.to_dict() for result in results]

@router.get("/health")
async def health_page():
    # This would return an HTML template with the health status
    results = await health_service.check_all_feeds()
    return {
        "template": "health.html",
        "context": {
            "feeds": [result.to_dict() for result in results]
        }
    } 