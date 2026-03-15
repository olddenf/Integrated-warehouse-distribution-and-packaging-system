<template>
  <div class="warehouse-list">
    <el-page-header>
      <template #content>
        <span>仓储管理</span>
      </template>
    </el-page-header>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>仓库列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新建仓库
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="仓库名称">
          <el-input v-model="searchForm.name" placeholder="请输入仓库名称" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="正常" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="warehouses" style="width: 100%">
        <el-table-column prop="id" label="仓库ID" width="100" />
        <el-table-column prop="name" label="仓库名称" />
        <el-table-column prop="location" label="仓库位置" />
        <el-table-column prop="capacity" label="容量" />
        <el-table-column prop="used" label="已使用" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
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
  name: '',
  status: ''
});

// 分页
const pagination = ref({
  current: 1,
  size: 10,
  total: 0
});

// 仓库数据
const warehouses = ref([
  {
    id: 1,
    name: '北京仓库',
    location: '北京市朝阳区建国路88号',
    capacity: 10000,
    used: 6500,
    status: 'active',
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 2,
    name: '上海仓库',
    location: '上海市浦东新区张江高科技园区',
    capacity: 15000,
    used: 9800,
    status: 'active',
    created_at: '2024-01-02 14:30:00'
  },
  {
    id: 3,
    name: '广州仓库',
    location: '广州市天河区珠江新城',
    capacity: 12000,
    used: 7200,
    status: 'active',
    created_at: '2024-01-03 09:15:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  pagination.value.total = warehouses.value.length;
});

// 搜索
const handleSearch = () => {
  // 模拟搜索
  console.log('搜索:', searchForm.value);
};

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    status: ''
  };
};

// 新增
const handleAdd = () => {
  // 模拟新增
  console.log('新增仓库');
};

// 编辑
const handleEdit = (row: any) => {
  // 模拟编辑
  console.log('编辑仓库:', row);
};

// 删除
const handleDelete = (row: any) => {
  // 模拟删除
  console.log('删除仓库:', row);
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