
from .recommendation import router as recommendation_router
from .interaction import router as interaction_router
from .health import router as health_router
from .user import router as user_router
from .model import router as model_router
from .data import router as data_router


routers = [recommendation_router, interaction_router, health_router,user_router,model_router,data_router]
