<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Your Cart</h1>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Đang tải giỏ hàng...</p>
    </div>

    <div v-else-if="error" class="text-center py-12 bg-white rounded-lg shadow-md">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <button @click="loadCart" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700">
        Thử lại
      </button>
    </div>

    <div v-else-if="cartItems.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="md:col-span-2">
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="p-4 border-b">
            <h2 class="text-lg font-semibold">Cart Items ({{ totalItems }})</h2>
          </div>

          <ul class="divide-y divide-gray-200">
            <li v-for="item in cartItems" :key="item.id" class="p-4 flex flex-col sm:flex-row sm:items-center">
              <div class="flex-shrink-0 mb-4 sm:mb-0 sm:mr-4">
                <img :src="item.image" :alt="item.name" class="w-20 h-20 object-cover rounded">
              </div>

              <div class="flex-grow">
                <h3 class="font-medium text-gray-800">{{ item.name }}</h3>
                <p class="text-gray-600 text-sm">{{ item.price.toFixed(2) }} $ each</p>
              </div>

              <div class="flex items-center mt-4 sm:mt-0">
                <button
                  @click="updateQuantity(item.product, item.quantity - 1)"
                  class="bg-gray-200 text-gray-700 px-2 py-1 rounded-l-md hover:bg-gray-300"
                  :disabled="item.quantity <= 1"
                >
                  <Minus class="h-4 w-4" />
                </button>

                <input
                  type="number"
                  v-model="item.quantity"
                  min="1"
                  class="w-12 text-center border-t border-b border-gray-200 py-1"
                  @change="updateQuantity(item.product, parseInt(item.quantity))"
                >

                <button
                  @click="updateQuantity(item.product, item.quantity + 1)"
                  class="bg-gray-200 text-gray-700 px-2 py-1 rounded-r-md hover:bg-gray-300"
                >
                  <Plus class="h-4 w-4" />
                </button>

                <span class="mx-4 font-medium">{{ (item.price * item.quantity).toFixed(2) }} $</span>

                <button
                  @click="removeItem(item.product)"
                  class="text-red-500 hover:text-red-700"
                >
                  <Trash2 class="h-5 w-5" />
                </button>
              </div>
            </li>
          </ul>

          <div class="p-4 border-t flex justify-between">
            <button
              @click="clearCart"
              class="text-red-500 hover:text-red-700 flex items-center"
            >
              <Trash2 class="h-5 w-5 mr-1" />
              Clear Cart
            </button>

            <router-link to="/" class="text-rose-600 hover:text-rose-800 flex items-center">
              <ArrowLeft class="h-5 w-5 mr-1" />
              Continue Shopping
            </router-link>
          </div>
        </div>
      </div>

      <div class="md:col-span-1">
        <div class="bg-white rounded-lg shadow-md overflow-hidden sticky top-4">
          <div class="p-4 border-b">
            <h2 class="text-lg font-semibold">Order Summary</h2>
          </div>

          <div class="p-4 space-y-4">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span class="font-medium">{{ subtotal.toFixed(2) }} $</span>
            </div>

            <div class="border-t pt-4 flex justify-between font-bold">
              <span>Total</span>
              <span>{{ total.toFixed(2) }} $</span>
            </div>

            <button
              @click="handleCheckout"
              class="block w-full bg-rose-600 text-white text-center py-3 px-4 rounded-lg hover:bg-rose-700"
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 bg-white rounded-lg shadow-md">
      <ShoppingCart class="h-16 w-16 mx-auto text-gray-400 mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Giỏ hàng trống</h3>
      <p class="text-gray-500 mb-6">Bạn chưa thêm sản phẩm nào vào giỏ hàng.</p>
      <router-link to="/" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700">
        Mua sắm ngay
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Minus, Plus, Trash2, ArrowLeft, ShoppingCart } from 'lucide-vue-next';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Cart',
  components: {
    Minus,
    Plus,
    Trash2,
    ArrowLeft,
    ShoppingCart
  },
  setup() {
    const cartItems = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const router = useRouter();

    // Lấy thông tin user từ localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
      window.location.href = '/login';
      return;
    }

    const accessToken = localStorage.getItem('access_token');

    // Load cart items from API
    const loadCart = async () => {
      try {
        loading.value = true;
        const response = await axios.get('https://demo-web-m8jr.onrender.com/api/cart/', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log('Cart API Response:', response);
        console.log('Cart Data:', response.data);

        if (response.data && response.data.items) {
          cartItems.value = response.data.items.map(item => ({
            id: item.id, // Sử dụng ID của item giỏ hàng
            product: item.product, // Lưu trữ ID sản phẩm
            name: item.product_name,
            price: Number(item.product_price),
            quantity: item.quantity,
            image: item.product_img // Bạn có thể cần gọi API sản phẩm để lấy hình ảnh
          }));
        } else {
          cartItems.value = [];
        }
      } catch (err) {
        console.error('Error loading cart:', err);
        error.value = 'Không thể tải giỏ hàng. Vui lòng thử lại sau.';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadCart();
    });

    // Calculate totals
    const subtotal = computed(() => {
      return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0);
    });

    const shipping = computed(() => {
      return 0;
    });

    const total = computed(() => {
      return subtotal.value + shipping.value;
    });

    const totalItems = computed(() => {
      return cartItems.value.reduce((count, item) => count + item.quantity, 0);
    });

    // Cart operations
    const updateQuantity = async (productId, newQuantity) => {
      if (newQuantity < 1) return;

      try {
        console.log('Updating quantity for product:', productId, 'to:', newQuantity);
        const response = await axios.post('https://demo-web-m8jr.onrender.com/api/cart/update/', {
          product_id: productId,
          quantity: newQuantity
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log('Update response:', response.data);

        // Refresh cart data
        await loadCart();

        // Emit custom event to update cart count in navbar
        console.log('Dispatching cartUpdated event');
        window.dispatchEvent(new Event('cartUpdated'));
      } catch (err) {
        console.error('Error updating quantity:', err);
        alert('Không thể cập nhật số lượng. Vui lòng thử lại sau.');
      }
    };

    const removeItem = async (productId) => {
      try {
        console.log('Removing product:', productId);
        const response = await axios.post('https://demo-web-m8jr.onrender.com/api/cart/remove/', {
          product_id: productId
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log('Remove response:', response.data);

        // Refresh cart data
        await loadCart();

        // Emit custom event to update cart count in navbar
        console.log('Dispatching cartUpdated event');
        window.dispatchEvent(new Event('cartUpdated'));
      } catch (err) {
        console.error('Error removing item:', err);
        alert('Không thể xóa sản phẩm. Vui lòng thử lại sau.');
      }
    };

    const clearCart = async () => {
      if (confirm('Bạn có chắc chắn muốn xóa toàn bộ giỏ hàng?')) {
        try {
          console.log('Clearing cart for user:', user.id);
          const response = await axios.post('https://demo-web-m8jr.onrender.com/api/cart/clear/', {}, { // Assuming clear cart API doesn't require body
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          console.log('Clear cart response:', response.data);

          // Refresh cart data
          await loadCart();

          // Emit custom event to update cart count in navbar
          console.log('Dispatching cartUpdated event');
          window.dispatchEvent(new Event('cartUpdated'));
        } catch (err) {
          console.error('Error clearing cart:', err);
          alert('Không thể xóa giỏ hàng. Vui lòng thử lại sau.');
        }
      }
    };

    const handleCheckout = async () => {
      try {
        // Kiểm tra giỏ hàng hiện tại
        if (cartItems.value.length === 0) {
          alert('Giỏ hàng trống!');
          return;
        }

        // Chuyển hướng đến trang Checkout
        router.push('/checkout');
      } catch (err) {
        console.error('Error during checkout:', err);
        alert('Có lỗi xảy ra trong quá trình thanh toán. Vui lòng thử lại sau.');
      }
    };

    return {
      cartItems,
      loading,
      error,
      subtotal,
      shipping,
      total,
      totalItems,
      updateQuantity,
      removeItem,
      clearCart,
      handleCheckout
    };
  }
};
</script>