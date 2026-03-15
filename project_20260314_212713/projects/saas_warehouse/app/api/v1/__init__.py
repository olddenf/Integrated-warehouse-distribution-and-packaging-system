from fastapi import APIRouter
from app.api.v1 import auth, orders, tasks, dispatch, reports


api_router = APIRouter(prefix="/api/v1")

# 注册路由
api_router.include_router(auth.router)
api_router.include_router(orders.router)
api_router.include_router(tasks.router)
api_router.include_router(dispatch.router)
api_router.include_router(reports.router)
