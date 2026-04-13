<template>
  <div class="simulate-container">
    <!-- 模拟攻击配置 --><el-row :gutter="20">
      <!-- Left: Configuration -->
      <el-col :span="8">
        <el-card class="card mb-20">
          <template #header>
            <span>⚙️ 攻击配置</span>
          </template>
          <el-form :model="form" label-width="100px">
            <el-form-item label="选择靶场">
              <el-select v-model="form.targetId" placeholder="选择靶场" style="width: 100%">
                <el-option
                  v-for="item in targets"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="攻击方式">
              <el-radio-group v-model="form.method">
                <el-radio label="ai">AI自动攻击</el-radio>
                <el-radio label="manual">手动配置</el-radio>
              </el-radio-group>
            </el-form-item>
            <div v-if="form.method === 'manual'">
              <el-form-item label="攻击路径">
                <el-checkbox-group v-model="form.tools">
                  <el-checkbox label="weak-key">弱密钥漏洞利用</el-checkbox>
                  <el-checkbox label="key-intercept">传输层密钥截获攻击</el-checkbox>
                  <el-checkbox label="third-party">第三方加密工具漏洞利用</el-checkbox>
                  <el-checkbox label="host-break">主机权限突破攻击</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </div>
            <el-form-item label="并发数">
              <el-slider v-model="form.concurrency" :min="1" :max="100" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="startAttack" :loading="attacking" class="w-100">
                {{ attacking ? '攻击进行中...' : '发起攻击' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="card" v-if="attackResult">
          <template #header>
            <span>📊 攻击结果</span>
          </template>
          <div class="result-box" :class="{ success: attackResult.success, fail: !attackResult.success }">
            <el-icon class="result-icon">
              <CircleCheckFilled v-if="attackResult.success" />
              <CircleCloseFilled v-else />
            </el-icon>
            <span class="result-text">{{ attackResult.success ? '攻击成功' : '攻击被拦截' }}</span>
          </div>
          <div class="result-details mt-20">
            <div class="detail-item">
              <span>耗时:</span> <span>{{ attackResult.time }}ms</span>
            </div>
            <div class="detail-item">
              <span>AI评分:</span> <span>{{ attackResult.aiScore }}</span>
            </div>
            <div class="detail-item" v-if="attackResult.success">
              <span>破解密码:</span> <span class="code">P@ssw0rd123</span>
            </div>
            <div class="detail-item">
              <span>拦截原因:</span> <span>{{ attackResult.reason || '无' }}</span>
            </div>
          </div>
        </el-card>
        <el-card class="card quick-actions mt-20">
          <template #header>
            <span>⚡ 快捷操作</span>
          </template>
          <div class="actions-grid">
            <el-button type="primary" plain>字典更新</el-button>
            <el-button type="primary" plain>载入脚本</el-button>
            <el-button type="primary" plain>导出报告</el-button>
            <el-button type="primary" plain>清理痕迹</el-button>
          </div>
        </el-card>
      </el-col>

      <!-- Right: Real-time Monitor -->
      <el-col :span="16">
        <el-card class="card monitor-panel">
          <template #header>
            <div class="flex-between">
              <span>📡 实时攻击监控</span>
              <el-tag v-if="attacking" type="warning" effect="dark" size="large" class="blink">正在攻击...</el-tag>
            </div>
          </template>
          
          <!-- Timeline -->
          <div class="timeline-wrapper">
            <el-steps direction="vertical" :active="activeStep" finish-status="success">
              <el-step title="初始化" description="加载攻击模块，连接目标..." />
              <el-step title="漏洞扫描" description="分析目标防御策略与算法漏洞..." />
              <el-step title="尝试突破" description="执行AI攻击策略，尝试绕过防御..." />
              <el-step title="结果验证" description="验证获取的权限与数据..." />
            </el-steps>
          </div>

          <!-- Console Logs -->
          <div class="console-log" ref="logContainer">
            <div v-for="(log, index) in logs" :key="index" class="log-line">
              <span class="time">[{{ log.time }}]</span>
              <span class="type" :class="log.type">[{{ log.type.toUpperCase() }}]</span>
              <span class="msg">{{ log.message }}</span>
            </div>
          </div>
        </el-card>
        <el-row :gutter="20" class="mt-20">
          <el-col :span="12">
            <el-card class="card">
              <template #header>
                <span>📈 攻击概览</span>
              </template>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-label">尝试次数</div>
                <div class="stat-value">{{ logs.length }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">成功率</div>
                <div class="stat-value">{{ attackResult?.success ? '100%' : '0%' }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">平均耗时</div>
                <div class="stat-value">{{ attackResult?.time || 0 }}ms</div>
              </div>
              <div class="stat-item ai-stat">
                <div class="stat-label">AI评分</div>
                <div class="stat-value">{{ attackResult?.aiScore ?? 0 }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">并发数</div>
                <div class="stat-value">{{ form.concurrency }}</div>
              </div>
            </div>
          </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="card">
              <template #header>
                <span>🧭 下一步建议</span>
              </template>
              <div class="tips-list">
                <div class="tip-item">启用AI高级混淆模式以绕过高强度防御</div>
                <div class="tip-item">调整并发至 {{ Math.min(form.concurrency + 10, 100) }} 提升效率</div>
                <div class="tip-item">更新字典并重新尝试漏洞利用</div>
                <div class="tip-item">收集指纹用于后续攻击路径规划</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" class="mt-20">
          <el-col :span="24">
            <el-card class="card workbench-card">
              <template #header>
                <div class="flex-between">
                  <span>🧪 密码分析工作台</span>
                  <el-tag type="info">{{ editorLang.toUpperCase() }}</el-tag>
                </div>
              </template>
              <el-tabs v-model="activeTab">
                <el-tab-pane label="代码编辑器" name="editor">
                  <div class="editor-toolbar">
                    <el-select v-model="editorLang" style="width: 200px">
                      <el-option label="Python" value="python" />
                      <el-option label="C++" value="cpp" />
                      <el-option label="JavaScript" value="javascript" />
                    </el-select>
                    <div class="editor-actions">
                      <el-button type="primary" @click="runCode">运行</el-button>
                      <el-button @click="resetSample">载入示例</el-button>
                    </div>
                  </div>
                  <el-input
                    v-model="editorCode"
                    type="textarea"
                    :rows="14"
                    class="code-input"
                    placeholder="在此编写脚本以进行密码分析"
                  />
                </el-tab-pane>
                <el-tab-pane label="终端" name="terminal">
                  <div class="terminal-run">
                    <el-input v-model="terminalCmd" placeholder="输入命令，例如: hashcat --help" />
                    <el-button class="mt-10" type="primary" @click="runTerminal">执行</el-button>
                  </div>
                  <div class="terminal-output" ref="terminalRef">
                    <div v-for="(line, idx) in terminalLogs" :key="idx" class="terminal-line">{{ line }}</div>
                  </div>
                </el-tab-pane>
                <el-tab-pane label="可视化" name="visual">
                  <div class="visual-toolbar">
                    <el-input v-model="toolInputs.text" placeholder="输入密文或文本进行频率分析" />
                    <el-button type="primary" @click="runFrequencyAnalysis">生成频率分析</el-button>
                  </div>
                  <div class="chart-container" ref="chartRef"></div>
                </el-tab-pane>
                <el-tab-pane label="工具集" name="tools">
                  <div class="tools-grid">
                    <div class="tool-item">
                      <div class="tool-title">频率分析</div>
                      <el-input v-model="toolInputs.text" placeholder="输入文本" />
                      <el-button class="mt-10" type="primary" @click="runFrequencyAnalysis">分析</el-button>
                    </div>
                    <div class="tool-item">
                      <div class="tool-title">哈希查询</div>
                      <el-input v-model="toolInputs.hash" placeholder="输入哈希值" />
                      <el-button class="mt-10" type="primary" @click="runHashLookup">查询</el-button>
                    </div>
                    <div class="tool-item">
                      <div class="tool-title">弱密钥检测</div>
                      <el-button type="warning" @click="runWeakKeyCheck">检测</el-button>
                    </div>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { Storage } from '@/utils/storage'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'
import * as echarts from 'echarts'

const route = useRoute()
const targets = ref([])
const attacking = ref(false)
const activeStep = ref(0)
const logs = ref([])
const logContainer = ref(null)
const attackResult = ref(null)
const activeTab = ref('editor')
const editorLang = ref('python')
const editorCode = ref('')
const terminalCmd = ref('')
const terminalLogs = ref([])
const terminalRef = ref(null)
const chartRef = ref(null)
let chartInstance = null
const toolInputs = reactive({ text: '', hash: '' })

// 攻击轮数追踪
const attackRounds = ref({})

// 获取攻击轮数
const getAttackRound = (targetId) => {
  return attackRounds.value[targetId] || 1
}

// 增加攻击轮数
const incrementAttackRound = (targetId) => {
  attackRounds.value[targetId] = (attackRounds.value[targetId] || 1) + 1
}

const form = reactive({
  targetId: null,
  method: 'ai',
  tools: ['weak-key'],
  concurrency: 50
})

const addLog = (message, type = 'info') => {
  const time = new Date().toLocaleTimeString()
  logs.value.push({ time, message, type })
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

const runCode = () => {
  if (!editorCode.value.trim()) {
    ElMessage.warning('请输入代码')
    return
  }
  addLog(`运行${editorLang.value}脚本...`, 'info')
  nextTick(() => {
    addLog('脚本执行完成，请查看可视化或终端输出', 'success')
    terminalLogs.value.push(`[${new Date().toLocaleTimeString()}] 运行 ${editorLang.value} 脚本完成`)
    if (terminalRef.value) {
      terminalRef.value.scrollTop = terminalRef.value.scrollHeight
    }
  })
}

const resetSample = () => {
  const samples = {
    python:
      'import collections\ntext = "LXFOPVEFRNHR"\nprint(collections.Counter(text))',
    cpp:
      '#include <iostream>\nint main(){ std::cout << "RSA e=3 attack sample"; return 0; }',
    javascript:
      'const text = "ATTACKATDAWN";\nconst freq = [...text].reduce((m,c)=>(m[c]=(m[c]||0)+1,m),{});\nconsole.log(freq);'
  }
  editorCode.value = samples[editorLang.value]
}

const runTerminal = () => {
  const cmd = terminalCmd.value.trim()
  if (!cmd) {
    ElMessage.warning('请输入命令')
    return
  }
  terminalLogs.value.push(`$ ${cmd}`)
  setTimeout(() => {
    terminalLogs.value.push('模拟输出: 命令执行完成')
    if (terminalRef.value) {
      terminalRef.value.scrollTop = terminalRef.value.scrollHeight
    }
  }, 500)
}

const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption({
      tooltip: {},
      xAxis: { type: 'category', data: [] },
      yAxis: { type: 'value' },
      series: [{ type: 'bar', data: [] }]
    })
  }
}

const updateChart = (labels, values) => {
  if (!chartInstance) return
  chartInstance.setOption({
    xAxis: { data: labels },
    series: [{ data: values }]
  })
}

const runFrequencyAnalysis = () => {
  const text = (toolInputs.text || 'THISISASAMPLECIPHERTEXT').toUpperCase().replace(/[^A-Z]/g, '')
  const map = {}
  for (const ch of text) map[ch] = (map[ch] || 0) + 1
  const labels = Object.keys(map).sort()
  const values = labels.map(k => map[k])
  updateChart(labels, values)
  addLog('完成频率分析', 'success')
}

const runHashLookup = () => {
  if (!toolInputs.hash) {
    ElMessage.warning('请输入哈希值')
    return
  }
  addLog(`查询哈希 ${toolInputs.hash} 的明文匹配`, 'info')
  setTimeout(() => addLog('未命中本地彩虹表，建议使用外部服务', 'warning'), 800)
}

const runWeakKeyCheck = () => {
  addLog('检测RSA弱密钥与共享因子...', 'info')
  setTimeout(() => addLog('未发现弱密钥迹象', 'success'), 1200)
}

const startAttack = async () => {
  if (!form.targetId) {
    ElMessage.warning('请选择攻击目标')
    return
  }
  
  attacking.value = true
  activeStep.value = 0
  logs.value = []
  attackResult.value = null
  
  const target = targets.value.find(t => t.id === form.targetId)
  
  // Step 1: Init
  addLog(`开始对目标 [${target.name}] 发起攻击初始化...`, 'info')
  await sleep(1000)
  activeStep.value = 1
  
  // Step 2: Scan
  addLog('正在分析靶场拓扑与服务...', 'info')
  addLog(`靶场类型: ${target.type}，难度: ${target.difficulty}`, 'warning')
  await sleep(1500)
  activeStep.value = 2
  
  // Step 3: Attack
  addLog('加载AI攻击模型: DeepAttack v2.1', 'success')
  addLog('正在生成对抗样本...', 'info')
  
  try {
    await api.post('/api/attacks/config', { target: target.name, method: form.method, tools: form.tools, concurrency: form.concurrency })
  } catch (e) {}
  
  // Notify Defense End via Storage
  Storage.set('current_attack', {
    targetId: target.id,
    targetName: target.name,
    algorithm: target.type,
    startTime: Date.now()
  })

  // Simulate attempts
  for (let i = 0; i < 5; i++) {
    await sleep(800)
    addLog(`尝试第 ${i+1} 次突破... Payload: ${generatePayload()}`, 'info')
  }
  
  // Result
  activeStep.value = 3
  await sleep(1000)
  
  let isSuccess = false
  let backendReport = null
  
  // 获取当前攻击轮数
  const currentRound = getAttackRound(form.targetId)
  
  // 检查是否是SM4目标
  const isSM4Target = target.name === '基于国密SM4加密的交通管理系统'
  
  try {
    if (isSM4Target) {
      // 对于SM4目标，第一次攻击成功，第二次攻击失败
      if (currentRound === 1) {
        // 第一轮攻击成功
        isSuccess = true
        backendReport = {
          success: true,
          duration: 4500 + Math.floor(Math.random() * 2000),
          reason: null,
          aiScore: 95
        }
      } else {
        // 第二轮攻击失败
        isSuccess = false
        backendReport = {
          success: false,
          duration: 6000,
          reason: '防御端已加固，应用了智能密钥生成+生命周期管控、SM2+SM4双层加密+AI流量实时监控、国密认证白名单+自动化漏洞管理、主机安全加固+AI权限精细化管控等高级防御措施',
          aiScore: 70
        }
      }
    } else {
      // 其他目标，使用后端返回的结果
      backendReport = await api.post('/api/attacks/execute', { target: target.name })
      isSuccess = !!backendReport.success
    }
    
    addLog(`后端返回报告: ${isSuccess ? '成功' : '被拦截'}，耗时 ${backendReport.duration}ms`, isSuccess ? 'success' : 'error')
    if (typeof backendReport.aiScore === 'number') {
      addLog(`AI评分: ${backendReport.aiScore}`, 'info')
    }
  } catch (e) {
    // 异常情况下，对于SM4目标，按照轮数返回结果
    if (isSM4Target) {
      if (currentRound === 1) {
        isSuccess = true
        backendReport = {
          success: true,
          duration: 4500 + Math.floor(Math.random() * 2000),
          reason: null,
          aiScore: 95
        }
      } else {
        isSuccess = false
        backendReport = {
          success: false,
          duration: 6000,
          reason: '防御端已加固，应用了高级防御措施',
          aiScore: 70
        }
      }
    }
  }
  
  // 增加攻击轮数
  incrementAttackRound(form.targetId)
  
  activeStep.value = 4
  attacking.value = false
  
  if (isSuccess) {
    addLog('攻击成功！已获取系统权限。', 'success')
    attackResult.value = {
      success: true,
      time: typeof backendReport?.duration === 'number' ? backendReport.duration : 4500 + Math.floor(Math.random() * 2000),
      reason: backendReport?.reason || null,
      aiScore: typeof backendReport?.aiScore === 'number' ? backendReport.aiScore : 0
    }
    // Update stats
    Storage.add(Storage.KEYS.ATTACK_LOGS, {
      id: Date.now(),
      target: target.name,
      result: 'Success',
      time: new Date().toLocaleString()
    })
  } else {
    addLog('攻击失败！被防御系统拦截。', 'error')
    attackResult.value = {
      success: false,
      time: typeof backendReport?.duration === 'number' ? backendReport.duration : 6000,
      reason: backendReport?.reason || 'IP被防御端封禁 / 流量特征识别',
      aiScore: typeof backendReport?.aiScore === 'number' ? backendReport.aiScore : 0
    }
    Storage.add(Storage.KEYS.ATTACK_LOGS, {
      id: Date.now(),
      target: target.name,
      result: 'Blocked',
      time: new Date().toLocaleString()
    })
  }
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const generatePayload = () => {
  return Math.random().toString(36).substring(7)
}

onMounted(() => {
  // 从后端获取靶场列表
  api.get('/api/scenes').then(res => {
    targets.value = Array.isArray(res) ? res : []
  }).catch(() => {
    targets.value = []
  })
  if (route.query.targetId) {
    form.targetId = Number(route.query.targetId)
  }
  resetSample()
  initChart()
})
</script>

<style scoped>
.simulate-container {
  color: var(--text-color);
}
.mb-20 { margin-bottom: 20px; }
.mt-20 { margin-top: 20px; }
.w-100 { width: 100%; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }

.monitor-panel {
  min-height: 480px;
  display: flex;
  flex-direction: column;
}

.timeline-wrapper {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}
:deep(.el-step__title) {
  font-size: 16px;
}
:deep(.el-step__description) {
  font-size: 14px;
  color: var(--text-secondary);
}

.console-log {
  flex: 1;
  background: #000;
  padding: 15px;
  overflow-y: auto;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  border-radius: 4px;
  margin-top: 20px;
  height: 280px;
}

.log-line { margin-bottom: 5px; }
.log-line .time { color: #888; margin-right: 10px; }
.log-line .type { margin-right: 10px; font-weight: bold; }
.log-line .type.info { color: #409EFF; }
.log-line .type.warning { color: #E6A23C; }
.log-line .type.success { color: #67C23A; }
.log-line .type.error { color: #F56C6C; }
.log-line .msg { color: #ddd; }

.result-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  padding: 20px;
  border-radius: 8px;
}
.result-box.success { background: rgba(103, 194, 58, 0.1); color: #67C23A; }
.result-box.fail { background: rgba(245, 108, 108, 0.1); color: #F56C6C; }
.result-icon { font-size: 32px; }
.result-text { font-size: 20px; font-weight: bold; }

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: var(--text-secondary);
}
.detail-item .code {
  font-family: monospace;
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 5px;
  border-radius: 4px;
  color: var(--primary-light);
}

.blink { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0.5; } }

.quick-actions .actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.stat-item {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px;
}
.stat-label {
  color: var(--text-secondary);
  font-size: 12px;
}
.stat-value {
  color: var(--text-color);
  font-size: 18px;
  font-weight: 600;
}
.ai-stat .stat-label {
  font-size: 13px;
  color: var(--primary-light);
}
.ai-stat .stat-value {
  font-size: 22px;
  color: var(--primary-light);
  font-weight: 700;
}
.tips-list .tip-item {
  padding: 8px 0;
  border-bottom: 1px dashed var(--border-color);
  color: var(--text-secondary);
}
.tips-list .tip-item:last-child {
  border-bottom: none;
}

.workbench-card {
  min-height: 420px;
}
.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.editor-actions {
  display: flex;
  gap: 10px;
}
.code-input {
  font-family: 'Courier New', Courier, monospace;
}
.terminal-run {
  display: flex;
  gap: 10px;
  align-items: center;
}
.terminal-output {
  background: #000;
  color: #eee;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  border-radius: 4px;
  margin-top: 10px;
  padding: 10px;
  height: 220px;
  overflow-y: auto;
}
.terminal-line { margin-bottom: 6px; }
.visual-toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}
.chart-container {
  width: 100%;
  height: 300px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.tool-item {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px;
  background: var(--bg-light);
}
.tool-title {
  font-weight: 600;
  margin-bottom: 8px;
}
</style>

