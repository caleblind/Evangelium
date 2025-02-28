<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <transition name="fade" mode="out-in">
        <!-- Profile View -->
        <div v-if="!editing" key="view" class="profile-card">
          <div class="profile-header">
            <h1>{{ profile.first_name }} {{ profile.last_name }}</h1>
            <button @click="editing = true" class="edit-btn">
              <i class="fas fa-edit"></i> Edit Profile
            </button>
          </div>

          <div class="profile-content">
            <div class="profile-section">
              <h3>Personal Information</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="label">Username</span>
                  <span class="value">{{ profile.user.username }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Email</span>
                  <span class="value">{{ profile.user.email }}</span>
                </div>
                <div class="info-item">
                  <span class="label">User Type</span>
                  <span class="value">{{ profile.user_type }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Denomination</span>
                  <span class="value">{{ profile.denomination }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Phone</span>
                  <span class="value">{{ profile.phone_number }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Years of Experience</span>
                  <span class="value">{{ profile.years_of_experience }}</span>
                </div>
              </div>
            </div>

            <div class="profile-section">
              <h3>Location</h3>
              <div class="address">
                <p>{{ profile.street_address }}</p>
                <p>{{ profile.city }}, {{ profile.state }}</p>
                <p>{{ profile.country }}</p>
              </div>
            </div>

            <div class="profile-section">
              <h3>Tags</h3>
              <div class="tags">
                <span v-for="tag in profile.tags" :key="tag.id" class="tag">
                  {{ tag.name }}
                </span>
              </div>
            </div>

            <div class="profile-section">
              <h3>Description</h3>
              <p class="description">{{ profile.description }}</p>
            </div>
          </div>
        </div>

        <!-- Edit Profile Form -->
        <div v-else key="edit" class="profile-card edit-mode">
          <div class="profile-header">
            <h1>Edit Profile</h1>
            <button @click="editing = false" class="cancel-btn">
              <i class="fas fa-times"></i> Cancel
            </button>
          </div>

          <form @submit.prevent="updateProfile" class="edit-form">
            <div class="form-grid">
              <div class="form-group">
                <label>First Name</label>
                <input v-model="profile.first_name" type="text" required />
              </div>

              <div class="form-group">
                <label>Last Name</label>
                <input v-model="profile.last_name" type="text" required />
              </div>

              <div class="form-group">
                <label>Phone Number</label>
                <input v-model="profile.phone_number" type="text" />
              </div>

              <div class="form-group">
                <label>Street Address</label>
                <input v-model="profile.street_address" type="text" />
              </div>

              <div class="form-group">
                <label>City</label>
                <input v-model="profile.city" type="text" />
              </div>

              <div class="form-group">
                <label>State</label>
                <input v-model="profile.state" type="text" />
              </div>

              <div class="form-group">
                <label>Country</label>
                <input v-model="profile.country" type="text" />
              </div>

              <div class="form-group">
                <label>Years of Experience</label>
                <input v-model="profile.years_of_experience" type="number" />
              </div>
            </div>

            <div class="form-group full-width">
              <label>Tags</label>
              <select v-model="selectedTags" multiple class="tag-select">
                <option
                  v-for="tag in availableTags"
                  :key="tag.id"
                  :value="tag.id"
                >
                  {{ tag.name }}
                </option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>Description</label>
              <textarea v-model="profile.description" rows="4"></textarea>
            </div>

            <div class="form-actions">
              <button type="submit" class="save-btn">
                <i class="fas fa-save"></i> Save Changes
              </button>
            </div>
          </form>
        </div>
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

.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.profile-card.edit-mode {
  width: 100%;
  max-width: 900px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.profile-header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.profile-section {
  margin-bottom: 2rem;
}

.profile-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .profile-container {
    padding: 2rem 1rem;
    align-items: flex-start;
  }

  .profile-card,
  .profile-card.edit-mode {
    max-width: 100%;
  }
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.3rem;
}

.value {
  font-size: 1.1rem;
  color: #2c3e50;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #e1f5fe;
  color: #0288d1;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.description {
  line-height: 1.6;
  color: #2c3e50;
}

.edit-btn,
.save-btn,
.cancel-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.edit-btn {
  background: #3498db;
  color: white;
}

.edit-btn:hover {
  background: #2980b9;
}

.save-btn {
  background: #2ecc71;
  color: white;
}

.save-btn:hover {
  background: #27ae60;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background: #c0392b;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #3498db;
  outline: none;
}

.tag-select {
  min-height: 100px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
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
</style>

<script>
import axios from "axios";

export default {
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

    async updateProfile() {
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
          if (this.profile[field] !== this.originalProfile[field]) {
            changedFields[field] = this.profile[field];
          }
        });

        const originalTagIds = this.originalProfile.tags.map((tag) => tag.id);
        if (
          JSON.stringify(this.selectedTags.sort()) !==
          JSON.stringify(originalTagIds.sort())
        ) {
          changedFields.tags = this.selectedTags;
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
