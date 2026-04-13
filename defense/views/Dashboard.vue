<template>
  <div class="dashboard-container">
    <!-- 实时防御状态 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="16">
        <el-card class="monitor-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">🛡️ 实时防御状态</span>
              <el-tag type="success" effect="dark" class="blink">{{ aiStatusText }}</el-tag>
            </div>
          </template>
          <div class="status-bars">
            <div class="status-item">
              <div class="status-label">防御进度</div>
              <el-progress :percentage="defenseProgress" :color="'var(--success-color)'" />
            </div>
            <div class="status-item">
              <div class="status-label">加固进度</div>
              <el-progress :percentage="hardeningProgress" :color="'var(--primary-color)'" />
            </div>
            <div class="status-item">
              <div class="status-label">AI评分进度</div>
              <el-progress :percentage="aiScoreProgress" :color="'var(--warning-color)'" />
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🤖 AI防御体状态</span>
          </template>
          <div class="ai-status">
            <div class="ai-item">
              <span class="ai-label">版本</span>
              <span class="ai-value">DeepDefense v2.1</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">训练完成度</span>
              <span class="ai-value text-success">95.2%</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">防御成功率</span>
              <span class="ai-value text-success">92.8%</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">当前阶段</span>
              <span class="ai-value" :class="{ 'text-success': currentPhase === '加固完成', 'text-warning': currentPhase === '防御中', 'text-info': currentPhase === '分析阶段' }">{{ currentPhase }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- AI评分结果展示 -->
    <el-row :gutter="20" class="mb-20" v-if="showDefenseScore">
      <el-col :span="24">
        <el-card class="score-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">🎯 防御端AI评分结果</span>
              <el-tag type="success" effect="dark">防御端</el-tag>
            </div>
          </template>
          <div class="score-result">
            <div class="score-main">
              <div class="score-circle defense">
                <span class="score-number">{{ defenseScore }}</span>
                <span class="score-unit">分</span>
              </div>
              <div class="score-breakdown">
                <div class="score-item">
                  <span class="score-label">防御方案评分：</span>
                  <span class="score-value text-success">95分</span>
                </div>
                <div class="score-item">
                  <span class="score-label">加固效果评分：</span>
                  <span class="score-value text-success">90分</span>
                </div>
              </div>
            </div>
            <div class="score-comment">
              <h4>📋 防御报告评价</h4>
              <p>{{ defenseReportComment }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- AI深度思考 -->
    <el-row :gutter="20" class="mb-20" v-if="showDeepThinking">
      <el-col :span="24">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🤖 AI深度思考</span>
          </template>
          <div class="ai-deep-thinking">
            <div class="deep-thinking-text">{{ aiStatusText }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 防御报告展示 -->
    <el-row :gutter="20" class="mb-20" v-if="showDefenseReport">
      <el-col :span="24">
        <el-card class="report-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">📄 防御报告</span>
              <el-button type="success" size="small" @click="downloadDefenseReport">下载报告</el-button>
            </div>
          </template>
          <div class="report-content">
            <h3>密码防御演练分析报告</h3>
            <div class="report-section">
              <h4>一、防御概述</h4>
              <p>本次防御演练中，防守方成功抵御了攻击方的两轮攻击，第一轮由于系统存在安全漏洞被攻破，第二轮通过实施加固措施成功阻断了所有攻击。</p>
            </div>
            <div class="report-section">
              <h4>二、加固措施分析</h4>
              <p>防守方实施了多项安全加固措施，包括：密码哈希加盐存储、密钥轮换机制、多因素认证、账户锁定机制等。</p>
            </div>
            <div class="report-section">
              <h4>三、防御结果</h4>
              <ul>
                <li>第一轮防御：失败，被攻破，评分30分</li>
                <li>第二轮防御：成功，阻断了所有攻击，评分95分</li>
                <li>综合评分：92分</li>
              </ul>
            </div>
            <div class="report-section">
              <h4>四、改进建议</h4>
              <p>防守方应继续加强对新型攻击手法的学习，定期进行安全审计和漏洞扫描，建立完善的安全响应机制，不断完善防御体系。</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">🛡️</div>
          <div class="stat-value">{{ protectedSystems }}</div>
          <div class="stat-label">已保护的系统</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">🔒</div>
          <div class="stat-value">{{ patchedVulnerabilities }}</div>
          <div class="stat-label">已修复的漏洞</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">⏱️</div>
          <div class="stat-value">{{ averageHardeningTime }}</div>
          <div class="stat-label">平均加固时间</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 场景卡片网格 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="12">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">📊 防御流程</span>
          </template>
          <div class="defense-flow">
            <div 
              v-for="(step, index) in defenseFlowSteps" 
              :key="index"
              class="flow-step"
              :class="{ 'completed': step.status === 'completed', 'current': step.status === 'current', 'pending': step.status === 'pending' }"
            >
              <div class="flow-step-number">{{ index + 1 }}</div>
              <div class="flow-step-content">
                <div class="flow-step-title">{{ step.title }}</div>
                <div class="flow-step-description">{{ step.description }}</div>
                <div v-if="step.status === 'completed'" class="flow-step-result">{{ step.result }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="monitor-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">🎯 防御目标列表</span>
              <el-button 
                type="success" 
                @click="handleAIScore"
              >
                AI评分
              </el-button>
            </div>
          </template>
          <el-table :data="defenseTargets" style="width: 100%">
            <el-table-column prop="name" label="目标" width="220">
              <template #default="scope">
                <div class="target-name">
                  <span class="target-icon">🛡️</span>
                  <span class="target-text">{{ scope.row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="defenseLevel" label="防御等级" width="120">
              <template #default="scope">
                <el-tag 
                  :type="getDefenseLevelType(scope.row.defenseLevel)"
                  effect="dark"
                >
                  {{ scope.row.defenseLevel }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="scope">
                <el-tag 
                  :type="{
                    '未加固': 'info',
                    '加固中': 'warning',
                    '已加固': 'success'
                  }[scope.row.status]"
                  effect="dark"
                >
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="action" label="操作" width="100">
              <template #default="scope">
                <el-button 
                  type="success" 
                  size="small"
                  :disabled="scope.row.status === '已加固'"
                  @click="handleHarden(scope.row)"
                >
                  加固
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- AI评分状态提示 -->
    <el-dialog
      v-model="aiScoreDialogVisible"
      title="AI评分"
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="ai-score-status">
        <div class="status-icon" v-if="aiScoreStatus === 'scoring'">
          <el-icon class="is-loading"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 1024a512 512 0 1 1 512-512a512 512 0 0 1-512 512zm0-896a384 384 0 1 0 384 384a384 384 0 0 0-384-384z" opacity=".3"></path><path fill="currentColor" d="M716.8 512a204.8 204.8 0 1 1-409.6 0a204.8 204.8 0 0 1 409.6 0z" opacity=".3"></path><path fill="currentColor" d="M870.4 512a358.4 358.4 0 1 1-716.8 0a358.4 358.4 0 0 1 716.8 0z"></path></svg></el-icon>
        </div>
        <div class="status-icon" v-else-if="aiScoreStatus === 'reporting'">
          <el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="currentColor" d="M832 64H192a32 32 0 0 0-32 32v832a32 32 0 0 0 32 32h640a32 32 0 0 0 32-32V96a32 32 0 0 0-32-32zm-256 704h-64v-64h64v64zm0-128h-64v-64h64v64zm0-128h-64v-64h64v64zm-192 256h-64v-64h64v64zm0-128h-64v-64h64v64zm0-128h-64v-64h64v64zm256 0h-64v-64h64v64zm0 128h-64v-64h64v64z"></path></svg></el-icon>
        </div>
        <div class="status-text" v-if="aiScoreStatus === 'scoring'">AI评分中...</div>
        <div class="status-text" v-else-if="aiScoreStatus === 'reporting'">防御报告生成中...</div>
      </div>
    </el-dialog>

    <!-- 场景卡片网格 -->
    <div class="scenarios-grid">
      <scenario-card
        v-for="scenario in scenarios"
        :key="scenario.id"
        :scenario="scenario"
        @start-training="handleStartTraining"
      ></scenario-card>
    </div>

    <!-- DeepSeek AI 助手 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="24">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🤖 DeepSeek AI 助手</span>
          </template>
          <DeepSeekChat :context="'密码虚拟攻防平台 - 防御端'" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/../shared/utils/api.js'
import ScenarioCard from '../components/ScenarioCard.vue'
import DeepSeekChat from '@/../attack/components/DeepSeekChat.vue'

// 场景数据
const scenarios = ref([])
// 防御措施数据
const defenseMeasures = ref([
  {
    id: 1,
    name: '智能密钥生成+生命周期管控',
    description: '使用AI算法生成强密钥，并对密钥进行全生命周期管理，包括生成、分发、使用、轮换和销毁',
    effectiveness: 98
  },
  {
    id: 2,
    name: 'SM2+SM4双层加密+AI流量实时监控',
    description: '采用SM2非对称加密和SM4对称加密相结合的双层加密方案，并使用AI技术实时监控流量异常',
    effectiveness: 99
  },
  {
    id: 3,
    name: '国密认证白名单+自动化漏洞管理',
    description: '建立基于国密标准的认证白名单机制，并实现漏洞的自动扫描、分类和修复建议',
    effectiveness: 95
  },
  {
    id: 4,
    name: '主机安全加固+AI权限精细化管控',
    description: '对主机系统进行安全加固，并使用AI技术实现基于行为的权限精细化管控',
    effectiveness: 97
  },
  {
    id: 7,
    name: 'SM4密钥加固',
    description: '增强SM4加密密钥的安全性，使用强密钥生成和定期轮换',
    effectiveness: 98
  }
])

// 防御目标数据
const defenseTargets = ref([
  { name: '访客WiFi网络', defenseLevel: 'Low', status: '已加固', action: '加固' },
  { name: '智能门禁系统', defenseLevel: 'Low', status: '已加固', action: '加固' },
  { name: '员工考勤管理系统', defenseLevel: 'Medium', status: '已加固', action: '加固' },
  { name: '企业VPN系统', defenseLevel: 'Medium', status: '已加固', action: '加固' },
  { name: '基于国密SM4加密的交通管理系统', defenseLevel: 'High', status: '未加固', action: '加固' },
  { name: '企业内部邮件系统', defenseLevel: 'High', status: '已加固', action: '加固' },
  { name: '金融交易平台', defenseLevel: 'High', status: '已加固', action: '加固' }
])

// 防御流程步骤
const defenseFlowSteps = ref([
  {
    title: '第一轮攻击',
    description: '攻击方从多个角度进行攻击',
    status: 'completed',
    result: '攻击成功，系统被攻破'
  },
  {
    title: '漏洞分析',
    description: '分析攻击方使用的攻击手段和漏洞',
    status: 'completed',
    result: '已识别所有攻击向量和漏洞'
  },
  {
    title: '系统加固',
    description: '针对漏洞进行系统加固',
    status: 'completed',
    result: '所有漏洞已修复，系统安全性提升'
  },
  {
    title: '第二轮防御',
    description: '防御攻击方的第二轮攻击',
    status: 'current',
    result: ''
  },
  {
    title: 'AI分析与评分',
    description: 'AI对防御过程进行深度分析和评分',
    status: 'pending',
    result: ''
  }
])

// 响应式数据
const defenseProgress = ref(50)
const hardeningProgress = ref(50)
const aiScoreProgress = ref(0)
const currentPhase = ref('第一轮攻击')
const protectedSystems = ref(15)
const patchedVulnerabilities = ref(23)
const averageHardeningTime = ref('32s')

// AI评分结果
const showDefenseScore = ref(false)
const showDeepThinking = ref(true)
const showDefenseReport = ref(false)
const defenseScore = ref(0)
const defenseReportComment = ref('')

// AI状态文本
const aiStatusText = ref('防御流程完成后，AI将进行深度分析和评分...')

// AI评分相关数据
const aiScoreDialogVisible = ref(false)
const aiScoreStatus = ref('scoring') // scoring, reporting, completed

// 获取防御措施
const getDefenseMeasures = async () => {
  try {
    const response = await api.get('/defense/measures')
    // 保留前端硬编码的防御措施数据
    // defenseMeasures.value = response
  } catch (error) {
    console.error('获取防御措施失败:', error)
    // 即使获取失败，也使用前端硬编码的防御措施数据
  }
}

// 从后端获取数据并转换格式
const fetchScenarios = async () => {
  try {
    // 模拟场景数据
    scenarios.value = [
      {
        id: 1,
        title: '弱密码防御',
        category: '密码安全',
        level: '初级',
        participants: 1500,
        description: '学习如何防御弱密码攻击',
        icon: '🔐'
      },
      {
        id: 2,
        title: 'RSA私钥保护',
        category: '密钥管理',
        level: '中级',
        participants: 1200,
        description: '学习如何安全管理RSA私钥',
        icon: '🔑'
      },
      {
        id: 3,
        title: '哈希碰撞防御',
        category: '密码算法',
        level: '高级',
        participants: 800,
        description: '学习如何防御哈希碰撞攻击',
        icon: '🧮'
      }
    ]
  } catch (error) {
    console.error('获取场景数据失败:', error)
    ElMessage.error('获取场景数据失败，请检查后端服务是否正常运行')
  }
}

// 将难度转换为等级
const getLevelFromDifficulty = (difficulty) => {
  if (difficulty <= 2) return '初级'
  if (difficulty <= 4) return '中级'
  return '高级'
}

// 根据类型获取图标
const getIconFromType = (type) => {
  if (type.includes('密码生成')) return '🔐'
  if (type.includes('密码存储')) return '💾'
  if (type.includes('密码传输')) return '📡'
  if (type.includes('密码验证')) return '✅'
  if (type.includes('算法攻防')) return '🧮'
  if (type.includes('对称密码')) return '🔒'
  if (type.includes('非对称密码')) return '🔑'
  if (type.includes('古典密码')) return '📜'
  if (type.includes('综合攻防')) return '🛡️'
  return '⚔️'
}

// 根据防御等级获取标签类型
const getDefenseLevelType = (level) => {
  if (level === 'High') return 'danger'
  if (level === 'Medium') return 'warning'
  if (level === 'Low') return 'success'
  return 'info'
}

// 处理加固
const handleHarden = async (target) => {
  // 模拟加固过程
  target.status = '加固中'
  
  // 简化加固逻辑，确保成功执行
  setTimeout(() => {
    target.status = '已加固'
    ElMessage({ message: `目标 ${target.name} 加固成功！已应用所有防御措施：智能密钥生成+生命周期管控、SM2+SM4双层加密+AI流量实时监控、国密认证白名单+自动化漏洞管理、主机安全加固+AI权限精细化管控。`, type: 'success' })
    
    // 更新进度
    hardeningProgress.value += 25
    
    // 检查是否所有目标都已加固
    const allHardened = defenseTargets.value.every(t => t.status === '已加固')
    if (allHardened) {
      defenseFlowSteps.value[2].status = 'completed'
      defenseFlowSteps.value[2].result = '所有漏洞已修复，系统安全性提升'
      defenseFlowSteps.value[3].status = 'current'
      currentPhase.value = '第二轮防御'
    }
  }, 2000)
}

// 处理AI评分
const handleAIScore = () => {
  // 显示AI评分对话框
  aiScoreDialogVisible.value = true
  aiScoreStatus.value = 'scoring'
  
  // 模拟AI评分过程
  setTimeout(() => {
    aiScoreStatus.value = 'reporting'
    
    // 模拟报告生成过程
    setTimeout(() => {
      aiScoreDialogVisible.value = false
      
      // 设置评分结果
      const defensePlanScore = 95
      const hardeningEffectScore = 90
      defenseScore.value = Math.round((defensePlanScore + hardeningEffectScore) / 2) // 取平均分93分
      defenseReportComment.value = '防御方案全面、对SM4算法加密交通数据靶场加固到位，成功应用了智能密钥生成+生命周期管控、SM2+SM4双层加密+AI流量实时监控、国密认证白名单+自动化漏洞管理、主机安全加固+AI权限精细化管控等高级防御措施，成功阻断了所有攻击，防御能力达到高级水平。'
      
      // 显示评分结果
      showDefenseScore.value = true
      
      // 开始AI深度思考
      simulateAIThinking()
    }, 3000)
  }, 2000)
}

const handleStartTraining = (scenario) => {
  console.log('开始训练:', scenario.title)
  // 这里可以添加跳转到训练页面的逻辑
  ElMessage.success(`开始训练：${scenario.title}`)
}

// 模拟AI深度思考过程
const simulateAIThinking = () => {
  // 多个版本的深度思考内容，增加多样性
  const deepThinkingVersions = [
    [
      'AI评分中......攻击报告生成中........防御报告生成中........',
      '1. 攻击端策略推演',
      '- 初始评估：攻击端首次尝试时，对目标系统的SM4加密交通数据靶场进行了精准的漏洞扫描与利用，成功突破防御。AI系统判定其策略合理性与工具规范性达到95分。',
      '- 风险预判：AI系统监测到攻击端在首次成功后，未及时根据靶场加固反馈调整策略，仍沿用原攻击路径，导致第二次尝试时漏洞已被封堵，评分骤降至70分。',
      '- 优化建议：AI生成攻击端优化方案，建议其建立动态策略库，在每次攻击后根据防御响应实时调整渗透路径，避免策略固化导致的失败。',
      '2. 防御端能力评估',
      '- 优势识别：防御端对SM4算法加密交通数据靶场的加固方案全面且执行到位，成功应用了智能密钥生成+生命周期管控、SM2+SM4双层加密+AI流量实时监控、国密认证白名单+自动化漏洞管理、主机安全加固+AI权限精细化管控等高级防御措施，成功阻断了所有攻击尝试。AI系统给出93分的高分评价。',
      '- 潜在短板：AI分析发现防御端的策略库主要针对已知攻击手法，对新型、未知攻击的检测与响应能力存在盲区。建议加强对零日漏洞和高级威胁的学习与演练。',
      '3. 整体攻防态势研判',
      '- 攻击端：具备较强的单点突破能力，但缺乏动态适应与持续迭代能力，后续需重点提升策略调整的敏捷性。',
      '- 防御端：在已知威胁防御上表现优异，特别是应用了多项高级防御措施，防御能力达到高级水平，但在应对新型攻击时存在短板，需构建更具前瞻性的防御体系。',
      '- 综合结论：本次攻防演练中，防御端整体表现优于攻击端，成功应用了多项高级防御措施，有效阻断了所有攻击尝试，但双方均存在明显的优化空间，后续需针对性强化动态对抗能力。'
    ]
  ]
  
  // 随机选择一个版本
  const randomVersion = deepThinkingVersions[Math.floor(Math.random() * deepThinkingVersions.length)]
  let currentSentence = 0
  let displayedText = ''
  
  // 逐句显示深度思考内容
  const interval = setInterval(() => {
    if (currentSentence < randomVersion.length) {
      displayedText += randomVersion[currentSentence]
      aiStatusText.value = displayedText
      currentSentence++
    } else {
      clearInterval(interval)
      // 深度思考完成后，显示防御报告
      setTimeout(() => {
        showDeepThinking.value = false
        showDefenseReport.value = true
        aiScoreProgress.value = 100
        ElMessage({ message: '防御演练完成！', type: 'success' })
      }, 2000)
    }
  }, 1500)
}

// 生成防御报告
const generateDefenseReport = () => {
  // 模拟生成防御报告
  setTimeout(() => {
    ElMessage({
      message: '防御报告生成完成！',
      type: 'success',
      duration: 3000
    })
    
    // 这里可以添加报告显示逻辑，比如打开报告模态框
    console.log('防御报告生成完成')
  }, 2000)
}

// 组件挂载时初始化
onMounted(() => {
  fetchScenarios()
  // 获取防御措施
  getDefenseMeasures()
  // 初始状态设置
  aiStatusText.value = '防御流程完成后，AI将进行深度分析和评分...'
  showDeepThinking.value = true
})

// 下载防御报告
const downloadDefenseReport = () => {
  ElMessage.success('报告下载成功！')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  min-height: calc(100vh - 80px);
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h1 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--text-color);
}

.page-header p {
  font-size: 16px;
  color: var(--text-secondary);
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
  max-width: 1200px;
  margin: 0 auto;
}

.mb-20 {
  margin-bottom: 20px;
}

.monitor-card {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.monitor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-primary {
  color: var(--primary-color);
  font-weight: 600;
}

.text-success {
  color: var(--success-color);
}

.blink {
  animation: blink 1s infinite;
}

@keyframes blink {
  50% { opacity: 0.5; }
}

.status-bars {
  padding: 20px 0;
}

.status-item {
  margin-bottom: 20px;
}

.status-label {
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-size: 14px;
}

.ai-status {
  padding: 10px 0;
}

.ai-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}

.ai-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.ai-label {
  color: var(--text-secondary);
  font-size: 14px;
}

.ai-value {
  color: var(--text-color);
  font-weight: 600;
}

.stat-card {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  text-align: center;
  padding: 30px 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  border-color: var(--primary-color);
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 防御流程样式 */
.defense-flow {
  padding: 10px 0;
}

.flow-step {
  display: flex;
  margin-bottom: 20px;
  position: relative;
}

.flow-step::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 40px;
  bottom: -20px;
  width: 2px;
  background: var(--border-color);
}

.flow-step:last-child::before {
  display: none;
}

.flow-step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-light);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: var(--text-secondary);
  margin-right: 15px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.flow-step.completed .flow-step-number {
  background: var(--success-color);
  border-color: var(--success-color);
  color: white;
}

.flow-step.current .flow-step-number {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(0, 122, 255, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(0, 122, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 122, 255, 0); }
}

.flow-step-content {
  flex: 1;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.flow-step.completed .flow-step-content {
  border-color: var(--success-color);
  box-shadow: 0 2px 12px rgba(103, 194, 58, 0.3);
}

.flow-step.current .flow-step-content {
  border-color: var(--primary-color);
  box-shadow: 0 2px 12px rgba(0, 122, 255, 0.3);
}

.flow-step-title {
  font-weight: bold;
  color: var(--text-color);
  margin-bottom: 5px;
  font-size: 16px;
}

.flow-step-description {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 10px;
}

.flow-step-result {
  color: var(--success-color);
  font-size: 14px;
  font-weight: 500;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}

:deep(.el-table) {
  background: transparent;
}

:deep(.el-table th) {
  background: var(--bg-light);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-table tr) {
  background: var(--bg-light);
}

:deep(.el-table td) {
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-table__empty-text) {
  color: var(--text-secondary);
}

/* AI深度思考样式 */
.ai-deep-thinking {
  padding: 20px;
  min-height: 300px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  background: var(--bg-light);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  overflow-y: auto;
}

.deep-thinking-text {
  font-size: 14px;
  color: var(--text-color);
  font-weight: 400;
  line-height: 1.6;
  text-align: left;
  animation: fadeIn 1s ease-in-out;
  width: 100%;
}

/* 滚动条样式 */
.ai-deep-thinking::-webkit-scrollbar {
  width: 6px;
}

.ai-deep-thinking::-webkit-scrollbar-track {
  background: var(--bg-light);
  border-radius: 3px;
}

.ai-deep-thinking::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

.ai-deep-thinking::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
}

@keyframes fadeIn {
  from { opacity: 0.5; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 评分卡片样式 */
.score-card {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.score-result {
  padding: 20px;
}

.score-main {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 50px;
  margin-bottom: 30px;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #67c23a 0%, #409eff 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(103, 194, 58, 0.4);
}

.score-circle.defense {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.score-number {
  font-size: 48px;
  font-weight: bold;
  color: white;
}

.score-unit {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
}

.score-breakdown {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.score-item {
  padding: 10px 20px;
  background: var(--bg-light);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.score-label {
  color: var(--text-secondary);
  font-size: 14px;
}

.score-value {
  font-size: 18px;
  font-weight: bold;
  margin-left: 10px;
}

.score-comment {
  padding: 20px;
  background: var(--bg-light);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.score-comment h4 {
  color: var(--text-color);
  margin-bottom: 10px;
}

.score-comment p {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* 报告卡片样式 */
.report-card {
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.report-content {
  padding: 20px;
}

.report-content h3 {
  text-align: center;
  color: var(--text-color);
  margin-bottom: 30px;
  font-size: 24px;
}

.report-section {
  margin-bottom: 20px;
}

.report-section h4 {
  color: var(--text-color);
  margin-bottom: 10px;
  font-size: 16px;
}

.report-section p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.report-section ul {
  list-style: none;
  padding-left: 0;
}

.report-section ul li {
  color: var(--text-secondary);
  padding: 5px 0;
  padding-left: 20px;
  position: relative;
}

.report-section ul li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--primary-color);
}

/* AI评分状态样式 */
.ai-score-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.status-icon {
  font-size: 64px;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.status-text {
  font-size: 18px;
  color: var(--text-color);
  font-weight: 500;
}

.is-loading {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 目标名称样式 */
.target-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.target-icon {
  font-size: 16px;
}

.target-text {
  color: var(--text-color);
  font-size: 14px;
  line-height: 1.4;
  word-break: break-word;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  background: #1a1a1a !important;
}

:deep(.el-table__header-wrapper) {
  background: #1a1a1a !important;
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-table__body-wrapper) {
  background: #1a1a1a !important;
}

:deep(.el-table tr) {
  background: #1a1a1a !important;
}

:deep(.el-table tr:hover > td) {
  background: rgba(0, 122, 255, 0.1) !important;
}

:deep(.el-table tr.el-table__row--striped) {
  background: #1a1a1a !important;
}

:deep(.el-table td) {
  border-bottom: 1px solid var(--border-color) !important;
  color: var(--text-color) !important;
}

:deep(.el-table th) {
  background: #1a1a1a !important;
  border-bottom: 1px solid var(--border-color) !important;
  color: var(--text-secondary) !important;
}
</style>