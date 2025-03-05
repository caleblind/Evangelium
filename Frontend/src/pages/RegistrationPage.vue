<template>
  <div class="registration-container">
    <div class="registration-card">
      <h1>Create Your Account</h1>

      <!-- Progress Bar -->
      <div class="progress-container">
        <div
          class="progress-bar"
          :style="{ width: progressPercentage + '%' }"
        ></div>
        <div class="step-indicators">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="step-indicator"
            :class="{
              active: currentStep >= index,
              completed: currentStep > index,
            }"
            @click="goToStep(index)"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-label">{{ step.label }}</div>
          </div>
        </div>
      </div>

      <form @submit.prevent="registerUser">
        <!-- Step 1: Account Information -->
        <div v-show="currentStep === 0" class="form-step">
          <h2 class="step-title">Account Information</h2>
          <div class="form-group">
            <label for="username">
              <span class="required">*</span> Username:
              <span class="required-text">required</span>
            </label>
            <input
              type="text"
              id="username"
              v-model="form.user.username"
              required
              placeholder="Choose a unique username"
            />

            <label for="email">
              <span class="required">*</span> Email:
              <span class="required-text">required</span>
            </label>
            <input
              type="email"
              id="email"
              v-model="form.user.email"
              required
              placeholder="Enter your email address"
            />

            <label for="password">
              <span class="required">*</span> Password:
              <span class="required-text">required</span>
            </label>
            <input
              type="password"
              id="password"
              v-model="form.user.password"
              required
              @blur="validatePassword"
              placeholder="Create a secure password"
            />

            <label for="confirmPassword">
              <span class="required">*</span> Confirm Password:
              <span class="required-text">required</span>
            </label>
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

            <!-- Add note about required fields -->
            <div class="info-message">
              <span class="info-icon">ℹ️</span>
              These account details are required. The following steps are
              optional but help complete your profile.
            </div>
          </div>
        </div>

        <!-- Step 2: Personal Information -->
        <div v-show="currentStep === 1" class="form-step">
          <h2 class="step-title">Personal Information</h2>
          <div class="form-group">
            <label for="userType">User Type:</label>
            <select id="userType" v-model="form.user_type">
              <option value="">Select User Type (optional)</option>
              <option value="Missionary">Missionary</option>
              <option value="Supporter">Supporter</option>
            </select>

            <div class="form-row">
              <div class="form-col">
                <label for="firstName">First Name:</label>
                <input
                  type="text"
                  id="firstName"
                  v-model="form.first_name"
                  placeholder="Enter your first name"
                />
              </div>
              <div class="form-col">
                <label for="lastName">Last Name:</label>
                <input
                  type="text"
                  id="lastName"
                  v-model="form.last_name"
                  placeholder="Enter your last name"
                />
              </div>
            </div>

            <label for="denomination">Denomination:</label>
            <input
              type="text"
              id="denomination"
              v-model="form.denomination"
              placeholder="Enter your religious denomination"
            />

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
          </div>
        </div>

        <!-- Step 3: Location Information -->
        <div v-show="currentStep === 2" class="form-step">
          <h2 class="step-title">Location Information</h2>
          <div class="form-group">
            <div class="address-section">
              <label for="streetAddress">Street Address:</label>
              <input
                type="text"
                id="streetAddress"
                v-model="form.street_address"
                ref="streetAddressInput"
                placeholder="Enter your street address"
              />
              <div
                v-if="suggestions.address.length > 0"
                class="suggestions-list"
              >
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
              <div class="form-col">
                <label for="city">City:</label>
                <input
                  type="text"
                  id="city"
                  v-model="form.city"
                  ref="cityInput"
                  placeholder="Enter your city"
                />
                <div
                  v-if="suggestions.city.length > 0"
                  class="suggestions-list"
                >
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

              <div class="form-col">
                <label for="state">State:</label>
                <input
                  type="text"
                  id="state"
                  v-model="form.state"
                  ref="stateInput"
                  placeholder="Enter your state"
                />
                <div
                  v-if="suggestions.state.length > 0"
                  class="suggestions-list"
                >
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
              <select
                id="country"
                v-model="form.country"
                class="country-select"
              >
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
          </div>
        </div>

        <!-- Step 4: Additional Information -->
        <div v-show="currentStep === 3" class="form-step">
          <h2 class="step-title">Additional Information</h2>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea
              id="description"
              v-model="form.description"
              placeholder="Tell us about yourself and your mission"
              rows="4"
            ></textarea>

            <label for="profilePicture">Profile Picture URL:</label>
            <input
              type="text"
              id="profilePicture"
              v-model="form.profile_picture"
              placeholder="Enter URL for your profile picture"
            />

            <label for="tags">Select Tags:</label>
            <div class="tags-container">
              <select id="tags" v-model="form.tags" multiple>
                <option
                  v-for="tag in availableTags"
                  :key="tag.id"
                  :value="tag.id"
                >
                  {{ tag.tag_name }}
                </option>
              </select>
              <p class="helper-text">
                Hold Ctrl (or Cmd on Mac) to select multiple tags
              </p>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="form-navigation">
          <button
            v-if="currentStep > 0"
            type="button"
            class="btn-secondary"
            @click="prevStep"
          >
            Previous
          </button>

          <!-- Skip to Final Step button - only visible in steps 0-2 when account info is valid -->
          <button
            v-if="
              currentStep < steps.length - 1 &&
              currentStep !== steps.length - 2 &&
              isStepOneValid()
            "
            type="button"
            class="btn-skip"
            @click="skipToFinal"
          >
            Skip to Final Step
          </button>

          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            class="btn-primary"
            @click="nextStep"
          >
            Next
          </button>
          <button
            v-if="currentStep === steps.length - 1"
            type="submit"
            class="btn-submit"
            :disabled="!isFormValid"
          >
            Create Account
          </button>
        </div>
      </form>

      <p
        v-if="message"
        :class="{ 'success-message': isSuccess, 'error-message': !isSuccess }"
      >
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

/* global google */

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
        other_country: "",
        phone_number: "",
        years_of_experience: null,
        description: "",
        profile_picture: "",
      },
      confirmPassword: "",
      passwordsDoNotMatch: false,
      message: "",
      isSuccess: false,
      availableTags: [],
      suggestions: {
        address: [],
        city: [],
        state: [],
      },
      autocompleteService: null,
      placesService: null,
      currentStep: 0,
      steps: [
        { label: "Account" },
        { label: "Personal" },
        { label: "Location" },
        { label: "Additional" },
      ],
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
    progressPercentage() {
      return (this.currentStep / (this.steps.length - 1)) * 100;
    },
  },
  methods: {
    // Navigation methods
    nextStep() {
      if (this.currentStep === 0 && !this.isStepOneValid()) {
        return;
      }
      if (this.currentStep < this.steps.length - 1) {
        this.currentStep++;
      }
    },
    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    },
    goToStep(step) {
      // Only allow going to completed steps or the next available step
      if (step <= this.currentStep + 1) {
        this.currentStep = step;
      }
    },
    isStepOneValid() {
      const { username, email, password } = this.form.user;
      const isValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        this.confirmPassword.trim() &&
        !this.passwordsDoNotMatch;

      if (!isValid) {
        this.message = "Please complete all required fields before proceeding.";
        this.isSuccess = false;
      } else {
        this.message = "";
      }

      return isValid;
    },

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
        this.isSuccess = true;
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
        this.isSuccess = false;
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

    skipToFinal() {
      this.currentStep = this.steps.length - 1;
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
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.registration-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  color: #333;
  font-weight: 600;
  font-size: 2rem;
}

.step-title {
  text-align: left;
  font-size: 1.4rem;
  margin-bottom: 20px;
  color: #333;
  font-weight: 500;
}

/* Progress Bar */
.progress-container {
  margin-bottom: 30px;
  position: relative;
  height: 80px;
}

.progress-bar {
  height: 4px;
  background: #4caf50;
  position: absolute;
  top: 30px;
  left: 0;
  transition: width 0.3s ease;
}

.step-indicators {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
  z-index: 1;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #757575;
  font-weight: bold;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.step-label {
  font-size: 0.8rem;
  color: #757575;
  transition: color 0.3s ease;
}

.step-indicator.active .step-number {
  background: #4caf50;
  color: white;
}

.step-indicator.active .step-label {
  color: #4caf50;
  font-weight: 500;
}

.step-indicator.completed .step-number {
  background: #4caf50;
  color: white;
}

/* Form Styling */
.form-step {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  text-align: left;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-col {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 500;
  margin-bottom: 5px;
  color: #555;
  font-size: 0.95rem;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background-color: #f9f9f9;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #4caf50;
  outline: none;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 15px center;
  background-size: 15px;
  padding-right: 40px;
}

select[multiple] {
  height: 120px;
  padding: 10px;
}

.tags-container {
  position: relative;
}

.helper-text {
  font-size: 0.8rem;
  color: #757575;
  margin-top: 5px;
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.required {
  color: #f44336;
  margin-right: 3px;
}

.required-text {
  color: #9e9e9e;
  font-size: 0.8rem;
  font-style: italic;
  margin-left: 5px;
}

.error-border {
  border-color: #f44336;
}

.error-message {
  color: #f44336;
  font-size: 0.9rem;
  margin-top: 5px;
}

.success-message {
  color: #4caf50;
  font-weight: 500;
  margin-top: 15px;
}

/* Address Autocomplete */
.address-section {
  position: relative;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 5px;
}

.suggestion-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.9rem;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

/* Navigation Buttons */
.form-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  gap: 10px;
}

button {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
}

.btn-primary:hover {
  background-color: #43a047;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #555;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

.btn-submit {
  background-color: #2196f3;
  color: white;
}

.btn-submit:hover {
  background-color: #1e88e5;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-skip {
  background-color: #ff9800;
  color: white;
  margin-right: auto;
  margin-left: 10px;
}

.btn-skip:hover {
  background-color: #f57c00;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

button:disabled {
  background-color: #e0e0e0;
  color: #9e9e9e;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Info Message */
.info-message {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 12px 15px;
  margin-top: 10px;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #0d47a1;
  display: flex;
  align-items: center;
}

.info-icon {
  margin-right: 8px;
  font-size: 1.1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .registration-card {
    padding: 25px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .step-label {
    display: none;
  }

  .progress-container {
    height: 60px;
  }
}
</style>
