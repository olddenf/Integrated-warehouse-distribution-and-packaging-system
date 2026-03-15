<template>
  <div class="reports-list">
    <el-page-header>
      <template #content>
        <span>报表分析</span>
      </template>
    </el-page-header>
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>数据概览</span>
        </div>
      </template>
      
      <div class="grid-content">
        <el-statistic title="总订单数" :value="1258" />
        <el-statistic title="总配送任务" :value="892" />
        <el-statistic title="总安装任务" :value="675" />
        <el-statistic title="总收入" :value="128500" prefix="¥" />
      </div>
    </el-card>
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>订单趋势</span>
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="handleDateChange"
          />
        </div>
      </template>
      
      <div class="chart-container">
        <div ref="orderChartRef" class="chart"></div>
      </div>
    </el-card>
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>费用分布</span>
        </div>
      </template>
      
      <div class="chart-container">
        <div ref="feeChartRef" class="chart"></div>
      </div>
    </el-card>
    
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务状态分布</span>
        </div>
      </template>
      
      <div class="chart-container">
        <div ref="statusChartRef" class="chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

// 日期范围
const dateRange = ref([] as any[]);

// 图表引用
const orderChartRef = ref<HTMLElement>();
const feeChartRef = ref<HTMLElement>();
const statusChartRef = ref<HTMLElement>();

// 图表实例
let orderChart: echarts.ECharts | null = null;
let feeChart: echarts.ECharts | null = null;
let statusChart: echarts.ECharts | null = null;

// 生命周期
onMounted(() => {
  nextTick(() => {
    initOrderChart();
    initFeeChart();
    initStatusChart();
  });
});

// 初始化订单趋势图表
const initOrderChart = () => {
  if (orderChartRef.value) {
    orderChart = echarts.init(orderChartRef.value);
    const option = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: [120, 200, 150, 80, 70, 110],
          type: 'line',
          smooth: true
        }
      ]
    };
    orderChart.setOption(option);
  }
};

// 初始化费用分布图表
const initFeeChart = () => {
  if (feeChartRef.value) {
    feeChart = echarts.init(feeChartRef.value);
    const option = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        top: '5%',
        left: 'center'
      },
      series: [
        {
          name: '费用分布',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: [
            { value: 30000, name: '仓储费' },
            { value: 50000, name: '配送费' },
            { value: 40000, name: '安装费' },
            { value: 8500, name: '其他费用' }
          ]
        }
      ]
    };
    feeChart.setOption(option);
  }
};

// 初始化任务状态分布图表
const initStatusChart = () => {
  if (statusChartRef.value) {
    statusChart = echarts.init(statusChartRef.value);
    const option = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        top: '5%',
        left: 'center'
      },
      series: [
        {
          name: '任务状态',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 350, name: '待处理' },
            { value: 420, name: '处理中' },
            { value: 580, name: '已完成' },
            { value: 30, name: '已取消' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };
    statusChart.setOption(option);
  }
};

// 日期范围变化处理
const handleDateChange = () => {
  // 模拟日期范围变化处理
  console.log('日期范围变化:', dateRange.value);
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.grid-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 20px 0;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.chart {
  height: 100%;
  width: 100%;
}

@media screen and (max-width: 768px) {
  .grid-content {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>