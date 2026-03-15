<template>
  <div class="users-list">
    <el-page-header>
      <template #content>
        <span>用户管理</span>
      </template>
    </el-page-header>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新建用户
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="searchForm.role" placeholder="请选择角色">
            <el-option label="系统管理员" value="admin" />
            <el-option label="调度员" value="dispatcher" />
            <el-option label="仓管员" value="warehouse" />
            <el-option label="司机" value="driver" />
            <el-option label="安装工" value="installer" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="用户ID" width="100" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <el-tag>{{ getRoleText(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
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
  username: '',
  role: '',
  status: ''
});

// 分页
const pagination = ref({
  current: 1,
  size: 10,
  total: 0
});

// 用户数据
const users = ref([
  {
    id: 1,
    username: 'admin',
    name: '系统管理员',
    email: 'admin@example.com',
    phone: '13800138000',
    role: 'admin',
    status: 'active',
    created_at: '2024-01-01 00:00:00'
  },
  {
    id: 2,
    username: 'dispatcher1',
    name: '调度员张三',
    email: 'dispatcher1@example.com',
    phone: '13800138001',
    role: 'dispatcher',
    status: 'active',
    created_at: '2024-01-02 10:00:00'
  },
  {
    id: 3,
    username: 'warehouse1',
    name: '仓管员李四',
    email: 'warehouse1@example.com',
    phone: '13800138002',
    role: 'warehouse',
    status: 'active',
    created_at: '2024-01-03 09:00:00'
  },
  {
    id: 4,
    username: 'driver1',
    name: '司机王五',
    email: 'driver1@example.com',
    phone: '13800138003',
    role: 'driver',
    status: 'active',
    created_at: '2024-01-04 08:00:00'
  },
  {
    id: 5,
    username: 'installer1',
    name: '安装工赵六',
    email: 'installer1@example.com',
    phone: '13800138004',
    role: 'installer',
    status: 'active',
    created_at: '2024-01-05 07:00:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  pagination.value.total = users.value.length;
});

// 获取角色文本
const getRoleText = (role: string) => {
  const textMap: Record<string, string> = {
    admin: '系统管理员',
    dispatcher: '调度员',
    warehouse: '仓管员',
    driver: '司机',
    installer: '安装工'
  };
  return textMap[role] || role;
};

// 搜索
const handleSearch = () => {
  // 模拟搜索
  console.log('搜索:', searchForm.value);
};

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    username: '',
    role: '',
    status: ''
  };
};

// 新增
const handleAdd = () => {
  // 模拟新增
  console.log('新增用户');
};

// 编辑
const handleEdit = (row: any) => {
  // 模拟编辑
  console.log('编辑用户:', row);
};

// 删除
const handleDelete = (row: any) => {
  // 模拟删除
  console.log('删除用户:', row);
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