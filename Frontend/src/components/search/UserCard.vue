<template>
  <div classes="card_container">
    <h2>{{ first_name }}</h2>
    <p>Contact: {{ description }}</p>
  </div>
</template>

<script>
export default {
  name: "UserCard",
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.card_container {
  display: flex;
  width: 283px;
  height: fit-content;
  padding: 12px;
  align-items: center;
  gap: 12px;
  border-radius: 8px;
  background: #ffff00;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card_info {
  display: flex;
  align-items: center;
  gap: 12px;
  align-self: stretch;
}

.card_picture {
  display: flex;
  width: 77px;
  height: 70px;
  align-items: center;
}

.card_tags-container {
  display: flex;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.card_pills {
  display: flex;
  padding: 4px 4px;
  justify-content: center;
  align-items: center;
  border-radius: 100px;
}

.card-flag {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  fill: #d9d9d9;
  stroke-width: 1px;
  stroke: #fff;
  font-size: 18px;
}
</style>
