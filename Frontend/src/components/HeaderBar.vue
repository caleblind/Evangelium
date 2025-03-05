<template>
  <header class="header">
    <nav class="nav-container">
      <router-link to="/" class="logo">
        <img
          src="@/assets/pictures/saltnlightlogo1.webp"
          alt="Salt-N-Light Logo"
        />
      </router-link>

      <div class="nav-links">
        <router-link to="/search" class="nav-link">
          <button class="nav-button">Profiles</button>
        </router-link>
        <router-link to="/AppLogin" class="nav-link">
          <button class="nav-button">Login</button>
        </router-link>
        <router-link to="/RegistrationPage" class="nav-link">
          <button class="nav-button">Register</button>
        </router-link>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: "HeaderBar",
};
</script>

<style scoped>
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
}

.nav-button {
  background-color: transparent;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  color: #333;
  transition: color 0.3s ease;
}

.nav-button:hover {
  color: #000;
}

.router-link-active .nav-button {
  color: #000;
  font-weight: 600;
}
</style>
