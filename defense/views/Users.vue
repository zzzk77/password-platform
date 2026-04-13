<template>
  <div class="users-container">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleAddUser">
        <el-icon><Plus /></el-icon>
        新增用户
      </el-button>
    </div>

    <el-card class="table-card">
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="department" label="部门" />
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">{{ getRoleLabel(row.role) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" effect="plain">
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最后登录时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 用户表单弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增用户' : '编辑用户'"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="form.department" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
            <el-option label="审计员" value="auditor" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch
            v-model="form.status"
            active-value="active"
            inactive-value="inactive"
            active-text="正常"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Storage } from '@/utils/storage'
import { api } from '@/utils/api'

const users = ref([])
const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' or 'edit'
const formRef = ref(null)

const form = reactive({
  id: null,
  username: '',
  department: '',
  role: '',
  status: 'active'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }]
}

onMounted(async () => {
  await loadUsers()
})

const loadUsers = async () => {
  try {
    users.value = await api.get('/api/users')
  } catch (e) {
    users.value = Storage.get(Storage.KEYS.USERS, [])
  }
}

const getRoleType = (role) => {
  const map = { admin: 'danger', user: 'primary', auditor: 'warning' }
  return map[role] || 'info'
}

const getRoleLabel = (role) => {
  const map = { admin: '管理员', user: '普通用户', auditor: '审计员' }
  return map[role] || role
}

const handleAddUser = () => {
  dialogType.value = 'add'
  Object.assign(form, {
    id: null,
    username: '',
    department: '',
    role: '',
    status: 'active'
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${row.username}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    api.del(`/api/users/${row.id}`).then(async () => {
      ElMessage.success('删除成功')
      await loadUsers()
    }).catch(() => {
      const newUsers = users.value.filter(u => u.id !== row.id)
      Storage.set(Storage.KEYS.USERS, newUsers)
      loadUsers()
      ElMessage.success('删除成功(本地)')
    })
  }).catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      if (dialogType.value === 'add') {
        const newUser = {
          ...form,
          id: Date.now(),
          lastLogin: '-'
        }
        api.post('/api/users', newUser).then(async () => {
          ElMessage.success('新增成功')
          dialogVisible.value = false
          await loadUsers()
        }).catch(() => {
          Storage.add(Storage.KEYS.USERS, newUser)
          ElMessage.success('新增成功(本地)')
          dialogVisible.value = false
          loadUsers()
        })
      } else {
        api.put(`/api/users/${form.id}`, form).then(async () => {
          ElMessage.success('更新成功')
          dialogVisible.value = false
          await loadUsers()
        }).catch(() => {
          Storage.update(Storage.KEYS.USERS, form.id, form)
          ElMessage.success('更新成功(本地)')
          dialogVisible.value = false
          loadUsers()
        })
      }
    }
  })
}
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--text-primary);
}

.table-card {
  border-radius: 8px;
}
</style>
