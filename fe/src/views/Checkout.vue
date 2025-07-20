<template>
  <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden mt-6">
    <div class="bg-rose-600 text-white py-4 px-6">
      <h2 class="text-xl font-bold">Thanh toán</h2>
    </div>

    <div class="p-6">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Đang tải thông tin...</p>
      </div>

      <div v-else-if="error" class="text-center py-12 bg-white rounded-lg shadow-md">
        <p class="text-red-600 mb-4">{{ error }}</p>
        <button @click="loadData" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700">
          Thử lại
        </button>
        <router-link to="/cart" class="ml-4 text-rose-600 hover:text-rose-800">
          Quay lại giỏ hàng
        </router-link>
      </div>

      <div v-else class="mb-8">
        <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Tóm tắt đơn hàng</h3>

        <div v-if="cartItems.length > 0">
          <div v-for="item in cartItems" :key="item.id" class="flex items-center py-3 border-b">
            <img :src="item.image" :alt="item.name" class="w-16 h-16 object-cover rounded-md mr-4">

            <div class="flex-grow">
              <h4 class="font-medium">{{ item.name }}</h4>
              <p class="text-gray-500 text-sm">Số lượng: {{ item.quantity }}</p>
            </div>

            <div class="text-right">
              <p class="font-medium">${{ (item.price * item.quantity).toFixed(2) }}</p>
            </div>
          </div>

          <div class="mt-4 space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Tổng tiền hàng</span>
              <span>${{ subtotal.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between">
              <span class="text-gray-600">Phí giao hàng</span>
              <span>${{ deliveryFee.toFixed(2) }}</span>
            </div>

            <div class="flex justify-between font-bold text-lg pt-2 border-t">
              <span>Tổng cộng</span>
              <span>${{ total.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <ShoppingCart class="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 class="text-xl font-semibold text-gray-700 mb-2">Giỏ hàng của bạn đang trống</h3>
          <p class="text-gray-500 mb-4">Thêm sản phẩm vào giỏ hàng để tiến hành thanh toán.</p>
          <router-link to="/" class="inline-block bg-rose-600 text-white py-2 px-4 rounded-lg hover:bg-rose-700">
            Xem menu
          </router-link>
        </div>
      </div>

      <div v-if="cartItems.length > 0">
        <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Thông tin giao hàng</h3>

        <form @submit.prevent="placeOrder">
          <div class="grid grid-cols-1 gap-6 mb-6">
            <div>
              <label for="fullName" class="block text-gray-700 font-medium mb-2">Họ và tên</label>
              <input type="text" id="fullName" v-model="form.fullName"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
              <input type="email" id="email" v-model="form.email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="phone" class="block text-gray-700 font-medium mb-2">Số điện thoại</label>
              <input type="tel" id="phone" v-model="form.phone"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="address" class="block text-gray-700 font-medium mb-2">Địa chỉ giao hàng</label>
              <input type="text" id="address" v-model="form.address"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>
          </div>

          <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Phương thức thanh toán</h3>

          <div class="space-y-4 mb-6">
            <!-- <div class="flex items-center">
              <input type="radio" id="vnpay" value="vnpay" v-model="form.paymentMethod"
                class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300"
                :checked="form.paymentMethod === 'vnpay'">
              <label for="vnpay" class="ml-2 block text-gray-700">
                VNPay
              </label>
            </div> -->

            <div class="flex items-center">
              <input type="radio" id="cashOnDelivery" value="cashOnDelivery" v-model="form.paymentMethod"
                class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300"
                :checked="form.paymentMethod === 'cod'">
              <label for="cashOnDelivery" class="ml-2 block text-gray-700">
                Thanh toán khi nhận hàng
              </label>
            </div>
          </div>

          <div class="flex items-center mb-6">
            <input type="checkbox" id="terms" v-model="form.termsAccepted"
              class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300 rounded" required>
            <label for="terms" class="ml-2 block text-gray-700">
              Tôi đồng ý với <a href="#" class="text-rose-600 hover:text-rose-800">Điều khoản và điều kiện</a>
            </label>
          </div>

          <div class="flex justify-between">
            <router-link to="/cart" class="flex items-center text-gray-600 hover:text-gray-800">
              <ArrowLeft class="h-5 w-5 mr-1" />
              Quay lại giỏ hàng
            </router-link>

            <button type="submit"
              class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2"
              :disabled="loading || !form.termsAccepted">
              <span v-if="loading">Đang xử lý...</span>
              <span v-else>Đặt hàng</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6 text-center">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Check class="h-8 w-8 text-green-600" />
        </div>

        <h2 class="text-2xl font-bold text-gray-800 mb-2">Đặt hàng thành công!</h2>
        <p class="text-gray-600 mb-6">Đơn hàng của bạn đã được đặt thành công. Chúng tôi sẽ gửi email xác nhận cho bạn trong thời gian ngắn.</p>

        <div class="bg-gray-50 rounded-lg p-4 mb-6">
          <p class="text-gray-700 font-medium">Mã đơn hàng</p>
          <p class="text-xl font-bold text-rose-600">{{ orderNumber }}</p>
        </div>

        <button @click="goToOrders" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700 w-full">
          Xem đơn hàng của tôi
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ShoppingCart, ArrowLeft, Check } from 'lucide-vue-next';
import axios from 'axios';

export default {
  name: 'Checkout',
  components: {
    ShoppingCart,
    ArrowLeft,
    Check
  },
  setup() {
    const router = useRouter();
    const cartItems = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const showSuccessModal = ref(false);
    const orderNumber = ref('');
    const user = ref(null);

    const form = ref({
      fullName: '',
      email: '',
      phone: '',
      address: '',
      paymentMethod: 'cod', // Giá trị mặc định
      termsAccepted: false
    });

    const getToken = () => localStorage.getItem('access_token');
    const getUserId = () => localStorage.getItem('userId');

    const loadData = async () => {
      try {
        loading.value = true;
        error.value = null;

        const token = getToken();
        const userId = getUserId();

        if (!token || !userId) {
          router.push('/login');
          return;
        }

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const userResponse = await axios.get(`https://demo-web-m8jr.onrender.com/api/users/${userId}`, { headers });
        user.value = userResponse.data;

        const cartResponse = await axios.get(`https://demo-web-m8jr.onrender.com/api/cart/`, { headers });
        console.log('Dữ liệu giỏ hàng:', cartResponse.data);

        // Kiểm tra và truy cập đúng mảng dữ liệu giỏ hàng
        if (!cartResponse.data || !cartResponse.data.items || !Array.isArray(cartResponse.data.items) || cartResponse.data.items.length === 0) {
          error.value = 'Giỏ hàng trống!';
          return;
        }

        cartItems.value = cartResponse.data.items.map(item => ({
          id: item.product, // Sử dụng item.product làm id
          name: item.product_name, // Sử dụng item.product_name
          price: parseFloat(item.product_price), // Sử dụng item.product_price và chuyển đổi sang số
          quantity: item.quantity,
          image: item.product_img, // Sử dụng item.product_img
        }));

        if (user.value) {
          form.value.email = user.value.email;
          form.value.fullName = user.value.fullname || '';
          form.value.phone = user.value.phone_number || '';
          form.value.address = user.value.address || '';
        }
      } catch (error) {
        console.error('Lỗi tải dữ liệu:', error);
        error.value = 'Có lỗi xảy ra khi tải thông tin. Vui lòng thử lại sau.';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadData();
    });

    const subtotal = computed(() => {
      return cartItems.value.reduce((total, item) => total + item.price * item.quantity, 0);
    });

    const deliveryFee = computed(() => {
      return 0; // Phí giao hàng là 0
    });

    const total = computed(() => {
      return subtotal.value + deliveryFee.value;
    });

    const placeOrder = async () => {
      const token = getToken();
      const userId = getUserId();

      if (!token || !userId) {
        alert('Vui lòng đăng nhập để tiếp tục');
        router.push('/login');
        return;
      }

      if (!form.value.termsAccepted) {
        alert('Vui lòng chấp nhận điều khoản và điều kiện');
        return;
      }

      loading.value = true;

      try {
        const headers = {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        };

        // 1. Tạo Order
        const orderData = {
          user: userId,
          total_amount: total.value,
          status: 'pending',
        };
        const orderResponse = await axios.post('https://demo-web-m8jr.onrender.com/api/orders/', orderData, { headers });
        const orderId = orderResponse.data.id;
        console.log('Đã tạo đơn hàng:', orderResponse.data);

        if (orderId) {
          // 2. Tạo Order Items
          for (const item of cartItems.value) {
            const orderItemData = {
              order: orderId,
              product: item.id,
              quantity: item.quantity,
              price: item.price,
            };
            await axios.post('https://demo-web-m8jr.onrender.com/api/order-items/', orderItemData, { headers });
            console.log('Đã tạo mục đơn hàng:', orderItemData);
          }

          // 3. Tạo Payment
          const paymentData = {
            order: orderId,
            method: form.value.paymentMethod,
            amount: total.value,
            is_paid: form.value.paymentMethod === 'cashOnDelivery' ? false : true, // Mặc định là chưa thanh toán nếu COD
          };
          const paymentResponse = await axios.post('https://demo-web-m8jr.onrender.com/api/payments/', paymentData, { headers });
          console.log('Đã tạo thanh toán:', paymentResponse.data);

          // 4. Xóa giỏ hàng
          // await axios.post('https://demo-web-m8jr.onrender.com/api/cart/clear/', { headers });
          // console.log('Đã xóa giỏ hàng');
          await axios.post('https://demo-web-m8jr.onrender.com/api/cart/clear/', {}, {
            headers: {
              Authorization: `Bearer ${token}`, // hoặc headers bạn muốn
            }
          });
          console.log('Đã xóa giỏ hàng');

          window.dispatchEvent(new CustomEvent('cartUpdated'));
          orderNumber.value = orderId;
          showSuccessModal.value = true;
        } else {
          alert('Không thể tạo đơn hàng.');
        }
      } catch (error) {
        console.error('Lỗi đặt hàng:', error);
        alert('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại sau.');
      } finally {
        loading.value = false;
      }
    };

    const goToOrders = () => {
      showSuccessModal.value = false;
      router.push('/orders');
    };

    return {
      cartItems,
      form,
      loading,
      error,
      subtotal,
      deliveryFee,
      total,
      showSuccessModal,
      orderNumber,
      placeOrder,
      goToOrders,
    };
  },
};
</script>