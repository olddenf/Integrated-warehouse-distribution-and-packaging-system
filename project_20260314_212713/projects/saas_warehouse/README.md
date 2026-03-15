# SaaS仓配装一体化管理系统

## 项目简介

SaaS仓配装一体化管理系统是一个基于Python FastAPI框架开发的现代化仓库、配送、安装一体化管理系统。系统支持订单管理、智能调度排单、任务执行、费用计算、报表分析等核心功能，为企业提供全流程的仓配装管理解决方案。

## 技术栈

- **后端**: Python FastAPI + SQLAlchemy + MySQL + Redis + Celery
- **前端**: Vue3 + Element Plus (Web端) + Vue3 + Vant (H5端)
- **部署**: Docker + Docker Compose

## 核心功能

### Web管理端
- 订单管理：订单录入、查询、编辑、取消
- 调度排单：智能排单、手动调整、工单管理
- 仓储管理：库存管理、卸货管理
- 配送管理：配送任务、路线规划、签收管理
- 安装管理：安装任务、验收拍照、材料使用
- 费用管理：费用计算、费用调整、费用审核
- 结算管理：结算状态、收款记录、开票管理
- 报表分析：订单报表、人员报表、费用报表

### H5移动端
- 卸货端：任务列表、卸货执行、拍照打卡
- 司机端：任务列表、一键导航、到货确认、签收确认
- 安装端：任务列表、任务详情、安装开始/完成、验收拍照

## 项目结构

```
saas_warehouse/
├── app/                # 应用代码
│   ├── core/          # 核心配置
│   ├── models/        # ORM模型
│   ├── schemas/       # Pydantic Schema
│   ├── services/      # 业务逻辑
│   ├── api/           # API路由
│   ├── repositories/  # 数据访问
│   ├── tasks/         # Celery任务
│   ├── utils/         # 工具函数
│   ├── exceptions/    # 异常处理
│   ├── middleware/    # 中间件
│   └── constants/     # 常量定义
├── tests/             # 测试代码
├── scripts/           # 脚本工具
├── requirements.txt   # 依赖列表
├── .env               # 环境变量
├── Dockerfile         # Docker镜像
└── docker-compose.yml # Docker编排
```

## 快速开始

### 1. 环境准备

- Python 3.8+
- MySQL 8.0+
- Redis 7.0+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置。

### 4. 初始化数据库

```bash
python scripts/init_db.py
```

### 5. 创建管理员用户

```bash
python scripts/create_admin.py
```

### 6. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. 访问系统

- API文档: http://localhost:8000/docs
- 系统首页: http://localhost:8000

## 管理员账号

- 用户名: admin
- 密码: admin123

## 部署

使用 Docker Compose 部署：

```bash
docker-compose up -d
```

## 项目特点

- **现代化技术栈**: 使用 FastAPI 框架，性能优异，自动生成 API 文档
- **异步处理**: 全异步架构，提高系统并发处理能力
- **智能排单**: 基于多维度评分的智能任务分配算法
- **实时监控**: 任务执行状态实时更新，位置打卡功能
- **数据分析**: 多维度报表，支持数据导出
- **安全可靠**: JWT 认证，权限控制，数据加密

## 许可证

MIT
