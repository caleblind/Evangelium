<template>
  <div class="search-page">
    <div class="search-container">
  <!-- Search Form -->
      <div class="search-form">
        <div class="search-input">
          <input
            type="text"
            v-model="searchParams.q"
            placeholder="Search by name or description..."
            @input="handleSearch"
          />
      </div>

        <div class="filters">
          <select v-model="searchParams.user_type" @change="handleSearch">
            <option value="">All Roles</option>
            <option value="missionary">Missionary</option>
            <option value="supporter">Supporter</option>
          </select>

        <input
          type="text"
            v-model="searchParams.location"
            placeholder="Location..."
            @input="handleSearch"
          />

          <div class="tags-select">
            <multiselect
              v-model="selectedTags"
              :options="availableTags"
              :multiple="true"
              :close-on-select="false"
              :clear-on-select="false"
              :preserve-search="true"
              placeholder="Select tags"
              label="tag_name"
              track-by="tag_name"
              @input="handleSearch"
              :max-height="300"
              :show-labels="false"
            >
              <template #tag="{ option, remove }">
                <span class="custom-tag">
                  {{ option.tag_name }}
                  <span class="custom-tag-remove" @click="remove(option)"
                    >&times;</span
                  >
                </span>
              </template>
              <template #option="{ option }">
                <span>{{ option.tag_name }}</span>
                <small v-if="option.tag_description" class="text-muted">
                  - {{ option.tag_description }}
                </small>
              </template>
            </multiselect>
      </div>
      </div>
      </div>

  <!-- Results Section -->
      <div class="results-container">
        <div v-if="isLoading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        <div v-else class="card-container">
      <UserCard
            v-for="profile in searchResults"
            :key="profile.id"
            :id="profile.user.id"
            :first_name="profile.first_name"
            :last_name="profile.last_name"
            :city="profile.city"
            :state="profile.state"
            :country="profile.country"
            :description="profile.description"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserCard from "@/components/search/UserCard.vue";
import searchService from "@/services/searchService";
import Multiselect from "vue-multiselect";

export default {
  name: "SearchPage",
  components: {
    UserCard,
    Multiselect,
  },
  data() {
    return {
      searchParams: {
        q: "",
        user_type: "",
        location: "",
      },
      selectedTags: [],
      availableTags: [],
      searchResults: [],
      isLoading: false,
      error: null,
      searchTimeout: null,
    };
  },
  created() {
    this.loadTags();
  },
  methods: {
    debounce(func, wait) {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        func.apply(this);
      }, wait);
    },
    handleSearch() {
      this.debounce(this.performSearch, 300);
    },
    async loadTags() {
      try {
        this.availableTags = await searchService.getTags();
      } catch (error) {
        console.error("Error loading tags:", error);
        this.error = "Failed to load tags. Please try again.";
      }
    },
    async performSearch() {
      this.isLoading = true;
      this.error = null;

      try {
        const params = {
          ...this.searchParams,
          tags: this.selectedTags.map((tag) => tag.tag_name),
        };

        this.searchResults = await searchService.searchProfiles(params);
      } catch (error) {
        this.error = "An error occurred while searching. Please try again.";
        console.error("Search error:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
  beforeUnmount() {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }
  },
};
</script>

<style>
@import "vue-multiselect/dist/vue-multiselect.css";

.search-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-input input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 15px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filters select,
.filters input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}

.tags-select {
  flex-grow: 1;
  min-width: 200px;
}

.results-container {
  margin-top: 20px;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

/* Custom styling for vue-multiselect */
.custom-tag {
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 100px;
  padding: 4px 12px;
  margin-right: 4px;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
}

.custom-tag-remove {
  margin-left: 8px;
  cursor: pointer;
  font-weight: bold;
  color: #1976d2;
}

.custom-tag-remove:hover {
  color: #dc3545;
}

/* Override vue-multiselect default styles */
.multiselect {
  min-height: 40px;
}

.multiselect__tags {
  min-height: 40px;
  padding: 8px 40px 0 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.multiselect__tag {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 100px;
}

.multiselect__option--highlight {
  background: #e3f2fd;
  color: #1976d2;
}

.multiselect__option--selected.multiselect__option--highlight {
  background: #dc3545;
  color: white;
}

.text-muted {
  color: #666;
  font-size: 12px;
  margin-left: 4px;
}
</style>
