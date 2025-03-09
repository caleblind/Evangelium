<template>
  <div id="app">
    <HeaderComponent />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.main-content {
  margin-top: 80px; /* Adjust based on your header height */
  min-height: calc(100vh - 80px);
  background-color: #f4f7fc;
}
</style>
