<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="first_name" type="text" placeholder="First Name" />
      <input v-model="last_name" type="text" placeholder="Last Name" />
      <button type="submit">Register</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      first_name: "",
      last_name: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await api.post("/registration/", {
          username: this.username,
          email: this.email,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
        });

        console.log("Registration successful:", response.data); // ✅ Now 'response' is used
        this.$router.push("/login"); // ✅ Redirect after successful registration
      } catch (error) {
        this.errorMessage = "Registration failed. Please check your input.";
      }
    },
  },
};

</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
}
.error {
  color: red;
}
</style>
