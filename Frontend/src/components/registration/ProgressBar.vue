<template>
  <div class="progress-container">
    <div
      class="progress-bar"
      :style="{ width: progressPercentage + '%' }"
    ></div>
    <div class="step-indicators">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step-indicator"
        :class="{
          active: currentStep >= index,
          completed: currentStep > index,
        }"
        @click="$emit('go-to-step', index)"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-label">{{ step.label }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: {
    steps: {
      type: Array,
      required: true,
    },
    currentStep: {
      type: Number,
      required: true,
    },
  },
  emits: ["go-to-step"],
  computed: {
    progressPercentage() {
      return (this.currentStep / (this.steps.length - 1)) * 100;
    },
  },
};
</script>
