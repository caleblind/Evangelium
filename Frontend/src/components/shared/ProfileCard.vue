<template>
  <div class="result-card" @click="handleCardClick">
    <img
      :src="
        result.profile_picture ||
        require('@/assets/pictures/defaultProfilePicture.png')
      "
      :alt="result.name"
      class="result-image"
    />
    <div class="result-content">
      <h3>{{ result.first_name }} {{ result.last_name }}</h3>
      <div class="meta-info">
        <span v-if="result.user_type" class="user-type">{{
          formatUserType(result.user_type)
        }}</span>
        <span v-if="result.denomination" class="denomination">{{
          result.denomination
        }}</span>
      </div>
      <p class="location">{{ formatLocation(result) }}</p>
      <p class="description">{{ result.description }}</p>
      <div class="tags">
        <span v-for="tag in result.tags" :key="tag" class="tag">
          {{ getTagName(tag) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileCard",
  props: {
    result: {
      type: Object,
      required: true,
    },
    tagMap: {
      type: Object,
      required: true,
    },
  },
  methods: {
    handleCardClick() {
      this.$emit("card-click", this.result);
    },
    formatLocation(result) {
      const parts = [result.city, result.state, result.country]
        .filter(Boolean)
        .join(", ");
      return parts || "Location not specified";
    },
    getTagName(tagId) {
      return this.tagMap[tagId] || "Unknown Tag";
    },
    formatUserType(userType) {
      if (!userType) return "Unknown Type";
      return userType === "other"
        ? "Church"
        : userType.charAt(0).toUpperCase() + userType.slice(1);
    },
  },
};
</script>

<style scoped>
.result-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
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

.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.user-type {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: 500;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
}

.denomination {
  background: #f5f5f5;
  color: #666;
  font-style: italic;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
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
</style>
