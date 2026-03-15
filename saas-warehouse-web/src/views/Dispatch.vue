<template>
  <div class="dispatch">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>调度排单</h2>
          <el-button type="primary" @click="handleAutoDispatch">自动排单</el-button>
          <el-button @click="handleManualDispatch">手动排单</el-button>
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
              <el-option label="待排单" value="PENDING" />
              <el-option label="已排单" value="DISPATCHED" />
              <el-option label="已完成" value="COMPLETED" />
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
        <el-table-column prop="appointmentTime" label="预约时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleDispatch(row.id)">排单</el-button>
            <el-button size="small" @click="handleViewOrder(row.id)">查看</el-button>
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
    
    <!-- 自动排单对话框 -->
    <el-dialog
      v-model="autoDispatchDialogVisible"
      title="自动排单"
      width="500px"
    >
      <el-form :model="autoDispatchForm" label-width="120px">
        <el-form-item label="订单类型">
          <el-select v-model="autoDispatchForm.orderType" placeholder="请选择订单类型">
            <el-option label="全部" value="" />
            <el-option label="配送" value="DELIVERY" />
            <el-option label="安装" value="INSTALL" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="autoDispatchForm.priority" placeholder="请选择优先级">
            <el-option label="时间优先" value="TIME" />
            <el-option label="距离优先" value="DISTANCE" />
            <el-option label="工作量均衡" value="WORKLOAD" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="autoDispatchDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAutoDispatchConfirm">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 手动排单对话框 -->
    <el-dialog
      v-model="manualDispatchDialogVisible"
      title="手动排单"
      width="500px"
    >
      <el-form :model="manualDispatchForm" label-width="120px">
        <el-form-item label="选择订单">
          <el-select v-model="manualDispatchForm.orderId" placeholder="请选择订单">
            <el-option
              v-for="order in orderList"
              :key="order.id"
              :label="order.orderNo + ' - ' + order.customerName"
              :value="order.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="选择人员">
          <el-select v-model="manualDispatchForm.workerId" placeholder="请选择人员">
            <el-option
              v-for="worker in workerList"
              :key="worker.id"
              :label="worker.name + ' - ' + worker.role"
              :value="worker.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="任务类型">
          <el-select v-model="manualDispatchForm.taskType" placeholder="请选择任务类型">
            <el-option label="配送" value="DELIVERY" />
            <el-option label="安装" value="INSTALL" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="manualDispatchDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleManualDispatchConfirm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

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
    appointmentTime: '2026-03-15 10:00:00',
    status: 'PENDING'
  },
  {
    id: '2',
    orderNo: '202603150002',
    customerName: '李四',
    customerPhone: '13800138002',
    address: '上海市浦东新区陆家嘴金融中心',
    appointmentTime: '2026-03-15 11:00:00',
    status: 'PENDING'
  },
  {
    id: '3',
    orderNo: '202603150003',
    customerName: '王五',
    customerPhone: '13800138003',
    address: '广州市天河区珠江新城',
    appointmentTime: '2026-03-15 12:00:00',
    status: 'DISPATCHED'
  }
])

// 工作人员列表
const workerList = ref([
  {
    id: '1',
    name: '赵司机',
    role: 'DRIVER'
  },
  {
    id: '2',
    name: '钱安装',
    role: 'INSTALLER'
  },
  {
    id: '3',
    name: '孙卸货',
    role: 'UNLOADER'
  }
])

// 自动排单对话框
const autoDispatchDialogVisible = ref(false)
const autoDispatchForm = reactive({
  orderType: '',
  priority: 'TIME'
})

// 手动排单对话框
const manualDispatchDialogVisible = ref(false)
const manualDispatchForm = reactive({
  orderId: '',
  workerId: '',
  taskType: 'DELIVERY'
})

// 状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'PENDING': return 'info'
    case 'DISPATCHED': return 'warning'
    case 'COMPLETED': return 'success'
    default: return 'info'
  }
}

// 状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'PENDING': return '待排单'
    case 'DISPATCHED': return '已排单'
    case 'COMPLETED': return '已完成'
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

// 自动排单
const handleAutoDispatch = () => {
  autoDispatchDialogVisible.value = true
}

// 手动排单
const handleManualDispatch = () => {
  manualDispatchDialogVisible.value = true
}

// 排单
const handleDispatch = (orderId: string) => {
  manualDispatchForm.orderId = orderId
  manualDispatchDialogVisible.value = true
}

// 查看订单
const handleViewOrder = (orderId: string) => {
  router.push(`/orders/detail/${orderId}`)
}

// 自动排单确认
const handleAutoDispatchConfirm = () => {
  // 这里应该调用API进行自动排单
  console.log('自动排单:', autoDispatchForm)
  autoDispatchDialogVisible.value = false
  ElMessage.success('自动排单成功')
}

// 手动排单确认
const handleManualDispatchConfirm = () => {
  // 这里应该调用API进行手动排单
  console.log('手动排单:', manualDispatchForm)
  manualDispatchDialogVisible.value = false
  ElMessage.success('手动排单成功')
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
.dispatch {
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