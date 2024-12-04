<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Company Name and Copyright -->
      <div class="footer-brand">
        <h2 class="company-name">Salt-N-Light</h2>
        <p class="copyright">© 2024 Your Company. All rights reserved.</p>
      </div>

      <!-- Navigation Links -->
      <nav class="footer-nav">
        <ul>
          <li><a href="#about-us">About Us</a></li>
          <li><a href="#services">Services</a></li>
          <li><a href="#team">The Team</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </nav>

      <!-- Help Section -->
      <div class="footer-help">
        <h3>Need Help?</h3>
        <ul>
          <li><a href="#support">Contact Support</a></li>
          <li><a href="#feedback">Give Feedback</a></li>
          <li><a href="#faq">FAQs</a></li>
        </ul>
      </div>

      <!-- Team Section -->
      <div class="footer-team">
        <h3>Get to Know Us</h3>
        <ul>
          <li><a href="#our-story">Our Story</a></li>
          <li><a href="#careers">Careers</a></li>
          <li><a href="#blog">Blog</a></li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterBar",
};
</script>

<style scoped>
.footer {
  background-color: #333;
  color: #fff;
  padding: 20px 0;
  font-family: Arial, sans-serif;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 0 20px;
  gap: 20px;
}

.footer-brand {
  flex: 1 1 100%;
  text-align: center;
}

.company-name {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.copyright {
  font-size: 0.9rem;
}

.footer-nav ul,
.footer-help ul,
.footer-team ul {
  list-style: none;
  padding: 0;
}

.footer-nav ul li,
.footer-help ul li,
.footer-team ul li {
  margin: 5px 0;
}

.footer-nav a,
.footer-help a,
.footer-team a {
  color: #ddd;
  text-decoration: none;
}

.footer-nav a:hover,
.footer-help a:hover,
.footer-team a:hover {
  color: #fff;
  text-decoration: underline;
}

.footer-nav {
  flex: 1 1 100%;
  text-align: center;
}

.footer-help,
.footer-team {
  flex: 1 1 100%;
  text-align: center;
}

h3 {
  margin-bottom: 10px;
  font-size: 1.2rem;
}

/* Media Queries for Mobile Responsiveness */
@media (min-width: 768px) {
  .footer-container {
    flex-wrap: nowrap;
    text-align: left;
  }

  .footer-brand {
    flex: 1 1 auto;
    text-align: left;
  }

  .footer-nav,
  .footer-help,
  .footer-team {
    flex: 1 1 auto;
  }
}

@media (max-width: 767px) {
  .footer-container {
    flex-direction: column;
    gap: 10px;
  }

  .footer-nav ul,
  .footer-help ul,
  .footer-team ul {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .footer-nav ul li,
  .footer-help ul li,
  .footer-team ul li {
    margin: 0;
  }

  h3 {
    font-size: 1rem;
  }

  .footer-nav a,
  .footer-help a,
  .footer-team a {
    font-size: 0.9rem;
  }
}
</style>
