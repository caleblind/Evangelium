<template>
  <div class="login-container">
    <h2>Login</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="handleLogin">Login</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await api.post("/api/token/", {
          username: this.username,
          password: this.password,
        });

        // ✅ Store tokens
        localStorage.setItem("accessToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);

        this.$router.push("/DashboardApi"); // ✅ Redirect after login
      } catch (error) {
        this.errorMessage = "Invalid credentials. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
}
.error {
  color: red;
}
</style>
