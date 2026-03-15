# 仓配装一体系统概要设计文档

## 文档信息
- **项目名称**: 仓配装一体系统
- **文档版本**: v2.0 (Python版)
- **创建日期**: 2026-03-12
- **文档类型**: 概要设计说明书
- **技术栈**: Python FastAPI + Vue3 + MySQL + Redis

---

## 一、设计概述

### 1.1 设计目标
本概要设计基于需求规格说明书，定义系统的整体架构、技术选型、模块划分、接口规范和数据库设计。采用Python技术栈，适配个人开发场景，确保10周内可交付可用系统。

### 1.2 设计原则
- **务实优先**: 单体架构，避免过度设计，快速迭代
- **高内聚低耦合**: 模块职责清晰，易于维护
- **开发效率**: Python生态成熟，代码量少，开发快
- **可扩展性**: 预留扩展接口，支持后期拆分为微服务
- **安全性**: 认证授权、数据加密、操作留痕

---

## 二、系统架构设计

### 2.1 整体架构图
```
┌─────────────────────────────────────────────────────────────────┐
│                           客户端层                                │
├──────────────────────────────┬───────────────────────────────────┤
│      Web管理端(PC)           │        H5移动端(三端)              │
│  - Vue3 + Element Plus       │    - Vue3 + Vant                  │
│  - 订单/调度/仓储/费用管理   │    - 卸货端/司机端/安装端         │
└──────────────────────────────┴───────────────────────────────────┘
                                    ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI应用层                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  路由层 (api/v1/)                                        │  │
│  │  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐      │  │
│  │  │orders│tasks │dispatch│warehouse│fees│reports│users │      │  │
│  │  └──────┴──────┴──────┴──────┴──────┴──────┴──────┘      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  服务层 (services/)                                       │  │
│  │  OrderService | TaskService | DispatchService | FeeService│  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  数据层 (models/ + repositories/)                         │  │
│  │  SQLAlchemy ORM + 异步Repository                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                        数据访问层                                │
│          SQLAlchemy ORM + Alembic + Pydantic验证                │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                        数据存储层                                │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   MySQL     │   Redis     │  OSS存储    │   Celery异步任务    │
│  8.0单实例  │  缓存+队列   │  图片/文档  │  图片压缩/报表生成  │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                        第三方服务                                │
│  高德地图API | 阿里云OSS | 短信服务 | 推送服务                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 技术架构选型（Python版）

| 层级 | 技术选型 | 版本 | 选型理由 |
|------|---------|------|---------|
| **Web框架** | FastAPI | 0.104+ | 现代异步框架，性能接近Go，自动API文档 |
| **ORM** | SQLAlchemy | 2.0+ | 成熟稳定，支持复杂查询，异步支持好 |
| **数据库迁移** | Alembic | 1.12+ | SQLAlchemy官方迁移工具 |
| **数据验证** | Pydantic | 2.0+ | 类型安全，自动校验，与FastAPI深度集成 |
| **异步任务** | Celery | 5.3+ | 图片压缩、报表生成、消息推送异步化 |
| **缓存** | Redis-py | 5.0+ | 热点数据缓存、分布式锁 |
| **认证** | python-jose | 3.3+ | JWT生成和验证 |
| **密码加密** | passlib | 1.7+ | BCrypt哈希，安全可靠 |
| **HTTP客户端** | httpx | 0.25+ | 异步HTTP请求，调用地图API |
| **数据库驱动** | aiomysql | 0.2.0+ | 异步MySQL驱动 |
| **前端Web** | Vue3 | 3.3+ | 组件化开发，生态成熟 |
| **前端UI** | Element Plus | 2.4+ | 管理后台组件库 |
| **前端H5** | Vue3 + Vant | 4.0+ | 移动端UI组件，三端复用 |
| **部署** | Docker Compose | 2.20+ | 单机部署，简单高效 |

### 2.3 部署架构
```
                        用户
                          ↓
                   Nginx反向代理
                          ↓
              ┌─────────────────────┐
              │   FastAPI应用容器    │  ← Gunicorn + Uvicorn Workers
              │   (4个Worker进程)    │
              └─────────────────────┘
                    ↓        ↓
            ┌──────────┐  ┌──────────┐
            │  MySQL   │  │  Redis   │  ← 单机部署
            │  8.0     │  │  7.0     │
            └──────────┘  └──────────┘
                    ↓
            ┌─────────────────────┐
            │   Celery Worker容器 │  ← 异步任务处理
            │   (2个Worker进程)   │
            └─────────────────────┘
                    ↓
            ┌─────────────────────┐
            │   阿里云OSS         │  ← 图片/文档存储
            └─────────────────────┘
```

---

## 三、模块设计

### 3.1 模块划分

| 模块编号 | 模块名称 | 负责人 | 说明 |
|---------|---------|-------|------|
| M01 | 订单管理模块 | - | 订单CRUD、状态流转、批量导入 |
| M02 | 调度排单模块 | - | 智能排单、手动调整、工单管理 |
| M03 | 仓储管理模块 | - | 库存管理、卸货管理 |
| M04 | 配送管理模块 | - | 配送任务、路线规划、签收管理 |
| M05 | 安装管理模块 | - | 安装任务、验收拍照、材料使用 |
| M06 | 费用管理模块 | - | 费用计算、费用调整、费用审核 |
| M07 | 结算管理模块 | - | 结算状态、收款记录、开票管理 |
| M08 | 报表分析模块 | - | 订单报表、人员报表、费用报表 |
| M09 | 用户权限模块 | - | 用户管理、角色管理、JWT认证 |
| M10 | 系统配置模块 | - | 字典配置、参数配置、日志管理 |
| M11 | 异步任务模块 | - | 图片压缩、报表生成、消息推送 |

### 3.2 核心模块详细设计

#### M01 订单管理模块
**职责**: 负责订单全生命周期管理

**Python核心类结构**:
```python
# app/api/v1/orders.py - 路由层
from fastapi import APIRouter, Depends
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["订单"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    service: OrderService = Depends()
):
    """创建订单"""
    return await service.create_order(data)

@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    status: str = None,
    page: int = 1,
    size: int = 20,
    service: OrderService = Depends()
):
    """查询订单列表"""
    return await service.get_orders(status, page, size)

# app/services/order_service.py - 服务层
class OrderService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_order(self, data: OrderCreate) -> Order:
        """创建订单"""
        # 1. 生成订单编号
        order_no = generate_order_no()
        # 2. 地址解析获取经纬度
        lat, lng = await geocode(data.address)
        # 3. 创建订单记录
        order = Order(
            order_no=order_no,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            address=data.address,
            latitude=lat,
            longitude=lng,
            appointment_time=data.appointment_time,
            status=OrderStatus.PENDING,
            total_amount=0
        )
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        # 4. 创建商品明细
        for product in data.products:
            order_product = OrderProduct(
                order_id=order.id,
                product_name=product.product_name,
                product_code=product.product_code,
                quantity=product.quantity,
                unit=product.unit
            )
            self.db.add(order_product)
        await self.db.commit()
        return order

# app/models/order.py - ORM模型
from sqlalchemy import Column, String, Enum, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"          # 待派单
    ASSIGNED = "assigned"        # 已派单
    DELIVERING = "delivering"    # 配送中
    INSTALLING = "installing"    # 安装中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(32), primary_key=True, index=True)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    customer_name = Column(String(50), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    appointment_time = Column(DateTime)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    total_amount = Column(DECIMAL(10, 2), default=0)
    remark = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    products = relationship("OrderProduct", back_populates="order")
    tasks = relationship("Task", back_populates="order")
```

**关键方法**:
| 方法名 | 说明 | 异步 | 缓存 |
|--------|------|------|------|
| create_order() | 创建订单 | ✅ | ❌ |
| update_order() | 更新订单 | ✅ | ❌ |
| cancel_order() | 取消订单（含业务校验） | ✅ | ❌ |
| get_orders() | 查询订单列表（分页） | ✅ | ✅(5分钟) |
| batch_import() | 批量导入（Celery异步） | ✅ | ❌ |

**状态流转（有限状态机）**:
```python
# app/core/state_machine.py
class OrderStateMachine:
    """订单状态机"""

    TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.ASSIGNED, OrderStatus.CANCELLED],
        OrderStatus.ASSIGNED: [OrderStatus.DELIVERING, OrderStatus.CANCELLED],
        OrderStatus.DELIVERING: [OrderStatus.INSTALLING, OrderStatus.CANCELLED],
        OrderStatus.INSTALLING: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: [],  # 终态
        OrderStatus.CANCELLED: []   # 终态
    }

    @classmethod
    def can_transition(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        """检查状态是否可以流转"""
        return to_status in cls.TRANSITIONS.get(from_status, [])

    @classmethod
    def transition(cls, order: Order, to_status: OrderStatus, operator_id: str):
        """执行状态流转"""
        if not cls.can_transition(order.status, to_status):
            raise ValueError(f"无法从{order.status}流转到{to_status}")

        old_status = order.status
        order.status = to_status
        order.update_time = datetime.now()

        # 记录状态变更日志
        log_status_change(order.id, old_status, to_status, operator_id)
```

#### M02 调度排单模块
**职责**: 智能分配任务给执行人员

**Python核心类结构**:
```python
# app/services/dispatch_service.py
class DispatchService:
    """调度服务"""

    async def auto_dispatch(
        self,
        order_ids: list[str],
        task_type: TaskType,
        dispatch_date: date
    ) -> DispatchResult:
        """
        智能排单
        1. 获取待排单订单
        2. 筛选可用执行人员
        3. 应用排单规则评分
        4. 分配任务
        5. 检测资源冲突
        """
        # 1. 获取订单
        orders = await self._get_pending_orders(order_ids)

        results = []
        for order in orders:
            # 2. 筛选候选执行人员
            candidates = await self._filter_candidates(
                order=order,
                task_type=task_type,
                dispatch_date=dispatch_date
            )

            if not candidates:
                results.append({
                    "order_id": order.id,
                    "success": False,
                    "reason": "无可用执行人员"
                })
                continue

            # 3. 评分排序
            scored_candidates = await self._score_candidates(
                candidates=candidates,
                order=order
            )

            best_worker = scored_candidates[0]["worker"]

            # 4. 创建任务
            task = await self._create_task(
                order=order,
                worker=best_worker,
                task_type=task_type
            )

            results.append({
                "order_id": order.id,
                "success": True,
                "task_id": task.id,
                "worker_name": best_worker.name
            })

        return results

    async def _filter_candidates(
        self,
        order: Order,
        task_type: TaskType,
        dispatch_date: date
    ) -> list[Worker]:
        """筛选候选执行人员"""
        workers = await self.worker_repo.get_active_workers()

        # 规则1: 区域匹配
        workers = [w for w in workers if self._match_region(w, order)]

        # 规则2: 技能匹配
        if task_type == TaskType.INSTALL:
            workers = [w for w in workers if self._match_skill(w, order.products)]

        # 规则3: 时间可用
        workers = [w for w in workers if await self._check_time_available(w, dispatch_date)]

        return workers

    async def _score_candidates(
        self,
        candidates: list[Worker],
        order: Order
    ) -> list[dict]:
        """为候选人评分"""
        scored = []
        for worker in candidates:
            score = 0
            reasons = []

            # 评分1: 工作量均衡 (权重40%)
            task_count = await self.task_repo.count_today_tasks(worker.id)
            workload_score = max(0, 100 - task_count * 10)
            score += workload_score * 0.4
            reasons.append(f"工作量:{task_count}")

            # 评分2: 距离 (权重30%)
            distance = await self._calculate_distance(worker, order)
            distance_score = max(0, 100 - distance)
            score += distance_score * 0.3
            reasons.append(f"距离:{distance:.1f}km")

            # 评分3: 历史评价 (权重30%)
            rating = await self.worker_repo.get_avg_rating(worker.id)
            rating_score = rating * 20  # 5分制 → 100分
            score += rating_score * 0.3
            reasons.append(f"评分:{rating}")

            scored.append({
                "worker": worker,
                "score": score,
                "reasons": reasons
            })

        # 按分数降序排序
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored
```

**排单规则配置化**:
```python
# app/models/dispatch_rule.py
class DispatchRule(Base):
    """排单规则"""
    __tablename__ = "dispatch_rules"

    id = Column(String(32), primary_key=True)
    rule_name = Column(String(50), nullable=False)
    rule_type = Column(Enum(RuleType), nullable=False)  # region/skill/time/workload
    weight = Column(Integer, default=10)  # 权重
    is_enabled = Column(Boolean, default=True)
    config = Column(JSON)  # 规则配置

# 规则配置示例
REGION_RULE_CONFIG = {
    "regions": ["朝阳区", "海淀区"],
    "worker_regions": {
        "W001": ["朝阳区"],
        "W002": ["海淀区"]
    }
}
```

#### M04 配送管理模块 + M05 安装管理模块
**职责**: 任务执行管理，支持H5端操作

**Python核心类结构**:
```python
# app/api/v1/tasks.py
@router.post("/{task_id}/start")
async def start_task(
    task_id: str,
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """开始任务（带位置打卡）"""
    return await service.start_task(task_id, location, current_user.id)

@router.post("/{task_id}/complete")
async def complete_task(
    task_id: str,
    data: TaskCompleteRequest,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """完成任务（上传照片）"""
    # 异步处理图片压缩
    task = await service.complete_task(task_id, data, current_user.id)
    # 触发后续流程
    await service.trigger_next_step(task)
    return task

# app/services/task_service.py
class TaskService:
    async def complete_task(
        self,
        task_id: str,
        data: TaskCompleteRequest,
        operator_id: str
    ) -> Task:
        """完成任务"""
        task = await self.get_task(task_id)

        # 1. 校验任务状态
        if task.status != TaskStatus.IN_PROGRESS:
            raise ValueError("任务不在进行中")

        # 2. 处理附件上传
        for file_url in data.photos:
            # 异步压缩图片
            compress_image.delay(file_url)  # Celery异步

            attachment = Attachment(
                task_id=task.id,
                file_name=file_url.split("/")[-1],
                file_url=file_url,
                upload_by=operator_id
            )
            self.db.add(attachment)

        # 3. 更新任务状态
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.now()
        task.remark = data.remark

        await self.db.commit()
        await self.db.refresh(task)

        # 4. 记录完成日志
        await self._log_completion(task, operator_id)

        return task
```

#### M06 费用管理模块
**职责**: 费用计算与调整

**Python核心类结构**:
```python
# app/services/fee_service.py
class FeeService:
    """费用服务"""

    async def calculate_fees(self, order_id: str) -> list[Fee]:
        """计算订单费用"""
        order = await self.order_repo.get(order_id)

        fees = []

        # 1. 配送费计算
        delivery_fee = await self._calculate_delivery_fee(order)
        fees.append(Fee(
            order_id=order_id,
            fee_type=FeeType.DELIVERY,
            amount=delivery_fee,
            status=FeeStatus.CALCULATED
        ))

        # 2. 安装费计算
        install_fee = await self._calculate_install_fee(order)
        fees.append(Fee(
            order_id=order_id,
            fee_type=FeeType.INSTALL,
            amount=install_fee,
            status=FeeStatus.CALCULATED
        ))

        # 3. 卸货费计算
        unload_fee = await self._calculate_unload_fee(order)
        fees.append(Fee(
            order_id=order_id,
            fee_type=FeeType.UNLOAD,
            amount=unload_fee,
            status=FeeStatus.CALCULATED
        ))

        # 4. 更新订单总金额
        total = sum(f.amount for f in fees)
        order.total_amount = total
        await self.db.commit()

        return fees

    async def _calculate_delivery_fee(self, order: Order) -> Decimal:
        """配送费计算逻辑"""
        # 方案1: 按距离计算
        # 调用高德路线规划API获取实际距离
        distance = await self._get_distance_by_api(order)

        # 费率: 5元/公里，起步价20元
        base_fee = Decimal("20")
        rate = Decimal("5")
        fee = base_fee + distance * rate
        return fee.quantize(Decimal("0.01"))

    async def _calculate_install_fee(self, order: Order) -> Decimal:
        """安装费计算逻辑"""
        total = Decimal("0")

        for product in order.products:
            # 根据商品类型获取安装费率
            fee_rate = await self._get_install_fee_rate(product.product_code)

            # 安装费 = 商品单价 × 数量 × 费率
            fee = Decimal(str(product.quantity)) * fee_rate
            total += fee

        return total.quantize(Decimal("0.01"))
```

#### M11 异步任务模块（Celery）
**职责**: 处理耗时任务

**Python核心类结构**:
```python
# app/tasks/celery_app.py
from celery import Celery

celery_app = Celery(
    "saas_warehouse",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# app/tasks/image_tasks.py
@celery_app.task
def compress_image(image_url: str):
    """压缩图片"""
    import requests
    from PIL import Image
    from io import BytesIO

    # 下载图片
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # 压缩
    output = BytesIO()
    img.save(output, format="JPEG", quality=80, optimize=True)

    # 上传回OSS
    compressed_url = upload_to_oss(output.getvalue())
    return compressed_url

# app/tasks/report_tasks.py
@celery_app.task
def generate_report(report_id: str, report_type: str):
    """生成报表"""
    # 1. 查询数据
    data = query_report_data(report_type)

    # 2. 生成Excel
    excel_file = generate_excel(data)

    # 3. 上传到OSS
    file_url = upload_to_oss(excel_file)

    # 4. 更新报表状态
    update_report_status(report_id, "completed", file_url)

    return file_url

# app/tasks/notify_tasks.py
@celery_app.task
def send_task_notification(worker_id: str, task_id: str):
    """发送任务通知"""
    worker = get_worker(worker_id)
    # 发送短信
    send_sms(worker.phone, f"您有新的任务: {task_id}")
    # 发送推送
    send_push(worker.device_token, "新任务通知", f"您有新的安装任务")
```

---

## 四、数据库设计

### 4.1 ER关系图
```
┌─────────┐         ┌─────────────┐         ┌─────────────────┐
│  users  │         │    tasks    │         │ task_records    │
└────┬────┘         └──────┬──────┘         └────────┬────────┘
     │ 1:N                 │ 1:N                     │
     │ assigned_to         │ task_id                 │
     ↓                     ↓                         ↓
┌─────────────────┐         ┌─────────────┐         ┌─────────────────┐
│    orders       │────────→│ task_records│←────────│  attachments    │
└────────┬────────┘ 1:N    └─────────────┘ 1:N    └─────────────────┘
         │ order_id
         ↓
┌─────────────────┐
│ order_products  │
└─────────────────┘

┌─────────────────┐
│      fees       │
└─────────────────┘
```

### 4.2 核心表结构（SQLAlchemy模型）

#### 用户表 (users)
```python
from sqlalchemy import Column, String, Enum, Boolean, DateTime
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"           # 管理员
    DISPATCHER = "dispatcher" # 调度员
    DRIVER = "driver"         # 司机
    INSTALLER = "installer"   # 安装师傅
    UNLOADER = "unloader"     # 卸货人员

class User(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)  # BCrypt哈希
    name = Column(String(50), nullable=False)
    phone = Column(String(20), index=True)
    role = Column(Enum(UserRole), nullable=False, index=True)
    region_id = Column(String(32))  # 所属区域
    status = Column(Boolean, default=True)  # 启用/禁用
    create_time = Column(DateTime, default=datetime.now)
```

#### 订单表 (orders)
```python
class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    DELIVERING = "delivering"
    INSTALLING = "installing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(32), primary_key=True, index=True)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    customer_name = Column(String(50), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    appointment_time = Column(DateTime, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    total_amount = Column(DECIMAL(10, 2), default=0)
    remark = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    products = relationship("OrderProduct", back_populates="order")
    tasks = relationship("Task", back_populates="order")
    fees = relationship("Fee", back_populates="order")
```

#### 任务表 (tasks)
```python
class TaskType(str, enum.Enum):
    UNLOAD = "unload"       # 卸货
    DELIVERY = "delivery"   # 配送
    INSTALL = "install"     # 安装

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(32), primary_key=True, index=True)
    task_no = Column(String(32), unique=True, nullable=False, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    task_type = Column(Enum(TaskType), nullable=False)
    assigned_to = Column(String(32), ForeignKey("users.id"), index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_distance = Column(DECIMAL(10, 2))  # 实际距离(公里)
    remark = Column(Text)
    create_time = Column(DateTime, default=datetime.now)

    # 关联关系
    order = relationship("Order", back_populates="tasks")
    assigned_worker = relationship("User")
    records = relationship("TaskRecord", back_populates="task")
    attachments = relationship("Attachment", back_populates="task")
```

#### 费用表 (fees)
```python
class FeeType(str, enum.Enum):
    DELIVERY = "delivery"   # 配送费
    INSTALL = "install"     # 安装费
    UNLOAD = "unload"       # 卸货费
    OTHER = "other"         # 其他费用

class FeeStatus(str, enum.Enum):
    CALCULATED = "calculated"  # 已计算
    ADJUSTED = "adjusted"      # 已调整
    CONFIRMED = "confirmed"    # 已确认

class Fee(Base):
    __tablename__ = "fees"

    id = Column(String(32), primary_key=True, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(255))
    status = Column(Enum(FeeStatus), default=FeeStatus.CALCULATED)
    create_time = Column(DateTime, default=datetime.now)

    # 关联关系
    order = relationship("Order", back_populates="fees")
```

### 4.3 数据库配置
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/saas_warehouse"

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 120

    # 高德地图配置
    AMAP_API_KEY: str = "your-amap-api-key"

    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID: str = "your-access-key-id"
    OSS_ACCESS_KEY_SECRET: str = "your-access-key-secret"
    OSS_BUCKET_NAME: str = "your-bucket-name"
    OSS_ENDPOINT: str = "https://oss-cn-beijing.aliyuncs.com"

    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # 开发环境打印SQL
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 依赖注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 五、接口设计

### 5.1 接口规范
- **协议**: HTTPS
- **数据格式**: JSON
- **认证方式**: JWT Token (Header: Authorization: Bearer {token})
- **版本控制**: URL路径版本 `/api/v1/xxx`
- **响应格式**: 统一JSON格式

### 5.2 统一响应格式
```python
# app/core/response.py
from fastapi import Response
from typing import Optional, Any

class ApiResponse(Response):
    """统一响应格式"""

    @staticmethod
    def success(data: Any = None, message: str = "success"):
        return {
            "code": 200,
            "message": message,
            "data": data,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }

    @staticmethod
    def error(message: str, code: int = 400, data: Any = None):
        return {
            "code": code,
            "message": message,
            "data": data,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
```

### 5.3 Pydantic Schema设计
```python
# app/schemas/order.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class OrderProductCreate(BaseModel):
    """订单商品创建Schema"""
    product_name: str = Field(..., description="商品名称")
    product_code: Optional[str] = Field(None, description="商品编码")
    quantity: int = Field(..., gt=0, description="数量")
    unit: str = Field(..., description="单位")

class OrderCreate(BaseModel):
    """订单创建Schema"""
    customer_name: str = Field(..., min_length=1, max_length=50, description="客户姓名")
    customer_phone: str = Field(..., regex=r"^1[3-9]\d{9}$", description="客户电话")
    address: str = Field(..., min_length=5, max_length=255, description="配送地址")
    appointment_time: datetime = Field(..., description="预约时间")
    products: List[OrderProductCreate] = Field(..., min_items=1, description="商品列表")
    remark: Optional[str] = Field(None, max_length=500, description="备注")

    @validator('appointment_time')
    def validate_appointment_time(cls, v):
        """预约时间必须在未来"""
        if v < datetime.now():
            raise ValueError('预约时间必须在未来')
        return v

class OrderResponse(BaseModel):
    """订单响应Schema"""
    id: str
    order_no: str
    customer_name: str
    customer_phone: str
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    appointment_time: datetime
    status: str
    total_amount: float
    products: List[dict]
    create_time: datetime

    class Config:
        from_attributes = True
```

### 5.4 核心接口列表（FastAPI路由）

#### 订单接口
```python
# app/api/v1/orders.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from app.core.response import ApiResponse

router = APIRouter(prefix="/orders", tags=["订单"])

@router.post("/", response_model=dict)
async def create_order(
    data: OrderCreate,
    service: OrderService = Depends()
):
    """
    创建订单

    - **customer_name**: 客户姓名
    - **customer_phone**: 客户电话
    - **address**: 配送地址
    - **appointment_time**: 预约时间
    - **products**: 商品列表
    """
    try:
        order = await service.create_order(data)
        return ApiResponse.success({
            "order_id": order.id,
            "order_no": order.order_no,
            "status": order.status
        })
    except Exception as e:
        return ApiResponse.error(str(e))

@router.get("/", response_model=dict)
async def get_orders(
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    service: OrderService = Depends()
):
    """
    查询订单列表

    - **status**: 订单状态筛选
    - **customer_name**: 客户姓名模糊搜索
    - **page**: 页码
    - **size**: 每页数量
    """
    orders = await service.get_orders(status, customer_name, page, size)
    return ApiResponse.success(orders)

@router.get("/{order_id}", response_model=dict)
async def get_order(
    order_id: str,
    service: OrderService = Depends()
):
    """订单详情"""
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return ApiResponse.success(order)

@router.put("/{order_id}", response_model=dict)
async def update_order(
    order_id: str,
    data: OrderUpdate,
    service: OrderService = Depends()
):
    """更新订单"""
    order = await service.update_order(order_id, data)
    return ApiResponse.success(order)

@router.post("/{order_id}/cancel", response_model=dict)
async def cancel_order(
    order_id: str,
    reason: str,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends()
):
    """
    取消订单

    - **reason**: 取消原因
    """
    order = await service.cancel_order(order_id, reason, current_user.id)
    return ApiResponse.success({"order_id": order.id, "status": order.status})
```

#### 调度接口
```python
# app/api/v1/dispatch.py
from fastapi import APIRouter, Depends
from app.schemas.dispatch import AutoDispatchRequest, ManualDispatchRequest
from app.services.dispatch_service import DispatchService
from app.core.response import ApiResponse

router = APIRouter(prefix="/dispatch", tags=["调度"])

@router.post("/auto", response_model=dict)
async def auto_dispatch(
    data: AutoDispatchRequest,
    service: DispatchService = Depends()
):
    """
    智能排单

    - **order_ids**: 订单ID列表
    - **task_type**: 任务类型（unload/delivery/install）
    - **dispatch_date**: 派单日期
    """
    result = await service.auto_dispatch(
        order_ids=data.order_ids,
        task_type=data.task_type,
        dispatch_date=data.dispatch_date
    )
    return ApiResponse.success(result)

@router.post("/manual", response_model=dict)
async def manual_dispatch(
    data: ManualDispatchRequest,
    current_user: User = Depends(get_current_user),
    service: DispatchService = Depends()
):
    """
    手动调整

    - **task_id**: 任务ID
    - **new_worker_id**: 新执行人ID
    - **reason**: 调整原因
    """
    task = await service.manual_dispatch(
        task_id=data.task_id,
        new_worker_id=data.new_worker_id,
        reason=data.reason,
        operator_id=current_user.id
    )
    return ApiResponse.success(task)
```

#### 任务接口（H5端）
```python
# app/api/v1/tasks.py
from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas.task import LocationUpdate, TaskCompleteRequest
from app.services.task_service import TaskService
from app.core.response import ApiResponse

router = APIRouter(prefix="/tasks", tags=["任务"])

@router.get("/my-tasks", response_model=dict)
async def get_my_tasks(
    task_type: Optional[str] = None,
    date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """
    我的任务列表（H5端）

    - **task_type**: 任务类型筛选
    - **date**: 日期筛选（YYYY-MM-DD）
    """
    tasks = await service.get_my_tasks(
        worker_id=current_user.id,
        task_type=task_type,
        date=date
    )
    return ApiResponse.success(tasks)

@router.get("/{task_id}", response_model=dict)
async def get_task_detail(
    task_id: str,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """任务详情"""
    task = await service.get_task_with_auth(task_id, current_user.id)
    return ApiResponse.success(task)

@router.post("/{task_id}/start", response_model=dict)
async def start_task(
    task_id: str,
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """
    开始任务（位置打卡）

    - **latitude**: 纬度
    - **longitude**: 经度
    """
    task = await service.start_task(task_id, location, current_user.id)
    return ApiResponse.success(task)

@router.post("/{task_id}/complete", response_model=dict)
async def complete_task(
    task_id: str,
    data: TaskCompleteRequest,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends()
):
    """
    完成任务

    - **photos**: 照片URL列表
    - **remark**: 备注
    """
    task = await service.complete_task(task_id, data, current_user.id)
    return ApiResponse.success(task)

@router.post("/{task_id}/upload", response_model=dict)
async def upload_photo(
    task_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传照片"""
    # 上传到OSS
    file_url = await upload_to_oss(file)
    # 异步压缩
    compress_image.delay(file_url)
    return ApiResponse.success({"file_url": file_url})
```

#### 报表接口
```python
# app/api/v1/reports.py
from fastapi import APIRouter, Depends, BackgroundTasks
from app.services.report_service import ReportService
from app.core.response import ApiResponse

router = APIRouter(prefix="/reports", tags=["报表"])

@router.get("/order", response_model=dict)
async def get_order_report(
    start_date: str,
    end_date: str,
    group_by: str = "day",  # day/week/month
    service: ReportService = Depends()
):
    """
    订单报表

    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **group_by**: 分组维度
    """
    report = await service.get_order_report(start_date, end_date, group_by)
    return ApiResponse.success(report)

@router.get("/worker", response_model=dict)
async def get_worker_report(
    start_date: str,
    end_date: str,
    service: ReportService = Depends()
):
    """
    人员工作量报表

    - **start_date**: 开始日期
    - **end_date**: 结束日期
    """
    report = await service.get_worker_report(start_date, end_date)
    return ApiResponse.success(report)

@router.post("/export", response_model=dict)
async def export_report(
    report_type: str,
    start_date: str,
    end_date: str,
    background_tasks: BackgroundTasks,
    service: ReportService = Depends()
):
    """
    导出报表（异步）

    - **report_type**: 报表类型（order/worker/fee）
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    """
    report_id = await service.create_export_task(report_type, start_date, end_date)
    # 异步生成报表
    background_tasks.add_task(
        generate_report,
        report_id=report_id,
        report_type=report_type
    )
    return ApiResponse.success({"report_id": report_id, "status": "generating"})
```

---

## 六、安全设计

### 6.1 JWT认证实现
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

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """创建JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict:
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

# app/api/v1/auth.py - 登录接口
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", response_model=dict)
async def login(
    data: LoginRequest,
    service: UserService = Depends()
):
    """用户登录"""
    # 1. 验证用户
    user = await service.get_by_username(data.username)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 2. 检查状态
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )

    # 3. 生成Token
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": user.role}
    )

    return {
        "code": 200,
        "message": "success",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "role": user.role
            }
        }
    }

# app/core/deps.py - 依赖注入
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效"
        )

    user_id = payload.get("sub")
    user = await db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user

def require_role(*roles: str):
    """角色权限检查"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        return current_user
    return role_checker
```

### 6.2 权限控制（RBAC）
```python
# app/core/permissions.py
from functools import wraps
from fastapi import HTTPException

class Permission:
    """权限控制"""

    @staticmethod
    def check(roles: list[str]):
        """检查角色权限"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                current_user = kwargs.get('current_user')
                if not current_user:
                    raise HTTPException(status_code=401, detail="未登录")
                if current_user.role not in roles:
                    raise HTTPException(status_code=403, detail="权限不足")
                return await func(*args, **kwargs)
            return wrapper
        return decorator

# 使用示例
@router.post("/")
@Permission.check(["admin", "dispatcher"])
async def create_order(data: OrderCreate):
    pass
```

### 6.3 敏感数据加密
```python
# app/core/encryption.py
from cryptography.fernet import Fernet
import base64

class Encryption:
    """数据加密工具"""

    @staticmethod
    def generate_key() -> str:
        """生成密钥"""
        return Fernet.generate_key().decode()

    @staticmethod
    def encrypt(data: str, key: str) -> str:
        """加密"""
        f = Fernet(key.encode())
        encrypted = f.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def decrypt(encrypted_data: str, key: str) -> str:
        """解密"""
        f = Fernet(key.encode())
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()

# 使用示例
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # 环境变量配置

phone_encrypted = Encryption.encrypt("13800138000", ENCRYPTION_KEY)
phone_decrypted = Encryption.decrypt(phone_encrypted, ENCRYPTION_KEY)
```

---

## 七、性能优化设计

### 7.1 Redis缓存策略
```python
# app/core/cache.py
from redis import asyncio as aioredis
from app.core.config import settings
from typing import Optional, Any
import json

class RedisCache:
    """Redis缓存封装"""

    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value: Any, expire: int = 300):
        """设置缓存（默认5分钟）"""
        await self.redis.setex(key, expire, json.dumps(value))

    async def delete(self, key: str):
        """删除缓存"""
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str):
        """批量删除缓存"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)

cache = RedisCache()

# 使用示例
# app/services/order_service.py
async def get_orders(
    self,
    status: str = None,
    page: int = 1,
    size: int = 20
) -> list[Order]:
    # 缓存Key
    cache_key = f"orders:{status}:{page}:{size}"

    # 尝试从缓存获取
    cached = await cache.get(cache_key)
    if cached:
        return cached

    # 缓存未命中，查询数据库
    orders = await self.order_repo.get_orders(status, page, size)

    # 写入缓存（5分钟过期）
    await cache.set(cache_key, [o.to_dict() for o in orders], expire=300)

    return orders
```

### 7.2 数据库优化
```python
# app/repositories/base.py
from sqlalchemy import select
from typing import TypeVar, Generic

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """基础Repository"""

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: str) -> Optional[ModelType]:
        """根据ID查询"""
        return await self.db.get(self.model, id)

    async def get_list(
        self,
        filters: dict = None,
        page: int = 1,
        size: int = 20
    ) -> list[ModelType]:
        """分页查询（优化版，使用覆盖索引）"""
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if value is not None:
                    query = query.where(getattr(self.model, key) == value)

        # 分页
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)

        result = await self.db.execute(query)
        return result.scalars().all()
```

### 7.3 异步任务（Celery）
```python
# app/tasks/__init__.py
from app.tasks.celery_app import celery_app

# app/tasks/image_tasks.py
@celery_app.task(bind=True)
def compress_image(self, image_url: str):
    """图片压缩任务"""
    import requests
    from PIL import Image
    from io import BytesIO
    from app.services.file_service import upload_to_oss

    try:
        # 下载图片
        response = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(response.content))

        # 压缩（最大宽度1920，质量80）
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # 保存为JPEG
        output = BytesIO()
        img.save(output, format="JPEG", quality=80, optimize=True)
        output.seek(0)

        # 上传回OSS
        new_url = upload_to_oss(output.getvalue(), image_url)

        return {"success": True, "original_url": image_url, "compressed_url": new_url}

    except Exception as e:
        self.retry(exc=e, countdown=60, max_retries=3)
        return {"success": False, "error": str(e)}

# 调用示例
from app.tasks.image_tasks import compress_image

# 异步调用
compress_image.delay(image_url="https://example.com/image.jpg")
```

---

## 八、部署方案

### 8.1 Docker Compose配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  # MySQL数据库
  mysql:
    image: mysql:8.0
    container_name: saas_mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - saas_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis缓存
  redis:
    image: redis:7.0-alpine
    container_name: saas_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - saas_network
    command: redis-server --appendonly yes

  # FastAPI后端
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: saas_backend
    environment:
      DATABASE_URL: mysql+aiomysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      AMAP_API_KEY: ${AMAP_API_KEY}
      OSS_ACCESS_KEY_ID: ${OSS_ACCESS_KEY_ID}
      OSS_ACCESS_KEY_SECRET: ${OSS_ACCESS_KEY_SECRET}
      OSS_BUCKET_NAME: ${OSS_BUCKET_NAME}
      OSS_ENDPOINT: ${OSS_ENDPOINT}
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/0
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - saas_network
    restart: unless-stopped

  # Celery Worker（异步任务）
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: saas_celery_worker
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=2
    environment:
      DATABASE_URL: mysql+aiomysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
      REDIS_URL: redis://redis:6379/0
      OSS_ACCESS_KEY_ID: ${OSS_ACCESS_KEY_ID}
      OSS_ACCESS_KEY_SECRET: ${OSS_ACCESS_KEY_SECRET}
      OSS_BUCKET_NAME: ${OSS_BUCKET_NAME}
      OSS_ENDPOINT: ${OSS_ENDPOINT}
    depends_on:
      - mysql
      - redis
    networks:
      - saas_network
    restart: unless-stopped

  # 前端Web端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: saas_frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - saas_network
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:

networks:
  saas_network:
    driver: bridge
```

### 8.2 后端Dockerfile
```dockerfile
# backend/Dockerfile
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

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### 8.3 环境变量配置
```bash
# .env
# 数据库配置
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=saas_warehouse
MYSQL_USER=saas_user
MYSQL_PASSWORD=your_password

# JWT配置
JWT_SECRET_KEY=your-super-secret-key-change-in-production

# 高德地图配置
AMAP_API_KEY=your_amap_api_key

# 阿里云OSS配置
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_BUCKET_NAME=your_bucket_name
OSS_ENDPOINT=https://oss-cn-beijing.aliyuncs.com

# 加密密钥
ENCRYPTION_KEY=your_encryption_key_for_sensitive_data
```

### 8.4 启动命令
```bash
# 1. 创建.env文件（复制上面的内容并修改）

# 2. 启动所有服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f backend

# 4. 数据库迁移
docker-compose exec backend alembic upgrade head

# 5. 停止服务
docker-compose down
```

---

## 九、开发计划

### 9.1 阶段划分（10周）

| 周 | 里程碑 | 核心功能 | 交付物 |
|----|--------|---------|--------|
| 第1周 | 搭架子 | FastAPI项目脚手架、数据库建表、JWT认证 | 项目框架、数据库脚本 |
| 第2周 | 订单模块P0 | 订单CRUD、状态流转 | 订单接口可用 |
| 第3周 | 用户任务 | 任务创建、任务列表（H5） | 任务基本流程跑通 |
| 第4周 | 执行流程 | 开始/完成任务、位置打卡、拍照上传 | H5端核心功能 |
| 第5周 | 费用计算 | 费用计算规则、费用调整 | 费用模块完成 |
| 第6周 | 调度排单 | 手动排单、简单智能排单（规则版） | 调度模块完成 |
| 第7周 | 仓储模块 | 库存管理、卸货管理 | 仓储模块完成 |
| 第8周 | 结算报表 | 结算状态、收款记录、简单报表 | 报表模块完成 |
| 第9周 | 优化测试 | 性能优化、Bug修复、UAT测试 | 测试报告 |
| 第10周 | 部署上线 | Docker部署、线上运行 | 生产环境 |

### 9.2 关键里程碑
- **M1（第2周）**: 订单模块完成，订单CRUD可用
- **M2（第4周）**: 核心流程跑通，H5端可用
- **M3（第6周）**: P0功能全部完成，系统可用
- **M4（第10周）**: 系统上线

### 9.3 个人开发建议
- **前6周聚焦P0功能**: 订单、任务、执行、费用、调度
- **后4周打磨P1功能**: 报表、结算、优化
- **每周五Code Review**: 自查代码质量
- **持续集成**: 每次提交自动运行测试

---

## 十、附录

### 10.1 项目结构（最终版）
```
saas-warehouse/
├── backend/                          # 后端
│   ├── app/
│   │   ├── api/                     # 路由层
│   │   │   └── v1/
│   │   │       ├── auth.py         # 认证路由
│   │   │       ├── orders.py       # 订单路由
│   │   │       ├── tasks.py        # 任务路由
│   │   │       ├── dispatch.py     # 调度路由
│   │   │       ├── fees.py         # 费用路由
│   │   │       ├── reports.py      # 报表路由
│   │   │       └── users.py        # 用户路由
│   │   ├── core/                    # 核心配置
│   │   │   ├── config.py           # 配置类
│   │   │   ├── database.py         # 数据库配置
│   │   │   ├── security.py         # JWT认证
│   │   │   ├── deps.py             # 依赖注入
│   │   │   ├── cache.py            # Redis缓存
│   │   │   └── response.py         # 统一响应
│   │   ├── models/                  # ORM模型
│   │   │   ├── user.py
│   │   │   ├── order.py
│   │   │   ├── task.py
│   │   │   ├── fee.py
│   │   │   └── ...
│   │   ├── schemas/                 # Pydantic模型
│   │   │   ├── auth.py
│   │   │   ├── order.py
│   │   │   ├── task.py
│   │   │   └── ...
│   │   ├── services/                # 业务逻辑层
│   │   │   ├── auth_service.py
│   │   │   ├── order_service.py
│   │   │   ├── task_service.py
│   │   │   ├── dispatch_service.py
│   │   │   ├── fee_service.py
│   │   │   └── ...
│   │   ├── repositories/            # 数据访问层
│   │   │   ├── base.py
│   │   │   ├── order_repo.py
│   │   │   └── ...
│   │   ├── tasks/                   # Celery异步任务
│   │   │   ├── celery_app.py
│   │   │   ├── image_tasks.py
│   │   │   └── report_tasks.py
│   │   └── main.py                  # FastAPI入口
│   ├── alembic/                     # 数据库迁移
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/                       # 测试
│   │   ├── test_orders.py
│   │   └── test_tasks.py
│   ├── requirements.txt             # Python依赖
│   ├── Dockerfile
│   └── .env.example                 # 环境变量示例
│
├── frontend/                         # Web端
│   ├── src/
│   │   ├── api/                     # API调用
│   │   ├── views/                   # 页面
│   │   ├── components/              # 组件
│   │   ├── router/                  # 路由
│   │   └── main.js
│   ├── package.json
│   └── Dockerfile
│
├── h5/                              # H5端（复用Web端代码）
│   └── ...
│
├── docker-compose.yml               # 一键启动
├── .env                             # 环境变量
└── README.md
```

### 10.2 Python依赖清单
```txt
# requirements.txt
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0

# ORM
sqlalchemy==2.0.23
aiomysql==0.2.0
alembic==1.12.1

# 数据验证
pydantic==2.5.0
pydantic-settings==2.1.0

# 认证加密
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# 缓存
redis[hiredis]==5.0.1

# 异步任务
celery==5.3.4

# HTTP客户端
httpx==0.25.2

# 文件处理
Pillow==10.1.0

# 环境变量
python-dotenv==1.0.0

# 日志
loguru==0.7.2

# 高德地图
amap==1.0.0

# 阿里云OSS
oss2==2.18.4
```

### 10.3 参考文档
- FastAPI官方文档: https://fastapi.tiangolo.com/
- SQLAlchemy文档: https://docs.sqlalchemy.org/
- Celery文档: https://docs.celeryproject.org/
- 高德地图API文档: https://lbs.amap.com/api/
- 阿里云OSS文档: https://help.aliyun.com/product/31815.html

### 10.4 变更记录
| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v2.0 | 2026-03-12 | 扣子 | 基于Python FastAPI技术栈重新编写概要设计 |
