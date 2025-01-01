<template>
    <div class="paypal-payment-container">
      <h2>Make a Purchase</h2>
      <form @submit.prevent="createPayment">
        <div class="form-group">
          <label for="itemName">Item Name:</label>
          <input
            v-model="itemName"
            type="text"
            id="itemName"
            placeholder="Enter item name"
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
  
        <button type="submit">Pay with PayPal</button>
      </form>
  
      <!-- Success or error messages -->
      <div v-if="successMessage" class="success">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="error">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import api from "@/api"; // Ensure you've set up the axios instance in api.js
  
  export default {
    data() {
      return {
        itemName: "",
        amount: "",
        successMessage: null,
        errorMessage: null,
      };
    },
    methods: {
      async createPayment() {
        try {
          // Clear previous messages
          this.successMessage = null;
          this.errorMessage = null;
  
          // Make POST request to create PayPal payment
          const response = await api.post("/paypal/create-paypal-payment/", {
            item_name: this.itemName,
            amount: this.amount,
          });
  
          // Redirect to PayPal for approval
          window.location.href = response.data.approval_url;
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while creating the payment.";
        }
      },
  
      async completePayment(paymentId, payerId) {
        try {
          const token = localStorage.getItem("access_token"); // Retrieve the stored token
  
          const response = await api.get(`/paypal/execute-paypal-payment/`, {
            headers: {
              Authorization: `Bearer ${token}`, // Include the token in the request headers
            },
            params: {
              paymentId,
              PayerID: payerId,
            },
          });
  
          // Handle successful payment response
          this.successMessage = response.data.message;
        } catch (error) {
          console.error("Error completing the payment:", error);
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while completing the payment.";
        }
      },
    },
    mounted() {
      // Check if there are payment parameters in the URL after PayPal redirects
      const params = new URLSearchParams(window.location.search);
      const paymentId = params.get("paymentId");
      const payerId = params.get("PayerID");
  
      // If paymentId and payerId exist, execute the payment
      if (paymentId && payerId) {
        this.completePayment(paymentId, payerId);
      }
    },
  };
  </script>