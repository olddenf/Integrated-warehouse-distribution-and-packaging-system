import instance from './index'

// 登录请求参数
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: string
    username: string
    name: string
    role: string
    status: boolean
  }
}

// 认证API
export const authApi = {
  // 登录
  login: async (params: LoginRequest): Promise<LoginResponse> => {
    const response = await instance.post('/auth/login', params)
    return response.data
  },
  
  // 登出
  logout: async (): Promise<void> => {
    await instance.post('/auth/logout')
  },
  
  // 获取当前用户信息
  getCurrentUser: async (): Promise<any> => {
    const response = await instance.get('/auth/me')
    return response.data
  }
}

export default authApi
