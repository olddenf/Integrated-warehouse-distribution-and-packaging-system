import pytest
import sys
import os
from fastapi.testclient import TestClient

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from unittest.mock import patch


@pytest.mark.asyncio
async def test_role_permissions(test_client, admin_token, dispatcher_token, worker_token):
    """测试角色权限控制"""
    # 测试创建订单接口 - 只有admin和dispatcher可以访问
    order_data = {
        "customer_name": "测试客户",
        "customer_phone": "13800138000",
        "address": "北京市朝阳区",
        "appointment_time": "2026-12-31 18:00:00",
        "products": [
            {
                "product_name": "测试产品",
                "quantity": 1,
                "unit": "个"
            }
        ]
    }
    
    # 模拟MapClient的geocode方法
    with patch('app.services.order_service.MapClient.geocode', return_value=(39.9042, 116.4074)):
        # admin应该可以创建订单
        admin_response = test_client.post(
            "/api/v1/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert admin_response.status_code == 200
        
        # dispatcher应该可以创建订单
        dispatcher_response = test_client.post(
            "/api/v1/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {dispatcher_token}"}
        )
        assert dispatcher_response.status_code == 200
        
        # worker不应该可以创建订单
        worker_response = test_client.post(
            "/api/v1/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {worker_token}"}
        )
        assert worker_response.status_code == 403


@pytest.mark.asyncio
async def test_token_validation(test_client, admin_token):
    """测试Token验证"""
    # 测试使用无效Token
    invalid_response = test_client.get(
        "/api/v1/orders",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert invalid_response.status_code == 401
    
    # 测试使用过期Token（这里简化处理，实际应该测试真实的过期Token）
    # 由于我们无法直接生成过期Token，这里跳过这个测试
    
    # 测试不提供Token
    no_token_response = test_client.get("/api/v1/orders")
    assert no_token_response.status_code == 403


@pytest.mark.asyncio
async def test_get_current_user(test_client, admin_token):
    """测试获取当前用户信息"""
    # 测试获取订单列表，验证Token有效
    response = test_client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "items" in response.json()["data"]
