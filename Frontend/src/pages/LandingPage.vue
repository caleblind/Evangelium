<template>
  <div class="landingpage">
    <HeroSection />
    <AboutUsSection />
    <BenefitsSection />
  </div>
</template>

<script>
import HeroSection from "@/components/landing/HeroSection.vue";
import AboutUsSection from "@/components/landing/AboutUsSection.vue";

export default {
  name: "LandingPage",
  components: {
    HeroSection,
    AboutUsSection,
  },
};
</script>
