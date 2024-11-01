<template>
  <section class="benefits-section">
    <div class="benefits-content-container">
      <div class="text-content">
        <h2>Benefits</h2>
        <h1>Experience a New Way to Connect and Collaborate</h1>
      </div>
      <div class="three-cards-section">
        <div class="three-cards-section"></div>
        <div class="three-cards-section"></div>
        <div class="three-cards-section"></div>
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
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Arial, sans-serif;
}

.benefits-content-container {
  display: flex;
}

.text-content {
  align-content: center;
}

.text-content h2 {
  font-size: 1rem;
  align-items: center;
}

.text-content h1 {
  font-size: 2.5rem;
}

.three-cards-section {
  display: flex; /* Use Flexbox for layout */
  justify-content: space-between; /* Space sections evenly */
  margin-top: 20px; /* Space above the process sections */
}
</style>
