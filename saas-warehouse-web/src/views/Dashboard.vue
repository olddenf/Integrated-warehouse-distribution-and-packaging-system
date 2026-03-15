<template>
  <div class="dashboard">
    <h1 class="page-title">首页</h1>
    
    <!-- 今日概览 -->
    <div class="overview-section">
      <h2 class="section-title">今日概览</h2>
      <div class="stat-cards">
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">今日订单</span>
            <el-icon class="stat-icon"><Document /></el-icon>
          </div>
          <div class="stat-value">{{ stats.todayOrders }}</div>
          <div class="stat-footer">
            <span class="stat-trend positive">↑ 12%</span>
            <span class="stat-label">较昨日</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">进行中</span>
            <el-icon class="stat-icon"><Timer /></el-icon>
          </div>
          <div class="stat-value">{{ stats.inProgress }}</div>
          <div class="stat-footer">
            <span class="stat-label">当前</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">已完成</span>
            <el-icon class="stat-icon"><Check /></el-icon>
          </div>
          <div class="stat-value">{{ stats.completed }}</div>
          <div class="stat-footer">
            <span class="stat-trend positive">↑ 8%</span>
            <span class="stat-label">较昨日</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">待处理</span>
            <el-icon class="stat-icon"><Warning /></el-icon>
          </div>
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-footer">
            <span class="stat-label">当前</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-item">
        <h3 class="chart-title">订单趋势图（7天）</h3>
        <div ref="trendChart" class="chart-container"></div>
      </div>
      
      <div class="chart-item">
        <h3 class="chart-title">人员工作量排名</h3>
        <div ref="rankingChart" class="chart-container"></div>
      </div>
    </div>
    
    <!-- 待办任务 -->
    <div class="todo-section">
      <h2 class="section-title">待办任务</h2>
      <el-table :data="todoTasks" stripe style="width: 100%">
        <el-table-column prop="orderNo" label="订单号" width="120" />
        <el-table-column prop="customer" label="客户" width="100" />
        <el-table-column prop="type" label="类型" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleAction(scope.row)">
              {{ scope.row.status === '待派单' ? '派单' : '详情' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import * as echarts from 'echarts'
import { Document, Timer, Check, Warning } from '@element-plus/icons-vue'

const trendChart = ref()
const rankingChart = ref()

const stats = reactive({
  todayOrders: 156,
  inProgress: 23,
  completed: 128,
  pending: 15
})

const todoTasks = reactive([
  { orderNo: 'SO001', customer: '张三', type: '配送', status: '待派单' },
  { orderNo: 'SO002', customer: '李四', type: '安装', status: '进行中' },
  { orderNo: 'SO003', customer: '王五', type: '卸货', status: '待派单' },
  { orderNo: 'SO004', customer: '赵六', type: '配送', status: '待派单' }
])

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    '待派单': 'info',
    '进行中': 'warning',
    '已完成': 'success',
    '已取消': 'danger'
  }
  return typeMap[status] || 'info'
}

const handleAction = (task: any) => {
  console.log('处理任务:', task)
  // 实现任务处理逻辑
}

const initTrendChart = () => {
  const chart = echarts.init(trendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['3/9', '3/10', '3/11', '3/12', '3/13', '3/14', '3/15']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '订单量',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 101, 134, 90, 230, 156],
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
            ]
          }
        }
      }
    ]
  }
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const initRankingChart = () => {
  const chart = echarts.init(rankingChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: ['张师傅', '李师傅', '王师傅', '赵师傅', '钱师傅']
    },
    series: [
      {
        name: '完成订单数',
        type: 'bar',
        data: [12, 10, 9, 8, 7],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        }
      }
    ]
  }
  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

onMounted(() => {
  initTrendChart()
  initRankingChart()
})
</script>

<style scoped lang="scss">
.dashboard {
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 24px;
  }
  
  .section-title {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16px;
  }
  
  .overview-section {
    margin-bottom: 32px;
  }
  
  .stat-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
  }
  
  .stat-card {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    
    .stat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      
      .stat-title {
        font-size: 14px;
        color: #606266;
      }
      
      .stat-icon {
        font-size: 20px;
        color: #409eff;
      }
    }
    
    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }
    
    .stat-footer {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .stat-trend {
        font-size: 12px;
        
        &.positive {
          color: #67c23a;
        }
        
        &.negative {
          color: #f56c6c;
        }
      }
      
      .stat-label {
        font-size: 12px;
        color: #909399;
      }
    }
  }
  
  .charts-section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
    margin-bottom: 32px;
    
    .chart-item {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
      
      .chart-title {
        font-size: 14px;
        font-weight: 600;
        color: #303133;
        margin-bottom: 16px;
      }
      
      .chart-container {
        height: 300px;
      }
    }
  }
  
  .todo-section {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
}
</style>
