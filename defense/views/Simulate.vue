<template>
  <div class="simulate-container">
    <el-row :gutter="20">
      <!-- Left: Configuration -->
      <el-col :span="8">
        <el-card class="card mb-20">
          <template #header>
            <span>⚙️ 防御配置</span>
          </template>
          <el-form :model="form" label-width="100px">
            <el-form-item label="防御范围">
              <el-select v-model="form.scope" style="width: 100%">
                <el-option label="全量用户" value="all" />
                <el-option label="指定高危用户" value="high_risk" />
              </el-select>
            </el-form-item>
            <el-form-item label="防御模式">
              <el-radio-group v-model="form.mode">
                <el-radio label="auto">AI自动防御</el-radio>
                <el-radio label="manual">手动介入</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="响应阈值">
              <el-slider v-model="form.threshold" :min="1" :max="100" />
            </el-form-item>
            <el-form-item label="自动修复">
              <el-switch v-model="form.autoFix" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="activateDefense" class="w-100" :disabled="isDefending">
                {{ isDefending ? '防御系统运行中...' : '启动全局防御' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- Current Attack Info -->
        <el-card class="card" v-if="currentAttack">
          <template #header>
            <div class="flex-between">
              <span>⚠️ 检测到攻击行为</span>
              <el-tag type="danger" effect="dark" size="large" class="blink">ATTACK DETECTED</el-tag>
            </div>
          </template>
          <div class="attack-info">
            <div class="info-row">
              <span class="label">攻击目标:</span>
              <span class="value">{{ currentAttack.targetName }}</span>
            </div>
            <div class="info-row">
              <span class="label">涉及算法:</span>
              <span class="value">{{ currentAttack.algorithm }}</span>
            </div>
            <div class="info-row">
              <span class="label">攻击时间:</span>
              <span class="value">{{ new Date(currentAttack.startTime).toLocaleTimeString() }}</span>
            </div>
          </div>
        </el-card>
        <el-card class="card quick-actions mt-20">
          <template #header>
            <span>🛠️ 运维快捷操作</span>
          </template>
          <div class="actions-grid">
            <el-button type="primary" plain>刷新策略</el-button>
            <el-button type="primary" plain>清理黑名单</el-button>
            <el-button type="primary" plain>导出日志</el-button>
            <el-button type="primary" plain>一键加固</el-button>
          </div>
        </el-card>
      </el-col>

      <!-- Right: Real-time Monitor -->
      <el-col :span="16">
        <el-card class="card monitor-panel">
          <template #header>
            <div class="flex-between">
              <span>🛡️ 实时防御监控</span>
              <div v-if="isDefending" class="status-badge">
                <span class="dot"></span> 系统监控中
              </div>
            </div>
          </template>
          
          <!-- Timeline -->
          <div class="timeline-wrapper">
            <el-steps direction="vertical" :active="activeStep" finish-status="success">
              <el-step title="威胁感知" description="实时监控流量，识别异常行为..." />
              <el-step title="AI分析" description="分析攻击特征与手段 (AI Inference)..." />
              <el-step title="策略执行" description="调用算法加固/IP封禁/流量清洗..." />
              <el-step title="防御反馈" description="生成防御报告，更新安全评分..." />
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
                <span>📈 防御概览</span>
              </template>
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-label">日志条数</div>
                  <div class="stat-value">{{ logs.length }}</div>
                </div>
              <div class="stat-item">
                <div class="stat-label">拦截率</div>
                <div class="stat-value">{{ Math.floor(70 + Math.random()*25) }}%</div>
              </div>
              <div class="stat-item ai-stat">
                <div class="stat-label">AI评分</div>
                <div class="stat-value">{{ defenseScore ?? 0 }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">响应阈值</div>
                <div class="stat-value">{{ form.threshold }}%</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">自动修复</div>
                <div class="stat-value">{{ form.autoFix ? '启用' : '关闭' }}</div>
              </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="card">
              <template #header>
                <span>✅ 加固建议</span>
              </template>
              <div class="tips-list">
                <div class="tip-item">开启流量清洗与速率限制策略</div>
                <div class="tip-item">对高危用户启用额外校验</div>
                <div class="tip-item">定期滚动密钥与证书</div>
                <div class="tip-item">启用AI行为识别并提高敏感度</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { Storage } from '@/utils/storage'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

const isDefending = ref(false)
const activeStep = ref(0)
const logs = ref([])
const logContainer = ref(null)
const currentAttack = ref(null)
const defenseScore = ref(null)

const form = reactive({
  scope: 'all',
  mode: 'auto',
  threshold: 80,
  autoFix: true
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

const activateDefense = async () => {
  isDefending.value = true
  addLog('全局防御系统已启动', 'success')
  addLog('正在加载 DeepGuard v3.0 模型...', 'info')
  addLog('全量用户安全扫描中...', 'info')
  try {
    await api.post('/api/defense/config', { ...form })
  } catch (e) {}
}

const handleAttack = async (attackData) => {
  if (!isDefending.value) return

  currentAttack.value = attackData
  activeStep.value = 0
  
  // Step 1: Detect
  addLog(`[ALERT] 检测到针对 [${attackData.targetName}] 的异常访问!`, 'error')
  await sleep(800)
  activeStep.value = 1
  
  // Step 2: Analyze
  addLog('AI引擎介入分析...', 'info')
  addLog(`识别攻击特征: 针对 ${attackData.algorithm} 算法的爆破尝试`, 'warning')
  await sleep(1000)
  activeStep.value = 2
  
  // Step 3: Execute
  addLog('匹配防御策略: 动态密钥更新 + 限制访问频率', 'info')
  addLog('正在执行算法加固...', 'success')
  
  // Check if auto-fix is needed
  if (form.autoFix) {
    const target = Storage.get(Storage.KEYS.TARGETS).find(t => t.id === attackData.targetId)
    if (target && target.isVulnerable) {
      addLog(`检测到 [${target.name}] 存在算法漏洞，执行热修复...`, 'warning')
      // Simulate fix
      setTimeout(() => {
        Storage.update(Storage.KEYS.TARGETS, target.id, {
           status: 'secure',
           isVulnerable: false,
           vulnerabilities: []
        })
        addLog(`[${target.name}] 漏洞已自动修复`, 'success')
      }, 500)
    }
  }
  
  await sleep(1000)
  activeStep.value = 3
  
  // Step 4: Feedback
  try {
    const report = await api.post('/api/defense/verify', { strategy: form.mode, attack: attackData })
    addLog(`防御报告: 拦截率 ${report.blockedRate}%`, 'success')
    if (typeof report.aiScore === 'number') {
      defenseScore.value = report.aiScore
      addLog(`AI评分: ${report.aiScore}`, 'info')
    }
  } catch (e) {
    addLog('防御成功！攻击已被拦截。', 'success')
  }
  activeStep.value = 4
  
  Storage.add(Storage.KEYS.DEFENSE_LOGS, {
    id: Date.now(),
    target: attackData.targetName,
    action: 'Intercepted',
    time: new Date().toLocaleString()
  })
  
  setTimeout(() => {
    currentAttack.value = null
    activeStep.value = 0 // Reset
  }, 3000)
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const onStorageUpdate = (e) => {
  if (e.detail.key === 'current_attack') {
    handleAttack(e.detail.value)
  }
}

onMounted(() => {
  window.addEventListener('local-storage-update', onStorageUpdate)
  activateDefense() // Auto start for demo
})

onUnmounted(() => {
  window.removeEventListener('local-storage-update', onStorageUpdate)
})
</script>

<style scoped>
.simulate-container {
  color: var(--text-color);
}
.mb-20 { margin-bottom: 20px; }
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

.status-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--success-color);
}
.status-badge .dot {
  width: 8px;
  height: 8px;
  background: var(--success-color);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.attack-info .info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  border-bottom: 1px dashed var(--border-color);
  padding-bottom: 5px;
}
.attack-info .label { color: var(--text-secondary); }
.attack-info .value { color: var(--text-color); font-weight: bold; }

.blink { animation: blink 1s infinite; }
@keyframes blink { 50% { opacity: 0.5; } }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

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
</style>

