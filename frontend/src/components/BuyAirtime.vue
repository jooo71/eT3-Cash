<template>
  <div class="buyairtime-container">
    <h2>Buy Airtime</h2>
    <form @submit.prevent="BuyAirtime">
      <div class="form-group">
        <label for="amount">Amount:</label>
        <input
          v-model="amount"
          type="number"
          id="amount"
          placeholder="Enter amount"
          required
          min="0"
        />
      </div>

      <button type="submit">Buy Airtime</button>
    </form>

    <!-- Success or error messages -->
    <div v-if="successMessage" class="success">
      {{ successMessage }}
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
  import '@/assets/buyairtime.css';
  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async BuyAirtime() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the buy_airtime API
          const response = await api.post("/buy-airtime/", {
            amount: this.amount,
          });
  
          // Handle successful response
          this.successMessage = response.data.message;
          this.amount = ""; // Reset form fields
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while buying airtime.";
        }
      },
    },
  };
  </script>
  
  
  