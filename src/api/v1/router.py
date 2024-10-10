from fastapi import APIRouter
from .endpoints import events, analytics

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(
    events.router,
    prefix="/events",
    tags=["events"]
)
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["analytics"]
)

@api_router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint to verify if the API is running."""
    return {"status": "healthy"}
