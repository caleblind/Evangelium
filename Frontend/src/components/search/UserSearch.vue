<template>
  <div class="search-container">
    <!-- Search Mode Toggle -->
    <div class="search-mode-toggle">
      <button
        :class="['mode-btn', { active: !isDetailedSearch }]"
        @click="isDetailedSearch = false"
      >
        Quick Search
      </button>
      <button
        :class="['mode-btn', { active: isDetailedSearch }]"
        @click="isDetailedSearch = true"
      >
        Detailed Search
      </button>
    </div>

    <!-- Quick Search -->
    <div v-if="!isDetailedSearch" class="quick-search">
      <div class="form-group">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by name, location, or interests"
          class="search-input"
          @input="handleQuickSearch"
        />
      </div>
    </div>

    <!-- Detailed Search -->
    <div v-else class="detailed-search">
      <div class="form-group">
        <label>Name</label>
        <input
          type="text"
          v-model="detailedFilters.name"
          placeholder="Enter name"
          class="search-input"
        />
      </div>

      <div class="filters">
        <!-- User Type Filter -->
        <div class="form-group">
          <label>User Type</label>
          <select v-model="detailedFilters.userType" class="select-input">
            <option value="">All Types</option>
            <option value="missionary">Missionary</option>
            <option value="supporter">Supporter</option>
          </select>
        </div>

        <!-- Location Filters -->
        <div class="form-group">
          <label>City</label>
          <input
            type="text"
            v-model="detailedFilters.city"
            placeholder="Enter city"
            class="search-input"
          />
        </div>
        <div class="form-group">
          <label>State</label>
          <input
            type="text"
            v-model="detailedFilters.state"
            placeholder="Enter state"
            class="search-input"
          />
        </div>
        <div class="form-group">
          <label>Country</label>
          <input
            type="text"
            v-model="detailedFilters.country"
            placeholder="Enter country"
            class="search-input"
          />
        </div>

        <!-- Tags Filter -->
        <div class="form-group">
          <label>Tags</label>
          <!-- Selected Tags Display -->
          <div class="selected-tags" v-if="detailedFilters.tags.length > 0">
            <div
              v-for="tag in detailedFilters.tags"
              :key="tag"
              class="selected-tag"
            >
              {{ getTagName(tag) }}
              <button class="remove-tag" @click="removeTag(tag)" type="button">
                ×
              </button>
            </div>
          </div>
          <!-- Searchable Tag Input -->
          <div class="tag-input-container">
            <input
              type="text"
              v-model="tagSearchQuery"
              @input="filterTags"
              @focus="showAllTags"
              @blur="handleBlur"
              @keydown.enter.prevent="addTag"
              @keydown.down.prevent="moveTagSelection(1)"
              @keydown.up.prevent="moveTagSelection(-1)"
              placeholder="Type to search or add new tags"
              class="tag-input"
            />
            <!-- Tag Suggestions Dropdown -->
            <div v-if="showTagSuggestions" class="tag-suggestions">
              <div
                v-for="(tag, index) in filteredTags"
                :key="tag.id"
                :class="[
                  'tag-suggestion',
                  { active: index === selectedTagIndex },
                ]"
                @click="selectTag(tag)"
                @mouseover="selectedTagIndex = index"
              >
                {{ tag.tag_name }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="search-btn" @click="handleDetailedSearch">Search</button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">Searching...</div>

    <!-- Results -->
    <slot
      name="results"
      :results="results"
      :isLoading="isLoading"
      :hasSearched="hasSearched"
    >
      <div v-if="!isLoading && results.length > 0" class="results-grid">
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
              <span v-for="tag in result.tags" :key="tag" class="tag">
                {{ getTagName(tag) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="hasSearched" class="no-results">
        No results found matching your criteria
      </div>
    </slot>
  </div>
</template>

<script>
import axios from "axios";
import { debounce } from "lodash";

export default {
  name: "UserSearch",
  props: {
    apiEndpoint: {
      type: String,
      default: "http://127.0.0.1:8000/api/profiles/",
    },
  },
  data() {
    return {
      isDetailedSearch: false,
      searchQuery: "",
      detailedFilters: {
        name: "",
        userType: "",
        city: "",
        state: "",
        country: "",
        tags: [],
      },
      results: [],
      availableTags: [],
      hasSearched: false,
      isLoading: false,
      tagSearchQuery: "",
      filteredTags: [],
      showTagSuggestions: false,
      selectedTagIndex: -1,
      tagMap: {}, // Map to store tag details
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    handleQuickSearch: debounce(async function () {
      this.isLoading = true;
      this.hasSearched = true;

      try {
        const params = new URLSearchParams();
        if (this.searchQuery) {
          params.append("search", this.searchQuery);
        }

        const response = await axios.get(
          `${this.apiEndpoint}?${params.toString()}`
        );
        this.results = this.processResults(response.data);
        this.$emit("search-results", this.results);
      } catch (error) {
        console.error("Quick search failed:", error);
        this.results = [];
        this.$emit("search-error", error);
      } finally {
        this.isLoading = false;
      }
    }, 300),

    async handleDetailedSearch() {
      this.isLoading = true;
      this.hasSearched = true;

      try {
        const params = new URLSearchParams();

        // Add name search
        if (this.detailedFilters.name) {
          params.append("search", this.detailedFilters.name);
        }

        // Add user type filter
        if (this.detailedFilters.userType) {
          params.append("user_type", this.detailedFilters.userType);
        }

        // Add location filters
        if (this.detailedFilters.city) {
          params.append("city", this.detailedFilters.city);
        }
        if (this.detailedFilters.state) {
          params.append("state", this.detailedFilters.state);
        }
        if (this.detailedFilters.country) {
          params.append("country", this.detailedFilters.country);
        }

        // Add tags filter - now handles multiple tags
        if (this.detailedFilters.tags && this.detailedFilters.tags.length > 0) {
          this.detailedFilters.tags.forEach((tag) => {
            params.append("tags", tag);
          });
        }

        const response = await axios.get(
          `${this.apiEndpoint}?${params.toString()}`
        );
        this.results = this.processResults(response.data);
        this.$emit("search-results", this.results);
      } catch (error) {
        console.error("Detailed search failed:", error);
        this.results = [];
        this.$emit("search-error", error);
      } finally {
        this.isLoading = false;
      }
    },

    processResults(data) {
      return data.map((result) => ({
        ...result,
        first_name: result.first_name || result.user?.username || "Unknown",
        last_name: result.last_name || "",
        tags: result.tags || [],
      }));
    },

    async fetchTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/");
        this.availableTags = response.data;
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

    formatLocation(result) {
      const parts = [result.city, result.state, result.country]
        .filter(Boolean)
        .join(", ");
      return parts || "Location not specified";
    },

    removeTag(tagToRemove) {
      this.detailedFilters.tags = this.detailedFilters.tags.filter(
        (tag) => tag !== tagToRemove
      );
      // Trigger search after removing a tag
      this.handleDetailedSearch();
    },

    showAllTags() {
      this.filteredTags = this.availableTags.filter(
        (tag) => !this.detailedFilters.tags.includes(tag.id)
      );
      this.showTagSuggestions = true;
      this.selectedTagIndex = -1;
    },

    handleBlur() {
      // Delay hiding suggestions to allow click events to fire
      setTimeout(() => {
        this.showTagSuggestions = false;
      }, 200);
    },

    filterTags() {
      if (!this.tagSearchQuery.trim()) {
        this.showAllTags();
        return;
      }

      const query = this.tagSearchQuery.toLowerCase();
      this.filteredTags = this.availableTags.filter(
        (tag) =>
          tag.tag_name.toLowerCase().includes(query) &&
          !this.detailedFilters.tags.includes(tag.id)
      );
      this.showTagSuggestions = true;
      this.selectedTagIndex = -1;
    },

    addTag() {
      const tagToAdd = this.tagSearchQuery.trim();
      if (!tagToAdd) return;

      // Only allow adding existing tags
      const existingTag = this.availableTags.find(
        (tag) => tag.tag_name.toLowerCase() === tagToAdd.toLowerCase()
      );

      if (existingTag && !this.detailedFilters.tags.includes(existingTag.id)) {
        this.detailedFilters.tags.push(existingTag.id);
        this.tagSearchQuery = "";
        this.filteredTags = [];
        this.showTagSuggestions = false;
        this.handleDetailedSearch();
      }
    },

    selectTag(tag) {
      if (!this.detailedFilters.tags.includes(tag.id)) {
        this.detailedFilters.tags.push(tag.id);
        this.tagSearchQuery = "";
        this.filteredTags = [];
        this.showTagSuggestions = false;
        this.handleDetailedSearch();
      }
    },

    moveTagSelection(direction) {
      if (!this.showTagSuggestions || this.filteredTags.length === 0) return;

      this.selectedTagIndex = Math.max(
        -1,
        Math.min(
          this.filteredTags.length - 1,
          this.selectedTagIndex + direction
        )
      );
    },
  },
};
</script>

<style scoped>
.search-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.search-mode-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.mode-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-btn.active {
  background: #007bff;
  color: white;
  border-color: #0056b3;
}

.quick-search {
  margin-bottom: 20px;
}

.detailed-search .filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.search-btn {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s ease;
}

.search-btn:hover {
  background: #0056b3;
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

.loading-state {
  text-align: center;
  padding: 20px;
  color: #666;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.result-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.select-input[multiple] {
  height: auto;
  min-height: 120px;
  padding: 8px;
}

.select-input[multiple] option {
  padding: 8px;
  margin: 2px 0;
  border-radius: 4px;
  cursor: pointer;
}

.select-input[multiple] option:checked {
  background: #007bff;
  color: white;
}

.help-text {
  display: block;
  margin-top: 4px;
  color: #666;
  font-size: 12px;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.selected-tag {
  display: inline-flex;
  align-items: center;
  background: #e3f2fd;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  color: #1976d2;
  margin-right: 8px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.selected-tag:hover {
  background: #bbdefb;
}

.remove-tag {
  background: none;
  border: none;
  padding: 0 0 0 8px;
  font: inherit;
  cursor: pointer;
  outline: inherit;
  color: #1976d2;
  font-size: 16px;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.remove-tag:hover {
  opacity: 1;
}

.tag-input-container {
  position: relative;
  width: 100%;
}

.tag-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.tag-input:focus {
  border-color: #007bff;
  outline: none;
}

.tag-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tag-suggestion {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.tag-suggestion:hover,
.tag-suggestion.active {
  background-color: #f0f0f0;
}
</style>
