import instance from './index'

// 用户查询参数
export interface UserQuery {
  role?: string
  status?: boolean
  keyword?: string
  page?: number
  size?: number
}

// 用户创建请求
export interface UserCreate {
  username: string
  password: string
  name: string
  phone?: string
  role: string
  status?: boolean
}

// 用户更新请求
export interface UserUpdate {
  name?: string
  phone?: string
  role?: string
  status?: boolean
  password?: string
}

// 用户响应
export interface UserResponse {
  id: string
  username: string
  name: string
  phone?: string
  role: string
  status: boolean
  createTime: string
  updateTime: string
}

// 用户列表响应
export interface UserListResponse {
  items: UserResponse[]
  total: number
  page: number
  size: number
  pages: number
}

// 用户API
export const userApi = {
  // 获取用户列表
  getList: async (params?: UserQuery): Promise<UserListResponse> => {
    const response = await instance.get('/users', { params })
    return response.data
  },
  
  // 获取用户详情
  getDetail: async (id: string): Promise<UserResponse> => {
    const response = await instance.get(`/users/${id}`)
    return response.data
  },
  
  // 创建用户
  create: async (data: UserCreate): Promise<UserResponse> => {
    const response = await instance.post('/users', data)
    return response.data
  },
  
  // 更新用户
  update: async (id: string, data: UserUpdate): Promise<UserResponse> => {
    const response = await instance.put(`/users/${id}`, data)
    return response.data
  },
  
  // 删除用户
  delete: async (id: string): Promise<void> => {
    await instance.delete(`/users/${id}`)
  },
  
  // 批量删除用户
  batchDelete: async (ids: string[]): Promise<void> => {
    await instance.post('/users/batch-delete', { ids })
  }
}

export default userApi
