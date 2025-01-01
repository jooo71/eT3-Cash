<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="phone_number">Phone Number:</label>
        <input
          v-model="phone_number"
          type="text"
          id="phone_number"
          placeholder="Enter your phone number"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          placeholder="Enter your password"
          required
        />
      </div>

      <button type="submit" class="btn">Login</button>
    </form>

    <!-- Error Message -->
    <div v-if="error" class="error">{{ error }}</div>
    
    <BackButton />
  </div>
</template>

<script>
import api from '@/api.js';
import BackButton from '@/components/BackButton.vue'; // Import BackButton component
import '@/assets/Login.css'; // Import the CSS file

export default {
  components: {
    BackButton, // Register the BackButton component
  },
  data() {
    return {
      phone_number: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.post('/login/', {
          phone_number: this.phone_number,
          password: this.password,
        });

        // Save the access token
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('user_name', response.data.user.name);
        this.$router.push('/dashboard'); // Redirect to a protected route
      } catch (err) {
        this.error = 'Invalid credentials';
      }
    }
  }
};
</script>
