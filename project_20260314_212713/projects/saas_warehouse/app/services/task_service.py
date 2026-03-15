from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.task import Task, TaskType, TaskStatus, Attachment, TaskRecord
from app.models.order import Order, OrderStatus
from app.schemas.task import TaskCompleteRequest, LocationUpdate
from app.repositories.task_repository import TaskRepository
from app.utils.id_generator import generate_uuid, generate_task_no
from app.core.state_machine import OrderStateMachine


class TaskService:
    """任务服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
    
    async def start_task(
        self, 
        task_id: str, 
        location: LocationUpdate, 
        worker_id: str
    ) -> Task:
        """开始任务"""
        task = await self.task_repo.get_with_auth(task_id, worker_id)
        
        if not task:
            raise ValueError("任务不存在或无权限")
        
        if task.status != TaskStatus.PENDING:
            raise ValueError(f"任务状态{task.status.value}不允许开始")
        
        # 更新任务
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = datetime.now()
        
        # 创建执行记录
        record = TaskRecord(
            id=generate_uuid(),
            task_id=task.id,
            record_type='start',
            location_lat=location.latitude,
            location_lng=location.longitude
        )
        self.db.add(record)
        
        await self.db.commit()
        await self.db.refresh(task)
        
        return task
    
    async def complete_task(
        self, 
        task_id: str, 
        data: TaskCompleteRequest, 
        worker_id: str
    ) -> Task:
        """完成任务"""
        task = await self.task_repo.get_with_auth(task_id, worker_id)
        
        if not task:
            raise ValueError("任务不存在或无权限")
        
        if task.status != TaskStatus.IN_PROGRESS:
            raise ValueError(f"任务状态{task.status.value}不允许完成")
        
        # 处理照片
        for photo_url in data.photos:
            attachment = Attachment(
                id=generate_uuid(),
                task_id=task.id,
                file_name=photo_url.split('/')[-1],
                file_url=photo_url,
                upload_by=worker_id
            )
            self.db.add(attachment)
        
        # 更新任务
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.now()
        task.remark = data.remark
        
        # 创建完成记录
        record = TaskRecord(
            id=generate_uuid(),
            task_id=task.id,
            record_type='complete',
            content=data.remark
        )
        self.db.add(record)
        
        await self.db.commit()
        await self.db.refresh(task)
        
        # 触发后续流程
        await self._trigger_next_step(task)
        
        return task
    
    async def _trigger_next_step(self, task: Task) -> None:
        """触发后续流程"""
        order = await self.db.get(Order, task.order_id)
        
        if task.task_type == TaskType.UNLOAD:
            # 卸货完成，创建配送任务
            await self._create_next_task(order, TaskType.DELIVERY)
        elif task.task_type == TaskType.DELIVERY:
            # 配送完成，创建安装任务
            await self._create_next_task(order, TaskType.INSTALL)
        elif task.task_type == TaskType.INSTALL:
            # 安装完成，订单完成
            log = OrderStateMachine.transition(
                order,
                OrderStatus.COMPLETED,
                'system',
                '安装完成自动完成订单'
            )
            self.db.add(log)
            await self.db.commit()
    
    async def _create_next_task(self, order: Order, task_type: TaskType) -> Task:
        """创建下一个任务"""
        from app.services.dispatch_service import DispatchService
        
        dispatch_service = DispatchService(self.db)
        
        # 智能分配
        result = await dispatch_service._dispatch_single_order(
            order.id,
            task_type,
            datetime.now().date()
        )
        
        if not result.get('success'):
            return None
        
        # 更新订单状态
        if task_type == TaskType.DELIVERY:
            log = OrderStateMachine.transition(
                order,
                OrderStatus.DELIVERING,
                'system',
                '配送任务创建'
            )
            self.db.add(log)
        elif task_type == TaskType.INSTALL:
            log = OrderStateMachine.transition(
                order,
                OrderStatus.INSTALLING,
                'system',
                '安装任务创建'
            )
            self.db.add(log)
        
        await self.db.commit()
        
        return await self.task_repo.get(result['task_id'])
    
    async def get_my_tasks(
        self, 
        worker_id: str, 
        task_type: Optional[str] = None, 
        date: Optional[datetime.date] = None
    ) -> List[Dict[str, Any]]:
        """获取我的任务列表"""
        tasks = await self.task_repo.get_worker_tasks(
            worker_id=worker_id,
            task_type=task_type,
            date=date
        )
        
        result = []
        for task in tasks:
            result.append({
                "task_id": task.id,
                "task_no": task.task_no,
                "task_type": task.task_type.value,
                "status": task.status.value,
                "start_time": task.start_time.isoformat() if task.start_time else None,
                "end_time": task.end_time.isoformat() if task.end_time else None,
                "order": {
                    "order_no": task.order.order_no,
                    "customer_name": task.order.customer_name,
                    "customer_phone": task.order.customer_phone,
                    "address": task.order.address,
                    "appointment_time": task.order.appointment_time.isoformat()
                },
                "products": [
                    {
                        "product_name": p.product_name,
                        "quantity": float(p.quantity),
                        "unit": p.unit
                    }
                    for p in task.order.products
                ]
            })
        
        return result
    
    async def get_task_detail(self, task_id: str, worker_id: str) -> Task:
        """获取任务详情"""
        task = await self.task_repo.get_with_auth(task_id, worker_id)
        if not task:
            raise ValueError("任务不存在或无权限")
        return task
