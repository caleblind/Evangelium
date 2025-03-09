<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <PublicProfileView :profile="profile" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PublicProfileView from "@/components/profile/PublicProfileView.vue";
import { jwtDecode } from "jwt-decode";

const API_BASE_URL = "http://127.0.0.1:8000";

export default {
  name: "PublicProfile",
  components: {
    PublicProfileView,
  },
  data() {
    return {
      profile: {},
      loading: true,
      error: null,
    };
  },
  methods: {
    getCurrentUserId() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const decodedToken = jwtDecode(token);
        return decodedToken.user_id;
      }
      return null;
    },
    async fetchProfile() {
      try {
        const profileId = this.$route.params.id;
        const currentUserId = this.getCurrentUserId();

        // If the profile being viewed belongs to the current user, redirect to UserProfile
        if (currentUserId && parseInt(profileId) === currentUserId) {
          this.$router.push("/UserProfile");
          return;
        }

        const [profileResponse, tagResponse] = await Promise.all([
          axios.get(`${API_BASE_URL}/api/profiles/${profileId}/`),
          axios.get(`${API_BASE_URL}/tag/`),
        ]);

        // Get the profile data
        const profileData = profileResponse.data;

        // Map the tags using the tag response data
        const availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

        // Map the profile tags to include the full tag information
        profileData.tags = profileData.tags.map(
          (tagId) =>
            availableTags.find((tag) => tag.id === tagId) || {
              id: tagId,
              name: "Unknown Tag",
            }
        );

        this.profile = profileData;
      } catch (err) {
        console.error("Failed to load profile:", err);
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
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error {
  background: #fee;
  color: #e74c3c;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}
</style>
