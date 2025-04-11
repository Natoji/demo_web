<template>
  <div class="order-list-page">
    <h1>Chi tiết Đơn hàng</h1>

    <div v-if="loading">
      Đang tải dữ liệu đơn hàng...
    </div>

    <div v-else-if="error">
      Lỗi khi tải dữ liệu đơn hàng: {{ error }}
    </div>

    <div v-else-if="order">
      <div class="order-detail">
        <p><strong>Mã đơn hàng:</strong> {{ order.id }}</p>
        <p><strong>Trạng thái:</strong> {{ order.status }}</p>
        <p><strong>Tổng tiền:</strong> {{ order.total_amount }} VND</p>
        <p><strong>Ngày tạo:</strong> {{ order.created_at }}</p>
        <p><strong>ID Người dùng:</strong> {{ order.user }}</p>
      </div>
    </div>

    <div v-else>
      Không có đơn hàng nào.
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'OrderListPage',
  setup() {
    const loading = ref(false)
    const error = ref(null)
    const order = ref(null)

    const API_BASE_URL = 'http://localhost:8000/api'

    onMounted(async () => {
      const userId = localStorage.getItem('userId')
      if (userId) {
        await fetchOrder(userId)
      } else {
        error.value = 'Không tìm thấy ID người dùng.'
      }
    })

    const fetchOrder = async (userId) => {
      loading.value = true
      error.value = null
      order.value = null
      try {
        const response = await axios.get(`${API_BASE_URL}/orders/${userId}`)
        order.value = response.data
      } catch (err) {
        error.value = err.message || 'Có lỗi xảy ra khi tải dữ liệu.'
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      error,
      order,
    }
  },
}
</script>

<style scoped>
.order-list-page {
  padding: 20px;
}

.order-detail {
  background-color: #f4f4f4;
  padding: 15px;
  border-radius: 5px;
}
</style>
