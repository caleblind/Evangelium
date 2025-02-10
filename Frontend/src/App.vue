<template>
  <div id="app">
    <AppNav />
    <HeaderComponent />
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
      </div>
    </div>
  </div>
  <nav>
    <router-link to="/login">Login</router-link> |
    <router-link to="/register">Register</router-link>
  </nav>
  <router-view />
</template>

<script>
import HeaderComponent from "@/components/common/HeaderComponent.vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
  },
};
</script>

<style>
nav {
  text-align: center;
  margin-bottom: 20px;
}
</style>