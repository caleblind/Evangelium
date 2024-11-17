<template>
  <div class="search-page">
    <FilterComponent :onUpdateFilters="updateFilters" />
    <SearchResults :results="searchResults" />
  </div>
</template>

<script>
import axios from "axios";
import FilterComponent from "@/components/search/FilterComponent.vue";
import SearchResults from "@/components/search/SearchResults.vue";
import Tags from "@/components/search/Tags.vue";

export default {
  name: "SearchPage",
  components: {
    FilterComponent,
    SearchResults,
  },
  data() {
    return {
      searchResults: [], // Stores API search results
      currentFilters: {}, // Tracks applied filters
      isLoading: false, // Loading state for API calls
      error: null, // Error state for handling API errors
    };
  },
  methods: {
    updateFilters(filters) {
      this.currentFilters = filters;
      this.fetchSearchResults();
    },
    fetchSearchResults() {
      this.isLoading = true;
      this.error = null;

      const params = new URLSearchParams(this.currentFilters).toString();

      axios
        .get(`/api/search?${params}`)
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          this.error = "Failed to load search results.";
          console.error("API Error:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  mounted() {
    // Initial load with no filters
    this.fetchSearchResults();
  },
};
</script>

<style scoped>
.search-page {
  padding: 20px;
}
</style>
