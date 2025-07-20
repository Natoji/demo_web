<template>
  <div>
    <div class="relative bg-orange-500 text-white py-16">
      <div class="container mx-auto px-4 flex flex-col items-center text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Delicious Food Delivered to Your Door</h1>
        <p class="text-xl mb-8 max-w-2xl">Explore our menu of fresh, tasty dishes prepared by expert chefs and delivered right to your doorstep.</p>
        <button class="bg-white text-rose-600 font-bold py-3 px-8 rounded-full hover:bg-rose-100 transition duration-300">
          Order Now
        </button>
      </div>
    </div>

    <div v-if="loading" class="container mx-auto px-4 py-8 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading menu items...</p>
    </div>

    <div v-else-if="error" class="container mx-auto px-4 py-8 text-center">
      <div class="text-red-600 mb-4">
        <svg class="h-12 w-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <p class="text-gray-600">{{ error }}</p>
    </div>

    <div v-else class="container mx-auto px-4 py-8">
      <div class="flex flex-wrap justify-center gap-4 mb-8">
        <button
          @click="selectedCategory = null"
          class="px-4 py-2 rounded-full"
          :class="selectedCategory === null ? 'bg-rose-600 text-white' : 'bg-gray-200 hover:bg-gray-300'"
        >
          All
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectedCategory = category.id"
          class="px-4 py-2 rounded-full"
          :class="selectedCategory === category.id ? 'bg-rose-600 text-white' : 'bg-gray-200 hover:bg-gray-300'"
        >
          {{ category.name }}
        </button>
      </div>

      <div class="max-w-md mx-auto mb-8">
        <div class="relative flex items-center">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search for food..."
            class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-rose-500"
          >
          <Search class="absolute right-3 text-gray-500 h-5 w-5" />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
        >
          <router-link :to="`/product/${product.id}`" class="block">
            <img
              v-if="product.img"
              :src="`${product.img}`"
              :alt="product.name"
              class="w-full h-48 object-cover hover:opacity-90 transition-opacity"
              @error="handleImageError"
            >
          </router-link>

          <div class="p-4">
            <router-link :to="`/product/${product.id}`" class="block">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-bold hover:text-rose-600 transition-colors">
                  {{ product.name }}
                </h3>
                <span class="bg-rose-100 text-rose-800 text-xs font-semibold px-2 py-1 rounded-full">{{ getCategoryNameForProduct(product.category) }}</span>
              </div>

              <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ product.description }}</p>

              <div class="flex justify-between items-center">
                <span class="text-rose-600 font-bold">{{ Number(product.price).toFixed(2) }} VNĐ</span>
              </div>
            </router-link>

            <div class="flex justify-end mt-4">
              <button
                @click="addToCart(product)"
                class="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-rose-700 flex items-center justify-center gap-2"
              >
                <ShoppingCart class="h-5 w-5" />
                Add to cart
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredProducts.length === 0" class="text-center py-12">
        <ShoppingBag class="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No products found</h3>
        <p class="text-gray-500">Try adjusting your search or filter to find what you're looking for.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Search, ShoppingCart, Eye, ShoppingBag } from 'lucide-vue-next';
import axios from 'axios';

export default {
  name: 'Home',
  components: {
    Search,
    ShoppingCart,
    Eye,
    ShoppingBag
  },
  setup() {
    const searchQuery = ref('');
    const selectedCategory = ref(null);
    const categories = ref([]); // Giữ nguyên là mảng cho danh sách bộ lọc
    const productCategories = ref({}); // Object để lưu trữ tên danh mục của sản phẩm
    const products = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const cartQuantity = ref(0);

    const handleImageError = (e) => {
      console.error('Image loading error:', e.target.src);
    };

    const updateCartQuantity = async () => {
      try {
        const userId = localStorage.getItem('userId');
        const accessToken = localStorage.getItem('access_token');
        if (!userId || !accessToken) return;

        const response = await axios.get(`http://localhost:8000/api/carts/${userId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        cartQuantity.value = response.data.cartItems.reduce((sum, item) => sum + item.quantity, 0);
      } catch (err) {
        console.error('Error updating cart quantity:', err);
      }
    };

    const fetchCategory = async (categoryId) => {
      try {
        const response = await axios.get(`http://localhost:8000/api/categories/${categoryId}/`);
        productCategories.value[categoryId] = response.data.name;
      } catch (err) {
        console.error(`Error fetching category ${categoryId}:`, err);
        productCategories.value[categoryId] = 'Unknown';
      }
    };

    onMounted(async () => {
      try {
        loading.value = true;
        const accessToken = localStorage.getItem('access_token');

        const [categoriesResponse, productsResponse] = await Promise.all([
          axios.get('http://localhost:8000/api/categories/', {
          }),
          axios.get('http://localhost:8000/api/products/', {
          }),
        ]);
        categories.value = categoriesResponse.data; // Giữ nguyên cách lấy danh sách danh mục
        products.value = productsResponse.data.map(product => ({
          ...product,
          price: Number(product.price),
        }));

        // Fetch category name for each product
        products.value.forEach(product => {
          if (!productCategories.value[product.category]) {
            fetchCategory(product.category);
          }
        });

        await updateCartQuantity();
      } catch (err) {
        error.value = 'Failed to load data. Please try again later.';
        console.error('Error loading data:', err);
      } finally {
        loading.value = false;
      }
    });

    const filteredProducts = computed(() => {
      return products.value.filter(product => {
        if (selectedCategory.value && product.category !== selectedCategory.value) {
          return false;
        }
        if (searchQuery.value) {
          const query = searchQuery.value.toLowerCase();
          return (
            product.name.toLowerCase().includes(query) ||
            product.description?.toLowerCase().includes(query)
          );
        }
        return true;
      });
    });

    const getCategoryName = (categoryId) => {
      const category = categories.value.find(c => c.id === categoryId);
      return category ? category.name : '';
    };

    const getCategoryNameForProduct = (categoryId) => {
      return productCategories.value[categoryId] || 'Loading...';
    };

    const addToCart = async (product) => {
      try {
        const userId = localStorage.getItem('userId');
        const accessToken = localStorage.getItem('access_token');
        if (!userId || !accessToken) {
          window.location.href = '/login';
          return;
        }

        console.log('Product to add:', {
          id: product.id,
          name: product.name,
          price: product.price,
        });

        const cartData = {
          product_id: Number(product.id), // Sử dụng product_id theo API mới
          quantity: 1,
        };

        console.log('Cart data to send:', cartData);

        const response = await axios.post('http://localhost:8000/api/cart/add/', cartData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response && response.data) {
          alert(`${product.name} đã được thêm vào giỏ hàng!`);
          await updateCartQuantity();
          window.dispatchEvent(new Event('cartUpdated'));
        }
      } catch (err) {
        console.error('Error adding to cart:', err);
        if (err.response) {
          console.error('Error response:', err.response.data);
        }
        alert('Không thể thêm sản phẩm vào giỏ hàng. Vui lòng thử lại sau.');
      }
    };

    return {
      searchQuery,
      selectedCategory,
      categories,
      filteredProducts,
      getCategoryName,
      getCategoryNameForProduct,
      addToCart,
      loading,
      error,
      cartQuantity,
      handleImageError,
    };
  },
};
</script>