<template>
  <div class="search-page">
    <!-- Top Navigation Bar -->
    <header class="top-nav">
      <div class="nav-left">
        <router-link to="/" class="logo">SnL</router-link>
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="Search..." />
          <div class="selected-tags">
            <div v-for="tag in selectedTags" :key="tag" class="tag">
              {{ tag }}
              <button @click="removeTag(tag)" class="remove-tag">×</button>
            </div>
          </div>
        </div>
      </div>
      <nav class="nav-right">
        <router-link to="/" class="nav-item">Home</router-link>
        <router-link to="/explore" class="nav-item active">Explore</router-link>
        <router-link to="/calendar" class="nav-item">Calendar</router-link>
        <router-link to="/saved" class="nav-item">Saved</router-link>
        <div class="user-menu">
          <img :src="userAvatar" alt="User" class="avatar" />
          <span>Me ▼</span>
        </div>
      </nav>
    </header>

    <div class="main-content">
      <!-- Left Sidebar -->
      <aside class="profile-sidebar">
        <div class="profile-card">
          <div class="profile-header">
            <img :src="userProfile.image" alt="Profile" class="profile-image" />
            <div class="country-flag">🇺🇸</div>
          </div>
          <h2>{{ userProfile.name }}</h2>
          <p class="role">{{ userProfile.role }}</p>

          <div class="interests-section">
            <div class="section-header">
              <h3>Your Interests</h3>
              <button class="edit-button">✎</button>
            </div>
            <div class="tags-grid">
              <span v-for="tag in userProfile.tags" :key="tag" class="tag">{{
                tag
              }}</span>
            </div>
            <button class="see-all">See all</button>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="search-results">
        <!-- Tabs -->
        <div class="tabs">
          <button
            class="tab"
            :class="{ active: activeTab === 'churches' }"
            @click="activeTab = 'churches'"
          >
            Churches
          </button>
          <button
            class="tab"
            :class="{ active: activeTab === 'missionaries' }"
            @click="activeTab = 'missionaries'"
          >
            Missionaries
          </button>
        </div>

        <!-- Advanced Search -->
        <div class="advanced-search">
          <h2>Advanced Search</h2>
          <div class="search-form">
            <div class="form-group">
              <label>Contains</label>
              <input
                type="text"
                v-model="filters.contains"
                placeholder="Search for names, places, or interests"
              />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Denomination</label>
                <select v-model="filters.denomination">
                  <option value="">-Select a denomination-</option>
                  <option
                    v-for="denom in denominations"
                    :key="denom"
                    :value="denom"
                  >
                    {{ denom }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label>Mission Field</label>
                <select v-model="filters.missionField">
                  <option value="">-Select a field-</option>
                  <option
                    v-for="field in missionFields"
                    :key="field"
                    :value="field"
                  >
                    {{ field }}
                  </option>
                </select>
              </div>
            </div>
            <button class="search-button" @click="handleSearch">Search</button>
          </div>
        </div>

        <!-- Results Section -->
        <div class="results-section">
          <h2>Results in "{{ searchQuery }}"</h2>
          <div class="results-grid">
            <div
              v-for="result in filteredResults"
              :key="result.id"
              class="result-card"
            >
              <img
                :src="result.image"
                :alt="result.name"
                class="result-image"
              />
              <div class="result-content">
                <div class="result-header">
                  <div class="result-title">
                    <h3>{{ result.name }}</h3>
                    <p class="location">
                      {{ result.city }}, {{ result.state }},
                      {{ result.country }}
                    </p>
                  </div>
                  <button class="bookmark-button">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                      ></path>
                    </svg>
                  </button>
                </div>
                <p class="description">{{ result.description }}</p>
                <div class="result-tags">
                  <span v-for="tag in result.tags" :key="tag" class="tag">{{
                    tag
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchPage",
  data() {
    return {
      searchQuery: "",
      selectedTags: ["Community Outreach", "Church Planting"],
      activeTab: "churches",
      userProfile: {
        name: "John Smith",
        role: "Missionary",
        image: "/path/to/profile-image.jpg",
        tags: [
          "Baptist",
          "Community Outreach",
          "Men's Ministry",
          "Church Planting",
          "Worship & Music Ministry",
        ],
      },
      filters: {
        contains: "",
        denomination: "",
        missionField: "",
      },
      denominations: [
        "Baptist",
        "Catholic",
        "Protestant",
        "Non-Denominational",
      ],
      missionFields: ["Youth", "Education", "Medical", "Community"],
      results: [],
      userAvatar: "/path/to/avatar.jpg",
      tagMap: {}, // Map of tag IDs to tag names
    };
  },
  computed: {
    filteredResults() {
      return this.results.map((result) => ({
        ...result,
        tags: result.tags.map(
          (tagId) => this.tagMap[tagId]?.tag_name || "Unknown Tag"
        ),
      }));
    },
  },
  methods: {
    removeTag(tag) {
      this.selectedTags = this.selectedTags.filter((t) => t !== tag);
    },
    async handleSearch() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profiles/",
          {
            params: {
              search: this.searchQuery,
              ...this.filters,
            },
          }
        );
        this.results = response.data;
      } catch (error) {
        console.error("Search failed:", error);
      }
    },
    async fetchTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/");
        // Create a map of tag IDs to tag objects
        this.tagMap = response.data.reduce((acc, tag) => {
          acc[tag.id] = tag;
          return acc;
        }, {});
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
    },
  },
  async mounted() {
    await this.fetchTags();
    await this.handleSearch();
  },
};
</script>

<style scoped>
.search-page {
  min-height: 100vh;
  background-color: #f4f7fc;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}

.search-bar {
  position: relative;
  width: 400px;
}

.search-bar input {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.selected-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: #e3f2fd;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #1976d2;
}

.remove-tag {
  margin-left: 0.25rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-item {
  text-decoration: none;
  color: #666;
}

.nav-item.active {
  color: #1976d2;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.main-content {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.profile-sidebar {
  width: 300px;
  flex-shrink: 0;
}

.profile-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-header {
  position: relative;
  margin-bottom: 1rem;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.country-flag {
  position: absolute;
  bottom: 0;
  right: 0;
  font-size: 1.5rem;
}

.interests-section {
  margin-top: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.edit-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.see-all {
  width: 100%;
  padding: 0.5rem;
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.search-results {
  flex-grow: 1;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab.active {
  color: #1976d2;
  border-bottom-color: #1976d2;
}

.advanced-search {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button {
  padding: 0.75rem;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.results-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.result-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.result-content {
  padding: 1.25rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.result-title h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.25rem 0;
}

.location {
  font-size: 0.875rem;
  color: #666;
  margin: 0;
}

.bookmark-button {
  background: none;
  border: none;
  padding: 0;
  color: #666;
  cursor: pointer;
}

.bookmark-button:hover {
  color: #1976d2;
}

.description {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
</style>
