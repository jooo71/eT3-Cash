<template>
  <div class="paybill-container">
    <h2>Pay Bill</h2>
    <form @submit.prevent="payBill">
      <div class="form-group">
        <label for="bill_name">Bill Name:</label>
        <input
          v-model="bill_name"
          type="text"
          id="bill_name"
          placeholder="Enter bill name"
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

      <button type="submit">Pay Bill</button>
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
  import '@/assets/paybill.css';
  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        bill_name: "",
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async payBill() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to the pay_bill API
          const response = await api.post("/pay-bill/", {
            bill_name: this.bill_name,
            amount: this.amount,
          });
  
          // Handle successful response
          this.successMessage = response.data.message;
          this.bill_name = ""; // Reset form fields
          this.amount = "";
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while paying the bill.";
        }
      },
    },
  };
  </script>
  
  
  