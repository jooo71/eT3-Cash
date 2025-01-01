<template>
  <div class="balance-container">
    <h2>Check Balance</h2>
    <button @click="getBalance">Check Balance</button>

    <!-- Success or error messages -->
    <div v-if="balanceMessage" class="balance-message">
      {{ balanceMessage }}
    </div>
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
  <BackButton/>
</template>

  
  <script>
  import api from "@/api"; // Ensure you've set up the axios instance in api.js
  import BackButton from '@/components/BackButton.vue'; // Import the BackButton component
  import '@/assets/balance.css';
  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        balanceMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async getBalance() {
        try {
          // Clear previous messages
          this.balanceMessage = null;
          this.errorMessage = null;
  
          // Make GET request to the balance API
          const response = await api.get("/balance/");
  
          // Handle successful response
          this.balanceMessage = response.data.message;
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while fetching the balance.";
        }
      },
    },
  };
  </script>
  
  