<template>
  <div class="profile-container">
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="profile-card">
        <h2>
          {{ profile.first_name }}
          {{ profile.last_name }}
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
        <!-- Edit Button -->
        <button @click="editing = !editing" class="edit-btn">
          {{ editing ? "Cancel" : "Edit Profile" }}
        </button>
      </div>
      <!-- Edit Profile Form -->
      <div v-if="editing" class="edit-form">
        <h2>Edit Profile</h2>
        <form @submit.prevent="updateProfile">
          <label>
            First Name:
            <input v-model="profile.first_name" type="text" required />
          </label>
          <label>
            Last Name:
            <input v-model="profile.last_name" type="text" required />
          </label>
          <label>
            Phone #:
            <input v-model="profile.phone_number" type="text" />
          </label>
          <label>
            Address:
            <input v-model="profile.street_address" type="text" />
          </label>
          <label>
            City:
            <input v-model="profile.city" type="text" />
          </label>
          <label>
            State:
            <input v-model="profile.state" type="text" />
          </label>
          <label>
            Country:
            <input v-model="profile.country" type="text" />
          </label>
          <label>
            Years Of Experience:
            <input v-model="profile.years_of_experience" type="number" />
          </label>
          <label>
            Description:
            <textarea v-model="profile.description"></textarea>
          </label>

          <button type="submit" class="save-btn">Save Changes</button>
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
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profiles/me/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
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
    async updateProfile() {
      try {
        const token = localStorage.getItem("access_token");
        const profileId = this.profile.user.id;
        const url = `http://127.0.0.1:8000/api/profiles/${profileId}/`;

        const updatedData = {
          user_type: this.profile.user_type,
          denomination: this.profile.denomination,
          phone_number: this.profile.phone_number,
          street_address: this.profile.street_address,
          city: this.profile.city,
          state: this.profile.state,
          country: this.profile.country,
          years_of_experience: this.profile.years_of_experience,
          description: this.profile.description,
        };

        await axios.patch(url, updatedData, {
          headers: { Authorization: `Bearer ${token}` },
        });

        alert("Profile updated successfully!");
        this.editing = false;
      } catch (err) {
        this.error = "Failed to update profile.";
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
  margin: auto;
  padding: 20px;
  text-align: center;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

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

.tags {
  background: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  display: inline-block;
  margin-top: 5px;
}

.description {
  margin-top: 15px;
  font-style: italic;
  color: #444;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
}
</style>
