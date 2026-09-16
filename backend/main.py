from fastapi import FastAPI
from fastapi import Depends
from backend.core.auth import get_current_user

from backend.core.config import settings
from backend.core.registry import MODULES


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


for router in MODULES:
    app.include_router(router)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "app": settings.app_name,
    }