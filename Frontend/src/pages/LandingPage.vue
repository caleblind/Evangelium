<template>
  <div class="landingpage">
    <HeroSection />
    <AboutUsSection />
    <BenefitsSection />
    <FooterBar />
  </div>
</template>

<script>
import HeroSection from "@/components/landing/HeroSection.vue";
import AboutUsSection from "@/components/landing/AboutUsSection.vue";
import BenefitsSection from "@/components/landing/BenefitsSection.vue";
import FooterBar from "@/components/layout/FooterNav.vue";

export default {
  name: "LandingPage",
  components: {
    HeroSection,
    AboutUsSection,
    BenefitsSection,
    FooterBar,
  },
};
</script>
