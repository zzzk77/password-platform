<template>
  <div class="timeline">
    <div 
      v-for="(item, index) in items" 
      :key="index"
      class="timeline-item"
    >
      <div class="timeline-time">{{ item.time }}</div>
      <div class="timeline-content">
        <div class="timeline-event">{{ item.event }}</div>
        <div v-if="item.description" class="timeline-description">
          {{ item.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  }
})
</script>

<style scoped>
.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
  padding-left: 20px;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -25px;
  top: 4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary-color);
  border: 2px solid var(--bg-color);
}

.timeline-time {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.timeline-event {
  font-size: 14px;
  color: var(--text-color);
  font-weight: 500;
}

.timeline-description {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}
</style>



