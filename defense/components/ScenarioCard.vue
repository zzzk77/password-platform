<template>
  <div class="scenario-card">
    <div class="card-header">
      <div class="card-icon">{{ scenario.icon }}</div>
      <div class="card-title">
        <h3>{{ scenario.title }}</h3>
        <div class="card-meta">
          <el-tag size="small" type="primary" effect="light">{{ scenario.category }}</el-tag>
          <el-tag size="small" :type="getLevelType(scenario.level)">{{ scenario.level }}</el-tag>
          <span class="participants">
            <el-icon><User /></el-icon>
            {{ scenario.participants }}人已练
          </span>
        </div>
      </div>
    </div>
    <div class="card-content">
      <p class="card-description">{{ scenario.description }}</p>
    </div>
    <div class="card-footer">
      <el-button type="primary" size="small" @click="handleStartTraining">
        <el-icon><VideoPlay /></el-icon>
        开始训练
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { User, VideoPlay } from '@element-plus/icons-vue'

const props = defineProps({
  scenario: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['start-training'])

const getLevelType = (level) => {
  switch (level) {
    case '初级':
      return 'success'
    case '中级':
      return 'warning'
    case '高级':
      return 'danger'
    default:
      return 'info'
  }
}

const handleStartTraining = () => {
  emit('start-training', props.scenario)
}
</script>

<style scoped>
.scenario-card {
  background-color: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
  padding: 20px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.scenario-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 18px 0 rgba(0, 0, 0, 0.4);
  border-color: var(--primary-color);
}

.card-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.card-icon {
  font-size: 40px;
  margin-right: 15px;
  flex-shrink: 0;
}

.card-title {
  flex: 1;
}

.card-title h3 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
  color: var(--text-color);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-meta .participants {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-content {
  flex: 1;
  margin-bottom: 20px;
}

.card-description {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-footer {
  text-align: center;
}

.card-footer .el-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  --el-button-bg-color: var(--primary-color);
  --el-button-border-color: var(--primary-color);
  --el-button-hover-bg-color: var(--primary-dark);
  --el-button-hover-border-color: var(--primary-dark);
}

.card-meta .el-tag {
  --el-tag-bg-color: var(--bg-light);
  --el-tag-border-color: var(--border-color);
  --el-tag-text-color: var(--text-color);
}
</style>