import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import '@/../shared/styles/themes.css'
import { initMockData } from '@/../shared/mock/data.js'
import App from './App.vue'
import router from './router'

// 全局API配置
window.__API_BASE_URL__ = 'http://localhost:4000/api'

// 初始化Mock数据
initMockData()

// 设置攻击端主题
document.documentElement.setAttribute('data-theme', 'attack')

const app = createApp(App)
const pinia = createPinia()

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.mount('#app')



