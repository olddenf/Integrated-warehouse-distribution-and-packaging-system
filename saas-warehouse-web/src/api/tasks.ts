import instance from './index'

// 任务查询参数
export interface TaskQuery {
  status?: string
  taskType?: string
  assignedTo?: string
  startDate?: string
  endDate?: string
  page?: number
  size?: number
}

// 任务响应
export interface TaskResponse {
  id: string
  taskNo: string
  orderId: string
  taskType: string
  assignedTo?: string
  assignedName?: string
  status: string
  startTime?: string
  endTime?: string
  remark?: string
  createTime: string
  order?: {
    customerName: string
    customerPhone: string
    address: string
  }
}

// 任务列表响应
export interface TaskListResponse {
  items: TaskResponse[]
  total: number
  page: number
  size: number
  pages: number
}

// 任务记录
export interface TaskRecord {
  id: string
  taskId: string
  recordType: string
  content?: string
  locationLat?: number
  locationLng?: number
  createTime: string
}

// 任务API
export const taskApi = {
  // 获取任务列表
  getList: async (params?: TaskQuery): Promise<TaskListResponse> => {
    const response = await instance.get('/tasks', { params })
    return response.data
  },
  
  // 获取我的任务列表
  getMyTasks: async (params?: TaskQuery): Promise<TaskListResponse> => {
    const response = await instance.get('/tasks/my-tasks', { params })
    return response.data
  },
  
  // 获取任务详情
  getDetail: async (id: string): Promise<TaskResponse> => {
    const response = await instance.get(`/tasks/${id}`)
    return response.data
  },
  
  // 开始任务
  start: async (id: string, location?: { lat: number; lng: number }): Promise<void> => {
    await instance.post(`/tasks/${id}/start`, location)
  },
  
  // 完成任务
  complete: async (id: string, data: {
    content?: string
    location?: { lat: number; lng: number }
  }): Promise<void> => {
    await instance.post(`/tasks/${id}/complete`, data)
  },
  
  // 上传附件
  upload: async (id: string, file: FormData): Promise<any> => {
    const response = await instance.post(`/tasks/${id}/upload`, file, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },
  
  // 获取任务记录
  getRecords: async (id: string): Promise<TaskRecord[]> => {
    const response = await instance.get(`/tasks/${id}/records`)
    return response.data
  }
}

export default taskApi
