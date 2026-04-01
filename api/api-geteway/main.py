from fastapi import FastAPI
from .api import v1
import uvicorn
import aiohttp

app = FastAPI()
app.include_router(v1.router)

@app.on_event("startup")
async def startup():
    app.state.session = aiohttp.ClientSession()

@app.on_event("shutdown")
async def shutdown():
    await app.state.session.close()

if (__name__ == '__main__'):
    uvicorn.run(app)

