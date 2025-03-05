<template>
  <div class="form-step">
    <h2 class="step-title">Personal Information</h2>
    <div class="form-group">
      <label for="userType">User Type:</label>
      <select id="userType" v-model="localData.user_type" @change="updateData">
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
            v-model="localData.first_name"
            placeholder="Enter your first name"
            @input="updateData"
          />
        </div>
        <div class="form-col">
          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="localData.last_name"
            placeholder="Enter your last name"
            @input="updateData"
          />
        </div>
      </div>

      <label for="denomination">Denomination:</label>
      <input
        type="text"
        id="denomination"
        v-model="localData.denomination"
        placeholder="Enter your religious denomination"
        @input="updateData"
      />

      <label for="phoneNumber">Phone Number:</label>
      <input
        type="text"
        id="phoneNumber"
        v-model="localData.phone_number"
        placeholder="Enter your phone number"
        @input="updateData"
      />

      <label for="yearsOfExperience">Years of Experience:</label>
      <input
        type="number"
        id="yearsOfExperience"
        v-model="localData.years_of_experience"
        placeholder="Enter your years of experience"
        @input="updateData"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "PersonalInfoStep",
  props: {
    personalData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:personalData"],
  data() {
    return {
      localData: {
        user_type: this.personalData.user_type || "",
        first_name: this.personalData.first_name || "",
        last_name: this.personalData.last_name || "",
        denomination: this.personalData.denomination || "",
        phone_number: this.personalData.phone_number || "",
        years_of_experience: this.personalData.years_of_experience || null,
      },
    };
  },
  methods: {
    /* Updates parent with current personal information values */
    updateData() {
      this.$emit("update:personalData", {
        ...this.personalData,
        ...this.localData,
      });
    },
  },
  watch: {
    /* Syncs local data when parent data changes */
    personalData: {
      handler(newValue) {
        this.localData = {
          user_type: newValue.user_type || "",
          first_name: newValue.first_name || "",
          last_name: newValue.last_name || "",
          denomination: newValue.denomination || "",
          phone_number: newValue.phone_number || "",
          years_of_experience: newValue.years_of_experience || null,
        };
      },
      deep: true,
    },
  },
};
</script>
