# 仓配装SaaS系统

## 项目概述

仓配装SaaS系统是一套集成仓储、配送、安装全流程管理的智能系统，旨在为企业提供高效、透明、可追溯的物流服务管理解决方案。系统通过数字化手段优化物流流程，提高运营效率，降低运营成本，提升客户满意度。

## 技术栈

- **后端**：Python 3.12 + FastAPI + SQLite
- **前端（Web）**：Vue 3 + TypeScript + Element Plus
- **前端（H5）**：Vue 3 + TypeScript + Vant
- **容器化**：Docker + Docker Compose

## 核心功能

- **订单管理**：订单创建、查询、状态追踪
- **调度排单**：智能调度、手动调度、任务优先级管理
- **仓储管理**：仓库管理、库存管理、卸货管理
- **配送管理**：配送任务跟踪、路线规划、实时定位、签收管理
- **安装管理**：安装任务跟踪、安装指南、难度评估、安装验收
- **费用管理**：费用记录、结算、统计、成本控制
- **报表分析**：订单、人员、费用、配送报表
- **用户管理**：角色管理、权限控制、用户状态管理

## 项目结构

```
Saas_program/
├── project_20260314_212713/
│   └── projects/
│       └── saas_warehouse/  # 后端服务
├── saas-warehouse-web/      # Web管理后台
├── saas-warehouse-h5/       # H5移动端
├── docker-compose.yml       # Docker Compose配置
├── DEPLOYMENT_GUIDE.md      # 部署指南
├── PRODUCT_SPEC.md          # 产品说明
└── README.md                # 项目说明
```

## 快速开始

### 一键部署

使用Docker Compose一键部署整个系统：

```bash
# 在项目根目录执行
docker-compose up -d --build
```

部署完成后，系统将通过以下地址访问：

- Web管理后台: <http://localhost>
- H5移动端: <http://localhost:8080>
- 后端API: <http://localhost:8000>

### 本地开发

#### 后端服务

```bash
# 进入后端目录
cd project_20260314_212713/projects/saas_warehouse

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 创建管理员用户
python scripts/create_admin.py

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Web管理后台

```bash
# 进入Web目录
cd saas-warehouse-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### H5移动端

```bash
# 进入H5目录
cd saas-warehouse-h5

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 系统角色

| 角色  | 权限   | 功能                       |
| --- | ---- | ------------------------ |
| 管理员 | 全部   | 系统配置、用户管理、订单管理、调度管理、报表查看 |
| 仓库员 | 仓储相关 | 仓库管理、卸货任务处理、库存管理         |
| 司机  | 配送相关 | 配送任务处理、路线导航、签收管理         |
| 安装工 | 安装相关 | 安装任务处理、安装指南查看、安装验收       |

## 环境配置

### 后端环境变量

在 `project_20260314_212713/projects/saas_warehouse/.env` 文件中配置：

```
# 数据库连接
DATABASE_URL=sqlite:///./saas_warehouse.db

# JWT配置
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 高德API
GAODE_API_KEY=your_gaode_api_key

# OSS配置
OSS_ACCESS_KEY=your_oss_access_key
OSS_SECRET_KEY=your_oss_secret_key
OSS_BUCKET=your_oss_bucket
OSS_ENDPOINT=your_oss_endpoint
```

### 前端API地址配置

在 `saas-warehouse-web/src/api/index.ts` 和 `saas-warehouse-h5/src/api/index.ts` 中配置：

```typescript
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  // ...
});
```

## 版本信息

| 版本     | 发布日期       | 主要功能                              |
| ------ | ---------- | --------------------------------- |
| v1.0.0 | 2026-03-15 | 基础功能实现，包括订单管理、调度排单、仓储管理、配送管理、安装管理 |
| v1.1.0 | 2026-04-15 | 增加报表分析功能，优化调度算法                   |
| v1.2.0 | 2026-05-15 | 增加费用管理功能，支持多仓库管理                  |
| v2.0.0 | 2026-06-15 | 重构系统架构，提升性能，增加AI辅助功能              |

## 一键部署说明

### 前提条件

使用一键部署指令前，需要先安装Docker和Docker Compose：

#### Windows系统

1. 访问 [Docker官方网站](https://www.docker.com/products/docker-desktop)
2. 下载并安装Docker Desktop for Windows
3. 安装完成后，启动Docker Desktop
4. 等待Docker服务启动完成（系统托盘图标显示绿色）

#### macOS系统

1. 访问 [Docker官方网站](https://www.docker.com/products/docker-desktop)
2. 下载并安装Docker Desktop for Mac
3. 安装完成后，启动Docker Desktop
4. 等待Docker服务启动完成

#### Linux系统

1. 根据不同的Linux发行版，使用相应的包管理器安装Docker
2. 安装完成后，启动Docker服务
3. 确保当前用户加入docker用户组

### 验证Docker安装

安装完成后，在PowerShell或终端中执行以下命令验证Docker是否正常运行：

```bash
docker --version
docker-compose --version
```

### 执行一键部署

Docker安装完成后，在项目根目录执行以下命令：

```bash
docker-compose up -d --build
```

部署完成后，系统将自动启动并通过以下地址访问：

- Web管理后台: <http://localhost>
- H5移动端: <http://localhost:8080>
- 后端API: <http://localhost:8000>

##
