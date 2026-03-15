<template>
  <div class="driver-tasks">
    <van-nav-bar
      title="配送任务"
      :right-text="`今日(${tasks.length})`"
      :safe-area-inset-top="true"
    />
    
    <!-- 快捷操作栏 -->
    <div class="quick-actions">
      <div class="action-item" @click="filterTasks('pending')">
        <div class="action-count">{{ pendingCount }}</div>
        <div class="action-label">待配送</div>
      </div>
      <div class="action-item" @click="filterTasks('in_progress')">
        <div class="action-count">{{ inProgressCount }}</div>
        <div class="action-label">配送中</div>
      </div>
      <div class="action-item" @click="filterTasks('completed')">
        <div class="action-count">{{ completedCount }}</div>
        <div class="action-label">已完成</div>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="task-list">
      <div
        v-for="task in filteredTasks"
        :key="task.id"
        class="task-card"
        @click="handleTaskClick(task)"
      >
        <div class="task-header">
          <span class="task-no">{{ task.taskNo }}</span>
          <van-tag :type="getStatusType(task.status)">{{ getStatusText(task.status) }}</van-tag>
        </div>
        
        <div class="task-info">
          <div class="info-row">
            <van-icon name="user-o" />
            <span>客户: {{ task.order.customerName }}</span>
          </div>
          <div class="info-row">
            <van-icon name="location-o" />
            <span class="address">{{ task.order.address }}</span>
          </div>
          <div class="info-row">
            <van-icon name="bag-o" />
            <span>商品: {{ productSummary(task.order.products) }}</span>
          </div>
          <div class="info-row">
            <van-icon name="money-o" />
            <span>金额: ¥{{ task.order.totalAmount.toFixed(2) }}</span>
          </div>
          <div class="info-row">
            <van-icon name="clock-o" />
            <span>预约: {{ formatTime(task.order.appointmentTime) }}</span>
          </div>
        </div>
        
        <div class="task-footer">
          <van-button
            v-if="task.status === 'pending'"
            type="primary"
            size="small"
            @click.stop="handleStart(task)"
          >
            开始
          </van-button>
          <van-button
            v-if="task.status === 'pending'"
            size="small"
            plain
            @click.stop="handleNavigation(task)"
          >
            导航
          </van-button>
          <van-button
            v-if="task.status === 'in_progress'"
            type="success"
            size="small"
            @click.stop="handleSign(task)"
          >
            签收
          </van-button>
          <van-button
            v-if="task.status === 'completed'"
            size="small"
            plain
            @click.stop="handleViewDetail(task)"
          >
            查看详情
          </van-button>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="filteredTasks.length === 0" class="empty-state">
        <van-icon name="logistics" size="64" color="#c8c9cc" />
        <p>暂无任务</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const activeFilter = ref('all')

const tasks = ref([
  {
    id: '1',
    taskNo: 'TK005',
    status: 'pending',
    order: {
      orderNo: 'SO20260312000005',
      customerName: '李四',
      customerPhone: '13900139000',
      address: '海淀区中关村科技园区',
      appointmentTime: '2026-03-15 14:00',
      totalAmount: 520,
      products: [
        { productName: '沙发', quantity: 1 }
      ]
    }
  },
  {
    id: '2',
    taskNo: 'TK006',
    status: 'in_progress',
    order: {
      orderNo: 'SO20260312000006',
      customerName: '王五',
      customerPhone: '13700137000',
      address: '朝阳区建国路88号',
      appointmentTime: '2026-03-15 15:00',
      totalAmount: 880,
      products: [
        { productName: '空调', quantity: 2 }
      ]
    }
  },
  {
    id: '3',
    taskNo: 'TK007',
    status: 'completed',
    order: {
      orderNo: 'SO20260312000007',
      customerName: '赵六',
      customerPhone: '13800138000',
      address: '丰台区方庄小区',
      appointmentTime: '2026-03-15 10:00',
      totalAmount: 360,
      products: [
        { productName: '洗衣机', quantity: 1 }
      ]
    }
  }
])

const pendingCount = computed(() => {
  return tasks.value.filter(task => task.status === 'pending').length
})

const inProgressCount = computed(() => {
  return tasks.value.filter(task => task.status === 'in_progress').length
})

const completedCount = computed(() => {
  return tasks.value.filter(task => task.status === 'completed').length
})

const filteredTasks = computed(() => {
  if (activeFilter.value === 'all') {
    return tasks.value
  } else {
    return tasks.value.filter(task => task.status === activeFilter.value)
  }
})

const getStatusType = (status: string) => {
  switch (status) {
    case 'pending': return 'warning';
    case 'in_progress': return 'primary';
    case 'completed': return 'success';
    case 'cancelled': return 'danger';
    default: return 'primary';
  }
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    'pending': '待配送',
    'in_progress': '配送中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return textMap[status] || status
}

const productSummary = (products: any[]) => {
  if (products.length <= 2) {
    return products.map(p => `${p.productName}×${p.quantity}`).join(' ')
  }
  return products.slice(0, 2).map(p => `${p.productName}×${p.quantity}`).join(' ') + '...'
}

const formatTime = (time: string) => {
  return time
}

const filterTasks = (status: string) => {
  activeFilter.value = status === 'all' ? 'all' : status
}

const handleTaskClick = (task: any) => {
  router.push(`/driver/task/${task.id}`)
}

const handleStart = (_task: any) => {
  showToast('开始配送')
  // 实现开始配送逻辑
}

const handleNavigation = (_task: any) => {
  showToast('导航功能')
  // 实现导航逻辑
}

const handleSign = (task: any) => {
  router.push(`/driver/sign/${task.id}`)
}

const handleViewDetail = (task: any) => {
  router.push(`/driver/task/${task.id}`)
}
</script>

<style scoped lang="scss">
.driver-tasks {
  min-height: 100vh;
  background-color: #f7f8fa;
  
  .quick-actions {
    display: flex;
    background-color: #ffffff;
    padding: 16px;
    margin-bottom: 12px;
    
    .action-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      
      .action-count {
        font-size: 20px;
        font-weight: 600;
        color: #1989fa;
        margin-bottom: 4px;
      }
      
      .action-label {
        font-size: 12px;
        color: #646566;
      }
    }
  }
  
  .task-list {
    padding: 12px;
  }
  
  .task-card {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    
    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      
      .task-no {
        font-size: 16px;
        font-weight: 600;
        color: #323233;
      }
    }
    
    .task-info {
      margin-bottom: 12px;
      
      .info-row {
        display: flex;
        align-items: flex-start;
        font-size: 14px;
        color: #646566;
        margin-bottom: 8px;
        
        .van-icon {
          margin-right: 8px;
          font-size: 16px;
          margin-top: 2px;
        }
        
        .address {
          flex: 1;
          line-height: 1.4;
        }
      }
    }
    
    .task-footer {
      display: flex;
      gap: 8px;
      
      .van-button {
        flex: 1;
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 0;
    
    p {
      margin-top: 16px;
      font-size: 14px;
      color: #969799;
    }
  }
}
</style>
