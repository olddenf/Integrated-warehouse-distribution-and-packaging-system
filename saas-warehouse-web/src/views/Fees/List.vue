<template>
  <div class="fees-list">
    <el-page-header>
      <template #content>
        <span>费用管理</span>
      </template>
    </el-page-header>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>费用记录列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新建费用记录
          </el-button>
        </div>
      </template>
      
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="费用类型">
          <el-select v-model="searchForm.type" placeholder="请选择费用类型">
            <el-option label="仓储费" value="warehouse" />
            <el-option label="配送费" value="delivery" />
            <el-option label="安装费" value="installation" />
            <el-option label="其他费用" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="费用状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="待结算" value="pending" />
            <el-option label="已结算" value="settled" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="fees" style="width: 100%">
        <el-table-column prop="id" label="费用ID" width="100" />
        <el-table-column prop="order_id" label="订单ID" width="120" />
        <el-table-column prop="type" label="费用类型">
          <template #default="{ row }">
            <el-tag>{{ getTypeText(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" width="120">
          <template #default="{ row }">
            ¥{{ row.amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'settled' ? 'success' : 'info'">
              {{ row.status === 'settled' ? '已结算' : '待结算' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
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
  type: '',
  status: '',
  date_range: [] as any[]
});

// 分页
const pagination = ref({
  current: 1,
  size: 10,
  total: 0
});

// 费用数据
const fees = ref([
  {
    id: 1,
    order_id: 'ORD-2024-001',
    type: 'warehouse',
    amount: 100.50,
    status: 'settled',
    description: '北京仓库存储费用',
    created_at: '2024-01-01 10:00:00'
  },
  {
    id: 2,
    order_id: 'ORD-2024-002',
    type: 'delivery',
    amount: 200.00,
    status: 'pending',
    description: '上海配送费用',
    created_at: '2024-01-02 09:30:00'
  },
  {
    id: 3,
    order_id: 'ORD-2024-003',
    type: 'installation',
    amount: 300.75,
    status: 'settled',
    description: '广州安装费用',
    created_at: '2024-01-03 14:00:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  pagination.value.total = fees.value.length;
});

// 获取费用类型文本
const getTypeText = (type: string) => {
  const textMap: Record<string, string> = {
    warehouse: '仓储费',
    delivery: '配送费',
    installation: '安装费',
    other: '其他费用'
  };
  return textMap[type] || type;
};

// 搜索
const handleSearch = () => {
  // 模拟搜索
  console.log('搜索:', searchForm.value);
};

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    type: '',
    status: '',
    date_range: []
  };
};

// 新增
const handleAdd = () => {
  // 模拟新增
  console.log('新增费用记录');
};

// 编辑
const handleEdit = (row: any) => {
  // 模拟编辑
  console.log('编辑费用记录:', row);
};

// 删除
const handleDelete = (row: any) => {
  // 模拟删除
  console.log('删除费用记录:', row);
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