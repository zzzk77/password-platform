<template>
  <div class="scenarios-container">
    <div class="page-header">
      <h2>密码学挑战场景</h2>
    </div>

    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="挑战列表" name="list">
        <div class="operation-bar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索挑战名称/类型"
            prefix-icon="Search"
            style="width: 300px"
          />
          <el-button @click="handleImport">导入挑战</el-button>
        </div>

        <!-- 按密码学算法分类展示 -->
        <div v-for="category in categories" :key="category.type" style="margin-top: 30px">
          <h3 class="category-title">{{ category.name }}</h3>
          <el-row :gutter="16" style="margin-top: 15px">
            <el-col :span="8" v-for="row in getScenariosByCategory(category.type)" :key="row.id">
              <el-card class="card" shadow="hover">
                <div class="flex-between">
                  <div class="title">{{ row.name }}</div>
                  <el-tag>{{ row.type }}</el-tag>
                </div>
                <div class="meta">
                  <el-rate v-model="row.difficulty" disabled />
                  <span class="count">已破解 {{ row.successCount || 0 }}</span>
                </div>
                <div class="desc">{{ row.desc }}</div>
                <div class="ops">
                  <el-button type="primary" @click="openDetail(row)">详情</el-button>
                  <el-button @click="startAnalyze(row)">开始分析</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>

      <el-tab-pane label="创建挑战" name="create">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card header="手动创建挑战">
              <el-form :model="createForm" label-width="100px">
                <el-form-item label="挑战名称">
                  <el-input v-model="createForm.name" />
                </el-form-item>
                <el-form-item label="挑战类型">
                  <el-select v-model="createForm.type" placeholder="请选择类型">
                    <el-option label="古典密码" value="密码生成·基础" />
                    <el-option label="对称密码" value="密码存储·进阶" />
                    <el-option label="非对称密码" value="算法攻防·核心" />
                    <el-option label="哈希" value="密码传输·进阶" />
                    <el-option label="侧信道" value="综合攻防" />
                  </el-select>
                </el-form-item>
                <el-form-item label="难度等级">
                  <el-rate v-model="createForm.difficulty" />
                </el-form-item>
                <el-form-item label="挑战描述">
                  <el-input type="textarea" v-model="createForm.description" rows="4" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleManualCreate">创建</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card header="AI 智能生成挑战" class="ai-card">
              <div class="chat-container">
                <div class="chat-messages" ref="chatRef">
                  <div v-for="(msg, index) in chatMessages" :key="index" :class="['message', msg.role]">
                    <div class="message-content">{{ msg.content }}</div>
                  </div>
                  <div v-if="isGenerating" class="message ai">
                    <div class="message-content">
                      <el-icon class="is-loading"><Loading /></el-icon>
                      正在设计场景拓扑...
                    </div>
                  </div>
                </div>
                <div class="chat-input">
                  <el-input
                    v-model="aiPrompt"
                    placeholder="描述您想要的场景，例如：生成一个包含Web服务器和数据库的电商渗透测试环境"
                    @keyup.enter="handleAiGenerate"
                  >
                    <template #append>
                      <el-button @click="handleAiGenerate">
                        <el-icon><Position /></el-icon>
                      </el-button>
                    </template>
                  </el-input>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-card v-if="topologyPreview" header="挑战拓扑预览" style="margin-top: 20px">
          <div class="topology-preview">
            <!-- Simple Mock Topology Visualization -->
            <div class="node" v-for="node in topologyPreview.nodes" :key="node.id" :style="node.style">
              <el-icon size="24"><component :is="node.icon" /></el-icon>
              <span>{{ node.label }}</span>
            </div>
            <div class="connection" v-for="(conn, idx) in topologyPreview.connections" :key="idx">
              <!-- Mock connections -->
            </div>
          </div>
          <div style="margin-top: 20px; text-align: center;">
             <el-button type="success" @click="confirmAiScenario">确认生成此挑战</el-button>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    <el-dialog v-model="detailVisible" title="挑战详情" width="640px">
      <div class="detail">
        <div class="row"><span>名称</span><span>{{ detailItem?.name }}</span></div>
        <div class="row"><span>类型</span><span>{{ mapType(detailItem?.type) }}</span></div>
        <div class="row"><span>难度</span><el-rate v-model="detailItem.difficulty" disabled /></div>
        <div class="row"><span>描述</span><span>{{ detailItem?.desc }}</span></div>
        <div class="row"><span>目标</span><span>找出明文或恢复密钥</span></div>
      </div>
      <template #footer>
        <el-button type="primary" @click="startAnalyze(detailItem)">开始分析</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted, computed } from 'vue'
import { Search, Plus, Loading, Position, Monitor, Coin } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

const activeTab = ref('list')
const searchQuery = ref('')
const isGenerating = ref(false)
const chatRef = ref(null)
const aiPrompt = ref('')
const topologyPreview = ref(null)

const scenarios = ref([])
const detailVisible = ref(false)
const detailItem = ref(null)

// 密码学算法分类
const categories = ref([
  { type: '古典密码加密', name: '1. 古典密码加密' },
  { type: '对称加密', name: '2. 对称加密' },
  { type: '非对称加密', name: '3. 非对称加密' },
  { type: '哈希算法', name: '4. 哈希算法' },
  { type: '数字签名', name: '5. 数字签名' },
  { type: '混合密码', name: '6. 混合密码' },
  { type: '量子密码', name: '7. 量子密码' }
])

const createForm = reactive({
  name: '',
  type: '',
  difficulty: 3,
  description: ''
})

const chatMessages = ref([
  { role: 'ai', content: '您好！我是AI场景设计助手。请告诉我您需要什么样的网络安全训练场景？' }
])

onMounted(async () => {
  try {
    scenarios.value = await api.get('/api/scenes')
  } catch (e) {
    scenarios.value = []
  }
})

// 根据分类获取场景
const getScenariosByCategory = (categoryType) => {
  return scenarios.value.filter(scene => scene.type === categoryType)
}

const handleManualCreate = async () => {
  if (!createForm.name) return ElMessage.warning('请输入场景名称')
  try {
    const created = await api.post('/api/scenes/manual', { ...createForm })
    scenarios.value.unshift(created)
    ElMessage.success('创建成功')
    activeTab.value = 'list'
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

const latestAiScene = ref(null)

const handleAiGenerate = async () => {
  if (!aiPrompt.value) return
  
  const prompt = aiPrompt.value
  chatMessages.value.push({ role: 'user', content: prompt })
  aiPrompt.value = ''
  isGenerating.value = true
  try {
    const scene = await api.post('/api/scenes/ai-generate', { description: prompt, preset: 'AI生成场景' })
    latestAiScene.value = scene
    topologyPreview.value = scene.topology || null
    chatMessages.value.push({ 
      role: 'ai', 
      content: `已根据您的需求"${prompt}"生成场景设计方案，并已保存。请查看拓扑预览。` 
    })
    scenarios.value.unshift(scene)
  } catch (e) {
    chatMessages.value.push({ role: 'ai', content: '生成失败，请稍后重试。' })
  } finally {
    isGenerating.value = false
    nextTick(() => {
      if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight
    })
  }
}

const confirmAiScenario = () => {
  ElMessage.success('场景生成并保存成功')
  activeTab.value = 'list'
  topologyPreview.value = null
  chatMessages.value = [{ role: 'ai', content: '您好！我是AI场景设计助手。请告诉我您需要什么样的网络安全训练场景？' }]
}

const handleRun = (row) => {
  row.status = row.status === 'running' ? 'stopped' : 'running'
  ElMessage.success(row.status === 'running' ? '场景已启动' : '场景已停止')
  api.put(`/api/scenes/${row.id}`, { status: row.status }).catch(() => {})
}

const handleDelete = (row) => {
  scenarios.value = scenarios.value.filter(s => s.id !== row.id)
  ElMessage.success('删除成功')
}

const handleEdit = (row) => {
  ElMessage.info('编辑功能待开发')
}

const handleImport = () => {
  ElMessage.info('导入功能待开发')
}

const openDetail = (row) => {
  detailItem.value = row
  detailVisible.value = true
}

const startAnalyze = (row) => {
  detailVisible.value = false
  // 根据场景名称跳转到对应的靶场页面
  if (row.name === 'CTF入门密码题') {
    window.open('http://localhost:8081', '_blank')
  } else if (row.name === '古典密码通信系统') {
    window.open('http://localhost:8082', '_blank')
  } else if (row.name === '古典密码破解挑战') {
    window.open('http://localhost:8083', '_blank')
  } else if (row.name === 'DES弱密钥靶场') {
    window.open('http://localhost:8084', '_blank')
  } else {
    // 其他场景保持原来的跳转逻辑
    window.location.hash = `#/attack/simulate?targetId=${row.id}`
  }
}

const mapType = (t) => {
  if (!t) return '其他'
  if (t.includes('生成')) return '古典密码'
  if (t.includes('存储')) return '对称密码'
  if (t.includes('传输')) return '哈希/协议'
  if (t.includes('算法攻防')) return '非对称密码'
  return '综合/侧信道'
}
</script>

<style scoped>
.scenarios-container {
  padding: 20px;
}

.operation-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.title { color: var(--text-color); font-weight: 600; }
.meta { display: flex; align-items: center; gap: 10px; margin: 8px 0; color: var(--text-secondary); }
.count { margin-left: auto; }
.desc { color: var(--text-secondary); min-height: 40px; }
.ops { display: flex; gap: 10px; }
.detail .row { display: flex; align-items: center; justify-content: space-between; margin: 8px 0; }

.ai-card {
  height: 500px;
  display: flex;
  flex-direction: column;
}
:deep(.el-card__header) {
  font-size: 18px;
  font-weight: 600;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 400px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: var(--bg-light);
  border-radius: 4px;
  margin-bottom: 10px;
}

.message {
  margin-bottom: 10px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.ai {
  justify-content: flex-start;
}

.message-content {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user .message-content {
  background: var(--primary-color);
  color: white;
}

.message.ai .message-content {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  font-size: 16px;
}

.topology-preview {
  height: 200px;
  background: var(--bg-light);
  position: relative;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.node {
  position: absolute; /* simple mock positioning */
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--bg-card);
  color: var(--text-color);
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  border: 1px solid var(--border-color);
}

.category-title {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 2px solid var(--primary-color);
}
</style>
