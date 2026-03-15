from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.order import Order, OrderStatus
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """订单数据访问层"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Order
    
    async def get_by_order_no(self, order_no: str) -> Optional[Order]:
        """根据订单号获取订单"""
        query = select(Order).where(Order.order_no == order_no)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_in_progress_tasks(self, order_id: str) -> List[Any]:
        """获取订单进行中的任务"""
        from app.models.task import Task, TaskStatus
        query = select(Task).where(
            Task.order_id == order_id,
            Task.status == TaskStatus.IN_PROGRESS
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_pending_tasks(self, order_id: str) -> List[Any]:
        """获取订单待处理任务"""
        from app.models.task import Task, TaskStatus
        query = select(Task).where(
            Task.order_id == order_id,
            Task.status == TaskStatus.PENDING
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_statistics(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """订单统计数据"""
        # 总订单数
        total_stmt = select(func.count(Order.id)).where(
            Order.create_time.between(start_date, end_date)
        )
        total_orders = await self.session.scalar(total_stmt)
        
        # 按状态统计
        status_stmt = select(
            Order.status,
            func.count(Order.id)
        ).where(
            Order.create_time.between(start_date, end_date)
        ).group_by(Order.status)
        status_result = await self.session.execute(status_stmt)
        by_status = {status.value: count for status, count in status_result.all()}
        
        # 总金额和平均金额
        amount_stmt = select(
            func.sum(Order.total_amount),
            func.avg(Order.total_amount)
        ).where(
            Order.create_time.between(start_date, end_date),
            Order.status != OrderStatus.CANCELLED
        )
        total_amount, avg_amount = await self.session.execute(amount_stmt).one()
        
        return {
            "total_orders": total_orders or 0,
            "by_status": by_status,
            "total_amount": float(total_amount or 0),
            "avg_amount": float(avg_amount or 0)
        }
