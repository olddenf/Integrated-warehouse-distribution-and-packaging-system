<template>
  <div class="settings-list">
    <el-page-header>
      <template #content>
        <span>系统设置</span>
      </template>
    </el-page-header>
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>基本设置</span>
        </div>
      </template>
      
      <el-form :model="basicSettings" label-width="120px">
        <el-form-item label="系统名称">
          <el-input v-model="basicSettings.system_name" />
        </el-form-item>
        <el-form-item label="系统版本">
          <el-input v-model="basicSettings.system_version" disabled />
        </el-form-item>
        <el-form-item label="系统描述">
          <el-input v-model="basicSettings.system_description" type="textarea" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>API配置</span>
        </div>
      </template>
      
      <el-form :model="apiSettings" label-width="120px">
        <el-form-item label="高德API密钥">
          <el-input v-model="apiSettings.gaode_api_key" type="password" />
        </el-form-item>
        <el-form-item label="高德API服务地址">
          <el-input v-model="apiSettings.gaode_api_url" />
        </el-form-item>
        <el-form-item label="OSS存储配置">
          <el-input v-model="apiSettings.oss_config" type="textarea" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveApiSettings">保存设置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统日志</span>
        </div>
      </template>
      
      <el-table :data="logs" style="width: 100%">
        <el-table-column prop="id" label="日志ID" width="100" />
        <el-table-column prop="level" label="日志级别">
          <template #default="{ row }">
            <el-tag :type="getLogLevelType(row.level)">{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="日志内容" />
        <el-table-column prop="created_at" label="创建时间" />
      </el-table>
      
      <div class="mt-4">
        <el-button type="danger" @click="clearLogs">清空日志</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// 基本设置
const basicSettings = ref({
  system_name: '仓配装SaaS系统',
  system_version: '1.0.0',
  system_description: '智能仓储配送安装管理系统'
});

// API配置
const apiSettings = ref({
  gaode_api_key: 'your_gaode_api_key',
  gaode_api_url: 'https://restapi.amap.com',
  oss_config: `{
  "access_key": "your_access_key",
  "secret_key": "your_secret_key",
  "bucket": "your_bucket",
  "endpoint": "your_endpoint"
}`
});

// 系统日志
const logs = ref([
  {
    id: 1,
    level: 'info',
    message: '系统启动成功',
    created_at: '2024-01-01 00:00:00'
  },
  {
    id: 2,
    level: 'warning',
    message: 'API调用频率过高',
    created_at: '2024-01-01 10:30:00'
  },
  {
    id: 3,
    level: 'error',
    message: '数据库连接失败',
    created_at: '2024-01-01 15:45:00'
  }
]);

// 生命周期
onMounted(() => {
  // 初始化数据
  console.log('系统设置页面加载');
});

// 获取日志级别类型
const getLogLevelType = (level: string) => {
  const typeMap: Record<string, string> = {
    info: 'info',
    warning: 'warning',
    error: 'danger'
  };
  return typeMap[level] || 'info';
};

// 保存基本设置
const saveBasicSettings = () => {
  // 模拟保存
  console.log('保存基本设置:', basicSettings.value);
};

// 保存API设置
const saveApiSettings = () => {
  // 模拟保存
  console.log('保存API设置:', apiSettings.value);
};

// 清空日志
const clearLogs = () => {
  // 模拟清空
  console.log('清空日志');
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>