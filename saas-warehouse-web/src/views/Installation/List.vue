<template>
  <div class="installation-list">
    <el-page-header>
      <template #content>
        <span>安装管理</span>
      </template>
    </el-page-header>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>安装任务列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新建安装任务
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="任务编号">
          <el-input v-model="searchForm.task_id" placeholder="请输入任务编号" />
        </el-form-item>
        <el-form-item label="安装状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="待安装" value="pending" />
            <el-option label="安装中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="安装工">
          <el-input v-model="searchForm.installer_name" placeholder="请输入安装工姓名" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="installations" style="width: 100%">
        <el-table-column prop="id" label="任务ID" width="100" />
        <el-table-column prop="order_id" label="订单ID" width="120" />
        <el-table-column prop="installer_name" label="安装工" />
        <el-table-column prop="installation_address" label="安装地址" />
        <el-table-column prop="difficulty_level" label="难度等级">
          <template #default="{ row }">
            <el-tag :type="getDifficultyType(row.difficulty_level)">
              {{ getDifficultyText(row.difficulty_level) }}
            </el-tag>
          </template>
        </el-table-column>
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
  installer_name: ''
});

// 分页
const pagination = ref({
  current: 1,
  size: 10,
  total: 0
});

// 安装数据
const installations = ref([
  {
    id: 1,
    order_id: 'ORD-2024-001',
    installer_name: '赵六',
    installation_address: '北京市朝阳区客户A',
    difficulty_level: 'medium',
    status: 'completed',
    created_at: '2024-01-01 15:00:00',
    updated_at: '2024-01-01 18:30:00'
  },
  {
    id: 2,
    order_id: 'ORD-2024-002',
    installer_name: '孙七',
    installation_address: '上海市浦东新区客户B',
    difficulty_level: 'high',
    status: 'in_progress',
    created_at: '2024-01-02 11:00:00',
    updated_at: '2024-01-02 14:30:00'
  },
  {
    id: 3,
    order_id: 'ORD-2024-003',
    installer_name: '周八',
    installation_address: '广州市天河区客户C',
    difficulty_level: 'low',
    status: 'pending',
    created_at: '2024-01-03 09:00:00',
    updated_at: '2024-01-03 09:00:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  pagination.value.total = installations.value.length;
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
    pending: '待安装',
    in_progress: '安装中',
    completed: '已完成',
    cancelled: '已取消'
  };
  return textMap[status] || status;
};

// 获取难度类型
const getDifficultyType = (level: string) => {
  const typeMap: Record<string, string> = {
    low: 'success',
    medium: 'warning',
    high: 'danger'
  };
  return typeMap[level] || 'info';
};

// 获取难度文本
const getDifficultyText = (level: string) => {
  const textMap: Record<string, string> = {
    low: '低',
    medium: '中',
    high: '高'
  };
  return textMap[level] || level;
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
    installer_name: ''
  };
};

// 新增
const handleAdd = () => {
  // 模拟新增
  console.log('新增安装任务');
};

// 编辑
const handleEdit = (row: any) => {
  // 模拟编辑
  console.log('编辑安装任务:', row);
};

// 删除
const handleDelete = (row: any) => {
  // 模拟删除
  console.log('删除安装任务:', row);
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