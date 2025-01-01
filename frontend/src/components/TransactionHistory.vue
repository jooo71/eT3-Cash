<template>
  <div class="transaction-history-container">
    <h2>Transaction History</h2>
    <button @click="TransactionHistory">Fetch Transaction History</button>

    <!-- Display Transactions -->
    <div v-if="transactions.length" class="transactions">
      <ul>
        <li v-for="(transaction, index) in transactions" :key="index">
          <strong>{{ transaction.transaction_type }}</strong> - 
          Amount: {{ transaction.amount }} - 
          Date: {{ formatDate(transaction.date) }} 
          <span v-if="transaction.sender"> (Sent by: {{ transaction.sender.name }})</span>
          <span v-if="transaction.recipient"> (Received by: {{ transaction.recipient.name }})</span>
        </li>
      </ul>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
  <BackButton/>
</template>

  
  <script>
  import api from "@/api"; // Axios instance
  import BackButton from '@/components/BackButton.vue'; // Import the BackButton component
  import '@/assets/transaction-history.css';
  export default {
    components: {
    BackButton, // Register the BackButton component
  },
    data() {
      return {
        transactions: [],
        errorMessage: null,
      };
    },
    methods: {
      async TransactionHistory() {
        try {
          // Clear previous messages
          this.errorMessage = null;
  
          // Make GET request to the transaction history API
          const response = await api.get("/transaction-history/");
  
          // Handle successful response
          this.transactions = response.data;
        } catch (error) {
          // Handle error response
          this.errorMessage =
            error.response && error.response.data.error
              ? error.response.data.error
              : "An error occurred while fetching the transaction history.";
        }
      },
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString(); // Format the date in a readable way
      },
    },
  };
  </script>
  
  