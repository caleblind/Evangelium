<template>
  <div class="missionary-form">
    <h2>Create A Profile That Tells Your Story!</h2>
    <h3>Don't worry, you can update this information later</h3>
    <label for="name">Full Name:</label>
    <input
      type="text"
      v-model="missionary.name"
      id="name"
      placeholder="Your Name"
    />

    <!-- Get the Missionaries Birthday, month, day then year -->
    <label for="birthdayMonth">Month:</label>
    <select v-model="missionary.birthdayMonth" id="birthdayMonth">
      <option value="" disabled selected>Select a month</option>
      <option v-for="month in months" :key="month" :value="month">
        {{ month }}
      </option>
    </select>

    <label for="birthdayDay">Day:</label>
    <select v-model="missionary.birthdayDay" id="birthdayDay">
      <option value="" disabled selected>Select a day</option>
      <!-- Dynamically generate day options from 1 to 31 -->
      <option v-for="day in days" :key="day" :value="day">{{ day }}</option>
    </select>

    <label for="birthdayYear">Year:</label>
    <select v-model="missionary.birthdayYear" id="birthdayYear">
      <option value="" disabled selected>Select a year</option>
      <!-- Dynamically generate year options from 1900 to current year -->
      <option v-for="year in years" :key="year" :value="year">
        {{ year }}
      </option>
    </select>

    <!-- display the birth date -->
    <p>
      Selected Date: {{ missionary.birthdayMonth }}
      {{ missionary.birthdayDay }},
      {{ missionary.birthdayYear }}
    </p>

    <label for="region">Choose a region:</label>
    <select v-model="selectedRegion" id="region">
      <option value="" disabled selected>Select a region</option>
      <!-- Placeholder option -->
      <option v-for="region in regions" :key="region" :value="region">
        {{ region }}
      </option>
    </select>

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

    <!-- State Dropdown -->
    <label for="state">State:</label>
    <select id="state" v-model="selectedState" :disabled="!selectedCountry">
      <option value="" disabled>Select a state</option>
      <option v-for="state in filteredStates" :key="state" :value="state">
        {{ state }}
      </option>
    </select>

    <!-- Bio Field -->
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

    <!-- choose denomination dropdown -->
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

    <!-- retrieving the mission field -->
    <label for="missionField">Mission Field:</label>
    <select v-model="missionary.missionField" id="missionField">
      <option value="" disabled selected>Select a Mission Field</option>
      <option
        v-for="missionField in missionFields"
        :key="missionField"
        :value="missionField"
      >
        {{ missionField }}
      </option>
      <option value="Custom">Other (Specify Below)</option>
    </select>

    <!-- Input field appears if "Custom" is selected -->
    <div v-if="missionary.missionField === 'Custom'">
      <label for="customMissionField">Specify Mission Field:</label>
      <input
        type="text"
        v-model="missionary.customMissionField"
        id="customMissionField"
        placeholder="Enter your mission field"
      />
    </div>

    <button @click="submitForm">Submit</button>
  </div>
</template>

<script>
export default {
  name: "MissionaryForm",
  data() {
    const currentYear = new Date().getFullYear();
    return {
      missionary: {
        name: "",
        birthdayMonth: "", // Initially empty or full with holding value
        birthdayDay: "", // Holds the selected day
        birthdayYear: "", // Holds the selected year
      },

      missionaryField: {
        missionField: "", // Predefined or Custom option
        customMissionField: "", // For specifying a custom mission field
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

      // birthday logical features
      months: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ],

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
      console.log("missionary form submitted:", this.missionary);
      // Here, you could also emit an event to notify the parent component about the form submission.
    },
  },
};
</script>

<style scoped>
.missionary-form {
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
