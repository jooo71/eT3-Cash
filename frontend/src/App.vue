<template>
  <div id="app">
    <nav v-if="['/', '/login', '/register'].includes($route.path)">
      <div class="button-container">
        <router-link to="/" class="nav-button">Home</router-link>
        <router-link to="/register" class="nav-button">Register</router-link>
        <router-link to="/login" class="nav-button">Login</router-link>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  // Your script logic here
};
</script>

<style src="./App.css"></style>  

