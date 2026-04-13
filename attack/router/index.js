
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/attack/home' },
  { path: '/attack/home', component: () => import('../views/Home.vue') },
  { path: '/attack/dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/attack/scenarios', component: () => import('../views/Scenarios.vue') },
  { path: '/attack/simulate', component: () => import('../views/Simulate.vue') },
  { path: '/attack/reports', component: () => import('../views/Reports.vue') },
  { path: '/attack/users', component: () => import('../views/Users.vue') },
  // 防御端路由
  { path: '/defense/dashboard', component: () => import('../../defense/views/Dashboard.vue') },
  { path: '/defense/labs', component: () => import('../../defense/views/Labs.vue') },
  { path: '/defense/simulate', component: () => import('../../defense/views/Simulate.vue') },
  { path: '/defense/users', component: () => import('../../defense/views/Users.vue') },
  { path: '/defense/reports', component: () => import('../../defense/views/Reports.vue') }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 移除认证检查
router.beforeEach((to, from, next) => {
  next()
})

export default router

