<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Manage Users</h1>
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
              placeholder="Search users..."
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
            <Search class="absolute right-3 top-2.5 text-gray-500 h-5 w-5" />
          </div>
        </div>

        <div class="w-full md:w-48">
          <label for="role" class="block text-sm font-medium text-gray-700 mb-1">Role</label>
          <select
            id="role"
            v-model="selectedRole"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          >
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="client">Client</option> </select>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="sortUsers('fullname')"
              >
                User
                <SortIcon :sortKey="sortKey" :sortOrder="sortOrder" :column="'fullname'" />
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="sortUsers('role_name')"
              >
                Role
                <SortIcon :sortKey="sortKey" :sortOrder="sortOrder" :column="'role_name'" />
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="sortUsers('created_at')"
              >
                Joined
                <SortIcon :sortKey="sortKey" :sortOrder="sortOrder" :column="'created_at'" />
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div
                    class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-semibold text-lg"
                  >
                    {{ user.fullname ? user.fullname.charAt(0) : "U" }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ user.fullname }}
                    </div>
                    <div class="text-sm text-gray-500">ID: {{ user.id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.email }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'"
                >
                  {{ user.role === "admin" ? "Admin" : "Client" }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click="editUser(user)" class="text-indigo-600 hover:text-indigo-900 mr-3">
                  <Edit class="h-5 w-5" />
                </button>
                <button
                  @click="toggleUserStatus(user)"
                  class="text-gray-600 hover:text-gray-900 mr-3"
                  :title="user.status === 'active' ? 'Deactivate User' : 'Activate User'"
                >
                  <template v-if="user.status === 'active'">
                    <UserX class="h-5 w-5" />
                  </template>
                  <template v-else>
                    <UserCheck class="h-5 w-5" />
                  </template>
                </button>
                <button @click="deleteUser(user.id)" class="text-red-600 hover:text-red-900">
                  <Trash2 class="h-5 w-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredUsers.length === 0" class="text-center py-12">
        <Users class="h-16 w-16 mx-auto text-gray-400 mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">No users found</h3>
        <p class="text-gray-500">
          Try adjusting your search or filter to find what you're looking for.
        </p>
      </div>
    </div>

    <div class="flex justify-center mt-4" v-if="filteredUsers.length > itemsPerPage">
      <button @click="currentPage--" :disabled="currentPage === 1" class="px-4 py-2 mx-1 bg-gray-200 rounded-md">
        Previous
      </button>
      <button
        @click="currentPage++"
        :disabled="currentPage * itemsPerPage >= filteredUsers.length"
        class="px-4 py-2 mx-1 bg-gray-200 rounded-md"
      >
        Next
      </button>
    </div>

    <div
      v-if="showAddUserModal || showEditUserModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">
            {{ showEditUserModal ? "Edit User" : "Add New User" }}
          </h2>
        </div>

        <form @submit.prevent="showEditUserModal ? updateUser() : addUser()" class="p-4">
          <div class="mb-4">
            <label for="userName" class="block text-sm font-medium text-gray-700 mb-1">
              Full Name
            </label>
            <input
              type="text"
              id="userName"
              v-model="currentUser.fullname"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>

          <div class="mb-4">
            <label for="userEmail" class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              id="userEmail"
              v-model="currentUser.email"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>

          <div class="mb-4" v-if="showAddUserModal">
            <label for="userPassword" class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              id="userPassword"
              v-model="currentUser.password"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            />
          </div>
          <div class="mb-4" v-else>
            <label for="userPassword" class="block text-sm font-medium text-gray-700 mb-1">
              New Password (leave blank to keep current)
            </label>
            <input
              type="password"
              id="userPassword"
              v-model="currentUser.password"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>

          <div class="mb-4">
            <label for="userRole" class="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <select
              id="userRole"
              v-model="currentUser.role"
              class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              required
            >
              <option value="admin">Admin</option>
              <option value="client">Client</option>
            </select>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button
              type="button"
              @click="closeUserModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button type="submit" class="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700">
              {{ showEditUserModal ? "Update" : "Add" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-4 border-b">
          <h2 class="text-lg font-semibold">Confirm Delete</h2>
        </div>

        <div class="p-4">
          <p class="text-gray-700 mb-4">
            Are you sure you want to delete this user? This action cannot be undone.
          </p>

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
import { ref, computed, onMounted, h } from "vue";
import axios from "axios";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  UserX,
  UserCheck,
  Users,
  ChevronUp,
  ChevronDown,
} from "lucide-vue-next";

const API_BASE_URL = `${import.meta.env.VITE_API_DOMAIN_SERVER}/api/users`;

export default {
  name: "AdminUsers",
  components: {
    Search,
    Plus,
    Edit,
    Trash2,
    UserX,
    UserCheck,
    Users,
    SortIcon: {
      props: ["sortKey", "sortOrder", "column"],
      setup(props) {
        return () => {
          if (props.sortKey !== props.column) return null;
          return props.sortOrder === "asc" ? h(ChevronUp) : h(ChevronDown);
        };
      },
    },
  },
  setup() {
    // State
    const searchQuery = ref("");
    const selectedRole = ref("");
    const showAddUserModal = ref(false);
    const showEditUserModal = ref(false);
    const showDeleteModal = ref(false);
    const userToDeleteId = ref(null);
    const users = ref([]);
    const currentUser = ref({ id: null, fullname: "", email: "", password: "", role: "client" }); // Cập nhật thành "client"
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const sortKey = ref(null);
    const sortOrder = ref("asc");

    // **Helper function to get the token**
    const getToken = () => localStorage.getItem("access_token");
    const setAuthHeader = () => {
      const token = getToken();
      if (token) axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      else delete axios.defaults.headers.common["Authorization"];
    };

    // Fetch users from API
    const fetchUsers = async () => {
      setAuthHeader();
      try {
        const response = await axios.get(API_BASE_URL);
        users.value = response.data;
        console.log("Fetched users:", users.value); // DEBUG
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    onMounted(fetchUsers);

    // Computed
    const filteredUsers = computed(() => {
      let result = [...users.value];

      console.log("Selected role:", selectedRole.value); // DEBUG

      // Filter by search query
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(user =>
          user.fullname.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        );
      }

      // Filter by role
      if (selectedRole.value) {
        result = result.filter(user => user.role === selectedRole.value); // Sửa thành 'user.role'
        console.log("Filtered users by role:", result); // DEBUG
      } else {
        console.log("No role selected, showing all users after search filter."); // DEBUG
      }

      // Sort users
      if (sortKey.value) {
        result.sort((a, b) => {
          const valA = a[sortKey.value];
          const valB = b[sortKey.value];

          if (key === 'role') { // Sửa logic sắp xếp cho 'role'
            return sortOrder.value === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
          } else if (typeof valA === "string" && typeof valB === "string") {
            return sortOrder.value === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
          } else if (typeof valA === 'number' && typeof valB === 'number') {
            return sortOrder.value === "asc" ? valA - valB : valB - valA;
          } else if (valA instanceof Date && valB instanceof Date) {
            return sortOrder.value === "asc" ? valA.getTime() - valB.getTime() : valB.getTime() - valA.getTime();
          } else {
            return 0; // Handle cases where data types are mixed or not comparable
          }
        });
      }

      return result;
    });

    const paginatedUsers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      const end = start + itemsPerPage.value;
      return filteredUsers.value.slice(start, end);
    });

    //// Methods
    const resetCurrentUser = () => {
      currentUser.value = { id: null, fullname: "", email: "", password: "", role: "customer" }; // Sửa thành 'role'
    };

    const closeUserModal = () => {
      showAddUserModal.value = false;
      showEditUserModal.value = false;
      resetCurrentUser();
    };

    const addUser = async () => {
      setAuthHeader();
      try {
        const existingUser = users.value.find(user => user.email === currentUser.value.email);
        if (existingUser) {
          alert("Email đã tồn tại!");
          return;
        }
        await axios.post(API_BASE_URL, { ...currentUser.value });
        fetchUsers();
        closeUserModal();
      } catch (error) {
        console.error("Error adding user:", error);
      }
    };

    const editUser = (user) => {
      currentUser.value = { ...user };
      showEditUserModal.value = true;
    };

    const updateUser = async () => {
      setAuthHeader();
      try {
        const updateData = {
          email: currentUser.value.email,
          fullname: currentUser.value.fullname,
          role: currentUser.value.role, // Sửa thành 'role'
        };

        // Chỉ gửi password nếu nó được thay đổi
        if (currentUser.value.password) {
          updateData.password = currentUser.value.password;
        }

        // Đảm bảo URL có dấu gạch chéo ở cuối
        const apiUrlWithSlash = `${API_BASE_URL}/${currentUser.value.id}/`;

        const response = await axios.put(
          apiUrlWithSlash,
          updateData
        );

        console.log("Update User Response:", response.data); // Log the response
        fetchUsers();
        closeUserModal();
      } catch (error) {
        console.error("Lỗi khi cập nhật người dùng:", error);
        if (error.response) {
          // Server trả về mã lỗi
          console.error("Dữ liệu lỗi từ Server:", error.response.data);
          console.error("Trạng thái lỗi từ Server:", error.response.status);
          console.error("Headers lỗi từ Server:", error.response.headers);
          alert(
            `Lỗi khi cập nhật người dùng: ${JSON.stringify(error.response.data)}`
          ); // Hiển thị thông tin lỗi từ server
        } else if (error.request) {
          // Không nhận được phản hồi từ server
          console.error("Không nhận được phản hồi. Server có thể đang gặp sự cố.");
          alert("Không thể kết nối đến server. Vui lòng thử lại sau.");
        } else {
          // Lỗi khác
          console.error("Thông báo lỗi:", error.message);
          alert("Đã xảy ra lỗi không mong muốn.");
        }
      }
    };

    const toggleUserStatus = async (user) => {
      setAuthHeader();
      try {
        await axios.put(`${API_BASE_URL}/${user.id}/`, { status: user.status === "active" ? "inactive" : "active" });
        fetchUsers();
      } catch (error) {
        console.error("Error toggling user status:", error);
      }
    };

    const deleteUser = (id) => {
      userToDeleteId.value = id;
      showDeleteModal.value = true;
    };

    const confirmDelete = async () => {
      setAuthHeader();
      try {
        await axios.delete(`${API_BASE_URL}/${userToDeleteId.value}/`);
        fetchUsers();
        showDeleteModal.value = false;
        userToDeleteId.value = null;
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    };

    const sortUsers = (key) => {
      if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
      } else {
        sortKey.value = key;
        sortOrder.value = "asc";
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    };

    return {
      searchQuery,
      selectedRole,
      users,
      filteredUsers,
      paginatedUsers,
      showAddUserModal,
      showEditUserModal,
      showDeleteModal,
      currentUser,
      addUser,
      editUser,
      updateUser,
      toggleUserStatus,
      deleteUser,
      confirmDelete,
      closeUserModal,
      currentPage,
      itemsPerPage,
      sortKey,
      sortOrder,
      sortUsers,
      formatDate,
      SortIcon: {
        props: ["sortKey", "sortOrder", "column"],
        setup(props) {
          return () => {
            if (props.sortKey !== props.column) return null;
            return props.sortOrder === "asc" ? h(ChevronUp) : h(ChevronDown);
          };
        },
      },
    };
  },
};
</script>