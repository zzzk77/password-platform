<template>
  <div class="permissions-container">
    <div class="header flex-between mb-20">
      <div class="title">
        <el-icon><Lock /></el-icon>
        <span>角色-权限映射配置</span>
      </div>
      <div class="actions">
        <el-button type="primary" @click="handleSave">保存配置</el-button>
        <el-button @click="handleReset">恢复默认</el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col v-for="role in roles" :key="role" :span="8">
        <el-card shadow="never" class="role-card">
          <div class="role-header">
            <el-tag :type="getRoleType(role)">{{ getRoleLabel(role) }}</el-tag>
          </div>
          <el-checkbox-group v-model="rolePermissions[role]" class="perm-group">
            <el-checkbox v-for="perm in permissions" :key="perm.key" :label="perm.key">
              {{ perm.label }}
            </el-checkbox>
          </el-checkbox-group>
        </el-card>
      </el-col>
    </el-row>
  </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
import { Storage } from '@/utils/storage'
import { api } from '@/utils/api'
  import { Lock } from '@element-plus/icons-vue'
  
  const permissions = ref([
    { key: 'scenario_edit', label: '场景编辑' },
    { key: 'attack_simulate', label: '攻击模拟' },
    { key: 'defense_simulate', label: '防御模拟' },
    { key: 'view_reports', label: '报告查看' },
    { key: 'manage_users', label: '用户管理' },
    { key: 'manage_targets', label: '靶场管理' },
    { key: 'manage_vulnerabilities', label: '漏洞管理' },
    { key: 'system_config', label: '系统配置' }
  ])
  
  const roles = ref([])
  const rolePermissions = reactive({})
  
  const getRoleLabel = (role) => {
    if (role === 'admin') return '管理员'
    if (role === 'user') return '普通用户'
    if (role === 'auditor') return '审计员'
    return role
  }
  
  const getRoleType = (role) => {
    if (role === 'admin') return 'danger'
    if (role === 'user') return 'warning'
    if (role === 'auditor') return 'success'
    return 'info'
  }
  
  const buildDefaultMapping = () => {
    return {
      admin: permissions.value.map(p => p.key),
      user: ['scenario_edit', 'attack_simulate', 'view_reports', 'manage_targets'],
      auditor: ['view_reports', 'manage_vulnerabilities']
    }
  }
  
const loadData = async () => {
  const users = Storage.get(Storage.KEYS.USERS, [])
  const uniqueRoles = Array.from(new Set(users.map(u => u.role)))
  roles.value = uniqueRoles.length ? uniqueRoles : ['admin', 'user', 'auditor']
  
  let saved = Storage.get(Storage.KEYS.ROLE_PERMISSIONS, null)
  try {
    saved = await api.get('/api/roles/permissions')
  } catch (e) {}
  const defaults = buildDefaultMapping()
  
  roles.value.forEach(r => {
    rolePermissions[r] = saved?.[r]?.slice() || (defaults[r] ? defaults[r].slice() : [])
  })
}

const handleSave = async () => {
  const data = JSON.parse(JSON.stringify(rolePermissions))
  try {
    await api.post('/api/roles/permissions', data)
    Storage.set(Storage.KEYS.ROLE_PERMISSIONS, data)
    ElMessage.success('权限配置已保存')
  } catch (e) {
    Storage.set(Storage.KEYS.ROLE_PERMISSIONS, data)
    ElMessage.success('权限配置已保存(本地)')
  }
}
  
  const handleReset = () => {
    const defaults = buildDefaultMapping()
    roles.value.forEach(r => {
      rolePermissions[r] = defaults[r] ? defaults[r].slice() : []
    })
    ElMessage.success('已恢复默认配置')
  }
  
  onMounted(() => {
    loadData()
  })
  </script>
  
  <style scoped>
  .permissions-container {
    color: var(--text-color);
  }
  .flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .mb-20 { margin-bottom: 20px; }
  
  .title {
    display: flex;
    gap: 8px;
    align-items: center;
    font-weight: 600;
    color: var(--text-color);
  }
  .actions {
    display: flex;
    gap: 10px;
  }
  
  .role-card {
    height: 220px;
  }
  
  .role-header {
    margin-bottom: 10px;
  }
  
  .perm-group {
    display: grid;
    grid-template-columns: 1fr;
    row-gap: 8px;
  }
  </style>
