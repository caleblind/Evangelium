import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  async searchProfiles(params) {
    try {
      const queryParams = new URLSearchParams();

      if (params.q) queryParams.append("q", params.q);
      if (params.user_type) queryParams.append("user_type", params.user_type);
      if (params.location) queryParams.append("location", params.location);
      if (params.tags && params.tags.length) {
        params.tags.forEach((tag) => queryParams.append("tags", tag));
      }

      const response = await axios.get(
        `${API_URL}/api/profiles/search/?${queryParams.toString()}`
      );
      return response.data;
    } catch (error) {
      console.error("Error searching profiles:", error);
      throw error;
    }
  },

  async getTags() {
    try {
      const response = await axios.get(`${API_URL}/tag/`);
      // Sort tags alphabetically by tag_name
      const tags = response.data.sort((a, b) =>
        a.tag_name.localeCompare(b.tag_name)
      );
      return tags;
    } catch (error) {
      console.error("Error fetching tags:", error);
      throw error;
    }
  },
};
