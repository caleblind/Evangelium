<template>
  <div class="donor-form">
    <h2>Create A Profile That Tells Your Story!</h2>
    <h2>This is my donor file</h2>
    <h3>Don't worry, you can update this information later</h3>
    <label for="name">Full Name:</label>
    <input type="text" v-model="donor.name" id="name" placeholder="Your Name" />

    <!-- Input field for Donor region of operation-->
    <label for="region">Choose a region:</label>
    <select v-model="selectedRegion" id="region">
      <option value="" disabled selected>Select a region</option>
      <!-- Placeholder option -->
      <option v-for="region in regions" :key="region" :value="region">
        {{ region }}
      </option>
    </select>

    <!-- Input field for Donor Country-->
    <label for="country">Choose a country:</label>
    <select v-model="selectedCountry" id="country" :disabled="!selectedRegion">
      <option value="" disabled selected>Select a region</option>
      <option
        v-for="country in filteredCountries"
        :key="country"
        :value="country"
      >
        {{ country }}
      </option>
    </select>

    <!--Input field for Donor State Dropdown -->
    <label for="state">State:</label>
    <select id="state" v-model="selectedState" :disabled="!selectedCountry">
      <option value="" disabled>Select a state</option>
      <option v-for="state in filteredStates" :key="state" :value="state">
        {{ state }}
      </option>
    </select>

    <!-- Input field for Donor Bio Field -->
    <label for="bio">Bio:</label>
    <textarea
      id="bio"
      v-model="bio"
      :maxlength="bioMaxLength"
      placeholder="Share your story, your journey, and the impact you hope to make"
    ></textarea>
    <p class="char-count">
      {{ bioMaxLength - bio.length }} characters remaining
    </p>

    <!-- Input fielf for Denomination -->
    <label for="denomination">Choose a denomination:</label>
    <select v-model="selectedDenomination" id="denomination">
      <option
        v-for="denomination in denomination"
        :key="denomination"
        :value="denomination"
      >
        {{ denomination }}
      </option>
    </select>

    <button @click="submitForm">Submit</button>
  </div>
</template>

<script>
export default {
  name: "DonorForm",
  data() {
    const currentYear = new Date().getFullYear();
    return {
      donor: {
        name: "",
      },

      // bio format
      bio: "", // Bio input
      bioMaxLength: 300, // Character limit for bio

      // region options
      selectedRegion: "", // Holds the selected region
      regions: ["North America", "Europe", "Asia", "Africa", "Australia"],

      // denomination options
      selectedDenomination: "", // Holds the selected region
      denomination: [
        "Southern Baptist",
        "Indipendant Baptist",
        "National Baptist Convention",
        "Missionary Baptist",
        "Free Will Baptist",
      ],

      // country options
      selectedCountry: "", // Holds the selected country
      countries: {
        // Countries categorized by regions
        "North America": ["USA", "Canada", "Mexico"],
        Europe: ["Germany", "France", "UK", "Spain"],
        Asia: ["China", "India", "Japan", "South Korea"],
        Africa: ["Nigeria", "Egypt", "South Africa"],
        Australia: ["Australia", "New Zealand"],
      },

      // State options
      selectedState: "",
      states: {
        USA: ["California", "New York", "Texas", "Florida", "Other"],
        Canada: ["Ontario", "Quebec", "British Columbia", "Other"],
        Mexico: ["Jalisco", "Nuevo León", "Chiapas", "Other"],
        Germany: ["Bavaria", "Berlin", "Saxony", "Other"],
        // Add more countries with states as needed
      },

      // days and years logical features
      days: Array.from({ length: 31 }, (_, i) => i + 1), // Days from 1 to 31
      years: Array.from(
        { length: currentYear - 1900 + 1 },
        (_, i) => currentYear - i
      ), // Years from 1900 to current year

      // mission field options
      missionFields: [
        "North America",
        "South America",
        "Europe",
        "Asia",
        "Africa",
        "Australia",
      ],
    };
  },

  computed: {
    // Computed properties go here
    filteredCountries() {
      return this.countries[this.selectedRegion] || [];
    },
    filteredStates() {
      return this.states[this.selectedCountry] || [];
    },
  },

  methods: {
    submitForm() {
      console.log("Donor form submitted:", this.donor);
      // Here, you could also emit an event to notify the parent component about the form submission.
    },
  },
};
</script>

<style scoped>
.donor-form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
}

input,
select {
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
