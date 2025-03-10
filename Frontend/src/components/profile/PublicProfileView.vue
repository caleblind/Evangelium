<template>
  <div class="profile-card">
    <div class="profile-header">
      <h1>{{ profile.first_name }} {{ profile.last_name }}</h1>
    </div>

    <div class="profile-content">
      <div class="profile-section">
        <h3>Personal Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Username</span>
            <span class="value">{{ profile.user?.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email</span>
            <span class="value">{{ profile.user?.email }}</span>
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
        <div class="tag-header">
          <h3>Tags</h3>
          <button
            v-if="!isOwnProfile"
            class="add-tag-btn"
            @click="showTagDialog = true"
          >
            <span class="plus-icon">+</span>
          </button>
        </div>
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

    <!-- Tag Dialog -->
    <div v-if="showTagDialog" class="dialog-overlay" @click="closeTagDialog">
      <div class="dialog" @click.stop>
        <h3>Add Tag</h3>
        <div class="dialog-content">
          <div class="form-group">
            <label>Select Tag:</label>
            <select v-model="selectedTag" class="tag-select">
              <option value="">Choose a tag...</option>
              <option
                v-for="tag in availableTags"
                :key="tag.id"
                :value="tag.id"
              >
                {{ tag.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Or Create New Tag:</label>
            <input
              v-model="newTagName"
              type="text"
              class="tag-input"
              placeholder="Enter tag name"
            />
          </div>
          <div class="dialog-actions">
            <button class="cancel-btn" @click="closeTagDialog">Cancel</button>
            <button
              class="add-btn"
              @click="handleAddTag"
              :disabled="!selectedTag && !newTagName"
            >
              Add Tag
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PublicProfileView",
  props: {
    profile: {
      type: Object,
      required: true,
    },
    isOwnProfile: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showTagDialog: false,
      selectedTag: "",
      newTagName: "",
      availableTags: [],
      error: null,
    };
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("access_token");
      return {
        Authorization: `Bearer ${token}`,
      };
    },
    async fetchAvailableTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/", {
          headers: this.getAuthHeader(),
        });
        this.availableTags = response.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
          description: tag.tag_description,
        }));
      } catch (error) {
        console.error("Error fetching tags:", error);
      }
    },
    closeTagDialog() {
      this.showTagDialog = false;
      this.selectedTag = "";
      this.newTagName = "";
    },
    async handleAddTag() {
      try {
        if (this.newTagName) {
          // Create new tag and add to profile
          const createResponse = await axios.post(
            "http://127.0.0.1:8000/tag/",
            {
              tag_name: this.newTagName,
              tag_description: "",
              tag_is_predefined: false,
              profile_id: this.profile.user.id,
            },
            {
              headers: this.getAuthHeader(),
            }
          );
          this.$emit("tag-added", createResponse.data);
        } else if (this.selectedTag) {
          // Add existing tag to profile
          const addResponse = await axios.post(
            "http://127.0.0.1:8000/tag/",
            {
              tag_id: this.selectedTag,
              profile_id: this.profile.user.id,
            },
            {
              headers: this.getAuthHeader(),
            }
          );
          this.$emit("tag-added", addResponse.data);
        }
        this.closeTagDialog();
      } catch (error) {
        console.error("Error adding tag:", error);
        this.error = error.response?.data?.message || "Error adding tag";
      }
    },
  },
  mounted() {
    this.fetchAvailableTags();
  },
};
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
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

@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }
}

.tag-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.add-tag-btn {
  background: #3498db;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-tag-btn:hover {
  background: #2980b9;
}

.plus-icon {
  font-size: 20px;
  line-height: 1;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dialog h3 {
  margin: 0 0 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.tag-select,
.tag-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn,
.add-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn {
  background: #f1f1f1;
  color: #666;
}

.add-btn {
  background: #3498db;
  color: white;
}

.add-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
</style>
