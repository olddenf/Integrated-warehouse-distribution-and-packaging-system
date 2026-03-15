<template>
  <div class="order-import">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>批量导入订单</h2>
        </div>
      </template>
      
      <div class="import-content">
        <el-alert
          title="导入说明"
          type="info"
          description="请按照模板格式填写订单数据，然后上传Excel文件进行批量导入。"
          show-icon
        />
        
        <div class="template-download">
          <el-button type="primary" @click="downloadTemplate">下载导入模板</el-button>
        </div>
        
        <div class="file-upload">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :show-file-list="false"
            accept=".xlsx,.xls"
          >
            <el-button type="primary">选择文件</el-button>
          </el-upload>
          <span v-if="fileName" class="file-name">{{ fileName }}</span>
        </div>
        
        <div class="import-button">
          <el-button type="primary" @click="handleImport" :disabled="!fileName">开始导入</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </div>
        
        <div v-if="importing" class="importing">
          <el-progress :percentage="importProgress" :status="importStatus" />
          <p>{{ importMessage }}</p>
        </div>
        
        <div v-if="importResult" class="import-result">
          <el-alert
            :title="importResult.success ? '导入成功' : '导入失败'"
            :type="importResult.success ? 'success' : 'error'"
            :description="importResult.message"
            show-icon
          />
          <el-button v-if="importResult.success" type="primary" @click="viewImportedOrders">查看导入的订单</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 文件信息
const fileName = ref('')
const file = ref<File | null>(null)

// 导入状态
const importing = ref(false)
const importProgress = ref(0)
const importStatus = ref<'success' | 'warning' | 'exception' | ''>('')
const importMessage = ref('')
const importResult = ref<{ success: boolean; message: string } | null>(null)

// 处理文件选择
const handleFileChange = (file: any) => {
  fileName.value = file.name
  file.value = file.raw
}

// 下载模板
const downloadTemplate = () => {
  // 这里应该生成并下载模板文件
  ElMessage.info('模板下载功能开发中')
}

// 开始导入
const handleImport = () => {
  if (!file.value) {
    ElMessage.warning('请选择文件')
    return
  }
  
  importing.value = true
  importProgress.value = 0
  importStatus.value = ''
  importMessage.value = '正在导入...'
  
  // 模拟导入过程
  const interval = setInterval(() => {
    importProgress.value += 10
    if (importProgress.value >= 100) {
      clearInterval(interval)
      importStatus.value = 'success'
      importMessage.value = '导入完成'
      importResult.value = {
        success: true,
        message: '成功导入3条订单数据'
      }
      importing.value = false
    }
  }, 200)
}

// 取消
const handleCancel = () => {
  router.push('/orders/list')
}

// 查看导入的订单
const viewImportedOrders = () => {
  router.push('/orders/list')
}
</script>

<style scoped lang="scss">
.order-import {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .import-content {
    padding: 20px 0;
  }
  
  .template-download {
    margin: 20px 0;
  }
  
  .file-upload {
    margin: 20px 0;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .file-name {
    font-size: 14px;
    color: #606266;
  }
  
  .import-button {
    margin: 20px 0;
  }
  
  .importing {
    margin: 20px 0;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
  }
  
  .import-result {
    margin: 20px 0;
  }
}
</style>