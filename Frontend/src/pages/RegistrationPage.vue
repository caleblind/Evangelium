<template>
  <div class="registration-container">
    <div class="registration-card">
      <h1>Register</h1>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            type="text"
            id="username"
            v-model="form.user.username"
            required
          />

          <label for="email">Email:</label>
          <input type="email" id="email" v-model="form.user.email" required />

          <label for="password">Password:</label>
          <input
            type="password"
            id="password"
            v-model="form.user.password"
            required
          />

          <label for="userType">User Type:</label>
          <input type="text" id="userType" v-model="form.user_type" />

          <label for="firstName">First Name:</label>
          <input type="text" id="firstName" v-model="form.first_name" />

          <label for="lastName">Last Name:</label>
          <input type="text" id="lastName" v-model="form.last_name" />

          <label for="denomination">Denomination:</label>
          <input type="text" id="denomination" v-model="form.denomination" />

          <label for="streetAddress">Street Address:</label>
          <input type="text" id="streetAddress" v-model="form.street_address" />

          <label for="city">City:</label>
          <input type="text" id="city" v-model="form.city" />

          <label for="state">State:</label>
          <input type="text" id="state" v-model="form.state" />

          <label for="country">Country:</label>
          <input type="text" id="country" v-model="form.country" />

          <label for="phoneNumber">Phone Number:</label>
          <input type="text" id="phoneNumber" v-model="form.phone_number" />

          <label for="yearsOfExperience">Years of Experience:</label>
          <input
            type="number"
            id="yearsOfExperience"
            v-model="form.years_of_experience"
          />

          <label for="description">Description:</label>
          <textarea id="description" v-model="form.description"></textarea>

          <label for="profilePicture">Profile Picture URL:</label>
          <input
            type="text"
            id="profilePicture"
            v-model="form.profile_picture"
          />
        </div>
        <button type="submit">Register</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: {
        user: {
          username: "",
          email: "",
          password: "",
        },
        tags: [],
        user_type: "",
        first_name: "",
        last_name: "",
        denomination: "",
        street_address: "",
        city: "",
        state: "",
        country: "",
        phone_number: "",
        years_of_experience: null,
        description: "",
        profile_picture: "",
      },
      message: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/profiles/",
          this.form
        );
        this.message = "Registration successful!";
        console.log("Registration response:", response.data);
      } catch (error) {
        console.error("Registration failed:", error.response?.data);
        this.message = "Registration failed. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Full-Screen Container */
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: white;
  padding: 20px;
  overflow-y: auto;
}

/* Registration Card */
.registration-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  text-align: center;
  max-height: 90vh;
  overflow-y: auto;
}

/* Form Layout */
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Form Groups */
.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

/* Inputs & Select */
input,
select,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border 0.3s ease-in-out;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #6a11cb;
  outline: none;
}

/* Multi-select dropdown */
select[multiple] {
  height: 120px;
  padding: 8px;
}

/* Button */
.register-btn {
  background: #6a11cb;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease-in-out;
}

.register-btn:hover {
  background: #2c60b9;
}

/* Message */
.message {
  margin-top: 15px;
  font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .registration-card {
    max-height: none;
    overflow-y: visible;
  }
}
</style>
