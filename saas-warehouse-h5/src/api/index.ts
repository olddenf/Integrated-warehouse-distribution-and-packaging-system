import axios from 'axios'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'

// 创建Axios实例
const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
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
    const { code, message } = response.data
    if (code === 200) {
      return response
    } else {
      showToast({ type: 'fail', message: message || '请求失败' })
      return Promise.reject(new Error(message || '请求失败'))
    }
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          showToast({ type: 'fail', message: '登录已过期，请重新登录' })
          useAuthStore().logout()
          window.location.href = '/login'
          break
        case 403:
          showToast({ type: 'fail', message: '权限不足' })
          break
        case 404:
          showToast({ type: 'fail', message: '请求的资源不存在' })
          break
        case 500:
          showToast({ type: 'fail', message: '服务器错误' })
          break
        default:
          showToast({ type: 'fail', message: data.message || '请求失败' })
      }
    } else if (error.request) {
      showToast({ type: 'fail', message: '网络错误，请检查网络连接' })
    } else {
      showToast({ type: 'fail', message: '请求配置错误' })
    }
    return Promise.reject(error)
  }
)

export default instance
