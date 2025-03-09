import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const searchService = {
  async quickSearch(query) {
    const params = new URLSearchParams();
    if (query) {
      params.append("q", query);
    }
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/profiles/search/?${params.toString()}`
      );
      return response.data.results || [];
    } catch (error) {
      console.error("Quick search failed:", error);
      throw error;
    }
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
    if (filters.description) {
      params.append("description", filters.description);
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

    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/profiles/detailed-search/?${params.toString()}`
      );
      return response.data.results || [];
    } catch (error) {
      console.error("Detailed search failed:", error);
      throw error;
    }
  },

  async fetchTags() {
    try {
      const response = await axios.get(`${API_BASE_URL}/tag/`);
      return response.data;
    } catch (error) {
      console.error("Failed to fetch tags:", error);
      throw error;
    }
  },

  async fetchDenominations() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/denominations/`);
      return response.data.denominations || [];
    } catch (error) {
      console.error("Failed to fetch denominations:", error);
      throw error;
    }
  },

  processResults(data) {
    if (!Array.isArray(data)) {
      console.warn("Received non-array data:", data);
      data = data.results || [];
    }
    return data.map((result) => ({
      id: result.id,
      ...result,
      first_name: result.first_name || result.user?.username || "Unknown",
      last_name: result.last_name || "",
      denomination: result.denomination || "Not Specified",
      tags: Array.isArray(result.tags) ? result.tags : [],
      formattedTags: Array.isArray(result.tags)
        ? result.tags.map((tag) =>
            typeof tag === "object" ? tag : { id: tag, name: `Tag ${tag}` }
          )
        : [],
    }));
  },
};
