from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import date, datetime
from app.models.task import Task, TaskStatus
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """任务数据访问层"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Task
    
    async def get_with_auth(self, task_id: str, worker_id: str) -> Optional[Task]:
        """获取任务并验证归属"""
        task = await self.get(task_id)
        if task and task.assigned_to == worker_id:
            return task
        return None
    
    async def get_delivery_task(self, order_id: str) -> Optional[Task]:
        """获取订单的配送任务"""
        from app.models.task import TaskType
        query = select(Task).where(
            Task.order_id == order_id,
            Task.task_type == TaskType.DELIVERY
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def count_today_tasks(self, worker_id: str, target_date: date) -> int:
        """统计工人当天的任务数"""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        query = select(Task).where(
            Task.assigned_to == worker_id,
            Task.create_time.between(start_datetime, end_datetime)
        )
        result = await self.session.execute(query)
        return len(result.scalars().all())
    
    async def get_worker_tasks_by_date(self, worker_id: str, target_date: date) -> List[Task]:
        """获取工人某天的任务"""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        query = select(Task).where(
            Task.assigned_to == worker_id,
            Task.create_time.between(start_datetime, end_datetime)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_worker_tasks(
        self, 
        worker_id: str, 
        task_type: Optional[str] = None, 
        date: Optional[date] = None
    ) -> List[Task]:
        """获取工人的任务列表"""
        query = select(Task).where(Task.assigned_to == worker_id)
        
        if task_type:
            query = query.where(Task.task_type == task_type)
        
        if date:
            start_datetime = datetime.combine(date, datetime.min.time())
            end_datetime = datetime.combine(date, datetime.max.time())
            query = query.where(Task.create_time.between(start_datetime, end_datetime))
        
        # 按创建时间倒序
        query = query.order_by(Task.create_time.desc())
        
        result = await self.session.execute(query)
        return result.scalars().all()
