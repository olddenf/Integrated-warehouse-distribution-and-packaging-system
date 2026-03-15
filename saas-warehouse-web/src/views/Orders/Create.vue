<template>
  <div class="order-create">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>新建订单</h2>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </div>
      </template>
      
      <el-form :model="orderForm" :rules="rules" ref="formRef" label-width="120px">
        <!-- 基本信息 -->
        <el-form-item label="客户姓名" prop="customerName">
          <el-input v-model="orderForm.customerName" placeholder="请输入客户姓名" />
        </el-form-item>
        
        <el-form-item label="客户电话" prop="customerPhone">
          <el-input v-model="orderForm.customerPhone" placeholder="请输入客户电话" />
        </el-form-item>
        
        <el-form-item label="地址" prop="address">
          <el-input v-model="orderForm.address" placeholder="请输入地址" type="textarea" :rows="3" />
        </el-form-item>
        
        <el-form-item label="预约时间" prop="appointmentTime">
          <el-date-picker
            v-model="orderForm.appointmentTime"
            type="datetime"
            placeholder="选择预约时间"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="orderForm.remark" placeholder="请输入备注" type="textarea" :rows="2" />
        </el-form-item>
        
        <!-- 商品信息 -->
        <el-form-item label="商品信息">
          <el-table :data="orderForm.products" style="width: 100%">
            <el-table-column prop="productName" label="商品名称">
              <template #default="{ row }">
                <el-input v-model="row.productName" placeholder="请输入商品名称" />
              </template>
            </el-table-column>
            <el-table-column prop="productCode" label="商品编码">
              <template #default="{ row }">
                <el-input v-model="row.productCode" placeholder="请输入商品编码" />
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量">
              <template #default="{ row }">
                <el-input v-model.number="row.quantity" type="number" placeholder="请输入数量" />
              </template>
            </el-table-column>
            <el-table-column prop="unit" label="单位">
              <template #default="{ row }">
                <el-input v-model="row.unit" placeholder="请输入单位" />
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="{ $index }">
                <el-button type="danger" size="small" @click="removeProduct($index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-button type="primary" @click="addProduct" style="margin-top: 10px">添加商品</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()

// 订单表单
const orderForm = reactive({
  customerName: '',
  customerPhone: '',
  address: '',
  appointmentTime: null,
  remark: '',
  products: [
    {
      productName: '',
      productCode: '',
      quantity: 1,
      unit: ''
    }
  ]
})

// 验证规则
const rules = {
  customerName: [
    { required: true, message: '请输入客户姓名', trigger: 'blur' }
  ],
  customerPhone: [
    { required: true, message: '请输入客户电话', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入地址', trigger: 'blur' }
  ]
}

// 添加商品
const addProduct = () => {
  orderForm.products.push({
    productName: '',
    productCode: '',
    quantity: 1,
    unit: ''
  })
}

// 删除商品
const removeProduct = (index: number) => {
  orderForm.products.splice(index, 1)
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  const valid = await formRef.value.validate()
  if (!valid) return
  
  // 这里应该调用API创建订单
  console.log('创建订单:', orderForm)
  
  ElMessage.success('订单创建成功')
  router.push('/orders/list')
}

// 取消
const handleCancel = () => {
  router.push('/orders/list')
}
</script>

<style scoped lang="scss">
.order-create {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>