<template>
  <footer class="bg-gray-800 text-white py-8 mt-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 class="text-xl font-bold mb-4">FoodShop</h3>
          <p class="text-gray-300">Delicious food delivered to your doorstep.</p>
        </div>

        <div>
          <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
          <ul class="space-y-2">
            <li><router-link to="/" class="text-gray-300 hover:text-white">Home</router-link></li>
            <li><router-link to="/about" class="text-gray-300 hover:text-white">About Us</router-link></li>
            <li><router-link to="/menu" class="text-gray-300 hover:text-white">Menu</router-link></li>
            <li><router-link to="/contact" class="text-gray-300 hover:text-white">Contact</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-lg font-semibold mb-4">Contact Us</h4>
          <ul class="space-y-2 text-gray-300">
            <li class="flex items-center">
              <MapPin class="h-5 w-5 mr-2" />
              123 Food Street, City
            </li>
            <li class="flex items-center">
              <Phone class="h-5 w-5 mr-2" />
              +1 234 567 890
            </li>
            <li class="flex items-center">
              <Mail class="h-5 w-5 mr-2" />
              info@foodshop.com
            </li>
          </ul>
        </div>

        <div>
          <h4 class="text-lg font-semibold mb-4">Follow Us</h4>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-300 hover:text-white">
              <Facebook class="h-6 w-6" />
            </a>
            <a href="#" class="text-gray-300 hover:text-white">
              <Instagram class="h-6 w-6" />
            </a>
            <a href="#" class="text-gray-300 hover:text-white">
              <Twitter class="h-6 w-6" />
            </a>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
        <p>&copy; {{ new Date().getFullYear() }} FoodShop. All rights reserved.</p>
      </div>
      <div id="preny-chatbot-container"></div>
    </div>
  </footer>
</template>

<script>
import { MapPin, Phone, Mail, Facebook, Instagram, Twitter } from 'lucide-vue-next';
import { onMounted } from 'vue';

export default {
  name: 'Footer',
  components: {
    MapPin,
    Phone,
    Mail,
    Facebook,
    Instagram,
    Twitter
  },
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://app.preny.ai/embed-global.js';
    script.async = true;
    script.defer = true;
    script.dataset.prenyBotId = '67f542f560a3a78c1ae4dbe4';
    script.dataset.buttonStyle = 'width:200px;height:200px';
    document.body.appendChild(script);
  }
}
</script>