<template>
  <div class="about-view">
    <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">关于图书推荐系统</h1>
    
      <div class="mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-3">系统简介</h2>
        <p class="text-gray-700 mb-4">
          本系统是一个基于Django和Vue.js开发的智能图书推荐系统，旨在为用户提供个性化的图书推荐服务。
          系统包含图书管理、分类管理、用户管理和评论管理等核心功能，支持图书搜索、分类浏览和评分评论等交互功能。
        </p>
        <p class="text-gray-700">
          通过本系统，用户可以方便地浏览图书信息，发表评论和评分，系统会根据用户的喜好和历史行为，推荐可能感兴趣的图书。
        </p>
      </div>
      
      <div class="mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-3">技术架构</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold mb-2">前端技术栈</h3>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li>Vue 3 - 渐进式JavaScript框架</li>
              <li>Vue Router - 官方路由管理器</li>
              <li>Pinia - 状态管理库</li>
              <li>Element Plus - UI组件库</li>
              <li>Axios - HTTP客户端</li>
              <li>Tailwind CSS - 实用工具优先的CSS框架</li>
              <li>ECharts - 数据可视化图表库</li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold mb-2">后端技术栈</h3>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li>Django - Python Web框架</li>
              <li>Django REST Framework - RESTful API工具包</li>
              <li>MySQL - 关系型数据库</li>
              <li>JWT - 用户认证</li>
              <li>Swagger/OpenAPI - API文档</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-3">系统功能</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <el-card shadow="hover" class="h-full">
            <template #header>
              <div class="flex items-center">
                <el-icon class="text-primary mr-2"><Document /></el-icon>
                <span class="font-bold">图书管理</span>
              </div>
            </template>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li>图书浏览与搜索</li>
              <li>图书详情查看</li>
              <li>添加、编辑、删除图书</li>
              <li>图书分类管理</li>
            </ul>
          </el-card>
          
          <el-card shadow="hover" class="h-full">
            <template #header>
              <div class="flex items-center">
                <el-icon class="text-primary mr-2"><User /></el-icon>
                <span class="font-bold">用户管理</span>
              </div>
            </template>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li>用户注册与登录</li>
              <li>个人信息管理</li>
              <li>用户权限控制</li>
              <li>密码修改与重置</li>
            </ul>
          </el-card>
          
          <el-card shadow="hover" class="h-full">
            <template #header>
              <div class="flex items-center">
                <el-icon class="text-primary mr-2"><ChatLineRound /></el-icon>
                <span class="font-bold">评论与推荐</span>
              </div>
            </template>
            <ul class="list-disc list-inside space-y-1 text-gray-700">
              <li>图书评分与评论</li>
              <li>个性化图书推荐</li>
              <li>热门图书推荐</li>
              <li>数据统计与分析</li>
            </ul>
          </el-card>
        </div>
      </div>
      
      <div class="mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-3">开发团队</h2>
        <p class="text-gray-700 mb-4">
          本系统由22数据2班：淡嘉浩、韦荣健、韦贻元打造，致力于打造高效、易用、智能的图书推荐平台。
        </p>
      </div>
      
      <div>
        <h2 class="text-xl font-bold text-gray-800 mb-3">联系我们</h2>
        <p class="text-gray-700 mb-2">
          如有任何问题或建议，请通过以下方式联系我们：
        </p>
        <ul class="list-disc list-inside space-y-1 text-gray-700">
          <li>邮箱：390482691@qq.com</li>
          <li>学号：2230823078、2230823095、2230823086</li>
          <li>地址：贺州学院西校区</li>
        </ul>
      </div>
    </div>
    
    <!-- API信息卡片 -->
    <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
      <h2 class="text-xl font-bold text-gray-800 mb-3">API文档</h2>
      <p class="text-gray-700 mb-4">
        本系统提供了RESTful API接口，方便开发者进行集成和扩展。完整的API文档可通过以下链接访问：
      </p>
        
      <div class="flex space-x-4 mt-6">
        <el-button type="primary" @click="openApiDocs('swagger')">
          <el-icon class="mr-2"><Document /></el-icon>
          Swagger文档
        </el-button>
        
        <el-button @click="openApiDocs('redoc')">
          <el-icon class="mr-2"><Document /></el-icon>
          ReDoc文档
        </el-button>
      </div>
    </div>
    
    <!-- 版本信息 -->
    <div class="bg-white p-6 rounded-lg shadow-sm">
      <div class="flex justify-between items-center">
    <div>
          <h2 class="text-xl font-bold text-gray-800 mb-1">系统版本</h2>
          <p class="text-gray-600">当前版本：v1.0.0</p>
        </div>
        
        <div>
          <p class="text-gray-600">最后更新：{{ new Date().toLocaleDateString() }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Document, User, ChatLineRound } from '@element-plus/icons-vue'

// 打开API文档
const openApiDocs = (type) => {
  const baseUrl = 'http://localhost:8000/'
  const url = type === 'swagger' ? `${baseUrl}swagger/` : `${baseUrl}redoc/`
  window.open(url, '_blank')
}
</script>

<style scoped>
.about-view {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.text-primary {
  color: #64B5F6;
}

:deep(.el-card__header) {
  padding: 12px 16px;
  background-color: #f8f9fa;
}
</style> 