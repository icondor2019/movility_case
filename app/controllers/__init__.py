from fastapi import APIRouter

from app.controllers import (
    health_controller,
    base_controller
)

api_router = APIRouter()
api_router.include_router(health_controller.api)
api_router.include_router(base_controller.api)
