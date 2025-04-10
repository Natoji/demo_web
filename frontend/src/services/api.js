import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const categoryAPI = {
  getAll: () => api.get('/categories/all'),
  getById: (id) => api.get(`/categories/get/${id}`),
};

export const menuItemAPI = {
  getAll: () => api.get('/menu-items/all'),
  getById: (id) => api.get(`/menu-items/get/${id}`),
};

export const userAPI = {
  getProfile: (id) => api.get(`/users/get/${id}`),
  updateProfile: (id, data) => api.put(`/users/update/${id}`, data),
  changePassword: (id, data) => api.put(`/users/change-password/${id}`, data),
  deleteAccount: (id) => api.delete(`/users/delete/${id}`),
};

export const cartAPI = {
  getCart: (userId) => api.get(`/carts/${userId}`),
  addToCart: (userId, data) => api.post(`/carts/${userId}/add`, data),
  updateCartItem: (userId, itemId, data) => api.put(`/carts/${userId}/items/${itemId}`, data),
  removeFromCart: (userId, itemId) => api.delete(`/carts/${userId}/items/${itemId}`),
  clearCart: (userId) => api.delete(`/carts/${userId}/clear`),
  getCartCount: (userId) => api.get(`/carts/${userId}/count`),
};

export const orderAPI = {
  getOrders: (userId) => api.get(`/orders/user/${userId}`),
  getOrderById: (orderId) => api.get(`/orders/${orderId}`),
  createOrder: (data) => api.post('/orders/create', data),
  updateOrder: (orderId, data) => api.put(`/orders/update/${orderId}`, data),
  cancelOrder: (orderId) => api.put(`/orders/cancel/${orderId}`),
  getOrderDetails: (orderId) => api.get(`/order-details/order/${orderId}`),
  getOrderByUserID: (userId) => api.get(`/orders/user/${userId}`),
  createOrderDetails: (data) => api.post('/order-details/create', data),
};

export const paymentAPI = {
  createPayment: (data) => api.post('/payments/create', data),
  getPaymentByOrderId: (orderId) => api.get(`/payments/order/${orderId}`),
  updatePayment: (id, data) => api.put(`/payments/update/${id}`, data),
  deletePayment: (id) => api.delete(`/payments/delete/${id}`),
  //thanh toan vn pay
  initiateVNPAY: (paymentData) => api.post('/payments/vnpay_initiate', paymentData),
};

export default api; 