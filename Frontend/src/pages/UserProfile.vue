<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="profile-card">
        <!---<img
          :src="profile.avatar || defaultAvatar"
          alt="Profile Picture"
          class="avatar"
        /> -->
        <h2>
          {{ profile.user.first_name }}
          {{ profile.user.last_name }}
        </h2>
        <p><strong>Username:</strong> {{ profile.user.username }}</p>
        <p><strong>Email:</strong> {{ profile.user.email }}</p>
        <p><strong>User Type:</strong> {{ profile.user_type }}</p>
        <p><strong>Demonination:</strong> {{ profile.denomination }}</p>
        <p><strong>Phone #:</strong> {{ profile.phone_number }}</p>
        <p>
          <strong>Address:</strong> {{ profile.street_address }},
          {{ profile.city }}, {{ profile.state }},
          {{ profile.country }}
        </p>
        <p>
          <strong>Years Of Experience:</strong>
          {{ profile.years_of_experience }}
        </p>
        <p><strong>Tags:</strong> {{ profile.tags.join(", ") }}</p>
        <p><strong>Description:</strong> {{ profile.description }}</p>
        <!--<button @click="editing = !editing">Edit Profile</button>-->
      </div>

      <!-- <div v-if="editing" class="edit-form">
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
      </div> -->
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
        const token = localStorage.getItem("access_token"); // Retrieve token from local storage (adjust if using sessions)
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profiles/me/",
          {
            headers: {
              Authorization: `Bearer ${token}`, // Include the authentication token
            },
            //withCredentials: true, // Include cookies if using session authentication
          }
        );
        this.profile = response.data;

        // Fetch tags separately
        const tagResponses = await Promise.all(
          this.profile.tags.map((tagId) =>
            axios.get(`http://127.0.0.1:8000/tag/${tagId}/`)
          )
        );

        // Extract tag names
        this.profile.tags = tagResponses.map((res) => res.data.tag_name);
      } catch (err) {
        this.error = "Failed to load profile data.";
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
/* General Container Styling */
.profile-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  text-align: center;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);

  /* Centering the container vertically */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 50vh; /* Make it take at least full viewport height */
}

/* Profile Card */
.profile-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: left;
  text-align: left;
}

/* Username & Email */
.username {
  font-size: 16px;
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

.email {
  font-size: 14px;
  color: #777;
  margin-bottom: 15px;
}

/* Tags */
.tags {
  background: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  display: inline-block;
  margin-top: 5px;
}

/* Description */
.description {
  margin-top: 15px;
  font-style: italic;
  color: #444;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
}
</style>
