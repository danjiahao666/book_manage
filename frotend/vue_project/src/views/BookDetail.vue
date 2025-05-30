<template>
  <div class="book-detail-view">
    <div class="container mx-auto py-8 px-4">
      <!-- 返回按钮 -->
      <div class="mb-6">
        <el-button @click="goBack" icon="ArrowLeft">返回</el-button>
      </div>
      
      <div v-if="loading" class="flex justify-center items-center py-12">
        <el-skeleton style="width: 100%" animated :rows="10" />
      </div>
      
      <div v-else-if="book" class="bg-white rounded-lg shadow-md p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- 左侧封面 -->
          <div class="flex flex-col items-center">
            <el-image
              style="width: 240px; height: 340px"
              :src="getBookCoverUrl(book.id, book.title)"
              fit="cover"
              class="mb-4 shadow-lg rounded-md"
            >
              <template #error>
                <div class="flex items-center justify-center h-full w-full bg-gray-100 border border-gray-200 rounded">
                  <el-icon class="text-gray-400 text-4xl"><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            
            <div class="text-center mt-2">
              <el-tag v-if="book.category" size="large" class="mb-2">{{ getCategoryName(book.category) }}</el-tag>
              <p class="text-gray-500 text-sm">ISBN: {{ book.isbn || '暂无' }}</p>
            </div>
          </div>
          
          <!-- 中间书籍信息 -->
          <div class="col-span-2">
            <h1 class="text-2xl font-bold mb-2">{{ book.title }}</h1>
            
            <div class="mb-6">
              <p class="text-lg">
                <span class="font-medium">作者:</span> {{ book.author }}
              </p>
              <p class="text-lg">
                <span class="font-medium">出版社:</span> {{ book.publisher }}
              </p>
              <p class="text-lg">
                <span class="font-medium">出版日期:</span> {{ formatDate(book.publish_date || book.publishDate) }}
              </p>
              <p class="text-lg">
                <span class="font-medium">价格:</span> {{ formatPrice(book.price) }}
              </p>
            </div>
            
            <div class="mb-6">
              <h2 class="text-xl font-bold mb-2">图书简介</h2>
              <p class="text-gray-700">{{ book.description || '暂无简介' }}</p>
            </div>
            
            <!-- 评论区 -->
            <div class="mt-8">
              <h2 class="text-xl font-bold mb-4">读者评论 ({{ bookReviews.length }})</h2>
              
              <div v-if="reviewsLoading" class="text-center py-4">
                <el-skeleton :rows="3" animated />
              </div>
              
              <div v-else-if="bookReviews.length === 0" class="text-center text-gray-500 py-4">
                暂无评论
              </div>
              
              <div v-else class="space-y-4 mb-6">
                <div v-for="review in bookReviews" :key="review.id" class="border-b pb-4">
                  <div class="flex justify-between">
                    <div class="flex items-center">
                      <el-avatar :size="40" class="mr-3">{{ review.user?.username?.charAt(0) || getUserInitial(review) }}</el-avatar>
                      <div>
                        <p class="font-medium">{{ getUserName(review) }}</p>
                        <p class="text-xs text-gray-500">{{ formatCommentTime(review.created_at) }}</p>
                      </div>
                    </div>
                    <div>
                      <el-rate v-model="review.rating" disabled text-color="#ff9900" />
                    </div>
                  </div>
                  <p class="mt-3 text-gray-700">{{ review.content || '无评论内容' }}</p>
                </div>
              </div>
              
              <!-- 添加评论表单 -->
              <div class="bg-gray-50 rounded-lg p-4 mt-6">
                <h3 class="text-lg font-bold mb-4">添加评论</h3>
                <el-form :model="reviewForm" ref="reviewFormRef">
                  <el-form-item label="评分">
                    <el-rate v-model="reviewForm.rating" />
                  </el-form-item>
                  <el-form-item label="评论">
                    <el-input 
                      v-model="reviewForm.content" 
                      type="textarea" 
                      :rows="4" 
                      placeholder="写下您对这本书的评价..."
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitReview" :loading="submitting">提交评论</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-12">
        <el-empty description="未找到图书信息" />
        <el-button class="mt-4" @click="goBack">返回图书列表</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '../stores/bookStore'
import { useUserStore } from '../stores/userStore'
import { ArrowLeft, Star, Picture } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus'
import { mediaUtils } from '../services/api'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const userStore = useUserStore()

// 状态变量
const loading = ref(true)
const book = ref(null)
const bookReviews = ref([])
const reviewsLoading = ref(false)
const submitting = ref(false)

// 评论表单
const reviewForm = reactive({
  rating: 5,
  content: '',
  book: null
})

// 表单引用
const reviewFormRef = ref(null)

// 监听路由ID变化
watch(() => route.query.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    console.log(`路由ID变化: ${oldId} -> ${newId}，重新加载图书`)
    resetBookDetail()
    loadBookDetail(Number(newId))
  }
}, { immediate: false })

// 重置图书详情状态
const resetBookDetail = () => {
  console.log('重置图书详情状态')
  book.value = null
  bookReviews.value = []
  reviewForm.content = ''
  reviewForm.rating = 5
  reviewForm.book = null
  
  // 如果有当前图书ID，清除其评论缓存
  const currentBookId = Number(route.query.id)
  if (currentBookId) {
    bookStore.clearBookReviews(currentBookId)
  }
}

// 加载图书详情
const loadBookDetail = async (bookId) => {
  if (!bookId) {
    ElMessage.error('未指定图书ID')
    return
  }
  
  // 先清除指定图书的评论缓存，确保加载最新评论
  bookStore.clearBookReviews(bookId)
  
  loading.value = true
  try {
    console.log(`正在加载图书ID: ${bookId} 的详细信息`)
    
    // 确保图书数据已加载
    if (bookStore.books.length === 0) {
      await bookStore.fetchBooks()
    }
    
    // 查找图书
    const foundBook = bookStore.books.find(b => b.id === bookId)
    
    if (foundBook) {
      book.value = foundBook
      console.log('成功加载图书详情:', book.value.title)
      reviewForm.book = bookId
      
      // 加载评论
      await loadBookReviews(bookId)
    } else {
      console.error('未找到指定ID的图书:', bookId)
      ElMessage.error('未找到指定的图书')
    }
  } catch (error) {
    console.error('加载图书详情失败:', error)
    ElMessage.error('加载图书详情失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 初始化页面
onMounted(async () => {
  // 获取URL中的图书ID
  const bookId = Number(route.query.id)
  await loadBookDetail(bookId)
})

// 组件销毁前清理
onBeforeUnmount(() => {
  resetBookDetail()
})

// 加载图书评论
const loadBookReviews = async (bookId) => {
  reviewsLoading.value = true
  try {
    bookReviews.value = await bookStore.fetchBookReviews(bookId)
    console.log(`成功加载 ${bookReviews.value.length} 条评论`)
  } catch (error) {
    console.error('加载评论失败:', error)
    ElMessage.warning('评论加载失败，请稍后再试')
    bookReviews.value = []
  } finally {
    reviewsLoading.value = false
  }
}

// 提交评论
const submitReview = async () => {
  if (!reviewForm.content) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  if (!reviewForm.book) {
    ElMessage.error('未找到图书ID')
    return
  }
  
  submitting.value = true
  try {
    // 检查用户是否登录
    if (!userStore.isAuthenticated) {
      ElMessage.warning('请先登录后再评论')
      router.push({ path: '/login', query: { redirect: route.fullPath } })
      return
    }
    
    // 保存评论内容副本用于后续处理
    const reviewContent = reviewForm.content
    const reviewRating = reviewForm.rating
    
    // 添加评论前先检查是否已有评论
    const hasExistingReview = bookReviews.value.some(
      review => review.user?.id === userStore.currentUser?.id
    )
    
    const response = await bookStore.addReview({
      book: reviewForm.book,
      rating: reviewRating,
      content: reviewContent
    })
  
    // 重置表单
    reviewForm.content = ''
    reviewForm.rating = 5
    
    // 重新加载评论
    await loadBookReviews(book.value.id)
  } catch (error) {
    console.error('提交评论失败:', error)
    // 错误处理在store中已经完成
  } finally {
    submitting.value = false
  }
}

// 获取图书封面URL - 使用统一的工具函数
const getBookCoverUrl = (id, title) => {
  return mediaUtils.getBookCoverUrl(id, title)
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

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知';
  
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

// 格式化评论时间
const formatCommentTime = (dateString) => {
  if (!dateString) return '';
  
  try {
    const commentDate = new Date(dateString);
    if (isNaN(commentDate.getTime())) return dateString;
    
    const now = new Date();
    const diffMs = now - commentDate;
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffSeconds < 60) {
      return '刚刚';
    } else if (diffMinutes < 60) {
      return `${diffMinutes}分钟前`;
    } else if (diffHours < 24) {
      return `${diffHours}小时前`;
    } else if (diffDays < 30) {
      return `${diffDays}天前`;
    } else {
      return commentDate.toLocaleDateString('zh-CN');
    }
  } catch (error) {
    console.error('评论时间格式化错误:', error);
    return dateString;
  }
}

// 获取用户姓名
const getUserName = (review) => {
  if (review.user && review.user.username) {
    return review.user.username;
  }
  
  return '匿名用户';
}

// 获取用户头像显示的字母
const getUserInitial = (review) => {
  if (review.user && review.user.username) {
    return review.user.username.charAt(0).toUpperCase();
  }
  
  return 'U';
}

// 返回上一页
const goBack = () => {
  router.back();
}

// 组件名称，用于keep-alive排除
defineOptions({
  name: 'BookDetail'
})
</script>

<style scoped>
.book-detail-view {
  min-height: calc(100vh - 120px);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style> 