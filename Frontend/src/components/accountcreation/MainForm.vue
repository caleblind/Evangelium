<template>
  <div class="form-container">
    <h2>Are you a Missionry or Donor?</h2>
    <div class="button-container">
      <button @click="goToMissionaryForm">Missionary</button>
      <button @click="goToDonorForm">Donor</button>
    </div>
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
  flex-direction: column; /* Keeps the heading and buttons vertically aligned */
  align-items: center;
  text-align: center; /* Center the text of the question */
}

.button-container {
  display: flex;
  flex-direction: row; /* Align buttons horizontally */
  gap: 10px; /* Adds space between the buttons */
}

button {
  padding: 10px 20px;
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
