<template>
  <section id="benefits" class="benefits-section">
    <div class="benefits-content-container">
      <div class="text-content">
        <h2>Benefits</h2>
        <h1>Experience a New Way to Connect and Collaborate</h1>
      </div>
      <div class="cards-container">
        <div class="card">
          <h3>Connect</h3>
          <p>Connect with mission-driven churches and missionaries.</p>
          <router-link to="/SearchPage" class="card-btn"
            >SearchPage Now</router-link
          >
        </div>
        <div class="card">
          <h3>Join</h3>
          <p>Register to become part of our growing community.</p>
          <router-link to="/RegistrationPage" class="card-btn"
            >Register Today</router-link
          >
        </div>
        <div class="card">
          <h3>Profile</h3>
          <p>View your profile and manage your connections.</p>
          <router-link to="/UserProfile" class="card-btn"
            >View Profile</router-link
          >
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
  padding: 60px 20px;
  background-color: #fff;
  text-align: center;
}

.benefits-content-container {
  max-width: 1200px;
  margin: 0 auto;
}

.text-content h2 {
  font-size: 1rem;
  text-transform: uppercase;
  color: #333;
  margin-bottom: 10px;
}

.text-content h1 {
  font-size: 2.5rem;
  margin-bottom: 40px;
}

.cards-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

.card {
  background: #f7f7f7;
  padding: 20px;
  border-radius: 8px;
  width: 30%;
  min-width: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.card p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.card-btn {
  background-color: #000;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.card-btn:hover {
  background-color: #333;
}
</style>
