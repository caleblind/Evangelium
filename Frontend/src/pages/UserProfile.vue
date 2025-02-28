<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <transition name="fade" mode="out-in">
        <ProfileView
          v-if="!editing"
          :profile="profile"
          @edit="editing = true"
          key="view"
        />
        <ProfileEdit
          v-else
          :profile="profile"
          :available-tags="availableTags"
          :selected-tags="selectedTags"
          @cancel="editing = false"
          @submit="updateProfile"
          key="edit"
        />
      </transition>
    </div>
  </div>
</template>

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

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 2rem 1rem;
    align-items: flex-start;
  }
}
</style>

<script>
import axios from "axios";
import ProfileView from "@/components/profile/ProfileView.vue";
import ProfileEdit from "@/components/profile/ProfileEdit.vue";

export default {
  name: "UserProfile",
  components: {
    ProfileView,
    ProfileEdit,
  },
  data() {
    return {
      profile: {},
      originalProfile: {},
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
        this.originalProfile = JSON.parse(JSON.stringify(response.data));

        this.selectedTags = response.data.tags.map((tag) => tag.id);

        const tagResponse = await axios.get("http://127.0.0.1:8000/tag/");
        this.availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

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

    async updateProfile(formData) {
      try {
        const token = localStorage.getItem("access_token");
        const profileId = this.profile.user.id;
        const url = `http://127.0.0.1:8000/api/profiles/${profileId}/`;

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
          JSON.stringify(formData.tags.sort()) !==
          JSON.stringify(originalTagIds.sort())
        ) {
          changedFields.tags = formData.tags;
        }

        if (Object.keys(changedFields).length > 0) {
          await axios.patch(url, changedFields, {
            headers: { Authorization: `Bearer ${token}` },
          });

          alert("Profile updated successfully!");
          this.editing = false;
          this.fetchProfile();
        } else {
          this.editing = false;
        }
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
