<template>
  <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden mt-6">
    <div class="bg-rose-600 text-white py-4 px-6">
      <h2 class="text-xl font-bold">Checkout</h2>
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
        <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Order Summary</h3>

        <div v-if="cartItems.length > 0">
          <div v-for="item in cartItems" :key="item.id" class="flex items-center py-3 border-b">
            <img :src="item.image" :alt="item.name" class="w-16 h-16 object-cover rounded-md mr-4">

            <div class="flex-grow">
              <h4 class="font-medium">{{ item.name }}</h4>
              <p class="text-gray-500 text-sm">Quantity: {{ item.quantity }}</p>
            </div>

            <div class="text-right">
              <p class="font-medium">{{ (item.price * item.quantity).toFixed(2) }} VNĐ</p>
            </div>
          </div>

          <div class="mt-4 space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span>{{ subtotal.toFixed(2) }} VNĐ</span>
            </div>

            <div class="flex justify-between">
              <span class="text-gray-600">Delivery Fee</span>
              <span>{{ deliveryFee.toFixed(2) }} VNĐ</span>
            </div>

            <div class="flex justify-between font-bold text-lg pt-2 border-t">
              <span>Total</span>
              <span>{{ total.toFixed(2) }} VNĐ</span>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <ShoppingCart class="h-16 w-16 mx-auto text-gray-400 mb-4" />
          <h3 class="text-xl font-semibold text-gray-700 mb-2">Your cart is empty</h3>
          <p class="text-gray-500 mb-4">Add some items to your cart to proceed with checkout.</p>
          <router-link to="/" class="inline-block bg-rose-600 text-white py-2 px-4 rounded-lg hover:bg-rose-700">
            Browse Menu
          </router-link>
        </div>
      </div>

      <div v-if="cartItems.length > 0">
        <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Delivery Information</h3>

        <form @submit.prevent="placeOrder">
          <div class="grid grid-cols-1 gap-6 mb-6">
            <div>
              <label for="fullName" class="block text-gray-700 font-medium mb-2">Full Name</label>
              <input type="text" id="fullName" v-model="form.fullName"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
              <input type="email" id="email" v-model="form.email"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="phone" class="block text-gray-700 font-medium mb-2">Phone Number</label>
              <input type="tel" id="phone" v-model="form.phone"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>

            <div>
              <label for="address" class="block text-gray-700 font-medium mb-2">Address</label>
              <input type="text" id="address" v-model="form.address"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500" required>
            </div>
          </div>

          <h3 class="text-lg font-semibold mb-4 pb-2 border-b">Payment Method</h3>

          <div class="space-y-4 mb-6">
            <div class="flex items-center">
              <input type="radio" id="vnpay" value="vnpay" v-model="form.paymentMethod"
                class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300"
                :checked="form.paymentMethod === 'vnpay'">
              <label for="vnpay" class="ml-2 block text-gray-700">
                VNPay
              </label>
            </div>

            <div class="flex items-center">
              <input type="radio" id="cashOnDelivery" value="cashOnDelivery" v-model="form.paymentMethod"
                class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300"
                :checked="form.paymentMethod === 'cashOnDelivery'">
              <label for="cashOnDelivery" class="ml-2 block text-gray-700">
                Cash on Delivery
              </label>
            </div>
          </div>

          <div class="flex items-center mb-6">
            <input type="checkbox" id="terms" v-model="form.termsAccepted"
              class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300 rounded" required>
            <label for="terms" class="ml-2 block text-gray-700">
              I agree to the <a href="#" class="text-rose-600 hover:text-rose-800">Terms and Conditions</a>
            </label>
          </div>

          <div class="flex justify-between">
            <router-link to="/cart" class="flex items-center text-gray-600 hover:text-gray-800">
              <ArrowLeft class="h-5 w-5 mr-1" />
              Back to Cart
            </router-link>

            <button type="submit"
              class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2"
              :disabled="loading || !form.termsAccepted">
              <span v-if="loading">Processing...</span>
              <span v-else>Place Order</span>
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

        <h2 class="text-2xl font-bold text-gray-800 mb-2">Order Placed Successfully!</h2>
        <p class="text-gray-600 mb-6">Your order has been placed successfully. You will receive a confirmation email
          shortly.</p>

        <div class="bg-gray-50 rounded-lg p-4 mb-6">
          <p class="text-gray-700 font-medium">Order Number</p>
          <p class="text-xl font-bold text-rose-600">{{ orderNumber }}</p>
        </div>

        <button @click="goToOrders" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700 w-full">
          View my orders
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ShoppingCart, ArrowLeft, Check } from 'lucide-vue-next';
import { userAPI, cartAPI, orderAPI, paymentAPI } from '../services/api';

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
      paymentMethod: 'vnpay', // Giá trị mặc định là VNPay
      termsAccepted: false
    });

    // Load user data and cart items
    const loadData = async () => {
      try {
        loading.value = true;
        error.value = null;

        // Lấy thông tin user từ localStorage
        const storedUser = JSON.parse(localStorage.getItem('user'));
        if (!storedUser) {
          router.push('/login');
          return;
        }

        // Lấy thông tin chi tiết user từ API
        const userResponse = await userAPI.getProfile(storedUser.id);
        user.value = userResponse.data;

        // Lấy thông tin giỏ hàng từ API
        const cartResponse = await cartAPI.getCart(storedUser.id);
        console.log('Cart response:', cartResponse);

        if (!cartResponse.data || !cartResponse.data.items || cartResponse.data.items.length === 0) {
          error.value = 'Giỏ hàng trống!';
          return;
        }

        cartItems.value = cartResponse.data.items.map(item => ({
          id: item.menu_item_id,
          name: item.MenuItem.name,
          price: item.price,
          quantity: item.quantity,
          image: item.MenuItem.img
        }));

        // Pre-fill form with user data
        if (user.value) {
          form.value.email = user.value.email;
          form.value.fullName = user.value.fullname || '';
          form.value.phone = user.value.phone_number || '';
          form.value.address = user.value.address || '';
        }
      } catch (error) {
        console.error('Error loading data:', error);
        error.value = 'Có lỗi xảy ra khi tải thông tin. Vui lòng thử lại sau.';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadData();
    });

    // Calculate totals
    const subtotal = computed(() => {
      return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0);
    });

    const deliveryFee = computed(() => {
      return subtotal.value > 50 ? 0 : 5.99; // Free delivery for orders over $50
    });

    const total = computed(() => {
      return subtotal.value + deliveryFee.value;
    });

    // Place order
    const placeOrder = async () => {
      if (!user.value) {
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
        // Tạo đơn hàng mới
        const orderData = {
          user_Id: user.value.id,
          total_price: total.value,
          status: 'pending',
          payment_status: form.value.paymentMethod === 'vnpay' ? 'pending' : 'pending', // Trạng thái thanh toán ban đầu
          shipping_address: form.value.address,
          full_name: form.value.fullName,
          phone_number: form.value.phone,
          email: form.value.email,
          payment_method: form.value.paymentMethod
        };

        console.log('Creating order with data:', orderData);
        const orderResponse = await orderAPI.createOrder(orderData);
        console.log('Order response:', orderResponse);

        if (orderResponse.data && orderResponse.data.order) {
          const orderId = orderResponse.data.order.id;

          // Tạo chi tiết đơn hàng cho từng món
          for (const item of cartItems.value) {
            const orderDetailData = {
              order_Id: orderId,
              menu_item_Id: item.id,
              quantity: item.quantity,
              price: item.price,
              total_price: item.price * item.quantity
            };
            console.log('Creating order detail with data:', orderDetailData);
            await orderAPI.createOrderDetails(orderDetailData);
          }

          // Nếu là VNPay, lưu orderNumber và gọi hàm khởi tạo thanh toán
          if (form.value.paymentMethod === 'vnpay') {
            orderNumber.value = orderId;
            await initiateVNPayPayment(orderId);
          } else {
            // Nếu không phải VNPay (ví dụ: Cash on Delivery), tiến hành tạo payment thông thường và hiển thị modal
            const paymentData = {
              order_Id: orderId,
              user_Id: user.value.id,
              total_payment: total.value,
              method: form.value.paymentMethod,
              status: 'pending'
            };
            console.log('Creating payment with data:', paymentData);
            await paymentAPI.createPayment(paymentData);

            // Xóa giỏ hàng
            await cartAPI.clearCart(user.value.id);

            // Cập nhật số lượng sản phẩm trên navbar
            //localStorage.setItem('cartCount', '0');
            window.dispatchEvent(new CustomEvent('cartUpdated'));
            // Hiển thị modal thành công
            orderNumber.value = orderId;
            showSuccessModal.value = true;
          }
        }
      } catch (error) {
        console.error('Error placing order:', error);
        alert('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại sau.');
      } finally {
        loading.value = false;
      }
    };

    const initiateVNPayPayment = async (orderId) => {
      loading.value = true;
      try {
        const paymentData = {
          orderId: orderId,
          amount: total.value, // Gửi trực tiếp giá trị total (đã là VND)
          orderInfo: `${orderId}`,
          returnUrl: 'http://localhost:5173/orders' // Điều chỉnh URL trả về nếu cần
        };

        console.log('Dữ liệu gửi đến backend để thanh toán VNPay:', JSON.stringify(paymentData, null, 2));

        const vnpayResponse = await paymentAPI.initiateVNPAY(paymentData);

        if (vnpayResponse && vnpayResponse.data && vnpayResponse.data.data) {
          
            // Xóa giỏ hàng
            await cartAPI.clearCart(user.value.id);

            // Cập nhật số lượng sản phẩm trên navbar
            //localStorage.setItem('cartCount', '0');
            window.dispatchEvent(new CustomEvent('cartUpdated'));
          // Chuyển hướng người dùng đến URL thanh toán của VNPAY
          window.location.href = vnpayResponse.data.data;
        } else {
          alert('Có lỗi xảy ra khi khởi tạo thanh toán VNPay.');
          console.error('Lỗi khởi tạo thanh toán VNPay:', vnpayResponse);
        }
      } catch (error) {
        console.error('Error initiating VNPay payment:', error);
        alert('Không thể khởi tạo thanh toán VNPay. Vui lòng thử lại sau.');
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
      goToOrders
    };
  }
};
</script>