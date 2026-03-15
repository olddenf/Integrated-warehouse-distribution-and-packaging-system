<template>
  <div class="guide">
    <van-nav-bar title="安装指南" />
    <van-scroll-view class="scroll-view" scroll-y>
      <div class="guide-content">
        <van-cell title="安装前准备">
          <template #default>
            <ul class="guide-list">
              <li>1. 确认安装地址和时间</li>
              <li>2. 检查安装工具是否齐全</li>
              <li>3. 确认产品是否完好</li>
              <li>4. 与客户沟通安装细节</li>
            </ul>
          </template>
        </van-cell>
        
        <van-cell title="安装步骤">
          <template #default>
            <ul class="guide-list">
              <li>1. 开箱验货</li>
              <li>2. 组装产品</li>
              <li>3. 安装固定</li>
              <li>4. 测试功能</li>
              <li>5. 客户验收</li>
            </ul>
          </template>
        </van-cell>
        
        <van-cell title="注意事项">
          <template #default>
            <ul class="guide-list">
              <li>• 遵守安全操作规范</li>
              <li>• 保持现场清洁</li>
              <li>• 注意保护产品表面</li>
              <li>• 操作时轻拿轻放</li>
              <li>• 安装完成后清理现场</li>
            </ul>
          </template>
        </van-cell>
        
        <van-cell title="常见问题">
          <template #default>
            <ul class="guide-list">
              <li>Q: 安装工具不足怎么办？</li>
              <li>A: 联系调度员协调工具</li>
              <li>Q: 产品有损坏怎么办？</li>
              <li>A: 拍照记录并联系客服</li>
              <li>Q: 客户不在现场怎么办？</li>
              <li>A: 联系调度员确认后续安排</li>
            </ul>
          </template>
        </van-cell>
      </div>
    </van-scroll-view>
  </div>
</template>

<script setup lang="ts">
// 安装指南页面
</script>

<style scoped>
.guide {
  height: 100vh;
  background-color: #f5f7fa;
}

.scroll-view {
  height: calc(100vh - 46px);
}

.guide-content {
  padding: 16px;
}

.guide-list {
  margin: 0;
  padding-left: 20px;
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.guide-list li {
  margin-bottom: 8px;
}
</style>