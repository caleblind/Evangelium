<template>
  <div class="progress-bar">
    <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: {
    currentStep: {
      type: Number,
      required: true,
    },
    totalSteps: {
      type: Number,
      required: true,
    },
  },
  computed: {
    progressPercentage() {
      return (this.currentStep / this.totalSteps) * 100;
    },
  },
};
</script>

<style scoped>
.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  margin-bottom: 20px;
}

.progress {
  height: 100%;
  background-color: #4caf50;
  border-radius: 5px;
}
</style>
