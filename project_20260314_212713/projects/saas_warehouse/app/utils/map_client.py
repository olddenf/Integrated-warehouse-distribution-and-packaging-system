import httpx
from app.core.config import settings


class MapClient:
    """地图API客户端"""
    
    def __init__(self):
        self.api_key = settings.AMAP_API_KEY
        self.base_url = "https://restapi.amap.com/v3"
    
    async def geocode(self, address: str) -> tuple[float, float]:
        """地址解析
        返回: (纬度, 经度)
        """
        url = f"{self.base_url}/geocode/geo"
        params = {
            "key": self.api_key,
            "address": address
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get("status") == "1" and data.get("geocodes"):
                location = data["geocodes"][0]["location"]
                lng, lat = map(float, location.split(","))
                return lat, lng
            else:
                raise Exception(f"地址解析失败: {data.get('info')}")
    
    async def direction(self, origin: tuple[float, float], destination: tuple[float, float]) -> dict:
        """路线规划
        origin: (纬度, 经度)
        destination: (纬度, 经度)
        """
        url = f"{self.base_url}/direction/driving"
        origin_str = f"{origin[1]},{origin[0]}"  # 高德API使用 lng,lat
        dest_str = f"{destination[1]},{destination[0]}"
        
        params = {
            "key": self.api_key,
            "origin": origin_str,
            "destination": dest_str
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json()
