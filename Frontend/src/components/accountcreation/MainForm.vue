<template>
  <div class="form-container">
    <h2>Are you a Missionary or Donor?</h2>
    <div class="button-container">
      <button @click="selectRole('missionary')">Missionary</button>
      <button @click="selectRole('donor')">Donor</button>
    </div>

    <div v-if="roleSelected" class="user-details">
      <h3>Enter your details</h3>
      <div>
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Enter your email"
          aria-label="Email address"
        />
      </div>
      <div>
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter your password"
          aria-label="Password"
        />
        <span v-if="password && password.length < 8" class="error-text"
          >Password must be at least 8 characters long.</span
        >
      </div>
      <div>
        <label for="phonenumber">Phone Number:</label>
        <input
          type="tel"
          id="phonenumber"
          v-model="phonenumber"
          placeholder="Enter your phone number"
          aria-label="Phone number"
        />
      </div>

      <button :disabled="isSubmitting" @click="submitForm">
        {{ isSubmitting ? "Submitting..." : "Submit" }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MainForm",
  data() {
    return {
      roleSelected: null,
      email: "",
      password: "",
      phonenumber: "",
      isSubmitting: false,
    };
  },
  methods: {
    async submitForm() {
      if (!this.email || !this.password || !this.roleSelected) {
        alert("Please fill in all fields and select a role.");
        return;
      }

      // Check if email is valid
      if (!/\S+@\S+\.\S+/.test(this.email)) {
        alert("Please enter a valid email.");
        return;
      }

      // Check password length
      if (this.password.length < 8) {
        alert("Password must be at least 8 characters long.");
        return;
      }

      this.isSubmitting = true;
      const formData = {
        email: this.email,
        password: this.password,
        user_type: this.roleSelected,
        phone_number: this.phonenumber,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/register/",
          formData,
          {
            headers: { "Content-Type": "application/json" },
          }
        );
        console.log("User form submitted successfully:", response.data);
        alert("Form submitted successfully!");
        this.roleSelected === "missionary"
          ? this.goToMissionaryForm()
          : this.goToDonorForm();
        this.resetForm();
      } catch (error) {
        console.error("Error submitting form:", error);
        alert("There was an error submitting the form. Please try again.");
      } finally {
        this.isSubmitting = false;
      }
    },

    goToMissionaryForm() {
      this.$emit("next-step", "missionary");
    },

    goToDonorForm() {
      this.$emit("next-step", "donor");
    },

    resetForm() {
      this.email = "";
      this.password = "";
      this.phonenumber = "";
      this.roleSelected = null;
    },

    selectRole(role) {
      this.roleSelected = role;
    },
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 20px;
}

.button-container {
  display: flex;
  flex-direction: row;
  gap: 10px;
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

.user-details {
  margin-top: 20px;
}

label {
  margin-right: 10px;
}

input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
}

.error-text {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}
</style>
