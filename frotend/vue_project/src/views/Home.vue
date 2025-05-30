<template>
  <div class="home-view">
    <!-- 欢迎语和统计数据 -->
    <div class="mb-8 animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">欢迎使用图书管理系统</h1>
      <p class="text-lg text-gray-600">一个简洁、高效的图书管理解决方案</p>
      
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><DocumentCopy /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">图书总数</h3>
              <p class="text-2xl font-bold">{{ bookStore.getTotalBooks }}</p>
            </div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Files /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">分类总数</h3>
              <p class="text-2xl font-bold">{{ bookStore.getAllCategories.length }}</p>
            </div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Star /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">热门分类</h3>
              <p class="text-2xl font-bold">{{ mostPopularCategory.name }}</p>
            </div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Calendar /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">今天日期</h3>
              <p class="text-xl font-bold">{{ formatDate(new Date()) }}</p>
            </div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Timer /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">当前时间</h3>
              <p class="text-xl font-bold">{{ currentTime }}</p>
            </div>
          </div>
        </el-card>
        
        <!-- 随机推荐书籍 -->
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300 book-recommend-card" 
                @click="randomBook.id && viewBookDetails(randomBook.id)" 
                :class="{'cursor-pointer hover:bg-blue-50': randomBook.id}">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Promotion /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">今日推荐</h3>
              <p class="text-xl font-bold text-truncate" style="max-width: 180px;">{{ randomBook.title || '暂无图书' }}</p>
              <p v-if="randomBook.id" class="text-xs text-blue-500">点击查看详情</p>
            </div>
          </div>
        </el-card>
        
        <!-- 藏书总价值 -->
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Wallet /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">藏书价值</h3>
              <p class="text-xl font-bold">¥{{ totalBookValue.toFixed(2) }}</p>
            </div>
          </div>
        </el-card>
        
        <!-- 阅读时间预估 -->
        <el-card shadow="hover" class="hover:shadow-lg transition-shadow duration-300" @click="showReadingTimeInfo">
          <div class="flex items-center">
            <el-icon class="text-primary text-3xl mr-2"><Clock /></el-icon>
            <div class="ml-4">
              <h3 class="text-lg font-medium mb-1">阅读时间</h3>
              <p class="text-xl font-bold">{{ estimatedReadingTime }}</p>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 最新图书 -->
    <div class="mb-8 animate-fade-in">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold text-gray-900">最新图书</h2>
        <router-link to="/books" class="btn btn-outline flex items-center">
          <span>查看全部</span>
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </router-link>
      </div>
      
      <el-carousel :interval="4000" type="card" height="360px">
        <el-carousel-item v-for="book in recentBooks" :key="book.id">
          <div class="card h-full flex flex-col justify-between p-6 bg-white rounded-lg shadow-sm">
            <div class="flex">
              <div class="mr-4 flex-shrink-0">
                <el-image
                  style="width: 120px; height: 170px"
                  :src="getBookCoverUrl(book.id, book.title)"
                  fit="cover"
                  class="shadow-md rounded"
                >
                  <template #error>
                    <div class="flex items-center justify-center h-full w-full bg-gray-100 border border-gray-200 rounded">
                      <el-icon class="text-gray-400 text-3xl"><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-bold mb-2">{{ book.title }}</h3>
                <div class="mb-2">
                  <el-tag size="small" class="mr-2">{{ getCategoryName(book.category) }}</el-tag>
                  <span class="text-gray-500 text-sm">{{ formatBookDate(book.publish_date || book.publishDate) }}</span>
                </div>
                <p class="text-gray-700 mb-4 line-clamp-3">{{ book.description }}</p>
                <p class="text-gray-600 mb-1">
                  <el-icon class="mr-1"><User /></el-icon>
                  作者: {{ book.author }}
                </p>
                <p class="text-gray-600 mb-1">
                  <el-icon class="mr-1"><OfficeBuilding /></el-icon>
                  出版社: {{ book.publisher }}
                </p>
              </div>
            </div>
            <div class="flex justify-between items-center mt-4">
              <span class="text-lg font-bold text-primary">{{ formatPrice(book.price) }}</span>
              <el-button type="primary" size="small" @click="viewBookDetails(book.id)">
                查看详情
              </el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
    
    <!-- 图书分类 -->
    <div class="mb-8 animate-fade-in">
      <h2 class="text-2xl font-bold text-gray-900 mb-4">图书分类</h2>
      
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div 
          v-for="category in bookStore.getAllCategories" 
          :key="category.id" 
          class="card flex flex-col items-center justify-center p-4 bg-white rounded-lg shadow-sm cursor-pointer hover:shadow transition-shadow duration-300"
          @click="navigateToCategory(category.name)"
        >
          <el-icon class="text-primary text-3xl mb-2"><Folder /></el-icon>
          <h4 class="text-lg font-medium mb-1">{{ category.name }}</h4>
          <p class="text-gray-500">{{ category.count }} 本</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBookStore } from '../stores/bookStore'
import {
  Calendar,
  Star,
  ArrowRight,
  User,
  Folder,
  DocumentCopy,
  Files,
  OfficeBuilding,
  Picture,
  Timer,
  Promotion,
  Wallet,
  Clock
} from '@element-plus/icons-vue'
import { ElMessageBox, ElLoading } from 'element-plus'
import { mediaUtils } from '../services/api'

// 路由
const router = useRouter()

// 获取书籍存储
const bookStore = useBookStore()

// 加载状态
const loading = ref(false)

// 初始化数据
onMounted(async () => {
  loading.value = true
  try {
    console.log('首页加载中，准备获取数据...')
    bookStore.clearData() // 清除现有数据
    await bookStore.initialize() // 从API加载数据
    
    // 更新分类图书数量
    await bookStore.updateCategoriesBookCount()
    
    console.log(`成功加载 ${bookStore.books.length} 本图书和 ${bookStore.categories.length} 个分类`)
    
    // 检查数据有效性
    if (bookStore.books.length === 0) {
      console.warn('未能获取到图书数据')
    }
    
    updateTime() // 更新当前时间
    timeInterval = setInterval(updateTime, 1000) // 启动时间更新定时器
  } catch (error) {
    console.error('初始化数据失败:', error)
  } finally {
    loading.value = false
  }
})

// 计算最新图书（按id倒序，取前5本）
const recentBooks = computed(() => {
  // 确保books数据有效
  if (!bookStore.books || !bookStore.books.length) {
    return [];
  }
  
  try {
    return [...bookStore.books]
      .filter(book => book && book.id) // 过滤无效的书籍数据
      .sort((a, b) => b.id - a.id)
      .slice(0, 5)
      .map(book => {
        // 确保每本书都有基本属性
        return {
          ...book,
          title: book.title || '未知书名',
          author: book.author || '未知作者',
          publisher: book.publisher || '未知出版社',
          description: book.description || '暂无简介',
          price: book.price || 0
        };
      });
  } catch (error) {
    console.error('处理最新图书数据时出错:', error);
    return [];
  }
})

// 计算最流行的分类（书籍数量最多的）
const mostPopularCategory = computed(() => {
  if (bookStore.categories.length === 0) {
    return { name: '加载中...', count: 0 }
  }
  return [...bookStore.categories]
    .sort((a, b) => b.count - a.count)[0]
})

// 格式化日期
const formatDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 查看图书详情
const viewBookDetails = (bookId) => {
  router.push({
    path: '/book-detail',
    query: { id: bookId }
  })
}

// 导航到分类
const navigateToCategory = (categoryName) => {
  // 查找分类ID
  const category = bookStore.categories.find(c => c.name === categoryName);
  
  if (category) {
    router.push({
      path: '/categories',
      query: { category_id: category.id }
    });
  } else {
    router.push({
      path: '/categories',
      query: { name: categoryName }
    });
  }
}

// 获取图书封面URL - 使用统一的工具函数
const getBookCoverUrl = (id, title) => {
  return mediaUtils.getBookCoverUrl(id, title)
}

// 获取当前时间
const currentTime = ref('')
const updateTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${hours}:${minutes}:${seconds}`
}

// 设置定时器更新时间
let timer = null
onMounted(() => {
  updateTime() // 立即更新一次
  timer = setInterval(updateTime, 1000) // 每秒更新一次
})

// 组件卸载时清除定时器
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})

// 随机推荐一本书
const randomBook = computed(() => {
  if (bookStore.books.length === 0) {
    return { title: '加载中...' }
  }
  const randomIndex = Math.floor(Math.random() * bookStore.books.length)
  const book = bookStore.books[randomIndex]
  
  // 确保book是一个有效对象
  if (!book || typeof book !== 'object') {
    console.warn('随机图书数据无效:', book)
    return { title: '数据错误' }
  }
  
  return book
})

// 计算藏书总价值
const totalBookValue = computed(() => {
  return bookStore.books.reduce((sum, book) => {
    // 确保price是有效数字
    const price = parseFloat(book.price)
    return sum + (isNaN(price) ? 0 : price)
  }, 0)
})

// 计算所有藏书的估计阅读时间（假设平均每本书需要8小时）
const estimatedReadingTime = computed(() => {
  const totalHours = bookStore.books.length * 8
  if (totalHours < 24) {
    return `${totalHours}小时`
  } else {
  const days = Math.floor(totalHours / 24)
    const hours = totalHours % 24
    return `${days}天${hours}小时`
  }
})

// 显示阅读时间详情
const showReadingTimeInfo = () => {
  ElMessageBox.alert(
    `<p>总计${bookStore.books.length}本书</p>
     <p>按照每本书平均阅读时间8小时计算</p>
     <p>总阅读时间：${Math.floor(bookStore.books.length * 8)}小时</p>
     <p>如果每天阅读4小时，需要${Math.ceil(bookStore.books.length * 8 / 4)}天可以读完</p>`,
    '阅读时间估算',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确定'
    }
  )
}

// 获取分类名称
const getCategoryName = (category) => {
  try {
    // 如果category是字符串，直接返回
    if (typeof category === 'string') {
      return category;
    }
    
    // 如果category是对象，返回name属性
    if (typeof category === 'object' && category !== null) {
      if (category.name) {
        return category.name;
      }
    }
    
    // 默认返回
    return '未分类';
  } catch (error) {
    console.error('获取分类名称错误:', error);
    return '未分类';
  }
}

// 格式化价格
const formatPrice = (price) => {
  if (price === undefined || price === null) return '暂无价格';
  
  try {
    const parsedPrice = parseFloat(price);
    if (isNaN(parsedPrice)) return '价格错误';
    return `¥${parsedPrice.toFixed(2)}`;
  } catch (error) {
    console.error('价格格式化错误:', error, price);
    return '价格错误';
  }
}

// 格式化图书日期
const formatBookDate = (dateString) => {
  if (!dateString) return '未知日期';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  } catch (error) {
    console.error('日期格式化错误:', error);
    return dateString;
  }
}
</script>

<style scoped>
/* 自定义样式 */
.home-view {
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

/* 改进Element Plus组件样式 */
.el-card {
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.book-recommend-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.el-carousel__item {
  border-radius: 0.5rem;
  overflow: hidden;
}

:deep(.el-carousel) {
  width: 100%;
}

:deep(.el-carousel__container) {
  width: 100%;
}

/* 主题色应用 */
:deep(.text-primary) {
  color: #64B5F6;
}

:deep(.el-button--primary) {
  background-color: #64B5F6;
  border-color: #64B5F6;
}

:deep(.el-button--primary:hover) {
  background-color: #42A5F5;
  border-color: #42A5F5;
}

/* 暗黑模式文本适配 */
html.dark .text-gray-900 {
  color: #ffffff !important;
}

html.dark .text-gray-700,
html.dark .text-gray-600 {
  color: #e0e0e0 !important;
}

html.dark .text-gray-500 {
  color: #bbbbbb !important;
}

/* 轮播图暗黑模式适配 */
html.dark .card {
  background-color: #2d2d2d !important;
  border: 1px solid #444444;
}

html.dark .el-carousel__item .card h3 {
  color: #ffffff !important;
}

html.dark .el-carousel__item .card p {
  color: #e0e0e0 !important;
}

html.dark .el-tag {
  background-color: #444444;
  border-color: #555555;
}

html.dark .text-primary {
  color: #64B5F6 !important;
}

/* 链接和按钮在暗黑模式下的样式 */
html.dark .btn {
  color: #64B5F6 !important;
}

html.dark .btn:hover {
  color: #42A5F5 !important;
}

/* 查看详情链接 */
html.dark .text-blue-500 {
  color: #64B5F6 !important;
}

/* 首页标题和副标题 */
html.dark h1.text-gray-900,
html.dark h2.text-gray-900 {
  color: #ffffff !important;
}

/* 分类区域暗黑模式适配 */
html.dark .card h4 {
  color: #ffffff !important;
}

html.dark .card p {
  color: #bbbbbb !important;
}

/* 分类卡片样式 */
html.dark .grid-cols-6 .card {
  background-color: #2d2d2d !important;
  border: 1px solid #3a3a3a;
  transition: all 0.3s ease;
}

html.dark .grid-cols-6 .card:hover {
  background-color: #333333 !important;
  transform: translateY(-2px);
  border-color: #4a4a4a;
}

/* 分类图标颜色 */
html.dark .card .text-primary {
  color: #64B5F6 !important;
}
</style> 
 