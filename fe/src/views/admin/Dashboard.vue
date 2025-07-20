<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Admin Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Dashboard Cards -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100 text-orange-600 mr-4">
            <ShoppingCart class="h-6 w-6" />
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Orders</p>
            <h3 class="text-2xl font-bold">128</h3>
          </div>
        </div>
        <div class="mt-4 text-sm text-green-600 flex items-center">
          <TrendingUp class="h-4 w-4 mr-1" />
          <span>12% increase</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
            <DollarSign class="h-6 w-6" />
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Revenue</p>
            <h3 class="text-2xl font-bold">$6,240</h3>
          </div>
        </div>
        <div class="mt-4 text-sm text-green-600 flex items-center">
          <TrendingUp class="h-4 w-4 mr-1" />
          <span>8% increase</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100 text-green-600 mr-4">
            <Users class="h-6 w-6" />
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Users</p>
            <h3 class="text-2xl font-bold">64</h3>
          </div>
        </div>
        <div class="mt-4 text-sm text-green-600 flex items-center">
          <TrendingUp class="h-4 w-4 mr-1" />
          <span>24% increase</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
            <Package class="h-6 w-6" />
          </div>
          <div>
            <p class="text-gray-500 text-sm">Total Products</p>
            <h3 class="text-2xl font-bold">32</h3>
          </div>
        </div>
        <div class="mt-4 text-sm text-red-600 flex items-center">
          <TrendingDown class="h-4 w-4 mr-1" />
          <span>3% decrease</span>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Orders -->
      <div class="lg:col-span-2 bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-semibold">Recent Orders</h2>
          <router-link to="/admin/orders" class="text-orange-600 hover:text-orange-800 text-sm">View All</router-link>
        </div>
        
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="order in recentOrders" :key="order.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ order.id }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.customer }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.date }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${{ order.amount.toFixed(2) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="{
                      'bg-green-100 text-green-800': order.status === 'Completed',
                      'bg-yellow-100 text-yellow-800': order.status === 'Processing',
                      'bg-blue-100 text-blue-800': order.status === 'Shipped',
                      'bg-red-100 text-red-800': order.status === 'Cancelled'
                    }"
                  >
                    {{ order.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Top Products -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">Top Products</h2>
        </div>
        
        <ul class="divide-y divide-gray-200">
          <li v-for="product in topProducts" :key="product.id" class="p-4">
            <div class="flex items-center">
              <img :src="product.image" :alt="product.name" class="w-10 h-10 object-cover rounded mr-3">
              <div class="flex-grow">
                <h3 class="text-sm font-medium text-gray-900">{{ product.name }}</h3>
                <p class="text-sm text-gray-500">${{ product.price.toFixed(2) }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900">{{ product.sales }} sold</p>
                <p class="text-xs text-gray-500">{{ product.revenue }}</p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { 
  ShoppingCart, 
  DollarSign, 
  Users, 
  Package, 
  TrendingUp, 
  TrendingDown 
} from 'lucide-vue-next'

export default {
  name: 'AdminDashboard',
  components: {
    ShoppingCart,
    DollarSign,
    Users,
    Package,
    TrendingUp,
    TrendingDown
  },
  setup() {
    // Mock data for recent orders
    const recentOrders = ref([
      { id: '1001', customer: 'John Doe', date: '2023-04-01', amount: 89.99, status: 'Completed' },
      { id: '1002', customer: 'Jane Smith', date: '2023-04-02', amount: 124.50, status: 'Processing' },
      { id: '1003', customer: 'Robert Johnson', date: '2023-04-02', amount: 45.75, status: 'Shipped' },
      { id: '1004', customer: 'Emily Davis', date: '2023-04-03', amount: 65.25, status: 'Completed' },
      { id: '1005', customer: 'Michael Brown', date: '2023-04-03', amount: 32.99, status: 'Cancelled' }
    ])
    
    // Mock data for top products
    const topProducts = ref([
      { 
        id: 1, 
        name: 'Classic Burger', 
        price: 8.99, 
        sales: 42, 
        revenue: '$377.58',
        image: '/placeholder.svg?height=100&width=100'
      },
      { 
        id: 2, 
        name: 'Margherita Pizza', 
        price: 12.99, 
        sales: 38, 
        revenue: '$493.62',
        image: '/placeholder.svg?height=100&width=100'
      },
      { 
        id: 3, 
        name: 'California Roll', 
        price: 9.99, 
        sales: 35, 
        revenue: '$349.65',
        image: '/placeholder.svg?height=100&width=100'
      },
      { 
        id: 4, 
        name: 'Chocolate Brownie', 
        price: 6.99, 
        sales: 30, 
        revenue: '$209.70',
        image: '/placeholder.svg?height=100&width=100'
      },
      { 
        id: 5, 
        name: 'Strawberry Milkshake', 
        price: 4.99, 
        sales: 28, 
        revenue: '$139.72',
        image: '/placeholder.svg?height=100&width=100'
      }
    ])
    
    return {
      recentOrders,
      topProducts
    }
  }
}
</script>