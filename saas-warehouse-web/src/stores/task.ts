import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import taskApi, { TaskQuery, TaskResponse } from '@/api/tasks'

// 任务存储
export const useTaskStore = defineStore('task', () => {
  // 状态
  const tasks = ref<TaskResponse[]>([])
  const myTasks = ref<TaskResponse[]>([])
  const currentTask = ref<TaskResponse | null>(null)
  const loading = ref<boolean>(false)
  const error = ref<string>('')
  const total = ref<number>(0)
  const page = ref<number>(1)
  const size = ref<number>(20)
  const filters = ref<TaskQuery>({})

  // Getters
  const taskList = computed(() => tasks.value)
  const myTaskList = computed(() => myTasks.value)
  const taskCount = computed(() => total.value)
  const currentPage = computed(() => page.value)
  const pageSize = computed(() => size.value)
  const hasMore = computed(() => page.value * size.value < total.value)

  // Actions
  const fetchTasks = async (params?: TaskQuery) => {
    loading.value = true
    error.value = ''
    try {
      const query = { ...filters.value, ...params }
      const response = await taskApi.getList(query)
      tasks.value = response.items
      total.value = response.total
      page.value = response.page
      size.value = response.size
    } catch (err: any) {
      error.value = err.message || '获取任务列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchMyTasks = async (params?: TaskQuery) => {
    loading.value = true
    error.value = ''
    try {
      const query = { ...filters.value, ...params }
      const response = await taskApi.getMyTasks(query)
      myTasks.value = response.items
      total.value = response.total
      page.value = response.page
      size.value = response.size
    } catch (err: any) {
      error.value = err.message || '获取我的任务列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchTaskDetail = async (id: string) => {
    loading.value = true
    error.value = ''
    try {
      const task = await taskApi.getDetail(id)
      currentTask.value = task
      return task
    } catch (err: any) {
      error.value = err.message || '获取任务详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const startTask = async (id: string, location?: { lat: number; lng: number }) => {
    loading.value = true
    error.value = ''
    try {
      await taskApi.start(id, location)
      const task = tasks.value.find((t: TaskResponse) => t.id === id)
      if (task) {
        task.status = 'in_progress'
      }
      const myTask = myTasks.value.find((t: TaskResponse) => t.id === id)
      if (myTask) {
        myTask.status = 'in_progress'
      }
      if (currentTask.value?.id === id) {
        currentTask.value.status = 'in_progress'
      }
    } catch (err: any) {
      error.value = err.message || '开始任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const completeTask = async (id: string, data: {
    content?: string
    location?: { lat: number; lng: number }
  }) => {
    loading.value = true
    error.value = ''
    try {
      await taskApi.complete(id, data)
      const task = tasks.value.find((t: TaskResponse) => t.id === id)
      if (task) {
        task.status = 'completed'
      }
      const myTask = myTasks.value.find((t: TaskResponse) => t.id === id)
      if (myTask) {
        myTask.status = 'completed'
      }
      if (currentTask.value?.id === id) {
        currentTask.value.status = 'completed'
      }
    } catch (err: any) {
      error.value = err.message || '完成任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const uploadAttachment = async (id: string, file: FormData) => {
    loading.value = true
    error.value = ''
    try {
      const response = await taskApi.upload(id, file)
      return response
    } catch (err: any) {
      error.value = err.message || '上传附件失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const setFilters = (newFilters: TaskQuery) => {
    filters.value = newFilters
    page.value = 1
  }

  const resetFilters = () => {
    filters.value = {}
    page.value = 1
  }

  return {
    tasks,
    myTasks,
    currentTask,
    loading,
    error,
    total,
    page,
    size,
    filters,
    taskList,
    myTaskList,
    taskCount,
    currentPage,
    pageSize,
    hasMore,
    fetchTasks,
    fetchMyTasks,
    fetchTaskDetail,
    startTask,
    completeTask,
    uploadAttachment,
    setFilters,
    resetFilters
  }
})
