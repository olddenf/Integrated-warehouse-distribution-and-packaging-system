import instance from './index'

// 订单查询参数
export interface OrderQuery {
  status?: string
  customerName?: string
  startDate?: string
  endDate?: string
  page?: number
  size?: number
}

// 订单商品
export interface OrderProduct {
  productName: string
  productCode?: string
  quantity: number
  unit: string
}

// 创建订单请求
export interface OrderCreate {
  customerName: string
  customerPhone: string
  address: string
  appointmentTime: string
  products: OrderProduct[]
  remark?: string
}

// 更新订单请求
export interface OrderUpdate {
  customerName?: string
  customerPhone?: string
  address?: string
  appointmentTime?: string
  remark?: string
}

// 订单响应
export interface OrderResponse {
  id: string
  orderNo: string
  customerName: string
  customerPhone: string
  address: string
  latitude?: number
  longitude?: number
  appointmentTime: string
  status: string
  totalAmount?: number
  remark?: string
  createTime: string
  updateTime: string
  products?: OrderProduct[]
}

// 订单列表响应
export interface OrderListResponse {
  items: OrderResponse[]
  total: number
  page: number
  size: number
  pages: number
}

// 订单API
export const orderApi = {
  // 创建订单
  create: async (data: OrderCreate): Promise<OrderResponse> => {
    const response = await instance.post('/orders', data)
    return response.data
  },
  
  // 获取订单列表
  getList: async (params?: OrderQuery): Promise<OrderListResponse> => {
    const response = await instance.get('/orders', { params })
    return response.data
  },
  
  // 获取订单详情
  getDetail: async (id: string): Promise<OrderResponse> => {
    const response = await instance.get(`/orders/${id}`)
    return response.data
  },
  
  // 更新订单
  update: async (id: string, data: OrderUpdate): Promise<OrderResponse> => {
    const response = await instance.put(`/orders/${id}`, data)
    return response.data
  },
  
  // 取消订单
  cancel: async (id: string, reason: string): Promise<void> => {
    await instance.post(`/orders/${id}/cancel`, { reason })
  },
  
  // 批量导入订单
  batchImport: async (file: FormData): Promise<any> => {
    const response = await instance.post('/orders/batch-import', file, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
}

export default orderApi
