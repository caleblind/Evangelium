<template>
  <div class="search-page">
    <!-- User Type Filters -->
    <div class="filter-buttons">
      <button
        :class="['filter-button', { active: !userTypeFilter }]"
        @click="setUserTypeFilter('')"
      >
        All
      </button>
      <button
        :class="['filter-button', { active: userTypeFilter === 'missionary' }]"
        @click="setUserTypeFilter('missionary')"
      >
        Missionaries
      </button>
      <button
        :class="['filter-button', { active: userTypeFilter === 'supporter' }]"
        @click="setUserTypeFilter('supporter')"
      >
        Supporters
      </button>
    </div>

    <!-- Search Component -->
    <UserSearch
      ref="userSearch"
      :filters="['location', 'tags']"
      :initial-filters="{
        userType: userTypeFilter,
      }"
      @search-results="handleSearchResults"
      @search-error="handleError"
    >
      <template #results="{ results, isLoading, hasSearched }">
        <div v-if="isLoading" class="loading-state">Searching...</div>
        <div v-else-if="results.length > 0" class="results-grid">
          <ProfileCard
            v-for="result in results"
            :key="result.id"
            :result="result"
            :tag-map="tagMap"
            @card-click="navigateToProfile"
          >
          </ProfileCard>
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
import ProfileCard from "@/components/shared/ProfileCard.vue";
import { searchService } from "@/services/searchService";

export default {
  name: "SearchPage",
  components: {
    UserSearch,
    ProfileCard,
  },
  data() {
    return {
      userTypeFilter: "",
      tagMap: {}, // Map to store tag details
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    navigateToProfile(profile) {
      this.$router.push(`/profile/${profile.id}`);
    },
    setUserTypeFilter(userType) {
      this.userTypeFilter = userType;
      if (this.$refs.userSearch) {
        this.$refs.userSearch.detailedFilters.userType = userType;
        this.$refs.userSearch.handleDetailedSearch();
      }
    },
    handleSearchResults(results) {
      console.log(
        "Search results (detailed):",
        JSON.stringify(results, null, 2)
      );
      results.forEach((result) => {
        console.log(
          "Profile ID:",
          result.id,
          "Name:",
          result.first_name,
          result.last_name
        );
      });
    },
    handleError(error) {
      console.error("Search error:", error);
    },
    async fetchTags() {
      try {
        const tags = await searchService.fetchTags();
        this.tagMap = tags.reduce((acc, tag) => {
          acc[tag.id] = tag.tag_name;
          return acc;
        }, {});
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
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

.filter-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.filter-button {
  padding: 8px 20px;
  font-size: 14px;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-button:hover {
  border-color: #4285f4;
  color: #4285f4;
}

.filter-button.active {
  background: #4285f4;
  color: white;
  border-color: #4285f4;
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
