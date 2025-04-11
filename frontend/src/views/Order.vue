<template>
    <div class="orders-container">
      <div class="orders-header">
        <h1>My Orders</h1>
        <div class="filters">
          <select v-model="statusFilter" class="filter-select">
            <option value="all">All Orders</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <select v-model="sortBy" class="filter-select">
            <option value="date-desc">Newest First</option>
            <option value="date-asc">Oldest First</option>
            <option value="total-desc">Highest Amount</option>
            <option value="total-asc">Lowest Amount</option>
          </select>
        </div>
      </div>
  
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading your orders...</p>
      </div>
  
      <div v-else-if="error" class="error-container">
        <p class="error-message">{{ error }}</p>
        <button @click="fetchOrders" class="retry-btn">Try Again</button>
      </div>
  
      <div v-else-if="filteredOrders.length === 0" class="empty-state">
        <div class="empty-icon">
          <ShoppingBag class="icon" />
        </div>
        <h2>No orders found</h2>
        <p v-if="statusFilter !== 'all'">Try changing your filter or check back later.</p>
        <p v-else>You haven't placed any orders yet.</p>
        <router-link to="/" class="shop-now-btn">Shop Now</router-link>
      </div>
  
      <div v-else class="orders-list">
        <div v-for="order in paginatedOrders" :key="order.id" class="order-card">
          <div class="order-header">
            <div>
              <span class="order-number">Order #{{ order.id }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="order-status" :class="'status-' + order.status.toLowerCase()">
              {{ capitalizeFirstLetter(order.status) }}
            </div>
          </div>
  
          <div class="order-info">
            <div class="payment-method">
              <span class="payment-label">Payment Method:</span>
              <span class="payment-value">{{ formatPaymentMethod(order.payment_method) }}</span>
            </div>
          </div>
  
          <div class="order-items">
            <div v-for="(item, index) in order.OrderDetails" :key="index" class="order-item">
              <div class="item-image">
                <img :src="item.MenuItem.img" :alt="item.MenuItem.name">
              </div>
              <div class="item-details">
                <h3>{{ item.MenuItem.name }}</h3>
                <div class="item-quantity-price">
                  <span>Qty: {{ item.quantity }}</span>
                  <span>${{ formatPrice(item.price) }}</span>
                </div>
              </div>
            </div>
          </div>
  
          <div class="order-footer">
            <div class="order-summary">
              <div class="summary-row">
                <span>Subtotal:</span>
                <span>${{ formatPrice(calculateSubtotal(order)) }}</span>
              </div>
              <div class="summary-row">
                <span>Shipping:</span>
                <span>${{ formatPrice(order.shipping_fee) }}</span>
              </div>
              <div class="summary-row">
                <span>Tax:</span>
                <span>${{ formatPrice(order.tax) }}</span>
              </div>
              <div class="summary-row total">
                <span>Total:</span>
                <span>${{ formatPrice(order.total_price) }}</span>
              </div>
            </div>
            
            <div class="order-actions">
              <button class="action-btn details-btn" @click="viewOrderDetails(order)">
                View Details
              </button>
              <button 
                v-if="order.status.toLowerCase() === 'delivered'" 
                class="action-btn review-btn"
                @click="leaveReview(order.id)"
              >
                Leave Review
              </button>
              <button 
                v-if="canCancelOrder(order)" 
                class="action-btn cancel-btn"
                @click="cancelOrder(order.id)"
              >
                Cancel Order
              </button>
            </div>
          </div>
        </div>
  
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button 
            :disabled="currentPage === 1" 
            @click="currentPage--" 
            class="pagination-btn"
          >
            Previous
          </button>
          <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            :disabled="currentPage === totalPages" 
            @click="currentPage++" 
            class="pagination-btn"
          >
            Next
          </button>
        </div>
      </div>

      <!-- Order Details Modal -->
      <div v-if="showOrderModal" class="modal-overlay" @click="closeOrderModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Order Details #{{ selectedOrder?.id }}</h2>
            <button class="close-btn" @click="closeOrderModal">&times;</button>
          </div>
          
          <div class="modal-body">
            <div class="order-info-section">
              <h3>Order Information</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">Order Date:</span>
                  <span class="info-value">{{ formatDate(selectedOrder?.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Status:</span>
                  <span class="info-value status-badge" :class="'status-' + selectedOrder?.status.toLowerCase()">
                    {{ capitalizeFirstLetter(selectedOrder?.status) }}
                  </span>
                </div>
                <div class="info-item">
                  <span class="info-label">Payment Method:</span>
                  <span class="info-value">{{ formatPaymentMethod(selectedOrder?.payment_method) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Shipping Address:</span>
                  <span class="info-value">{{ selectedOrder?.shipping_address || 'Not specified' }}</span>
                </div>
              </div>
            </div>
            
            <div class="order-items-section">
              <h3>Order Items</h3>
              <div class="order-items-list">
                <div v-for="(item, index) in selectedOrder?.OrderDetails" :key="index" class="order-item-detail">
                  <div class="item-image">
                    <img :src="item.MenuItem.img" :alt="item.MenuItem.name">
                  </div>
                  <div class="item-info">
                    <h4>{{ item.MenuItem.name }}</h4>
                    <p class="item-description">{{ item.MenuItem.description || 'No description available' }}</p>
                    <div class="item-price-qty">
                      <span class="item-price">${{ formatPrice(item.price) }}</span>
                      <span class="item-quantity">Quantity: {{ item.quantity }}</span>
                      <span class="item-subtotal">Subtotal: ${{ formatPrice(item.price * item.quantity) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="order-summary-section">
              <h3>Order Summary</h3>
              <div class="summary-details">
                <div class="summary-row">
                  <span>Subtotal:</span>
                  <span>${{ formatPrice(calculateSubtotal(selectedOrder)) }}</span>
                </div>
                <div class="summary-row">
                  <span>Shipping Fee:</span>
                  <span>${{ formatPrice(selectedOrder?.shipping_fee) }}</span>
                </div>
                <div class="summary-row">
                  <span>Tax:</span>
                  <span>${{ formatPrice(selectedOrder?.tax) }}</span>
                </div>
                <div class="summary-row total">
                  <span>Total:</span>
                  <span>${{ formatPrice(selectedOrder?.total_price) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="modal-btn close-modal-btn" @click="closeOrderModal">Close</button>
            <button 
              v-if="canCancelOrder(selectedOrder)" 
              class="modal-btn cancel-order-btn"
              @click="cancelOrderFromModal(selectedOrder.id)"
            >
              Cancel Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import { ref, computed, onMounted, watch } from 'vue';
  import { ShoppingBag } from 'lucide-vue-next';
  import { orderAPI, paymentAPI } from '../services/api';
  import { useRoute } from 'vue-router'; // Import useRoute

  export default {
    name: 'OrderPage',
    components: {
      ShoppingBag
    },
    setup() {
      const orders = ref([]);
      const loading = ref(true);
      const error = ref(null);
      const statusFilter = ref('all');
      const sortBy = ref('date-desc');
      const currentPage = ref(1);
      const ordersPerPage = 3;

      // Modal state
      const showOrderModal = ref(false);
      const selectedOrder = ref(null);

      // Lấy thông tin user từ localStorage
      const user = JSON.parse(localStorage.getItem('user'));
      if (!user) {
        window.location.href = '/login';
        return;
      }

      // Get route information
      const route = useRoute();

      // Check for successful payment query parameter on mount
      onMounted(() => {
        fetchOrders();
        if (route.query.vnp_TransactionStatus === '00') {
          alert('Thanh toán thành công!');
          // Optionally clear the query parameters from the URL
          // history.replaceState({}, document.title, window.location.pathname);
        } else if (route.query.vnp_TransactionStatus) {
          alert('Thanh toán không thành công hoặc bị hủy.');
          console.log('Payment Return Query:', route.query);
          // Optionally log or handle the failure scenario
        }
      });

      // Fetch orders from API
      const fetchOrders = async () => {
        try {
          loading.value = true;
          error.value = null;
          const response = await orderAPI.getOrderByUserID(user.id);
          console.log('API Response:', response);

          // Kiểm tra response và gán dữ liệu
          if (response && Array.isArray(response)) {
            orders.value = response;
          } else if (response && response.data && Array.isArray(response.data)) {
            orders.value = response.data;
          } else {
            orders.value = [];
            console.warn('No orders found or invalid response format');
          }

          // Fetch order details and payment info for each order
          for (let order of orders.value) {
            try {
              // Fetch order details
              const detailsResponse = await orderAPI.getOrderDetails(order.id);
              if (detailsResponse && detailsResponse.data) {
                order.OrderDetails = detailsResponse.data;
              }

              // Fetch payment info
              const paymentResponse = await paymentAPI.getPaymentByOrderId(order.id);
              if (paymentResponse && paymentResponse.data) {
                order.payment_method = paymentResponse.data.method;
                order.payment_status = paymentResponse.data.status;
              }

              // Fetch full order details
              const orderResponse = await orderAPI.getOrderById(order.id);
              if (orderResponse && orderResponse.data) {
                order.shipping_address = orderResponse.data.shipping_address;
                order.full_name = orderResponse.data.full_name;
                order.phone_number = orderResponse.data.phone_number;
                order.email = orderResponse.data.email;
              }
            } catch (err) {
              console.error('Error fetching order details or payment:', err);
            }
          }
        } catch (err) {
          console.error('Error fetching orders:', err);
          error.value = 'Không thể tải danh sách đơn hàng. Vui lòng thử lại sau.';
          orders.value = [];
        } finally {
          loading.value = false;
        }
      };

      // Filter and sort orders
      const filteredOrders = computed(() => {
        let result = [...orders.value];

        // Apply status filter
        if (statusFilter.value !== 'all') {
          result = result.filter(order => order.status.toLowerCase() === statusFilter.value);
        }

        // Apply sorting
        switch (sortBy.value) {
          case 'date-desc':
            result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
          case 'date-asc':
            result.sort((a, b) => new Date(a.created_at) - new Date(a.created_at));
            break;
          case 'total-desc':
            result.sort((a, b) => b.total_price - a.total_price);
            break;
          case 'total-asc':
            result.sort((a, b) => a.total_price - b.total_price);
            break;
        }

        return result;
      });

      // Pagination
      const totalPages = computed(() => {
        return Math.ceil(filteredOrders.value.length / ordersPerPage);
      });

      const paginatedOrders = computed(() => {
        const startIndex = (currentPage.value - 1) * ordersPerPage;
        const endIndex = startIndex + ordersPerPage;
        return filteredOrders.value.slice(startIndex, endIndex);
      });

      // Reset to page 1 when filters change
      const resetPagination = () => {
        currentPage.value = 1;
      };

      // Watch for filter changes
      watch([statusFilter, sortBy], () => {
        resetPagination();
      });

      // Helper functions
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      };

      const formatPrice = (price) => {
        const numericPrice = Number(price);
        if (isNaN(numericPrice)) return '0.00';
        return numericPrice.toFixed(2);
      };

      const formatPaymentMethod = (method) => {
        if (!method) return 'Not specified';

        switch (method.toLowerCase()) {
          case 'vnpay':
            return 'VNPay';
          case 'cashondelivery':
            return 'Cash on Delivery';
          default:
            return capitalizeFirstLetter(method);
        }
      };

      const calculateSubtotal = (order) => {
        if (!order || !order.OrderDetails) return 0;
        return order.OrderDetails.reduce((sum, item) => {
          const price = Number(item.price) || 0;
          const quantity = Number(item.quantity) || 0;
          return sum + (price * quantity);
        }, 0);
      };

      const capitalizeFirstLetter = (string) => {
        if (!string) return '';
        return string.charAt(0).toUpperCase() + string.slice(1);
      };

      const canCancelOrder = (order) => {
        if (!order) return false;
        return ['pending', 'processing'].includes(order.status.toLowerCase());
      };

      // Modal functions
      const viewOrderDetails = async (order) => {
        selectedOrder.value = order;

        // Fetch payment info if not already loaded
        if (!order.payment_method) {
          try {
            const paymentResponse = await paymentAPI.getPaymentByOrderId(order.id);
            if (paymentResponse && paymentResponse.data) {
              selectedOrder.value.payment_method = paymentResponse.data.method;
              selectedOrder.value.payment_status = paymentResponse.data.status;
            }
          } catch (err) {
            console.error('Error fetching payment info:', err);
          }
        }

        // Fetch full order details if needed
        if (!order.shipping_address) {
          try {
            const orderResponse = await orderAPI.getOrderById(order.id);
            if (orderResponse && orderResponse.data) {
              selectedOrder.value.shipping_address = orderResponse.data.shipping_address;
              selectedOrder.value.full_name = orderResponse.data.full_name;
              selectedOrder.value.phone_number = orderResponse.data.phone_number;
              selectedOrder.value.email = orderResponse.data.email;
            }
          } catch (err) {
            console.error('Error fetching order details:', err);
          }
        }

        showOrderModal.value = true;
      };

      const closeOrderModal = () => {
        showOrderModal.value = false;
        selectedOrder.value = null;
      };

      const cancelOrderFromModal = async (orderId) => {
        if (confirm('Bạn có chắc chắn muốn hủy đơn hàng này?')) {
          try {
            await orderAPI.cancelOrder(orderId);
            // Refresh orders after cancellation
            fetchOrders();
            // Close modal
            closeOrderModal();
          } catch (err) {
            console.error('Error cancelling order:', err);
            alert('Không thể hủy đơn hàng. Vui lòng thử lại sau.');
          }
        }
      };

      const leaveReview = (orderId) => {
        // Navigate to review page
        window.location.href = `/review/${orderId}`;
      };

      const cancelOrder = async (orderId) => {
        if (confirm('Bạn có chắc chắn muốn hủy đơn hàng này?')) {
          try {
            await orderAPI.cancelOrder(orderId);
            // Refresh orders after cancellation
            fetchOrders();
          } catch (err) {
            console.error('Error cancelling order:', err);
            alert('Không thể hủy đơn hàng. Vui lòng thử lại sau.');
          }
        }
      };

      return {
        orders,
        loading,
        error,
        statusFilter,
        sortBy,
        currentPage,
        filteredOrders,
        paginatedOrders,
        totalPages,
        formatDate,
        formatPrice,
        formatPaymentMethod,
        calculateSubtotal,
        capitalizeFirstLetter,
        canCancelOrder,
        viewOrderDetails,
        leaveReview,
        cancelOrder,
        fetchOrders,
        // Modal state
        showOrderModal,
        selectedOrder,
        closeOrderModal,
        cancelOrderFromModal
      };
    }
  }
</script>
  <style scoped>
  .orders-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .orders-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .orders-header h1 {
    font-size: 1.8rem;
    font-weight: 600;
    color: #333;
    margin: 0;
  }
  
  .filters {
    display: flex;
    gap: 0.75rem;
  }
  
  .filter-select {
    padding: 0.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.375rem;
    background-color: white;
    font-size: 0.875rem;
    color: #4b5563;
    cursor: pointer;
  }
  
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 0;
  }
  
  .loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 4px solid #3b82f6;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .error-container {
    text-align: center;
    padding: 4rem 0;
    color: #ef4444;
  }
  
  .error-message {
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }
  
  .retry-btn {
    padding: 0.5rem 1.5rem;
    background-color: #3b82f6;
    color: white;
    border-radius: 0.375rem;
    border: none;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
  }
  
  .retry-btn:hover {
    background-color: #2563eb;
  }
  
  .empty-state {
    text-align: center;
    padding: 4rem 0;
    color: #6b7280;
  }
  
  .empty-icon {
    margin-bottom: 1rem;
  }
  
  .empty-icon .icon {
    width: 64px;
    height: 64px;
    color: #9ca3af;
  }
  
  .empty-state h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: #4b5563;
  }
  
  .shop-now-btn {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.5rem 1.5rem;
    background-color: #3b82f6;
    color: white;
    border-radius: 0.375rem;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.2s;
  }
  
  .shop-now-btn:hover {
    background-color: #2563eb;
  }
  
  .orders-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .order-card {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .order-number {
    font-weight: 600;
    color: #111827;
    margin-right: 1rem;
  }
  
  .order-date {
    color: #6b7280;
    font-size: 0.875rem;
  }
  
  .order-status {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .status-pending {
    background-color: #fef3c7;
    color: #92400e;
  }
  
  .status-processing {
    background-color: #e0f2fe;
    color: #0369a1;
  }
  
  .status-shipped {
    background-color: #dbeafe;
    color: #1e40af;
  }
  
  .status-delivered {
    background-color: #d1fae5;
    color: #065f46;
  }
  
  .status-cancelled {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .order-info {
    padding: 0.75rem 1rem;
    background-color: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .payment-method {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .payment-label {
    font-size: 0.875rem;
    color: #6b7280;
  }
  
  .payment-value {
    font-size: 0.875rem;
    font-weight: 500;
    color: #111827;
  }
  
  .order-items {
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .order-item {
    display: flex;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .order-item:last-child {
    border-bottom: none;
  }
  
  .item-image {
    width: 80px;
    height: 80px;
    flex-shrink: 0;
  }
  
  .item-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 0.25rem;
  }
  
  .item-details {
    flex: 1;
  }
  
  .item-details h3 {
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 0.25rem 0;
    color: #111827;
  }
  
  .item-quantity-price {
    display: flex;
    justify-content: space-between;
    color: #4b5563;
    font-size: 0.875rem;
  }
  
  .order-footer {
    padding: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: space-between;
  }
  
  .order-summary {
    flex: 1;
    min-width: 200px;
  }
  
  .summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    color: #4b5563;
  }
  
  .summary-row.total {
    font-weight: 600;
    color: #111827;
    font-size: 1rem;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #e5e7eb;
  }
  
  .order-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: flex-end;
  }
  
  .action-btn {
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: background-color 0.2s;
  }
  
  .details-btn {
    background-color: #f3f4f6;
    color: #4b5563;
  }
  
  .details-btn:hover {
    background-color: #e5e7eb;
  }
  
  .review-btn {
    background-color: #eff6ff;
    color: #1d4ed8;
  }
  
  .review-btn:hover {
    background-color: #dbeafe;
  }
  
  .cancel-btn {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .cancel-btn:hover {
    background-color: #fecaca;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 2rem;
    gap: 1rem;
  }
  
  .pagination-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    background-color: white;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    color: #4b5563;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .pagination-btn:hover:not(:disabled) {
    background-color: #f3f4f6;
  }
  
  .pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .page-info {
    font-size: 0.875rem;
    color: #6b7280;
  }
  
  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1rem;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 0.5rem;
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .modal-header h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin: 0;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #6b7280;
    cursor: pointer;
    padding: 0.25rem;
    line-height: 1;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .order-info-section,
  .order-items-section,
  .order-summary-section {
    margin-bottom: 2rem;
  }
  
  .order-info-section h3,
  .order-items-section h3,
  .order-summary-section h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 1rem 0;
  }
  
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .info-item {
    display: flex;
    flex-direction: column;
  }
  
  .info-label {
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 0.25rem;
  }
  
  .info-value {
    font-size: 1rem;
    color: #111827;
    font-weight: 500;
  }
  
  .status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    width: fit-content;
  }
  
  .order-items-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .order-item-detail {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
  }
  
  .item-info {
    flex: 1;
  }
  
  .item-info h4 {
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 0.5rem 0;
    color: #111827;
  }
  
  .item-description {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0 0 0.75rem 0;
  }
  
  .item-price-qty {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.875rem;
    color: #4b5563;
  }
  
  .item-price {
    font-weight: 500;
  }
  
  .item-subtotal {
    margin-left: auto;
    font-weight: 500;
  }
  
  .summary-details {
    border: 1px solid #e5e7eb;
    border-radius: 0.375rem;
    padding: 1rem;
  }
  
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1rem 1.5rem;
    border-top: 1px solid #e5e7eb;
  }
  
  .modal-btn {
    padding: 0.5rem 1.5rem;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: background-color 0.2s;
  }
  
  .close-modal-btn {
    background-color: #f3f4f6;
    color: #4b5563;
  }
  
  .close-modal-btn:hover {
    background-color: #e5e7eb;
  }
  
  .cancel-order-btn {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .cancel-order-btn:hover {
    background-color: #fecaca;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .orders-header {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .order-footer {
      flex-direction: column;
    }
    
    .order-actions {
      width: 100%;
    }
    
    .action-btn {
      flex: 1;
      text-align: center;
    }
    
    .info-grid {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 640px) {
    .filters {
      width: 100%;
      flex-direction: column;
    }
    
    .filter-select {
      width: 100%;
    }
    
    .order-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
    
    .order-status {
      align-self: flex-start;
    }
    
    .modal-content {
      padding: 0;
    }
    
    .modal-body {
      padding: 1rem;
    }
    
    .order-item-detail {
      flex-direction: column;
    }
    
    .item-image {
      width: 100%;
      height: auto;
      max-height: 200px;
    }
  }
  </style>