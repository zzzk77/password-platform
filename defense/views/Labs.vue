<template>
  <div class="labs-container">
    <div class="page-header">
      <h2>靶场搭建</h2>
      <div class="actions">
        <el-select v-model="filters.type" placeholder="类型" style="width: 160px" clearable>
          <el-option v-for="t in types" :key="t" :label="t" :value="t" />
        </el-select>
        <el-select v-model="filters.level" placeholder="难度" style="width: 140px" clearable>
          <el-option label="基础" value="基础" />
          <el-option label="进阶" value="进阶" />
          <el-option label="核心" value="核心" />
        </el-select>
        <el-input v-model="filters.q" placeholder="搜索名称或描述" style="width: 240px" />
        <el-button type="primary" @click="load">刷新</el-button>
        <el-button type="success" @click="aiQuickBuild">AI一键搭建</el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col v-for="item in filtered" :key="item.id" :span="8">
        <el-card class="lab-card" shadow="hover">
          <div class="lab-header">
            <div class="title">{{ item.name }}</div>
            <el-tag type="info">{{ item.type }}</el-tag>
          </div>
          <div class="desc">{{ item.desc }}</div>
          <div class="meta">
            <el-tag :type="difficultyTag(item.difficulty)">难度 {{ item.difficulty }}</el-tag>
            <el-tag :type="item.status === '运行中' ? 'success' : 'warning'">{{ item.status }}</el-tag>
          </div>
          <div class="ops">
            <el-button type="primary" @click="start(item)" :disabled="item.status === '运行中'">搭建</el-button>
            <el-button @click="stop(item)" :disabled="item.status !== '运行中'">停止</el-button>
            <el-button text type="primary" @click="preview(item)">预览拓扑</el-button>
            <el-button type="success" plain @click="aiBuild(item)">AI智能搭建</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="topologyVisible" title="拓扑预览" width="520px">
      <div class="topology">
        <div class="node" v-for="n in currentTopo.nodes || []" :key="n.id">{{ n.label || n.id }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/utils/api'
import { ElMessage } from 'element-plus'

const list = ref([])
const filters = ref({ type: '', level: '', q: '' })
const types = ['密码生成', '密码存储', '密码传输', '密码验证', '算法攻防', '综合攻防']

const load = async () => {
  try {
    list.value = await api.get('/api/scenes')
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

const filtered = computed(() => {
  return list.value.filter(s => {
    const matchType = !filters.value.type || s.type.startsWith(filters.value.type)
    const levelWord = s.type.includes('·') ? s.type.split('·')[1] : ''
    const matchLevel = !filters.value.level || levelWord === filters.value.level || (filters.value.level === '核心' && s.type.includes('核心'))
    const matchQ = !filters.value.q || `${s.name}${s.desc}${s.type}`.includes(filters.value.q)
    return matchType && matchLevel && matchQ
  })
})

const start = async (item) => {
  try {
    const updated = await api.put(`/api/scenes/${item.id}`, { status: '运行中' })
    Object.assign(item, updated)
    ElMessage.success('已开始搭建')
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const stop = async (item) => {
  try {
    const updated = await api.put(`/api/scenes/${item.id}`, { status: '已停止' })
    Object.assign(item, updated)
    ElMessage.success('已停止')
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const aiQuickBuild = async () => {
  try {
    const desc = filters.value.q || '自动生成密码攻防靶场'
    const scene = await api.post('/api/scenes/ai-generate', { description: desc, preset: 'AI自动生成场景' })
    list.value.unshift(scene)
    ElMessage.success('AI已生成并启动新靶场')
  } catch (e) {
    ElMessage.error('AI生成失败')
  }
}

const topologyVisible = ref(false)
const currentTopo = ref({})
const preview = (item) => {
  currentTopo.value = item.topology || {}
  topologyVisible.value = true
}

const difficultyTag = (d) => d >= 4 ? 'danger' : d >= 3 ? 'warning' : 'success'

const aiBuild = async (item) => {
  const t = item.type || ''
  const nodes = []
  const edges = []
  if (t.includes('密码生成')) {
    nodes.push({ id: 'web', label: 'Web服务器' }, { id: 'redis', label: 'Redis' })
    edges.push({ from: 'web', to: 'redis' })
  } else if (t.includes('密码存储')) {
    nodes.push({ id: 'web', label: 'Web服务器' }, { id: 'db', label: '数据库' }, { id: 'backup', label: '备份服务器' })
    edges.push({ from: 'web', to: 'db' }, { from: 'db', to: 'backup' })
  } else if (t.includes('密码传输')) {
    nodes.push({ id: 'client', label: '客户端' }, { id: 'web', label: 'Web服务器' }, { id: 'waf', label: 'WAF' })
    edges.push({ from: 'client', to: 'web' }, { from: 'web', to: 'waf' })
  } else if (t.includes('密码验证')) {
    nodes.push({ id: 'web', label: 'Web服务器' }, { id: 'auth', label: '认证服务' }, { id: 'rate', label: '速率限制' })
    edges.push({ from: 'web', to: 'auth' }, { from: 'web', to: 'rate' })
  } else if (t.includes('算法攻防')) {
    nodes.push({ id: 'web', label: 'Web服务器' }, { id: 'db', label: '数据库' }, { id: 'dc', label: '域控制器' }, { id: 'waf', label: 'WAF' })
    edges.push({ from: 'web', to: 'db' }, { from: 'web', to: 'waf' }, { from: 'waf', to: 'dc' })
  } else {
    nodes.push({ id: 'web', label: 'Web服务器' }, { id: 'db', label: '数据库' }, { id: 'cache', label: '缓存' }, { id: 'waf', label: 'WAF' }, { id: 'mq', label: '消息队列' })
    edges.push({ from: 'web', to: 'db' }, { from: 'web', to: 'cache' }, { from: 'web', to: 'waf' }, { from: 'web', to: 'mq' })
  }
  try {
    const updated = await api.put(`/api/scenes/${item.id}`, { status: '运行中', topology: { nodes, edges } })
    Object.assign(item, updated)
    ElMessage.success('AI已完成搭建')
  } catch (e) {
    ElMessage.error('AI搭建失败')
  }
}

onMounted(load)
</script>

<style scoped>
.labs-container {
  padding: 20px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.actions {
  display: flex;
  gap: 10px;
}
.lab-card {
  margin-bottom: 20px;
}
.lab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.title {
  font-weight: 600;
  color: var(--text-color);
}
.desc {
  color: var(--text-secondary);
  min-height: 40px;
}
.meta {
  display: flex;
  gap: 10px;
  margin: 10px 0;
}
.ops {
  display: flex;
  gap: 10px;
}
.topology {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.node {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 12px;
}
</style>
