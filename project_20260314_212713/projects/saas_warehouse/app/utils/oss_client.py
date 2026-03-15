import oss2
from app.core.config import settings


class OSSClient:
    """OSS客户端"""
    
    def __init__(self):
        self.auth = oss2.Auth(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET
        )
        self.bucket = oss2.Bucket(
            self.auth,
            settings.OSS_ENDPOINT,
            settings.OSS_BUCKET_NAME
        )
    
    def upload_file(self, file_path: str, object_name: str) -> str:
        """上传文件
        返回: 文件URL
        """
        self.bucket.put_object_from_file(object_name, file_path)
        return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT.replace('https://', '')}/{object_name}"
    
    def upload_content(self, content: bytes, object_name: str) -> str:
        """上传内容
        返回: 文件URL
        """
        self.bucket.put_object(object_name, content)
        return f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT.replace('https://', '')}/{object_name}"
    
    def delete_file(self, object_name: str) -> bool:
        """删除文件
        返回: 是否成功
        """
        try:
            self.bucket.delete_object(object_name)
            return True
        except Exception:
            return False
