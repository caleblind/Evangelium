<template>
  <div class="registration">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="form.user.username" required />

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
      <input type="text" id="profilePicture" v-model="form.profile_picture" />

      <button type="submit">Register</button>
    </form>

    <p v-if="message">{{ message }}</p>
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
        tags: [], // Empty array for tags
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
