<template>
  <div class="AccountCreationPage">
    <ProgressBar :currentStep="currentStep" :totalSteps="totalSteps" />
    <MainForm v-if="step === 1" @next-step="handleNextStep" />
    <MissionaryForm v-if="step === 2" />
    <DonorForm v-if="step === 3" />
  </div>
</template>

<script>
import ProgressBar from "@/components/accountcreation/ProgressBar.vue";
import MissionaryForm from "@/components/accountcreation/MissionaryForm";
import DonorForm from "@/components/accountcreation/DonorForm";
import MainForm from "@/components/accountcreation/MainForm.vue";

export default {
  name: "AccountCreationPage",
  components: {
    ProgressBar,
    MainForm,
    MissionaryForm,
    DonorForm,
  },
  data() {
    return {
      step: 1, // Step 1: Form, Step 2: Missionary, Step 3: Donor
      totalSteps: 3,
    };
  },
  methods: {
    handleNextStep(userType) {
      if (userType === "missionary") {
        this.step = 2;
      } else if (userType === "donor") {
        this.step = 3;
      }
    },
  },
};
</script>

<style scoped>
.AccountCreationPage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}
</style>
