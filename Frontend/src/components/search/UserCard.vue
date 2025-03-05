<template>
  <div class="user-card">
    <div class="user-info">
      <h3>{{ first_name }} {{ last_name }}</h3>
      <p class="location">{{ formatLocation }}</p>
      <p class="description">{{ description || "No description available" }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserCard",
  props: {
    first_name: {
      type: String,
      required: true,
    },
    last_name: {
      type: String,
      required: true,
    },
    city: {
      type: String,
      default: "",
    },
    state: {
      type: String,
      default: "",
    },
    country: {
      type: String,
      default: "",
    },
    description: {
      type: String,
      default: "",
    },
  },
  computed: {
    formatLocation() {
      const parts = [this.city, this.state, this.country].filter(Boolean);
      return parts.length > 0 ? parts.join(", ") : "Location not specified";
    },
  },
};
</script>

<style scoped>
.user-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.user-card:hover {
  transform: translateY(-2px);
}

.user-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  color: #333;
}

.location {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 10px 0;
}

.description {
  color: #444;
  font-size: 0.95rem;
  line-height: 1.4;
  margin: 0;
}
</style>
