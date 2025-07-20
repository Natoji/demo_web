<template>
    <div class="relative mt-4">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search..." 
        class="w-full px-4 py-2 pl-10 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
      >
      <Search class="absolute left-3 top-2.5 text-gray-500 h-5 w-5" />
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { Search } from 'lucide-vue-next'
  
  export default {
    name: 'SearchForm',
    components: {
      Search
    },
    setup() {
      const searchQuery = ref('')
      
      return {
        searchQuery
      }
    }
  }
  </script>