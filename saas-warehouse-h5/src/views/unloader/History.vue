<template>
  <div class="history">
    <van-nav-bar title="历史任务" />
    <van-scroll-view class="scroll-view" scroll-y>
      <div class="history-content">
        <van-tabs v-model:active="activeTab">
          <van-tab title="已完成">
            <div class="task-list">
              <van-cell v-for="task in completedTasks" :key="task.id" :title="task.orderNo" :value="task.statusText">
                <template #default>
                  <div class="task-info">
                    <div class="task-customer">{{ task.customer }}</div>
                    <div class="task-time">{{ task.completedTime }}</div>
                  </div>
                </template>
              </van-cell>
            </div>
          </van-tab>
          <van-tab title="已取消">
            <div class="task-list">
              <van-cell v-for="task in cancelledTasks" :key="task.id" :title="task.orderNo" :value="task.statusText">
                <template #default>
                  <div class="task-info">
                    <div class="task-customer">{{ task.customer }}</div>
                    <div class="task-time">{{ task.cancelledTime }}</div>
                  </div>
                </template>
              </van-cell>
            </div>
          </van-tab>
        </van-tabs>
      </div>
    </van-scroll-view>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const activeTab = ref(0);

const completedTasks = ref([
  {
    id: '1',
    orderNo: 'ORD-2024-001',
    customer: '张三',
    statusText: '已完成',
    completedTime: '2024-01-01 10:30:00'
  },
  {
    id: '2',
    orderNo: 'ORD-2024-002',
    customer: '李四',
    statusText: '已完成',
    completedTime: '2024-01-02 09:15:00'
  },
  {
    id: '3',
    orderNo: 'ORD-2024-003',
    customer: '王五',
    statusText: '已完成',
    completedTime: '2024-01-03 08:45:00'
  }
]);

const cancelledTasks = ref([
  {
    id: '4',
    orderNo: 'ORD-2024-004',
    customer: '赵六',
    statusText: '已取消',
    cancelledTime: '2024-01-04 09:20:00'
  }
]);
</script>

<style scoped>
.history {
  height: 100vh;
  background-color: #f5f7fa;
}

.scroll-view {
  height: calc(100vh - 46px);
}

.history-content {
  padding: 16px;
}

.task-list {
  margin-top: 16px;
}

.task-info {
  font-size: 14px;
  line-height: 1.5;
}

.task-customer {
  color: #333;
  margin-bottom: 4px;
}

.task-time {
  color: #999;
  font-size: 12px;
}
</style>