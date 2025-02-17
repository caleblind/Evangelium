<template>
  <div class="container">
    <h1>User Profiles</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="profiles">
      <div v-for="user in users" :key="user.user" class="profile-card">
        <img
          v-if="user.profile_picture"
          :src="user.profile_picture"
          alt="Profile Picture"
          class="profile-picture"
        />
        <h2>{{ user.first_name }} {{ user.last_name }}</h2>
        <p>Username: {{ user.user.username }}</p>
        <p>User Type: {{ user.user_type }}</p>
        <p>Denomination: {{ user.denomination }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      loading: true,
      error: null,
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/profiles");
        this.users = response.data;
      } catch (err) {
        this.error = "Failed to fetch data";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
body {
  background-color: #f3f4f6;
  font-family: Arial, sans-serif;
}
.container {
  padding: 20px;
}
.profiles {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.profile-card {
  background: white;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 300px;
}
.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
.error {
  color: red;
}
</style>
