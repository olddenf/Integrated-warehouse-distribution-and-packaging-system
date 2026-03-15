# 仓配装一体系统详细设计文档

## 文档信息
- **项目名称**: 仓配装一体系统
- **文档版本**: v3.0 (Python详细设计版)
- **创建日期**: 2026-03-12
- **文档类型**: 详细设计说明书
- **技术栈**: Python FastAPI + Vue3 + MySQL + Redis + Celery

---

## 一、详细设计概述

### 1.1 设计目标
本详细设计文档基于需求文档和概要设计文档，进一步细化到每个模块的类设计、方法实现、接口规范、数据库字段定义、异常处理、性能优化等层面，为开发人员提供可直接编码的详细指导。

### 1.2 文档结构
- 模块详细设计（每个模块的类、方法、逻辑）
- 数据库详细设计（完整表结构、索引、约束）
- 接口详细设计（请求/响应示例、错误码）
- 异常处理与日志设计
- 性能优化方案
- 安全设计实现
- 部署配置详解

---

## 二、目录结构设计

```
saas_warehouse/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI应用入口
│   ├── core/                      # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py              # 配置管理
│   │   ├── database.py            # 数据库连接
│   │   ├── security.py            # JWT认证
│   │   ├── deps.py                # 依赖注入
│   │   ├── permissions.py         # 权限控制
│   │   └── state_machine.py       # 状态机
│   ├── models/                    # ORM模型
│   │   ├── __init__.py
│   │   ├── user.py                # 用户模型
│   │   ├── order.py               # 订单模型
│   │   ├── task.py                # 任务模型
│   │   ├── warehouse.py           # 仓储模型
│   │   ├── fee.py                 # 费用模型
│   │   ├── report.py              # 报表模型
│   │   └── system.py              # 系统模型
│   ├── schemas/                   # Pydantic Schema
│   │   ├── __init__.py
│   │   ├── user.py                # 用户Schema
│   │   ├── order.py               # 订单Schema
│   │   ├── task.py                # 任务Schema
│   │   ├── fee.py                 # 费用Schema
│   │   └── common.py              # 通用Schema
│   ├── services/                  # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py        # 用户服务
│   │   ├── order_service.py       # 订单服务
│   │   ├── task_service.py        # 任务服务
│   │   ├── dispatch_service.py    # 调度服务
│   │   ├── warehouse_service.py   # 仓储服务
│   │   ├── fee_service.py         # 费用服务
│   │   └── report_service.py     # 报表服务
│   ├── api/                       # API路由层
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py            # 认证接口
│   │       ├── users.py           # 用户接口
│   │       ├── orders.py          # 订单接口
│   │       ├── tasks.py           # 任务接口
│   │       ├── dispatch.py        # 调度接口
│   │       ├── warehouse.py       # 仓储接口
│   │       ├── fees.py            # 费用接口
│   │       └── reports.py         # 报表接口
│   ├── repositories/              # 数据访问层
│   │   ├── __init__.py
│   │   ├── base_repository.py     # 基础Repository
│   │   ├── user_repository.py     # 用户Repository
│   │   ├── order_repository.py    # 订单Repository
│   │   └── task_repository.py     # 任务Repository
│   ├── tasks/                     # Celery异步任务
│   │   ├── __init__.py
│   │   ├── celery_app.py          # Celery配置
│   │   ├── image_tasks.py         # 图片处理任务
│   │   ├── report_tasks.py        # 报表生成任务
│   │   └── notify_tasks.py        # 通知任务
│   ├── utils/                     # 工具函数
│   │   ├── __init__.py
│   │   ├── id_generator.py        # ID生成器
│   │   ├── map_client.py          # 地图API客户端
│   │   ├── oss_client.py          # OSS存储客户端
│   │   ├── sms_client.py          # 短信客户端
│   │   └── validators.py          # 验证器
│   ├── exceptions/                # 自定义异常
│   │   ├── __init__.py
│   │   ├── base.py                # 基础异常
│   │   └── business.py            # 业务异常
│   ├── middleware/                # 中间件
│   │   ├── __init__.py
│   │   ├── logging.py             # 日志中间件
│   │   └── error_handler.py       # 异常处理中间件
│   └── constants/                 # 常量定义
│       ├── __init__.py
│       ├── error_codes.py         # 错误码
│       └── enums.py               # 枚举
├── tests/                         # 测试代码
│   ├── __init__.py
│   ├── conftest.py                # pytest配置
│   ├── test_api/
│   ├── test_services/
│   └── test_repositories/
├── alembic/                       # 数据库迁移
│   ├── versions/
│   └── env.py
├── scripts/                       # 脚本工具
│   ├── init_db.py                 # 初始化数据库
│   └── create_admin.py            # 创建管理员
├── requirements.txt               # 依赖列表
├── Dockerfile                     # Docker镜像
├── docker-compose.yml             # Docker编排
├── .env.example                   # 环境变量示例
└── README.md
```

---

## 三、核心模块详细设计

### 3.1 订单管理模块

#### 3.1.1 类设计

**OrderService (订单服务)**

```python
class OrderService:
    """
    订单服务
    职责：订单CRUD、状态流转、费用计算
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.map_client = MapClient()
        self.fee_service = FeeService(db)
    
    async def create_order(self, data: OrderCreate) -> Order:
        """
        创建订单
        
        流程：
        1. 生成订单编号
        2. 地址解析获取经纬度
        3. 创建订单主记录
        4. 创建商品明细
        5. 自动计算费用
        6. 记录创建日志
        
        异常：
        - AddressParseException: 地址解析失败
        - DuplicateOrderException: 订单号重复
        
        返回：Order对象
        """
        # 1. 生成订单编号 (格式: SO20260312000001)
        order_no = generate_order_no()
        
        # 2. 地址解析（异步）
        try:
            lat, lng = await self.map_client.geocode(data.address)
        except Exception as e:
            logger.error(f"地址解析失败: {data.address}, {str(e)}")
            lat, lng = None, None  # 失败时允许继续，后续可手动修正
        
        # 3. 创建订单
        order = Order(
            id=generate_uuid(),
            order_no=order_no,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            address=data.address,
            latitude=Decimal(str(lat)) if lat else None,
            longitude=Decimal(str(lng)) if lng else None,
            appointment_time=data.appointment_time,
            status=OrderStatus.PENDING,
            total_amount=Decimal('0'),
            remark=data.remark,
            create_time=datetime.now(),
            update_time=datetime.now()
        )
        
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        
        # 4. 创建商品明细
        for product in data.products:
            order_product = OrderProduct(
                id=generate_uuid(),
                order_id=order.id,
                product_name=product.product_name,
                product_code=product.product_code,
                quantity=product.quantity,
                unit=product.unit
            )
            self.db.add(order_product)
        
        await self.db.commit()
        
        # 5. 自动计算费用
        await self.fee_service.calculate_fees(order.id)
        
        # 6. 记录日志
        await self._log_order_action(
            order.id, 
            'CREATE', 
            '创建订单',
            None
        )
        
        # 7. 刷新订单获取总金额
        await self.db.refresh(order)
        
        return order
    
    async def update_order(self, order_id: str, data: OrderUpdate) -> Order:
        """
        更新订单
        
        约束：
        - 待派单状态可修改所有字段
        - 已派单状态仅允许修改备注
        """
        order = await self.get_order(order_id)
        
        # 状态校验
        if order.status != OrderStatus.PENDING:
            allowed_fields = {'remark'}
            actual_fields = set(data.dict(exclude_unset=True).keys())
            if not actual_fields.issubset(allowed_fields):
                raise BusinessException(
                    f"当前状态{order.status.value}仅允许修改备注"
                )
        
        # 更新字段
        update_data = data.dict(exclude_unset=True)
        
        # 如果地址变化，重新解析
        if 'address' in update_data and update_data['address'] != order.address:
            try:
                lat, lng = await self.map_client.geocode(update_data['address'])
                update_data['latitude'] = Decimal(str(lat)) if lat else None
                update_data['longitude'] = Decimal(str(lng)) if lng else None
            except Exception as e:
                logger.error(f"地址解析失败: {str(e)}")
        
        for field, value in update_data.items():
            setattr(order, field, value)
        
        order.update_time = datetime.now()
        await self.db.commit()
        await self.db.refresh(order)
        
        await self._log_order_action(order_id, 'UPDATE', '更新订单', update_data)
        
        return order
    
    async def cancel_order(self, order_id: str, reason: str, operator_id: str) -> Order:
        """
        取消订单
        
        流程：
        1. 校验订单状态（仅待派单/已派单可取消）
        2. 检查是否有进行中的任务
        3. 取消相关任务
        4. 更新订单状态
        5. 记录取消原因
        """
        order = await self.get_order(order_id)
        
        # 状态校验
        if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise BusinessException(f"订单状态{order.status.value}不允许取消")
        
        # 检查进行中的任务
        in_progress_tasks = await self.task_repo.get_in_progress_tasks(order_id)
        if in_progress_tasks:
            raise BusinessException("存在进行中的任务，无法取消")
        
        # 取消未开始的任务
        pending_tasks = await self.task_repo.get_pending_tasks(order_id)
        for task in pending_tasks:
            task.status = TaskStatus.CANCELLED
            task.remark = f"订单取消: {reason}"
        
        # 更新订单状态
        old_status = order.status
        order.status = OrderStatus.CANCELLED
        order.update_time = datetime.now()
        
        await self.db.commit()
        
        # 记录日志
        await self._log_order_action(
            order_id,
            'CANCEL',
            f'取消订单: {reason}',
            {'old_status': old_status.value, 'new_status': order.status.value}
        )
        
        return order
    
    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        customer_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        size: int = 20
    ) -> dict:
        """
        查询订单列表（分页）
        
        缓存策略：
        - 无筛选条件时缓存5分钟
        - 有筛选条件时不缓存
        """
        cache_key = f"orders:list:{status}:{customer_name}:{start_date}:{end_date}:{page}:{size}"
        
        # 无筛选条件尝试从缓存获取
        if not any([status, customer_name, start_date, end_date]):
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        
        # 查询数据库
        result = await self.order_repo.paginate(
            filters={
                'status': status,
                'customer_name__ilike': f"%{customer_name}%" if customer_name else None,
                'create_time__gte': start_date,
                'create_time__lte': end_date
            },
            order_by=[Order.create_time.desc()],
            page=page,
            size=size
        )
        
        # 缓存结果
        if not any([status, customer_name, start_date, end_date]):
            await redis_client.setex(cache_key, 300, json.dumps(result))
        
        return result
    
    async def get_order(self, order_id: str) -> Order:
        """获取订单详情"""
        order = await self.order_repo.get(order_id)
        if not order:
            raise BusinessException("订单不存在")
        return order
    
    async def batch_import(self, file_path: str) -> dict:
        """
        批量导入订单
        
        流程：
        1. 解析Excel文件
        2. 数据校验
        3. 批量插入
        4. 返回导入结果
        
        异步执行（Celery）
        """
        # 异步任务
        task = batch_import_orders.delay(file_path)
        return {
            "task_id": task.id,
            "status": "processing",
            "message": "批量导入任务已提交，请稍后查询结果"
        }
    
    async def _log_order_action(self, order_id: str, action: str, detail: str, extra: dict):
        """记录订单操作日志"""
        log = OrderLog(
            id=generate_uuid(),
            order_id=order_id,
            action=action,
            detail=detail,
            extra=json.dumps(extra) if extra else None,
            create_time=datetime.now()
        )
        self.db.add(log)
        await self.db.commit()
```

**OrderRepository (订单数据访问)**

```python
class OrderRepository(BaseRepository):
    """
    订单数据访问层
    """
    
    async def get_by_order_no(self, order_no: str) -> Optional[Order]:
        """根据订单号查询"""
        stmt = select(Order).where(Order.order_no == order_no)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_in_progress_tasks(self, order_id: str) -> list[Task]:
        """获取订单进行中的任务"""
        stmt = select(Task).where(
            Task.order_id == order_id,
            Task.status == TaskStatus.IN_PROGRESS
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_pending_tasks(self, order_id: str) -> list[Task]:
        """获取订单待处理任务"""
        stmt = select(Task).where(
            Task.order_id == order_id,
            Task.status == TaskStatus.PENDING
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_statistics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """
        订单统计数据
        
        返回：
        {
            "total_orders": 100,
            "by_status": {
                "pending": 10,
                "assigned": 20,
                "completed": 60,
                "cancelled": 10
            },
            "total_amount": 50000.00,
            "avg_amount": 500.00
        }
        """
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
```

#### 3.1.2 状态流转详细设计

```python
class OrderStateMachine:
    """
    订单状态机
    
    状态流转规则：
    - PENDING -> ASSIGNED (派单)
    - PENDING -> CANCELLED (取消)
    - ASSIGNED -> DELIVERING (配送中)
    - ASSIGNED -> CANCELLED (取消)
    - DELIVERING -> INSTALLING (安装中)
    - DELIVERING -> CANCELLED (取消)
    - INSTALLING -> COMPLETED (完成)
    """
    
    TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.ASSIGNED, OrderStatus.CANCELLED],
        OrderStatus.ASSIGNED: [OrderStatus.DELIVERING, OrderStatus.CANCELLED],
        OrderStatus.DELIVERING: [OrderStatus.INSTALLING, OrderStatus.CANCELLED],
        OrderStatus.INSTALLING: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: [],
        OrderStatus.CANCELLED: []
    }
    
    @classmethod
    def can_transition(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        """检查状态是否可以流转"""
        return to_status in cls.TRANSITIONS.get(from_status, [])
    
    @classmethod
    def transition(
        cls,
        order: Order,
        to_status: OrderStatus,
        operator_id: str,
        remark: Optional[str] = None
    ) -> Order:
        """执行状态流转"""
        if not cls.can_transition(order.status, to_status):
            raise BusinessException(
                f"无法从{order.status.value}流转到{to_status.value}"
            )
        
        old_status = order.status
        order.status = to_status
        order.update_time = datetime.now()
        
        # 记录状态变更
        log = OrderStatusLog(
            id=generate_uuid(),
            order_id=order.id,
            from_status=old_status,
            to_status=to_status,
            operator_id=operator_id,
            remark=remark,
            create_time=datetime.now()
        )
        
        return order
```

#### 3.1.3 接口详细设计

**创建订单接口**

- **路径**: `POST /api/v1/orders`
- **认证**: 需要认证
- **请求示例**:
```json
{
  "customer_name": "张三",
  "customer_phone": "13800138000",
  "address": "北京市朝阳区建国路88号",
  "appointment_time": "2026-03-15T10:00:00",
  "products": [
    {
      "product_name": "空调挂机",
      "product_code": "AC-001",
      "quantity": 2,
      "unit": "台"
    }
  ],
  "remark": "请提前电话联系"
}
```

- **响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "order_no": "SO20260312000001",
    "status": "pending",
    "total_amount": 680.00
  },
  "timestamp": 1741768269000
}
```

- **错误示例**:
```json
{
  "code": 400,
  "message": "客户电话格式不正确",
  "data": null,
  "timestamp": 1741768269000
}
```

---

### 3.2 调度排单模块

#### 3.2.1 类设计

```python
class DispatchService:
    """
    调度服务
    职责：智能排单、手动调整、冲突检测
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.worker_repo = WorkerRepository(db)
        self.map_client = MapClient()
    
    async def auto_dispatch(
        self,
        order_ids: list[str],
        task_type: TaskType,
        dispatch_date: date
    ) -> list[dict]:
        """
        智能排单
        
        流程：
        1. 获取待排单订单
        2. 筛选可用执行人员
        3. 为每个订单生成候选执行人员集
        4. 应用排单规则评分
        5. 分配任务给最优执行人员
        6. 检测资源冲突
        7. 生成排单结果
        
        返回：排单结果列表
        """
        results = []
        
        for order_id in order_ids:
            try:
                result = await self._dispatch_single_order(
                    order_id,
                    task_type,
                    dispatch_date
                )
                results.append(result)
            except BusinessException as e:
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
    ) -> dict:
        """单订单排单"""
        # 1. 获取订单
        order_repo = OrderRepository(self.db)
        order = await order_repo.get(order_id)
        if not order:
            raise BusinessException("订单不存在")
        
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
    ) -> list[User]:
        """筛选候选执行人员"""
        workers = await self.worker_repo.get_active_workers_by_role(
            role=self._map_task_to_role(task_type)
        )
        
        candidates = []
        
        for worker in workers:
            # 规则1: 区域匹配
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
        candidates: list[User],
        order: Order
    ) -> list[dict]:
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
            if worker.latitude and worker.longitude:
                distance = await self._calculate_distance(
                    float(worker.latitude),
                    float(worker.longitude),
                    float(order.latitude) if order.latitude else 0,
                    float(order.longitude) if order.longitude else 0
                )
                distance_score = max(0, 100 - distance)
                score += distance_score * 0.3
                reasons.append(f"距离:{distance:.1f}km")
            else:
                score += 30  # 无位置信息给中等分
                reasons.append("距离:未知")
            
            # 评分3: 历史评价 (权重30%)
            avg_rating = await self.worker_repo.get_avg_rating(worker.id)
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
        import math
        
        R = 6371  # 地球半径（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    async def _match_region(self, worker: User, order: Order) -> bool:
        """区域匹配"""
        if not worker.region_id or not order.address:
            return True  # 无区域信息不限制
        # 简单匹配：地址包含区域名称
        # 实际应用中可以使用更精确的行政区划匹配
        return True
    
    async def _match_skill(self, worker: User, products: list) -> bool:
        """技能匹配"""
        worker_skills = await self.worker_repo.get_worker_skills(worker.id)
        product_codes = [p.product_code for p in products]
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
            task_start = task.start_time
            task_end = task.start_time + timedelta(hours=2)
            
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
        task_no = generate_task_no(task_type)
        
        task = Task(
            id=generate_uuid(),
            task_no=task_no,
            order_id=order.id,
            task_type=task_type,
            assigned_to=worker.id,
            status=TaskStatus.PENDING,
            create_time=datetime.now()
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
        task = await self.task_repo.get(task_id)
        if not task:
            raise BusinessException("任务不存在")
        
        if task.status != TaskStatus.PENDING:
            raise BusinessException("仅待处理任务可调整执行人")
        
        # 记录变更
        old_worker_id = task.assigned_to
        task.assigned_to = new_worker_id
        task.update_time = datetime.now()
        
        # 记录日志
        log = TaskDispatchLog(
            id=generate_uuid(),
            task_id=task.id,
            old_worker_id=old_worker_id,
            new_worker_id=new_worker_id,
            operator_id=operator_id,
            reason=reason,
            create_time=datetime.now()
        )
        self.db.add(log)
        
        await self.db.commit()
        await self.db.refresh(task)
        
        return task
```

---

### 3.3 任务管理模块

#### 3.3.1 类设计

```python
class TaskService:
    """
    任务服务
    职责：任务执行、状态更新、照片上传
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repo = TaskRepository(db)
    
    async def start_task(
        self,
        task_id: str,
        location: LocationUpdate,
        worker_id: str
    ) -> Task:
        """
        开始任务（位置打卡）
        
        流程：
        1. 校验任务归属
        2. 检查任务状态
        3. 记录开始时间
        4. 记录位置
        5. 创建执行记录
        """
        task = await self.task_repo.get_with_auth(task_id, worker_id)
        
        if task.status != TaskStatus.PENDING:
            raise BusinessException(f"任务状态{task.status.value}不允许开始")
        
        # 更新任务
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = datetime.now()
        task.update_time = datetime.now()
        
        # 创建执行记录
        record = TaskRecord(
            id=generate_uuid(),
            task_id=task.id,
            record_type='start',
            location_lat=Decimal(str(location.latitude)),
            location_lng=Decimal(str(location.longitude)),
            create_time=datetime.now()
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
        """
        完成任务
        
        流程：
        1. 校验任务归属
        2. 检查任务状态
        3. 处理照片上传
        4. 更新任务状态
        5. 触发后续流程
        """
        task = await self.task_repo.get_with_auth(task_id, worker_id)
        
        if task.status != TaskStatus.IN_PROGRESS:
            raise BusinessException(f"任务状态{task.status.value}不允许完成")
        
        # 处理照片
        for photo_url in data.photos:
            attachment = Attachment(
                id=generate_uuid(),
                task_id=task.id,
                file_name=photo_url.split('/')[-1],
                file_url=photo_url,
                upload_by=worker_id,
                create_time=datetime.now()
            )
            self.db.add(attachment)
            
            # 异步压缩图片
            compress_image.delay(photo_url)
        
        # 更新任务
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.now()
        task.remark = data.remark
        task.update_time = datetime.now()
        
        # 创建完成记录
        record = TaskRecord(
            id=generate_uuid(),
            task_id=task.id,
            record_type='complete',
            content=data.remark,
            create_time=datetime.now()
        )
        self.db.add(record)
        
        await self.db.commit()
        await self.db.refresh(task)
        
        # 触发后续流程
        await self._trigger_next_step(task)
        
        return task
    
    async def _trigger_next_step(self, task: Task) -> None:
        """
        触发后续流程
        
        规则：
        - 卸货完成 -> 创建配送任务
        - 配送完成 -> 创建安装任务
        - 安装完成 -> 更新订单状态为已完成
        """
        order = await self.order_repo.get(task.order_id)
        
        if task.task_type == TaskType.UNLOAD:
            # 卸货完成，创建配送任务
            await self._create_next_task(order, TaskType.DELIVERY)
        
        elif task.task_type == TaskType.DELIVERY:
            # 配送完成，创建安装任务
            await self._create_next_task(order, TaskType.INSTALL)
        
        elif task.task_type == TaskType.INSTALL:
            # 安装完成，订单完成
            OrderStateMachine.transition(
                order,
                OrderStatus.COMPLETED,
                'system',
                '安装完成自动完成订单'
            )
            await self.db.commit()
    
    async def _create_next_task(
        self,
        order: Order,
        task_type: TaskType
    ) -> Task:
        """创建下一个任务"""
        dispatch_service = DispatchService(self.db)
        
        # 智能分配
        result = await dispatch_service._dispatch_single_order(
            order.id,
            task_type,
            date.today()
        )
        
        if not result.get('success'):
            # 智能分配失败，记录日志但不阻断流程
            logger.warning(f"自动创建{task_type}任务失败: {result.get('reason')}")
            return None
        
        # 更新订单状态
        if task_type == TaskType.DELIVERY:
            OrderStateMachine.transition(
                order,
                OrderStatus.DELIVERING,
                'system',
                '配送任务创建'
            )
        elif task_type == TaskType.INSTALL:
            OrderStateMachine.transition(
                order,
                OrderStatus.INSTALLING,
                'system',
                '安装任务创建'
            )
        
        await self.db.commit()
        
        return await self.task_repo.get(result['task_id'])
    
    async def get_my_tasks(
        self,
        worker_id: str,
        task_type: Optional[TaskType] = None,
        date: Optional[date] = None
    ) -> list[dict]:
        """
        获取我的任务列表
        
        返回格式化后的任务列表，包含订单信息
        """
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
                        "quantity": p.quantity,
                        "unit": p.unit
                    }
                    for p in task.order.products
                ]
            })
        
        return result
```

---

### 3.4 费用管理模块

#### 3.4.1 费用计算规则引擎

```python
class FeeService:
    """
    费用服务
    职责：费用计算、费用调整、费用审核
    """
    
    # 费率配置（可从数据库读取）
    RATE_CONFIG = {
        "delivery": {
            "base_fee": Decimal("20.00"),
            "per_km_rate": Decimal("5.00"),
            "per_weight_rate": Decimal("0.10"),  # 每公斤
            "per_volume_rate": Decimal("0.05")   # 每立方米
        },
        "install": {
            "rates": {  # 商品编码 -> 安装费率
                "AC-001": Decimal("150.00"),  # 空调
                "FURN-001": Decimal("200.00"), # 家具
                "DEFAULT": Decimal("100.00")   # 默认
            }
        },
        "unload": {
            "per_item_rate": Decimal("5.00"),
            "per_weight_rate": Decimal("0.20")
        }
    }
    
    async def calculate_fees(self, order_id: str) -> list[Fee]:
        """
        计算订单费用
        
        流程：
        1. 获取订单信息
        2. 计算配送费
        3. 计算安装费
        4. 计算卸货费
        5. 汇总总金额
        6. 更新订单
        """
        order_repo = OrderRepository(self.db)
        order = await order_repo.get(order_id)
        
        fees = []
        
        # 1. 配送费
        delivery_fee = await self._calculate_delivery_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.DELIVERY,
            amount=delivery_fee,
            description="配送费",
            status=FeeStatus.CALCULATED,
            create_time=datetime.now()
        ))
        
        # 2. 安装费
        install_fee = await self._calculate_install_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.INSTALL,
            amount=install_fee,
            description="安装费",
            status=FeeStatus.CALCULATED,
            create_time=datetime.now()
        ))
        
        # 3. 卸货费
        unload_fee = await self._calculate_unload_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.UNLOAD,
            amount=unload_fee,
            description="卸货费",
            status=FeeStatus.CALCULATED,
            create_time=datetime.now()
        ))
        
        # 批量保存
        for fee in fees:
            self.db.add(fee)
        
        # 更新订单总金额
        total_amount = sum(f.amount for f in fees)
        order.total_amount = total_amount
        order.update_time = datetime.now()
        
        await self.db.commit()
        
        return fees
    
    async def _calculate_delivery_fee(self, order: Order) -> Decimal:
        """
        计算配送费
        
        方案：
        - 基础费 + 距离费
        - 如果有实际距离数据，使用实际距离
        - 否则使用预估距离
        """
        config = self.RATE_CONFIG["delivery"]
        
        # 获取任务信息
        task_repo = TaskRepository(self.db)
        delivery_task = await task_repo.get_delivery_task(order.id)
        
        if delivery_task and delivery_task.actual_distance:
            distance = delivery_task.actual_distance
        else:
            # 使用地图API估算距离
            distance = await self._estimate_distance(order)
        
        # 计算：基础费 + 距离 * 单价
        fee = config["base_fee"] + Decimal(str(distance)) * config["per_km_rate"]
        
        return fee.quantize(Decimal("0.01"))
    
    async def _calculate_install_fee(self, order: Order) -> Decimal:
        """
        计算安装费
        
        方案：
        - 根据商品类型使用不同费率
        - 安装费 = 商品数量 × 单品安装费
        """
        config = self.RATE_CONFIG["install"]
        total = Decimal("0")
        
        for product in order.products:
            # 获取商品安装费率
            rate = config["rates"].get(
                product.product_code,
                config["rates"]["DEFAULT"]
            )
            
            # 计算
            fee = Decimal(str(product.quantity)) * rate
            total += fee
        
        return total.quantize(Decimal("0.01"))
    
    async def _calculate_unload_fee(self, order: Order) -> Decimal:
        """
        计算卸货费
        
        方案：
        - 按商品数量计算
        """
        config = self.RATE_CONFIG["unload"]
        
        # 计算总数量
        total_quantity = sum(p.quantity for p in order.products)
        
        fee = Decimal(str(total_quantity)) * config["per_item_rate"]
        
        return fee.quantize(Decimal("0.01"))
    
    async def _estimate_distance(self, order: Order) -> float:
        """估算距离"""
        if not order.latitude or not order.longitude:
            # 无位置信息，使用默认10公里
            return 10.0
        
        # 获取仓库坐标
        warehouse_lat = 39.9042  # 示例：北京
        warehouse_lng = 116.4074
        
        # 计算距离
        from app.services.dispatch_service import DispatchService
        distance = await DispatchService._calculate_distance(
            warehouse_lat,
            warehouse_lng,
            float(order.latitude),
            float(order.longitude)
        )
        
        return distance
    
    async def adjust_fee(
        self,
        fee_id: str,
        new_amount: Decimal,
        reason: str,
        operator_id: str
    ) -> Fee:
        """调整费用"""
        fee = await self.db.get(Fee, fee_id)
        if not fee:
            raise BusinessException("费用记录不存在")
        
        old_amount = fee.amount
        fee.amount = new_amount
        fee.status = FeeStatus.ADJUSTED
        fee.description = f"{fee.description} (调整: {reason})"
        fee.update_time = datetime.now()
        
        # 记录调整日志
        log = FeeAdjustLog(
            id=generate_uuid(),
            fee_id=fee_id,
            old_amount=old_amount,
            new_amount=new_amount,
            reason=reason,
            operator_id=operator_id,
            create_time=datetime.now()
        )
        self.db.add(log)
        
        # 更新订单总金额
        order = fee.order
        fees = await self.db.execute(
            select(Fee).where(Fee.order_id == order.id)
        ).scalars().all()
        order.total_amount = sum(f.amount for f in fees)
        
        await self.db.commit()
        await self.db.refresh(fee)
        
        return fee
```

---

### 3.5 报表管理模块

#### 3.5.1 类设计

```python
class ReportService:
    """
    报表服务
    职责：数据统计、报表生成、Excel导出
    """
    
    async def get_order_report(
        self,
        start_date: str,
        end_date: str,
        group_by: str = "day"
    ) -> dict:
        """
        订单报表
        
        参数：
        - start_date: 开始日期 YYYY-MM-DD
        - end_date: 结束日期 YYYY-MM-DD
        - group_by: 分组维度 day/week/month
        
        返回：
        {
            "summary": {
                "total_orders": 1000,
                "completed_orders": 800,
                "total_amount": 500000.00,
                "avg_amount": 500.00
            },
            "trend": [
                {"date": "2026-03-01", "count": 100, "amount": 50000.00},
                ...
            ],
            "by_status": {
                "pending": 50,
                "assigned": 100,
                "completed": 800,
                "cancelled": 50
            }
        }
        """
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        order_repo = OrderRepository(self.db)
        
        # 汇总统计
        summary = await order_repo.get_statistics(start_dt, end_dt)
        
        # 趋势数据
        trend = await self._get_order_trend(start_dt, end_dt, group_by)
        
        return {
            "summary": summary,
            "trend": trend
        }
    
    async def _get_order_trend(
        self,
        start_dt: datetime,
        end_dt: datetime,
        group_by: str
    ) -> list[dict]:
        """获取订单趋势"""
        from sqlalchemy import func, extract
        
        if group_by == "day":
            date_format = func.date(Order.create_time)
        elif group_by == "week":
            date_format = func.concat(
                extract('year', Order.create_time),
                '-W',
                extract('week', Order.create_time)
            )
        else:  # month
            date_format = func.concat(
                extract('year', Order.create_time),
                '-',
                extract('month', Order.create_time)
            )
        
        stmt = select(
            date_format.label('date'),
            func.count(Order.id).label('count'),
            func.sum(Order.total_amount).label('amount')
        ).where(
            Order.create_time.between(start_dt, end_dt),
            Order.status != OrderStatus.CANCELLED
        ).group_by(
            date_format
        ).order_by(
            date_format
        )
        
        result = await self.db.execute(stmt)
        
        return [
            {
                "date": str(row.date),
                "count": row.count,
                "amount": float(row.amount or 0)
            }
            for row in result.all()
        ]
    
    async def get_worker_report(
        self,
        start_date: str,
        end_date: str
    ) -> list[dict]:
        """
        人员工作量报表
        
        返回：
        [
            {
                "worker_id": "xxx",
                "worker_name": "张三",
                "role": "installer",
                "total_tasks": 50,
                "completed_tasks": 48,
                "completion_rate": 96.0,
                "total_amount": 24000.00,
                "avg_rating": 4.8
            },
            ...
        ]
        """
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        # 查询每个人员的任务统计
        stmt = select(
            User.id,
            User.name,
            User.role,
            func.count(Task.id).label('total_tasks'),
            func.sum(case((Task.status == TaskStatus.COMPLETED, 1), else_=0)).label('completed_tasks')
        ).join(
            Task, User.id == Task.assigned_to
        ).where(
            Task.create_time.between(start_dt, end_dt)
        ).group_by(
            User.id
        )
        
        result = await self.db.execute(stmt)
        
        report = []
        for row in result.all():
            total_tasks = row.total_tasks or 0
            completed_tasks = row.completed_tasks or 0
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # 获取评价
            avg_rating = await self.worker_repo.get_avg_rating(row.id)
            
            report.append({
                "worker_id": row.id,
                "worker_name": row.name,
                "role": row.role.value,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": round(completion_rate, 2),
                "avg_rating": avg_rating or 0.0
            })
        
        return report
    
    async def export_report(
        self,
        report_type: str,
        start_date: str,
        end_date: str
    ) -> str:
        """
        导出报表（异步）
        
        返回：下载URL
        """
        # 创建导出任务记录
        export_record = ReportExport(
            id=generate_uuid(),
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            status="generating",
            create_time=datetime.now()
        )
        self.db.add(export_record)
        await self.db.commit()
        
        # 异步生成报表
        generate_report.delay(
            export_record.id,
            report_type,
            start_date,
            end_date
        )
        
        return f"/api/v1/reports/export/{export_record.id}"
```

---

## 四、数据库详细设计

### 4.1 完整表结构

#### 用户表 (users)

```sql
CREATE TABLE `users` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '用户ID',
  `username` VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希(BCrypt)',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `phone` VARCHAR(20) COMMENT '手机号',
  `avatar_url` VARCHAR(500) COMMENT '头像URL',
  `role` ENUM('admin', 'dispatcher', 'driver', 'installer', 'unloader') NOT NULL COMMENT '角色',
  `region_id` VARCHAR(32) COMMENT '所属区域ID',
  `latitude` DECIMAL(10, 7) COMMENT '默认位置-纬度',
  `longitude` DECIMAL(10, 7) COMMENT '默认位置-经度',
  `status` TINYINT DEFAULT 1 COMMENT '状态(1启用 0禁用)',
  `device_token` VARCHAR(500) COMMENT '推送设备Token',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_username` (`username`),
  INDEX `idx_phone` (`phone`),
  INDEX `idx_role` (`role`),
  INDEX `idx_region` (`region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 订单表 (orders)

```sql
CREATE TABLE `orders` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '订单ID',
  `order_no` VARCHAR(32) UNIQUE NOT NULL COMMENT '订单编号',
  `customer_name` VARCHAR(50) NOT NULL COMMENT '客户姓名',
  `customer_phone` VARCHAR(20) NOT NULL COMMENT '客户电话',
  `address` VARCHAR(255) NOT NULL COMMENT '配送地址',
  `latitude` DECIMAL(10, 7) COMMENT '纬度',
  `longitude` DECIMAL(10, 7) COMMENT '经度',
  `appointment_time` DATETIME COMMENT '预约时间',
  `status` ENUM('pending', 'assigned', 'delivering', 'installing', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '订单状态',
  `total_amount` DECIMAL(10, 2) DEFAULT 0.00 COMMENT '总金额',
  `remark` VARCHAR(500) COMMENT '备注',
  `source` ENUM('web', 'import', 'api') DEFAULT 'web' COMMENT '订单来源',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_order_no` (`order_no`),
  INDEX `idx_status` (`status`),
  INDEX `idx_appointment` (`appointment_time`),
  INDEX `idx_create_time` (`create_time`),
  INDEX `idx_customer_phone` (`customer_phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

#### 订单商品表 (order_products)

```sql
CREATE TABLE `order_products` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '主键ID',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单ID',
  `product_name` VARCHAR(100) NOT NULL COMMENT '商品名称',
  `product_code` VARCHAR(50) COMMENT '商品编码',
  `quantity` INT DEFAULT 1 COMMENT '数量',
  `unit` VARCHAR(20) COMMENT '单位',
  `price` DECIMAL(10, 2) COMMENT '商品单价',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  INDEX `idx_order` (`order_id`),
  INDEX `idx_product_code` (`product_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单商品表';
```

#### 任务表 (tasks)

```sql
CREATE TABLE `tasks` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '任务ID',
  `task_no` VARCHAR(32) UNIQUE NOT NULL COMMENT '任务编号',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单ID',
  `task_type` ENUM('unload', 'delivery', 'install') NOT NULL COMMENT '任务类型',
  `assigned_to` VARCHAR(32) COMMENT '执行人ID',
  `status` ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '任务状态',
  `start_time` DATETIME COMMENT '开始时间',
  `end_time` DATETIME COMMENT '完成时间',
  `actual_distance` DECIMAL(10, 2) COMMENT '实际距离(公里)',
  `remark` VARCHAR(500) COMMENT '备注',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`assigned_to`) REFERENCES `users`(`id`),
  INDEX `idx_task_no` (`task_no`),
  INDEX `idx_order` (`order_id`),
  INDEX `idx_assigned` (`assigned_to`),
  INDEX `idx_status` (`status`),
  INDEX `idx_type_status` (`task_type`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务表';
```

#### 任务执行记录表 (task_records)

```sql
CREATE TABLE `task_records` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '记录ID',
  `task_id` VARCHAR(32) NOT NULL COMMENT '任务ID',
  `record_type` ENUM('start', 'complete', 'location', 'exception') NOT NULL COMMENT '记录类型',
  `content` TEXT COMMENT '内容',
  `location_lat` DECIMAL(10, 7) COMMENT '位置-纬度',
  `location_lng` DECIMAL(10, 7) COMMENT '位置-经度',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
  INDEX `idx_task` (`task_id`),
  INDEX `idx_type` (`record_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务执行记录表';
```

#### 附件表 (attachments)

```sql
CREATE TABLE `attachments` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '附件ID',
  `task_id` VARCHAR(32) NOT NULL COMMENT '任务ID',
  `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
  `file_url` VARCHAR(500) NOT NULL COMMENT '文件URL',
  `file_size` INT COMMENT '文件大小(字节)',
  `file_type` VARCHAR(50) COMMENT '文件类型',
  `upload_by` VARCHAR(32) COMMENT '上传人ID',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
  INDEX `idx_task` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='附件表';
```

#### 费用表 (fees)

```sql
CREATE TABLE `fees` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '费用ID',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单ID',
  `fee_type` ENUM('delivery', 'install', 'unload', 'other') NOT NULL COMMENT '费用类型',
  `amount` DECIMAL(10, 2) NOT NULL COMMENT '金额',
  `description` VARCHAR(255) COMMENT '费用说明',
  `status` ENUM('calculated', 'adjusted', 'confirmed') DEFAULT 'calculated' COMMENT '状态',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  INDEX `idx_order` (`order_id`),
  INDEX `idx_type` (`fee_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='费用表';
```

#### 订单日志表 (order_logs)

```sql
CREATE TABLE `order_logs` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '日志ID',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单ID',
  `action` VARCHAR(50) NOT NULL COMMENT '操作类型',
  `detail` VARCHAR(500) COMMENT '详情',
  `operator_id` VARCHAR(32) COMMENT '操作人ID',
  `extra` TEXT COMMENT '额外信息(JSON)',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  INDEX `idx_order` (`order_id`),
  INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单日志表';
```

#### 订单状态变更日志表 (order_status_logs)

```sql
CREATE TABLE `order_status_logs` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '日志ID',
  `order_id` VARCHAR(32) NOT NULL COMMENT '订单ID',
  `from_status` VARCHAR(20) NOT NULL COMMENT '原状态',
  `to_status` VARCHAR(20) NOT NULL COMMENT '新状态',
  `operator_id` VARCHAR(32) COMMENT '操作人ID',
  `remark` VARCHAR(500) COMMENT '备注',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`) ON DELETE CASCADE,
  INDEX `idx_order` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单状态变更日志表';
```

#### 费用调整日志表 (fee_adjust_logs)

```sql
CREATE TABLE `fee_adjust_logs` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '日志ID',
  `fee_id` VARCHAR(32) NOT NULL COMMENT '费用ID',
  `old_amount` DECIMAL(10, 2) NOT NULL COMMENT '原金额',
  `new_amount` DECIMAL(10, 2) NOT NULL COMMENT '新金额',
  `reason` VARCHAR(500) COMMENT '调整原因',
  `operator_id` VARCHAR(32) NOT NULL COMMENT '操作人ID',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`fee_id`) REFERENCES `fees`(`id`) ON DELETE CASCADE,
  INDEX `idx_fee` (`fee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='费用调整日志表';
```

#### 报表导出表 (report_exports)

```sql
CREATE TABLE `report_exports` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '导出ID',
  `report_type` VARCHAR(50) NOT NULL COMMENT '报表类型',
  `start_date` DATE NOT NULL COMMENT '开始日期',
  `end_date` DATE NOT NULL COMMENT '结束日期',
  `status` ENUM('generating', 'completed', 'failed') DEFAULT 'generating' COMMENT '状态',
  `file_url` VARCHAR(500) COMMENT '文件URL',
  `error_message` TEXT COMMENT '错误信息',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `complete_time` DATETIME COMMENT '完成时间',
  INDEX `idx_status` (`status`),
  INDEX `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报表导出表';
```

#### 工人技能表 (worker_skills)

```sql
CREATE TABLE `worker_skills` (
  `id` VARCHAR(32) PRIMARY KEY COMMENT '技能ID',
  `worker_id` VARCHAR(32) NOT NULL COMMENT '工人ID',
  `product_code` VARCHAR(50) NOT NULL COMMENT '商品编码',
  `skill_level` INT DEFAULT 3 COMMENT '技能等级(1-5)',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  UNIQUE KEY `uk_worker_product` (`worker_id`, `product_code`),
  FOREIGN KEY (`worker_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  INDEX `idx_worker` (`worker_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工人技能表';
```

---

### 4.2 索引设计说明

#### 核心索引

| 表名 | 索引名 | 字段 | 类型 | 说明 |
|-----|-------|------|------|------|
| users | idx_username | username | UNIQUE | 登录用 |
| users | idx_phone | phone | INDEX | 手机号查询 |
| users | idx_role | role | INDEX | 角色筛选 |
| orders | idx_order_no | order_no | UNIQUE | 订单号查询 |
| orders | idx_status | status | INDEX | 状态筛选 |
| orders | idx_appointment | appointment_time | INDEX | 预约时间查询 |
| orders | idx_create_time | create_time | INDEX | 时间范围查询 |
| tasks | idx_task_no | task_no | UNIQUE | 任务号查询 |
| tasks | idx_order | order_id | INDEX | 订单关联查询 |
| tasks | idx_assigned | assigned_to | INDEX | 工人任务查询 |
| tasks | idx_status | status | INDEX | 状态筛选 |
| tasks | idx_type_status | task_type, status | COMPOSITE | 任务类型+状态 |

#### 复合索引策略

1. **orders表**:
   - `(status, create_time)`: 用于订单列表查询（按状态筛选+按创建时间排序）
   
2. **tasks表**:
   - `(assigned_to, status, create_time)`: 用于我的任务列表查询
   - `(task_type, status)`: 用于任务统计

---

### 4.3 数据分区策略（可选）

对于大数据量场景，可对订单表进行分区：

```sql
-- 按月份分区
ALTER TABLE orders PARTITION BY RANGE (TO_DAYS(create_time)) (
    PARTITION p202601 VALUES LESS THAN (TO_DAYS('2026-02-01')),
    PARTITION p202602 VALUES LESS THAN (TO_DAYS('2026-03-01')),
    PARTITION p202603 VALUES LESS THAN (TO_DAYS('2026-04-01')),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

---

## 五、接口详细设计

### 5.1 接口规范

#### 认证方式

所有需要认证的接口，请求头需携带：

```
Authorization: Bearer {JWT_TOKEN}
```

#### 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1741768269000
}
```

#### 错误码定义

```python
# app/constants/error_codes.py
ERROR_CODES = {
    # 通用错误 1000-1999
    1000: "系统错误",
    1001: "参数错误",
    1002: "请求方法不支持",
    1003: "请求频率超限",
    
    # 认证授权 2000-2999
    2000: "未登录",
    2001: "Token无效",
    2002: "Token已过期",
    2003: "权限不足",
    
    # 订单相关 3000-3999
    3000: "订单不存在",
    3001: "订单状态不允许此操作",
    3002: "订单已取消",
    3003: "订单已完成",
    
    # 任务相关 4000-4999
    4000: "任务不存在",
    4001: "任务状态不允许此操作",
    4002: "无可用执行人员",
    
    # 业务错误 5000-5999
    5000: "地址解析失败",
    5001: "库存不足",
    5002: "余额不足",
}
```

### 5.2 核心接口详情

#### 订单接口

**1. 创建订单**

```yaml
POST /api/v1/orders
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "customer_name": "张三",
  "customer_phone": "13800138000",
  "address": "北京市朝阳区建国路88号",
  "appointment_time": "2026-03-15T10:00:00",
  "products": [
    {
      "product_name": "空调挂机",
      "product_code": "AC-001",
      "quantity": 2,
      "unit": "台"
    }
  ],
  "remark": "请提前电话联系"
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "order_no": "SO20260312000001",
    "status": "pending",
    "total_amount": 680.00
  },
  "timestamp": 1741768269000
}

Response 400:
{
  "code": 1001,
  "message": "客户电话格式不正确",
  "data": null,
  "timestamp": 1741768269000
}
```

**2. 查询订单列表**

```yaml
GET /api/v1/orders?status=pending&page=1&size=20
Authorization: Bearer {token}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "page": 1,
    "size": 20,
    "items": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "order_no": "SO20260312000001",
        "customer_name": "张三",
        "customer_phone": "13800138000",
        "address": "北京市朝阳区建国路88号",
        "status": "pending",
        "total_amount": 680.00,
        "appointment_time": "2026-03-15T10:00:00",
        "create_time": "2026-03-12T10:00:00"
      }
    ]
  },
  "timestamp": 1741768269000
}
```

**3. 取消订单**

```yaml
POST /api/v1/orders/{order_id}/cancel
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "reason": "客户取消"
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "cancelled"
  },
  "timestamp": 1741768269000
}
```

#### 调度接口

**1. 智能排单**

```yaml
POST /api/v1/dispatch/auto
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "order_ids": ["order1", "order2", "order3"],
  "task_type": "delivery",
  "dispatch_date": "2026-03-15"
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "order_id": "order1",
      "success": true,
      "task_id": "task1",
      "task_no": "DT20260315000001",
      "worker_name": "李四",
      "worker_phone": "13900139000",
      "score": 85.5,
      "score_details": ["今日任务:3", "距离:5.2km", "评分:4.8"]
    },
    {
      "order_id": "order2",
      "success": false,
      "reason": "无可用执行人员"
    }
  ],
  "timestamp": 1741768269000
}
```

**2. 手动调整**

```yaml
POST /api/v1/dispatch/manual
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "task_id": "task1",
  "new_worker_id": "worker2",
  "reason": "原工人请假"
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "task1",
    "assigned_to": "worker2"
  },
  "timestamp": 1741768269000
}
```

#### 任务接口（H5端）

**1. 我的任务列表**

```yaml
GET /api/v1/tasks/my-tasks?task_type=delivery&date=2026-03-15
Authorization: Bearer {token}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "task_id": "task1",
      "task_no": "DT20260315000001",
      "task_type": "delivery",
      "status": "pending",
      "order": {
        "order_no": "SO20260312000001",
        "customer_name": "张三",
        "customer_phone": "13800138000",
        "address": "北京市朝阳区建国路88号",
        "appointment_time": "2026-03-15T10:00:00"
      },
      "products": [
        {
          "product_name": "空调挂机",
          "quantity": 2,
          "unit": "台"
        }
      ]
    }
  ],
  "timestamp": 1741768269000
}
```

**2. 开始任务**

```yaml
POST /api/v1/tasks/{task_id}/start
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "latitude": 39.9042,
  "longitude": 116.4074
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "task1",
    "status": "in_progress",
    "start_time": "2026-03-15T09:55:00"
  },
  "timestamp": 1741768269000
}
```

**3. 完成任务**

```yaml
POST /api/v1/tasks/{task_id}/complete
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "photos": [
    "https://oss.example.com/photo1.jpg",
    "https://oss.example.com/photo2.jpg"
  ],
  "remark": "已签收"
}

Response 200:
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "task1",
    "status": "completed",
    "end_time": "2026-03-15T10:30:00"
  },
  "timestamp": 1741768269000
}
```

---

## 六、异常处理与日志设计

### 6.1 自定义异常体系

```python
# app/exceptions/base.py
class BaseException(Exception):
    """基础异常"""
    code: int = 1000
    message: str = "系统错误"
    
    def __init__(self, message: str = None, code: int = None):
        if message:
            self.message = message
        if code:
            self.code = code
        super().__init__(self.message)

# app/exceptions/business.py
class BusinessException(BaseException):
    """业务异常"""
    code: int = 5000

class OrderNotFoundException(BusinessException):
    code: int = 3000
    message: str = "订单不存在"

class OrderStatusException(BusinessException):
    code: int = 3001
    message: str = "订单状态不允许此操作"

class TaskNotFoundException(BusinessException):
    code: int = 4000
    message: str = "任务不存在"

class NoWorkerAvailableException(BusinessException):
    code: int = 4002
    message: str = "无可用执行人员"
```

### 6.2 全局异常处理中间件

```python
# app/middleware/error_handler.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.exceptions.base import BaseException
from app.exceptions.business import BusinessException
import traceback
import logging

logger = logging.getLogger(__name__)

async def exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    
    # 业务异常
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None,
                "timestamp": int(time.time() * 1000)
            }
        )
    
    # 基础异常
    if isinstance(exc, BaseException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": None,
                "timestamp": int(time.time() * 1000)
            }
        )
    
    # 未捕获异常
    logger.error(f"未捕获异常: {str(exc)}\n{traceback.format_exc()}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 1000,
            "message": "系统错误",
            "data": None,
            "timestamp": int(time.time() * 1000)
        }
    )
```

### 6.3 日志配置

```python
# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """配置日志"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 应用日志
    app_handler = RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    app_handler.setFormatter(formatter)
    
    # 错误日志
    error_handler = RotatingFileHandler(
        f"{log_dir}/error.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    
    # 访问日志
    access_handler = RotatingFileHandler(
        f"{log_dir}/access.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    access_handler.setFormatter(formatter)
    
    return app_handler, error_handler, access_handler
```

---

## 七、性能优化方案

### 7.1 数据库优化

#### 7.1.1 查询优化

```python
# 使用selectinload避免N+1查询
from sqlalchemy.orm import selectinload

stmt = select(Order).options(
    selectinload(Order.products),
    selectinload(Order.tasks).selectinload(Task.assigned_worker)
).where(Order.status == OrderStatus.PENDING)

result = await self.db.execute(stmt)
orders = result.scalars().all()
```

#### 7.1.2 分页优化

```python
# 使用游标分页（大数据量场景）
async def get_orders_cursor(
    self,
    cursor: Optional[str] = None,
    limit: int = 20
) -> dict:
    """游标分页"""
    stmt = select(Order)
    
    if cursor:
        # cursor是order_id，使用它作为起始点
        stmt = stmt.where(Order.id > cursor)
    
    stmt = stmt.order_by(Order.id).limit(limit)
    
    result = await self.db.execute(stmt)
    orders = result.scalars().all()
    
    next_cursor = orders[-1].id if orders else None
    
    return {
        "items": orders,
        "next_cursor": next_cursor,
        "has_more": len(orders) == limit
    }
```

### 7.2 缓存策略

#### 7.2.1 Redis缓存设计

```python
# app/utils/cache.py
import redis
import json
from functools import wraps
from typing import Optional

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def cache(ttl: int = 300, prefix: str = ""):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存key
            key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            redis_client.setex(key, ttl, json.dumps(result, default=str))
            
            return result
        return wrapper
    return decorator

# 使用示例
@cache(ttl=300, prefix="orders")
async def get_orders(self, status: str = None):
    """订单列表缓存"""
    ...
```

#### 7.2.2 缓存失效策略

```python
class CacheInvalidator:
    """缓存失效管理"""
    
    @staticmethod
    def invalidate_order(order_id: str):
        """订单相关缓存失效"""
        patterns = [
            f"orders:get_order:{order_id}",
            f"orders:list:*",
            f"reports:order:*"
        ]
        
        for pattern in patterns:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
    
    @staticmethod
    def invalidate_task(task_id: str):
        """任务相关缓存失效"""
        patterns = [
            f"tasks:get_task:{task_id}",
            f"tasks:my_tasks:*",
            f"orders:get_order:*"
        ]
        
        for pattern in patterns:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
```

### 7.3 异步任务优化

#### 7.3.1 Celery配置优化

```python
# app/tasks/celery_app.py
from celery import Celery
import os

celery_app = Celery(
    "saas_warehouse",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/1"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/1")
)

# 任务预取（避免worker饥饿）
celery_app.conf.task_prefetch_multiplier = 1

# 任务结果过期时间
celery_app.conf.result_expires = 3600

# 任务时间限制
celery_app.conf.task_time_limit = 600  # 10分钟
celery_app.conf.task_soft_time_limit = 540  # 9分钟

# 任务路由
celery_app.conf.task_routes = {
    'app.tasks.image_tasks.compress_image': {'queue': 'image'},
    'app.tasks.report_tasks.generate_report': {'queue': 'report'},
    'app.tasks.notify_tasks.*': {'queue': 'notify'},
}
```

---

## 八、安全设计实现

### 8.1 认证授权详细实现

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """密码加密"""
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:
    """创建JWT Token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """解码JWT Token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

### 8.2 权限控制装饰器

```python
# app/core/permissions.py
from functools import wraps
from fastapi import HTTPException, status
from app.models.user import UserRole, User
from typing import List

def require_role(*roles: List[UserRole]):
    """角色权限检查"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User, **kwargs):
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

def require_resource_owner(resource_type: str = "order"):
    """资源归属检查"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User, resource_id: str, **kwargs):
            # 检查资源归属
            # 管理员和调度员可以查看所有
            if current_user.role in [UserRole.ADMIN, UserRole.DISPATCHER]:
                return await func(*args, current_user=current_user, resource_id=resource_id, **kwargs)
            
            # 其他角色只能查看自己的
            # 需要根据实际业务实现
            return await func(*args, current_user=current_user, resource_id=resource_id, **kwargs)
        return wrapper
    return decorator
```

### 8.3 数据加密

```python
# app/utils/encryption.py
from cryptography.fernet import Fernet
import base64

class Encryption:
    """数据加密"""
    
    @staticmethod
    def generate_key() -> str:
        """生成密钥"""
        return Fernet.generate_key().decode()
    
    @staticmethod
    def encrypt(plain_text: str, key: str) -> str:
        """加密"""
        f = Fernet(key.encode())
        encrypted = f.encrypt(plain_text.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt(cipher_text: str, key: str) -> str:
        """解密"""
        f = Fernet(key.encode())
        decrypted = f.decrypt(cipher_text.encode())
        return decrypted.decode()
```

---

## 九、部署配置详解

### 9.1 Docker配置

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  # FastAPI应用
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://root:password@mysql:3306/saas_warehouse
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=your-secret-key-change-in-production
    depends_on:
      - mysql
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Celery Worker
  celery-worker:
    build: .
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=2
    environment:
      - DATABASE_URL=mysql+aiomysql://root:password@mysql:3306/saas_warehouse
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    restart: unless-stopped

  # MySQL
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=saas_warehouse
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7.0
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

### 9.2 Nginx配置

```nginx
# nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss;

    # 限流
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    upstream app {
        server app:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # HTTP重定向到HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL配置
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # API限流
        limit_req zone=api burst=20 nodelay;

        location /api/ {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 静态文件
        location /static/ {
            alias /app/static/;
            expires 30d;
        }
    }
}
```

---

## 十、开发实施计划

### 10.1 开发阶段划分

| 阶段 | 时间 | 主要任务 | 交付物 |
|-----|------|---------|--------|
| 阶段1：基础框架搭建 | 第1周 | 项目初始化、数据库设计、基础配置 | 项目骨架、数据库表 |
| 阶段2：核心模块开发 | 第2-4周 | 订单、调度、任务模块 | 核心功能API |
| 阶段3：辅助模块开发 | 第5-6周 | 费用、报表、用户权限模块 | 完整后端API |
| 阶段4：前端开发 | 第4-6周 | Web管理端、H5移动端 | 前端代码 |
| 阶段5：集成测试 | 第7周 | 接口联调、功能测试 | 测试报告 |
| 阶段6：部署上线 | 第8周 | 环境部署、数据迁移 | 生产环境 |

### 10.2 里程碑

- **M1**: 基础框架完成（第1周末）
- **M2**: 核心API完成（第4周末）
- **M3**: 前后端集成完成（第6周末）
- **M4**: 测试完成（第7周末）
- **M5**: 正式上线（第8周末）

---

## 十一、附录

### 11.1 依赖列表

```txt
# requirements.txt
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.23
alembic==1.12.1
aiomysql==0.2.0

# 数据验证
pydantic==2.5.0
pydantic-settings==2.1.0

# 认证安全
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==41.0.7

# 缓存
redis==5.0.1

# 异步任务
celery==5.3.4

# HTTP客户端
httpx==0.25.2

# 工具库
python-dateutil==2.8.2
pytz==2023.3

# 日志
loguru==0.7.2

# 测试
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# 代码质量
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

### 11.2 环境变量配置

```bash
# .env.example

# 数据库配置
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/saas_warehouse

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=120

# 高德地图配置
AMAP_API_KEY=your-amap-api-key

# 阿里云OSS配置
OSS_ACCESS_KEY_ID=your-access-key-id
OSS_ACCESS_KEY_SECRET=your-access-key-secret
OSS_BUCKET_NAME=your-bucket-name
OSS_ENDPOINT=https://oss-cn-beijing.aliyuncs.com

# Celery配置
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# 短信配置
SMS_ACCESS_KEY_ID=your-sms-access-key
SMS_ACCESS_KEY_SECRET=your-sms-secret
SMS_SIGN_NAME=your-sign-name
SMS_TEMPLATE_CODE=SMS_TEMPLATE_CODE

# 应用配置
APP_NAME=仓配装一体系统
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO
```

### 11.3 数据库初始化脚本

```sql
-- init.sql

-- 创建数据库
CREATE DATABASE IF NOT EXISTS saas_warehouse DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE saas_warehouse;

-- 创建初始管理员用户
INSERT INTO users (id, username, password_hash, name, role, status) 
VALUES (
    'admin-001',
    'admin',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 密码: admin123
    '系统管理员',
    'admin',
    1
);

-- 创建初始区域数据
INSERT INTO regions (id, region_name, region_code) VALUES
('region-001', '朝阳区', 'CY'),
('region-002', '海淀区', 'HD'),
('region-003', '丰台区', 'FT');

-- 创建初始工人技能
INSERT INTO worker_skills (id, worker_id, product_code, skill_level)
SELECT 
    CONCAT('skill-', uuid()) as id,
    'worker-001' as worker_id,
    'AC-001' as product_code,
    5 as skill_level;
```

---

## 文档变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| v3.0 | 2026-03-12 | 初始版本，基于需求和概要设计创建详细设计 | - |

---

## 总结

本详细设计文档在需求文档和概要设计文档的基础上，进一步细化到：

1. **类设计**：每个核心模块的类、方法、参数、返回值
2. **数据库设计**：完整的表结构、索引、约束、ER图
3. **接口设计**：详细的API规范、请求/响应示例、错误码
4. **异常处理**：自定义异常体系、全局异常处理、日志配置
5. **性能优化**：查询优化、缓存策略、异步任务优化
6. **安全设计**：认证授权、权限控制、数据加密
7. **部署配置**：Docker配置、Nginx配置、环境变量

本文档可作为开发人员的详细编码指南，确保系统开发的一致性和质量。
