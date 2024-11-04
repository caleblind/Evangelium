<template>
  <div class="signuppage">
    <!-- Displays progress bar dynamically-->
    <ProgressBarSection />

    <!-- Displays signup form dynamically-->
    <FormSection />
  </div>
</template>

<script>
import ProgressBarSection from "@/components/signup/ProgressBarSection.vue";
import FormSection from "@/components/signup/FormSection.vue";

export default {
  name: "SignUpPage",
  components: {
    ProgressBarSection,
    FormSection,
  },
};
</script>
