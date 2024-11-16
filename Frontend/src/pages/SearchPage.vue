<template>
  <div class="search-page">
    <h1>Search Users:</h1>

    <!-- Filters Section -->
    <div class="filters">
      <!-- Role Filter -->
      <div class="filter-group">
        <label for="user_type">Role:</label>
        <select v-model="filters.user_type">
          <option value="">All</option>
          <option value="Missionary">Missionary</option>
          <option value="Supporter">Supporter</option>
        </select>
      </div>

      <!-- Tags Filter -->
      <div class="filter-group">
        <label for="tags">Tags:</label>
        <input
          type="text"
          id="tags"
          placeholder="e.g., Youth, Outreach"
          v-model="filters.tags"
        />
      </div>

      <!-- Location Filter -->
      <div class="filter-group">
        <label for="location">Location:</label>
        <input
          type="text"
          id="location"
          placeholder="Enter location"
          v-model="filters.location"
        />
      </div>

      <!-- Search Button -->
      <button @click="fetchSearchResults" class="search-button">Search</button>
    </div>

    <!-- Results Section -->
    <div class="results">
      <h2>Search Results</h2>
      <p v-if="isLoading">Loading...</p>
      <p v-if="error">{{ error }}</p>
      <ul v-if="searchResults.length > 0">
        <li v-for="result in searchResults" :key="result.id">
          <strong>{{ result.email }}</strong> - {{ result.user_type }}<br />
          <span>{{ result.description || "No description" }}</span
          ><br />
          <span>{{ result.phone_number || "No phone number" }}</span
          ><br />
          <hr />
        </li>
      </ul>
      <p v-if="!isLoading && searchResults.length === 0">No results found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchPage",
  data() {
    return {
      filters: {
        user_type: "", // Role (Missionary or Supporter)
        tags: "", // Tags to filter by
        location: "", // Location to filter by
      },
      searchResults: [], // Holds API response data
      isLoading: false, // Loading state indicator
      error: null, // Error message if request fails
    };
  },

  methods: {
    fetchSearchResults() {
      this.isLoading = true;
      this.error = null;

      // Base URL for user data
      const baseURL = "http://127.0.0.1:8000/user/";

      // Construct query parameters based on filters
      const queryParams = new URLSearchParams();

      if (this.filters.user_type) {
        queryParams.append("user_type", this.filters.user_type);
      }
      if (this.filters.tags) {
        queryParams.append("tags", this.filters.tags);
      }
      if (this.filters.location) {
        queryParams.append("location", this.filters.location);
      }

      // Full URL with query parameters
      const url = `${baseURL}?${queryParams.toString()}`;

      axios
        .get(url)
        .then((response) => {
          this.searchResults = response.data.results || response.data;
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
};
</script>

<style scoped>
.search-page {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.filters {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.filter-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-button {
  padding: 10px;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}

.results {
  margin-top: 20px;
}

.results h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px 0;
}

hr {
  border: 0;
  border-top: 1px solid #ddd;
}
</style>
