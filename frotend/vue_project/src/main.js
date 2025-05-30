import './assets/main.css'

// 引入自定义主题过渡动画CSS
import './assets/theme-transition.css'
// 引入暗黑模式样式覆盖
import './assets/dark-mode.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
// 引入Element Plus暗黑模式CSS变量
import 'element-plus/theme-chalk/dark/css-vars.css'
import App from './App.vue'

// 导入路由配置
import routes from './router'

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 创建Pinia实例
const pinia = createPinia()

// 创建Vue应用
const app = createApp(App)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 应用插件
app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 路由前置守卫 - 注意：必须在Pinia和router配置之后添加
// 这部分逻辑也在App.vue中实现了，这里作为双重保障
import { useUserStore } from './stores/userStore'
router.beforeEach((to, from, next) => {
  // 如果页面需要登录权限
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    // 如果没有登录，重定向到登录页
    if (!userStore.isAuthenticated) {
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else {
      next()
    }
  } else {
    next()
  }
})

// 挂载应用
app.mount('#app')
