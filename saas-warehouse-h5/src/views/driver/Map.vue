<template>
  <div class="map">
    <van-nav-bar title="路线导航" />
    <div class="map-container">
      <!-- 这里可以集成地图API，如高德地图、百度地图等 -->
      <div class="map-placeholder">
        <van-icon name="location" size="64" color="#409eff" />
        <p class="map-placeholder-text">地图加载中...</p>
        <p class="map-placeholder-subtext">请确保您的设备已开启定位服务</p>
      </div>
      
      <div class="route-info">
        <div class="route-item">
          <van-icon name="location-o" size="20" color="#409eff" />
          <div class="route-details">
            <div class="route-label">起点</div>
            <div class="route-address">{{ route.startAddress }}</div>
          </div>
        </div>
        
        <div class="route-line">
          <div class="line"></div>
        </div>
        
        <div class="route-item">
          <van-icon name="location" size="20" color="#67c23a" />
          <div class="route-details">
            <div class="route-label">终点</div>
            <div class="route-address">{{ route.endAddress }}</div>
          </div>
        </div>
      </div>
      
      <div class="route-stats">
        <div class="stat-item">
          <div class="stat-value">{{ route.distance }}</div>
          <div class="stat-label">距离</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ route.duration }}</div>
          <div class="stat-label">预计时间</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ route.estimatedArrival }}</div>
          <div class="stat-label">预计到达</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const route = ref({
  startAddress: '北京仓库',
  endAddress: '北京市朝阳区建国路88号',
  distance: '12.5公里',
  duration: '30分钟',
  estimatedArrival: '15:30'
});
</script>

<style scoped>
.map {
  height: 100vh;
  background-color: #f5f7fa;
}

.map-container {
  height: calc(100vh - 46px);
  position: relative;
}

.map-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #999;
}

.map-placeholder-text {
  font-size: 16px;
  margin-top: 16px;
  margin-bottom: 8px;
}

.map-placeholder-subtext {
  font-size: 14px;
  color: #ccc;
}

.route-info {
  position: absolute;
  bottom: 120px;
  left: 16px;
  right: 16px;
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.route-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
}

.route-details {
  margin-left: 12px;
  flex: 1;
}

.route-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.route-address {
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}

.route-line {
  position: relative;
  height: 24px;
  margin-left: 10px;
  margin-bottom: 12px;
}

.line {
  position: absolute;
  top: 0;
  left: 0;
  width: 2px;
  height: 100%;
  background-color: #e4e7ed;
}

.route-stats {
  position: absolute;
  bottom: 16px;
  left: 16px;
  right: 16px;
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #999;
}
</style>