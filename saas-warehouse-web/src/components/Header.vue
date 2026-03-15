<template>
  <el-header class="app-header">
    <!-- 左侧 Logo 和标题 -->
    <div class="header-left">
      <img src="@/assets/vue.svg" class="logo" />
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

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Bell, Plus, ArrowDown } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const searchKeyword = ref('')
const unreadCount = ref(3)

const user = computed(() => {
  return {
    name: authStore.user?.name || '管理员',
    avatar: authStore.user?.avatar || ''
  }
})

const handleSearch = () => {
  console.log('搜索:', searchKeyword.value)
  // 实现搜索逻辑
}

const showNotifications = () => {
  console.log('显示通知')
  // 实现通知逻辑
}

const handleQuickAction = (command: string) => {
  switch (command) {
    case 'createOrder':
      router.push('/orders/create')
      break
    case 'batchImport':
      router.push('/orders/import')
      break
    case 'quickDispatch':
      router.push('/dispatch')
      break
  }
}

const handleUserAction = (command: string) => {
  switch (command) {
    case 'profile':
      console.log('个人中心')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      authStore.logout()
      router.push('/login')
      break
  }
}
</script>

<style scoped lang="scss">
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;

  .logo {
    width: 32px;
    height: 32px;
    margin-right: 12px;
  }

  .app-title {
    font-size: 18px;
    font-weight: 600;
    color: #409eff;
  }
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;

  .user-profile {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 4px 12px;
    border-radius: 20px;
    transition: background-color 0.3s;

    &:hover {
      background-color: #f5f7fa;
    }

    .user-name {
      font-size: 14px;
      color: #303133;
    }

    .dropdown-icon {
      font-size: 12px;
      color: #909399;
    }
  }
}
</style>
