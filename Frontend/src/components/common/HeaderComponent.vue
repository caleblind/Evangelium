<template>
  <header class="header-banner">
    <!-- Site Icon -->
    <div class="site-icon">
      <a href="/LandingPage" title="SaltnLife">
        <img src="/path-to-site-icon.png" alt="SaltnLight Logo" class="icon" />
      </a>
    </div>

    <!-- Navigation Links -->
    <nav class="nav-links">
      <a href="/SearchPage" class="nav-link">Explore</a>
      <!--<a href="/UserProfile" class="nav-link">Profile Page</a>-->
      <div>
    <button @click="logout">Logout</button>
  </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: "HeaderComponent",
  methods: {
    logout() {
      // Clear tokens from localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Redirect to login
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* General Header Styling */
.header-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
  font-family: Arial, sans-serif;
}

/* Site Icon */
.site-icon .icon {
  height: 40px;
  width: auto;
}

/* Navigation Links */
.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.nav-link:hover {
  color: #007bff;
}
</style>
