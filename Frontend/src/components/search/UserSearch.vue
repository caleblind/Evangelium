<template>
  <div class="search-container">
    <!-- Main search input -->
    <div class="search-input-wrapper">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search users..."
        class="search-input"
        @input="handleSearch"
        :disabled="isLoading"
      />
      <div v-if="isLoading" class="loading-indicator">
        <span class="loader"></span>
      </div>
    </div>

    <!-- Filter section -->
    <div class="filters" v-if="showFilters">
      <!-- User Type filter -->
      <div class="filter-group" v-if="filters.includes('userType')">
        <label>User Type</label>
        <select v-model="selectedFilters.userType" @change="handleSearch">
          <option value="">All Types</option>
          <option value="Missionary">Missionary</option>
          <option value="Supporter">Supporter</option>
        </select>
      </div>

      <!-- Location filter -->
      <div class="filter-group" v-if="filters.includes('location')">
        <label>Location</label>
        <input
          type="text"
          v-model="selectedFilters.location"
          placeholder="City, State, or Country"
          @input="handleSearch"
        />
      </div>

      <!-- Tags filter -->
      <div class="filter-group" v-if="filters.includes('tags')">
        <label>Tags</label>
        <select v-model="selectedFilters.tags" multiple @change="handleSearch">
          <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
            {{ tag.tag_name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Results section -->
    <div v-if="isLoading" class="loading-state">Searching...</div>
    <div v-else-if="results.length > 0" class="search-results">
      <slot name="result-item" :results="results">
        <UserCard
          v-for="user in results"
          :key="user.id"
          :first_name="user.first_name"
          :last_name="user.last_name"
          :city="user.city"
          :state="user.state"
          :country="user.country"
          :description="user.description"
        />
      </slot>
    </div>
    <div v-else-if="hasSearched" class="no-results">
      No users found matching your search criteria
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { debounce } from "lodash";
import UserCard from "./UserCard.vue";

export default {
  name: "UserSearch",
  components: {
    UserCard,
  },
  props: {
    // Configure which filters to show
    filters: {
      type: Array,
      default: () => ["userType", "location", "tags"],
    },
    // Show/hide filter section
    showFilters: {
      type: Boolean,
      default: true,
    },
    // Initial filters to apply
    initialFilters: {
      type: Object,
      default: () => ({}),
    },
    // API endpoint for searching
    apiEndpoint: {
      type: String,
      default: "http://127.0.0.1:8000/api/profiles/search",
    },
  },
  data() {
    return {
      searchQuery: "",
      selectedFilters: {
        userType: "",
        location: "",
        tags: [],
      },
      results: [],
      availableTags: [],
      hasSearched: false,
      isLoading: false,
    };
  },
  created() {
    // Apply initial filters
    this.selectedFilters = {
      ...this.selectedFilters,
      ...this.initialFilters,
    };

    // If we have initial filters, perform search
    if (Object.keys(this.initialFilters).length > 0) {
      this.handleSearch();
    }

    // Fetch available tags
    this.fetchTags();
  },
  methods: {
    handleSearch: debounce(async function () {
      this.isLoading = true;
      try {
        const params = {
          q: this.searchQuery,
          ...this.selectedFilters,
        };

        const response = await axios.get(this.apiEndpoint, { params });
        this.results = response.data;
        this.hasSearched = true;

        // Emit the results for parent components
        this.$emit("search-results", this.results);
      } catch (error) {
        console.error("Search failed:", error);
        this.$emit("search-error", error);
      } finally {
        this.isLoading = false;
      }
    }, 300),

    async fetchTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/");
        this.availableTags = response.data.filter(
          (tag) => tag.tag_is_predefined
        );
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
    },
  },
};
</script>

<style scoped>
.search-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.search-input-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #000;
  outline: none;
}

.loading-indicator {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

.loader {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  font-size: 14px;
}

.filter-group select,
.filter-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.no-results {
  text-align: center;
  color: #666;
  padding: 40px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
