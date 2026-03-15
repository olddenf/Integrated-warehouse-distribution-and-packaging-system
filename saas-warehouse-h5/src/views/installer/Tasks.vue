<template>
  <div class="installer-tasks">
    <van-nav-bar
      title="安装任务"
      :right-text="`今日(${tasks.length})`"
      :safe-area-inset-top="true"
    />
    
    <!-- 状态筛选 -->
    <div class="filter-bar">
      <van-tabs v-model="activeTab" @click-tab="handleTabClick">
        <van-tab title="全部" />
        <van-tab :title="`待安装 (${pendingCount})`" />
        <van-tab :title="`进行中 (${inProgressCount})`" />
      </van-tabs>
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
            <span>商品:</span>
          </div>
          <div class="product-list">
            <div v-for="(product, index) in task.order.products" :key="index" class="product-item">
              • {{ product.productName }} × {{ product.quantity }}
            </div>
          </div>
          <div class="info-row">
            <van-icon name="clock-o" />
            <span>预约: {{ formatTime(task.order.appointmentTime) }}</span>
          </div>
          <div class="info-row">
            <van-icon name="star-o" />
            <span>难度: {{ getDifficultyStars(task.difficulty) }}</span>
          </div>
        </div>
        
        <div class="task-footer">
          <van-button
            v-if="task.status === 'pending'"
            type="primary"
            size="small"
            @click.stop="handleStart(task)"
          >
            去安装
          </van-button>
          <van-button
            v-if="task.status === 'in_progress'"
            type="success"
            size="small"
            @click.stop="handleComplete(task)"
          >
            完成安装
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
        <van-icon name="todo-list-o" size="64" color="#c8c9cc" />
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
const activeTab = ref(0)

const tasks = ref([
  {
    id: '1',
    taskNo: 'TK008',
    status: 'pending',
    difficulty: 3,
    order: {
      orderNo: 'SO20260312000008',
      customerName: '王五',
      customerPhone: '13700137000',
      address: '丰台区方庄小区',
      appointmentTime: '2026-03-15 15:00',
      products: [
        { productName: '空调挂机', quantity: 2 },
        { productName: '智能门锁', quantity: 1 }
      ]
    }
  },
  {
    id: '2',
    taskNo: 'TK009',
    status: 'in_progress',
    difficulty: 2,
    order: {
      orderNo: 'SO20260312000009',
      customerName: '赵六',
      customerPhone: '13800138000',
      address: '东城区王府井',
      appointmentTime: '2026-03-15 16:00',
      products: [
        { productName: '电视', quantity: 1 }
      ]
    }
  },
  {
    id: '3',
    taskNo: 'TK010',
    status: 'completed',
    difficulty: 1,
    order: {
      orderNo: 'SO20260312000010',
      customerName: '孙七',
      customerPhone: '13600136000',
      address: '西城区西单',
      appointmentTime: '2026-03-15 10:00',
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

const filteredTasks = computed(() => {
  if (activeTab.value === 0) {
    return tasks.value
  } else if (activeTab.value === 1) {
    return tasks.value.filter(task => task.status === 'pending')
  } else {
    return tasks.value.filter(task => task.status === 'in_progress')
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
    'pending': '待安装',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return textMap[status] || status
}

const getDifficultyStars = (difficulty: number) => {
  return '⭐'.repeat(difficulty)
}

const formatTime = (time: string) => {
  return time
}

const handleTabClick = (tab: any) => {
  activeTab.value = tab.index
}

const handleTaskClick = (task: any) => {
  router.push(`/installer/task/${task.id}`)
}

const handleStart = (_task: any) => {
  showToast('开始安装')
  // 实现开始安装逻辑
}

const handleComplete = (_task: any) => {
  showToast('完成安装')
  // 实现完成安装逻辑
}

const handleViewDetail = (task: any) => {
  router.push(`/installer/task/${task.id}`)
}
</script>

<style scoped lang="scss">
.installer-tasks {
  min-height: 100vh;
  background-color: #f7f8fa;
  
  .filter-bar {
    background-color: #ffffff;
    margin-bottom: 12px;
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
      
      .product-list {
        margin-left: 24px;
        margin-bottom: 8px;
        
        .product-item {
          font-size: 14px;
          color: #646566;
          margin-bottom: 4px;
        }
      }
    }
    
    .task-footer {
      display: flex;
      justify-content: flex-end;
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
