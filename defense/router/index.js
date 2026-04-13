
import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', redirect: '/defense/dashboard' },
  { path: '/defense/dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/defense/labs', component: () => import('../views/Labs.vue') },
  { path: '/defense/simulate', component: () => import('../views/Simulate.vue') },
  { path: '/defense/users', component: () => import('../views/Users.vue') },
  { path: '/defense/reports', component: () => import('../views/Reports.vue') }
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
