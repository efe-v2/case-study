
from .recommendation import router as recommendation_router
from .interaction import router as interaction_router
from .health import router as health_router

routers = [recommendation_router, interaction_router, health_router]
