<template>
  <nav class="bg-orange-500 text-white p-4 fixed top-0 left-0 right-0 z-50 shadow-md">
    <div class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-2xl font-bold">FoodShop</router-link>

      <div class="flex items-center space-x-6">
        <template v-if="user">
          <router-link to="/" class="hover:text-orange-200 transition-colors">Home</router-link>
          <template v-if="user.user.role !== 'admin'">
            <router-link to="/contact" class="hover:text-orange-200 transition-colors">Liên hệ</router-link>
            <router-link to="/cart" class="hover:text-orange-200 relative transition-colors">
              <ShoppingCart class="h-6 w-6" />
              <span v-if="cartCount > 0"
                class="absolute -top-2 -right-2 bg-yellow-400 text-orange-700 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">
                {{ cartCount }}
              </span>
            </router-link>
          </template>

          <div class="relative">
            <button @click="isUserMenuOpen = !isUserMenuOpen"
              class="flex items-center hover:text-orange-200 transition-colors focus:outline-none">
              <User class="h-5 w-5 mr-1" />
              {{ user.user.fullname }}
              <ChevronDown class="h-4 w-4 ml-1" :class="{ 'transform rotate-180': isUserMenuOpen }" />
            </button>

            <div v-if="isUserMenuOpen"
              class="absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-md shadow-lg py-1 z-10"
              @mouseleave="isUserMenuOpen = false">
              <template v-if="user.user.role !== 'admin'">
                <router-link to="/orders" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <ClipboardList class="h-4 w-4 mr-2" />
                    My Orders
                  </div>
                </router-link>
                <router-link to="/profile" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <User class="h-4 w-4 mr-2" />
                    Profile
                  </div>
                </router-link>
              </template>
              <template v-if="user.user.role === 'admin'">
                <router-link to="/admin/dashboard" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <LayoutDashboard class="h-4 w-4 mr-2" />
                    Dashboard
                  </div>
                </router-link>
                <router-link to="/admin/products" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <Package class="h-4 w-4 mr-2" />
                    Manage Products
                  </div>
                </router-link>
                <router-link to="/admin/orders" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <ClipboardList class="h-4 w-4 mr-2" />
                    Manage Orders
                  </div>
                </router-link>
                <router-link to="/admin/users" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <Users class="h-4 w-4 mr-2" />
                    Manage Users
                  </div>
                </router-link>
                <router-link to="/admin/adminCategories" class="block px-4 py-2 hover:bg-orange-100 transition-colors"
                  @click="isUserMenuOpen = false">
                  <div class="flex items-center">
                    <Tags class="h-4 w-4 mr-2" />
                    Manage Categories
                  </div>
                </router-link>
                <div class="border-t border-gray-200 my-1"></div>
              </template>
              <button @click="handleLogout" class="block w-full text-left px-4 py-2 hover:bg-orange-100 transition-colors">
                <div class="flex items-center text-red-600">
                  <LogOut class="h-4 w-4 mr-2" />
                  Logout
                </div>
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="hover:text-orange-200 transition-colors">Login</router-link>
          <router-link to="/register" class="hover:text-orange-200 transition-colors">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
  <div class="h-16"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import {
  ShoppingCart,
  User,
  ChevronDown,
  ClipboardList,
  LayoutDashboard,
  Package,
  Users,
  Tags,
  LogOut
} from 'lucide-vue-next'
import { cartAPI } from '../services/api'

export default {
  name: 'Navbar',
  components: {
    ShoppingCart,
    User,
    ChevronDown,
    ClipboardList,
    LayoutDashboard,
    Package,
    Users,
    Tags,
    LogOut
  },
  props: {
    user: Object
  },
  setup(props, { emit }) {
    const cartCount = ref(0)
    const isUserMenuOpen = ref(false)

    const updateCartCount = async () => {
      if (props.user) {
        try {
          console.log('Updating cart count for user:', props.user.user.id); // Corrected access
          const response = await cartAPI.getCartCount(props.user.user.id); // Corrected access
          console.log('Cart count response:', response.data);
          if (response.data && typeof response.data.count === 'number') {
            cartCount.value = response.data.count;
            localStorage.setItem(`cartCount_${props.user.user.id}`, response.data.count); // Corrected access
            localStorage.setItem('currentUser', JSON.stringify(props.user));
          } else {
            console.error('Invalid cart count response:', response.data);
            cartCount.value = 0;
            localStorage.removeItem(`cartCount_${props.user.user.id}`);
          }
        } catch (error) {
          console.error('Error fetching cart count:', error);
          cartCount.value = 0;
          localStorage.removeItem(`cartCount_${props.user.user.id}`);
        }
      } else {
        // Kiểm tra xem có user info trong localStorage không
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
          try {
            const user = JSON.parse(savedUser);
            console.log('Found saved user:', user);
            const response = await cartAPI.getCartCount(user.user.id); // Corrected access
            if (response.data && typeof response.data.count === 'number') {
              cartCount.value = response.data.count;
              localStorage.setItem(`cartCount_${user.user.id}`, response.data.count);
            }
          } catch (error) {
            console.error('Error restoring cart count:', error);
            localStorage.removeItem('currentUser');
            localStorage.removeItem(`cartCount_${JSON.parse(savedUser).user.id}`); // Corrected access
          }
        } else {
          cartCount.value = 0;
        }
      }
    }

    // Khôi phục cart count từ localStorage khi component mounts
    onMounted(() => {
      console.log('Navbar mounted');
      console.log('User prop received:', props.user);
      if (props.user) {
        console.log('User ID:', props.user.user.id); // Corrected access
        console.log('User Name:', props.user.user.fullname); // Corrected access
        console.log('User Role:', props.user.user.role); // Corrected access
      } else {
        console.log('User prop is undefined or null.');
      }
      updateCartCount();
    })

    // Create a custom event for cart updates
    const handleCartUpdate = () => {
      console.log('Cart update event received');
      updateCartCount();
    }

    // Add event listener for custom cart update event
    onMounted(() => {
      console.log('Adding cartUpdated event listener');
      window.addEventListener('cartUpdated', handleCartUpdate);
    })

    // Clean up event listener when component unmounts
    onBeforeUnmount(() => {
      console.log('Removing cartUpdated event listener');
      window.removeEventListener('cartUpdated', handleCartUpdate);
    })

    // Handle logout
    const handleLogout = () => {
      isUserMenuOpen.value = false;
      if (props.user) {
        localStorage.removeItem(`cartCount_${props.user.user.id}`); // Corrected access
      }
      localStorage.removeItem('currentUser');
      cartCount.value = 0;
      emit('logout');
    }

    return {
      cartCount,
      isUserMenuOpen,
      handleLogout
    }
  }
}
</script>