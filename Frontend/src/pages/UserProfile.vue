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
        <p>
          <strong>Tags:</strong>
          {{ profile.tags.map((tag) => tag.name).join(", ") }}
        </p>
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
          <label>
            Tags:
            <select v-model="selectedTags" multiple>
              <option
                v-for="tag in availableTags"
                :key="tag.id"
                :value="tag.id"
              >
                {{ tag.name }}
              </option>
            </select>
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
      selectedTags: [],
      availableTags: [],
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

        // Makes sure selectedTags contains only IDs for updating
        this.selectedTags = response.data.tags.map((tag) => tag.id);

        // Fetch all available tags from backend
        const tagResponse = await axios.get("http://127.0.0.1:8000/tag/");
        this.availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

        // Makes sure profile.tags is an array of tag objects for display
        this.profile.tags = response.data.tags.map((tagId) => {
          return (
            this.availableTags.find((tag) => tag.id === tagId) || {
              id: tagId,
              name: "Unknown Tag",
            }
          );
        });
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
          tags: this.selectedTags,
        };

        await axios.patch(url, updatedData, {
          headers: { Authorization: `Bearer ${token}` },
        });

        alert("Profile updated successfully!");
        this.editing = false;
        this.fetchProfile();
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
