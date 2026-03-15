<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <div class="login-header">
        <img src="@/assets/vue.svg" class="logo" />
        <h1 class="title">仓配装管理系统</h1>
        <p class="subtitle">请登录您的账号</p>
      </div>
      
      <van-form @submit="handleLogin">
        <van-field
          v-model="form.username"
          name="username"
          label="用户名"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        
        <van-field
          v-model="form.password"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
        />
        
        <van-cell center>
          <van-checkbox v-model="form.remember">记住我</van-checkbox>
          <van-button class="forgot-password">忘记密码？</van-button>
        </van-cell>
        
        <van-button
          type="primary"
          class="login-btn"
          :loading="loading"
          native-type="submit"
        >
          登录
        </van-button>
      </van-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  loading.value = true
  
  try {
    await authStore.login(form.username, form.password)
    showToast({ type: 'success', message: '登录成功' })
    // 根据用户角色跳转到不同的页面
    if (authStore.user?.role === 'ADMIN') {
      router.push('/unloader/tasks')
    } else if (authStore.user?.role === 'DRIVER') {
      router.push('/driver/tasks')
    } else if (authStore.user?.role === 'INSTALLER') {
      router.push('/installer/tasks')
    } else {
      router.push('/unloader/tasks')
    }
  } catch (error) {
    showToast({ type: 'fail', message: '登录失败，请检查用户名和密码' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 40px 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;

  .logo {
    width: 64px;
    height: 64px;
    margin-bottom: 20px;
  }

  .title {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8px;
  }

  .subtitle {
    font-size: 14px;
    color: #909399;
  }
}

.login-btn {
  width: 100%;
  margin-top: 20px;
}

.forgot-password {
  color: #409eff;
}
</style>