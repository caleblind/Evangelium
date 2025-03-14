<template>
  <div class="form-step">
    <h2 class="step-title">Account Information</h2>
    <div class="form-group">
      <label for="username">
        <span class="required">*</span> Username:
        <span class="required-text">required</span>
      </label>
      <input
        type="text"
        id="username"
        v-model="localUserData.username"
        required
        placeholder="Choose a unique username"
        @input="validateUsername"
      />
      <p v-if="usernameError" class="error-message">
        {{ usernameError }}
      </p>

      <label for="email">
        <span class="required">*</span> Email:
        <span class="required-text">required</span>
      </label>
      <input
        type="email"
        id="email"
        v-model="localUserData.email"
        required
        placeholder="Enter your email address"
        @input="validateEmail"
      />
      <p v-if="emailError" class="error-message">
        {{ emailError }}
      </p>

      <label for="password">
        <span class="required">*</span> Password:
        <span class="required-text">required</span>
      </label>
      <input
        type="password"
        id="password"
        v-model="localUserData.password"
        required
        @blur="validatePassword"
        placeholder="Create a secure password"
        @input="updateUserData"
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
        These account details are required. The following steps are optional but
        help complete your profile.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AccountInfoStep",
  props: {
    userData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:userData", "password-validation"],
  data() {
    return {
      localUserData: {
        username: this.userData.username || "",
        email: this.userData.email || "",
        password: this.userData.password || "",
      },
      confirmPassword: "",
      passwordsDoNotMatch: false,
      usernameError: "",
      emailError: "",
    };
  },
  methods: {
    validateUsername() {
      const alphanumericRegex = /^[a-zA-Z0-9]+$/;
      if (!alphanumericRegex.test(this.localUserData.username)) {
        this.usernameError = "Username can only contain letters and numbers";
        this.$emit("password-validation", false);
      } else {
        this.usernameError = "";
        this.validateAll();
      }
      this.updateUserData();
    },

    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.localUserData.email)) {
        this.emailError = "Please enter a valid email address";
        this.$emit("password-validation", false);
      } else {
        this.emailError = "";
        this.validateAll();
      }
      this.updateUserData();
    },

    validateAll() {
      const isValid =
        !this.usernameError &&
        !this.emailError &&
        !this.passwordsDoNotMatch &&
        this.localUserData.username &&
        this.localUserData.email &&
        this.localUserData.password;
      this.$emit("password-validation", isValid);
    },

    validatePassword() {
      this.passwordsDoNotMatch =
        this.localUserData.password !== this.confirmPassword;
      this.validateAll();
    },

    updateUserData() {
      console.log(
        "AccountInfoStep - updateUserData called",
        this.localUserData
      );
      this.$emit("update:userData", { ...this.localUserData });
    },
  },
  watch: {
    userData: {
      handler(newValue) {
        this.localUserData = { ...newValue };
      },
      deep: true,
    },
    "localUserData.password": {
      handler() {
        this.validatePassword();
      },
    },
    confirmPassword: {
      handler() {
        this.validatePassword();
      },
    },
  },
  mounted() {
    console.log("AccountInfoStep mounted", this.userData);
  },
};
</script>
