<template>
  <div class="sign">
    <van-nav-bar title="签收确认" />
    <van-scroll-view class="scroll-view" scroll-y>
      <div class="sign-content">
        <van-card>
          <template #header>
            <div class="card-header">
              <h3 class="order-no">订单号: {{ order.orderNo }}</h3>
            </div>
          </template>
          
          <van-cell title="客户信息">
            <template #default>
              <div class="customer-info">
                <div>{{ order.customer }}</div>
                <div>{{ order.phone }}</div>
              </div>
            </template>
          </van-cell>
          
          <van-cell title="配送地址">
            <template #default>
              <div>{{ order.address }}</div>
            </template>
          </van-cell>
          
          <van-cell title="货物信息">
            <template #default>
              <div class="goods-info">
                <div v-for="item in order.goods" :key="item.id" class="goods-item">
                  <div class="goods-name">{{ item.name }}</div>
                  <div class="goods-quantity">数量: {{ item.quantity }} {{ item.unit }}</div>
                </div>
              </div>
            </template>
          </van-cell>
          
          <van-cell title="签收方式">
            <template #default>
              <div class="sign-methods">
                <van-radio-group v-model="signMethod">
                  <van-radio name="signature">电子签名</van-radio>
                  <van-radio name="photo">拍照确认</van-radio>
                  <van-radio name="code">验证码</van-radio>
                </van-radio-group>
              </div>
            </template>
          </van-cell>
          
          <div v-if="signMethod === 'signature'" class="signature-area">
            <h4 class="section-title">请在下方签名</h4>
            <div class="signature-pad">
              <!-- 这里可以集成签名库，如 signature_pad -->
              <div class="signature-placeholder">
                <van-icon name="edit" size="48" color="#999" />
                <p>点击此处开始签名</p>
              </div>
            </div>
            <van-button type="default" class="clear-button" @click="clearSignature">清除签名</van-button>
          </div>
          
          <div v-if="signMethod === 'photo'" class="photo-area">
            <h4 class="section-title">请拍摄货物照片</h4>
            <van-uploader :after-read="afterRead" :max-count="3">
              <van-button type="primary" icon="photograph">上传照片</van-button>
            </van-uploader>
          </div>
          
          <div v-if="signMethod === 'code'" class="code-area">
            <h4 class="section-title">请输入验证码</h4>
            <van-field
              v-model="verificationCode"
              placeholder="请输入客户提供的验证码"
              maxlength="6"
              type="number"
            />
          </div>
        </van-card>
        
        <van-button type="primary" class="submit-button" @click="submitSign">提交签收</van-button>
      </div>
    </van-scroll-view>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const order = ref({
  orderNo: 'ORD-2024-001',
  customer: '张三',
  phone: '13800138001',
  address: '北京市朝阳区建国路88号',
  goods: [
    { id: '1', name: '商品A', quantity: 10, unit: '件' },
    { id: '2', name: '商品B', quantity: 5, unit: '箱' }
  ]
});

const signMethod = ref('signature');
const verificationCode = ref('');

const afterRead = (file: any) => {
  console.log('上传的文件:', file);
};

const clearSignature = () => {
  console.log('清除签名');
};

const submitSign = () => {
  console.log('提交签收');
  // 这里可以调用API提交签收信息
  router.push('/driver/tasks');
};
</script>

<style scoped>
.sign {
  height: 100vh;
  background-color: #f5f7fa;
}

.scroll-view {
  height: calc(100vh - 46px);
}

.sign-content {
  padding: 16px;
}

.card-header {
  margin-bottom: 16px;
}

.order-no {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.customer-info {
  line-height: 1.5;
}

.goods-info {
  line-height: 1.5;
}

.goods-item {
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.goods-name {
  font-weight: 500;
  color: #333;
}

.goods-quantity {
  font-size: 14px;
  color: #666;
}

.sign-methods {
  margin-top: 8px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 16px 0 12px 0;
}

.signature-pad {
  width: 100%;
  height: 200px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background-color: #f9f9f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signature-placeholder {
  text-align: center;
  color: #999;
}

.signature-placeholder p {
  margin-top: 8px;
  font-size: 14px;
}

.clear-button {
  margin-top: 12px;
  width: 100%;
}

.photo-area {
  margin-top: 16px;
}

.code-area {
  margin-top: 16px;
}

.submit-button {
  margin-top: 24px;
  width: 100%;
}
</style>