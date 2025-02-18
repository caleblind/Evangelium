<template>
  <div class="registration-container">
    <div class="registration-card">
      <h1>Create Your Account</h1>
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

          <label for="tags">Select Tags:</label>
          <select id="tags" v-model="form.tags" multiple>
            <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
              {{ tag.tag_name }}
            </option>
          </select>

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
        <button type="submit">Sign Up</button>
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
      availableTags: [],
    };
  },
  methods: {
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
    // Calls the profiles endpoint to register the user
    async registerUser() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/profiles/",
          this.form
        );
        this.message = "Registration successful!";
        console.log("Registration response:", response.data);

        // Redirects to login page after successful registration
        setTimeout(() => {
          this.$router.push("/AppLogin");
        }, 1000); // Optional delay for user to read the success message
      } catch (error) {
        console.error("Registration failed:", error.response?.data);
        this.message = "Registration failed. Please try again.";
      }
    },
  },
  // Fetches all the predefined tags on page load
  mounted() {
    this.fetchTags();
  },
};
</script>

<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: #f4f7fc;
  padding: 20px;
}

.registration-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.form-title {
  text-align: center;
  margin-bottom: 15px;
  font-size: 1rem;
  font-weight: bold;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
}

input,
select,
textarea {
  width: 100%;
  padding: 14px;
  border: 2.3px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  transition: border 0.3s ease-in-out;
}

input:focus,
select:focus,
textarea:focus {
  border-color: black;
  outline: none;
}

button {
  background-color: black;
  color: white;
  padding: 15px 25px;
  border: 2px solid black;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 30px;
}

button:hover {
  background-color: white;
  color: black;
  border-color: black;
}

button:active {
  transform: translateY(1px);
}

.message {
  margin-top: 15px;
  font-weight: bold;
  color: #333;
}
</style>
