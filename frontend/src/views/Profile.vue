<template>
    <div class="profile-container">
      <div class="profile-header">
        <h1>My Profile</h1>
        <button @click="toggleEditMode" class="edit-btn">
          {{ isEditing ? 'Cancel' : 'Edit Profile' }}
        </button>
      </div>
  
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading your profile...</p>
      </div>
  
      <div v-else class="profile-content">
        <!-- Profile Summary -->
        <div class="profile-card">
          <div class="profile-summary">
            <div class="avatar-container">
              <img :src="user.avatar || 'https://via.placeholder.com/150'" alt="Profile picture" class="avatar">
              <div v-if="isEditing" class="avatar-overlay">
                <label for="avatar-upload" class="avatar-upload-label">
                  <Camera class="camera-icon" />
                  <span class="sr-only">Upload new photo</span>
                </label>
                <input id="avatar-upload" type="file" class="avatar-upload" @change="handleAvatarChange">
              </div>
            </div>
            <div class="profile-info">
              <h2>{{ user.fullname }}</h2>
              <p class="member-since">Member since {{ formatDate(user.createdAt) }}</p>
            </div>
          </div>
        </div>
  
        <!-- Personal Information -->
        <div class="profile-card">
          <h3 class="section-title">Personal Information</h3>
          <div v-if="!isEditing" class="info-display">
            <div class="info-row">
              <span class="info-label">Full Name:</span>
              <span class="info-value">{{ user.fullname }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Phone:</span>
              <span class="info-value">{{ user.phone || 'Not provided' }}</span>
            </div>
          </div>
          <form v-else class="edit-form" @submit.prevent="savePersonalInfo">
            <div class="form-group">
              <label for="fullname">Full Name</label>
              <input 
                type="text" 
                id="fullname" 
                v-model="editForm.fullname" 
                class="form-input" 
                required
              >
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="editForm.email" 
                class="form-input" 
                required
              >
            </div>
            <div class="form-group">
              <label for="phone">Phone</label>
              <input 
                type="tel" 
                id="phone" 
                v-model="editForm.phone" 
                class="form-input"
              >
            </div>
            <div class="form-actions">
              <button type="submit" class="save-btn">Save Changes</button>
            </div>
          </form>
        </div>
  
        <!-- Shipping Address -->
        <div class="profile-card">
          <h3 class="section-title">Shipping Address</h3>
          <div v-if="!isEditing" class="info-display">
            <div v-if="user.address" class="address-display">
              <p class="address-text">{{ user.address }}</p>
            </div>
            <div v-else class="empty-address">
              <p>No shipping address provided.</p>
            </div>
          </div>
          <form v-else class="edit-form" @submit.prevent="saveAddress">
            <div class="form-group">
              <label for="address">Address</label>
              <input 
                type="text" 
                id="address" 
                v-model="editForm.address" 
                class="form-input" 
                required
              >
            </div>
            <div class="form-actions">
              <button type="submit" class="save-btn">Save Address</button>
            </div>
          </form>
        </div>
  
        <!-- Password Change -->
        <div class="profile-card">
          <h3 class="section-title">Change Password</h3>
          <form class="edit-form" @submit.prevent="changePassword">
            <div class="form-group">
              <label for="currentPassword">Current Password</label>
              <input 
                type="password" 
                id="currentPassword" 
                v-model="passwordForm.currentPassword" 
                class="form-input" 
                required
              >
            </div>
            <div class="form-group">
              <label for="newPassword">New Password</label>
              <input 
                type="password" 
                id="newPassword" 
                v-model="passwordForm.newPassword" 
                class="form-input" 
                required
                minlength="8"
              >
            </div>
            <div class="form-group">
              <label for="confirmPassword">Confirm New Password</label>
              <input 
                type="password" 
                id="confirmPassword" 
                v-model="passwordForm.confirmPassword" 
                class="form-input" 
                required
              >
              <p v-if="passwordMismatch" class="error-message">Passwords do not match</p>
            </div>
            <div class="form-actions">
              <button type="submit" class="save-btn">Update Password</button>
            </div>
          </form>
        </div>
  
        <!-- Preferences -->
        <div class="profile-card">
          <h3 class="section-title">Preferences</h3>
          <div class="preferences-section">
            <div class="preference-item">
              <div class="preference-info">
                <h4>Email Notifications</h4>
                <p>Receive emails about your orders, account updates, and promotions</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="preferences.emailNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="preference-item">
              <div class="preference-info">
                <h4>SMS Notifications</h4>
                <p>Receive text messages about your orders and delivery updates</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="preferences.smsNotifications">
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="preference-item">
              <div class="preference-info">
                <h4>Newsletter</h4>
                <p>Subscribe to our newsletter for the latest products and deals</p>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="preferences.newsletter">
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="form-actions">
              <button @click="savePreferences" class="save-btn">Save Preferences</button>
            </div>
          </div>
        </div>
  
        <!-- Danger Zone -->
        <div class="profile-card danger-zone">
          <h3 class="section-title">Account Actions</h3>
          <div class="danger-actions">
            <div class="danger-info">
              <h4>Delete Account</h4>
              <p>Permanently delete your account and all associated data. This action cannot be undone.</p>
            </div>
            <button @click="confirmDeleteAccount" class="delete-btn">Delete Account</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue';
  import { Camera } from 'lucide-vue-next';
  import { userAPI } from '../services/api';
  
  export default {
    name: 'ProfilePage',
    components: {
      Camera
    },
    setup() {
      const loading = ref(true);
      const isEditing = ref(false);
      const passwordMismatch = ref(false);
      const user = ref({});
      
      // Form for editing profile
      const editForm = reactive({
        fullname: '',
        email: '',
        phone: '',
        address: ''
      });
      
      // Form for changing password
      const passwordForm = reactive({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      
      // User preferences
      const preferences = reactive({
        emailNotifications: true,
        smsNotifications: false,
        newsletter: true
      });
      
      // Fetch user profile
      const fetchUserProfile = async () => {
        try {
          // Get user from localStorage
          const storedUser = localStorage.getItem('user');
          if (!storedUser) {
            // Redirect to login if no user is found
            window.location.href = '/login';
            return;
          }
          
          // Parse user data
          const userData = JSON.parse(storedUser);
          console.log('User data from localStorage:', userData);
          
          // Fetch user data from API
          const response = await userAPI.getProfile(userData.id);
          const apiUserData = response.data;
          
          // Set user data
          user.value = {
            id: apiUserData.id,
            fullname: apiUserData.fullname || '',
            email: apiUserData.email || '',
            phone: apiUserData.phone || apiUserData.phone_number || '',
            avatar: apiUserData.avatar || 'https://via.placeholder.com/150',
            createdAt: apiUserData.createdAt || apiUserData.created_at || new Date().toISOString(),
            address: apiUserData.address || ''
          };
          
          // Initialize edit form with user data
          Object.assign(editForm, {
            fullname: user.value.fullname,
            email: user.value.email,
            phone: user.value.phone || '',
            address: user.value.address || ''
          });
          
          loading.value = false;
        } catch (error) {
          console.error('Error fetching profile:', error);
          loading.value = false;
        }
      };
      
      // Toggle edit mode
      const toggleEditMode = () => {
        if (isEditing.value) {
          // Reset form to original values if canceling
          Object.assign(editForm, {
            fullname: user.value.fullname,
            email: user.value.email,
            phone: user.value.phone || '',
            address: user.value.address || ''
          });
        }
        isEditing.value = !isEditing.value;
      };
      
      // Save personal information
      const savePersonalInfo = async () => {
        try {
          // Prepare data for API
          const updateData = {
            fullname: editForm.fullname,
            email: editForm.email,
            phone: editForm.phone
          };
          
          // Call API to update profile
          await userAPI.updateProfile(user.value.id, updateData);
          
          // Update local user object
          Object.assign(user.value, updateData);
          
          // Save updated user to localStorage
          localStorage.setItem('user', JSON.stringify(user.value));
          
          // Exit edit mode
          isEditing.value = false;
          
          console.log('Personal info saved:', updateData);
          alert('Personal information updated successfully!');
        } catch (error) {
          console.error('Error saving profile:', error);
          alert('Failed to update personal information. Please try again.');
        }
      };
      
      // Save address
      const saveAddress = async () => {
        try {
          // Prepare data for API
          const updateData = {
            address: editForm.address
          };
          
          // Call API to update address
          await userAPI.updateProfile(user.value.id, updateData);
          
          // Update local user object
          user.value.address = editForm.address;
          
          // Save updated user to localStorage
          localStorage.setItem('user', JSON.stringify(user.value));
          
          console.log('Address saved:', editForm.address);
          alert('Address updated successfully!');
        } catch (error) {
          console.error('Error saving address:', error);
          alert('Failed to update address. Please try again.');
        }
      };
      
      // Change password
      const changePassword = async () => {
        // Check if passwords match
        if (passwordForm.newPassword !== passwordForm.confirmPassword) {
          passwordMismatch.value = true;
          return;
        }
        
        passwordMismatch.value = false;
        
        try {
          // Prepare data for API
          const passwordData = {
            currentPassword: passwordForm.currentPassword,
            newPassword: passwordForm.newPassword
          };
          
          // Call API to change password
          const response = await userAPI.changePassword(user.value.id, passwordData);
          
          // Reset password form
          passwordForm.currentPassword = '';
          passwordForm.newPassword = '';
          passwordForm.confirmPassword = '';
          
          console.log('Password changed:', response.data);
          alert('Đổi mật khẩu thành công!');
        } catch (error) {
          console.error('Error changing password:', error);
          if (error.response) {
            // Server trả về lỗi
            alert(error.response.data.message || 'Không thể đổi mật khẩu. Vui lòng kiểm tra lại mật khẩu hiện tại.');
          } else if (error.request) {
            // Không nhận được response
            alert('Không thể kết nối đến server. Vui lòng thử lại sau.');
          } else {
            // Lỗi khác
            alert('Có lỗi xảy ra. Vui lòng thử lại.');
          }
        }
      };
      
      // Save preferences
      const savePreferences = async () => {
        try {
          // Save preferences to localStorage
          localStorage.setItem('userPreferences', JSON.stringify(preferences));
          
          console.log('Preferences saved:', preferences);
          alert('Preferences updated successfully!');
        } catch (error) {
          console.error('Error saving preferences:', error);
          alert('Failed to update preferences. Please try again.');
        }
      };
      
      // Handle avatar change
      const handleAvatarChange = (event) => {
        const file = event.target.files[0];
        if (!file) return;
        
        // Create a local URL for the avatar
        const reader = new FileReader();
        reader.onload = (e) => {
          user.value.avatar = e.target.result;
          
          // Save updated user to localStorage
          localStorage.setItem('user', JSON.stringify(user.value));
        };
        reader.readAsDataURL(file);
        
        console.log('Avatar changed');
      };
      
      // Confirm account deletion
      const confirmDeleteAccount = () => {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
          deleteAccount();
        }
      };
      
      // Delete account
      const deleteAccount = async () => {
        try {
          // Call API to delete account
          await userAPI.deleteAccount(user.value.id);
          
          console.log('Account deleted');
          alert('Your account has been deleted. You will be logged out.');
          
          // Clear localStorage
          localStorage.removeItem('user');
          localStorage.removeItem('userPreferences');
          
          // Redirect to login page
          window.location.href = '/login';
        } catch (error) {
          console.error('Error deleting account:', error);
          alert('Failed to delete account. Please try again.');
        }
      };
      
      // Format date
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      };
      
      onMounted(() => {
        fetchUserProfile();
        
        // Load preferences from localStorage
        const storedPreferences = localStorage.getItem('userPreferences');
        if (storedPreferences) {
          Object.assign(preferences, JSON.parse(storedPreferences));
        }
      });
      
      return {
        user,
        loading,
        isEditing,
        editForm,
        passwordForm,
        passwordMismatch,
        preferences,
        toggleEditMode,
        savePersonalInfo,
        saveAddress,
        changePassword,
        savePreferences,
        handleAvatarChange,
        confirmDeleteAccount,
        formatDate
      };
    }
  }
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .profile-header h1 {
    font-size: 1.8rem;
    font-weight: 600;
    color: #333;
    margin: 0;
  }
  
  .edit-btn {
    padding: 0.5rem 1.25rem;
    background-color: #f3f4f6;
    color: #4b5563;
    border: none;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .edit-btn:hover {
    background-color: #e5e7eb;
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
  
  .profile-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .profile-card {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    overflow: hidden;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
  }
  
  .profile-summary {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }
  
  .avatar-container {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
  }
  
  .avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  
  .avatar-upload-label {
    cursor: pointer;
  }
  
  .camera-icon {
    color: white;
    width: 24px;
    height: 24px;
  }
  
  .avatar-upload {
    display: none;
  }
  
  .profile-info h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #111827;
  }
  
  .member-since {
    color: #6b7280;
    font-size: 0.875rem;
    margin: 0 0 0.25rem 0;
  }
  
  .email {
    color: #4b5563;
    margin: 0;
  }
  
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 1.25rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .info-display {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .info-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .info-label {
    font-weight: 500;
    color: #4b5563;
    min-width: 120px;
  }
  
  .info-value {
    color: #111827;
    flex: 1;
  }
  
  .empty-address {
    color: #6b7280;
    font-style: italic;
  }
  
  .edit-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .form-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
    min-width: 250px;
  }
  
  .form-group label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #4b5563;
  }
  
  .form-input {
    padding: 0.625rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    color: #111827;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 0.5rem;
  }
  
  .save-btn {
    padding: 0.5rem 1.25rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .save-btn:hover {
    background-color: #2563eb;
  }
  
  .error-message {
    color: #dc2626;
    font-size: 0.75rem;
    margin-top: 0.25rem;
  }
  
  .preferences-section {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .preference-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f3f4f6;
  }
  
  .preference-item:last-of-type {
    border-bottom: none;
  }
  
  .preference-info h4 {
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 0.25rem 0;
    color: #111827;
  }
  
  .preference-info p {
    color: #6b7280;
    font-size: 0.875rem;
    margin: 0;
  }
  
  .toggle {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 24px;
  }
  
  .toggle input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #e5e7eb;
    transition: .4s;
    border-radius: 24px;
  }
  
  .toggle-slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }
  
  input:checked + .toggle-slider {
    background-color: #3b82f6;
  }
  
  input:checked + .toggle-slider:before {
    transform: translateX(24px);
  }
  
  .danger-zone {
    border-color: #fee2e2;
  }
  
  .danger-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .danger-info h4 {
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 0.25rem 0;
    color: #b91c1c;
  }
  
  .danger-info p {
    color: #6b7280;
    font-size: 0.875rem;
    margin: 0;
    max-width: 500px;
  }
  
  .delete-btn {
    padding: 0.5rem 1.25rem;
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fecaca;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .delete-btn:hover {
    background-color: #fecaca;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .profile-summary {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    
    .danger-actions {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .delete-btn {
      align-self: flex-end;
    }
  }
  
  @media (max-width: 640px) {
    .profile-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .edit-btn {
      width: 100%;
    }
    
    .form-row {
      flex-direction: column;
    }
    
    .form-group {
      min-width: 100%;
    }
  }
  
  .address-display {
    padding: 1rem;
    background-color: #f9fafb;
    border-radius: 0.375rem;
    margin-bottom: 1rem;
  }
  
  .address-text {
    color: #374151;
    font-size: 0.875rem;
    line-height: 1.5;
    margin: 0;
  }
  </style>