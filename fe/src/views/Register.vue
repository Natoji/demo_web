<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden mt-10">
    <div class="bg-orange-600 text-white py-4 px-6">
      <h2 class="text-xl font-bold">Create an Account</h2>
    </div>

    <form @submit.prevent="handleRegister" class="p-6">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ error }}
      </div>

      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
        {{ success }}
      </div>

      <div class="mb-4">
        <label for="fullname" class="block text-gray-700 font-medium mb-2">Full Name</label>
        <input
          type="text"
          id="fullname"
          v-model="fullname"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          required
        >
      </div>

      <div class="mb-4">
        <label for="email" class="block text-gray-700 font-medium mb-2">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          required
        >
      </div>

      <div class="mb-4">
        <label for="password" class="block text-gray-700 font-medium mb-2">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          required
        >
      </div>
      <div class="mb-6">
        <label for="confirmPassword" class="block text-gray-700 font-medium mb-2">
          Confirm Password
        </label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          required
        >
      </div>

      <div class="mb-6">
        <div class="flex items-center">
          <input
            type="checkbox"
            id="terms"
            v-model="agreeToTerms"
            class="h-4 w-4 text-orange-600 focus:ring-orange-500 border-gray-300 rounded"
            required
          >
          <label for="terms" class="ml-2 block text-gray-700">
            I agree to the
            <a href="#" class="text-orange-600 hover:text-orange-800">Terms and Conditions</a>
          </label>
        </div>
      </div>

      <button
        type="submit"
        class="w-full bg-orange-600 text-white py-2 px-4 rounded-lg hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
        :disabled="loading || !agreeToTerms"
      >
        <span v-if="loading">Loading...</span>
        <span v-else>Register</span>
      </button>

      <div class="mt-4 text-center">
        <p class="text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-orange-600 hover:text-orange-800">Login</router-link>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'Register',
  setup() {
    const router = useRouter();
    const fullname = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const agreeToTerms = ref(false);
    const error = ref('');
    const success = ref('');
    const loading = ref(false);

    const handleRegister = async () => {
      loading.value = true;
      error.value = '';
      success.value = '';

      try {
        // Validate form
        if (password.value !== confirmPassword.value) {
          error.value = 'Passwords do not match';
          return;
        }

        // API call to /api/auth/register/
        const response = await axios.post(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/auth/register/`, {
          email: email.value,
          fullname: fullname.value,
          password: password.value,
        });

        // Registration success
        success.value = 'Registration successful! Redirecting to login...';

        // **"Bắt" sự kiện thành công ở đây:**
        console.log('Registration API call successful:', response.data);
        // Gọi một hàm khác nếu cần
        // doSomethingAfterSuccess(response.data);

        // Redirect to login after a delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);

      } catch (err) {
        console.error('Registration error:', err);
        if (err.response && err.response.data) {
          error.value = err.response.data.message || 'Registration failed.';
        } else {
          error.value = 'An error occurred. Please try again.';
        }
      } finally {
        loading.value = false;
      }
    };

    // Ví dụ về một hàm bạn có thể gọi sau thành công
    // const doSomethingAfterSuccess = (userData) => {
    //   console.log('Performing additional action after successful registration:', userData);
    //   // Có thể lưu trữ token, hiển thị thông báo đặc biệt, v.v.
    // };

    return {
      router,
      fullname,
      email,
      password,
      confirmPassword,
      agreeToTerms,
      error,
      success,
      loading,
      handleRegister,
      // doSomethingAfterSuccess, // Nếu bạn định gọi hàm này
    };
  },
};
</script>