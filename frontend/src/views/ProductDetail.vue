<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-rose-600"></div>
    </div>

    <div v-else-if="product" class="bg-white rounded-lg shadow-lg overflow-hidden">
      <div class="md:flex">
        <div class="md:w-1/2 p-4">
          <div class="relative aspect-square w-full max-w-[500px] max-h-[500px] mx-auto bg-gray-100 rounded-lg overflow-hidden">
            <img
              v-if="product.img"
              :src="`${product.img}`"
              :alt="product.name"
              class="absolute inset-0 w-full h-full object-contain"
              @error="handleImageError"
            >
          </div>
        </div>

        <div class="md:w-1/2 p-6 md:p-8">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ product.name }}</h1>
              <span class="inline-block bg-rose-100 text-rose-800 text-sm font-semibold px-3 py-1 rounded-full mb-4">
                {{ getCategoryName(product.cat_Id) }}
              </span>
            </div>
            <span class="text-2xl font-bold text-rose-600">${{ Number(product.price).toFixed(2) }}</span>
          </div>

          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-700 mb-2">Description</h2>
            <p class="text-gray-600">{{ product.description }}</p>
          </div>

          <div class="mb-6">
            <h2 class="text-lg font-semibold text-gray-700 mb-2">Quantity</h2>
            <div class="flex items-center">
              <button
                @click="quantity > 1 ? quantity-- : null"
                class="bg-gray-200 text-gray-700 px-3 py-1 rounded-l-md hover:bg-gray-300"
              >
                <Minus class="h-5 w-5" />
              </button>

              <input
                type="number"
                v-model="quantity"
                min="1"
                class="w-16 text-center border-t border-b border-gray-200 py-1"
                readonly
              >

              <button
                @click="quantity++"
                class="bg-gray-200 text-gray-700 px-3 py-1 rounded-r-md hover:bg-gray-300"
              >
                <Plus class="h-5 w-5" />
              </button>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <button
              @click="addToCart"
              class="flex-1 bg-rose-600 text-white py-3 px-6 rounded-lg hover:bg-rose-700 flex items-center justify-center gap-2"
            >
              <ShoppingCart class="h-5 w-5" />
              Add to Cart
            </button>

            <button
              class="flex-1 border border-rose-600 text-rose-600 py-3 px-6 rounded-lg hover:bg-rose-50 flex items-center justify-center gap-2"
            >
              <Heart class="h-5 w-5" />
              Add to Favorites
            </button>
          </div>

          <div class="mt-8 border-t border-gray-200 pt-6">
            <h2 class="text-lg font-semibold text-gray-700 mb-4">Customer Reviews</h2>

            <div class="flex items-center mb-4">
              <div class="flex text-yellow-400">
                <Star class="h-5 w-5 fill-current" />
                <Star class="h-5 w-5 fill-current" />
                <Star class="h-5 w-5 fill-current" />
                <Star class="h-5 w-5 fill-current" />
                <Star class="h-5 w-5" />
              </div>
              <span class="ml-2 text-gray-600">4.0 out of 5</span>
            </div>

            <p class="text-gray-600 text-sm">Based on 24 reviews</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <AlertCircle class="h-16 w-16 mx-auto text-gray-400 mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Product not found</h3>
      <p class="text-gray-500 mb-6">The product you're looking for doesn't exist or has been removed.</p>
      <router-link to="/" class="bg-rose-600 text-white py-2 px-6 rounded-lg hover:bg-rose-700">
        Back to Home
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ShoppingCart, Heart, Star, Minus, Plus, AlertCircle } from 'lucide-vue-next'
import { menuItemAPI, categoryAPI, cartAPI } from '../services/api'

export default {
  name: 'ProductDetail',
  components: {
    ShoppingCart,
    Heart,
    Star,
    Minus,
    Plus,
    AlertCircle
  },
  setup() {
    const route = useRoute()
    const productId = parseInt(route.params.id)

    const product = ref(null)
    const loading = ref(true)
    const quantity = ref(1)
    const categories = ref([])

    // Function to handle image loading errors
    const handleImageError = (e) => {
      console.error('Image loading error:', e.target.src)
      // If there's an error loading the product image, do nothing (don't show placeholder)
    }

    onMounted(async () => {
      try {
        loading.value = true
        // Scroll to top of the page
        window.scrollTo({ top: 0, behavior: 'smooth' })

        // Fetch both product and categories data
        const [productResponse, categoriesResponse] = await Promise.all([
          menuItemAPI.getById(productId),
          categoryAPI.getAll()
        ])

        // Process product data
        if (productResponse.data) {
          product.value = {
            ...productResponse.data,
            price: Number(productResponse.data.price)
          }
        }

        categories.value = categoriesResponse.data
      } catch (error) {
        console.error('Error fetching product:', error)
      } finally {
        loading.value = false
      }
    })

    const getCategoryName = (categoryId) => {
      const category = categories.value.find(c => c.id === categoryId)
      return category ? category.name : ''
    }

    const addToCart = async () => {
      if (!product.value) return

      try {
        // Lấy thông tin user từ localStorage
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          window.location.href = '/login'
          return
        }

        // Thêm sản phẩm vào giỏ hàng qua API
        const response = await cartAPI.addToCart(user.id, {
          menuItemId: parseInt(product.value.id),
          quantity: parseInt(quantity.value)
        })

        if (response.data) {
          // Hiển thị thông báo thành công
          alert(`${quantity.value} ${product.value.name}${quantity.value > 1 ? 's' : ''} đã được thêm vào giỏ hàng!`)

          // Reset quantity
          quantity.value = 1

          // Dispatch custom event to notify other components
          window.dispatchEvent(new Event('cartUpdated'))
        }
      } catch (err) {
        console.error('Error adding to cart:', err)
        alert('Không thể thêm sản phẩm vào giỏ hàng. Vui lòng thử lại sau.')
      }
    }

    return {
      product,
      loading,
      quantity,
      getCategoryName,
      addToCart,
      handleImageError
    }
  }
}
</script>