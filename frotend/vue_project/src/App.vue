<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElIcon, ElMessage } from 'element-plus'
import { Document, MoonNight, Sunny, User } from '@element-plus/icons-vue'
// 引入暗黑模式相关函数
import { useDark, useToggle } from '@vueuse/core'
// 引入用户状态管理
import { useUserStore } from './stores/userStore'

// 初始化暗黑模式
const isDark = useDark()
const toggleDark = useToggle(isDark)

// 获取路由
const router = useRouter()
const route = useRoute()

// 获取用户状态
const userStore = useUserStore()

// 获取所有可见的路由信息
const visibleRoutes = computed(() => {
  return router.options.routes.filter(route => 
    route.path !== '/' && route.meta && route.meta.title &&
    // 过滤登录和注册页面，不在导航栏显示
    route.path !== '/login' && route.path !== '/register' &&
    // 过滤设置了hideInMenu的路由
    !route.meta.hideInMenu
  )
})

// 当前活动的导航项
const activeIndex = computed(() => route.path)

// 用户下拉菜单显示控制
const userDropdownVisible = ref(false)

// 计算用户是否已登录
const isLoggedIn = computed(() => userStore.isAuthenticated)

// 获取用户名
const username = computed(() => userStore.username || '未登录')

// 退出登录
const handleLogout = () => {
  userStore.logout()
  ElMessage.success('退出登录成功')
  // 如果当前页面需要认证，则重定向到登录页
  if (route.meta.requiresAuth) {
    router.push('/login')
  }
}

// 应用初始化
onMounted(async () => {
  console.log('应用初始化开始');
  document.title = '图书管理系统'
  
  // 初始化用户状态
  if (userStore.token) {
    console.log('发现Token，尝试初始化用户状态:', userStore.token);
    try {
      const user = await userStore.initialize();
      if (user) {
        console.log('用户初始化成功:', user);
        ElMessage.success(`欢迎回来，${user.username || '用户'}！`);
      } else {
        console.log('用户初始化失败，没有返回用户信息');
      }
    } catch (error) {
      console.error('用户初始化出错:', error);
      ElMessage.error('登录状态已失效，请重新登录');
    }
  } else {
    console.log('没有找到Token，跳过用户初始化');
  }
  
  console.log('应用初始化完成');
})

// 监听路由变化，处理需要认证的页面
watch(
  () => route.path,
  async (newPath) => {
    const targetRoute = router.options.routes.find(r => r.path === newPath)
    if (targetRoute?.meta?.requiresAuth && !isLoggedIn.value) {
      ElMessage.warning('请先登录')
      router.push('/login')
    }
    
    // 当路由切换到图书列表页面时，确保获取最新数据
    if (newPath === '/books') {
      console.log('进入图书列表页面，准备刷新数据')
      // 图书数据会在组件内部刷新，这里不需要额外操作
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="book-management-app min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-md">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center" style="max-width: 1100px;">
        <div class="flex items-center">
          <el-icon class="text-primary text-3xl mr-2"><Document /></el-icon>
          <h1 class="text-2xl font-bold text-gray-800">图书管理系统</h1>
        </div>
        
        <!-- 右侧导航菜单 -->
        <div class="flex items-center">
          <el-menu
            mode="horizontal"
            :default-active="activeIndex"
            router
            class="border-0"
          >
            <el-menu-item 
              v-for="route in visibleRoutes" 
              :key="route.path" 
              :index="route.path"
            >
              {{ route.meta.title }}
            </el-menu-item>
          </el-menu>
          
          <!-- 用户菜单 -->
          <el-dropdown class="ml-4" @command="(command) => command === 'logout' ? handleLogout() : router.push(command)">
            <div class="user-dropdown-link">
              <el-icon class="user-icon"><User /></el-icon>
              <span class="ml-1">{{ username }}</span>
              <el-icon class="ml-1"><el-icon-arrow-down /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <template v-if="isLoggedIn">
                  <el-dropdown-item command="/profile">个人信息</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </template>
                <template v-else>
                  <el-dropdown-item command="/login">登录</el-dropdown-item>
                  <el-dropdown-item command="/register">注册</el-dropdown-item>
                </template>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <!-- 主题切换按钮 -->
          <el-tooltip
            :content="isDark ? '切换到亮色模式' : '切换到暗黑模式'"
            placement="bottom"
          >
            <el-button
              circle
              class="ml-4 theme-toggle-btn"
              @click="toggleDark()"
            >
              <el-icon class="theme-icon">
                <MoonNight v-if="!isDark" />
                <Sunny v-else />
              </el-icon>
            </el-button>
          </el-tooltip>
        </div>
    </div>
  </header>

    <!-- 主内容区域 -->
    <main class="py-6">
      <div style="width: 1200px; max-width: 100%; margin: 0 auto; padding: 0 15px; box-sizing: border-box;">
        <!-- 路由视图 - 动画过渡效果 -->
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <keep-alive :exclude="['BookDetail']">
              <component :is="Component" :key="route.fullPath" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
  </main>
    
    <!-- 底部版权信息 -->
    <footer class="bg-white border-t mt-auto py-4">
      <div class="container mx-auto px-4 text-center text-gray-600" style="max-width: 1100px;">
        <p>© 2025 图书管理系统 - 基于 Vue 3 与 ElementPlus 开发</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* 导入TailwindCSS */
@import './assets/main.css';

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 全局样式 */
body {
  font-family: 'Inter', system-ui, sans-serif;
  color: #333;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

.book-management-app {
    display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

/* 修复Element Plus样式 */
.el-menu.el-menu--horizontal {
  border-bottom: none;
}

.el-menu-item.is-active {
  color: #64B5F6 !important;
}

.text-primary {
  color: #64B5F6;
  }

.el-menu-item:hover {
  color: #42A5F5 !important;
}

/* 用户下拉菜单样式 */
.user-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
  color: #606266;
}

.user-dropdown-link:hover {
  background-color: #f5f7fa;
}

.user-icon {
  font-size: 18px;
  color: #64B5F6;
}

/* 暗黑模式样式覆盖 */
html.dark {
  --el-bg-color: #1a1a1a;
}

html.dark .book-management-app {
  background-color: #121212;
  }

html.dark .bg-white {
  background-color: #1f1f1f !important;
}

html.dark .text-gray-800 {
  color: #e0e0e0 !important;
}

html.dark .text-gray-600 {
  color: #bdbdbd !important;
}

html.dark .border-t {
  border-color: #333 !important;
}

html.dark .user-dropdown-link:hover {
  background-color: #2c2c2c;
}

/* 主题切换按钮样式 */
.theme-toggle-btn {
  transition: transform 0.3s ease;
}

.theme-toggle-btn:hover {
  transform: rotate(15deg);
}

.theme-icon {
  transition: all 0.3s ease;
  }

html.dark .theme-icon {
  color: #FFD54F;
}
</style>
