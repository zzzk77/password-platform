<template>
  <div class="path-visualization">
    <div class="nodes">
      <div 
        v-for="(node, index) in nodes" 
        :key="node.id" 
        class="node-wrapper"
        :class="{ active: activeNodeId === node.id, compromised: compromisedNodes.includes(node.id) }"
      >
        <div class="node">
          <el-icon :size="24"><component :is="node.icon" /></el-icon>
          <span class="label">{{ node.label }}</span>
        </div>
        <div v-if="index < nodes.length - 1" class="connection">
          <div class="line" :class="{ active: activeConnectionIndex === index }"></div>
          <el-icon v-if="activeConnectionIndex === index" class="arrow"><Right /></el-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Right, User, Monitor, Lock, Coin } from '@element-plus/icons-vue'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => [
      { id: 'attacker', label: 'Attacker', icon: 'User' },
      { id: 'firewall', label: 'Firewall', icon: 'Lock' },
      { id: 'web', label: 'Web Server', icon: 'Monitor' },
      { id: 'db', label: 'Database', icon: 'Coin' }
    ]
  },
  activeNodeId: {
    type: String,
    default: ''
  },
  compromisedNodes: {
    type: Array,
    default: () => []
  },
  activeConnectionIndex: {
    type: Number,
    default: -1
  }
})
</script>

<style scoped>
.path-visualization {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  overflow-x: auto;
}

.nodes {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 600px;
}

.node-wrapper {
  display: flex;
  align-items: center;
}

.node {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  background: white;
  border: 2px solid #dcdfe6;
  border-radius: 8px;
  width: 100px;
  transition: all 0.3s;
}

.node-wrapper.active .node {
  border-color: var(--primary-color);
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.node-wrapper.compromised .node {
  border-color: #f56c6c;
  background-color: #fef0f0;
}

.connection {
  display: flex;
  align-items: center;
  margin: 0 20px;
  position: relative;
  width: 100px;
}

.line {
  height: 2px;
  background: #dcdfe6;
  width: 100%;
  transition: all 0.3s;
}

.line.active {
  background: var(--primary-color);
  height: 3px;
}

.arrow {
  position: absolute;
  right: 0;
  color: var(--primary-color);
  animation: moveArrow 1s infinite;
}

@keyframes moveArrow {
  0% { transform: translateX(-10px); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateX(0); opacity: 0; }
}
</style>
