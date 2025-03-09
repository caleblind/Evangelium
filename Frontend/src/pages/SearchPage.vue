<template>
  <div class="search-page">
    <!-- Tabs -->
    <div class="tabs">
      <button
        :class="['tab-button', { active: activeTab === 'churches' }]"
        @click="activeTab = 'churches'"
      >
        Churches
      </button>
      <button
        :class="['tab-button', { active: activeTab === 'missionaries' }]"
        @click="activeTab = 'missionaries'"
      >
        Missionaries
      </button>
    </div>

    <!-- Search Component -->
    <UserSearch
      :filters="['location', 'tags']"
      :initial-filters="{
        userType: activeTab === 'churches' ? 'other' : 'missionary',
      }"
      @search-results="handleSearchResults"
      @search-error="handleError"
    >
      <template #results="{ results, isLoading, hasSearched }">
        <div v-if="isLoading" class="loading-state">Searching...</div>
        <div v-else-if="results.length > 0" class="results-grid">
          <div v-for="result in results" :key="result.id" class="result-card">
            <img
              :src="result.profile_picture || '/default-profile.jpg'"
              :alt="result.name"
              class="result-image"
            />
            <div class="result-content">
              <h3>{{ result.first_name }} {{ result.last_name }}</h3>
              <div class="meta-info">
                <span class="user-type">{{
                  formatUserType(result.user_type)
                }}</span>
                <span v-if="result.denomination" class="denomination">{{
                  result.denomination
                }}</span>
              </div>
              <p class="location">{{ formatLocation(result) }}</p>
              <p class="description">{{ result.description }}</p>
              <div class="tags">
                <span v-for="tag in result.tags" :key="tag" class="tag">
                  {{ getTagName(tag) }}
                </span>
              </div>
            </div>
            <button class="bookmark-button">
              <i class="fas fa-bookmark"></i>
            </button>
          </div>
        </div>
        <div v-else-if="hasSearched" class="no-results">
          No results found matching your criteria
        </div>
      </template>
    </UserSearch>
  </div>
</template>

<script>
import UserSearch from "@/components/search/UserSearch.vue";
import axios from "axios";

export default {
  name: "SearchPage",
  components: {
    UserSearch,
  },
  data() {
    return {
      activeTab: "churches",
      tagMap: {}, // Map to store tag details
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    handleSearchResults(results) {
      console.log("Search results:", results);
    },
    handleError(error) {
      console.error("Search error:", error);
    },
    formatLocation(result) {
      const parts = [result.city, result.state, result.country]
        .filter(Boolean)
        .join(", ");
      return parts || "Location not specified";
    },
    async fetchTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/");
        // Create a map of tag IDs to tag names
        this.tagMap = response.data.reduce((acc, tag) => {
          acc[tag.id] = tag.tag_name;
          return acc;
        }, {});
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
    },
    getTagName(tagId) {
      return this.tagMap[tagId] || "Unknown Tag";
    },
    formatUserType(userType) {
      if (!userType) return "Unknown Type";
      // Capitalize first letter and handle 'other' type
      return userType === "other"
        ? "Church"
        : userType.charAt(0).toUpperCase() + userType.slice(1);
    },
  },
};
</script>

<style scoped>
.search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
}

.tab-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background: none;
  cursor: pointer;
  color: #666;
  position: relative;
}

.tab-button.active {
  color: #4285f4;
  font-weight: 600;
}

.tab-button.active::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #4285f4;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.result-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

.result-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.result-content {
  padding: 20px;
}

.result-content h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #333;
}

.location {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
}

.description {
  color: #444;
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.4;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
}

.bookmark-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.meta-info {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 14px;
}

.user-type {
  color: #4285f4;
  font-weight: 500;
}

.denomination {
  color: var(--secondary-color);
  font-style: italic;
}
</style>
