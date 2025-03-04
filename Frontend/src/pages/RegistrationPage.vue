<template>
  <div class="registration-container">
    <div class="registration-card">
      <h1>Create Your Account</h1>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <!-- User fields for registration form  -->
          <label for="username"
            ><span class="required">*</span> Username:
            <span class="required-text">required</span></label
          >
          <input
            type="text"
            id="username"
            v-model="form.user.username"
            required
            placeholder="Choose a unique username"
          />

          <label for="email"
            ><span class="required">*</span> Email:
            <span class="required-text">required</span></label
          >
          <input
            type="email"
            id="email"
            v-model="form.user.email"
            required
            placeholder="Enter your email address"
          />

          <label for="password"
            ><span class="required">*</span> Password:
            <span class="required-text">required</span></label
          >
          <input
            type="password"
            id="password"
            v-model="form.user.password"
            required
            @blur="validatePassword"
            placeholder="Create a secure password"
          />

          <!-- Password Confirmation -->
          <label for="confirmPassword"
            ><span class="required">*</span> Confirm Password:
            <span class="required-text">required</span></label
          >
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            :class="{ 'error-border': passwordsDoNotMatch }"
            @blur="validatePassword"
            placeholder="Confirm your password"
          />
          <p v-if="passwordsDoNotMatch" class="error-message">
            Passwords do not match.
          </p>

          <!-- Profile fields for registration form -->
          <label for="tags">Select Tags:</label>
          <select id="tags" v-model="form.tags" multiple>
            <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
              {{ tag.tag_name }}
            </option>
          </select>

          <label for="userType">User Type:</label>
          <select id="userType" v-model="form.user_type">
            <option value="">Select User Type (optional)</option>
            <option value="Missionary">Missionary</option>
            <option value="Supporter">Supporter</option>
          </select>

          <label for="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            v-model="form.first_name"
            placeholder="Enter your first name"
          />

          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="form.last_name"
            placeholder="Enter your last name"
          />

          <label for="denomination">Denomination:</label>
          <input
            type="text"
            id="denomination"
            v-model="form.denomination"
            placeholder="Enter your religious denomination"
          />

          <!-- Address Fields with Google Places Autocomplete -->
          <div class="address-section">
            <label for="streetAddress">Street Address:</label>
            <input
              type="text"
              id="streetAddress"
              v-model="form.street_address"
              ref="streetAddressInput"
              placeholder="Enter your street address"
            />
            <div v-if="suggestions.address.length > 0" class="suggestions-list">
              <div
                v-for="(suggestion, index) in suggestions.address"
                :key="index"
                class="suggestion-item"
                @click="selectAddress(suggestion)"
              >
                {{ suggestion.description }}
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="city">City:</label>
              <input
                type="text"
                id="city"
                v-model="form.city"
                ref="cityInput"
                placeholder="Enter your city"
              />
              <div v-if="suggestions.city.length > 0" class="suggestions-list">
                <div
                  v-for="(suggestion, index) in suggestions.city"
                  :key="index"
                  class="suggestion-item"
                  @click="selectCity(suggestion)"
                >
                  {{ suggestion.description }}
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="state">State:</label>
              <input
                type="text"
                id="state"
                v-model="form.state"
                ref="stateInput"
                placeholder="Enter your state"
              />
              <div v-if="suggestions.state.length > 0" class="suggestions-list">
                <div
                  v-for="(suggestion, index) in suggestions.state"
                  :key="index"
                  class="suggestion-item"
                  @click="selectState(suggestion)"
                >
                  {{ suggestion.description }}
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label for="country">Country:</label>
            <select id="country" v-model="form.country" class="country-select">
              <option value="">Select your country (optional)</option>
              <option value="United States">United States</option>
              <option value="Canada">Canada</option>
              <option value="United Kingdom">United Kingdom</option>
              <option value="Australia">Australia</option>
              <option value="Philippines">Philippines</option>
              <option value="India">India</option>
              <option value="Nigeria">Nigeria</option>
              <option value="Kenya">Kenya</option>
              <option value="South Africa">South Africa</option>
              <option value="Other">Other (specify below)</option>
            </select>
            <div v-if="form.country === 'Other'" class="other-country-input">
              <input
                type="text"
                v-model="form.other_country"
                placeholder="Enter your country"
                class="mt-2"
              />
            </div>
          </div>

          <label for="phoneNumber">Phone Number:</label>
          <input
            type="text"
            id="phoneNumber"
            v-model="form.phone_number"
            placeholder="Enter your phone number"
          />

          <label for="yearsOfExperience">Years of Experience:</label>
          <input
            type="number"
            id="yearsOfExperience"
            v-model="form.years_of_experience"
            placeholder="Enter your years of experience"
          />

          <label for="description">Description:</label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="Tell us about yourself and your mission"
          ></textarea>

          <label for="profilePicture">Profile Picture URL:</label>
          <input
            type="text"
            id="profilePicture"
            v-model="form.profile_picture"
            placeholder="Enter URL for your profile picture"
          />
        </div>
        <button type="submit" :disabled="!isFormValid">Sign Up</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

/* global google */

export default {
  // Format of data sent to the backend
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
        other_country: "",
        phone_number: "",
        years_of_experience: null,
        description: "",
        profile_picture: "",
      },
      confirmPassword: "",
      passwordsDoNotMatch: false,
      message: "",
      availableTags: [],
      suggestions: {
        address: [],
        city: [],
        state: [],
      },
      autocompleteService: null,
      placesService: null,
    };
  },
  computed: {
    // Ensures that only required fields must be filled
    isFormValid() {
      const { username, email, password } = this.form.user;
      return (
        username.trim() &&
        email.trim() &&
        password.trim() &&
        this.confirmPassword.trim() &&
        !this.passwordsDoNotMatch
      );
    },
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

    // Check Password Confirmation
    validatePassword() {
      this.passwordsDoNotMatch =
        this.form.user.password !== this.confirmPassword;
    },

    // Calls the profiles endpoint to register the user
    async registerUser() {
      try {
        // Create the data in the nested format expected by the backend
        const formData = {
          user: {
            username: this.form.user.username,
            email: this.form.user.email,
            password: this.form.user.password,
          },
          tags: this.form.tags,
          user_type: this.form.user_type
            ? this.form.user_type.toLowerCase()
            : null,
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          denomination: this.form.denomination,
          street_address: this.form.street_address,
          city: this.form.city,
          state: this.form.state,
          country:
            this.form.country === "Other"
              ? this.form.other_country
              : this.form.country,
          phone_number: this.form.phone_number,
          years_of_experience: this.form.years_of_experience,
          description: this.form.description,
          profile_picture: this.form.profile_picture,
        };

        // Log the data being sent
        console.log("Registration data being sent:", formData);

        const response = await axios.post(
          "http://127.0.0.1:8000/api/profiles/",
          formData
        );
        console.log("Registration response:", response.data);

        this.message = "Registration successful!";
        setTimeout(() => this.$router.push("/AppLogin"), 1000);
      } catch (error) {
        console.error("Registration failed:", error.response?.data);
        console.error("Error status:", error.response?.status);
        console.error("Error details:", error);
        this.message =
          error.response?.data?.detail ||
          error.response?.data?.user?.username?.[0] ||
          error.response?.data?.user?.email?.[0] ||
          "Registration failed. Please try again.";
      }
    },

    // Google Places API for Address Autocomplete
    initGooglePlaces() {
      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyCzHCbngGLUj41VG6hmwFsAoUak7QwnX3k&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => {
        this.autocompleteService = new google.maps.places.AutocompleteService();
        this.placesService = new google.maps.places.PlacesService(
          document.createElement("div")
        );

        // Add input event listeners
        ["streetAddress", "city", "state"].forEach((field) => {
          this.$refs[`${field}Input`]?.addEventListener("input", (e) =>
            this.handleInput(e, field)
          );
        });
      };
      document.head.appendChild(script);
    },

    async handleInput(event, field) {
      const input = event.target.value;
      if (input.length < 2) {
        this.suggestions[field] = [];
        return;
      }

      try {
        const types = {
          streetAddress: ["address"],
          city: ["(cities)"],
          state: ["administrative_area_level_1"],
        };

        const response = await this.autocompleteService.getPlacePredictions({
          input,
          types: types[field],
        });
        this.suggestions[field] = response.predictions;
      } catch (error) {
        console.error(`Error fetching ${field} suggestions:`, error);
        this.suggestions[field] = [];
      }
    },

    selectAddress(place) {
      this.suggestions.address = [];
      this.form.street_address = place.description;

      this.placesService.getDetails(
        {
          placeId: place.place_id,
          fields: ["address_components"],
        },
        (result, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            result.address_components.forEach((component) => {
              const type = component.types[0];
              if (type === "locality") this.form.city = component.long_name;
              if (type === "administrative_area_level_1")
                this.form.state = component.long_name;
            });
          }
        }
      );
    },

    selectCity(suggestion) {
      this.suggestions.city = [];
      this.form.city = suggestion.description;
    },

    selectState(suggestion) {
      this.suggestions.state = [];
      this.form.state = suggestion.description;
    },
  },
  // Fetches all the predefined tags on page load
  mounted() {
    this.fetchTags();
    this.initGooglePlaces();
  },
  beforeUnmount() {
    // Clean up event listeners
    ["streetAddress", "city", "state"].forEach((field) => {
      this.$refs[`${field}Input`]?.removeEventListener("input", (e) =>
        this.handleInput(e, field)
      );
    });
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
  font-family: inherit;
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

.error-border {
  border: 2px solid red;
}

.error-message {
  color: red;
  font-size: 0.9rem;
}

.required {
  color: red;
  font-weight: bold;
  margin-left: 5px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.required-text {
  color: #b0b0b0;
  font-style: italic;
  font-weight: normal;
  margin-left: 5px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.address-section {
  position: relative;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

.form-group {
  position: relative;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.country-select {
  width: 100%;
  padding: 14px;
  border: 2.3px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border 0.3s ease-in-out;
  background-color: white;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
}

.country-select:focus {
  border-color: black;
  outline: none;
}

.other-country-input {
  margin-top: 8px;
}

.other-country-input input {
  width: 100%;
  padding: 14px;
  border: 2.3px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border 0.3s ease-in-out;
}

.other-country-input input:focus {
  border-color: black;
  outline: none;
}

.mt-2 {
  margin-top: 8px;
}
</style>
