<template>
  <span :class="['status-badge', `status-${type}`]">
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (v) => ['success', 'warning', 'danger', 'info'].includes(v)
  },
  text: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-success {
  background: rgba(16, 185, 129, 0.2);
  color: #10B981;
}

.status-warning {
  background: rgba(245, 158, 11, 0.2);
  color: #F59E0B;
}

.status-danger {
  background: rgba(239, 68, 68, 0.2);
  color: #EF4444;
}

.status-info {
  background: rgba(22, 93, 255, 0.2);
  color: #165DFF;
}
</style>



