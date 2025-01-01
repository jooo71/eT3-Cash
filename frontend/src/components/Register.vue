<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="name">Name:</label>
        <input
          v-model="name"
          type="text"
          id="name"
          placeholder="Enter your name"
          required
        />
      </div>

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

      <button type="submit">Register</button>
    </form>

    <!-- Success or error messages -->
    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import api from "@/api"; // Ensure you've set up the axios instance in api.js
import '@/assets/Register.css'; // Import the CSS file

export default {
  data() {
    return {
      name: "",
      phone_number: "",
      password: "",
      successMessage: null,
      errorMessage: null,
    };
  },
  methods: {
    async register() {
      try {
        // Clear previous messages
        this.successMessage = null;
        this.errorMessage = null;

        // Make POST request to the register API
        const response = await api.post("/register/", {
          name: this.name,
          phone_number: this.phone_number,
          password: this.password,
        });

        // Handle successful response
        this.successMessage = "Registration successful!";
        this.name = "";
        this.phone_number = "";
        this.password = "";
      } catch (error) {
        // Handle error response
        this.errorMessage =
          error.response && error.response.data.error
            ? error.response.data.error
            : "An error occurred during registration.";
      }
    },
  },
};
</script>
