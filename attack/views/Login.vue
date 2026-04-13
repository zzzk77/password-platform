<template>
  <LoginForm title="攻击端登录 - 密码虚拟攻防平台" @login="onLogin" />
</template>

<script setup>
import LoginForm from '@/../shared/components/LoginForm.vue'
import { useAuthStore } from '@/../shared/stores/auth.js'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const router = useRouter()

const onLogin = async ({ username, password }) => {
  try {
    await authStore.login(username, password)
    ElMessage.success('登录成功')
    router.push('/attack/dashboard')
  } catch (error) {
    ElMessage.error('登录失败: ' + error.message)
  }
}
</script>
