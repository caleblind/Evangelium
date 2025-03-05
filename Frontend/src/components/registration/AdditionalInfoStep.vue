<template>
  <div class="form-step">
    <h2 class="step-title">Additional Information</h2>
    <div class="form-group">
      <label for="description">Description:</label>
      <textarea
        id="description"
        v-model="localData.description"
        placeholder="Tell us about yourself and your mission"
        rows="4"
        @input="updateData"
      ></textarea>

      <label for="profilePicture">Profile Picture URL:</label>
      <input
        type="text"
        id="profilePicture"
        v-model="localData.profile_picture"
        placeholder="Enter URL for your profile picture"
        @input="updateData"
      />

      <label for="tags">Select Tags:</label>
      <div class="tags-container">
        <select
          id="tags"
          v-model="localData.tags"
          multiple
          @change="updateData"
        >
          <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
            {{ tag.tag_name }}
          </option>
        </select>
        <p class="helper-text">
          Hold Ctrl (or Cmd on Mac) to select multiple tags
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdditionalInfoStep",
  props: {
    additionalData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:additionalData"],
  data() {
    return {
      localData: {
        description: this.additionalData.description || "",
        profile_picture: this.additionalData.profile_picture || "",
        tags: this.additionalData.tags || [],
      },
      availableTags: [],
    };
  },
  mounted() {
    this.fetchTags();
  },
  methods: {
    updateData() {
      this.$emit("update:additionalData", {
        ...this.additionalData,
        ...this.localData,
      });
    },
    // Fetches predefined tags from the backend
    async fetchTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/");
        this.availableTags = response.data.filter(
          (tag) => tag.tag_is_predefined
        );
      } catch (error) {
        console.error("Failed to fetch tags:", error.response?.data);
      }
    },
  },
  watch: {
    additionalData: {
      handler(newValue) {
        this.localData = {
          description: newValue.description || "",
          profile_picture: newValue.profile_picture || "",
          tags: newValue.tags || [],
        };
      },
      deep: true,
    },
  },
};
</script>
