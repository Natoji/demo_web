<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Manage Categories</h1>
      <button @click="openAddCategoryModal"
        class="bg-orange-600 text-white py-2 px-4 rounded-lg hover:bg-orange-700 flex items-center">
        <Plus class="h-5 w-5 mr-1" />
        Add Category
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-grow">
          <label for="search" class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <div class="relative">
            <input type="text" id="search" v-model="searchQuery" placeholder="Search categories..."
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500">
            <Search class="absolute right-3 top-2.5 text-gray-500 h-5 w-5" />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th @click="sortTable('name')"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                Category
                <span v-if="sortColumn === 'name'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th @click="sortTable('description')"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                Description
                <span v-if="sortColumn === 'description'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Products</th>
              <th @click="sortTable('id')"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                ID
                <span v-if="sortColumn === 'id'">{{ sortDirection === 'asc' ? '▲' : '▼' }}</span>
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="category in paginatedCategories" :key="category.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-md bg-gray-200 flex items-center justify-center overflow-hidden">
                    <img v-if="category.image" :src="category.image" :alt="category.name"
                      class="h-full w-full object-cover">
                    <Utensils v-else class="h-5 w-5 text-gray-500" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ category.name }}</div>
                    <div class="text-xs text-gray-500">ID: {{ category.id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                <div class="max-w-xs truncate">{{ category.description || 'No description' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ category.productCount }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ category.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="openEditCategoryModal(category)" class="text-indigo-600 hover:text-indigo-900 mr-3">
                  <Edit class="h-5 w-5" />
                </button>
                <button @click="confirmDeleteCategory(category.id)" class="text-red-600 hover:text-red-900"
                  :disabled="category.productCount > 0"
                  :class="{ 'opacity-50 cursor-not-allowed': category.productCount > 0 }"
                  :title="category.productCount > 0 ? 'Cannot delete category with products' : 'Delete Category'">
                  <Trash2 class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredCategories.length === 0" class="text-center py-12">
        <Utensils class="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No categories found</h3>
        <p class="text-gray-500">Try adjusting your search or filter to find what you're looking for.</p>
      </div>
    </div>

    <div class="flex justify-center mt-4" v-if="totalPages > 1">
      <button :disabled="currentPage === 1" @click="currentPage--"
        class="px-3 py-1 mx-1 border rounded-md">Previous</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++"
        class="px-3 py-1 mx-1 border rounded-md">Next</button>
    </div>

    <div v-if="showAddCategoryModal || showEditCategoryModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">{{ showEditCategoryModal ? 'Edit Category' : 'Add New Category' }}</h2>
        </div>

        <form @submit.prevent="showEditCategoryModal ? updateCategory() : addCategory()" class="p-4">
          <div class="mb-4">
            <label for="categoryName" class="block text-sm font-medium text-gray-700 mb-1">Category Name</label>
            <input type="text" id="categoryName" v-model="currentCategory.name"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500" required>
          </div>

          <div class="mb-4">
            <label for="categoryDescription" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea id="categoryDescription" v-model="currentCategory.description" rows="3"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"></textarea>
          </div>

          <div class="mb-4">
            <label for="categoryImage" class="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
            <input type="text" id="categoryImage" v-model="currentCategory.image"
              placeholder="https://example.com/image.jpg"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500">
            <p class="mt-1 text-xs text-gray-500">Leave empty to use default icon</p>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="closeCategoryModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700">
              {{ showEditCategoryModal ? 'Update' : 'Add' }}
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
          <p class="text-gray-700 mb-4">Are you sure you want to delete this category? This action cannot be undone.</p>

          <div class="flex justify-end gap-3">
            <button @click="closeDeleteModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
              Cancel
            </button>
            <button @click="confirmDeleteCategoryAction"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700">
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
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Utensils,
} from 'lucide-vue-next';

export default {
  name: 'AdminCategories',
  components: {
    Search,
    Plus,
    Edit,
    Trash2,
    Utensils,
  },
  setup() {
    const searchQuery = ref('');
    const categories = ref([]);
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const sortColumn = ref('id');
    const sortDirection = ref('asc');
    const showAddCategoryModal = ref(false);
    const showEditCategoryModal = ref(false);
    const showDeleteModal = ref(false);
    const categoryToDeleteId = ref(null);

    const currentCategory = ref({
      id: null,
      name: '',
      description: '',
      image: '',
    });

    const getToken = () => localStorage.getItem('access_token');
    const setAuthHeader = () => {
      const token = getToken();
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      } else {
        delete axios.defaults.headers.common['Authorization'];
      }
    };

    const filteredCategories = computed(() => {
      let result = [...categories.value];
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(category =>
          category.name.toLowerCase().includes(query) ||
          (category.description && category.description.toLowerCase().includes(query))
        );
      }
      result.sort((a, b) => {
        const valueA = a[sortColumn.value];
        const valueB = b[sortColumn.value];
        if (typeof valueA === 'string' && typeof valueB === 'string') {
          return sortDirection.value === 'asc' ? valueA.localeCompare(valueB) : valueB.localeCompare(valueA);
        } else {
          return sortDirection.value === 'asc' ? (valueA > valueB ? 1 : -1) : (valueA < valueB ? 1 : -1);
        }
      });
      return result;
    });

    const paginatedCategories = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      const end = start + itemsPerPage.value;
      return filteredCategories.value.slice(start, end);
    });

    const totalPages = computed(() => {
      return Math.ceil(filteredCategories.value.length / itemsPerPage.value);
    });

    const resetCurrentCategory = () => {
      currentCategory.value = { id: null, name: '', description: '', image: '' };
    };

    const openAddCategoryModal = () => {
      resetCurrentCategory();
      showAddCategoryModal.value = true;
      showEditCategoryModal.value = false;
    };

    const openEditCategoryModal = async (category) => {
      setAuthHeader();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/${category.id}/`);
        const apiCategory = response.data;
        currentCategory.value = { ...apiCategory };
        showEditCategoryModal.value = true;
        showAddCategoryModal.value = false;
      } catch (error) {
        console.error('Error fetching category for edit:', error);
      }
    };

    const closeCategoryModal = () => {
      showAddCategoryModal.value = false;
      showEditCategoryModal.value = false;
      resetCurrentCategory();
    };

    const addCategory = async () => {
      setAuthHeader();
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/`, {
          name: currentCategory.value.name,
          description: currentCategory.value.description,
          image: currentCategory.value.image,
        });
        categories.value.push(response.data);
        closeCategoryModal();
      } catch (error) {
        console.error('Error adding category:', error);
      } finally {
        await fetchCategories();
      }
    };

    const updateCategory = async () => {
      try {
        await axios.put(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/${currentCategory.value.id}/`
        , {
          name: currentCategory.value.name,
          description: currentCategory.value.description,
          image: currentCategory.value.image,
        });
        await fetchCategories();
        closeCategoryModal();
      } catch (error) {
        console.error('Error updating category:', error);
      }
    };

    const confirmDeleteCategory = (id) => {
      categoryToDeleteId.value = id;
      showDeleteModal.value = true;
    };

    const closeDeleteModal = () => {
      showDeleteModal.value = false;
      categoryToDeleteId.value = null;
    };

    const confirmDeleteCategoryAction = async () => {
      setAuthHeader();
      try {
        await axios.delete(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/${categoryToDeleteId.value}/`);
        categories.value = categories.value.filter(cat => cat.id !== categoryToDeleteId.value);
        closeDeleteModal();
      } catch (error) {
        console.error('Error deleting category:', error);
      } finally {
        await fetchCategories();
      }
    };

    const fetchCategories = async () => {
      setAuthHeader();
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_DOMAIN_SERVER}/api/categories/`);
        categories.value = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    const sortTable = (column) => {
      if (sortColumn.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortColumn.value = column;
        sortDirection.value = 'asc';
      }
      currentPage.value = 1;
    };
    onMounted(async () => {
      await fetchCategories();
    });

    return {
      searchQuery,
      categories,
      filteredCategories,
      paginatedCategories,
      totalPages,
      currentPage,
      showAddCategoryModal,
      showEditCategoryModal,
      showDeleteModal,
      currentCategory,
      openAddCategoryModal,
      openEditCategoryModal,
      closeCategoryModal,
      addCategory,
      updateCategory,
      confirmDeleteCategory,
      closeDeleteModal,
      confirmDeleteCategoryAction,
      sortTable,
      sortColumn,
      sortDirection,
    };
  },
};
</script>