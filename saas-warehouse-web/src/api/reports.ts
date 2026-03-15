import instance from './index'

// 报表查询参数
export interface ReportQuery {
  startDate: string
  endDate: string
  groupBy?: string // day, week, month
  type?: string // order, task, fee, worker
}

// 订单报表数据
export interface OrderReportData {
  date: string
  count: number
  amount: number
  status: {
    pending: number
    assigned: number
    delivering: number
    installing: number
    completed: number
    cancelled: number
  }
}

// 人员报表数据
export interface WorkerReportData {
  workerId: string
  workerName: string
  role: string
  taskCount: number
  completedCount: number
  efficiency: number
  totalAmount: number
}

// 费用报表数据
export interface FeeReportData {
  date: string
  deliveryFee: number
  installFee: number
  unloadFee: number
  otherFee: number
  totalFee: number
}

// 任务报表数据
export interface TaskReportData {
  date: string
  taskCount: number
  completedCount: number
  avgDuration: number
  type: {
    delivery: number
    install: number
    unload: number
  }
}

// 报表API
export const reportApi = {
  // 获取订单报表
  getOrderReport: async (params: ReportQuery): Promise<OrderReportData[]> => {
    const response = await instance.get('/reports/orders', { params })
    return response.data
  },
  
  // 获取人员报表
  getWorkerReport: async (params: ReportQuery): Promise<WorkerReportData[]> => {
    const response = await instance.get('/reports/workers', { params })
    return response.data
  },
  
  // 获取费用报表
  getFeeReport: async (params: ReportQuery): Promise<FeeReportData[]> => {
    const response = await instance.get('/reports/fees', { params })
    return response.data
  },
  
  // 获取任务报表
  getTaskReport: async (params: ReportQuery): Promise<TaskReportData[]> => {
    const response = await instance.get('/reports/tasks', { params })
    return response.data
  },
  
  // 导出报表
  exportReport: async (params: ReportQuery): Promise<Blob> => {
    const response = await instance.get('/reports/export', {
      params,
      responseType: 'blob'
    })
    return response.data
  }
}

export default reportApi
