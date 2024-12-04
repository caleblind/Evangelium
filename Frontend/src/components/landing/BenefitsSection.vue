<template>
  <section class="benefits-section">
    <div class="benefits-content-container">
      <div class="text-content">
        <h2>Benefits</h2>
        <h1>Experience a New Way to Connect and Collaborate</h1>
      </div>
      <div class="three-cards-section">
        <div class="card">
          <h2>Connect with Like-Minded Churches or Missionaries</h2>
          <p>Find missionaries and supporters who align with your values!</p>
        </div>
        <div class="card">
          <h2>Personnalized Recommendations</h2>
          <p>
            A carefully tailored algorithm will connect you to ministry partners
          </p>
        </div>
        <div class="card">
          <h2>Easy Search and Explore</h2>
          <p>
            Search our accurate and ever expanding directory of churches and
            missionaries
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "BenefitsSection",
};
</script>

<style scoped>
.benefits-section {
  width: 1440px; /* Fixed width */
  height: 782px; /* Fixed height */
  position: absolute; /* Allows positioning with 'top' */
  top: 1466px; /* Positioned 1466px from the top of the container */
  padding: 120px 0 0 0; /* Padding: 120px top, 0px for right, bottom, and left */
  gap: 10px; /* Space between child elements */
  opacity: 1; /* Opacity set to fully visible */
  display: flex; /* Flexbox layout */
  justify-content: center; /* Centers content horizontally */
  align-items: center; /* Centers content vertically */
  background-color: #f9f9f9; /* Optional background color for clarity */
  margin: 0 auto; /* Centers the section horizontally */
}

.benefits-content-container {
  display: flex; /* Flex layout for content alignment */
  flex-direction: column; /* Stack content vertically */
  align-items: center; /* Center-align text and cards */
}

.text-content {
  text-align: center; /* Center text within the section */
  margin-bottom: 20px; /* Adds spacing below the text */
}

.text-content h2 {
  font-size: 1rem;
  margin: 0; /* Remove default margins for consistency */
}

.text-content h1 {
  font-size: 2.5rem;
  margin: 10px 0; /* Adds spacing between h2 and h1 */
}

.three-cards-section {
  display: flex; /* Use Flexbox for layout */
  justify-content: space-between; /* Space cards evenly */
  width: 100%; /* Ensure cards span the container width */
  gap: 10px; /* Adds spacing between cards */
}

.card {
  width: 30%; /* Adjust as needed to fit 3 cards */
  height: 200px; /* Example height for the cards */
  background-color: #e0e0e0; /* Example background color */
  border-radius: 8px; /* Optional rounded corners */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional shadow for cards */
}
</style>
