from fastapi import APIRouter
from src.api.v1 import events

router = APIRouter(prefix="/v1")

router.include_router(events.router, prefix="/events")