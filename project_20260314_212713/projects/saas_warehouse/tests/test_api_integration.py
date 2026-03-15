"""
API集成测试 - 测试完整的API流程
"""
import pytest
import sys
from datetime import datetime, timedelta

sys.path.append("../")


class TestUserAuthAPI:
    """用户认证API测试"""
    
    @pytest.fixture
    def client(self, test_client):
        """使用test_client fixture"""
        return test_client
    
    def test_admin_login(self, client):
        """测试管理员登录"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "admin",
                "password": "admin123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
    
    def test_wrong_password_login(self, client):
        """测试错误密码登录"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "admin",
                "password": "wrong_password"
            }
        )
        assert response.status_code in [400, 401]
    
    def test_nonexistent_user_login(self, client):
        """测试不存在用户登录"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "password"
            }
        )
        assert response.status_code in [400, 401, 404]


class TestOrderAPI:
    """订单API测试"""
    
    @pytest.fixture
    def admin_headers(self, test_client):
        """获取管理员认证头"""
        response = test_client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.fixture
    def client(self, test_client):
        """使用test_client fixture"""
        return test_client
    
    def test_get_orders_empty(self, client, admin_headers):
        """测试获取空订单列表"""
        response = client.get(
            "/api/v1/orders/",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
    
    def test_get_orders_with_pagination(self, client, admin_headers):
        """测试分页查询订单"""
        response = client.get(
            "/api/v1/orders/?page=1&size=10",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["page"] == 1
        assert data["data"]["size"] == 10
    
    def test_get_orders_with_status_filter(self, client, admin_headers):
        """测试按状态筛选订单"""
        response = client.get(
            "/api/v1/orders/?status=pending",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestPermissionAPI:
    """权限API测试"""
    
    @pytest.fixture
    def client(self, test_client):
        """使用test_client fixture"""
        return test_client
    
    def test_worker_cannot_create_order(self, client):
        """测试工人无法创建订单"""
        # 工人登录
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "worker", "password": "worker123"}
        )
        worker_token = response.json()["access_token"]
        
        # 尝试创建订单
        response = client.post(
            "/api/v1/orders/",
            json={
                "customer_name": "测试客户",
                "customer_phone": "13800138000",
                "address": "北京市朝阳区",
                "products": [{"product_name": "测试商品", "quantity": 1}]
            },
            headers={"Authorization": f"Bearer {worker_token}"}
        )
        # 应该返回403（权限不足）或401（未授权）
        assert response.status_code in [401, 403]


class TestRootAPI:
    """根路径API测试"""
    
    def test_root_endpoint(self, test_client):
        """测试根路径"""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_docs_endpoint(self, test_client):
        """测试API文档"""
        response = test_client.get("/docs")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
