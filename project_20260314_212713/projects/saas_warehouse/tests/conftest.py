import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import asyncio

# 测试数据库连接字符串
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_saas_warehouse.db"


@pytest.fixture(scope="module")
def test_client():
    """测试客户端"""
    # 创建测试引擎
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    # 创建测试会话工厂
    test_session_local = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # 创建数据库表结构并初始化数据
    async def init_db():
        # 创建表结构
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # 创建测试用户
        async with test_session_local() as session:
            # 检查用户是否已存在
            from sqlalchemy import select
            result = await session.execute(select(User).where(User.username == "admin"))
            if not result.scalar():
                admin_user = User(
                    id="admin-1",
                    username="admin",
                    password_hash=get_password_hash("admin123"),
                    name="管理员",
                    role=UserRole.ADMIN,
                    status=True
                )
                
                dispatcher_user = User(
                    id="dispatcher-1",
                    username="dispatcher",
                    password_hash=get_password_hash("dispatcher123"),
                    name="调度员",
                    role=UserRole.DISPATCHER,
                    status=True
                )
                
                worker_user = User(
                    id="worker-1",
                    username="worker",
                    password_hash=get_password_hash("worker123"),
                    name="工人",
                    role=UserRole.DRIVER,
                    status=True
                )
                
                session.add_all([admin_user, dispatcher_user, worker_user])
                await session.commit()
    
    # 运行初始化
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_db())
    
    # 覆盖数据库依赖
    async def override_get_db():
        async with test_session_local() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    yield client
    
    # 测试结束后清理
    async def cleanup():
        # 删除表结构
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        # 关闭引擎
        await test_engine.dispose()
    
    loop.run_until_complete(cleanup())
    loop.close()
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def admin_token(test_client):
    """管理员Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def dispatcher_token(test_client):
    """调度员Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "dispatcher", "password": "dispatcher123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def worker_token(test_client):
    """工人Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "worker", "password": "worker123"}
    )
    return response.json()["access_token"]
