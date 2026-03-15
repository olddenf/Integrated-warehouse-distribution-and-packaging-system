<template>
  <el-aside class="app-sidebar" :width="isCollapsed ? '64px' : '200px'">
    <div class="sidebar-header">
      <el-button
        :icon="isCollapsed ? Expand : Fold"
        circle
        @click="toggleCollapse"
        class="collapse-btn"
      />
    </div>
    
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      :collapse="isCollapsed"
      :collapse-transition="false"
      router
      @select="handleMenuSelect"
    >
      <template v-for="item in menuConfig" :key="item.path">
        <el-menu-item
          v-if="!item.children"
          :index="item.path"
          :disabled="!hasPermission(item.meta.roles)"
        >
          <el-icon><component :is="getIconComponent(item.icon)" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
        
        <el-sub-menu
          v-else
          :index="item.path"
          :disabled="!hasPermission(item.meta.roles)"
        >
          <template #title>
            <el-icon><component :is="getIconComponent(item.icon)" /></el-icon>
            <span>{{ item.title }}</span>
          </template>
          <el-menu-item
            v-for="child in item.children"
            :key="child.path"
            :index="child.path"
            :disabled="!hasPermission(child.meta.roles)"
          >
            {{ child.title }}
          </el-menu-item>
        </el-sub-menu>
      </template>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Fold, Expand } from '@element-plus/icons-vue'
import { menuConfig } from '@/router/menuConfig'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const isCollapsed = ref(false)

const activeMenu = computed(() => {
  const path = route.path
  return menuConfig.find((item: any) => {
    if (item.path === path) return true
    if (item.children) {
      return item.children.some((child: any) => child.path === path)
    }
    return false
  })?.path || path
})

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const handleMenuSelect = (key: string) => {
  console.log('菜单选择:', key)
}

const hasPermission = (roles: string[]) => {
  return authStore.hasPermission(roles)
}

const getIconComponent = (_iconName: string) => {
  // 这里需要根据实际使用的图标库进行映射
  // 暂时返回一个默认图标
  return 'DataAnalysis'
}
</script>

<style scoped lang="scss">
.app-sidebar {
  height: 100%;
  background-color: #ffffff;
  border-right: 1px solid #e4e7ed;
  transition: width 0.3s ease;
  overflow: hidden;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 12px;
  border-bottom: 1px solid #e4e7ed;
}

.collapse-btn {
  transition: transform 0.3s ease;
}

.sidebar-menu {
  border-right: none;
  height: calc(100% - 60px);
  overflow-y: auto;

  .el-menu-item {
    height: 50px;
    line-height: 50px;
    font-size: 14px;

    &:hover {
      background-color: #ecf5ff !important;
    }

    &.is-active {
      background-color: #ecf5ff !important;
      color: #409eff !important;
    }
  }

  .el-sub-menu__title {
    height: 50px;
    line-height: 50px;
    font-size: 14px;

    &:hover {
      background-color: #ecf5ff !important;
    }
  }

  .el-sub-menu .el-menu-item {
    padding-left: 50px !important;
  }
}
</style>
