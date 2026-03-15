# SaaS仓配装一体化管理系统需求设计文档

## 文档信息
- **项目名称**: SaaS仓配装一体化管理系统
- **文档版本**: v1.0
- **创建日期**: 2026-03-12
- **文档类型**: 需求规格说明书

---

## 一、项目背景与目标

### 1.1 业务背景
企业当前面临仓配装全流程管理效率低下、信息不透明、成本管控困难等问题，需要通过数字化手段实现订单-仓储-配送-安装的一体化管理。

### 1.2 项目目标
- 实现订单全流程可视化管理
- 提升配送和安装调度效率30%以上
- 降低人力成本，减少沟通成本
- 提供数据报表支持决策分析

### 1.3 目标用户
| 用户角色 | 用户规模 | 使用场景 | 核心诉求 |
|---------|---------|---------|---------|
| 调度员 | 5-10人 | Web端 | 高效排单、实时监控、快速响应 |
| 主管/管理层 | 3-5人 | Web端 | 数据分析、成本管控、决策支持 |
| 卸货人员 | 10-20人 | H5端 | 任务清晰、操作便捷、快速打卡 |
| 司机 | 10-30人 | H5端 | 导航准确、签收便捷、状态同步 |
| 安装师傅 | 5-10人 | H5端 | 任务详细、验收规范、多图上传 |

---

## 二、系统架构设计

### 2.1 系统组成
```
┌─────────────────────────────────────────────────────┐
│                    SaaS云服务平台                    │
├─────────────────────────────────────────────────────┤
│  Web管理端(PC)      │    H5移动端(三端)              │
│  - 订单管理        │    - 卸货端                    │
│  - 调度排单        │    - 司机端                    │
│  - 仓储管理        │    - 安装端                    │
│  - 配送管理        │                                │
│  - 安装管理        │                                │
│  - 费用管理        │                                │
│  - 结算管理        │                                │
│  - 报表分析        │                                │
└─────────────────────────────────────────────────────┘
              ↑              ↓
        ┌─────────────────────────────┐
        │     第三方服务集成          │
        │  - 高德/百度地图API         │
        │  - 云存储服务(OSS)          │
        │  - 短信/推送服务            │
        └─────────────────────────────┘
```

### 2.2 技术架构建议
| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端(Web) | Vue3 + Element Plus | 管理后台，组件化开发 |
| 前端(H5) | Vue3 + Vant | 移动端三端复用，响应式设计 |
| 后端 | Node.js / Java / Python | 根据团队技术栈选择 |
| 数据库 | MySQL + Redis | 关系型数据库+缓存 |
| 文件存储 | 阿里云OSS / 腾讯云COS | 图片、文档云存储 |
| 地图服务 | 高德地图API / 百度地图API | 导航、路线规划 |
| 部署方式 | Docker + K8s | 容器化部署 |

---

## 三、功能模块详细设计

### 3.1 Web管理端

#### 模块1: 订单管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| OM-01 | 订单录入 | 手动录入订单信息，支持批量导入Excel | 客户信息、商品信息、配送地址、预约时间 | 订单编号、订单状态 | P0 |
| OM-02 | 订单查询 | 支持多条件组合查询订单 | 订单编号、客户名称、时间范围、状态 | 订单列表 | P0 |
| OM-03 | 订单编辑 | 编辑订单基本信息和状态 | 订单ID、修改内容 | 操作结果 | P1 |
| OM-04 | 订单取消 | 取消订单并记录原因 | 订单ID、取消原因 | 操作结果 | P1 |

**数据模型**:
```javascript
Order {
  id: String                    // 订单编号（自动生成）
  customerName: String          // 客户姓名
  customerPhone: String         // 客户电话
  address: String               // 配送地址
  latitude: Number              // 纬度
  longitude: Number             // 经度
  productList: Array            // 商品列表
 预约时间: DateTime             // 预约配送/安装时间
  status: Enum                  // 待派单/已派单/配送中/已完成/已取消
  createTime: DateTime           // 创建时间
  updateTime: DateTime           // 更新时间
}
```

#### 模块2: 调度排单
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| DM-01 | 智能排单 | 基于规则自动分配任务给执行人员 | 订单列表、执行人员列表 | 工单分配结果 | P1 |
| DM-02 | 手动调整 | 手动调整工单分配关系 | 工单ID、新执行人员 | 操作结果 | P0 |
| DM-03 | 工单管理 | 查看和管理所有工单状态 | 查询条件 | 工单列表 | P0 |

**智能排单规则**:
- 按区域分配：根据配送地址自动匹配对应区域的执行人员
- 按负载均衡：根据执行人员当前任务数量分配
- 按技能匹配：根据商品类型匹配具备相应技能的安装师傅
- 时间冲突检测：避免同一执行人员时间重叠

#### 模块3: 仓储管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| WM-01 | 库存管理 | 商品入库、出库、盘点 | 商品信息、数量变动 | 库存记录 | P0 |
| WM-02 | 卸货管理 | 卸货任务记录与完成确认 | 任务ID、卸货数量 | 完成记录 | P0 |

#### 模块4: 配送管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| DM-01 | 配送任务 | 生成配送任务并分配给司机 | 订单ID、司机ID | 任务单 | P0 |
| DM-02 | 路线规划 | 基于地址自动规划配送路线 | 任务列表 | 路线图 | P1 |
| DM-03 | 签收管理 | 查看签收状态和签收凭证 | 任务ID | 签收信息 | P0 |

#### 模块5: 安装管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| IM-01 | 安装任务 | 生成安装任务并分配给师傅 | 订单ID、师傅ID | 任务单 | P0 |
| IM-02 | 安装记录 | 查看安装执行进度 | 任务ID | 安装进度 | P0 |
| IM-03 | 验收管理 | 查看验收照片和验收结果 | 任务ID | 验收信息 | P0 |

#### 模块6: 费用管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| FM-01 | 费用计算 | 基于规则自动计算各项费用 | 订单ID | 费用明细 | P0 |
| FM-02 | 费用调整 | 手动调整费用金额 | 订单ID、调整项、金额 | 调整记录 | P1 |
| FM-03 | 费用审核 | 费用调整审核流程 | 调整记录ID | 审核结果 | P1 |

**费用计算规则**:
- 配送费：按距离/重量/体积计算
- 安装费：按商品类型/安装难度计算
- 卸货费：按货物数量/卸货难度计算
- 其他费用：按实际发生记录

#### 模块7: 结算管理
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| SM-01 | 结算状态 | 查看订单结算状态 | 查询条件 | 结算列表 | P0 |
| SM-02 | 收款记录 | 记录收款信息 | 订单ID、收款金额、方式 | 收款记录 | P0 |
| SM-03 | 开票管理 | 开票记录和发票管理 | 订单ID、发票信息 | 开票记录 | P1 |

#### 模块8: 报表分析
| 功能编号 | 功能名称 | 功能描述 | 输入 | 输出 | 优先级 |
|---------|---------|---------|------|------|--------|
| RM-01 | 订单报表 | 订单数量、金额、状态统计 | 时间范围 | 统计图表/Excel | P0 |
| RM-02 | 人员报表 | 执行人员工作量、效率统计 | 时间范围、人员ID | 统计图表/Excel | P0 |
| RM-03 | 费用报表 | 费用构成、成本分析 | 时间范围 | 统计图表/Excel | P1 |

---

### 3.2 H5移动端

#### 卸货端
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|---------|---------|---------|--------|
| UL-01 | 任务列表 | 查看今日卸货任务列表 | P0 |
| UL-02 | 卸货执行 | 选择任务执行卸货，记录卸货数量 | P0 |
| UL-03 | 拍照打卡 | 卸货完成拍照打卡(GPS定位) | P0 |

#### 司机端
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|---------|---------|---------|--------|
| DR-01 | 任务列表 | 查看今日配送任务列表 | P0 |
| DR-02 | 一键导航 | 调用地图导航到客户地址 | P0 |
| DR-03 | 到货确认 | 到达客户位置确认(GPS定位) | P0 |
| DR-04 | 签收确认 | 客户签收确认(签名/拍照) | P0 |
| DR-05 | 异常上报 | 配送异常情况上报 | P1 |
| DR-06 | 历史记录 | 查看历史配送记录 | P1 |

#### 安装端
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|---------|---------|---------|--------|
| IM-01 | 任务列表 | 查看今日安装任务列表 | P0 |
| IM-02 | 任务详情 | 查看安装任务详细信息(商品、客户) | P0 |
| IM-03 | 安装开始 | 开始安装，记录开始时间 | P0 |
| IM-04 | 安装完成 | 完成安装，记录结束时间 | P0 |
| IM-05 | 验收拍照 | 上传验收照片(支持多图) | P0 |
| IM-06 | 材料使用 | 记录使用材料信息 | P1 |
| IM-07 | 问题反馈 | 安装过程问题反馈 | P1 |
| IM-08 | 客户评价 | 客户满意度评价 | P1 |
| IM-09 | 安装教程 | 查看安装指导视频/文档 | P2 |
| IM-10 | 历史记录 | 查看历史安装记录 | P1 |
| IM-11 | 统计数据 | 个人工作量统计 | P1 |
| IM-12 | 消息通知 | 接收任务推送通知 | P0 |
| IM-13 | 个人中心 | 个人信息管理 | P1 |
| IM-14 | 设置 | 系统设置(消息、缓存) | P2 |
| IM-15 | 帮助中心 | 常见问题解答 | P2 |

---

## 四、核心功能详细设计

### 4.1 智能排单算法

#### 排单规则优先级
1. **强制规则**（必须满足）
   - 执行人员工作时间匹配
   - 任务不重叠
   - 区域权限匹配

2. **优化规则**（尽量满足）
   - 工作量均衡
   - 距离最短
   - 技能匹配

#### 排单流程
```
开始
  ↓
获取待排单订单列表
  ↓
筛选可用的执行人员（按区域、技能、时间）
  ↓
为每个订单生成可行执行人员候选集
  ↓
应用排单规则评分排序
  ↓
分配任务给最优执行人员
  ↓
检测资源冲突 → 如有冲突，调整分配
  ↓
生成排单结果
  ↓
结束
```

### 4.2 地图集成方案

#### 功能需求
- 地址解析：将客户地址转换为经纬度坐标
- 路线规划：为配送任务规划最优路线
- 导航功能：一键跳转地图应用导航

#### 技术实现
```javascript
// 地址解析示例
async function geocode(address) {
  const response = await fetch(
    `https://restapi.amap.com/v3/geocode/geo?key=${API_KEY}&address=${address}`
  )
  const data = await response.json()
  return data.geocodes[0].location.split(',') // [lng, lat]
}

// 路线规划示例
async function routePlanning(origin, destination, waypoints) {
  const response = await fetch(
    `https://restapi.amap.com/v3/direction/driving?key=${API_KEY}&origin=${origin}&destination=${destination}&waypoints=${waypoints}`
  )
  return await response.json()
}
```

#### 费用说明
| 服务 | 调用量 | 免费额度 | 超出费用 |
|------|-------|---------|---------|
| 地址解析 | 10000次/日 | 5000次/日 | ¥0.005/次 |
| 路线规划 | 5000次/日 | 2000次/日 | ¥0.01/次 |

### 4.3 照片上传功能

#### 技术要求
- 支持多图上传（最多9张）
- 图片压缩（≤2MB/张）
- 支持预览和删除
- 上传进度显示

#### 实现方案
```javascript
// 图片压缩
async function compressImage(file, maxWidth = 1920, quality = 0.8) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (e) => {
      const img = new Image()
      img.src = e.target.result
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const width = Math.min(maxWidth, img.width)
        const height = (width / img.width) * img.height
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)
        canvas.toBlob((blob) => {
          resolve(new File([blob], file.name, { type: 'image/jpeg' }))
        }, 'image/jpeg', quality)
      }
    }
  })
}

// 上传到云存储
async function uploadToOSS(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData
  })
  return await response.json() // { url: 'https://...' }
}
```

---

## 五、非功能性需求

### 5.1 性能指标
| 指标项 | 要求 | 测试方法 |
|--------|------|---------|
| 页面加载时间 | ≤2秒 | 性能测试工具 |
| 接口响应时间 | ≤1秒 | 接口性能测试 |
| 并发用户数 | 50-100人同时在线 | 压力测试 |
| 数据库查询 | ≤500ms | 慢查询监控 |

### 5.2 可用性
- 系统可用性：≥99.5%（月度）
- 数据备份：每日自动备份，保留30天
- 容灾方案：支持主从切换

### 5.3 兼容性
| 平台 | 版本要求 |
|------|---------|
| Web浏览器 | Chrome 80+、Edge 80+、Safari 14+、Firefox 75+ |
| 移动端 | iOS 12+、Android 8.0+ |
| 企业应用 | 企业微信、钉钉H5容器 |

### 5.4 安全性
- 用户认证：JWT Token认证
- 数据传输：HTTPS加密
- 数据存储：敏感信息加密存储
- 权限控制：基于角色的权限管理(RBAC)
- 操作日志：关键操作记录日志

### 5.5 可扩展性
- 模块化设计，支持功能模块插拔
- API标准化，支持第三方系统集成
- 支持多租户SaaS模式

---

## 六、数据库设计（核心表）

### 6.1 核心数据表

#### 用户表 (users)
```sql
CREATE TABLE users (
  id VARCHAR(32) PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  phone VARCHAR(20),
  role ENUM('admin', 'dispatcher', 'driver', 'installer', 'unloader') NOT NULL,
  status TINYINT DEFAULT 1,
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_role (role),
  INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 订单表 (orders)
```sql
CREATE TABLE orders (
  id VARCHAR(32) PRIMARY KEY,
  order_no VARCHAR(32) UNIQUE NOT NULL,
  customer_name VARCHAR(50) NOT NULL,
  customer_phone VARCHAR(20) NOT NULL,
  address VARCHAR(255) NOT NULL,
  latitude DECIMAL(10,7),
  longitude DECIMAL(10,7),
  appointment_time DATETIME,
  status ENUM('pending', 'assigned', 'delivering', 'installing', 'completed', 'cancelled') DEFAULT 'pending',
  total_amount DECIMAL(10,2),
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_appointment (appointment_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 订单商品表 (order_products)
```sql
CREATE TABLE order_products (
  id VARCHAR(32) PRIMARY KEY,
  order_id VARCHAR(32) NOT NULL,
  product_name VARCHAR(100) NOT NULL,
  product_code VARCHAR(50),
  quantity INT DEFAULT 1,
  unit VARCHAR(20),
  FOREIGN KEY (order_id) REFERENCES orders(id),
  INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 任务表 (tasks)
```sql
CREATE TABLE tasks (
  id VARCHAR(32) PRIMARY KEY,
  task_no VARCHAR(32) UNIQUE NOT NULL,
  order_id VARCHAR(32) NOT NULL,
  task_type ENUM('unload', 'delivery', 'install') NOT NULL,
  assigned_to VARCHAR(32),
  status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
  start_time DATETIME,
  end_time DATETIME,
  remark TEXT,
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (assigned_to) REFERENCES users(id),
  INDEX idx_assigned (assigned_to),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 任务执行记录表 (task_records)
```sql
CREATE TABLE task_records (
  id VARCHAR(32) PRIMARY KEY,
  task_id VARCHAR(32) NOT NULL,
  record_type ENUM('start', 'complete', 'photo', 'location', 'exception') NOT NULL,
  content TEXT,
  location_lat DECIMAL(10,7),
  location_lng DECIMAL(10,7),
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (task_id) REFERENCES tasks(id),
  INDEX idx_task (task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 附件表 (attachments)
```sql
CREATE TABLE attachments (
  id VARCHAR(32) PRIMARY KEY,
  task_id VARCHAR(32) NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_url VARCHAR(500) NOT NULL,
  file_size INT,
  file_type VARCHAR(50),
  upload_by VARCHAR(32),
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (task_id) REFERENCES tasks(id),
  INDEX idx_task (task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 费用表 (fees)
```sql
CREATE TABLE fees (
  id VARCHAR(32) PRIMARY KEY,
  order_id VARCHAR(32) NOT NULL,
  fee_type ENUM('delivery', 'install', 'unload', 'other') NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  description VARCHAR(255),
  status ENUM('calculated', 'adjusted', 'confirmed') DEFAULT 'calculated',
  create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  INDEX idx_order (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 七、接口设计规范

### 7.1 接口规范
- **协议**: HTTPS
- **数据格式**: JSON
- **请求方法**: GET（查询）、POST（创建）、PUT（更新）、DELETE（删除）
- **认证方式**: JWT Token（Header: Authorization: Bearer {token}）

### 7.2 统一响应格式
```javascript
// 成功响应
{
  "code": 200,
  "message": "success",
  "data": {}
}

// 失败响应
{
  "code": 400,
  "message": "错误信息",
  "data": null
}
```

### 7.3 核心接口列表

#### 订单相关接口
| 接口路径 | 方法 | 说明 |
|---------|------|------|
| /api/orders | POST | 创建订单 |
| /api/orders | GET | 查询订单列表 |
| /api/orders/{id} | GET | 订单详情 |
| /api/orders/{id} | PUT | 更新订单 |
| /api/orders/{id}/cancel | POST | 取消订单 |
| /api/orders/batch-import | POST | 批量导入订单 |

#### 任务相关接口
| 接口路径 | 方法 | 说明 |
|---------|------|------|
| /api/tasks | POST | 创建任务 |
| /api/tasks/my-tasks | GET | 我的任务列表 |
| /api/tasks/{id}/start | POST | 开始任务 |
| /api/tasks/{id}/complete | POST | 完成任务 |
| /api/tasks/{id}/upload | POST | 上传附件 |

#### 文件上传接口
| 接口路径 | 方法 | 说明 |
|---------|------|------|
| /api/upload/image | POST | 图片上传 |
| /api/upload/file | POST | 文件上传 |

---

## 八、项目实施计划

### 8.1 阶段划分

| 阶段 | 时间 | 主要内容 | 交付物 |
|------|------|---------|--------|
| 需求分析与设计 | 1-2周 | 需求确认、架构设计、UI设计 | 需求文档、设计稿 |
| 开发阶段 | 6-8周 | 前后端开发、接口联调 | 源代码 |
| 测试阶段 | 2周 | 功能测试、性能测试、UAT | 测试报告 |
| 部署上线 | 1周 | 环境部署、数据迁移、正式上线 | 线上系统 |
| 培训与运维 | 持续 | 用户培训、运维支持 | 操作手册 |

### 8.2 里程碑
- **M1**: 需求确认（第2周）
- **M2**: 核心功能开发完成（第5周）
- **M3**: 系统测试完成（第9周）
- **M4**: 系统正式上线（第10周）

---

## 九、风险与应对

| 风险项 | 风险等级 | 应对措施 |
|--------|---------|---------|
| 需求变更 | 高 | 建立变更控制流程，评估变更影响 |
| 地图API费用超预期 | 中 | 监控调用量，设置费用预警 |
| 移动端兼容性问题 | 中 | 多设备测试，适配主流机型 |
| 数据安全风险 | 高 | 数据加密、权限控制、备份恢复 |
| 用户接受度低 | 中 | 提前培训、收集反馈、持续优化 |

---

## 十、报价所需关键信息确认

### 10.1 功能范围确认
- [ ] 智能排单功能是否需要高级版（AI优化）？
- [ ] 是否需要支持二次开发？
- [ ] 是否需要对接现有ERP/CRM系统？
- [ ] 是否需要PDF报表导出功能？

### 10.2 技术选型确认
- [ ] 后端技术栈偏好（Node.js/Java/Python）？
- [ ] 是否需要部署在特定云服务商？
- [ ] 数据库是否有特殊要求？

### 10.3 费用构成
- [ ] 订阅费：按用户数计费 / 按订单量计费 / 统一定价
- [ ] 实施费：一次性费用（预计￥XXX）
- [ ] 定制开发费：￥XXX/人天
- [ ] 地图API费用：甲方承担 / 乙方承担
- [ ] 云存储费用：甲方承担 / 乙方承担

### 10.4 服务保障
- [ ] 响应时间：2小时内响应 / 4小时内响应
- [ ] 是否需要SLA保障？
- [ ] 系统升级是否免费？
- [ ] 是否需要驻场培训？

---

## 附录

### 附录A：专业术语表
| 术语 | 说明 |
|------|------|
| SaaS | Software as a Service，软件即服务 |
| H5 | HTML5移动网页 |
| GPS | 全球定位系统 |
| API | 应用程序接口 |
| OSS | Object Storage Service，对象存储服务 |

### 附录B：参考文档
- 《高德地图API开发文档》
- 《阿里云OSS使用指南》
- 《企业微信H5开发规范》

### 附录C：联系方式
- 产品经理：XXX
- 技术负责人：XXX
- 商务联系人：XXX
