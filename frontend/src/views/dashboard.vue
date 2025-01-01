<!-- <template>
  <nav>
    <router-link to="/deposit">deposit</router-link> |
    <router-link to="/withdraw">withdraw</router-link> |
    <router-link to="/payBill">payBill</router-link> |
    <router-link to="/buyAirtime">buyairtime</router-link> |
    <router-link to="/transfer">transfer</router-link> |
    <router-link to="/balance">balance</router-link> |
    <router-link to="/transaction-history">transactionHistory</router-link> |
    <a href="#" @click="logout">logout</a> 

  </nav>

  <BackButton/>
  <router-view/>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c502e;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
import axios from 'axios';
import BackButton from '@/components/BackButton.vue'; // Import the BackButton component

export default {
  components: {
    BackButton, // Register the BackButton component
  },
  methods: {
    async logout() {
      try {
        // Get the access token from localStorage
        const token = localStorage.getItem('access_token');

        // Call the server-side logout API with the token
        await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
          headers: {
            'Authorization': `Bearer ${token}`, // Send the token in the Authorization header
          }
        });
        
        // Remove the access token from localStorage
        localStorage.removeItem('access_token');
        
        // Redirect to the login page
        this.$router.push('/login');
      } catch (error) {
        console.error("Error logging out:", error);
        // Always redirect to login even if there's an error
        this.$router.push('/login');
      }
    }
  }
};
</script> -->

<template>
  <div id="dashboard">
    <header>
      <h1>Dashboard</h1>
      <h1>Welcome {{ user_name }}</h1> 
    </header>

    <main>
      <div class ="position">
          <a href="#" @click="logout" class="dashboard-button logout">Logout</a>

      </div>
      <!-- Navigation buttons in two rows -->
      <div class="button-container">
        <div class="row">
          <router-link to="/deposit" class="dashboard-button">Deposit</router-link>
          <router-link to="/withdraw" class="dashboard-button">Withdraw</router-link>
          <router-link to="/payBill" class="dashboard-button">Pay Bill</router-link>
          <router-link to="/buyAirtime" class="dashboard-button">Buy Airtime</router-link>
        </div>
        <div class="row">
          <router-link to="/transfer" class="dashboard-button">Transfer</router-link>
          <router-link to="/balance" class="dashboard-button">Balance</router-link>
          <router-link to="/transaction-history" class="dashboard-button">Transaction History</router-link>
          <router-link to="/paypal/create-paypal-payment" class="dashboard-button">Pay pal</router-link>

          <!-- <a href="#" @click="logout" class="dashboard-button logout">Logout</a> -->


        </div>
      </div>
      

    </main>
  </div>
</template>


<script>
import axios from 'axios';
import '@/assets/dashboard.css';
export default {
  data() {
    return {
      user_name: '', // Initialize userName
    };
  },
  mounted() {
    // Fetch the userName from localStorage
    this.user_name = localStorage.getItem('user_name');
  },
  methods: {
    async logout() {
      try {
        const token = localStorage.getItem('access_token');
        await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_name');
        this.$router.push('/login');
      } catch (error) {
        console.error("Error logging out:", error);
        this.$router.push('/login');
      }
    }
  }
};
</script>
