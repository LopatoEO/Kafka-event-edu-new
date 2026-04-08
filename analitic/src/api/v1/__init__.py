from fastapi import APIRouter
from . import events

router = APIRouter(prefix="/v1")

router.include_router(events.router, prefix="/events")