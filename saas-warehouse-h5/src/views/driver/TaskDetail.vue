<template>
  <div class="task-detail">
    <van-nav-bar title="任务详情" />
    <van-scroll-view class="scroll-view" scroll-y>
      <div class="detail-content">
        <van-card>
          <template #header>
            <div class="card-header">
              <h3 class="order-no">订单号: {{ task.orderNo }}</h3>
              <van-tag :type="statusType">{{ statusText }}</van-tag>
            </div>
          </template>
          
          <van-cell title="客户信息">
            <template #default>
              <div class="customer-info">
                <div>{{ task.customer }}</div>
                <div>{{ task.phone }}</div>
              </div>
            </template>
          </van-cell>
          
          <van-cell title="起点">
            <template #default>
              <div>{{ task.startAddress }}</div>
            </template>
          </van-cell>
          
          <van-cell title="终点">
            <template #default>
              <div>{{ task.endAddress }}</div>
            </template>
          </van-cell>
          
          <van-cell title="货物信息">
            <template #default>
              <div class="goods-info">
                <div v-for="item in task.goods" :key="item.id" class="goods-item">
                  <div class="goods-name">{{ item.name }}</div>
                  <div class="goods-quantity">数量: {{ item.quantity }} {{ item.unit }}</div>
                </div>
              </div>
            </template>
          </van-cell>
          
          <van-cell title="备注">
            <template #default>
              <div>{{ task.remark || '无' }}</div>
            </template>
          </van-cell>
        </van-card>
        
        <div class="action-buttons">
          <van-button type="primary" class="action-button" @click="handleStart" v-if="task.status === 'pending'">开始配送</van-button>
          <van-button type="primary" class="action-button" @click="handleNavigation" v-else-if="task.status === 'in_progress'">导航</van-button>
          <van-button type="primary" class="action-button" @click="handleComplete" v-else-if="task.status === 'in_progress'">完成配送</van-button>
        </div>
      </div>
    </van-scroll-view>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const task = ref({
  id: '1',
  orderNo: 'ORD-2024-001',
  customer: '张三',
  phone: '13800138001',
  startAddress: '北京仓库',
  endAddress: '北京市朝阳区建国路88号',
  status: 'pending',
  goods: [
    { id: '1', name: '商品A', quantity: 10, unit: '件' },
    { id: '2', name: '商品B', quantity: 5, unit: '箱' }
  ],
  remark: '注意轻拿轻放'
});

const taskStatus = computed(() => task.value.status);

const statusType = computed(() => {
  switch (taskStatus.value) {
    case 'pending': return 'primary';
    case 'in_progress': return 'warning';
    case 'completed': return 'success';
    case 'cancelled': return 'danger';
    default: return 'primary';
  }
});

const statusText = computed(() => {
  switch (taskStatus.value) {
    case 'pending': return '待配送';
    case 'in_progress': return '配送中';
    case 'completed': return '已完成';
    case 'cancelled': return '已取消';
    default: return taskStatus.value;
  }
});

const handleStart = () => {
  console.log('开始配送');
  task.value.status = 'in_progress';
};

const handleNavigation = () => {
  console.log('导航');
  router.push('/driver/map');
};

const handleComplete = () => {
  console.log('完成配送');
  task.value.status = 'completed';
};
</script>

<style scoped>
.task-detail {
  height: 100vh;
  background-color: #f5f7fa;
}

.scroll-view {
  height: calc(100vh - 46px);
}

.detail-content {
  padding: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.order-no {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.customer-info {
  line-height: 1.5;
}

.goods-info {
  line-height: 1.5;
}

.goods-item {
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.goods-name {
  font-weight: 500;
  color: #333;
}

.goods-quantity {
  font-size: 14px;
  color: #666;
}

.action-buttons {
  margin-top: 24px;
}

.action-button {
  width: 100%;
  margin-bottom: 12px;
}
</style>