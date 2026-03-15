import instance from './index'

// 调度查询参数
export interface DispatchQuery {
  status?: string
  date?: string
  workerId?: string
}

// 调度任务
export interface DispatchTask {
  id: string
  orderId: string
  taskType: string
  customerName: string
  address: string
  appointmentTime: string
  priority: number
  distance?: number
}

// 执行人员
export interface Worker {
  id: string
  name: string
  role: string
  status: boolean
  currentTasks?: number
  location?: { lat: number; lng: number }
}

// 调度结果
export interface DispatchResult {
  taskId: string
  workerId: string
  workerName: string
  estimatedTime: string
}

// 手动调整请求
export interface DispatchAdjust {
  taskId: string
  workerId: string
  reason: string
}

// 调度API
export const dispatchApi = {
  // 获取待调度任务
  getPendingTasks: async (params?: DispatchQuery): Promise<DispatchTask[]> => {
    const response = await instance.get('/dispatch/pending-tasks', { params })
    return response.data
  },
  
  // 获取执行人员
  getWorkers: async (params?: { role?: string; status?: boolean }): Promise<Worker[]> => {
    const response = await instance.get('/dispatch/workers', { params })
    return response.data
  },
  
  // 智能排单
  autoDispatch: async (data: {
    taskIds: string[]
    strategy?: string
  }): Promise<DispatchResult[]> => {
    const response = await instance.post('/dispatch/auto', data)
    return response.data
  },
  
  // 手动调整
  adjust: async (data: DispatchAdjust): Promise<void> => {
    await instance.post('/dispatch/adjust', data)
  },
  
  // 获取调度日志
  getLogs: async (params?: { taskId?: string; workerId?: string }): Promise<any[]> => {
    const response = await instance.get('/dispatch/logs', { params })
    return response.data
  }
}

export default dispatchApi
