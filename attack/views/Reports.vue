<template>
  <div class="reports-container">
    <div class="page-header">
      <h2>攻击分析报告</h2>
      <div class="ops">
        <el-button @click="loadData">刷新</el-button>
        <el-button type="primary" plain @click="exportAllJson">导出全部(JSON)</el-button>
        <el-button type="primary" plain @click="exportAllCsv">导出全部(CSV)</el-button>
      </div>
    </div>
    <el-table :data="reports" style="width: 100%" @row-click="openDetail">
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="target" label="攻击目标" />
      <el-table-column label="结果">
        <template #default="{ row }">
          <el-tag :type="row.success ? 'success' : 'danger'">
            {{ row.success ? '成功' : '拦截' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="步骤">
        <template #default="{ row }">
          <el-tag v-for="s in row.steps" :key="s" style="margin-right: 6px">{{ s }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="耗时(ms)" width="120" />
      <el-table-column prop="reason" label="说明" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button link type="primary" @click.stop="openDetail(row)">查看</el-button>
          <el-button link type="success" @click.stop="exportJson(row)">导出</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="detailVisible" title="攻击报告详情" width="600px">
      <div class="detail">
        <div class="row"><span>ID</span><span>{{ detailItem?.id }}</span></div>
        <div class="row"><span>目标</span><span>{{ detailItem?.target }}</span></div>
        <div class="row"><span>结果</span><span>{{ detailItem?.success ? '成功' : '拦截' }}</span></div>
        <div class="row"><span>耗时</span><span>{{ detailItem?.duration }} ms</span></div>
        <div class="row"><span>AI评分</span><span>{{ detailItem?.aiScore }}</span></div>
        <div class="row"><span>说明</span><span>{{ detailItem?.reason }}</span></div>
        <div class="row"><span>步骤</span><span>{{ (detailItem?.steps || []).join(' / ') }}</span></div>
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

const loadData = async () => {
  try {
    reports.value = await api.get('/api/attacks/reports')
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
  a.download = `attack-report-${row.id}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const exportAllJson = () => {
  const dataStr = JSON.stringify(reports.value, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `attack-reports.json`
  a.click()
  URL.revokeObjectURL(url)
}

const exportAllCsv = () => {
  const header = ['id','target','success','duration','aiScore','reason','steps']
  const lines = [header.join(',')]
  for (const r of reports.value) {
    const row = [
      r.id,
      `"${r.target || ''}"`,
      r.success,
      r.duration,
      r.aiScore ?? '',
      `"${(r.reason || '').replace(/"/g,'""')}"`,
      `"${(r.steps || []).join('|').replace(/"/g,'""')}"`
    ]
    lines.push(row.join(','))
  }
  const blob = new Blob([lines.join('\n')], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'attack-reports.csv'
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
.ops { display: flex; gap: 10px; }
.detail .row { display: flex; justify-content: space-between; margin: 8px 0; }
</style>

