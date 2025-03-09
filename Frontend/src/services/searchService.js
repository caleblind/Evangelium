import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const searchService = {
  async quickSearch(query) {
    const params = new URLSearchParams();
    if (query) {
      params.append("search", query);
    }
    const response = await axios.get(
      `${API_BASE_URL}/api/profiles/?${params.toString()}`
    );
    return response.data;
  },

  async detailedSearch(filters) {
    const params = new URLSearchParams();

    if (filters.name) {
      params.append("name", filters.name);
    }
    if (filters.userType) {
      params.append("user_type", filters.userType);
    }
    if (filters.denomination) {
      params.append("denomination", filters.denomination);
    }
    if (filters.city) {
      params.append("city", filters.city);
    }
    if (filters.state) {
      params.append("state", filters.state);
    }
    if (filters.country) {
      params.append("country", filters.country);
    }
    if (filters.tags && filters.tags.length > 0) {
      filters.tags.forEach((tag) => {
        params.append("tags", tag);
      });
    }

    const response = await axios.get(
      `${API_BASE_URL}/api/profiles/detailed-search/?${params.toString()}`
    );
    return response.data.results;
  },

  async fetchTags() {
    const response = await axios.get(`${API_BASE_URL}/tag/`);
    return response.data;
  },

  processResults(data) {
    return data.map((result) => ({
      ...result,
      first_name: result.first_name || result.user?.username || "Unknown",
      last_name: result.last_name || "",
      tags: result.tags || [],
    }));
  },
};
