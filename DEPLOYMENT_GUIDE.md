# 仓配装SaaS系统部署指南

## 项目结构

```
Saas_program/
├── project_20260314_212713/
│   └── projects/
│       └── saas_warehouse/  # 后端服务
├── saas-warehouse-web/      # Web管理后台
├── saas-warehouse-h5/       # H5移动端
├── docker-compose.yml       # Docker Compose配置
└── DEPLOYMENT_GUIDE.md      # 部署指南
```

## 部署方式

### 1. 本地开发环境

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

### 2. Docker容器化部署

#### 构建和启动

```bash
# 在项目根目录执行
docker-compose up -d --build
```

#### 访问地址

- Web管理后台: http://localhost
- H5移动端: http://localhost:8080
- 后端API: http://localhost:8000

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

## 技术栈

### 后端
- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (数据验证)
- JWT (认证)
- SQLite (数据库)

### 前端

#### Web管理后台
- Vue 3
- TypeScript
- Element Plus (UI库)
- ECharts (图表)
- Pinia (状态管理)
- Vue Router (路由)

#### H5移动端
- Vue 3
- TypeScript
- Vant (UI库)
- Pinia (状态管理)
- Vue Router (路由)

## 核心功能

### 1. 订单管理
- 订单创建、编辑、查询
- 批量导入订单
- 订单状态跟踪

### 2. 调度排单
- 自动调度算法
- 手动调度
- 任务分配

### 3. 仓储管理
- 仓库管理
- 库存管理
- 卸货管理

### 4. 配送管理
- 配送任务跟踪
- 司机管理
- 路线规划

### 5. 安装管理
- 安装任务跟踪
- 安装工管理
- 安装难度评估

### 6. 费用管理
- 费用记录
- 费用结算
- 费用统计

### 7. 报表分析
- 订单趋势
- 人员工作量
- 费用分布

### 8. 用户管理
- 用户角色管理
- 权限控制
- 用户状态管理

### 9. 系统设置
- 系统配置
- API配置
- 系统日志

## 注意事项

1. **安全性**：生产环境中应使用强密码和安全的密钥
2. **性能**：建议使用Redis缓存和数据库索引优化
3. **监控**：建议配置日志监控和错误报警
4. **备份**：定期备份数据库和配置文件
5. **更新**：更新代码前请先备份数据

## 故障排查

### 常见问题

1. **API连接失败**：检查后端服务是否运行，API地址是否正确
2. **数据库连接错误**：检查数据库配置和权限
3. **前端页面白屏**：检查网络连接和API响应
4. **权限问题**：检查用户角色和权限配置

### 日志查看

```bash
# 查看后端日志
docker-compose logs backend

# 查看Web日志
docker-compose logs web

# 查看H5日志
docker-compose logs h5
```
