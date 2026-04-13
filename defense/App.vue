<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-left">
        <div class="logo">
          <span class="logo-icon">🛡️</span>
          <span class="logo-text">密码虚拟攻防平台</span>
        </div>
      </div>
      <div class="header-center">
        <el-menu :default-active="activeNav" mode="horizontal" :background-color="'transparent'" :text-color="'var(--text-secondary)'" :active-text-color="'var(--primary-color)'" :border-bottom="'none'" @select="handleMenuSelect">
          <el-menu-item index="home">防御端控制台</el-menu-item>
          <el-menu-item index="scenarios">攻防场景</el-menu-item>
          <el-menu-item index="range">靶场演练</el-menu-item>
          <el-menu-item index="training">在线学习</el-menu-item>
          <el-menu-item index="reports">报告分析</el-menu-item>
        </el-menu>
      </div>
      <div class="header-right">
        <el-input placeholder="搜索场景" prefix-icon="Search" size="small" class="search-input"></el-input>
        <el-button type="primary" @click="goToHomePage">
          返回首页
        </el-button>
        <el-button type="primary" @click="switchToAttack">
          切换到攻击端
        </el-button>
        <el-dropdown>
          <el-button type="primary" plain>
            <el-icon><User /></el-icon>
            <span>用户</span>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人设置</el-dropdown-item>
              <el-dropdown-item>系统设置</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Message, Search, User } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeNav = ref('home')

const handleMenuSelect = (key) => {
  activeNav.value = key
  switch (key) {
    case 'home':
      router.push('/defense/dashboard')
      break
    case 'scenarios':
      router.push('/defense/labs')
      break
    case 'range':
      router.push('/defense/simulate')
      break
    case 'training':
      router.push('/defense/training')
      break
    case 'reports':
      router.push('/defense/reports')
      break
  }
}

const switchToAttack = () => {
  router.push('/attack/dashboard')
}

const goToHomePage = () => {
  window.open('http://localhost:3001', '_blank')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.app-header {
  height: 60px;
  background-color: var(--bg-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
}

.logo-icon {
  margin-right: 10px;
  font-size: 24px;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-input {
  width: 250px;
  --el-input-bg-color: var(--bg-light);
  --el-input-border-color: var(--border-color);
  --el-input-text-color: var(--text-color);
}

.header-right .el-button {
  --el-button-bg-color: var(--bg-light);
  --el-button-border-color: var(--primary-color);
  --el-button-text-color: var(--primary-color);
  --el-button-hover-bg-color: var(--primary-color);
  --el-button-hover-border-color: var(--primary-color);
  --el-button-hover-text-color: #fff;
}

.app-main {
  padding: 30px;
}

.app-main > * {
  max-width: 1200px;
  margin: 0 auto;
}
</style>