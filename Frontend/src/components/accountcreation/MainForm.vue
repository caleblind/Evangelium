<template>
  <div class="form-container">
    <h2>Are you a Missionry or Donor?</h2>
    <button @click="goToMissionaryForm">Missionary</button>
    <button @click="goToDonorForm">Donor</button>
  </div>
</template>

<script>
export default {
  name: "MainForm",
  methods: {
    goToMissionaryForm() {
      this.$emit("next-step", "missionary");
    },
    goToDonorForm() {
      this.$emit("next-step", "donor");
    },
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  padding: 10px 20px;
  margin: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
