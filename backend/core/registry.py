from backend.modules.community.router import router as community_router
from backend.modules.stories.router import router as stories_router
from backend.modules.users.router import router as users_router

MODULES = [
    users_router,
    stories_router,
    community_router,
]
