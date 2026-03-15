"""
单元测试 - 工具函数和服务层
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
import asyncio

# 导入需要测试的模块
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.id_generator import generate_uuid, generate_order_no, generate_task_no


class TestIdGenerator:
    """ID生成器单元测试"""
    
    def test_generate_uuid(self):
        """测试UUID生成"""
        uuid1 = generate_uuid()
        uuid2 = generate_uuid()
        
        # 验证UUID不为空
        assert uuid1 is not None
        assert uuid2 is not None
        
        # 验证UUID是唯一的
        assert uuid1 != uuid2
        
        # 验证UUID长度
        assert len(uuid1) == 36  # 标准UUID长度
    
    def test_generate_order_no(self):
        """测试订单编号生成"""
        order_no = generate_order_no()
        
        # 验证订单编号格式
        assert order_no.startswith("SO")
        assert len(order_no) == 16  # SO + 8位日期 + 6位随机数
        
        # 验证日期部分
        today = datetime.now().strftime("%Y%m%d")
        assert order_no[2:10] == today
        
        # 验证订单编号唯一性
        order_no2 = generate_order_no()
        assert order_no != order_no2
    
    def test_generate_task_no_delivery(self):
        """测试配送任务编号生成"""
        task_no = generate_task_no("delivery")
        
        # 验证任务编号格式
        assert task_no.startswith("DL")
        assert len(task_no) == 16  # DL + 8位日期 + 6位随机数
    
    def test_generate_task_no_install(self):
        """测试安装任务编号生成"""
        task_no = generate_task_no("install")
        
        # 验证任务编号格式
        assert task_no.startswith("IN")
        assert len(task_no) == 16
    
    def test_generate_task_no_unload(self):
        """测试卸货任务编号生成"""
        task_no = generate_task_no("unload")
        
        # 验证任务编号格式
        assert task_no.startswith("UL")
        assert len(task_no) == 16
    
    def test_generate_task_no_unknown_type(self):
        """测试未知任务类型编号生成"""
        task_no = generate_task_no("unknown")
        
        # 验证默认前缀
        assert task_no.startswith("TK")
        assert len(task_no) == 16


class TestMapClient:
    """地图客户端单元测试"""
    
    @pytest.fixture
    def map_client(self):
        """创建地图客户端实例"""
        from app.utils.map_client import MapClient
        return MapClient()
    
    @pytest.mark.skip(reason="需要配置地图API密钥")
    @pytest.mark.asyncio
    async def test_geocode_success(self, map_client):
        """测试地址解析成功"""
        # Mock HTTP客户端
        with patch('httpx.AsyncClient') as mock_client_class:
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
            
            lat, lng = await map_client.geocode("北京市朝阳区")
            
            # 验证返回值
            assert lat is not None
            assert lng is not None
            assert isinstance(lat, float)
            assert isinstance(lng, float)
    
    @pytest.mark.skip(reason="需要配置地图API密钥")
    @pytest.mark.asyncio
    async def test_geocode_failure(self, map_client):
        """测试地址解析失败"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "0",
                "info": "INVALID_USER_KEY"
            }
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            # 应该抛出异常
            with pytest.raises(Exception):
                await map_client.geocode("无效地址")


class TestOssClient:
    """OSS客户端单元测试"""
    
    @pytest.fixture
    def oss_client(self):
        """创建OSS客户端实例"""
        from app.utils.oss_client import OSSClient
        return OSSClient()
    
    @pytest.mark.skip(reason="需要配置OSS凭证")
    def test_upload_file(self, oss_client):
        """测试文件上传"""
        # Mock OSS上传
        with patch.object(oss_client, 'bucket', create=True) as mock_bucket:
            mock_bucket.put_object_from_file.return_value = None
            
            file_path = "/tmp/test.jpg"
            result = oss_client.upload_file(file_path, "test.jpg")
            
            # 验证上传结果
            assert result is not None
            assert "test.jpg" in result or "http" in result
    
    @pytest.mark.skip(reason="需要配置OSS凭证")
    def test_delete_file(self, oss_client):
        """测试文件删除"""
        with patch.object(oss_client, 'bucket', create=True) as mock_bucket:
            mock_bucket.delete_object.return_value = None
            
            result = oss_client.delete_file("test.jpg")
            
            # 验证删除结果
            assert result is True


class TestOrderService:
    """订单服务单元测试"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock数据库会话"""
        return Mock(spec=AsyncSession)
    
    @pytest.fixture
    def order_service(self, mock_db):
        """创建订单服务实例"""
        from app.services.order_service import OrderService
        from unittest.mock import MagicMock
        
        # Mock dependencies
        with patch('app.services.order_service.MapClient') as mock_map:
            with patch('app.services.order_service.FeeService') as mock_fee:
                service = OrderService(mock_db)
                return service
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_create_order_success(self, order_service, mock_db):
        """测试创建订单成功"""
        from app.schemas.order import OrderCreate, OrderProductCreate
        
        # 准备测试数据
        order_data = OrderCreate(
            customer_name="张三",
            customer_phone="13800138000",
            address="北京市朝阳区",
            appointment_time=datetime.now(),
            products=[OrderProductCreate(
                product_name="测试商品",
                quantity=1
            )]
        )
        
        # Mock数据库操作
        with patch.object(order_service, '_log_order_action', new_callable=AsyncMock):
            with patch.object(order_service.fee_service, 'calculate_fees', new_callable=AsyncMock):
                # Mock commit和refresh
                mock_db.commit = AsyncMock()
                mock_db.refresh = AsyncMock()
                
                order = await order_service.create_order(order_data)
                
                # 验证订单创建
                assert order is not None
                assert order.customer_name == "张三"
                assert order.customer_phone == "13800138000"
                
                # 验证数据库操作被调用
                mock_db.commit.assert_called()
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_create_order_with_geocode(self, order_service, mock_db):
        """测试创建订单时地址解析"""
        from app.schemas.order import OrderCreate, OrderProductCreate
        
        order_data = OrderCreate(
            customer_name="李四",
            customer_phone="13900139000",
            address="上海市浦东新区",
            appointment_time=datetime.now(),
            products=[OrderProductCreate(
                product_name="测试商品2",
                quantity=2
            )]
        )
        
        # Mock地址解析返回经纬度
        with patch.object(order_service.map_client, 'geocode', new_callable=AsyncMock) as mock_geocode:
            mock_geocode.return_value = (31.230416, 121.473701)
            with patch.object(order_service, '_log_order_action', new_callable=AsyncMock):
                with patch.object(order_service.fee_service, 'calculate_fees', new_callable=AsyncMock):
                    mock_db.commit = AsyncMock()
                    mock_db.refresh = AsyncMock()
                    
                    order = await order_service.create_order(order_data)
                    
                    # 验证经纬度被正确设置
                    assert order.latitude is not None
                    assert order.longitude is not None


class TestTaskService:
    """任务服务单元测试"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock数据库会话"""
        return Mock(spec=AsyncSession)
    
    @pytest.fixture
    def task_service(self, mock_db):
        """创建任务服务实例"""
        from app.services.task_service import TaskService
        return TaskService(mock_db)
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_create_task_success(self, task_service, mock_db):
        """测试创建任务成功"""
        from app.schemas.task import TaskCreate
        
        task_data = TaskCreate(
            order_id="order-1",
            task_type="delivery",
            assigned_to="worker-1"
        )
        
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        with patch('app.services.task_service.generate_uuid', return_value='task-1'):
            with patch('app.services.task_service.generate_task_no', return_value='DL20260313000001'):
                task = await task_service.create_task(task_data)
                
                # 验证任务创建
                assert task is not None
                assert task.order_id == "order-1"
                assert task.assigned_to == "worker-1"
                
                # 验证数据库操作
                mock_db.commit.assert_called()
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_update_task_status(self, task_service, mock_db):
        """测试更新任务状态"""
        # Mock返回的任务
        mock_task = Mock()
        mock_task.status = "pending"
        
        with patch.object(task_service.task_repo, 'get_by_id', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_task
            
            mock_db.commit = AsyncMock()
            mock_db.refresh = AsyncMock()
            
            result = await task_service.update_task_status("task-1", "in_progress")
            
            # 验证状态更新
            assert result is not None
            mock_task.status = "in_progress"
            mock_db.commit.assert_called()


class TestFeeService:
    """费用服务单元测试"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock数据库会话"""
        return Mock(spec=AsyncSession)
    
    @pytest.fixture
    def fee_service(self, mock_db):
        """创建费用服务实例"""
        from app.services.fee_service import FeeService
        return FeeService(mock_db)
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_calculate_fees(self, fee_service, mock_db):
        """测试费用计算"""
        # Mock订单数据
        mock_order = Mock()
        mock_order.id = "order-1"
        mock_order.address = "北京市朝阳区"
        
        with patch.object(fee_service.order_repo, 'get_by_id', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_order
            
            mock_db.commit = AsyncMock()
            
            result = await fee_service.calculate_fees("order-1")
            
            # 验证费用计算
            assert result is not None


class TestUserService:
    """用户服务单元测试"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock数据库会话"""
        return Mock(spec=AsyncSession)
    
    @pytest.fixture
    def user_service(self, mock_db):
        """创建用户服务实例"""
        from app.services.user_service import UserService
        return UserService(mock_db)
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_db):
        """测试创建用户成功"""
        from app.schemas.user import UserCreate
        
        user_data = UserCreate(
            username="testuser",
            password="password123",
            name="测试用户",
            phone="13700137000",
            role="driver"
        )
        
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        with patch('app.services.user_service.generate_uuid', return_value='user-1'):
            with patch('app.services.user_service.get_password_hash', return_value='hashed_password'):
                user = await user_service.create_user(user_data)
                
                # 验证用户创建
                assert user is not None
                assert user.username == "testuser"
                assert user.role.value == "driver"
                
                # 验证密码被哈希
                assert user.password_hash == "hashed_password"


class TestDispatchService:
    """调度服务单元测试"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock数据库会话"""
        return Mock(spec=AsyncSession)
    
    @pytest.fixture
    def dispatch_service(self, mock_db):
        """创建调度服务实例"""
        from app.services.dispatch_service import DispatchService
        return DispatchService(mock_db)
    
    @pytest.mark.skip(reason="需要完整的数据库环境和依赖")
    @pytest.mark.asyncio
    async def test_auto_dispatch(self, dispatch_service, mock_db):
        """测试自动调度"""
        # Mock订单数据
        mock_order = Mock()
        mock_order.id = "order-1"
        mock_order.latitude = 39.90923
        mock_order.longitude = 116.397428
        
        # Mock工人数据
        mock_worker = Mock()
        mock_worker.id = "worker-1"
        mock_worker.latitude = 39.910
        mock_worker.longitude = 116.398
        
        with patch.object(dispatch_service.order_repo, 'get_by_id', new_callable=AsyncMock) as mock_get_order:
            mock_get_order.return_value = mock_order
            
            with patch.object(dispatch_service.user_repo, 'get_available_workers', new_callable=AsyncMock) as mock_get_workers:
                mock_get_workers.return_value = [mock_worker]
                
                mock_db.commit = AsyncMock()
                mock_db.refresh = AsyncMock()
                
                result = await dispatch_service.auto_dispatch("order-1")
                
                # 验证调度结果
                assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=app", "--cov-report=html"])
