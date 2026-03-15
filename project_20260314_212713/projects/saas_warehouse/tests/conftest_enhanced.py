"""
增强版测试配置 - 支持Mock外部API
"""
import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
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


@pytest.fixture(scope="function")
def test_client():
    """测试客户端"""
    # 创建测试引擎
    TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_saas_warehouse.db"
    
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
    # 创建测试会话工厂
    test_session_local = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # 创建数据库表结构
    async def init_db():
        # 删除旧表
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        # 创建新表
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # 创建测试用户
        async with test_session_local() as session:
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
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()
    
    loop.run_until_complete(cleanup())
    loop.close()
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_token(test_client):
    """管理员Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def dispatcher_token(test_client):
    """调度员Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "dispatcher", "password": "dispatcher123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def worker_token(test_client):
    """工人Token"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "worker", "password": "worker123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def mock_map_client():
    """Mock地图客户端"""
    with patch('app.utils.map_client.httpx.AsyncClient') as mock_client_class:
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "1",
            "geocodes": [{
                "location": "116.397428,39.90923"
            }]
        }
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        yield mock_client_class


@pytest.fixture
def mock_oss_client():
    """Mock OSS客户端"""
    with patch('app.utils.oss_client.oss2') as mock_oss2:
        mock_auth = Mock()
        mock_bucket = Mock()
        mock_bucket.put_object_from_file.return_value = None
        mock_bucket.delete_object.return_value = None
        
        mock_oss2.Auth.return_value = mock_auth
        mock_oss2.Bucket.return_value = mock_bucket
        
        yield mock_oss2


@pytest.fixture
async def test_session(test_client):
    """获取测试会话"""
    from app.core.database import get_db
    
    async for session in get_db():
        yield session
        break
