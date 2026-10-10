from backend.modules.community.router import router as community_router
from backend.modules.stories.routers.stories import router as stories_router
from backend.modules.stories.routers.categories import router as categories_router
from backend.modules.stories.routers.tags import router as tags_router
from backend.modules.users.router import router as users_router
from backend.modules.interactions.router import router as interactions_router

MODULES = [
    users_router,
    stories_router,
    categories_router,
    tags_router,
    community_router,
    interactions_router,
]
