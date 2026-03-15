# SaaS仓配装一体化管理系统 Web管理后台UI设计文档

## 文档信息
- **项目名称**: SaaS仓配装一体化管理系统
- **文档版本**: v1.0
- **创建日期**: 2026-03-15
- **文档类型**: Web UI设计说明书
- **技术栈**: Vue3 + Element Plus + ECharts

---

## 一、设计概述

### 1.1 设计目标
为管理员、调度员、管理层提供高效、直观、美观的Web管理界面，实现订单全流程可视化管理、智能调度、数据分析和决策支持。

### 1.2 设计原则
- **信息密度优化**: 在有限屏幕空间展示关键信息，减少页面跳转
- **操作便捷性**: 常用操作一键触达，复杂操作分步引导
- **数据可视化**: 用图表直观展示趋势和对比，提升决策效率
- **响应式布局**: 适配1920×1080、1366×768等主流分辨率
- **一致性**: 统一的视觉语言、交互逻辑和反馈机制

### 1.3 目标用户
| 用户角色 | 核心场景 | 设计重点 |
|---------|---------|---------|
| 管理员 | 系统配置、用户管理、权限控制 | 安全性、完整性 |
| 调度员 | 订单管理、智能排单、任务监控 | 效率、实时性、容错性 |
| 主管/管理层 | 数据分析、成本管控、决策支持 | 可视化、洞察性 |

---

## 二、整体布局设计

### 2.1 布局结构
```
┌─────────────────────────────────────────────────────────────────┐
│                           顶部导航栏                               │
│  [Logo] 仓配装管理系统    |  搜索  |  通知  |  用户名 ▼  退出      │
├─────────┬───────────────────────────────────────────────────────┤
│         │                                                       │
│  左侧   │                     主内容区                           │
│  菜单   │                  (页面内容+右侧抽屉)                   │
│         │                                                       │
│ 首页    │                                                       │
│ 订单管理│                                                       │
│ 调度排单│                                                       │
│ 仓储管理│                                                       │
│ 配送管理│                                                       │
│ 安装管理│                                                       │
│ 费用管理│                                                       │
│ 报表分析│                                                       │
│ 用户管理│                                                       │
│         │                                                       │
└─────────┴───────────────────────────────────────────────────────┘
```

### 2.2 顶部导航栏设计

#### 组件结构
```vue
<template>
  <el-header class="app-header">
    <!-- 左侧 Logo 和标题 -->
    <div class="header-left">
      <img src="@/assets/logo.png" class="logo" />
      <span class="app-title">仓配装管理系统</span>
    </div>

    <!-- 中间 搜索和快捷操作 -->
    <div class="header-center">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索订单/客户/任务..."
        clearable
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 右侧 操作区 -->
    <div class="header-right">
      <!-- 全局通知 -->
      <el-badge :value="unreadCount" :hidden="unreadCount === 0">
        <el-button :icon="Bell" circle @click="showNotifications" />
      </el-badge>

      <!-- 快捷操作 -->
      <el-dropdown @command="handleQuickAction">
        <el-button :icon="Plus" circle />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="createOrder">新建订单</el-dropdown-item>
            <el-dropdown-item command="batchImport">批量导入</el-dropdown-item>
            <el-dropdown-item command="quickDispatch">快速排单</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 用户菜单 -->
      <el-dropdown @command="handleUserAction">
        <div class="user-profile">
          <el-avatar :size="32" :src="user.avatar">
            {{ user.name.charAt(0) }}
          </el-avatar>
          <span class="user-name">{{ user.name }}</span>
          <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="settings">系统设置</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>
```

### 2.3 左侧菜单设计

#### 菜单配置
```typescript
// src/router/menuConfig.ts
export const menuConfig: MenuItem[] = [
  {
    path: '/dashboard',
    icon: 'DataAnalysis',
    title: '首页',
    meta: { roles: ['admin', 'dispatcher', 'manager'] }
  },
  {
    path: '/orders',
    icon: 'Document',
    title: '订单管理',
    meta: { roles: ['admin', 'dispatcher', 'manager'] },
    children: [
      { path: '/orders/list', title: '订单列表' },
      { path: '/orders/create', title: '新建订单' },
      { path: '/orders/import', title: '批量导入' }
    ]
  },
  {
    path: '/dispatch',
    icon: 'Position',
    title: '调度排单',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/warehouse',
    icon: 'Box',
    title: '仓储管理',
    meta: { roles: ['admin', 'dispatcher'] },
    children: [
      { path: '/warehouse/inventory', title: '库存管理' },
      { path: '/warehouse/unload', title: '卸货管理' }
    ]
  },
  {
    path: '/delivery',
    icon: 'Van',
    title: '配送管理',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/install',
    icon: 'Tools',
    title: '安装管理',
    meta: { roles: ['admin', 'dispatcher'] }
  },
  {
    path: '/fees',
    icon: 'Money',
    title: '费用管理',
    meta: { roles: ['admin', 'manager'] }
  },
  {
    path: '/reports',
    icon: 'TrendCharts',
    title: '报表分析',
    meta: { roles: ['admin', 'manager'] },
    children: [
      { path: '/reports/orders', title: '订单报表' },
      { path: '/reports/workers', title: '人员报表' },
      { path: '/reports/fees', title: '费用报表' }
    ]
  },
  {
    path: '/users',
    icon: 'User',
    title: '用户管理',
    meta: { roles: ['admin'] }
  },
  {
    path: '/settings',
    icon: 'Setting',
    title: '系统设置',
    meta: { roles: ['admin'] }
  }
]
```

#### 菜单折叠状态
- 默认展开：显示图标+文字
- 折叠后：仅显示图标，鼠标悬停显示Tooltip
- 当前高亮：激活路由对应的菜单项高亮

---

## 三、核心页面设计

### 3.1 首页（Dashboard）

#### 页面布局
```
┌─────────────────────────────────────────────────────────────────┐
│  今日概览                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │今日订单  │  │进行中    │  │已完成    │  │待处理    │        │
│  │  156    │  │   23     │  │  128     │  │   15     │        │
│  │  ↑12%   │  │          │  │  ↑8%     │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
├─────────────────────────────────────────────────────────────────┤
│  订单趋势图（7天）              │  人员工作量排名                │
│  ┌────────────────────────┐    │  ┌──────────────────────┐   │
│  │      折线图            │    │  │  1. 张师傅  12单     │   │
│  │                        │    │  │  2. 李师傅  10单     │   │
│  │                        │    │  │  3. 王师傅  9单      │   │
│  └────────────────────────┘    │  └──────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  待办任务                                                        │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 订单号    客户    类型    状态    操作                    │  │
│  │ SO001    张三   配送    待派单   [派单]                  │  │
│  │ SO002    李四   安装    进行中   [详情]                  │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

#### 数据卡片设计
```vue
<template>
  <div class="stat-card">
    <div class="stat-header">
      <span class="stat-title">{{ title }}</span>
      <el-icon :class="iconClass"><component :is="icon" /></el-icon>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-footer">
      <span class="stat-trend" :class="trendClass">
        {{ trend > 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}%
      </span>
      <span class="stat-label">较昨日</span>
    </div>
  </div>
</template>
```

### 3.2 订单列表页

#### 页面布局
```
┌─────────────────────────────────────────────────────────────────┐
│  订单管理  > 订单列表                                             │
├─────────────────────────────────────────────────────────────────┤
│  搜索栏                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 订单号 [______]  客户 [______]  状态 [全部▼]              │   │
│  │ 日期 [______ 至 ______]  [查询] [重置] [导出]             │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  操作栏                                                          │
│  [新建订单] [批量导入] [批量派单] [取消订单] [更多▼]            │
├─────────────────────────────────────────────────────────────────┤
│  数据表格                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ □  订单号   客户    地址         状态    金额    操作   │   │
│  │ ☑  SO001    张三   朝阳区建国路   待派单   ¥680   详情 │   │
│  │     SO002    李四   海淀区中关村   配送中   ¥520   详情 │   │
│  │    SO003    王五   丰台区方庄    安装中   ¥850   详情 │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  分页 (共 156 条)  [上一页] 1 / 16  [下一页]                     │
└─────────────────────────────────────────────────────────────────┘
```

#### 表格列配置
```typescript
// 订单列表列配置
export const orderColumns: Column[] = [
  {
    type: 'selection',
    width: 50,
    fixed: 'left'
  },
  {
    prop: 'orderNo',
    label: '订单号',
    width: 150,
    fixed: 'left',
    render: (row) => (
      <el-link type="primary" onClick={() => goToDetail(row.id)}>
        {row.orderNo}
      </el-link>
    )
  },
  {
    prop: 'customerName',
    label: '客户',
    width: 100
  },
  {
    prop: 'customerPhone',
    label: '联系电话',
    width: 120
  },
  {
    prop: 'address',
    label: '配送地址',
    minWidth: 200,
    ellipsis: true,
    render: (row) => (
      <el-tooltip content={row.address} placement="top">
        <span>{row.address}</span>
      </el-tooltip>
    )
  },
  {
    prop: 'appointmentTime',
    label: '预约时间',
    width: 160,
    formatter: (row) => formatDate(row.appointmentTime, 'YYYY-MM-DD HH:mm')
  },
  {
    prop: 'status',
    label: '状态',
    width: 100,
    render: (row) => <StatusTag status={row.status} />
  },
  {
    prop: 'totalAmount',
    label: '金额',
    width: 100,
    align: 'right',
    formatter: (row) => `¥${row.totalAmount.toFixed(2)}`
  },
  {
    prop: 'createTime',
    label: '创建时间',
    width: 160,
    formatter: (row) => formatDate(row.createTime, 'YYYY-MM-DD HH:mm')
  },
  {
    prop: 'action',
    label: '操作',
    width: 200,
    fixed: 'right',
    render: (row) => (
      <el-space>
        <el-link type="primary" onClick={() => goToDetail(row.id)}>详情</el-link>
        {row.status === 'pending' && (
          <el-link type="primary" onClick={() => dispatchOrder(row.id)}>派单</el-link>
        )}
        {row.status === 'pending' && (
          <el-link type="danger" onClick={() => cancelOrder(row.id)}>取消</el-link>
        )}
      </el-space>
    )
  }
]
```

### 3.3 订单详情页

#### 页面布局（左右分栏）
```
┌─────────────────────────────────────────────────────────────────┐
│  订单管理  > 订单详情  > SO20260312000001                         │
│  [返回列表] [打印订单] [取消订单]                                 │
├───────────────────────────┬───────────────────────────────────┤
│                           │  订单状态流程                         │
│  基本信息                  │  ┌────────────────────────────┐   │
│  ┌───────────────────────┐ │  │  ● 待派单                  │   │
│  │ 订单号: SO001         │ │  │    ↓                      │   │
│  │ 客户: 张三            │ │  │  ● 配送中  (当前)        │   │
│  │ 电话: 13800138000     │ │  │    ↓                      │   │
│  │ 地址: 朝阳区建国路    │ │  │  ○ 安装中                 │   │
│  │ 预约: 2026-03-15 10:00│ │  │    ↓                      │   │
│  │ 金额: ¥680.00         │ │  │  ○ 已完成                 │   │
│  └───────────────────────┘ │  └────────────────────────────┘   │
│                           │                                     │
│  商品信息                  │  任务列表                           │
│  ┌───────────────────────┐ │  ┌────────────────────────────┐   │
│  │ 商品名称  数量  单价   │ │  │ 任务编号    类型  执行人    │   │
│  │ 空调挂机   2台  ¥200  │ │  │ TK001      卸货  王大力    │   │
│  │ 智能门锁   1把  ¥280  │ │  │ TK002      配送  张小明    │   │
│  └───────────────────────┘ │  │ TK003      安装  李师傅    │   │
│                           │  └────────────────────────────┘   │
│  费用明细                  │                                     │
│  ┌───────────────────────┐ │  操作日志                           │
│  │ 配送费: ¥120.00       │ │  ┌────────────────────────────┐   │
│  │ 安装费: ¥480.00       │ │  │ 03-15 09:30  创建订单      │   │
│  │ 卸货费: ¥80.00        │ │  │ 03-15 09:35  自动派单      │   │
│  │ 合计:   ¥680.00       │ │  │ 03-15 10:00  开始配送      │   │
│  └───────────────────────┘ │  └────────────────────────────┘   │
└───────────────────────────┴───────────────────────────────────┘
```

#### 状态流程组件
```vue
<template>
  <el-steps :active="currentStep" align-center finish-status="success">
    <el-step
      v-for="(step, index) in steps"
      :key="index"
      :title="step.title"
      :description="step.description"
      :status="getStatus(index)"
    >
      <template #icon>
        <el-icon><component :is="step.icon" /></el-icon>
      </template>
    </el-step>
  </el-steps>
</template>

<script setup lang="ts">
const steps = [
  { title: '待派单', description: '等待分配', icon: 'Clock' },
  { title: '配送中', description: '正在配送', icon: 'Van' },
  { title: '安装中', description: '正在安装', icon: 'Tools' },
  { title: '已完成', description: '订单完成', icon: 'CircleCheck' }
]
</script>
```

### 3.4 调度排单页

#### 页面布局
```
┌─────────────────────────────────────────────────────────────────┐
│  调度排单                                                        │
├─────────────────────────────────────────────────────────────────┤
│  [智能排单] [手动排单] [排单规则]                                  │
│                                                                   │
│  智能排单模式                                                     │
│  ┌───────────────────┬─────────────────────────────────────────┐ │
│  │  选择待排单订单    │           排单设置                        │ │
│  │  ┌─────────────┐  │  ┌─────────────────────────────────┐   │ │
│  │  │ ☑ SO001    │  │  │ 任务类型: [卸货▼]                │   │ │
│  │  │ ☑ SO002    │  │  │ 派单日期: [2026-03-15]           │   │ │
│  │  │ ☑ SO003    │  │  │ 排单规则:                        │   │ │
│  │  │ ☐ SO004    │  │  │   ☑ 区域匹配                     │   │ │
│  │  │ ☐ SO005    │  │  │   ☑ 技能匹配                     │   │ │
│  │  └─────────────┘  │  │   ☑ 工作量均衡                   │   │ │
│  │  [全选] [反选]    │  │   ☐ 距离优先                     │   │ │
│  │                  │  │                                   │   │ │
│  │  已选 3 个订单    │  │  [开始排单] [预览结果]            │   │ │
│  └───────────────────┘  └─────────────────────────────────────────┘ │
│                                                                   │
│  排单结果预览                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 订单号    推荐执行人    距离    工作量    评分    操作   │   │
│  │ SO001     王师傅       3.2km   8单       4.8     [调整] │   │
│  │ SO002     张师傅       5.1km   6单       4.5     [调整] │   │
│  │ SO003     李师傅       2.8km   9单       4.9     [调整] │   │
│  └─────────────────────────────────────────────────────────┘   │
│  [确认排单] [重新排单]                                           │
└─────────────────────────────────────────────────────────────────┘
```

#### 地图排单视图
```vue
<template>
  <div class="dispatch-map-view">
    <div class="map-container">
      <!-- 高德地图 -->
      <div id="amap" class="amap"></div>

      <!-- 图例 -->
      <div class="map-legend">
        <div class="legend-item">
          <span class="legend-color" style="background: #67C23A"></span>
          <span>仓库</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #409EFF"></span>
          <span>订单</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #E6A23C"></span>
          <span>执行人</span>
        </div>
      </div>

      <!-- 侧边订单列表 -->
      <div class="order-list">
        <el-scrollbar height="calc(100vh - 200px)">
          <div
            v-for="order in orders"
            :key="order.id"
            class="order-item"
            :class="{ active: selectedOrderId === order.id }"
            @click="selectOrder(order)"
          >
            <div class="order-no">{{ order.orderNo }}</div>
            <div class="order-address">{{ order.address }}</div>
            <el-tag :type="getStatusType(order.status)">
              {{ getStatusText(order.status) }}
            </el-tag>
          </div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>
```

### 3.5 报表分析页

#### 页面布局
```
┌─────────────────────────────────────────────────────────────────┐
│  报表分析  > 订单报表                                             │
├─────────────────────────────────────────────────────────────────┤
│  筛选条件                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 时间范围: [最近7天▼]  自定义: [____至____]                │   │
│  │ 分组维度: [按天▼]  状态: [全部▼]                          │   │
│  │ [查询] [导出Excel] [导出PDF]                               │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  统计卡片                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │订单总量  │  │完成率    │  │总金额    │  │平均金额  │        │
│  │  1,256  │  │  89.5%  │  │¥456,780 │  │¥363.50  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
├─────────────────────────────────────────────────────────────────┤
│  趋势图表（左右布局）                                            │
│  ┌────────────────────────────┐  ┌───────────────────────────┐ │
│  │  订单数量趋势              │  │  订单金额趋势             │ │
│  │   [折线图]                 │  │   [折线图]                │ │
│  │                            │  │                           │ │
│  └────────────────────────────┘  └───────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  状态分布（饼图）              │  完成率趋势（柱状图）            │
│  ┌────────────────────┐        │  ┌────────────────────────┐  │ │
│  │   [环形图]         │        │  │   [柱状图]             │  │ │
│  │                    │        │  │                        │  │ │
│  └────────────────────┘        │  └────────────────────────┘  │ │
└─────────────────────────────────────────────────────────────────┘
```

#### ECharts 图表配置
```typescript
// 订单趋势图配置
export const getTrendChartOption = (data: TrendData) => ({
  title: {
    text: '订单趋势',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['订单数量', '订单金额'],
    bottom: 0
  },
  xAxis: {
    type: 'category',
    data: data.dates
  },
  yAxis: [
    {
      type: 'value',
      name: '订单数量',
      position: 'left'
    },
    {
      type: 'value',
      name: '金额（元）',
      position: 'right'
    }
  ],
  series: [
    {
      name: '订单数量',
      type: 'line',
      data: data.counts,
      smooth: true,
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
          ]
        }
      }
    },
    {
      name: '订单金额',
      type: 'line',
      yAxisIndex: 1,
      data: data.amounts,
      smooth: true,
      itemStyle: {
        color: '#67C23A'
      }
    }
  ]
})
```

---

## 四、通用组件设计

### 4.1 数据表格组件 (DataTable)

#### 功能特性
- 支持排序、筛选、分页
- 支持多选、固定列、行高亮
- 支持自定义渲染
- 支持导出Excel

```vue
<template>
  <div class="data-table">
    <!-- 工具栏 -->
    <div v-if="$slots.toolbar" class="table-toolbar">
      <slot name="toolbar" />
    </div>

    <!-- 表格 -->
    <el-table
      ref="tableRef"
      :data="data"
      :loading="loading"
      :stripe="stripe"
      :border="border"
      :height="height"
      :row-key="rowKey"
      @selection-change="handleSelectionChange"
      @sort-change="handleSortChange"
    >
      <!-- 多选列 -->
      <el-table-column
        v-if="selection"
        type="selection"
        width="50"
        fixed="left"
      />

      <!-- 数据列 -->
      <el-table-column
        v-for="col in columns"
        :key="col.prop"
        :prop="col.prop"
        :label="col.label"
        :width="col.width"
        :min-width="col.minWidth"
        :fixed="col.fixed"
        :sortable="col.sortable"
        :align="col.align || 'left'"
        :formatter="col.formatter"
      >
        <template #default="{ row, column, $index }">
          <slot
            v-if="col.render"
            :name="col.prop"
            :row="row"
            :column="column"
            :index="$index"
          >
            {{ col.render(h, { row, column, $index }) }}
          </slot>
          <span v-else>{{ row[col.prop] }}</span>
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column
        v-if="$slots.actions"
        label="操作"
        width="150"
        fixed="right"
      >
        <template #default="{ row }">
          <slot name="actions" :row="row" />
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div v-if="pagination" class="table-pagination">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="pagination.pageSizes || [10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>
```

### 4.2 搜索表单组件 (SearchForm)

#### 功能特性
- 支持多种表单项类型（输入、选择、日期范围等）
- 支持折叠展开
- 支持重置、查询、导出

```vue
<template>
  <div class="search-form">
    <el-form
      ref="formRef"
      :model="formData"
      :inline="inline"
      :label-width="labelWidth"
    >
      <el-row :gutter="20">
        <el-col
          v-for="item in formItems"
          :key="item.prop"
          :span="item.span || 6"
        >
          <el-form-item :label="item.label" :prop="item.prop">
            <!-- 输入框 -->
            <el-input
              v-if="item.type === 'input'"
              v-model="formData[item.prop]"
              :placeholder="item.placeholder"
              clearable
            />

            <!-- 选择框 -->
            <el-select
              v-else-if="item.type === 'select'"
              v-model="formData[item.prop]"
              :placeholder="item.placeholder"
              clearable
            >
              <el-option
                v-for="opt in item.options"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>

            <!-- 日期选择 -->
            <el-date-picker
              v-else-if="item.type === 'date'"
              v-model="formData[item.prop]"
              type="date"
              :placeholder="item.placeholder"
              clearable
            />

            <!-- 日期范围 -->
            <el-date-picker
              v-else-if="item.type === 'daterange'"
              v-model="formData[item.prop]"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              clearable
            />
          </el-form-item>
        </el-col>

        <!-- 操作按钮 -->
        <el-col :span="6">
          <el-form-item>
            <el-space>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>
                查询
              </el-button>
              <el-button @click="handleReset">
                <el-icon><RefreshLeft /></el-icon>
                重置
              </el-button>
              <el-button v-if="showExport" @click="handleExport">
                <el-icon><Download /></el-icon>
                导出
              </el-button>
            </el-space>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>
```

### 4.3 状态标签组件 (StatusTag)

#### 状态映射配置
```typescript
// 订单状态配置
export const orderStatusConfig = {
  pending: {
    label: '待派单',
    type: 'info' as const,
    icon: 'Clock'
  },
  assigned: {
    label: '已派单',
    type: 'primary' as const,
    icon: 'Check'
  },
  delivering: {
    label: '配送中',
    type: 'warning' as const,
    icon: 'Van'
  },
  installing: {
    label: '安装中',
    type: 'warning' as const,
    icon: 'Tools'
  },
  completed: {
    label: '已完成',
    type: 'success' as const,
    icon: 'CircleCheck'
  },
  cancelled: {
    label: '已取消',
    type: 'danger' as const,
    icon: 'CircleClose'
  }
}
```

#### 组件实现
```vue
<template>
  <el-tag :type="statusConfig[type]" effect="dark">
    <el-icon v-if="showIcon">
      <component :is="statusConfig.icon" />
    </el-icon>
    <span>{{ statusConfig.label }}</span>
  </el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { orderStatusConfig } from '@/config/statusConfig'

const props = defineProps<{
  type: keyof typeof orderStatusConfig
  showIcon?: boolean
}>()

const statusConfig = computed(() => orderStatusConfig[props.type])
</script>
```

---

## 五、交互设计规范

### 5.1 加载状态

#### 全局加载
```typescript
import { ElLoading } from 'element-plus'

const showLoading = (text = '加载中...') => {
  return ElLoading.service({
    lock: true,
    text,
    background: 'rgba(0, 0, 0, 0.7)'
  })
}

const hideLoading = (instance: ReturnType<typeof ElLoading.service>) => {
  instance.close()
}
```

#### 局部加载
```vue
<el-button :loading="loading" @click="handleSubmit">
  提交
</el-button>
```

### 5.2 消息提示

#### 成功提示
```typescript
ElMessage.success('操作成功')
```

#### 警告提示
```typescript
ElMessage.warning('请检查输入')
```

#### 错误提示
```typescript
ElMessage.error('操作失败，请重试')
```

#### 确认对话框
```typescript
ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning'
})
  .then(() => {
    // 确认操作
  })
  .catch(() => {
    // 取消操作
  })
```

### 5.3 表单验证

#### 验证规则
```typescript
// 订单表单验证规则
export const orderFormRules = {
  customerName: [
    { required: true, message: '请输入客户姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  customerPhone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号',
      trigger: 'blur'
    }
  ],
  address: [
    { required: true, message: '请输入配送地址', trigger: 'blur' },
    { min: 5, message: '地址不能少于5个字符', trigger: 'blur' }
  ],
  appointmentTime: [
    {
      type: 'date',
      required: true,
      message: '请选择预约时间',
      trigger: 'change'
    }
  ],
  products: [
    {
      type: 'array',
      required: true,
      message: '请至少添加一个商品',
      trigger: 'change'
    }
  ]
}
```

---

## 六、响应式设计

### 6.1 断点定义
```scss
$breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 992px,
  xl: 1200px,
  xxl: 1600px
);
```

### 6.2 媒体查询示例
```scss
// 小屏幕隐藏某些列
@media (max-width: 768px) {
  .data-table {
    .hide-on-mobile {
      display: none;
    }
  }
}

// 平板端调整布局
@media (min-width: 768px) and (max-width: 992px) {
  .dashboard {
    .stat-card {
      width: 50%;
    }
  }
}
```

---

## 七、性能优化

### 7.1 组件懒加载
```typescript
const routes = [
  {
    path: '/orders',
    component: () => import('@/views/Orders/index.vue')
  }
]
```

### 7.2 图片懒加载
```vue
<img v-lazy="imageUrl" alt="商品图片" />
```

### 7.3 虚拟滚动
```vue
<el-virtual-list
  :data="largeData"
  :item-size="50"
  height="400px"
>
  <template #default="{ item }">
    <div>{{ item }}</div>
  </template>
</el-virtual-list>
```

---

## 八、设计规范总结

### 8.1 颜色规范
```scss
// 主色调
$primary-color: #409EFF;
$success-color: #67C23A;
$warning-color: #E6A23C;
$danger-color: #F56C6C;
$info-color: #909399;

// 中性色
$text-primary: #303133;
$text-regular: #606266;
$text-secondary: #909399;
$text-placeholder: #C0C4CC;

// 边框色
$border-base: #DCDFE6;
$border-light: #E4E7ED;
$border-lighter: #EBEEF5;
$border-extra-light: #F2F6FC;

// 背景色
$bg-color: #F5F7FA;
$bg-color-page: #FFFFFF;
```

### 8.2 间距规范
```scss
// 间距系统
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
```

### 8.3 字体规范
```scss
// 字体大小
$font-size-xs: 12px;
$font-size-sm: 13px;
$font-size-base: 14px;
$font-size-md: 16px;
$font-size-lg: 18px;
$font-size-xl: 20px;

// 字重
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-bold: 600;
```

---

## 附录

### 附录A：图标库
使用 Element Plus 内置图标，自定义图标使用 SVG

### 附录B：参考资源
- Element Plus: https://element-plus.org/
- ECharts: https://echarts.apache.org/
