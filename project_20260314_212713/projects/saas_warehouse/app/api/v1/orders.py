from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from app.schemas.common import ApiResponse
from app.services.order_service import OrderService
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole


router = APIRouter(prefix="/orders", tags=["订单"])


@router.post("/", response_model=ApiResponse)
async def create_order(
    data: OrderCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """创建订单"""
    service = OrderService(db)
    order = await service.create_order(data)
    return ApiResponse(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "status": order.status.value,
        "total_amount": float(order.total_amount)
    })


@router.get("/", response_model=ApiResponse)
async def get_orders(
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """查询订单列表"""
    service = OrderService(db)
    
    # 解析日期
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    result = await service.get_orders(
        status=status,
        customer_name=customer_name,
        start_date=start_dt,
        end_date=end_dt,
        page=page,
        size=size
    )
    
    # 转换为响应格式
    items = [OrderResponse.model_validate(item) for item in result['items']]
    return ApiResponse(data={
        "items": items,
        "total": result['total'],
        "page": result['page'],
        "size": result['size']
    })


@router.get("/{order_id}", response_model=ApiResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """订单详情"""
    service = OrderService(db)
    order = await service.get_order(order_id)
    return ApiResponse(data=OrderResponse.model_validate(order))


@router.put("/{order_id}", response_model=ApiResponse)
async def update_order(
    order_id: str,
    data: OrderUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """更新订单"""
    service = OrderService(db)
    order = await service.update_order(order_id, data)
    return ApiResponse(data=OrderResponse.model_validate(order))


@router.post("/{order_id}/cancel", response_model=ApiResponse)
async def cancel_order(
    order_id: str,
    reason: str,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """取消订单"""
    service = OrderService(db)
    order = await service.cancel_order(order_id, reason, current_user.id)
    return ApiResponse(data={
        "order_id": order.id,
        "status": order.status.value
    })
