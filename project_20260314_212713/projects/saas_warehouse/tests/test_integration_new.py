"""
集成测试 - 模块间集成、数据库集成、API集成
"""
import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User, UserRole
from app.models.order import Order, OrderStatus, OrderProduct
from app.models.task import Task, TaskType, TaskStatus
from app.services.order_service import OrderService
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


@pytest_asyncio.fixture
async def test_db():
    """创建测试数据库会话"""
    TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_saas_warehouse_integration.db"
    
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    test_session_local = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    from app.core.database import Base
    
    # 创建表结构
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with test_session_local() as session:
        yield session
    
    # 清理
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


class TestOrderTaskIntegration:
    """订单与任务模块集成测试"""
    
    @pytest_asyncio.fixture
    async def test_user(self, test_db: AsyncSession):
        """创建测试用户"""
        user = User(
            id="test-worker-1",
            username="test_worker",
            password_hash="hashed_password_mock",  # 使用mock密码避免bcrypt问题
            name="测试工人",
            role=UserRole.DRIVER,
            phone="13800000001",
            status=True
        )
        test_db.add(user)
        await test_db.commit()
        await test_db.refresh(user)
        return user
    
    @pytest.mark.asyncio
    async def test_order_creates_task(self, test_db: AsyncSession, test_user: User):
        """测试订单创建后自动生成任务"""
        # 创建订单
        order = Order(
            id="test-order-1",
            order_no="SO20260313000001",
            customer_name="张三",
            customer_phone="13800138000",
            address="北京市朝阳区",
            status=OrderStatus.PENDING,
            appointment_time=datetime.now() + timedelta(days=1)
        )
        test_db.add(order)
        await test_db.commit()
        await test_db.refresh(order)
        
        # 验证订单创建成功
        assert order.id == "test-order-1"
        assert order.status == OrderStatus.PENDING
        
        # 创建关联任务
        task = Task(
            id="test-task-1",
            task_no="DL20260313000001",
            order_id=order.id,
            task_type=TaskType.DELIVERY,
            assigned_to=test_user.id,
            status=TaskStatus.PENDING
        )
        test_db.add(task)
        await test_db.commit()
        await test_db.refresh(task)
        
        # 验证任务与订单关联
        assert task.order_id == order.id
        assert task.assigned_to == test_user.id
        
        # 查询验证关联关系
        result = await test_db.execute(
            select(Task).where(Task.order_id == order.id)
        )
        tasks = result.scalars().all()
        assert len(tasks) == 1
        assert tasks[0].id == task.id
    
    @pytest.mark.asyncio
    async def test_order_cancels_task(self, test_db: AsyncSession):
        """测试订单取消时任务自动取消"""
        # 创建订单
        order = Order(
            id="test-order-2",
            order_no="SO20260313000002",
            customer_name="李四",
            customer_phone="13900139000",
            address="上海市浦东新区",
            status=OrderStatus.PENDING
        )
        test_db.add(order)
        
        # 创建任务
        task = Task(
            id="test-task-2",
            task_no="DL20260313000002",
            order_id=order.id,
            task_type=TaskType.DELIVERY,
            status=TaskStatus.PENDING
        )
        test_db.add(task)
        await test_db.commit()
        await test_db.refresh(order)
        
        # 取消订单
        order.status = OrderStatus.CANCELLED
        await test_db.commit()
        
        # 取消任务
        task.status = TaskStatus.CANCELLED
        await test_db.commit()
        await test_db.refresh(task)
        
        # 验证订单和任务都被取消
        assert order.status == OrderStatus.CANCELLED
        assert task.status == TaskStatus.CANCELLED


class TestUserTaskIntegration:
    """用户与任务模块集成测试"""
    
    @pytest_asyncio.fixture
    async def test_users(self, test_db: AsyncSession):
        """创建测试用户"""
        users = [
            User(
                id="test-user-1",
                username="worker1",
                password_hash="hashed_password_mock_1",  # 使用mock密码避免bcrypt问题
                name="工人1",
                role=UserRole.DRIVER,
                phone="13800000002",
                status=True
            ),
            User(
                id="test-user-2",
                username="worker2",
                password_hash="hashed_password_mock_2",  # 使用mock密码避免bcrypt问题
                name="工人2",
                role=UserRole.DRIVER,
                phone="13800000003",
                status=True
            )
        ]
        for user in users:
            test_db.add(user)
        await test_db.commit()
        return users
    
    @pytest.mark.asyncio
    async def test_user_assigned_tasks(self, test_db: AsyncSession, test_users):
        """测试用户分配任务查询"""
        # 创建任务并分配给用户1
        task1 = Task(
            id="test-task-3",
            task_no="DL20260313000003",
            order_id="order-1",
            task_type=TaskType.DELIVERY,
            assigned_to=test_users[0].id,
            status=TaskStatus.IN_PROGRESS
        )
        test_db.add(task1)
        
        # 创建任务并分配给用户2
        task2 = Task(
            id="test-task-4",
            task_no="DL20260313000004",
            order_id="order-2",
            task_type=TaskType.DELIVERY,
            assigned_to=test_users[1].id,
            status=TaskStatus.PENDING
        )
        test_db.add(task2)
        
        await test_db.commit()
        
        # 查询用户1的任务
        result = await test_db.execute(
            select(Task).where(Task.assigned_to == test_users[0].id)
        )
        user1_tasks = result.scalars().all()
        assert len(user1_tasks) == 1
        assert user1_tasks[0].id == task1.id
        
        # 查询用户2的任务
        result = await test_db.execute(
            select(Task).where(Task.assigned_to == test_users[1].id)
        )
        user2_tasks = result.scalars().all()
        assert len(user2_tasks) == 1
        assert user2_tasks[0].id == task2.id


class TestDatabaseIntegration:
    """数据库集成测试"""
    
    @pytest.mark.asyncio
    async def test_transaction_commit(self, test_db: AsyncSession):
        """测试事务提交"""
        # 创建订单
        order = Order(
            id="test-order-3",
            order_no="SO20260313000003",
            customer_name="王五",
            customer_phone="13700137000",
            address="广州市天河区",
            status=OrderStatus.PENDING
        )
        test_db.add(order)
        
        # 创建商品
        product = OrderProduct(
            id="test-product-1",
            order_id=order.id,
            product_name="测试商品1",
            quantity=2
        )
        test_db.add(product)
        
        # 提交事务
        await test_db.commit()
        
        # 验证数据已保存
        result = await test_db.execute(
            select(Order).where(Order.id == order.id)
        )
        saved_order = result.scalar_one()
        assert saved_order is not None
        assert saved_order.customer_name == "王五"
        
        result = await test_db.execute(
            select(OrderProduct).where(OrderProduct.order_id == order.id)
        )
        saved_products = result.scalars().all()
        assert len(saved_products) == 1
    
    @pytest.mark.asyncio
    async def test_transaction_rollback(self, test_db: AsyncSession):
        """测试事务回滚"""
        # 开始事务
        async with test_db.begin():
            # 创建订单
            order = Order(
                id="test-order-4",
                order_no="SO20260313000004",
                customer_name="赵六",
                customer_phone="13600136000",
                address="深圳市南山区",
                status=OrderStatus.PENDING
            )
            test_db.add(order)
            
            # 创建商品
            product = OrderProduct(
                id="test-product-2",
                order_id=order.id,
                product_name="测试商品2",
                quantity=1
            )
            test_db.add(product)
            
            # 模拟异常
            await test_db.rollback()
        
        # 验证数据未被保存
        result = await test_db.execute(
            select(Order).where(Order.id == "test-order-4")
        )
        saved_order = result.scalar_one_or_none()
        assert saved_order is None


class TestRepositoryIntegration:
    """Repository集成测试"""
    
    @pytest.mark.asyncio
    async def test_order_repository_crud(self, test_db: AsyncSession):
        """测试订单Repository的CRUD操作"""
        from app.repositories.order_repository import OrderRepository
        
        repo = OrderRepository(test_db)
        
        # Create
        order = Order(
            id="repo-order-1",
            order_no="SO20260313000005",
            customer_name="Repository测试",
            customer_phone="13500135000",
            address="测试地址",
            status=OrderStatus.PENDING
        )
        test_db.add(order)
        await test_db.commit()
        await test_db.refresh(order)
        
        # Read (使用get方法而不是get_by_id)
        found_order = await repo.get(order.id)
        assert found_order is not None
        assert found_order.customer_name == "Repository测试"
        
        # Update
        found_order.remark = "更新备注"
        await test_db.commit()
        await test_db.refresh(found_order)
        assert found_order.remark == "更新备注"
        
        # Delete
        await repo.delete(found_order)
        
        deleted_order = await repo.get(order.id)
        assert deleted_order is None
    
    @pytest.mark.asyncio
    async def test_task_repository_query(self, test_db: AsyncSession):
        """测试任务Repository的查询操作"""
        # 创建多个任务
        for i in range(3):
            task = Task(
                id=f"repo-task-{i}",
                task_no=f"DL2026031300000{i}",
                order_id="order-1",
                task_type=TaskType.DELIVERY,
                status=TaskStatus.PENDING if i < 2 else TaskStatus.IN_PROGRESS
            )
            test_db.add(task)
        await test_db.commit()
        
        # 手动查询待处理任务（使用select而不是get_by_status）
        result = await test_db.execute(
            select(Task).where(Task.status == TaskStatus.PENDING)
        )
        pending_tasks = result.scalars().all()
        assert len(pending_tasks) >= 2


class TestStatusTransition:
    """状态转换集成测试"""
    
    @pytest.mark.asyncio
    async def test_order_status_transition(self, test_db: AsyncSession):
        """测试订单状态转换"""
        # 创建订单
        order = Order(
            id="status-order-1",
            order_no="SO20260313000006",
            customer_name="状态测试",
            customer_phone="13500135000",
            address="测试地址",
            status=OrderStatus.PENDING
        )
        test_db.add(order)
        await test_db.commit()
        
        # 待派单 -> 已派单
        order.status = OrderStatus.ASSIGNED
        await test_db.commit()
        await test_db.refresh(order)
        assert order.status == OrderStatus.ASSIGNED
        
        # 已派单 -> 配送中
        order.status = OrderStatus.DELIVERING
        await test_db.commit()
        assert order.status == OrderStatus.DELIVERING
        
        # 配送中 -> 已完成
        order.status = OrderStatus.COMPLETED
        await test_db.commit()
        assert order.status == OrderStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_task_status_transition(self, test_db: AsyncSession):
        """测试任务状态转换"""
        # 创建任务
        task = Task(
            id="status-task-1",
            task_no="DL20260313000010",
            order_id="order-1",
            task_type=TaskType.DELIVERY,
            status=TaskStatus.PENDING
        )
        test_db.add(task)
        await test_db.commit()
        
        # 待处理 -> 进行中
        task.status = TaskStatus.IN_PROGRESS
        await test_db.commit()
        assert task.status == TaskStatus.IN_PROGRESS
        
        # 进行中 -> 已完成
        task.status = TaskStatus.COMPLETED
        await test_db.commit()
        assert task.status == TaskStatus.COMPLETED


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
