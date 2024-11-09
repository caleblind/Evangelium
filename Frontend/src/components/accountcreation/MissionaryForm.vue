<template>
  <div class="missionary-form">
    <h2>Missionary Form</h2>
    <label for="name">Name:</label>
    <input
      type="text"
      v-model="missionary.name"
      id="name"
      placeholder="Your Name"
    />

    <label for="country">Country of Mission:</label>
    <input
      type="text"
      v-model="missionary.country"
      id="country"
      placeholder="Country"
    />

    <label for="calling">Missionary Calling:</label>
    <input
      type="text"
      v-model="missionary.calling"
      id="calling"
      placeholder="Describe your calling"
    />

    <button @click="submitForm">Submit</button>
  </div>
</template>

<script>
export default {
  name: "MissionaryForm",
  data() {
    return {
      missionary: {
        name: "",
        country: "",
        calling: "",
      },
    };
  },
  methods: {
    submitForm() {
      console.log("Missionary form submitted:", this.missionary);
      // Here, you could also emit an event to notify the parent component about the form submission.
    },
  },
};
</script>

<style scoped>
.missionary-form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
}

input {
  margin-bottom: 10px;
  padding: 10px;
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  margin-top: 20px;
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
