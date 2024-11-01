<template>
  <div id="app">
    <!-- Header Component -->
    <!--<Header />-->

    <!-- Main Content Area -->
    <main>
      <router-view />
      <!-- Renders the current page component based on the route -->
    </main>

    <!-- Footer Component -->
    <!--<Footer/>-->
  </div>
</template>

<script>
// Import the layout components heaader and footer when/if I make them here

export default {
  name: "App",
  components: {},
};
</script>
