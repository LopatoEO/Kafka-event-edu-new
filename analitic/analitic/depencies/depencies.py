from fastapi import Request
from aiochclient import ChClient

async def get_ch(request: Request) -> ChClient:
    return request.app.state.ch