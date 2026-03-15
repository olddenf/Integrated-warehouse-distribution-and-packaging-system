<template>
  <div class="installer-task-detail">
    <van-nav-bar title="任务详情" left-text="返回" left-arrow @click-left="goBack" />
    
    <div class="task-info" v-if="task">
      <div class="task-header">
        <div class="task-id">订单号: {{ task.orderNo }}</div>
        <van-tag :type="task.statusType">{{ task.statusText }}</van-tag>
      </div>
      
      <div class="task-content">
        <van-cell-group>
          <van-cell title="客户姓名" :value="task.customer" />
          <van-cell title="联系电话" :value="task.phone" />
          <van-cell title="安装地址" :value="task.address" :label="task.address" />
          <van-cell title="安装时间" :value="task.installTime || '未安排'" />
          <van-cell title="难度等级" :value="task.difficulty || '普通'">
            <template #right>
              <van-icon :name="getDifficultyIcon(task.difficulty)" :color="getDifficultyColor(task.difficulty)" />
            </template>
          </van-cell>
        </van-cell-group>
        
        <div class="goods-section">
          <h3>安装物品</h3>
          <van-list>
            <van-cell v-for="item in task.goods" :key="item.id" :title="item.name" :value="`${item.quantity} ${item.unit}`" />
          </van-list>
        </div>
        
        <div class="remark-section" v-if="task.remark">
          <h3>备注信息</h3>
          <div class="remark-content">{{ task.remark }}</div>
        </div>
      </div>
      
      <div class="task-actions">
        <van-button v-if="task.status === 'pending'" type="primary" block @click="handleStart">开始安装</van-button>
        <van-button v-else-if="task.status === 'in_progress'" type="primary" block @click="handleComplete">完成安装</van-button>
        <van-button v-else type="default" block disabled>{{ task.statusText }}</van-button>
      </div>
    </div>
    
    <van-loading v-else type="spinner" color="#1989fa" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const taskId = route.params.id as string

const task = ref<any>(null)
const loading = ref(false)

const goBack = () => {
  router.back()
}

const getDifficultyIcon = (difficulty: string) => {
  switch (difficulty) {
    case '简单':
      return 'success'
    case '普通':
      return 'info'
    case '困难':
      return 'warning'
    default:
      return 'info'
  }
}

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case '简单':
      return '#07c160'
    case '普通':
      return '#1989fa'
    case '困难':
      return '#ff9500'
    default:
      return '#1989fa'
  }
}

const fetchTaskDetail = async () => {
  try {
    loading.value = true
    const response = await api.get(`/tasks/${taskId}`)
    const taskData = response.data
    // 添加状态类型和文本
    taskData.statusType = getStatusType(taskData.status)
    taskData.statusText = getStatusText(taskData.status)
    task.value = taskData
  } catch (error) {
    showToast('获取任务详情失败')
    console.error('获取任务详情失败:', error)
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending: 'primary',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'primary'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || status
}

const handleStart = async () => {
  try {
    loading.value = true
    await api.put(`/tasks/${taskId}/start`)
    showToast('开始安装成功')
    // 更新本地状态
    task.value.status = 'in_progress'
    task.value.statusType = getStatusType('in_progress')
    task.value.statusText = getStatusText('in_progress')
  } catch (error) {
    showToast('开始安装失败')
    console.error('开始安装失败:', error)
  } finally {
    loading.value = false
  }
}

const handleComplete = async () => {
  try {
    loading.value = true
    await api.put(`/tasks/${taskId}/complete`)
    showToast('安装完成成功')
    // 更新本地状态
    task.value.status = 'completed'
    task.value.statusType = getStatusType('completed')
    task.value.statusText = getStatusText('completed')
  } catch (error) {
    showToast('安装完成失败')
    console.error('安装完成失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTaskDetail()
})
</script>

<style scoped>
.installer-task-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.task-info {
  padding: 16px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.task-id {
  font-size: 16px;
  font-weight: bold;
}

.task-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.goods-section,
.remark-section {
  margin-top: 16px;
}

h3 {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.remark-content {
  background-color: #f9f9f9;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.task-actions {
  padding: 16px;
}
</style>