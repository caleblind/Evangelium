<template>
  <div class="donor-form">
    <h2>Donor Form</h2>
    <label for="name">Full Name:</label>
    <input type="text" v-model="donor.name" id="name" placeholder="Your Name" />

    <label for="donation">Amount you want to donate:</label>
    <input
      type="number"
      v-model="donor.donationAmount"
      id="donation"
      placeholder="Donation Amount"
    />

    <label for="birthdayMonth">Month:</label>
    <select v-model="donor.birthdayMonth" id="birthdayMonth">
      <option value="" disabled selected>Select a month</option>
      <!-- Placeholder -->
      <option value="January">January</option>
      <option value="February">February</option>
      <option value="March">March</option>
      <option value="April">April</option>
      <option value="May">May</option>
      <option value="June">June</option>
      <option value="July">July</option>
      <option value="August">August</option>
      <option value="September">September</option>
      <option value="October">October</option>
      <option value="November">November</option>
      <option value="December">December</option>
    </select>

    <label for="birthdayDay">Day:</label>
    <select v-model="donor.birthdayDay" id="birthdayDay">
      <option value="" disabled selected>Select a day</option>
      <!-- Dynamically generate day options from 1 to 31 -->
      <option v-for="day in days" :key="day" :value="day">{{ day }}</option>
    </select>

    <label for="birthdayYear">Year:</label>
    <select v-model="donor.birthdayYear" id="birthdayYear">
      <option value="" disabled selected>Select a year</option>
      <!-- Dynamically generate year options from 1900 to current year -->
      <option v-for="year in years" :key="year" :value="year">
        {{ year }}
      </option>
    </select>

    <p>
      Selected Date: {{ donor.birthdayMonth }} {{ donor.birthdayDay }},
      {{ donor.birthdayYear }}
    </p>

    <label for="region">Choose a region:</label>
    <select v-model="selectedRegion" id="region">
      <option v-for="region in regions" :key="region" :value="region">
        {{ region }}
      </option>
    </select>

    <label for="country">Choose a country:</label>
    <select v-model="selectedCountry" id="country" :disabled="!selectedRegion">
      <option
        v-for="country in filteredCountries"
        :key="country"
        :value="country"
      >
        {{ country }}
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
        donationAmount: "",
        birthdayMonth: "", // Initially empty or full with holding value
        birthdayDay: "", // Holds the selected day
        birthdayYear: "", // Holds the selected year
      },

      // region options
      selectedRegion: "", // Holds the selected region
      regions: ["North America", "Europe", "Asia", "Africa", "Australia"],

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
      // days and years logical features
      days: Array.from({ length: 31 }, (_, i) => i + 1), // Days from 1 to 31
      years: Array.from(
        { length: currentYear - 1900 + 1 },
        (_, i) => currentYear - i
      ), // Years from 1900 to current year
    };
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
