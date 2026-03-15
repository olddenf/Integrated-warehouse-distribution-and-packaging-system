import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  // 登录页
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  
  // 卸货端
  {
    path: '/unloader',
    name: 'UnloaderLayout',
    component: () => import('@/components/UnloaderLayout.vue'),
    meta: { requiresAuth: true, role: 'unloader' },
    children: [
      {
        path: 'tasks',
        name: 'UnloaderTasks',
        component: () => import('@/views/unloader/Tasks.vue')
      },
      {
        path: 'history',
        name: 'UnloaderHistory',
        component: () => import('@/views/unloader/History.vue')
      },
      {
        path: 'profile',
        name: 'UnloaderProfile',
        component: () => import('@/views/unloader/Profile.vue')
      },
      {
        path: 'task/:id',
        name: 'UnloaderTaskDetail',
        component: () => import('@/views/unloader/TaskDetail.vue')
      }
    ]
  },
  
  // 司机端
  {
    path: '/driver',
    name: 'DriverLayout',
    component: () => import('@/components/DriverLayout.vue'),
    meta: { requiresAuth: true, role: 'driver' },
    children: [
      {
        path: 'tasks',
        name: 'DriverTasks',
        component: () => import('@/views/driver/Tasks.vue')
      },
      {
        path: 'map',
        name: 'DriverMap',
        component: () => import('@/views/driver/Map.vue')
      },
      {
        path: 'history',
        name: 'DriverHistory',
        component: () => import('@/views/driver/History.vue')
      },
      {
        path: 'profile',
        name: 'DriverProfile',
        component: () => import('@/views/driver/Profile.vue')
      },
      {
        path: 'task/:id',
        name: 'DriverTaskDetail',
        component: () => import('@/views/driver/TaskDetail.vue')
      },
      {
        path: 'sign/:id',
        name: 'DriverSign',
        component: () => import('@/views/driver/Sign.vue')
      }
    ]
  },
  
  // 安装端
  {
    path: '/installer',
    name: 'InstallerLayout',
    component: () => import('@/components/InstallerLayout.vue'),
    meta: { requiresAuth: true, role: 'installer' },
    children: [
      {
        path: 'tasks',
        name: 'InstallerTasks',
        component: () => import('@/views/installer/Tasks.vue')
      },
      {
        path: 'guide',
        name: 'InstallerGuide',
        component: () => import('@/views/installer/Guide.vue')
      },
      {
        path: 'history',
        name: 'InstallerHistory',
        component: () => import('@/views/installer/History.vue')
      },
      {
        path: 'profile',
        name: 'InstallerProfile',
        component: () => import('@/views/installer/Profile.vue')
      },
      {
        path: 'task/:id',
        name: 'InstallerTaskDetail',
        component: () => import('@/views/installer/TaskDetail.vue')
      }
    ]
  },
  
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth !== false
  
  if (requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    // 根据用户角色重定向到对应首页
    const role = authStore.user?.role
    if (role === 'unloader') {
      next('/unloader/tasks')
    } else if (role === 'driver') {
      next('/driver/tasks')
    } else if (role === 'installer') {
      next('/installer/tasks')
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
