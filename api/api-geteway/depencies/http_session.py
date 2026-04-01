from fastapi import Request
from aiohttp import ClientSession

async def get_session(request: Request) -> ClientSession:
    return request.app.state.session