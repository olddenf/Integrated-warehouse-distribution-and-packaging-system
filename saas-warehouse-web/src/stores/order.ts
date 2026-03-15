import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import orderApi, { OrderCreate, OrderUpdate, OrderQuery, OrderResponse } from '@/api/orders'

// 订单存储
export const useOrderStore = defineStore('order', () => {
  // 状态
  const orders = ref<OrderResponse[]>([])
  const currentOrder = ref<OrderResponse | null>(null)
  const loading = ref<boolean>(false)
  const error = ref<string>('')
  const total = ref<number>(0)
  const page = ref<number>(1)
  const size = ref<number>(20)
  const filters = ref<OrderQuery>({})

  // Getters
  const orderList = computed(() => orders.value)
  const orderCount = computed(() => total.value)
  const currentPage = computed(() => page.value)
  const pageSize = computed(() => size.value)
  const hasMore = computed(() => page.value * size.value < total.value)

  // Actions
  const fetchOrders = async (params?: OrderQuery) => {
    loading.value = true
    error.value = ''
    try {
      const query = { ...filters.value, ...params }
      const response = await orderApi.getList(query)
      orders.value = response.items
      total.value = response.total
      page.value = response.page
      size.value = response.size
    } catch (err: any) {
      error.value = err.message || '获取订单列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchOrderDetail = async (id: string) => {
    loading.value = true
    error.value = ''
    try {
      const order = await orderApi.getDetail(id)
      currentOrder.value = order
      return order
    } catch (err: any) {
      error.value = err.message || '获取订单详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createOrder = async (order: OrderCreate) => {
    loading.value = true
    error.value = ''
    try {
      const newOrder = await orderApi.create(order)
      orders.value.unshift(newOrder)
      total.value++
      return newOrder
    } catch (err: any) {
      error.value = err.message || '创建订单失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateOrder = async (id: string, data: OrderUpdate) => {
    loading.value = true
    error.value = ''
    try {
      const updatedOrder = await orderApi.update(id, data)
      const index = orders.value.findIndex((o: OrderResponse) => o.id === id)
      if (index !== -1) {
        orders.value[index] = { ...orders.value[index], ...updatedOrder }
      }
      if (currentOrder.value?.id === id) {
        currentOrder.value = { ...currentOrder.value, ...updatedOrder }
      }
      return updatedOrder
    } catch (err: any) {
      error.value = err.message || '更新订单失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const cancelOrder = async (id: string, reason: string) => {
    loading.value = true
    error.value = ''
    try {
      await orderApi.cancel(id, reason)
      const order = orders.value.find((o: OrderResponse) => o.id === id)
      if (order) {
        order.status = 'cancelled'
      }
      if (currentOrder.value?.id === id) {
        currentOrder.value.status = 'cancelled'
      }
    } catch (err: any) {
      error.value = err.message || '取消订单失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const setFilters = (newFilters: OrderQuery) => {
    filters.value = newFilters
    page.value = 1
  }

  const resetFilters = () => {
    filters.value = {}
    page.value = 1
  }

  return {
    orders,
    currentOrder,
    loading,
    error,
    total,
    page,
    size,
    filters,
    orderList,
    orderCount,
    currentPage,
    pageSize,
    hasMore,
    fetchOrders,
    fetchOrderDetail,
    createOrder,
    updateOrder,
    cancelOrder,
    setFilters,
    resetFilters
  }
})
