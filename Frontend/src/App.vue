<template>
  <div id="app">
    <AppNav />

    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "App",
  components: {
  },
};
</script>
