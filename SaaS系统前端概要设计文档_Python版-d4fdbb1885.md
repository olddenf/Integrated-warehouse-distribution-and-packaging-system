# SaaS仓配装一体化管理系统前端概要设计文档

## 文档信息
- **项目名称**: SaaS仓配装一体化管理系统
- **文档版本**: v1.0
- **创建日期**: 2026-03-15
- **文档类型**: 前端概要设计说明书
- **技术栈**: Vue3 + TypeScript + Vite + Element Plus/Vant

---

## 一、设计概述

### 1.1 设计目标
本前端概要设计基于后端概要设计和需求文档，定义前端整体架构、技术选型、模块划分、状态管理、路由设计等，为前端开发提供清晰的指导方针。

### 1.2 设计原则
- **响应式优先**: Web端适配主流屏幕分辨率，H5端适配主流移动设备
- **组件化开发**: 高度封装通用组件，提升开发效率
- **类型安全**: 全面使用TypeScript，减少运行时错误
- **用户体验**: 关注操作流畅性、加载性能、错误提示友好性
- **可维护性**: 代码规范统一，模块职责清晰
- **渐进增强**: 核心功能优先，非核心功能可降级处理

---

## 二、前端整体架构

### 2.1 架构图
```
┌─────────────────────────────────────────────────────────────────┐
│                           浏览器/移动端                            │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                         前端应用层                                │
├──────────────────────────────┬───────────────────────────────────┤
│      Web管理端(PC)           │        H5移动端(三端)              │
│  ┌──────────────────────┐   │   ┌──────────────────────────┐   │
│  │   Vue3 应用容器      │   │   │   Vue3 应用容器          │   │
│  │   - Vue Router       │   │   │   - Vue Router           │   │
│  │   - Pinia (状态管理) │   │   │   - Pinia (状态管理)     │   │
│  │   - Axios (HTTP)     │   │   │   - Axios (HTTP)         │   │
│  └──────────────────────┘   │   └──────────────────────────┘   │
│                              │                                    │
│  ┌──────────────────────┐   │   ┌──────────────────────────┐   │
│  │   Element Plus 组件库│   │   │   Vant4 组件库           │   │
│  │   - 表格/表单/弹窗   │   │   │   - 按钮/表单/上传       │   │
│  └──────────────────────┘   │   └──────────────────────────┘   │
└──────────────────────────────┴───────────────────────────────────┘
                                    ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      后端API层 (FastAPI)                         │
│         /api/v1/orders, /api/v1/tasks, /api/v1/dispatch        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选型

| 层级 | 技术选型 | 版本 | 选型理由 |
|------|---------|------|---------|
| **核心框架** | Vue3 | 3.3+ | 响应式系统性能优化，Composition API代码组织更优 |
| **开发语言** | TypeScript | 5.0+ | 类型安全，IDE支持完善，减少运行时错误 |
| **构建工具** | Vite | 5.0+ | 开发启动快，HMR即时更新，生产构建性能优 |
| **Web UI库** | Element Plus | 2.4+ | 组件丰富，文档完善，管理后台首选 |
| **H5 UI库** | Vant4 | 4.0+ | 移动端组件完善，三端复用性高 |
| **状态管理** | Pinia | 2.1+ | Vue官方推荐，API简洁，TypeScript支持好 |
| **路由管理** | Vue Router | 4.2+ | Vue3官方路由，动态路由支持好 |
| **HTTP客户端** | Axios | 1.6+ | 拦截器功能强大，取消请求、并发控制方便 |
| **图表库** | ECharts | 5.4+ | 交互丰富，性能优秀，报表首选 |
| **地图组件** | 高德地图JS API | 2.0+ | 国内最稳定，文档完善，后端已选型 |
| **代码规范** | ESLint + Prettier | 最新 | 代码风格统一，自动格式化 |
| **测试框架** | Vitest + Vue Test Utils | 最新 | Vite原生支持，测试速度快 |

### 2.3 浏览器兼容性

| 平台 | 支持版本 | 说明 |
|------|---------|------|
| Chrome | 90+ | 主力浏览器 |
| Edge | 90+ | 主力浏览器 |
| Firefox | 88+ | 兼容性良好 |
| Safari | 14+ | Mac用户 |
| IE | 不支持 | Vue3不支持IE |

**移动端兼容性**:
- iOS: 12.0+
- Android: 8.0+
- 微信浏览器: 7.0+
- 企业微信/钉钉容器: 全版本支持

---

## 三、项目目录结构设计

### 3.1 Web管理后台目录结构
```
saas-warehouse-web/
├── public/                      # 静态资源
│   ├── favicon.ico
│   └── logo.png
├── src/
│   ├── api/                     # API接口层
│   │   ├── index.ts             # Axios实例配置
│   │   ├── orders.ts            # 订单接口
│   │   ├── tasks.ts             # 任务接口
│   │   ├── dispatch.ts          # 调度接口
│   │   ├── warehouse.ts         # 仓储接口
│   │   ├── fees.ts              # 费用接口
│   │   ├── reports.ts           # 报表接口
│   │   └── users.ts             # 用户接口
│   ├── assets/                  # 资源文件
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │       ├── index.scss       # 全局样式
│   │       ├── variables.scss   # 样式变量
│   │       └── mixins.scss      # 样式混入
│   ├── components/              # 通用组件
│   │   ├── layout/              # 布局组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   └── AppMain.vue
│   │   ├── business/            # 业务组件
│   │   │   ├── OrderCard.vue
│   │   │   ├── TaskTimeline.vue
│   │   │   └── DispatchMap.vue
│   │   └── common/             # 通用组件
│   │       ├── DataTable.vue
│   │       ├── SearchForm.vue
│   │       ├── UploadImage.vue
│   │       └── StatusTag.vue
│   ├── composables/             # 组合式函数
│   │   ├── useAuth.ts           # 认证相关
│   │   ├── useTable.ts          # 表格相关
│   │   ├── useForm.ts           # 表单相关
│   │   └── useMap.ts            # 地图相关
│   ├── router/                  # 路由配置
│   │   ├── index.ts             # 路由入口
│   │   ├── modules/
│   │   │   ├── orders.ts        # 订单路由
│   │   │   ├── tasks.ts         # 任务路由
│   │   │   ├── dispatch.ts      # 调度路由
│   │   │   ├── warehouse.ts     # 仓储路由
│   │   │   ├── fees.ts          # 费用路由
│   │   │   ├── reports.ts       # 报表路由
│   │   │   └── users.ts         # 用户路由
│   │   └── guards.ts            # 路由守卫
│   ├── stores/                  # Pinia状态管理
│   │   ├── index.ts
│   │   ├── auth.ts              # 认证状态
│   │   ├── user.ts              # 用户状态
│   │   ├── order.ts             # 订单状态
│   │   └── app.ts               # 应用状态
│   ├── types/                   # TypeScript类型定义
│   │   ├── api.d.ts             # API类型
│   │   ├── order.d.ts           # 订单类型
│   │   ├── task.d.ts            # 任务类型
│   │   └── common.d.ts          # 通用类型
│   ├── utils/                   # 工具函数
│   │   ├── request.ts           # 请求封装
│   │   ├── auth.ts              # 认证工具
│   │   ├── storage.ts           # 本地存储
│   │   ├── validate.ts          # 表单验证
│   │   ├── format.ts            # 格式化
│   │   └── map.ts               # 地图工具
│   ├── views/                   # 页面视图
│   │   ├── Login/               # 登录页
│   │   ├── Dashboard/           # 首页
│   │   ├── Orders/              # 订单管理
│   │   ├── Dispatch/            # 调度排单
│   │   ├── Warehouse/           # 仓储管理
│   │   ├── Fees/                # 费用管理
│   │   ├── Reports/             # 报表分析
│   │   └── Users/               # 用户管理
│   ├── App.vue                  # 根组件
│   └── main.ts                  # 应用入口
├── tests/                       # 测试文件
├── .env.development             # 开发环境变量
├── .env.production              # 生产环境变量
├── .eslintrc.js                 # ESLint配置
├── .prettierrc.js               # Prettier配置
├── tsconfig.json                # TypeScript配置
├── vite.config.ts               # Vite配置
├── package.json
└── README.md
```

### 3.2 H5移动端目录结构
```
saas-warehouse-h5/
├── src/
│   ├── api/                     # API接口层
│   ├── assets/
│   ├── components/              # H5专用组件
│   │   ├── layout/
│   │   ├── business/            # 业务组件
│   │   │   ├── TaskList.vue     # 任务列表
│   │   │   ├── TaskDetail.vue   # 任务详情
│   │   │   ├── PhotoUpload.vue  # 照片上传
│   │   │   └── MapPicker.vue    # 地图选点
│   │   └── common/
│   ├── composables/             # H5专用组合式函数
│   │   ├── useGeolocation.ts    # 定位
│   │   ├── useCamera.ts         # 拍照
│   │   └── useUpload.ts         # 上传
│   ├── router/                  # 路由配置
│   ├── stores/                  # 状态管理
│   ├── types/                   # 类型定义
│   ├── utils/                   # 工具函数
│   │   ├── map.ts               # 地图封装
│   │   └── bridge.ts            # App Bridge
│   ├── views/                   # 页面视图
│   │   ├── login/               # 登录
│   │   ├── unloader/            # 卸货端
│   │   ├── driver/              # 司机端
│   │   ├── installer/           # 安装端
│   │   └── profile/             # 个人中心
│   ├── App.vue
│   └── main.ts
└── ...
```

---

## 四、核心模块设计

### 4.1 认证模块

#### 认证流程
```
用户输入账号密码
    ↓
调用 /api/v1/auth/login
    ↓
后端返回 access_token + user_info
    ↓
前端存储 token (localStorage + Pinia)
    ↓
Axios 拦截器自动添加 token 到请求头
    ↓
路由守卫检查 token 有效性
    ↓
访问受保护页面
```

#### Token 管理
```typescript
// src/stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const user = ref<User | null>(null)

  // 登录
  const login = async (credentials: LoginRequest) => {
    const { data } = await api.auth.login(credentials)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', token.value)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  // 登出
  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  // 检查token是否有效
  const isValid = computed(() => !!token.value)

  return { token, user, login, logout, isValid }
})
```

#### 路由守卫
```typescript
// src/router/guards.ts
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')

  // 白名单路由不需要认证
  const whiteList = ['/login', '/forgot-password']
  if (whiteList.includes(to.path)) {
    next()
    return
  }

  // 未登录跳转登录页
  if (!token) {
    next(`/login?redirect=${to.path}`)
    return
  }

  // 已登录访问登录页跳转首页
  if (to.path === '/login' && authStore.isValid) {
    next('/')
    return
  }

  // 权限检查
  if (to.meta.roles && !to.meta.roles.includes(authStore.user?.role)) {
    ElMessage.error('权限不足')
    next('/403')
    return
  }

  next()
})
```

### 4.2 请求模块设计

#### Axios 配置
```typescript
// src/api/index.ts
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    const { code, message, data } = response.data
    if (code === 200) {
      return { data, message }
    } else {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message || '请求失败'))
    }
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          useAuthStore().logout()
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(data.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

export default instance
```

### 4.3 状态管理设计

#### 认证状态 (auth.ts)
```typescript
interface AuthState {
  token: string
  user: User | null
  permissions: string[]
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    permissions: []
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    hasPermission: (state) => (permission: string) => {
      return state.permissions.includes(permission)
    }
  },

  actions: {
    async login(credentials: LoginRequest) {
      const response = await api.auth.login(credentials)
      this.token = response.data.access_token
      this.user = response.data.user
      this.permissions = response.data.permissions || []
      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    async logout() {
      await api.auth.logout()
      this.token = ''
      this.user = null
      this.permissions = []
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
  }
})
```

#### 订单状态 (order.ts)
```typescript
export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [] as Order[],
    currentOrder: null as Order | null,
    loading: false,
    filters: {
      status: '',
      customerName: '',
      dateRange: []
    } as OrderFilters
  }),

  actions: {
    async fetchOrders(params?: OrderQuery) {
      this.loading = true
      try {
        const { data } = await api.orders.getList(params)
        this.orders = data.items
        return data
      } finally {
        this.loading = false
      }
    },

    async fetchOrderDetail(id: string) {
      const { data } = await api.orders.getDetail(id)
      this.currentOrder = data
      return data
    },

    async createOrder(order: OrderCreate) {
      const { data } = await api.orders.create(order)
      this.orders.unshift(data)
      return data
    },

    async updateOrder(id: string, data: OrderUpdate) {
      const response = await api.orders.update(id, data)
      const index = this.orders.findIndex(o => o.id === id)
      if (index !== -1) {
        this.orders[index] = { ...this.orders[index], ...data }
      }
      return response.data
    },

    async cancelOrder(id: string, reason: string) {
      await api.orders.cancel(id, reason)
      const order = this.orders.find(o => o.id === id)
      if (order) {
        order.status = 'cancelled'
      }
    }
  }
})
```

### 4.4 路由设计

#### 路由模块化设计
```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/index.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard/index.vue'),
        meta: { title: '首页' }
      },
      {
        path: '/orders',
        name: 'Orders',
        component: () => import('@/views/Orders/index.vue'),
        meta: { title: '订单管理' }
      },
      {
        path: '/orders/:id',
        name: 'OrderDetail',
        component: () => import('@/views/Orders/detail.vue'),
        meta: { title: '订单详情' }
      },
      {
        path: '/dispatch',
        name: 'Dispatch',
        component: () => import('@/views/Dispatch/index.vue'),
        meta: { title: '调度排单', roles: ['admin', 'dispatcher'] }
      },
      {
        path: '/warehouse',
        name: 'Warehouse',
        component: () => import('@/views/Warehouse/index.vue'),
        meta: { title: '仓储管理' }
      },
      {
        path: '/fees',
        name: 'Fees',
        component: () => import('@/views/Fees/index.vue'),
        meta: { title: '费用管理' }
      },
      {
        path: '/reports',
        name: 'Reports',
        component: () => import('@/views/Reports/index.vue'),
        meta: { title: '报表分析' }
      },
      {
        path: '/users',
        name: 'Users',
        component: () => import('@/views/Users/index.vue'),
        meta: { title: '用户管理', roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

---

## 五、组件设计规范

### 5.1 组件命名规范
- **页面组件**: PascalCase，如 `OrderList.vue`
- **业务组件**: PascalCase，如 `OrderCard.vue`
- **通用组件**: PascalCase，如 `Button.vue`、`DataTable.vue`
- **工具函数**: camelCase，如 `formatDate.ts`

### 5.2 组件目录结构
```
components/
├── common/              # 通用组件
│   ├── Button/
│   │   ├── Button.vue
│   │   ├── Button.test.ts
│   │   ├── types.ts
│   │   └── README.md
│   └── DataTable/
├── business/            # 业务组件
│   ├── OrderCard/
│   └── TaskTimeline/
└── layout/              # 布局组件
    ├── AppHeader/
    └── AppSidebar/
```

### 5.3 组件Props类型定义
```typescript
// src/components/common/DataTable/types.ts
export interface DataTableProps {
  data: any[]
  columns: Column[]
  loading?: boolean
  pagination?: PaginationConfig
  selection?: boolean
  stripe?: boolean
  border?: boolean
}

export interface Column {
  prop: string
  label: string
  width?: number
  minWidth?: number
  align?: 'left' | 'center' | 'right'
  fixed?: 'left' | 'right'
  sortable?: boolean
  formatter?: (row: any, column: Column, cellValue: any) => string
  render?: (h: any, { row, column, $index }: any) => VNode
}

export interface PaginationConfig {
  total: number
  pageSize: number
  currentPage: number
  pageSizes?: number[]
}
```

---

## 六、性能优化策略

### 6.1 路由懒加载
```typescript
const routes = [
  {
    path: '/orders',
    component: () => import('@/views/Orders/index.vue') // 懒加载
  }
]
```

### 6.2 组件懒加载
```vue
<template>
  <div>
    <el-dialog v-model="visible">
      <Suspense>
        <template #default>
          <OrderDetail :order-id="orderId" />
        </template>
        <template #fallback>
          <div class="loading">加载中...</div>
        </template>
      </Suspense>
    </el-dialog>
  </div>
</template>
```

### 6.3 图片懒加载
```typescript
// src/directives/lazyLoad.ts
import { useIntersectionObserver } from '@vueuse/core'

export default {
  mounted(el: HTMLImageElement, binding) {
    const { stop } = useIntersectionObserver(
      el,
      ([{ isIntersecting }]) => {
        if (isIntersecting) {
          el.src = binding.value
          stop()
        }
      }
    )
  }
}
```

### 6.4 列表虚拟滚动
```vue
<template>
  <el-virtual-list
    :data="largeData"
    :item-size="50"
    height="400px"
  >
    <template #default="{ item }">
      <div>{{ item }}</div>
    </template>
  </el-virtual-list>
</template>
```

### 6.5 请求防抖和节流
```typescript
// src/utils/debounce.ts
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout> | null = null
  return function(this: any, ...args: Parameters<T>) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 使用
const handleSearch = debounce((keyword: string) => {
  search(keyword)
}, 500)
```

---

## 七、开发规范

### 7.1 代码风格
- 使用 ESLint + Prettier 统一代码风格
- 使用 Husky + lint-staged 提交前检查
- 组件使用 Composition API + `<script setup>`
- 优先使用组合式函数复用逻辑

### 7.2 Git提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

### 7.3 注释规范
```typescript
/**
 * 订单列表查询
 * @param params 查询参数
 * @returns 订单列表数据
 */
export async function getOrderList(params: OrderQuery): Promise<OrderListResponse> {
  // ...
}
```

---

## 八、部署方案

### 8.1 构建配置
```typescript
// vite.config.ts
export default defineConfig({
  base: '/saas-warehouse/',
  build: {
    outDir: 'dist',
    assetsDir: 'static',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'element-plus': ['element-plus'],
          'echarts': ['echarts']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

### 8.2 环境变量
```bash
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=仓配装管理系统(开发)
VITE_MAP_API_KEY=your-dev-key

# .env.production
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
VITE_APP_TITLE=仓配装管理系统
VITE_MAP_API_KEY=your-prod-key
```

---

## 九、安全设计

### 9.1 XSS防护
- 使用 Vue3 模板语法自动转义
- 避免 `v-html`，如必须使用需过滤

### 9.2 CSRF防护
- 后端返回 CSRF Token
- Axios 自动添加到请求头

### 9.3 敏感信息处理
- Token 存储在 localStorage（生产环境可考虑 HttpOnly Cookie）
- 敏感信息不在 URL 中传递
- 登出时清除本地存储

---

## 十、后续扩展

### 10.1 国际化 (i18n)
预留国际化支持，使用 Vue I18n

### 10.2 主题切换
预留暗色主题支持，使用 CSS 变量

### 10.3 PWA
支持安装为桌面应用，使用 Vite PWA 插件

---

## 附录

### 附录A：技术参考文档
- Vue3 官方文档: https://cn.vuejs.org/
- Element Plus 文档: https://element-plus.org/
- Vant 文档: https://vant-ui.github.io/vant/
- Pinia 文档: https://pinia.vuejs.org/

### 附录B：开发环境要求
- Node.js: 18.0+
- pnpm: 8.0+ (推荐) 或 npm 9.0+
- 浏览器: Chrome 90+ / Edge 90+
