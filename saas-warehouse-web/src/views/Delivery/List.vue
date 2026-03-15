<template>
  <div class="delivery-list">
    <el-page-header>
      <template #content>
        <span>配送管理</span>
      </template>
    </el-page-header>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配送任务列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新建配送任务
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="任务编号">
          <el-input v-model="searchForm.task_id" placeholder="请输入任务编号" />
        </el-form-item>
        <el-form-item label="配送状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="待配送" value="pending" />
            <el-option label="配送中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="司机">
          <el-input v-model="searchForm.driver_name" placeholder="请输入司机姓名" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="deliveries" style="width: 100%">
        <el-table-column prop="id" label="任务ID" width="100" />
        <el-table-column prop="order_id" label="订单ID" width="120" />
        <el-table-column prop="driver_name" label="司机" />
        <el-table-column prop="start_location" label="起始位置" />
        <el-table-column prop="end_location" label="目的位置" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="updated_at" label="更新时间" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="mt-4">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Plus } from '@element-plus/icons-vue';

// 搜索表单
const searchForm = ref({
  task_id: '',
  status: '',
  driver_name: ''
});

// 分页
const pagination = ref({
  current: 1,
  size: 10,
  total: 0
});

// 配送数据
const deliveries = ref([
  {
    id: 1,
    order_id: 'ORD-2024-001',
    driver_name: '张三',
    start_location: '北京仓库',
    end_location: '北京市朝阳区客户A',
    status: 'completed',
    created_at: '2024-01-01 10:00:00',
    updated_at: '2024-01-01 14:30:00'
  },
  {
    id: 2,
    order_id: 'ORD-2024-002',
    driver_name: '李四',
    start_location: '上海仓库',
    end_location: '上海市浦东新区客户B',
    status: 'in_progress',
    created_at: '2024-01-02 09:00:00',
    updated_at: '2024-01-02 10:30:00'
  },
  {
    id: 3,
    order_id: 'ORD-2024-003',
    driver_name: '王五',
    start_location: '广州仓库',
    end_location: '广州市天河区客户C',
    status: 'pending',
    created_at: '2024-01-03 08:00:00',
    updated_at: '2024-01-03 08:00:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  pagination.value.total = deliveries.value.length;
});

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  };
  return typeMap[status] || 'info';
};

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '待配送',
    in_progress: '配送中',
    completed: '已完成',
    cancelled: '已取消'
  };
  return textMap[status] || status;
};

// 搜索
const handleSearch = () => {
  // 模拟搜索
  console.log('搜索:', searchForm.value);
};

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    task_id: '',
    status: '',
    driver_name: ''
  };
};

// 新增
const handleAdd = () => {
  // 模拟新增
  console.log('新增配送任务');
};

// 编辑
const handleEdit = (row: any) => {
  // 模拟编辑
  console.log('编辑配送任务:', row);
};

// 删除
const handleDelete = (row: any) => {
  // 模拟删除
  console.log('删除配送任务:', row);
};

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.value.size = size;
};

const handleCurrentChange = (current: number) => {
  pagination.value.current = current;
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>