import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.map_client import MapClient
from app.utils.oss_client import OSSClient


@pytest.mark.asyncio
@patch('app.utils.map_client.httpx.AsyncClient.get')
async def test_geocode(mock_get):
    """测试高德API地址解析功能"""
    # 模拟高德API响应
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "1",
        "geocodes": [
            {
                "location": "116.407413,39.904211"
            }
        ]
    }
    mock_get.return_value = mock_response
    
    # 创建地图客户端实例
    map_client = MapClient()
    
    # 测试地址解析
    result = await map_client.geocode("北京市朝阳区")
    
    # 验证结果
    assert result == (39.904211, 116.407413)
    mock_get.assert_called_once()


@pytest.mark.asyncio
@patch('app.utils.map_client.httpx.AsyncClient.get')
async def test_direction(mock_get):
    """测试高德API路线规划功能"""
    # 模拟高德API响应
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "1",
        "route": {
            "paths": [
                {
                    "distance": 1000,
                    "duration": 60
                }
            ]
        }
    }
    mock_get.return_value = mock_response
    
    # 创建地图客户端实例
    map_client = MapClient()
    
    # 测试路线规划
    origin = (39.904211, 116.407413)
    destination = (39.914211, 116.417413)
    result = await map_client.direction(origin, destination)
    
    # 验证结果
    assert result["status"] == "1"
    assert "route" in result
    mock_get.assert_called_once()


@pytest.mark.asyncio
@patch('app.utils.oss_client.oss2.Bucket')
async def test_oss_upload(mock_bucket):
    """测试OSS存储上传功能"""
    # 模拟OSS Bucket
    mock_bucket_instance = MagicMock()
    mock_bucket.return_value = mock_bucket_instance
    
    # 创建OSS客户端实例
    oss_client = OSSClient()
    
    # 测试上传文件
    file_path = "test.txt"
    object_name = "test/test.txt"
    result = oss_client.upload_file(file_path, object_name)
    
    # 验证结果
    assert isinstance(result, str)
    assert "test/test.txt" in result
    mock_bucket_instance.put_object_from_file.assert_called_once_with(object_name, file_path)


@pytest.mark.asyncio
@patch('app.utils.oss_client.oss2.Bucket')
async def test_oss_upload_content(mock_bucket):
    """测试OSS存储上传内容功能"""
    # 模拟OSS Bucket
    mock_bucket_instance = MagicMock()
    mock_bucket.return_value = mock_bucket_instance
    
    # 创建OSS客户端实例
    oss_client = OSSClient()
    
    # 测试上传内容
    content = b"test content"
    object_name = "test/test.txt"
    result = oss_client.upload_content(content, object_name)
    
    # 验证结果
    assert isinstance(result, str)
    assert "test/test.txt" in result
    mock_bucket_instance.put_object.assert_called_once_with(object_name, content)


@pytest.mark.asyncio
@patch('app.utils.oss_client.oss2.Bucket')
async def test_oss_delete(mock_bucket):
    """测试OSS存储删除功能"""
    # 模拟OSS Bucket
    mock_bucket_instance = MagicMock()
    mock_bucket.return_value = mock_bucket_instance
    
    # 创建OSS客户端实例
    oss_client = OSSClient()
    
    # 测试删除文件
    object_name = "test/test.txt"
    result = oss_client.delete_file(object_name)
    
    # 验证结果
    assert result is True
    mock_bucket_instance.delete_object.assert_called_once_with(object_name)
