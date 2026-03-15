import pytest
import sys
import os
from fastapi.testclient import TestClient

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from unittest.mock import patch
import pytest_asyncio


@pytest.mark.asyncio
@pytest.mark.parametrize("username, password, expected_status", [
    ("admin", "admin123", 200),
    ("dispatcher", "dispatcher123", 200),
    ("worker", "worker123", 200),
    ("admin", "wrongpassword", 401),
    ("nonexistent", "admin123", 401),
])
async def test_login(test_client, username, password, expected_status):
    """测试登录接口"""
    response = test_client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password}
    )
    assert response.status_code == expected_status
    
    if expected_status == 200:
        assert "access_token" in response.json()
        assert "user" in response.json()


@pytest.mark.asyncio
async def test_create_order(test_client, admin_token):
    """测试创建订单接口"""
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
        response = test_client.post(
            "/api/v1/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    assert response.status_code == 200
    assert "order_id" in response.json()["data"]
    assert "order_no" in response.json()["data"]
    assert "status" in response.json()["data"]
    assert "total_amount" in response.json()["data"]


@pytest.mark.asyncio
async def test_get_orders(test_client, admin_token):
    """测试查询订单列表接口"""
    response = test_client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    assert "items" in response.json()["data"]
    assert "total" in response.json()["data"]
    assert "page" in response.json()["data"]
    assert "size" in response.json()["data"]


@pytest.mark.asyncio
async def test_get_my_tasks(test_client, worker_token):
    """测试获取我的任务列表接口"""
    response = test_client.get(
        "/api/v1/tasks/my-tasks",
        headers={"Authorization": f"Bearer {worker_token}"}
    )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auto_dispatch(test_client, admin_token):
    """测试智能排单接口"""
    # 先创建一个订单
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
        create_response = test_client.post(
            "/api/v1/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    order_id = create_response.json()["data"]["order_id"]
    
    # 测试智能排单
    dispatch_data = {
        "order_ids": [order_id],
        "task_type": "delivery",
        "dispatch_date": "2024-12-31"
    }
    
    response = test_client.post(
        "/api/v1/dispatch/auto",
        json=dispatch_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    assert "results" in response.json()["data"]
