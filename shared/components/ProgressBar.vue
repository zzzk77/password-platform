<template>
  <div class="progress-container">
    <div class="progress-info">
      <span class="progress-label">{{ label }}</span>
      <span class="progress-value">{{ value }}%</span>
    </div>
    <div class="progress-bar">
      <div 
        class="progress-bar-fill" 
        :style="{ width: value + '%', backgroundColor: color }"
      ></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: '进度'
  },
  value: {
    type: Number,
    default: 0,
    validator: (v) => v >= 0 && v <= 100
  },
  color: {
    type: String,
    default: 'var(--primary-color)'
  }
})
</script>

<style scoped>
.progress-container {
  width: 100%;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.progress-label {
  color: var(--text-secondary);
}

.progress-value {
  color: var(--text-color);
  font-weight: 500;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  transition: width 0.3s ease;
}
</style>



