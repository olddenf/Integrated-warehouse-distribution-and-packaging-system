<template>
  <div class="not-found">
    <div class="not-found-content">
      <van-icon name="info-o" size="80" color="#999" />
      <h1>404</h1>
      <p>页面不存在</p>
      <van-button type="primary" @click="goHome">返回首页</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.not-found-content {
  text-align: center;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 48px;
  color: #999;
  margin: 20px 0;
}

p {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}
</style>