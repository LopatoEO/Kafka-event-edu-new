from fastapi import APIRouter
from src.api.v1.event import event_router

router = APIRouter(prefix="/v1")

router.include_router(event_router, prefix="/events")