<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="profile-card">
        <img
          :src="profile.avatar || defaultAvatar"
          alt="Profile Picture"
          class="avatar"
        />
        <h2>{{ profile.username }}</h2>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>Full Name:</strong> {{ profile.full_name }}</p>
        <p><strong>Bio:</strong> {{ profile.bio }}</p>
        <button @click="editing = !editing">Edit Profile</button>
      </div>

      <div v-if="editing" class="edit-form">
        <h2>Edit Profile</h2>
        <form @submit.prevent="updateProfile">
          <label
            >Username:
            <input v-model="profile.username" type="text" required />
          </label>
          <label
            >Email:
            <input v-model="profile.email" type="email" required />
          </label>
          <label
            >Full Name:
            <input v-model="profile.full_name" type="text" />
          </label>
          <label
            >Bio:
            <textarea v-model="profile.bio"></textarea>
          </label>
          <button type="submit">Save Changes</button>
          <button type="button" @click="editing = false">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      profile: {},
      loading: true,
      error: null,
      editing: false,
      defaultAvatar: "https://via.placeholder.com/150",
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token"); // Retrieve token from local storage (adjust if using sessions)
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profile/me/",
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the authentication token
            },
            withCredentials: true, // Include cookies if using session authentication
          }
        );
        this.profile = response.data;
      } catch (err) {
        this.error = "Failed to load profile data.";
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      try {
        await axios.put(
          `http://127.0.0.1:8000/api/profiles/${this.profile.id}/`,
          this.profile
        );
        this.editing = false;
      } catch (err) {
        this.error = "Failed to update profile data.";
      }
    },
  },
  created() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}
.profile-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
.error {
  color: red;
}
.edit-form {
  margin-top: 20px;
}
form label {
  display: block;
  margin: 10px 0;
}
input,
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}
button {
  margin-top: 10px;
  padding: 10px;
}
</style>
