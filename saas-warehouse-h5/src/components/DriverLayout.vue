<template>
  <div class="driver-layout">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    
    <!-- 底部Tab导航 -->
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="logistics" to="/driver/tasks">任务</van-tabbar-item>
      <van-tabbar-item icon="location-o" to="/driver/map">地图</van-tabbar-item>
      <van-tabbar-item icon="records-o" to="/driver/history">历史</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/driver/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const active = computed({
  get: () => {
    const path = route.path
    if (path.includes('/tasks')) return 0
    if (path.includes('/map')) return 1
    if (path.includes('/history')) return 2
    if (path.includes('/profile')) return 3
    return 0
  },
  set: (_) => {
    // Tab切换由路由处理
  }
})
</script>

<style scoped lang="scss">
.driver-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  
  .van-tabbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
