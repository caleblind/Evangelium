<template>
  <div id="app">
    <HeaderBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import HeaderBar from "@/components/HeaderBar.vue";

export default {
  name: "App",
  components: {
    HeaderBar,
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
