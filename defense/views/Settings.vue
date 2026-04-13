<template>
  <div class="settings-container">
    <div class="page-header">
      <h2>系统设置</h2>
      <div>
        <el-button type="primary" @click="save">保存</el-button>
        <el-button @click="load">刷新</el-button>
      </div>
    </div>
    <el-card class="section-card">
      <h3 class="section-title">资源阈值</h3>
      <el-form :model="form" label-width="120px" style="max-width: 600px">
        <el-form-item label="CPU阈值(%)">
          <el-input-number v-model="form.resourceThreshold.cpu" :min="10" :max="100" />
        </el-form-item>
        <el-form-item label="内存阈值(%)">
          <el-input-number v-model="form.resourceThreshold.mem" :min="10" :max="100" />
        </el-form-item>
        <el-form-item label="启用日志">
          <el-switch v-model="form.logging" />
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="section-card">
      <h3 class="section-title">系统日志</h3>
      <el-table :data="logs" style="width: 100%">
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="msg" label="内容" />
        <el-table-column prop="time" label="时间" width="220" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'
import { ElMessage } from 'element-plus'

const form = ref({ resourceThreshold: { cpu: 80, mem: 80 }, logging: true })
const logs = ref([])

const load = async () => {
  try {
    form.value = await api.get('/api/settings')
    logs.value = await api.get('/api/settings/logs')
  } catch (e) {
    ElMessage.error('加载设置失败')
  }
}

const save = async () => {
  try {
    const res = await api.post('/api/settings', form.value)
    if (res && res.ok) {
      ElMessage.success('保存成功')
      logs.value = await api.get('/api/settings/logs')
    } else {
      ElMessage.error('保存失败')
    }
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

onMounted(load)
</script>

<style scoped>
.settings-container {
  padding: 20px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-card {
  margin-bottom: 20px;
}
.section-title {
  margin-bottom: 10px;
}
</style>
