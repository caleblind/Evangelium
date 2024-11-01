<template>
  <div class="app">
    <HeroSection />
    <AboutUsSection />
    <BenefitsSection />
  </div>
</template>

<script>
import HeroSection from "@/components/landing/HeroSection.vue";
import AboutUsSection from "@/components/landing/AboutUsSection.vue";
import BenefitsSection from "@/components/landing/BenefitsSection.vue";

export default {
  name: "LandingPage",
  components: {
    HeroSection,
    AboutUsSection,
    BenefitsSection,
  },
};
</script>
