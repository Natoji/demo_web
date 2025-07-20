<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Manage Products</h1>
      <button
        @click="openAddProductModal"
        class="bg-rose-600 text-white py-2 px-4 rounded-lg hover:bg-rose-700 flex items-center"
      >
        <Plus class="h-5 w-5 mr-1" />
        Add Product
      </button>
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
              placeholder="Search products..."
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
            <Search class="absolute right-3 top-2.5 text-gray-500 h-5 w-5" />
          </div>
        </div>

        <div class="w-full md:w-48">
          <label for="category" class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select
            id="category"
            v-model="selectedCategory"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="w-full md:w-48">
          <label for="sort" class="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select
            id="sort"
            v-model="sortBy"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
          >
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="cat_Id">Category</option>
          </select>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="product in paginatedProducts" :key="product.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <img :src="product.img" :alt="product.name" class="w-10 h-10 object-cover rounded-md mr-3" />
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ product.name }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ product.description }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-rose-100 text-rose-800">
                  {{ getCategoryName(product.category) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${{ parseFloat(product.price).toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click="openEditProductModal(product)"
                  class="text-indigo-600 hover:text-indigo-900 mr-3"
                >
                  <Edit class="h-5 w-5" />
                </button>
                <button @click="deleteProduct(product.id)" class="text-red-600 hover:text-red-900">
                  <Trash2 class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredProducts.length === 0" class="text-center py-12">
        <Package class="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No products found</h3>
        <p class="text-gray-500">Try adjusting your search or filter to find what you're looking for.</p>
      </div>
    </div>

    <div class="flex justify-center mt-4">
      <button :disabled="currentPage === 1" @click="currentPage--" class="px-3 py-1 mx-1 border rounded-md">Previous</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++" class="px-3 py-1 mx-1 border rounded-md">Next</button>
    </div>

    <div v-if="showAddProductModal || showEditProductModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">{{ showEditProductModal ? 'Edit Product' : 'Add New Product' }}</h2>
        </div>

        <form @submit.prevent="showEditProductModal ? updateProduct() : addProduct()" class="p-4">
          <div class="mb-4">
            <label for="productName" class="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
            <input
              type="text"
              id="productName"
              v-model="currentProduct.name"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>

          <div class="mb-4">
            <label for="productDescription" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              id="productDescription"
              v-model="currentProduct.description"
              rows="3"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
            ></textarea>
          </div>

          <div class="mb-4">
            <label for="productPrice" class="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
            <input
              type="number"
              id="productPrice"
              v-model="currentProduct.price"
              step="0.01"
              min="0"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>

          <div class="mb-4">
            <label for="productCategory" class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              id="productCategory"
              v-model="currentProduct.category"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            >
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label for="productImage" class="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
            <input
              type="text"
              id="productImage"
              v-model="currentProduct.img"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button
              type="button"
              @click="closeProductModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 bg-rose-600 text-white rounded-md hover:bg-rose-700">
              {{ showEditProductModal ? 'Update' : 'Add' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">Confirm Delete</h2>
        </div>

        <div class="p-4">
          <p class="text-gray-700 mb-4">Are you sure you want to delete this product? This action cannot be undone.</p>

          <div class="flex justify-end gap-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { Search, Plus, Edit, Trash2, Package } from 'lucide-vue-next';

export default {
  name: 'AdminProducts',
  components: {
    Search,
    Plus,
    Edit,
    Trash2,
    Package,
  },
  setup() {
    const searchQuery = ref('');
    const selectedCategory = ref('');
    const sortBy = ref('name');
    const showAddProductModal = ref(false);
    const showEditProductModal = ref(false);
    const showDeleteModal = ref(false);
    const productToDeleteId = ref(null);
    const products = ref([]);
    const categories = ref([]);
    const currentPage = ref(1);
    const itemsPerPage = ref(10);

    const currentProduct = ref({
      id: null,
      name: '',
      description: '',
      price: 0,
      stock: 0,
      brand: 1,
      img: '/placeholder.svg?height=300&width=400',
      category: 1,
    });

    const filteredProducts = computed(() => {
      let result = [...products.value];
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(product => {
          const name = product.name ? product.name.toLowerCase() : '';
          const desc = product.description ? product.description.toLowerCase() : '';
          return name.includes(query) || desc.includes(query);
        });
      }
      if (selectedCategory.value) {
        result = result.filter(product => product.category === parseInt(selectedCategory.value));
      }
      result.sort((a, b) => {
        if (sortBy.value === 'name') return a.name.localeCompare(b.name);
        if (sortBy.value === 'price') return parseFloat(a.price) - parseFloat(b.price);
        if (sortBy.value === 'cat_Id') return a.category - b.category;
        return 0;
      });
      return result;
    });

    const paginatedProducts = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      return filteredProducts.value.slice(start, start + itemsPerPage.value);
    });

    const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage.value));

    const getCategoryName = (id) => {
      const cat = categories.value.find(c => c.id === id);
      return cat ? cat.name : '';
    };

    const resetCurrentProduct = () => {
      currentProduct.value = {
        id: null,
        name: '',
        description: '',
        price: 0,
        stock: 0,
        brand: 1,
        img: '/placeholder.svg?height=300&width=400',
        category: 1,
      };
    };

    const openAddProductModal = () => {
      resetCurrentProduct();
      showAddProductModal.value = true;
      showEditProductModal.value = false;
    };

    const openEditProductModal = async (product) => {
      try {
        const token = localStorage.getItem('access_token');
        const res = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/products/${product.id}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        currentProduct.value = { ...res.data, category: res.data.category };
        showEditProductModal.value = true;
      } catch (err) {
        console.error('Edit product fetch error:', err);
      }
    };

    const closeProductModal = () => {
      showAddProductModal.value = false;
      showEditProductModal.value = false;
      resetCurrentProduct();
    };

    const addProduct = async () => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/products/`, {
          name: currentProduct.value.name,
          description: currentProduct.value.description,
          price: parseFloat(currentProduct.value.price),
          stock: 0,
          brand: 1,
          category: parseInt(currentProduct.value.category),
          img: currentProduct.value.img,
        }, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
        await fetchProducts();
        closeProductModal();
      } catch (err) {
        console.error('Add product error:', err);
      }
    };

    const updateProduct = async () => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/products/${currentProduct.value.id}/`, {
          name: currentProduct.value.name,
          description: currentProduct.value.description,
          price: parseFloat(currentProduct.value.price),
          stock: 0,
          brand: 1,
          category: parseInt(currentProduct.value.category),
          img: currentProduct.value.img,
        }, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
        await fetchProducts();
        closeProductModal();
      } catch (err) {
        console.error('Update product error:', err);
      }
    };

    const deleteProduct = (id) => {
      productToDeleteId.value = id;
      showDeleteModal.value = true;
    };

    const confirmDelete = async () => {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/products/${productToDeleteId.value}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        await fetchProducts();
        showDeleteModal.value = false;
        productToDeleteId.value = null;
      } catch (err) {
        console.error('Delete product error:', err);
      }
    };

    const fetchProducts = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const res = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/products/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        products.value = res.data;
      } catch (err) {
        console.error('Fetch products error:', err);
      }
    };

    const fetchCategories = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const res = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        categories.value = res.data;
      } catch (err) {
        console.error('Fetch categories error:', err);
      }
    };

    onMounted(() => {
      fetchProducts();
      fetchCategories();
    });

    return {
      searchQuery,
      selectedCategory,
      sortBy,
      showAddProductModal,
      showEditProductModal,
      showDeleteModal,
      productToDeleteId,
      products,
      categories,
      currentPage,
      itemsPerPage,
      currentProduct,
      filteredProducts,
      paginatedProducts,
      totalPages,
      getCategoryName,
      openAddProductModal,
      openEditProductModal,
      closeProductModal,
      addProduct,
      updateProduct,
      deleteProduct,
      confirmDelete,
    };
  },
};
</script>

<style scoped>
/* Optional: custom styles */
</style>