# SaaS仓配装一体化管理系统 H5移动端UI设计文档

## 文档信息
- **项目名称**: SaaS仓配装一体化管理系统
- **文档版本**: v1.0
- **创建日期**: 2026-03-15
- **文档类型**: H5 UI设计说明书
- **技术栈**: Vue3 + Vant4 + TypeScript

---

## 一、设计概述

### 1.1 设计目标
为卸货人员、司机、安装师傅提供简洁、高效、易用的移动端操作界面，实现任务接收、位置打卡、照片上传、导航等核心功能，提升现场作业效率。

### 1.2 设计原则
- **大屏友好**: 按钮和文字尺寸适配移动端操作习惯
- **操作简化**: 减少操作步骤，常用功能一键触达
- **容错性强**: 防误触设计，操作可撤销
- **离线优先**: 核心功能支持离线使用，联网后自动同步
- **三端差异化**: 卸货/司机/安装三端针对性优化交互流程

### 1.3 目标用户
| 用户角色 | 核心场景 | 设计重点 |
|---------|---------|---------|
| 卸货人员 | 任务查看、卸货打卡 | 任务清晰、打卡便捷 |
| 司机 | 导航、签收、状态同步 | 导航准确、签收便捷 |
| 安装师傅 | 任务详情、验收拍照 | 信息详细、多图上传 |

---

## 二、整体布局设计

### 2.1 移动端布局结构
```
┌─────────────────────────────────┐
│          顶部导航栏                │
│  [←] 任务列表            [通知]  │
├─────────────────────────────────┤
│                                 │
│          主内容区                 │
│                                 │
│  (页面内容 + 底部操作栏)          │
│                                 │
└─────────────────────────────────┘
│          底部Tab导航               │
│  [任务] [我的] [消息] [我的]      │
└─────────────────────────────────┘
```

### 2.2 顶部导航栏设计

#### 组件实现
```vue
<template>
  <van-nav-bar
    :title="title"
    :left-arrow="showBack"
    :left-text="leftText"
    :right-text="rightText"
    :safe-area-inset-top="safeAreaInsetTop"
    @click-left="handleBack"
    @click-right="handleRight"
  >
    <template #left v-if="showBack">
      <van-icon name="arrow-left" />
    </template>
    <template #right v-if="showNotification">
      <van-badge :content="unreadCount" :max="99">
        <van-icon name="bell" size="20" />
      </van-badge>
    </template>
  </van-nav-bar>
</template>

<script setup lang="ts">
const props = defineProps<{
  title: string
  showBack?: boolean
  leftText?: string
  rightText?: string
  showNotification?: boolean
  safeAreaInsetTop?: boolean
}>()

const emit = defineEmits(['back', 'right'])

const handleBack = () => {
  emit('back')
  // 默认返回上一页
  if (!props.showBack) {
    window.history.back()
  }
}

const handleRight = () => {
  emit('right')
}
</script>
```

### 2.3 底部Tab导航设计

#### 卸货端Tab配置
```typescript
export const unloaderTabConfig = [
  {
    path: '/unloader/tasks',
    icon: 'todo-list-o',
    text: '任务',
    badge: 0
  },
  {
    path: '/unloader/history',
    icon: 'records-o',
    text: '历史',
    badge: 0
  },
  {
    path: '/unloader/profile',
    icon: 'user-o',
    text: '我的',
    badge: 0
  }
]
```

#### 司机端Tab配置
```typescript
export const driverTabConfig = [
  {
    path: '/driver/tasks',
    icon: 'logistics',
    text: '任务',
    badge: 0
  },
  {
    path: '/driver/map',
    icon: 'location-o',
    text: '地图',
    badge: 0
  },
  {
    path: '/driver/history',
    icon: 'records-o',
    text: '历史',
    badge: 0
  },
  {
    path: '/driver/profile',
    icon: 'user-o',
    text: '我的',
    badge: 0
  }
]
```

#### 安装端Tab配置
```typescript
export const installerTabConfig = [
  {
    path: '/installer/tasks',
    icon: 'todo-list-o',
    text: '任务',
    badge: 0
  },
  {
    path: '/installer/guide',
    icon: 'guide-o',
    text: '教程',
    badge: 0
  },
  {
    path: '/installer/history',
    icon: 'records-o',
    text: '历史',
    badge: 0
  },
  {
    path: '/installer/profile',
    icon: 'user-o',
    text: '我的',
    badge: 0
  }
]
```

---

## 三、卸货端页面设计

### 3.1 任务列表页

#### 页面布局
```
┌─────────────────────────────────┐
│  [←] 卸货任务         今日(5)    │
├─────────────────────────────────┤
│  筛选栏                          │
│  [全部▼] [待处理 3] [已完成 2]  │
├─────────────────────────────────┤
│  任务卡片                        │
│  ┌─────────────────────────────┐│
│  │  TK001 · 卸货任务            ││
│  │  ─────────────────────────   ││
│  │  订单: SO20260312000001     ││
│  │  客户: 张三                  ││
│  │  商品: 空调×2 智能门锁×1      ││
│  │  ─────────────────────────   ││
│  │  预约: 2026-03-15 10:00     ││
│  │  仓库: 朝阳仓库              ││
│  │  ─────────────────────────   ││
│  │  <span class="status">待处理</span>│
│  │              [去卸货]         ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │  TK002 · 卸货任务            ││
│  │  ...                        ││
│  └─────────────────────────────┘│
└─────────────────────────────────┘
│  [任务] [历史] [我的]            │
└─────────────────────────────────┘
```

#### 任务卡片组件
```vue
<template>
  <div class="task-card" @click="handleClick">
    <!-- 头部 -->
    <div class="task-header">
      <span class="task-no">{{ task.taskNo }}</span>
      <van-tag :type="statusType">{{ statusText }}</van-tag>
    </div>

    <!-- 信息区 -->
    <div class="task-info">
      <div class="info-row">
        <van-icon name="orders-o" />
        <span>订单: {{ task.order.orderNo }}</span>
      </div>
      <div class="info-row">
        <van-icon name="user-o" />
        <span>客户: {{ task.order.customerName }}</span>
      </div>
      <div class="info-row">
        <van-icon name="bag-o" />
        <span>商品: {{ productSummary }}</span>
      </div>
      <div class="info-row">
        <van-icon name="clock-o" />
        <span>预约: {{ formatTime(task.order.appointmentTime) }}</span>
      </div>
      <div class="info-row">
        <van-icon name="shop-o" />
        <span>仓库: {{ task.warehouseName }}</span>
      </div>
    </div>

    <!-- 底部操作 -->
    <div class="task-footer">
      <van-button
        v-if="task.status === 'pending'"
        type="primary"
        size="small"
        @click.stop="handleStart"
      >
        去卸货
      </van-button>
      <van-button
        v-if="task.status === 'in_progress'"
        type="success"
        size="small"
        @click.stop="handleComplete"
      >
        完成卸货
      </van-button>
      <van-button
        v-if="task.status === 'completed'"
        size="small"
        plain
        @click.stop="handleViewDetail"
      >
        查看详情
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TaskStatus } from '@/types/task'

const props = defineProps<{
  task: Task
}>()

const statusType = computed(() => {
  const typeMap = {
    [TaskStatus.PENDING]: 'warning',
    [TaskStatus.IN_PROGRESS]: 'primary',
    [TaskStatus.COMPLETED]: 'success',
    [TaskStatus.CANCELLED]: 'danger'
  }
  return typeMap[props.task.status]
})

const statusText = computed(() => {
  const textMap = {
    [TaskStatus.PENDING]: '待处理',
    [TaskStatus.IN_PROGRESS]: '进行中',
    [TaskStatus.COMPLETED]: '已完成',
    [TaskStatus.CANCELLED]: '已取消'
  }
  return textMap[props.task.status]
})

const productSummary = computed(() => {
  const products = props.task.order.products
  if (products.length <= 2) {
    return products.map(p => `${p.productName}×${p.quantity}`).join(' ')
  }
  return products.slice(0, 2).map(p => `${p.productName}×${p.quantity}`).join(' ') + '...'
})
</script>

<style scoped lang="scss">
.task-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;

    .task-no {
      font-size: 16px;
      font-weight: 600;
      color: #323233;
    }
  }

  .task-info {
    margin-bottom: 12px;

    .info-row {
      display: flex;
      align-items: center;
      font-size: 14px;
      color: #646566;
      margin-bottom: 8px;

      .van-icon {
        margin-right: 8px;
        font-size: 16px;
      }
    }
  }

  .task-footer {
    display: flex;
    justify-content: flex-end;
  }
}
</style>
```

### 3.2 卸货执行页

#### 页面布局
```
┌─────────────────────────────────┐
│  [←] 卸货执行                     │
├─────────────────────────────────┤
│  订单信息                        │
│  ┌─────────────────────────────┐│
│  │ 订单号: SO20260312000001   ││
│  │ 客户: 张三  13800138000     ││
│  │ 仓库: 朝阳仓库              ││
│  │                             ││
│  │ 商品清单:                    ││
│  │ • 空调挂机 × 2              ││
│  │ • 智能门锁 × 1              ││
│  │                             ││
│  │ 合计: 3件                   ││
│  └─────────────────────────────┘│
│                                 │
│  卸货记录                        │
│  ┌─────────────────────────────┐│
│  │ 空调挂机: [____] 台         ││
│  │ 智能门锁: [____] 把         ││
│  └─────────────────────────────┘│
│                                 │
│  位置确认                        │
│  ┌─────────────────────────────┐│
│  │  ✓ 已定位: 朝阳区...        ││
│  │  (距离仓库 500m)            ││
│  │                             ││
│  │  [重新定位]                 ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │  拍照打卡                    ││
│  │  ┌─────┐ ┌─────┐ ┌─────┐  ││
│  │  │  +  │ │  +  │ │  +  │  ││
│  │  └─────┘ └─────┘ └─────┘  ││
│  │  (最多3张，单张≤2MB)        ││
│  └─────────────────────────────┘│
│                                 │
│  备注说明                        │
│  ┌─────────────────────────────┐│
│  │  [_____________________]    ││
│  │  请输入备注信息              ││
│  └─────────────────────────────┘│
│                                 │
│           [完成卸货]              │
└─────────────────────────────────┘
```

#### 位置定位组件
```vue
<template>
  <div class="location-picker">
    <div v-if="location" class="location-info">
      <van-icon name="checked" color="#07c160" size="20" />
      <div class="location-text">
        <div class="address">{{ location.address }}</div>
        <div class="distance" v-if="location.distance">
          (距离目标 {{ location.distance }}m)
        </div>
      </div>
      <van-button size="mini" plain @click="relocate">重新定位</van-button>
    </div>
    <div v-else class="location-loading">
      <van-loading type="spinner" size="20" />
      <span>正在定位...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast, showLoadingToast, closeToast } from 'vant'
import { useGeolocation } from '@/composables/useGeolocation'

const { getLocation } = useGeolocation()

const location = ref<Location | null>(null)

onMounted(async () => {
  await locate()
})

const locate = async () => {
  showLoadingToast({
    message: '正在定位...',
    forbidClick: true
  })

  try {
    location.value = await getLocation()
    closeToast()
    showToast({ type: 'success', message: '定位成功' })
  } catch (error) {
    closeToast()
    showToast({ type: 'fail', message: '定位失败，请检查权限' })
  }
}

const relocate = () => {
  locate()
}
</script>
```

#### 照片上传组件
```vue
<template>
  <div class="photo-uploader">
    <van-uploader
      v-model="fileList"
      :max-count="maxCount"
      :max-size="maxSize * 1024 * 1024"
      :after-read="afterRead"
      :before-delete="beforeDelete"
      accept="image/*"
      multiple
    >
      <div class="upload-btn">
        <van-icon name="photograph" size="32" />
        <span>点击上传</span>
      </div>
    </van-uploader>
    <div class="upload-tip">
      最多{{ maxCount }}张，单张≤{{ maxSize }}MB
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UploaderFileListItem } from 'vant'

const props = defineProps<{
  maxCount?: number
  maxSize?: number // MB
}>()

const emit = defineEmits(['upload', 'delete'])

const fileList = ref<UploaderFileListItem[]>([])

const afterRead = (file: UploaderFileListItem | UploaderFileListItem[]) => {
  const files = Array.isArray(file) ? file : [file]
  files.forEach(f => {
    // 压缩图片
    compressImage(f.file as File).then(compressed => {
      f.file = compressed
      emit('upload', f)
    })
  })
}

const beforeDelete = (file: UploaderFileListItem) => {
  emit('delete', file)
  return true
}

const compressImage = async (file: File): Promise<File> => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (e) => {
      const img = new Image()
      img.src = e.target?.result as string
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const width = Math.min(1920, img.width)
        const height = (width / img.width) * img.height
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx?.drawImage(img, 0, 0, width, height)
        canvas.toBlob(
          (blob) => {
            resolve(new File([blob!], file.name, { type: 'image/jpeg' }))
          },
          'image/jpeg',
          0.8
        )
      }
    }
  })
}
</script>
```

---

## 四、司机端页面设计

### 4.1 任务列表页

#### 页面布局
```
┌─────────────────────────────────┐
│  [←] 配送任务         今日(8)    │
├─────────────────────────────────┤
│  快捷操作栏                      │
│  ┌─────┐ ┌─────┐ ┌─────┐       │
│  │待配送│ │配送中│ │已完成│       │
│  │  4  │ │  2  │ │  2  │       │
│  └─────┘ └─────┘ └─────┘       │
├─────────────────────────────────┤
│  任务卡片(待配送)                │
│  ┌─────────────────────────────┐│
│  │  TK005 · 配送任务            ││
│  │  ─────────────────────────   ││
│  │  客户: 李四  13900139000    ││
│  │  地址: 海淀区中关村...       ││
│  │  ─────────────────────────   ││
│  │  商品: 沙发×1               ││
│  │  金额: ¥520.00             ││
│  │  ─────────────────────────   ││
│  │  预约: 2026-03-15 14:00     ││
│  │                             ││
│  │  <span class="status">待配送</span>│
│  │              [导航] [开始]   ││
│  └─────────────────────────────┘│
└─────────────────────────────────┘
│  [任务] [地图] [历史] [我的]      │
└─────────────────────────────────┘
```

#### 导航功能组件
```vue
<template>
  <div class="navigation-bar">
    <van-button
      type="primary"
      size="large"
      icon="location-o"
      @click="handleNavigation"
    >
      一键导航
    </van-button>
    <div v-if="task" class="route-info">
      <div class="info-item">
        <van-icon name="clock-o" />
        <span>预计耗时: {{ estimatedTime }}</span>
      </div>
      <div class="info-item">
        <van-icon name="guide-o" />
        <span>行驶距离: {{ distance }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { showToast, showConfirmDialog } from 'vant'

const props = defineProps<{
  task: Task
  address: string
}>()

const estimatedTime = ref<string>('')
const distance = ref<string>('')

onMounted(async () => {
  await calculateRoute()
})

const calculateRoute = async () => {
  try {
    // 调用高德地图路径规划API
    const result = await routePlanning(props.address)
    estimatedTime.value = result.duration
    distance.value = result.distance
  } catch (error) {
    console.error('路径规划失败', error)
  }
}

const handleNavigation = () => {
  showConfirmDialog({
    title: '开始导航',
    message: `是否导航至 ${props.address}？`
  }).then(() => {
    // 调用高德地图App导航
    const url = `amapuri://route/plan/?dname=${encodeURIComponent(props.address)}`
    window.location.href = url
  }).catch(() => {
    // 用户取消
  })
}
</script>
```

### 4.2 签收确认页

#### 页面布局
```
┌─────────────────────────────────┐
│  [←] 签收确认                     │
├─────────────────────────────────┤
│  订单信息                        │
│  ┌─────────────────────────────┐│
│  │ 订单号: SO20260312000005   ││
│  │ 客户: 李四                  ││
│  │ 配送地址: 海淀区中关村...   ││
│  │ 预约时间: 2026-03-15 14:00 ││
│  └─────────────────────────────┘│
│                                 │
│  位置确认                        │
│  ┌─────────────────────────────┐│
│  │  ✓ 已到达客户位置            ││
│  │  海淀区中关村...             ││
│  │  (误差 10m)                 ││
│  └─────────────────────────────┘│
│                                 │
│  签收方式                        │
│  ┌─────────────────────────────┐│
│  │  ☑ 本人签收                  ││
│  │  ☐ 代签收                    ││
│  │  ☐ 无人签收                  ││
│  └─────────────────────────────┘│
│                                 │
│  签收照片                        │
│  ┌─────────────────────────────┐│
│  │  ┌─────┐ ┌─────┐           ││
│  │  │  +  │ │  +  │           ││
│  │  └─────┘ └─────┘           ││
│  │  (上传签收照片，最多2张)      ││
│  └─────────────────────────────┘│
│                                 │
│  签收备注                        │
│  ┌─────────────────────────────┐│
│  │  [_____________________]    ││
│  │  请输入签收备注              ││
│  └─────────────────────────────┘│
│                                 │
│           [确认签收]              │
└─────────────────────────────────┘
```

#### 签收组件
```vue
<template>
  <div class="sign-confirmation">
    <van-cell-group title="签收方式">
      <van-radio-group v-model="signType" direction="horizontal">
        <van-radio name="self">本人签收</van-radio>
        <van-radio name="proxy">代签收</van-radio>
        <van-radio name="nobody">无人签收</van-radio>
      </van-radio-group>
    </van-cell-group>

    <van-field
      v-if="signType === 'proxy'"
      v-model="proxyName"
      label="代签人姓名"
      placeholder="请输入代签人姓名"
    />

    <van-field
      v-if="signType === 'proxy'"
      v-model="proxyPhone"
      label="代签人电话"
      placeholder="请输入代签人电话"
    />

    <van-field
      v-if="signType === 'nobody'"
      v-model="nobodyReason"
      label="无人签收原因"
      type="textarea"
      placeholder="请说明原因"
      rows="3"
    />

    <van-cell-group title="签收照片">
      <van-uploader
        v-model="photos"
        :max-count="2"
        :after-read="handlePhotoUpload"
      />
    </van-cell-group>

    <van-cell-group title="签收备注">
      <van-field
        v-model="remark"
        type="textarea"
        placeholder="请输入签收备注（可选）"
        rows="3"
      />
    </van-cell-group>

    <div class="submit-btn">
      <van-button type="primary" size="large" @click="handleSubmit">
        确认签收
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast, showLoadingToast, closeToast } from 'vant'

const emit = defineEmits(['submit'])

const signType = ref<'self' | 'proxy' | 'nobody'>('self')
const proxyName = ref('')
const proxyPhone = ref('')
const nobodyReason = ref('')
const photos = ref([])
const remark = ref('')

const handlePhotoUpload = (file: any) => {
  // 压缩和上传逻辑
  console.log('上传照片', file)
}

const handleSubmit = async () => {
  // 验证
  if (signType.value === 'proxy' && !proxyName.value) {
    showToast('请输入代签人姓名')
    return
  }
  if (signType.value === 'proxy' && !proxyPhone.value) {
    showToast('请输入代签人电话')
    return
  }
  if (signType.value === 'nobody' && !nobodyReason.value) {
    showToast('请说明无人签收原因')
    return
  }
  if (photos.value.length === 0) {
    showToast('请上传签收照片')
    return
  }

  showLoadingToast({
    message: '提交中...',
    forbidClick: true
  })

  try {
    await emit('submit', {
      signType: signType.value,
      proxyName: proxyName.value,
      proxyPhone: proxyPhone.value,
      nobodyReason: nobodyReason.value,
      photos: photos.value,
      remark: remark.value
    })

    closeToast()
    showToast({ type: 'success', message: '签收成功' })
  } catch (error) {
    closeToast()
    showToast({ type: 'fail', message: '签收失败' })
  }
}
</script>
```

---

## 五、安装端页面设计

### 5.1 任务列表页

#### 页面布局
```
┌─────────────────────────────────┐
│  [←] 安装任务         今日(6)    │
├─────────────────────────────────┤
│  状态筛选                        │
│  [全部▼] [待安装 4] [进行中 1]  │
├─────────────────────────────────┤
│  任务卡片                        │
│  ┌─────────────────────────────┐│
│  │  TK008 · 安装任务            ││
│  │  ─────────────────────────   ││
│  │  客户: 王五  13700137000    ││
│  │  地址: 丰台区方庄...         ││
│  │  ─────────────────────────   ││
│  │  商品:                        ││
│  │  • 空调挂机 × 2              ││
│  │  • 智能门锁 × 1              ││
│  │  ─────────────────────────   ││
│  │  预约: 2026-03-15 15:00     ││
│  │  难度: ⭐⭐⭐                ││
│  │                             ││
│  │  <span class="status">待安装</span>│
│  │              [去安装]         ││
│  └─────────────────────────────┘│
└─────────────────────────────────┘
│  [任务] [教程] [历史] [我的]      │
└─────────────────────────────────┘
```

### 5.2 安装详情页

#### 页面布局（上下滚动）
```
┌─────────────────────────────────┐
│  [←] 安装详情                     │
├─────────────────────────────────┤
│  客户信息                        │
│  ┌─────────────────────────────┐│
│  │  姓名: 王五                 ││
│  │  电话: 13700137000           ││
│  │  地址: 丰台区方庄...         ││
│  │  [拨打电话] [发短信]         ││
│  └─────────────────────────────┘│
│                                 │
│  安装商品                        │
│  ┌─────────────────────────────┐│
│  │  空调挂机 × 2               ││
│  │  ─────────────────────────   ││
│  │  [查看安装教程]              ││
│  └─────────────────────────────┘│
│                                 │
│  安装步骤                        │
│  ┌─────────────────────────────┐│
│  │  1. 开箱检查                 ││
│  │     ☑ 完成                  ││
│  │                             ││
│  │  2. 挂机安装                 ││
│  │     ☐ 进行中                ││
│  │     [上传安装照片]           ││
│  │                             ││
│  │  3. 管道连接                 ││
│  │     ☐ 未开始                ││
│  │                             ││
│  │  4. 调试测试                 ││
│  │     ☐ 未开始                ││
│  │                             ││
│  │  5. 清理现场                 ││
│  │     ☐ 未开始                ││
│  └─────────────────────────────┘│
│                                 │
│  材料使用                        │
│  ┌─────────────────────────────┐│
│  │  [+ 添加材料]                 ││
│  │  ─────────────────────────   ││
│  │  • 铜管 2米                  ││
│  │  • 螺丝 10颗                 ││
│  └─────────────────────────────┘│
│                                 │
│  问题反馈                        │
│  ┌─────────────────────────────┐│
│  │  [反馈问题]                  ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │  验收拍照                    ││
│  │  ┌─────┐ ┌─────┐ ┌─────┐  ││
│  │  │  +  │ │  +  │ │  +  │  ││
│  │  └─────┘ └─────┘ └─────┘  ││
│  │  (上传验收照片，最多9张)      ││
│  └─────────────────────────────┘│
│                                 │
│  客户评价                        │
│  ┌─────────────────────────────┐│
│  │  服务态度: ⭐⭐⭐⭐⭐      ││
│  │  技术水平: ⭐⭐⭐⭐⭐      ││
│  │  完成速度: ⭐⭐⭐⭐       ││
│  │                             ││
│  │  评价意见:                   ││
│  │  [___________________]      ││
│  └─────────────────────────────┘│
│                                 │
│           [完成安装]              │
└─────────────────────────────────┘
```

#### 安装步骤组件
```vue
<template>
  <div class="install-steps">
    <van-steps direction="vertical" :active="activeStep">
      <van-step v-for="(step, index) in steps" :key="index">
        <div class="step-content">
          <div class="step-title">{{ step.title }}</div>
          <div class="step-status" :class="getStatusClass(index)">
            {{ getStatusText(index) }}
          </div>
          <van-button
            v-if="index === activeStep && step.needPhoto"
            size="small"
            type="primary"
            @click="handleUploadPhoto(index)"
          >
            上传照片
          </van-button>
          <div v-if="step.photos && step.photos.length > 0" class="step-photos">
            <van-image
              v-for="(photo, pIndex) in step.photos"
              :key="pIndex"
              :src="photo"
              width="60"
              height="60"
              fit="cover"
              @click="previewPhoto(photo)"
            />
          </div>
        </div>
      </van-step>
    </van-steps>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { showImagePreview } from 'vant'

const steps = ref([
  {
    title: '开箱检查',
    completed: true,
    photos: ['https://example.com/photo1.jpg']
  },
  {
    title: '挂机安装',
    completed: false,
    needPhoto: true,
    photos: []
  },
  {
    title: '管道连接',
    completed: false,
    needPhoto: true,
    photos: []
  },
  {
    title: '调试测试',
    completed: false,
    photos: []
  },
  {
    title: '清理现场',
    completed: false,
    photos: []
  }
])

const activeStep = computed(() => {
  return steps.value.findIndex(s => !s.completed)
})

const getStatusClass = (index: number) => {
  const step = steps.value[index]
  if (step.completed) return 'completed'
  if (index === activeStep.value) return 'active'
  return 'pending'
}

const getStatusText = (index: number) => {
  const step = steps.value[index]
  if (step.completed) return '已完成'
  if (index === activeStep.value) return '进行中'
  return '未开始'
}

const handleUploadPhoto = (index: number) => {
  console.log('上传照片', index)
}

const previewPhoto = (url: string) => {
  showImagePreview({ images: [url], showIndex: false })
}
</script>
```

#### 材料使用组件
```vue
<template>
  <div class="material-usage">
    <van-cell-group title="材料使用">
      <van-cell
        v-for="(material, index) in materials"
        :key="index"
        :title="material.name"
        :value="`${material.quantity} ${material.unit}`"
      >
        <template #icon>
          <van-icon name="bag-o" />
        </template>
        <template #right-icon>
          <van-button
            size="mini"
            type="danger"
            plain
            @click="handleRemove(index)"
          >
            删除
          </van-button>
        </template>
      </van-cell>

      <van-cell>
        <template #title>
          <van-button type="primary" size="small" block @click="showAddDialog">
            + 添加材料
          </van-button>
        </template>
      </van-cell>
    </van-cell-group>

    <!-- 添加材料弹窗 -->
    <van-popup v-model:show="showDialog" position="bottom" round>
      <van-form @submit="handleAddMaterial">
        <van-cell-group inset>
          <van-field
            v-model="form.name"
            name="name"
            label="材料名称"
            placeholder="请输入材料名称"
            required
          />
          <van-field
            v-model.number="form.quantity"
            name="quantity"
            label="数量"
            type="number"
            placeholder="请输入数量"
            required
          />
          <van-field
            v-model="form.unit"
            name="unit"
            label="单位"
            placeholder="请输入单位"
            required
          />
        </van-cell-group>
        <div style="padding: 16px">
          <van-button round block type="primary" native-type="submit">
            确定
          </van-button>
        </div>
      </van-form>
    </van-popup>
  </div>
</template>
```

### 5.3 验收拍照页

#### 多图上传组件
```vue
<template>
  <div class="photo-gallery">
    <van-uploader
      v-model="fileList"
      :max-count="9"
      :max-size="2 * 1024 * 1024"
      :after-read="afterRead"
      accept="image/*"
      multiple
    >
      <div class="upload-slot">
        <van-icon name="photograph" size="32" />
        <span>添加照片</span>
      </div>
    </van-uploader>

    <div class="photo-tips">
      <van-notice-bar
        left-icon="info-o"
        text="请拍摄清晰照片，包括产品外观、安装效果、现场环境"
      />
    </div>

    <!-- 照片预览 -->
    <van-image-preview
      v-model:show="showPreview"
      :images="previewImages"
      :start-position="previewIndex"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { UploaderFileListItem } from 'vant'
import { showToast } from 'vant'

const fileList = ref<UploaderFileListItem[]>([])
const showPreview = ref(false)
const previewIndex = ref(0)

const previewImages = computed(() => {
  return fileList.value
    .filter(f => f.url)
    .map(f => f.url as string)
})

const afterRead = (file: UploaderFileListItem | UploaderFileListItem[]) => {
  const files = Array.isArray(file) ? file : [file]

  files.forEach(f => {
    // 检查大小
    if ((f.file as File).size > 2 * 1024 * 1024) {
      showToast('图片大小不能超过2MB')
      return
    }

    // 压缩图片
    compressImage(f.file as File).then(compressed => {
      f.file = compressed
      showToast('图片上传成功')
    }).catch(() => {
      showToast('图片处理失败')
    })
  })
}

const compressImage = async (file: File): Promise<File> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (e) => {
      const img = new Image()
      img.src = e.target?.result as string
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const width = Math.min(1920, img.width)
        const height = (width / img.width) * img.height
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx?.drawImage(img, 0, 0, width, height)
        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(new File([blob], file.name, { type: 'image/jpeg' }))
            } else {
              reject(new Error('压缩失败'))
            }
          },
          'image/jpeg',
          0.8
        )
      }
      img.onerror = reject
    }
    reader.onerror = reject
  })
}
</script>
```

---

## 六、通用组件设计

### 6.1 任务状态标签
```vue
<template>
  <van-tag :type="tagType" size="medium">{{ tagText }}</van-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TaskStatus } from '@/types/task'

const props = defineProps<{
  status: TaskStatus
}>()

const tagType = computed(() => {
  const typeMap = {
    [TaskStatus.PENDING]: 'warning',
    [TaskStatus.IN_PROGRESS]: 'primary',
    [TaskStatus.COMPLETED]: 'success',
    [TaskStatus.CANCELLED]: 'danger'
  }
  return typeMap[props.status]
})

const tagText = computed(() => {
  const textMap = {
    [TaskStatus.PENDING]: '待处理',
    [TaskStatus.IN_PROGRESS]: '进行中',
    [TaskStatus.COMPLETED]: '已完成',
    [TaskStatus.CANCELLED]: '已取消'
  }
  return textMap[props.status]
})
</script>
```

### 6.2 底部操作栏
```vue
<template>
  <div class="bottom-action-bar" :class="{ safe: safeAreaInsetBottom }">
    <van-button
      v-for="btn in buttons"
      :key="btn.text"
      :type="btn.type"
      :plain="btn.plain"
      :loading="btn.loading"
      :disabled="btn.disabled"
      @click="btn.onClick"
    >
      {{ btn.text }}
    </van-button>
  </div>
</template>

<script setup lang="ts">
interface ActionButton {
  text: string
  type?: 'primary' | 'success' | 'warning' | 'danger'
  plain?: boolean
  loading?: boolean
  disabled?: boolean
  onClick: () => void
}

const props = defineProps<{
  buttons: ActionButton[]
  safeAreaInsetBottom?: boolean
}>()
</script>
```

---

## 七、性能优化

### 7.1 图片懒加载
```vue
<van-image
  v-lazy="imageUrl"
  width="100%"
  height="200px"
  fit="cover"
/>
```

### 7.2 列表虚拟滚动
```vue
<van-list
  v-model:loading="loading"
  :finished="finished"
  finished-text="没有更多了"
  @load="onLoad"
>
  <van-cell v-for="item in list" :key="item.id">
    {{ item }}
  </van-cell>
</van-list>
```

### 7.3 离线缓存
```typescript
// 使用IndexedDB缓存核心数据
import { setup } from 'axios-cache-adapter'

const { adapter } = setup({
  baseURL: '/api',
  cache: {
    maxAge: 15 * 60 * 1000, // 15分钟
    store: new IDBStore('api-cache')
  }
})
```

---

## 八、设计规范

### 8.1 颜色规范
```scss
// 主色调
$primary-color: #1989fa;    // Vant Blue
$success-color: #07c160;    // Green
$warning-color: #ff976a;    // Orange
$danger-color: #ee0a24;     // Red

// 背景色
$bg-color: #f7f8fa;
$bg-white: #ffffff;

// 文字色
$text-main: #323233;
$text-secondary: #969799;
$text-disabled: #c8c9cc;
```

### 8.2 间距规范
```scss
// 移动端适配
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 12px;
$spacing-lg: 16px;
$spacing-xl: 20px;
```

### 8.3 字体规范
```scss
// 基础字体
$font-size-xs: 10px;
$font-size-sm: 12px;
$font-size-md: 14px;
$font-size-lg: 16px;
$font-size-xl: 18px;
$font-size-xxl: 20px;
```

---

## 附录

### 附录A：Vant组件清单
- Navigation: van-nav-bar
- Button: van-button
- Icon: van-icon
- Cell: van-cell, van-cell-group
- Form: van-form, van-field
- Upload: van-uploader
- Steps: van-steps, van-step
- Tag: van-tag
- List: van-list
- Image: van-image
- Dialog: van-dialog, van-popup
- Toast: van-toast

### 附录B：第三方集成
- 高德地图: https://lbs.amap.com/api/jsapi-v2/summary
- 图片压缩: Canvas API
- 离线存储: IndexedDB
