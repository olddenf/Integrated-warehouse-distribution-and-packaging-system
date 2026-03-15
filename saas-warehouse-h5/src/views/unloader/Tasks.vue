<template>
  <div class="unloader-tasks">
    <van-nav-bar
      title="卸货任务"
      :right-text="`今日(${tasks.length})`"
      :safe-area-inset-top="true"
    />
    
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <van-tabs v-model="activeTab" @click-tab="handleTabClick">
        <van-tab title="全部" />
        <van-tab :title="`待处理 (${pendingCount})`" />
        <van-tab :title="`已完成 (${completedCount})`" />
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
            <van-icon name="orders-o" />
            <span>订单: {{ task.order.orderNo }}</span>
          </div>
          <div class="info-row">
            <van-icon name="user-o" />
            <span>客户: {{ task.order.customerName }}</span>
          </div>
          <div class="info-row">
            <van-icon name="bag-o" />
            <span>商品: {{ productSummary(task.order.products) }}</span>
          </div>
          <div class="info-row">
            <van-icon name="clock-o" />
            <span>预约: {{ formatTime(task.order.appointmentTime) }}</span>
          </div>
          <div class="info-row">
            <van-icon name="shop-o" />
            <span>仓库: {{ task.warehouseName }}</span>
          </div>
        </div>
        
        <div class="task-footer">
          <van-button
            v-if="task.status === 'pending'"
            type="primary"
            size="small"
            @click.stop="handleStart(task)"
          >
            去卸货
          </van-button>
          <van-button
            v-if="task.status === 'in_progress'"
            type="success"
            size="small"
            @click.stop="handleComplete(task)"
          >
            完成卸货
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
    taskNo: 'TK001',
    status: 'pending',
    warehouseName: '朝阳仓库',
    order: {
      orderNo: 'SO20260312000001',
      customerName: '张三',
      appointmentTime: '2026-03-15 10:00',
      products: [
        { productName: '空调', quantity: 2 },
        { productName: '智能门锁', quantity: 1 }
      ]
    }
  },
  {
    id: '2',
    taskNo: 'TK002',
    status: 'in_progress',
    warehouseName: '海淀仓库',
    order: {
      orderNo: 'SO20260312000002',
      customerName: '李四',
      appointmentTime: '2026-03-15 11:00',
      products: [
        { productName: '冰箱', quantity: 1 },
        { productName: '洗衣机', quantity: 1 }
      ]
    }
  },
  {
    id: '3',
    taskNo: 'TK003',
    status: 'completed',
    warehouseName: '丰台仓库',
    order: {
      orderNo: 'SO20260312000003',
      customerName: '王五',
      appointmentTime: '2026-03-15 09:00',
      products: [
        { productName: '电视', quantity: 1 }
      ]
    }
  }
])

const pendingCount = computed(() => {
  return tasks.value.filter(task => task.status === 'pending').length
})

const completedCount = computed(() => {
  return tasks.value.filter(task => task.status === 'completed').length
})

const filteredTasks = computed(() => {
  if (activeTab.value === 0) {
    return tasks.value
  } else if (activeTab.value === 1) {
    return tasks.value.filter(task => task.status === 'pending')
  } else {
    return tasks.value.filter(task => task.status === 'completed')
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
  switch (status) {
    case 'pending': return '待处理';
    case 'in_progress': return '进行中';
    case 'completed': return '已完成';
    case 'cancelled': return '已取消';
    default: return status;
  }
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

const handleTabClick = (tab: any) => {
  activeTab.value = tab.index
}

const handleTaskClick = (task: any) => {
  router.push(`/unloader/task/${task.id}`)
}

const handleStart = (_task: any) => {
  showToast('开始卸货')
  // 实现开始卸货逻辑
}

const handleComplete = (_task: any) => {
  showToast('完成卸货')
  // 实现完成卸货逻辑
}

const handleViewDetail = (task: any) => {
  router.push(`/unloader/task/${task.id}`)
}
</script>

<style scoped lang="scss">
.unloader-tasks {
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
        align-items: center;
        font-size: 14px;
        color: #646566;
        margin-bottom: 8px;
        
        .van-icon {
          margin-right: 8px;
          font-size: 16px;
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
