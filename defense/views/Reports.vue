<template>
  <div class="reports-container">
    <div class="page-header">
      <h2>防御报告</h2>
      <div class="ops">
        <el-button @click="loadData">刷新</el-button>
        <el-button type="primary" plain @click="exportAllJson">导出全部(JSON)</el-button>
        <el-button type="primary" plain @click="exportAllCsv">导出全部(CSV)</el-button>
      </div>
    </div>
    <el-card class="table-card">
      <el-table :data="reports" style="width: 100%" @row-click="openDetail">
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="target" label="目标" />
        <el-table-column prop="strategy" label="防御策略" />
        <el-table-column label="拦截率">
          <template #default="{ row }">
            <el-progress :percentage="row.blockedRate" :format="formatPct" />
          </template>
        </el-table-column>
        <el-table-column label="AI评分" width="120">
          <template #default="{ row }">
            <el-tag :type="getScoreType(row.aiScore)">{{ row.aiScore }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="缺陷分析">
          <template #default="{ row }">
            <el-tag v-for="v in row.vulns || []" :key="v" type="danger" effect="plain" style="margin-right: 6px">{{ v }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="防御要点">
          <template #default="{ row }">
            <el-tag v-for="d in row.details || []" :key="d" type="success" effect="plain" style="margin-right: 6px">{{ d }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click.stop="openDetail(row)">查看</el-button>
            <el-button link type="success" @click.stop="exportJson(row)">导出</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog v-model="detailVisible" title="防御报告详情" width="600px">
      <div class="detail">
        <div class="row"><span>ID</span><span>{{ detailItem?.id }}</span></div>
        <div class="row"><span>目标</span><span>{{ detailItem?.target }}</span></div>
        <div class="row"><span>防御策略</span><span>{{ detailItem?.strategy }}</span></div>
        <div class="row"><span>拦截率</span><span>{{ detailItem?.blockedRate }}%</span></div>
        <div class="row"><span>AI评分</span><span>{{ detailItem?.aiScore }}</span></div>
        <div class="row"><span>缺陷分析</span><span>{{ (detailItem?.vulns || []).join(' / ') }}</span></div>
        <div class="row"><span>防御要点</span><span>{{ (detailItem?.details || []).join(' / ') }}</span></div>
        <div class="row" v-if="detailItem?.correlationId"><span>关联攻击报告ID</span><span>{{ detailItem?.correlationId }}</span></div>
      </div>
      <template #footer>
        <el-button type="primary" @click="exportJson(detailItem)">导出JSON</el-button>
        <el-button @click="detailVisible=false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'
import { ElMessage } from 'element-plus'

const reports = ref([])
const detailVisible = ref(false)
const detailItem = ref(null)
const formatPct = (p) => `${p}%`
const getScoreType = (s) => s >= 80 ? 'success' : s >= 60 ? 'warning' : 'danger'

const loadData = async () => {
  try {
    reports.value = await api.get('/api/defense/reports')
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

onMounted(loadData)

const openDetail = (row) => {
  detailItem.value = row
  detailVisible.value = true
}

const exportJson = (row) => {
  const dataStr = JSON.stringify(row, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `defense-report-${row.id}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const exportAllJson = () => {
  const dataStr = JSON.stringify(reports.value, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `defense-reports.json`
  a.click()
  URL.revokeObjectURL(url)
}

const exportAllCsv = () => {
  const header = ['id','target','strategy','blockedRate','aiScore','vulns','details','correlationId']
  const lines = [header.join(',')]
  for (const r of reports.value) {
    const row = [
      r.id,
      `"${(r.target || '').replace(/"/g,'""')}"`,
      `"${(r.strategy || '').replace(/"/g,'""')}"`,
      r.blockedRate ?? '',
      r.aiScore ?? '',
      `"${(r.vulns || []).join('|').replace(/"/g,'""')}"`,
      `"${(r.details || []).join('|').replace(/"/g,'""')}"`,
      r.correlationId ?? ''
    ]
    lines.push(row.join(','))
  }
  const blob = new Blob([lines.join('\n')], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'defense-reports.csv'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.reports-container {
  padding: 20px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.table-card {
  border-radius: 8px;
}
.ops { display: flex; gap: 10px; }
.detail .row { display: flex; justify-content: space-between; margin: 8px 0; }
</style>
