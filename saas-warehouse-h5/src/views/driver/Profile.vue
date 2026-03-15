<template>
  <div class="profile">
    <van-nav-bar title="个人中心" />
    <van-scroll-view class="scroll-view" scroll-y>
      <div class="profile-content">
        <div class="user-info">
          <van-avatar :size="80" :src="user.avatar">{{ user.name.charAt(0) }}</van-avatar>
          <div class="user-details">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-role">司机</div>
          </div>
        </div>
        
        <van-cell-group>
          <van-cell title="个人信息" is-link @click="editProfile">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
          <van-cell title="工作统计" is-link @click="viewStats">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
          <van-cell title="我的评价" is-link @click="viewRatings">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
          <van-cell title="车辆信息" is-link @click="viewVehicle">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
          <van-cell title="设置" is-link @click="viewSettings">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
          <van-cell title="关于我们" is-link @click="viewAbout">
            <template #right-icon>
              <van-icon name="arrow" />
            </template>
          </van-cell>
        </van-cell-group>
        
        <van-button type="danger" class="logout-button" @click="logout">退出登录</van-button>
      </div>
    </van-scroll-view>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const user = ref({
  name: '司机李四',
  avatar: ''
});

const editProfile = () => {
  console.log('编辑个人信息');
};

const viewStats = () => {
  console.log('查看工作统计');
};

const viewRatings = () => {
  console.log('查看评价');
};

const viewVehicle = () => {
  console.log('查看车辆信息');
};

const viewSettings = () => {
  console.log('查看设置');
};

const viewAbout = () => {
  console.log('查看关于我们');
};

const logout = () => {
  // 退出登录逻辑
  router.push('/login');
};
</script>

<style scoped>
.profile {
  height: 100vh;
  background-color: #f5f7fa;
}

.scroll-view {
  height: calc(100vh - 46px);
}

.profile-content {
  padding: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.user-details {
  margin-left: 16px;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.user-role {
  font-size: 14px;
  color: #999;
}

.logout-button {
  margin-top: 32px;
  width: 100%;
}
</style>