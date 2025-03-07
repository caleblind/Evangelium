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
        // Check for token before making the request
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "Please log in to view your profile.";
          this.$router.push("/AppLogin");
          return;
        }

        const [profileResponse, tagResponse] = await Promise.all([
          axios.get(`${API_BASE_URL}/api/profiles/me/`, {
            headers: this.getAuthHeader(),
          }),
          axios.get(`${API_BASE_URL}/tag/`),
        ]);

        if (!profileResponse.data || !profileResponse.data.user) {
          throw new Error("Invalid profile data received");
        }

        this.profile = profileResponse.data;
        this.originalProfile = JSON.parse(JSON.stringify(profileResponse.data));
        this.selectedTags = profileResponse.data.tags.map((tag) => tag.id);

        this.availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

        this.profile.tags = profileResponse.data.tags.map(
          (tagId) =>
            this.availableTags.find((tag) => tag.id === tagId) || {
              id: tagId,
              name: "Unknown Tag",
            }
        );
      } catch (err) {
        console.error("Profile fetch error:", err);
        if (err.response?.status === 401 && retry) {
          try {
            const refreshed = await this.refreshToken();
            if (refreshed) {
              return this.fetchProfile(false);
            } else {
              this.error = "Session expired. Please log in again.";
              this.$router.push("/AppLogin");
            }
          } catch (refreshError) {
            console.error("Token refresh error:", refreshError);
            this.error = "Session expired. Please log in again.";
            this.$router.push("/AppLogin");
          }
        } else {
          this.error = "Failed to load profile data.";
        }
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      try {
        const profileId = this.profile.user.id;
        const changedFields = this.getChangedFields(formData);

        if (Object.keys(changedFields).length === 0) {
          this.editing = false;
          return;
        }

        try {
          await this.sendProfileUpdate(profileId, changedFields);
          alert("Profile updated successfully!");
          this.editing = false;
          this.fetchProfile();
        } catch (err) {
          if (err.response?.status === 401 && (await this.refreshToken())) {
            await this.sendProfileUpdate(profileId, changedFields);
            alert("Profile updated successfully!");
            this.editing = false;
            this.fetchProfile();
          } else {
            this.error =
              err.response?.status === 401
                ? "Session expired. Please log in again."
                : "Failed to update profile.";
          }
        }
      } catch (err) {
        this.error = "Failed to update profile.";
      }
    },

    async sendProfileUpdate(profileId, data) {
      return axios.patch(`${API_BASE_URL}/api/profiles/${profileId}/`, data, {
        headers: this.getAuthHeader(),
      });
    },

    getChangedFields(formData) {
      const changedFields = {};
      const fieldsToCheck = [
        "first_name",
        "last_name",
        "user_type",
        "denomination",
        "phone_number",
        "street_address",
        "city",
        "state",
        "country",
        "years_of_experience",
        "description",
      ];

      fieldsToCheck.forEach((field) => {
        if (formData[field] !== this.originalProfile[field]) {
          changedFields[field] = formData[field];
        }
      });

      const originalTagIds = this.originalProfile.tags.map((tag) => tag.id);
      if (
        JSON.stringify([...formData.tags].sort()) !==
        JSON.stringify([...originalTagIds].sort())
      ) {
        changedFields.tags = formData.tags;
      }

      return changedFields;
    },

    async refreshToken() {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        return false;
      }

      try {
        const response = await axios.post(
          `${API_BASE_URL}/api/token/refresh/`,
          {
            refresh: refreshToken,
          }
        );
        localStorage.setItem("access_token", response.data.access);
        return true;
      } catch (err) {
        console.error("Token refresh failed:", err);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return false;
      }
    },

    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push("/");
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
