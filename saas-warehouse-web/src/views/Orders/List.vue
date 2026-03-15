<template>
  <div class="order-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>订单列表</h2>
          <el-button type="primary" @click="handleCreateOrder">新建订单</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-form :inline="true" :model="searchForm" class="mb-4">
          <el-form-item label="订单号">
            <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" />
          </el-form-item>
          <el-form-item label="客户姓名">
            <el-input v-model="searchForm.customerName" placeholder="请输入客户姓名" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态">
              <el-option label="全部" value="" />
              <el-option label="待处理" value="PENDING" />
              <el-option label="已调度" value="DISPATCHED" />
              <el-option label="已完成" value="COMPLETED" />
              <el-option label="已取消" value="CANCELLED" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 订单列表 -->
      <el-table :data="orderList" style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="180" />
        <el-table-column prop="customerName" label="客户姓名" width="120" />
        <el-table-column prop="customerPhone" label="客户电话" width="150" />
        <el-table-column prop="address" label="地址" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalAmount" label="总金额" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleViewOrder(row.id)">查看</el-button>
            <el-button size="small" @click="handleEditOrder(row.id)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleCancelOrder(row.id)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 搜索表单
const searchForm = reactive({
  orderNo: '',
  customerName: '',
  status: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 订单列表
const orderList = ref([
  {
    id: '1',
    orderNo: '202603150001',
    customerName: '张三',
    customerPhone: '13800138001',
    address: '北京市朝阳区建国路88号',
    status: 'PENDING',
    totalAmount: 1000.00,
    createTime: '2026-03-15 10:00:00'
  },
  {
    id: '2',
    orderNo: '202603150002',
    customerName: '李四',
    customerPhone: '13800138002',
    address: '上海市浦东新区陆家嘴金融中心',
    status: 'DISPATCHED',
    totalAmount: 2000.00,
    createTime: '2026-03-15 11:00:00'
  },
  {
    id: '3',
    orderNo: '202603150003',
    customerName: '王五',
    customerPhone: '13800138003',
    address: '广州市天河区珠江新城',
    status: 'COMPLETED',
    totalAmount: 1500.00,
    createTime: '2026-03-15 12:00:00'
  }
])

// 状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'PENDING': return 'info'
    case 'DISPATCHED': return 'warning'
    case 'COMPLETED': return 'success'
    case 'CANCELLED': return 'danger'
    default: return 'info'
  }
}

// 状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'PENDING': return '待处理'
    case 'DISPATCHED': return '已调度'
    case 'COMPLETED': return '已完成'
    case 'CANCELLED': return '已取消'
    default: return status
  }
}

// 搜索
const handleSearch = () => {
  console.log('搜索:', searchForm)
  // 这里应该调用API进行搜索
}

// 重置
const resetForm = () => {
  searchForm.orderNo = ''
  searchForm.customerName = ''
  searchForm.status = ''
}

// 新建订单
const handleCreateOrder = () => {
  router.push('/orders/create')
}

// 查看订单
const handleViewOrder = (id: string) => {
  router.push(`/orders/detail/${id}`)
}

// 编辑订单
const handleEditOrder = (id: string) => {
  router.push(`/orders/edit/${id}`)
}

// 取消订单
const handleCancelOrder = (_id: string) => {
  ElMessageBox.confirm('确定要取消这个订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该调用API取消订单
    ElMessage.success('订单已取消')
  }).catch(() => {
    // 取消操作
  })
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  // 这里应该调用API获取数据
}

// 当前页变化
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current
  // 这里应该调用API获取数据
}

// 页面挂载时
onMounted(() => {
  // 这里应该调用API获取订单列表
  pagination.total = orderList.value.length
})
</script>

<style scoped lang="scss">
.order-list {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-filter {
    margin-bottom: 20px;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>