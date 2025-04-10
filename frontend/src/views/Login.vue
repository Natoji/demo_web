<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden mt-10">
    <div class="bg-rose-600 text-white py-4 px-6">
      <h2 class="text-xl font-bold">Login to Your Account</h2>
    </div>

    <form @submit.prevent="handleLogin" class="p-6">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div class="mb-4">
        <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
          required
        >
      </div>

      <div class="mb-6">
        <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
          required
        >
      </div>

      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center">
          <input type="checkbox" id="remember" class="h-4 w-4 text-rose-600 focus:ring-rose-500 border-gray-300 rounded">
          <label for="remember" class="ml-2 block text-gray-700">Remember me</label>
        </div>

        <a href="#" class="text-rose-600 hover:text-rose-800">Forgot password?</a>
      </div>

      <button
        type="submit"
        class="w-full bg-rose-600 text-white py-2 px-4 rounded-lg hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2"
        :disabled="loading"
      >
        <span v-if="loading">Loading...</span>
        <span v-else>Login</span>
      </button>

      <div class="mt-4 text-center">
        <p class="text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-rose-600 hover:text-rose-800">Register</router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'Login',
  emits: ['login-success'],
  setup(props, { emit }) {
    const email = ref(''); // Changed from phoneNumber
    const password = ref('');
    const error = ref('');
    const loading = ref(false);
    const router = useRouter();

    const handleLogin = async () => {
      loading.value = true;
      error.value = '';

      try {
        const response = await axios.post(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/auth/login/`, {
          email: email.value, // Using email here
          password: password.value,
        });

        const { refresh, access } = response.data;

        localStorage.setItem('refresh_token', refresh);
        localStorage.setItem('access_token', access);

        emit('login-success', response.data);

        router.push('/');

      } catch (err) {
        console.error('Login error:', err);
        if (err.response && err.response.data && err.response.data.message) {
          error.value = err.response.data.message;
        } else {
          error.value = 'Invalid email or password'; // Updated error message
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      email, // Using email here
      password,
      error,
      loading,
      handleLogin,
      router,
    };
  },
};
</script>