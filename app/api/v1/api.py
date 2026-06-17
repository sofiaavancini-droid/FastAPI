from fastapi import APIRouter

from .auth import router as auth_router
from .productos import router as productos_router
from .categorias import router as categorias_router

api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    productos_router,
    prefix="/productos",
    tags=["productos"]
)

api_router.include_router(
    categorias_router,
    prefix="/categorias",
    tags=["categorias"]
)