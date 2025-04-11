<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Manage Orders</h1>

      <div class="flex space-x-2">
        <button
          @click="exportOrders"
          class="bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 flex items-center"
        >
          <Download class="h-5 w-5 mr-1" />
          Export
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-grow">
          <label for="search" class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <div class="relative">
            <input
              type="text"
              id="search"
              v-model="searchQuery"
              placeholder="Search by order ID"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
            <Search class="absolute right-3 top-2.5 text-gray-500 h-5 w-5" />
          </div>
        </div>

        <div class="w-full md:w-48">
          <label for="dateRange" class="block text-sm font-medium text-gray-700 mb-1">Date Range</label>
          <select
            id="dateRange"
            v-model="dateRange"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
          >
            <option value="all">All Time</option>
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="order in paginatedOrders" :key="order.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                #{{ order.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ userNames[order.user] || 'Loading...' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${{ parseFloat(order.total_amount)?.toFixed(2) || 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <select
                  v-model="order.status"
                  @change="updateOrderStatus(order.id, order.status)"
                  class="text-xs font-semibold rounded-full px-2 py-1 border"
                  :class="{
                    'bg-yellow-100 text-yellow-800 border-yellow-200': order.status === 'pending',
                    'bg-blue-100 text-blue-800 border-blue-200': order.status === 'processing',
                    'bg-indigo-100 text-indigo-800 border-indigo-200': order.status === 'shipped',
                    'bg-green-100 text-green-800 border-green-200': order.status === 'delivered',
                    'bg-red-100 text-red-800 border-red-200': order.status === 'cancelled'
                  }"
                >
                  <option value="pending">Pending</option>
                  <option value="processing">Processing</option>
                  <option value="shipped">Shipped</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click="viewOrderDetails(order)"
                  class="text-indigo-600 hover:text-indigo-900 mr-3"
                >
                  <Eye class="h-5 w-5" />
                </button>
                <button
                  @click="printOrder(order.id)"
                  class="text-gray-600 hover:text-gray-900"
                >
                  <Printer class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredOrders.length === 0" class="text-center py-12">
        <ShoppingBag class="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No orders found</h3>
        <p class="text-gray-500">Try adjusting your search or filter to find what you're looking for.</p>
      </div>
    </div>

    <div class="flex justify-center mt-4" v-if="filteredOrders.length > itemsPerPage">
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="px-4 py-2 mx-1 bg-gray-200 rounded-md"
      >
        Previous
      </button>
      <button
        @click="currentPage++"
        :disabled="currentPage * itemsPerPage >= filteredOrders.length"
        class="px-4 py-2 mx-1 bg-gray-200 rounded-md"
      >
        Next
      </button>
    </div>

    <div v-if="showOrderDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-4 border-b flex justify-between items-center">
          <h2 class="text-lg font-semibold">Order Details - #{{ selectedOrder.id }}</h2>
          <button @click="showOrderDetailsModal = false" class="text-gray-500 hover:text-gray-700">
            <X class="h-5 w-5" />
          </button>
        </div>

        <div class="p-6">
          <p>User Name: {{ userNames[selectedOrder.user] || 'N/A' }}</p>
          <p>Total Price: ${{ parseFloat(selectedOrder.total_amount)?.toFixed(2) || 'N/A' }}</p>
          <p>Status: {{ selectedOrder.status }}</p>
          <p>Created At: {{ formatDate(selectedOrder.created_at) }}</p>
          <p>Updated At: {{ formatDate(selectedOrder.updated_at) }}</p>

          <div class="flex justify-end mt-4">
            <button
              @click="showOrderDetailsModal = false"
              class="bg-rose-600 text-white py-2 px-4 rounded-lg hover:bg-rose-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import {
  Search,
  Eye,
  Printer,
  Download,
  X,
  ShoppingBag,
} from 'lucide-vue-next';

export default {
  name: 'AdminOrders',
  components: {
    Search,
    Eye,
    Printer,
    Download,
    X,
    ShoppingBag,
  },
  setup() {
    const searchQuery = ref('');
    const selectedStatus = ref('');
    const dateRange = ref('all');
    const showOrderDetailsModal = ref(false);
    const selectedOrder = ref({});
    const orders = ref([]);
    const userNames = ref({});
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const fetchingUsers = ref(false); // Thêm trạng thái fetching

    const getToken = () => localStorage.getItem('access_token');
    const setAuthHeader = () => {
      const token = getToken();
      if (token) axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      else delete axios.defaults.headers.common['Authorization'];
    };

    const fetchUser = async (userId) => {
      setAuthHeader();
      console.log('Fetching user:', userId); // DEBUG
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/users/${userId}`);
        console.log('User data received:', response.data); // DEBUG
        userNames.value[userId] = response.data.fullname;
        console.log('userNames after update:', userNames.value); // DEBUG
      } catch (error) {
        console.error(`Error fetching user ${userId}:`, error);
        userNames.value[userId] = 'N/A';
      } finally {
        // Không cần thiết phải set fetchingUsers về false ở đây vì có thể có nhiều user đang được fetch
      }
    };

    const fetchOrders = async () => {
      setAuthHeader();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/orders`);
        orders.value = response.data;
        console.log('Orders data received:', orders.value); // DEBUG
        fetchingUsers.value = true; // Bắt đầu fetching users
        // Fetch user details for each order
        const userFetchPromises = orders.value.map(order => fetchUser(order.user));
        await Promise.all(userFetchPromises); // Đợi tất cả user được fetch xong
        fetchingUsers.value = false; // Kết thúc fetching users
      } catch (error) {
        console.error('Error fetching orders:', error);
        fetchingUsers.value = false;
      }
    };

    onMounted(fetchOrders);

    const filteredOrders = computed(() => {
      let result = [...orders.value];
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(order =>
          String(order.id).toLowerCase().includes(query) ||
          (userNames[order.user] && userNames[order.user].toLowerCase().includes(query))
        );
      }
      if (selectedStatus.value) {
        result = result.filter(order => order.status === selectedStatus.value);
      }
      if (dateRange.value !== 'all') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        yesterday.setHours(0, 0, 0, 0);
        yesterday.setMilliseconds(0);
        const thisWeekStart = new Date(today);
        thisWeekStart.setDate(thisWeekStart.getDate() - thisWeekStart.getDay());
        thisWeekStart.setHours(0, 0, 0, 0);
        thisWeekStart.setMilliseconds(0);
        const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);
        thisMonthStart.setHours(0, 0, 0, 0);
        thisMonthStart.setMilliseconds(0);
        result = result.filter(order => {
          const orderDate = new Date(order.created_at);
          orderDate.setHours(0, 0, 0, 0);
          orderDate.setMilliseconds(0);
          if (dateRange.value === 'today') return orderDate.getTime() === today.getTime();
          else if (dateRange.value === 'yesterday') return orderDate.getTime() === yesterday.getTime();
          else if (dateRange.value === 'week') return orderDate >= thisWeekStart;
          else if (dateRange.value === 'month') return orderDate >= thisMonthStart && orderDate < new Date(today.getFullYear(), today.getMonth() + 1, 1);
          return true;
        });
      }
      // Default sorting by created_at descending (vẫn giữ lại để hiển thị mới nhất trước)
      result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      return result;
    });

    const paginatedOrders = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      const end = start + itemsPerPage.value;
      return filteredOrders.value.slice(start, end);
    });

    const viewOrderDetails = (order) => {
      selectedOrder.value = order;
      showOrderDetailsModal.value = true;
    };

    const updateOrderStatus = async (orderId, status) => {
      setAuthHeader();
      try {
        await axios.put(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/orders/${orderId}`, { status });
        fetchOrders();
        if (selectedOrder.value.id === orderId) selectedOrder.value.status = status;
      } catch (error) {
        console.error('Error updating order status:', error);
      }
    };

    const printOrder = (orderId) => {
      console.log(`Printing order ${orderId}`);
      alert(`Printing order #${orderId}`);
    };

    const exportOrders = () => {
      console.log('Exporting orders');
      alert('Orders exported successfully');
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };

    watch(searchQuery, () => currentPage.value = 1);
    watch(selectedStatus, () => currentPage.value = 1);
    watch(dateRange, () => currentPage.value = 1);

    return {
      searchQuery,
      selectedStatus,
      dateRange,
      filteredOrders,
      paginatedOrders,
      showOrderDetailsModal,
      selectedOrder,
      viewOrderDetails,
      updateOrderStatus,
      printOrder,
      exportOrders,
      currentPage,
      itemsPerPage,
      formatDate,
      userNames,
      fetchingUsers, // Expose trạng thái fetching nếu cần hiển thị loading
    };
  },
};
</script>