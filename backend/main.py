from fastapi import FastAPI
from fastapi import Depends

from backend.core.config import settings
from backend.core.registry import MODULES


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


for router in MODULES:
    app.include_router(router)