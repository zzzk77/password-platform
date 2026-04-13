<template>
  <div class="dashboard-container">
    <!-- 实时攻击状态 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="16">
        <el-card class="monitor-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">⚡ 实时攻击状态</span>
              <el-tag type="warning" effect="dark" class="blink">{{ aiStatusText }}</el-tag>
            </div>
          </template>
          <div class="status-bars">
            <div class="status-item">
              <div class="status-label">攻击进度</div>
              <el-progress :percentage="attackProgress" :color="'var(--primary-color)'" />
            </div>
            <div class="status-item">
              <div class="status-label">破解进度</div>
              <el-progress :percentage="crackProgress" :color="'var(--warning-color)'" />
            </div>
            <div class="status-item">
              <div class="status-label">AI评分进度</div>
              <el-progress :percentage="aiScoreProgress" :color="'var(--success-color)'" />
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🤖 AI攻击体状态</span>
          </template>
          <div class="ai-status">
            <div class="ai-item">
              <span class="ai-label">版本</span>
              <span class="ai-value">DeepAttack v2.1</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">训练完成度</span>
              <span class="ai-value text-success">93.5%</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">攻击成功率</span>
              <span class="ai-value text-success">89.5%</span>
            </div>
            <div class="ai-item">
              <span class="ai-label">当前阶段</span>
              <span class="ai-value" :class="{ 'text-success': currentPhase === '第一轮攻击', 'text-warning': currentPhase === '第二轮攻击', 'text-info': currentPhase === '分析阶段' }">{{ currentPhase }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- AI评分结果展示 -->
    <el-row :gutter="20" class="mb-20" v-if="showAttackScore">
      <el-col :span="24">
        <el-card class="score-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">🎯 攻击端AI评分结果</span>
              <el-tag type="danger" effect="dark">攻击端</el-tag>
            </div>
          </template>
          <div class="score-result">
            <div class="score-main">
              <div class="score-circle">
                <span class="score-number">{{ attackScore }}</span>
                <span class="score-unit">分</span>
              </div>
              <div class="score-breakdown">
                <div class="score-item">
                  <span class="score-label">第一次攻击评分：</span>
                  <span class="score-value text-success">{{ firstAttackScore }}分</span>
                </div>
                <div class="score-item">
                  <span class="score-label">第二次攻击评分：</span>
                  <span class="score-value text-warning">{{ secondAttackScore }}分</span>
                </div>
              </div>
            </div>
            <div class="score-comment">
              <h4>📋 攻击报告评价</h4>
              <p>{{ attackReportComment }}</p>
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

    <!-- 攻击报告展示 -->
    <el-row :gutter="20" class="mb-20" v-if="showAttackReport">
      <el-col :span="24">
        <el-card class="report-card">
          <template #header>
            <div class="flex-between">
              <span class="text-primary">📄 攻击报告</span>
              <el-button type="primary" size="small" @click="downloadAttackReport">下载报告</el-button>
            </div>
          </template>
          <div class="report-content">
            <h3>密码攻击演练分析报告</h3>
            <div class="report-section">
              <h4>一、攻击概述</h4>
              <p>本次攻击演练分为两个阶段，第一阶段成功挖掘到目标系统的安全漏洞，第二阶段因防守方已实施加固措施，攻击未能成功。</p>
            </div>
            <div class="report-section">
              <h4>二、攻击向量分析</h4>
              <p>主要采用暴力破解、字典攻击和Hash破解等攻击手段，针对目标系统的弱密码策略进行攻击。</p>
            </div>
            <div class="report-section">
              <h4>三、攻击结果</h4>
              <ul>
                <li>第一次攻击：成功挖掘漏洞，评分95分</li>
                <li>第二次攻击：未能挖掘新漏洞，评分70分</li>
                <li>综合评分：83分</li>
              </ul>
            </div>
            <div class="report-section">
              <h4>四、改进建议</h4>
              <p>攻击方应加强对新型攻击手法的学习，如社会工程学攻击和零日漏洞利用，提高应对防御措施的能力。</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-value">{{ completedScenarios }}</div>
          <div class="stat-label">已完成的场景</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">🔓</div>
          <div class="stat-value">{{ crackedSystems }}</div>
          <div class="stat-label">破解的系统</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon">⏱️</div>
          <div class="stat-value">{{ averageTime }}</div>
          <div class="stat-label">平均破解时间</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- AI深度思考 -->
    <el-row :gutter="20" class="mb-20">
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

    <!-- 攻击流程展示 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="12">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">📊 攻击流程</span>
          </template>
          <div class="attack-flow">
            <div 
              v-for="(step, index) in attackFlowSteps" 
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
              <span class="text-primary">🎯 攻击目标列表</span>
              <el-button 
                type="primary" 
                @click="handleAIScore"
              >
                AI评分
              </el-button>
            </div>
          </template>
          <el-table :data="targets" style="width: 100%">
            <el-table-column prop="name" label="目标" width="220">
              <template #default="scope">
                <div class="target-name">
                  <span class="target-icon">🎯</span>
                  <span class="target-text">{{ scope.row.name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="defenseLevel" label="防御等级" width="120">
              <template #default="scope">
                <el-tag 
                  :type="{
                    'High': 'danger',
                    'Medium': 'warning',
                    'Low': 'success'
                  }[scope.row.defenseLevel]"
                  effect="dark"
                >
                  {{ scope.row.defenseLevel }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="vulnerable" label="可攻破" width="100">
              <template #default="scope">
                <el-tag 
                  :type="scope.row.vulnerable ? 'success' : 'danger'"
                  effect="dark"
                >
                  {{ scope.row.vulnerable ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="scope">
                <el-tag 
                  :type="{
                    '未攻击': 'info',
                    '攻击中': 'warning',
                    '攻击成功': 'success',
                    '攻击失败': 'danger',
                    '已攻击': 'success'
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
                  type="primary" 
                  size="small"
                  :disabled="scope.row.status === '已攻击' || scope.row.status === '攻击中'"
                  @click="handleAttack(scope.row)"
                >
                  攻击
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
        <div class="status-text" v-else-if="aiScoreStatus === 'reporting'">攻击报告生成中...</div>
      </div>
    </el-dialog>

    <!-- 工具使用统计 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="24">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🔧 工具使用统计</span>
          </template>
          <div class="chart-container" ref="toolChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- DeepSeek AI 助手 -->
    <el-row :gutter="20" class="mb-20">
      <el-col :span="24">
        <el-card class="monitor-card">
          <template #header>
            <span class="text-primary">🤖 DeepSeek AI 助手</span>
          </template>
          <DeepSeekChat :context="'密码虚拟攻防平台 - 攻击端'" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { api } from '@/../shared/utils/api.js'
import DeepSeekChat from '../components/DeepSeekChat.vue'

// 攻击场景数据
const attackScenarios = ref([])
// 攻击目标数据
const targets = ref([
  { name: '访客WiFi网络', defenseLevel: 'Low', vulnerable: true, status: '已攻击', action: '攻击' },
  { name: '智能门禁系统', defenseLevel: 'Low', vulnerable: true, status: '未攻击', action: '攻击' },
  { name: '员工考勤管理系统', defenseLevel: 'Medium', vulnerable: true, status: '已攻击', action: '攻击' },
  { name: '企业VPN系统', defenseLevel: 'Medium', vulnerable: true, status: '未攻击', action: '攻击' },
  { name: '基于国密SM4加密的交通管理系统', defenseLevel: 'High', vulnerable: true, status: '未攻击', action: '攻击' },
  { name: '企业内部邮件系统', defenseLevel: 'High', vulnerable: true, status: '未攻击', action: '攻击' },
  { name: '金融交易平台', defenseLevel: 'High', vulnerable: true, status: '未攻击', action: '攻击' }
])

// 攻击流程步骤
const attackFlowSteps = ref([
  {
    title: '第一轮攻击',
    description: '从多个角度进行攻击尝试',
    status: 'completed',
    result: '攻击成功，所有目标均被攻破'
  },
  {
    title: '防守方加固',
    description: '防守方针对攻击漏洞进行加固',
    status: 'completed',
    result: '防御措施已实施，系统安全性提升'
  },
  {
    title: '第二轮攻击',
    description: '从相同角度再次尝试攻击',
    status: 'current',
    result: ''
  },
  {
    title: 'AI分析与评分',
    description: 'AI对攻击过程进行深度分析和评分',
    status: 'pending',
    result: ''
  }
])

// 响应式数据
const attackProgress = ref(60)
const crackProgress = ref(45)
const aiScoreProgress = ref(30)
const currentPhase = ref('第二轮攻击')
const completedScenarios = ref(12)
const crackedSystems = ref(5)
const averageTime = ref('45s')

// AI评分结果
const showAttackScore = ref(false)
const showDeepThinking = ref(false)
const showAttackReport = ref(false)
const attackScore = ref(83)
const firstAttackScore = ref(95)
const secondAttackScore = ref(70)
const attackReportComment = ref('攻击策略合理、平台工具应用规范，第一次漏洞挖掘成功，第二次漏洞挖掘失败，没有及时调整攻击策略，有待后续进一步优化。')

// AI状态文本
const aiStatusText = ref('AI评分中......攻击报告生成中........防御报告生成中........')

// AI评分相关数据
const aiScoreDialogVisible = ref(false)
const aiScoreStatus = ref('scoring') // scoring, reporting, completed

// 图表引用
const toolChartRef = ref(null)
let toolChart = null

// 初始化图表
const initCharts = () => {
  nextTick(() => {
    if (toolChartRef.value) {
      toolChart = echarts.init(toolChartRef.value)
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '工具使用',
            type: 'pie',
            radius: '70%',
            data: [
              { value: 35, name: '暴力破解' },
              { value: 25, name: '字典攻击' },
              { value: 20, name: 'Hash破解' },
              { value: 15, name: 'SQL注入' },
              { value: 5, name: '其他' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      toolChart.setOption(option)
    }
  })
}

// 获取攻击场景
const getAttackScenarios = async () => {
  try {
    const response = await api.get('/attack/scenarios')
    attackScenarios.value = response
  } catch (error) {
    console.error('获取攻击场景失败:', error)
    ElMessage.error('获取攻击场景失败')
  }
}

// 攻击轮数
const attackRound = ref(1)

// 处理攻击
const handleAttack = async (target) => {
  // 模拟攻击过程
  target.status = '攻击中'
  
  try {
    // 调用后端API执行攻击
    const response = await api.post('/attack/execute', {
      scenarioId: 7, // SM4加密交通管理系统
      round: attackRound.value
    })
    
    // 模拟攻击结果
    setTimeout(() => {
      if (attackRound.value === 1) {
        // 第一轮攻击成功
        target.status = '攻击成功'
        target.vulnerable = '✅'
        ElMessage({ 
          message: `第一轮攻击 ${target.name} 成功！`, 
          type: 'success' 
        })
      } else {
        // 第二轮攻击失败
        target.status = '攻击失败'
        target.vulnerable = '❌'
        ElMessage({ 
          message: `第二轮攻击 ${target.name} 失败！`, 
          type: 'error' 
        })
      }
      
      // 更新进度
      attackProgress.value += 10
      crackProgress.value += 5
      aiScoreProgress.value += 15
      
      // 检查是否所有目标都已攻击
      const allAttacked = targets.value.every(t => t.status !== '未攻击')
      if (allAttacked) {
        if (attackRound.value === 1) {
          // 第一轮攻击完成，进入防守方加固阶段
          attackFlowSteps.value[0].status = 'completed'
          attackFlowSteps.value[0].result = '攻击成功，所有目标均被攻破'
          attackFlowSteps.value[1].status = 'current'
          currentPhase.value = '防守方加固'
          // 准备第二轮攻击
          attackRound.value = 2
        } else {
          // 第二轮攻击完成，进入分析阶段
          attackFlowSteps.value[2].status = 'completed'
          attackFlowSteps.value[2].result = '攻击失败，所有目标均未被攻破'
          attackFlowSteps.value[3].status = 'current'
          currentPhase.value = '分析阶段'
        }
      }
    }, 1500)
  } catch (error) {
    console.error('攻击执行失败:', error)
    if (attackRound.value === 1) {
      // 第一轮攻击成功
      target.status = '攻击成功'
      target.vulnerable = '✅'
      ElMessage({ 
        message: `第一轮攻击 ${target.name} 成功！`, 
        type: 'success' 
      })
    } else {
      // 第二轮攻击失败
      target.status = '攻击失败'
      target.vulnerable = '❌'
      ElMessage({ 
        message: `第二轮攻击 ${target.name} 失败！`, 
        type: 'error' 
      })
    }
  }
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
      firstAttackScore.value = 95
      secondAttackScore.value = 70
      attackScore.value = 83
      attackReportComment.value = '攻击策略合理、平台工具应用规范，第一次漏洞挖掘成功，第二次漏洞挖掘失败，没有及时调整攻击策略，有待后续进一步优化。'
      
      // 显示评分结果
      showAttackScore.value = true
      
      // 开始AI深度思考
      simulateAIThinking()
    }, 3000)
  }, 2000)
}

// 下载攻击报告
const downloadAttackReport = () => {
  ElMessage.success('报告下载成功！')
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
      '- 优势识别：防御端对SM4算法加密交通数据靶场的加固方案全面且执行到位，成功阻断了所有攻击尝试。AI系统给出92分的高分评价。',
      '- 潜在短板：AI分析发现防御端的策略库主要针对已知攻击手法，对新型、未知攻击的检测与响应能力存在盲区。建议加强对零日漏洞和高级威胁的学习与演练。',
      '3. 整体攻防态势研判',
      '- 攻击端：具备较强的单点突破能力，但缺乏动态适应与持续迭代能力，后续需重点提升策略调整的敏捷性。',
      '- 防御端：在已知威胁防御上表现优异，但在应对新型攻击时存在短板，需构建更具前瞻性的防御体系。',
      '- 综合结论：本次攻防演练中，防御端整体表现优于攻击端，但双方均存在明显的优化空间，后续需针对性强化动态对抗能力。'
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
      // 深度思考完成后，显示攻击报告
      setTimeout(() => {
        showDeepThinking.value = false
        showAttackReport.value = true
        aiScoreProgress.value = 100
        ElMessage({ message: '攻防演练完成！', type: 'success' })
      }, 2000)
    }
  }, 1500)
}

// 组件挂载时初始化
onMounted(() => {
  initCharts()
  // 获取攻击场景
  getAttackScenarios()
  // 初始状态设置为空白，攻击流程完成后再开始AI深度思考
  aiStatusText.value = '攻击流程完成后，AI将进行深度分析和评分...'
  showDeepThinking.value = true
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  min-height: calc(100vh - 80px);
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

.chart-container {
  width: 100%;
  height: 400px;
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

/* 攻击流程样式 */
.attack-flow {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
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