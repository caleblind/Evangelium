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

    <!-- Advanced Search Form -->
    <div class="search-form">
      <h2>Advanced Search</h2>

      <div class="form-group">
        <label>Contains</label>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search for names, places, or interests"
          class="search-input"
          @input="handleSearch"
        />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Denomination</label>
          <select
            v-model="filters.denomination"
            class="select-input"
            @change="handleSearch"
          >
            <option value="">-Select a denomination-</option>
            <option value="Baptist">Baptist</option>
            <option value="Catholic">Catholic</option>
            <option value="Protestant">Protestant</option>
            <option value="Non-Denominational">Non-Denominational</option>
          </select>
        </div>

        <div class="form-group">
          <label>Mission Field</label>
          <select
            v-model="filters.missionField"
            class="select-input"
            @change="handleSearch"
          >
            <option value="">-Select a field-</option>
            <option value="Youth Ministry">Youth Ministry</option>
            <option value="Education & Literacy">Education & Literacy</option>
            <option value="Community Outreach">Community Outreach</option>
            <option value="Church Planting">Church Planting</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">Searching...</div>

    <!-- Results Section -->
    <div v-else-if="results.length > 0" class="results-grid">
      <div v-for="result in results" :key="result.id" class="result-card">
        <img
          :src="result.profile_picture || '/default-profile.jpg'"
          :alt="result.name"
          class="result-image"
        />
        <div class="result-content">
          <h3>{{ result.first_name }} {{ result.last_name }}</h3>
          <p class="location">{{ formatLocation(result) }}</p>
          <p class="description">{{ result.description }}</p>
          <div class="tags">
            <span v-for="tag in result.tags" :key="tag.id" class="tag">
              {{ tag.tag_name }}
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
  </div>
</template>

<script>
import axios from "axios";
import { debounce } from "lodash";

export default {
  name: "SearchPage",
  data() {
    return {
      activeTab: "churches",
      searchQuery: "",
      filters: {
        denomination: "",
        missionField: "",
      },
      results: [],
      hasSearched: false,
      isLoading: false,
    };
  },
  created() {
    // Initial search when component is created
    this.handleSearch();
  },
  methods: {
    handleSearch: debounce(async function () {
      this.isLoading = true;
      this.hasSearched = true;

      try {
        // Start with basic search parameters
        const params = new URLSearchParams({
          q: this.searchQuery || "", // Empty string if no query
          type: this.activeTab,
        });

        // Only add filters if they are selected
        if (this.filters.denomination) {
          params.append("denomination", this.filters.denomination);
        }
        if (this.filters.missionField) {
          params.append("missionField", this.filters.missionField);
        }

        const url = `http://127.0.0.1:8000/api/profiles/search?${params.toString()}`;
        console.log("Making request to:", url);

        const response = await axios.get(url);
        console.log("Response received:", response.data);

        if (response.data && response.data.results) {
          this.results = response.data.results.map((result) => ({
            ...result,
            // Use username if first_name is not available
            first_name: result.first_name || result.user?.username || "Unknown",
            last_name: result.last_name || "",
            // Ensure tags is always an array
            tags: Array.isArray(result.tags) ? result.tags : [],
          }));
        } else {
          console.log("No results found in response:", response.data);
          this.results = [];
        }
      } catch (error) {
        console.error("Search failed:", error.response || error);
        this.results = [];
      } finally {
        this.isLoading = false;
      }
    }, 300),

    formatLocation(result) {
      const parts = [result.city, result.state, result.country]
        .filter(Boolean)
        .join(", ");
      return parts || "Location not specified";
    },
  },
  watch: {
    activeTab() {
      this.handleSearch();
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

.search-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.search-input,
.select-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-button {
  background-color: #4285f4;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.search-button:hover {
  background-color: #3367d6;
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

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
