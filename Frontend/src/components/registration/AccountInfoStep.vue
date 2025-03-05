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
        @input="updateUserData"
      />

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
        @input="updateUserData"
      />

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
    };
  },
  methods: {
    validatePassword() {
      this.passwordsDoNotMatch =
        this.localUserData.password !== this.confirmPassword;
      this.$emit("password-validation", !this.passwordsDoNotMatch);
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
    "localUserData.password"() {
      this.validatePassword();
    },
    confirmPassword() {
      this.validatePassword();
    },
  },
  mounted() {
    console.log("AccountInfoStep mounted", this.userData);
  },
};
</script>
