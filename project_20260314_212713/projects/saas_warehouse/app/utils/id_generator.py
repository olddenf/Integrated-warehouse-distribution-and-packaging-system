import uuid
from datetime import datetime


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


def generate_order_no() -> str:
    """生成订单编号
    格式: SO + 年月日 + 6位随机数
    示例: SO20260312000001
    """
    prefix = "SO"
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = str(uuid.uuid4().int)[:6]
    return f"{prefix}{date_str}{random_str}"


def generate_task_no(task_type: str) -> str:
    """生成任务编号
    格式: 任务类型 + 年月日 + 6位随机数
    示例: DL20260312000001 (配送)
    """
    type_prefix = {
        "unload": "UL",
        "delivery": "DL",
        "install": "IN"
    }.get(task_type, "TK")
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = str(uuid.uuid4().int)[:6]
    return f"{type_prefix}{date_str}{random_str}"
