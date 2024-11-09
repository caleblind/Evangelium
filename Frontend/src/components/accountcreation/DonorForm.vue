<template>
  <div class="donor-form">
    <h2>Donor Form</h2>
    <label for="name">Name:</label>
    <input type="text" v-model="donor.name" id="name" placeholder="Your Name" />

    <label for="donation">Amount you want to donate:</label>
    <input
      type="number"
      v-model="donor.donationAmount"
      id="donation"
      placeholder="Donation Amount"
    />

    <label for="donationMethod">Preferred Donation Method:</label>
    <select v-model="donor.donationMethod" id="donationMethod">
      <option value="credit_card">Credit Card</option>
      <option value="paypal">PayPal</option>
      <option value="bank_transfer">Bank Transfer</option>
    </select>

    <button @click="submitForm">Submit</button>
  </div>
</template>

<script>
export default {
  name: "DonorForm",
  data() {
    return {
      donor: {
        name: "",
        donationAmount: "",
        donationMethod: "credit_card",
      },
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
