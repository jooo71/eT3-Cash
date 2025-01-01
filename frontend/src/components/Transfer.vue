<template>
  <div class="transfer-container">
    <h2>Transfer Money</h2>
    <form @submit.prevent="Transfer">
      <div class="form-group">
        <label for="recipient_phone">Recipient Phone Number:</label>
        <input
          v-model="recipient_phone"
          type="text"
          id="recipient_phone"
          placeholder="Enter recipient's phone number"
          required
        />
      </div>

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

      <button type="submit">Transfer</button>
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
  import '@/assets/transfer.css';
  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        recipient_phone: "",
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async Transfer() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the transfer API
          const response = await api.post("/transfer/", {
            recipient_phone: this.recipient_phone,
            amount: this.amount,
          });
  
          // Handle successful response
          this.successMessage = response.data.message;
          this.recipient_phone = ""; // Reset form fields
          this.amount = "";
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while making the transfer.";
        }
      },
    },
  };
  </script>
  
  
  