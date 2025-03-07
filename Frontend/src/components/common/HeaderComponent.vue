<template>
  <header class="header-banner">
    <!-- Site Icon -->
    <div class="site-icon">
      <router-link to="/LandingPage" title="SaltnLife">
        <img
          src="@\assets\pictures\saltnlightlogo1.webp"
          alt="SaltnLight Logo"
          class="icon"
        />
      </router-link>
    </div>

    <!-- Navigation Links -->
    <nav class="nav-links">
      <router-link to="/search" class="nav-link">Explore</router-link>
      <router-link to="/RegistrationPage" class="nav-link">Sign Up</router-link>
      <a @click="navigateToProfile" class="nav-link" style="cursor: pointer"
        >Profile</a
      >
      <button @click="logout" class="logout-btn">Logout</button>
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
    navigateToProfile() {
      // Check if user is logged in by looking for access token
      const token = localStorage.getItem("access_token");
      if (token) {
        this.$router.push("/UserProfile");
      } else {
        this.$router.push("/AppLogin");
      }
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
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
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

/* Logout Button Styling */
.logout-btn {
  background-color: #dc3545;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>
