from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from app.models.task import Task, TaskType, TaskStatus
from app.models.order import Order
from app.models.user import User, UserRole
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository
from app.utils.id_generator import generate_uuid, generate_task_no
import math


class DispatchService:
    """调度服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.user_repo = UserRepository(db)
        self.task_repo = TaskRepository(db)
    
    async def auto_dispatch(
        self, 
        order_ids: List[str], 
        task_type: TaskType, 
        dispatch_date: date
    ) -> List[Dict[str, Any]]:
        """智能排单"""
        results = []
        
        for order_id in order_ids:
            try:
                result = await self._dispatch_single_order(
                    order_id,
                    task_type,
                    dispatch_date
                )
                results.append(result)
            except Exception as e:
                results.append({
                    "order_id": order_id,
                    "success": False,
                    "reason": str(e)
                })
        
        return results
    
    async def _dispatch_single_order(
        self, 
        order_id: str, 
        task_type: TaskType, 
        dispatch_date: date
    ) -> Dict[str, Any]:
        """单订单排单"""
        # 1. 获取订单
        order = await self.order_repo.get(order_id)
        if not order:
            raise ValueError("订单不存在")
        
        # 2. 筛选候选执行人员
        candidates = await self._filter_candidates(
            order=order,
            task_type=task_type,
            dispatch_date=dispatch_date
        )
        
        if not candidates:
            return {
                "order_id": order_id,
                "success": False,
                "reason": "无可用执行人员"
            }
        
        # 3. 评分排序
        scored_candidates = await self._score_candidates(
            candidates=candidates,
            order=order
        )
        
        # 4. 选择最优执行人员
        best_worker = scored_candidates[0]["worker"]
        
        # 5. 创建任务
        task = await self._create_task(
            order=order,
            worker=best_worker,
            task_type=task_type
        )
        
        return {
            "order_id": order_id,
            "success": True,
            "task_id": task.id,
            "task_no": task.task_no,
            "worker_name": best_worker.name,
            "worker_phone": best_worker.phone,
            "score": scored_candidates[0]["score"],
            "score_details": scored_candidates[0]["reasons"]
        }
    
    async def _filter_candidates(
        self, 
        order: Order, 
        task_type: TaskType, 
        dispatch_date: date
    ) -> List[User]:
        """筛选候选执行人员"""
        # 获取对应角色的工人
        role = self._map_task_to_role(task_type)
        workers = await self.user_repo.get_active_workers_by_role(role)
        
        candidates = []
        
        for worker in workers:
            # 规则1: 区域匹配（简化实现）
            if not self._match_region(worker, order):
                continue
            
            # 规则2: 技能匹配（仅安装任务）
            if task_type == TaskType.INSTALL:
                if not await self._match_skill(worker, order.products):
                    continue
            
            # 规则3: 时间可用
            if not await self._check_time_available(
                worker.id,
                dispatch_date,
                order.appointment_time
            ):
                continue
            
            candidates.append(worker)
        
        return candidates
    
    async def _score_candidates(
        self, 
        candidates: List[User], 
        order: Order
    ) -> List[Dict[str, Any]]:
        """为候选人评分"""
        scored = []
        
        for worker in candidates:
            score = 0
            reasons = []
            
            # 评分1: 工作量均衡 (权重40%)
            today_task_count = await self.task_repo.count_today_tasks(
                worker.id,
                date.today()
            )
            workload_score = max(0, 100 - today_task_count * 5)
            score += workload_score * 0.4
            reasons.append(f"今日任务:{today_task_count}")
            
            # 评分2: 距离 (权重30%)
            if worker.latitude and worker.longitude and order.latitude and order.longitude:
                distance = await self._calculate_distance(
                    float(worker.latitude),
                    float(worker.longitude),
                    float(order.latitude),
                    float(order.longitude)
                )
                distance_score = max(0, 100 - distance)
                score += distance_score * 0.3
                reasons.append(f"距离:{distance:.1f}km")
            else:
                score += 30  # 无位置信息给中等分
                reasons.append("距离:未知")
            
            # 评分3: 历史评价 (权重30%)
            avg_rating = await self.user_repo.get_avg_rating(worker.id)
            rating_score = (avg_rating or 3.0) * 20  # 5分制 → 100分
            score += rating_score * 0.3
            reasons.append(f"评分:{avg_rating or 3.0:.1f}")
            
            scored.append({
                "worker": worker,
                "score": score,
                "reasons": reasons
            })
        
        # 按分数降序排序
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored
    
    async def _calculate_distance(
        self, 
        lat1: float, 
        lng1: float, 
        lat2: float, 
        lng2: float
    ) -> float:
        """计算两点距离（公里）"""
        # Haversine公式
        R = 6371  # 地球半径（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _match_region(self, worker: User, order: Order) -> bool:
        """区域匹配"""
        # 简化实现，返回True
        return True
    
    async def _match_skill(self, worker: User, products: List) -> bool:
        """技能匹配"""
        worker_skills = await self.user_repo.get_worker_skills(worker.id)
        product_codes = [p.product_code for p in products if p.product_code]
        
        # 检查工人是否具备所有商品的安装技能
        for code in product_codes:
            if code not in worker_skills:
                return False
        return True
    
    async def _check_time_available(
        self, 
        worker_id: str, 
        dispatch_date: date, 
        appointment_time: datetime
    ) -> bool:
        """检查时间是否可用"""
        # 查询当天该执行人员的任务
        tasks = await self.task_repo.get_worker_tasks_by_date(worker_id, dispatch_date)
        
        for task in tasks:
            # 检查时间冲突（假设每个任务需要2小时）
            task_start = task.start_time or appointment_time
            task_end = task_start + timedelta(hours=2)
            
            if task_start <= appointment_time <= task_end:
                return False
        
        return True
    
    async def _create_task(
        self, 
        order: Order, 
        worker: User, 
        task_type: TaskType
    ) -> Task:
        """创建任务"""
        task_no = generate_task_no(task_type.value)
        
        task = Task(
            id=generate_uuid(),
            task_no=task_no,
            order_id=order.id,
            task_type=task_type,
            assigned_to=worker.id,
            status=TaskStatus.PENDING
        )
        
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        
        return task
    
    def _map_task_to_role(self, task_type: TaskType) -> UserRole:
        """任务类型映射到角色"""
        mapping = {
            TaskType.UNLOAD: UserRole.UNLOADER,
            TaskType.DELIVERY: UserRole.DRIVER,
            TaskType.INSTALL: UserRole.INSTALLER
        }
        return mapping.get(task_type)
    
    async def manual_dispatch(
        self, 
        task_id: str, 
        new_worker_id: str, 
        reason: str, 
        operator_id: str
    ) -> Task:
        """手动调整任务执行人"""
        from app.models.task import TaskDispatchLog
        
        task = await self.task_repo.get(task_id)
        if not task:
            raise ValueError("任务不存在")
        
        if task.status != TaskStatus.PENDING:
            raise ValueError("仅待处理任务可调整执行人")
        
        # 记录变更
        old_worker_id = task.assigned_to
        task.assigned_to = new_worker_id
        
        # 记录日志
        log = TaskDispatchLog(
            id=generate_uuid(),
            task_id=task.id,
            old_worker_id=old_worker_id,
            new_worker_id=new_worker_id,
            operator_id=operator_id,
            reason=reason
        )
        self.db.add(log)
        
        await self.db.commit()
        await self.db.refresh(task)
        
        return task
