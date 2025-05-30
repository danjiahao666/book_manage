<template>
  <div class="books-view">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 mb-1">图书列表</h1>
        <p class="text-gray-600">共 {{ bookStore.getTotalBooks }} 本图书</p>
      </div>
      
      <div class="flex space-x-2">
        <el-input 
          v-model="searchText" 
          placeholder="搜索图书" 
          prefix-icon="Search"
          class="w-64" 
          @keyup.enter="handleSearch"
        />
      </div>
    </div>
    
    <!-- 筛选选项 -->
    <div class="bg-white p-4 rounded-lg shadow-sm mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <span class="text-gray-700 font-medium">筛选：</span>
        
        <el-select v-model="filterCategory" placeholder="选择分类" clearable>
          <el-option label="全部分类" value="" />
          <el-option 
            v-for="category in bookStore.getAllCategories" 
            :key="category.id" 
            :label="category.name"
            :value="category.id"
          />
        </el-select>
        
        <el-select v-model="sortBy" placeholder="排序方式">
          <el-option label="默认排序" value="id" />
          <el-option label="书名 (A-Z)" value="titleAsc" />
          <el-option label="书名 (Z-A)" value="titleDesc" />
          <el-option label="价格 (低-高)" value="priceAsc" />
          <el-option label="价格 (高-低)" value="priceDesc" />
          <el-option label="出版日期 (新-旧)" value="dateDesc" />
          <el-option label="出版日期 (旧-新)" value="dateAsc" />
        </el-select>
        
        <el-button 
          plain 
          class="ml-auto" 
          @click="resetFilters"
        >
          重置筛选
        </el-button>
      </div>
    </div>
    
    <!-- 图书表格 -->
    <el-table
      :data="paginatedBooks"
      border
      stripe
      style="width: 100%"
      class="rounded-lg overflow-hidden"
      v-loading="bookStore.loading"
      row-key="id"
      @row-click="viewBook"
    >
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="封面" width="100">
        <template #default="{ row }">
          <div class="flex items-center justify-center">
            <el-image
              style="width: 70px; height: 100px"
              :src="getBookCoverUrl(row.id, row.title)"
              :preview-src-list="[getBookCoverUrl(row.id, row.title)]"
              fit="cover"
              lazy
              :z-index="10"
              @error="handleImageError"
            >
              <template #error>
                <div class="flex items-center justify-center h-full w-full bg-gray-100">
                  <div class="text-center">
                  <el-icon class="text-gray-400"><Picture /></el-icon>
                    <div class="text-xs text-gray-500 mt-1">图片加载失败</div>
                  </div>
                </div>
              </template>
            </el-image>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="title" label="书名" min-width="180" sortable />
      <el-table-column prop="author" label="作者" min-width="120" sortable />
      <el-table-column label="分类" min-width="120">
        <template #default="{ row }">
          <el-tag size="small">{{ getCategoryName(row.category) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="publisher" label="出版社" min-width="150" />
      <el-table-column prop="publish_date" label="出版日期" width="120" sortable>
        <template #default="{ row }">
          {{ formatDate(row.publish_date || row.publishDate) }}
        </template>
      </el-table-column>
      <el-table-column prop="price" label="价格" width="100" sortable>
        <template #default="{ row }">
          <span class="font-medium" v-if="row.price !== undefined && row.price !== null">
            ¥{{ parseFloat(row.price).toFixed(2) }}
          </span>
          <span class="text-gray-400" v-else>暂无价格</span>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="flex justify-center mt-6">
      <el-pagination
        v-model="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        background
        layout="total, sizes, prev, pager, next"
        :total="filteredBooks.length"
      />
    </div>
    
    <!-- 图书详情对话框 -->
    <el-dialog
      v-model="showViewDialog"
      :title="selectedBook ? selectedBook.title : '图书详情'"
      width="700px"
      @close="handleDialogClose"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      :show-close="true"
      :append-to-body="true"
      destroy-on-close
      v-if="selectedBook"
    >
      <div v-loading="reviewsLoading">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div class="flex flex-col items-center mb-6">
            <el-image
              style="width: 150px; height: 210px"
              :src="getBookCoverUrl(selectedBook.id, selectedBook.title)"
              fit="cover"
              class="mb-3 shadow-md rounded"
            >
              <template #error>
                <div class="flex items-center justify-center h-full w-full bg-gray-100 border border-gray-200 rounded">
                  <el-icon class="text-gray-400 text-3xl"><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            <span class="text-sm text-gray-500">ISBN: {{ selectedBook.isbn }}</span>
          </div>
          
          <div class="mb-4">
            <h3 class="text-lg font-medium mb-2">基本信息</h3>
            <p><span class="text-gray-600 mr-2">书名:</span> {{ selectedBook.title }}</p>
            <p><span class="text-gray-600 mr-2">作者:</span> {{ selectedBook.author }}</p>
            <p><span class="text-gray-600 mr-2">分类:</span> <el-tag size="small">{{ getCategoryName(selectedBook.category) }}</el-tag></p>
            <p><span class="text-gray-600 mr-2">价格:</span> {{ formatPrice(selectedBook.price) }}</p>
          </div>
          
          <div>
            <h3 class="text-lg font-medium mb-2">出版信息</h3>
            <p><span class="text-gray-600 mr-2">出版社:</span> {{ selectedBook.publisher }}</p>
            <p><span class="text-gray-600 mr-2">出版日期:</span> {{ formatDate(selectedBook.publish_date || selectedBook.publishDate) }}</p>
          </div>
        </div>
        
        <div>
          <h3 class="text-lg font-medium mb-2">图书简介</h3>
          <p class="text-gray-700">{{ selectedBook.description }}</p>
            
            <!-- 显示图书评论 -->
            <div class="mt-6">
              <h3 class="text-lg font-medium mb-2">读者评论 ({{ bookReviews.length }})</h3>
              
              <div v-if="bookReviews.length === 0" class="text-center text-gray-500 py-4">
                暂无评论
              </div>
              
              <div v-else class="space-y-4 mt-4">
                <div v-for="review in bookReviews" :key="review.id" class="border-b pb-3">
                  <div class="flex justify-between">
                    <div class="flex items-center">
                      <el-avatar :size="32" class="mr-2">{{ review.user?.username?.charAt(0) || getUserInitial(review) }}</el-avatar>
                      <div>
                        <p class="font-medium">{{ getUserName(review) }}</p>
                        <p class="text-xs text-gray-500">{{ formatCommentTime(review.created_at) }}</p>
                      </div>
                    </div>
                    <div>
                      <el-rate v-model="review.rating" disabled text-color="#ff9900" />
                    </div>
                  </div>
                  <p class="mt-2">{{ review.content || '无评论内容' }}</p>
                </div>
              </div>
              
              <!-- 添加评论表单 -->
              <div class="mt-4">
                <el-form :model="reviewForm" ref="reviewFormRef">
                  <el-form-item label="评分">
                    <el-rate v-model="reviewForm.rating" />
                  </el-form-item>
                  <el-form-item label="评论">
                    <el-input 
                      v-model="reviewForm.content" 
                      type="textarea" 
                      :rows="3" 
                      placeholder="写下您对这本书的评价..."
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitReview">提交评论</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end">
          <el-button type="primary" @click="viewFullBookDetail(selectedBook.id)" class="mr-2">
            查看完整详情
          </el-button>
          <el-button @click="handleDialogClose">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '../stores/bookStore'
import { useUserStore } from '../stores/userStore'
import { Picture, Search } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus'
import { mediaUtils, reviewApi } from '../services/api'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const userStore = useUserStore()

// 表格和筛选状态
const currentPage = ref(1)
const pageSize = ref(10)
const searchText = ref('')
const filterCategory = ref('')
const sortBy = ref('id')
const loading = ref(false)

// 对话框状态
const showViewDialog = ref(false)
const selectedBook = ref(null)
const dialogLocked = ref(false)

// 评论相关
const bookReviews = ref([])
const reviewsLoading = ref(false)
const reviewForm = reactive({
  rating: 5,
  content: '',
  book: null
})

// 表单引用
const reviewFormRef = ref(null)

// 初始化
onMounted(async () => {
  loading.value = true
  try {
    console.log('图书页面加载中，强制刷新数据...')
    // 强制刷新数据，不使用缓存
    bookStore.clearData() // 清除现有数据
    const booksPromise = bookStore.fetchBooks()
    const categoriesPromise = bookStore.fetchCategories()
    
    // 并行加载数据
    await Promise.all([booksPromise, categoriesPromise])
    
    console.log(`成功加载 ${bookStore.books.length} 本图书`)
    console.log(`成功加载 ${bookStore.categories.length} 个分类`)
    
    // 检查图书数据是否有效
    if (bookStore.books.length === 0) {
      console.warn('未获取到图书数据，请检查API')
      ElMessage.warning('未获取到图书数据，请检查网络连接')
    }
    
    // 检查是否有查询参数id，如果有，打开图书详情对话框
    const bookId = Number(route.query.id)
    if (bookId) {
      const book = bookStore.books.find(b => b.id === bookId)
      if (book) {
        viewBook(book)
      }
    }
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
})

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

// 获取分类ID
const getCategoryId = (category) => {
  try {
    // 如果category是数字，直接返回
    if (typeof category === 'number') {
      return category;
    }
    
    // 如果category是对象，返回id属性
    if (typeof category === 'object' && category !== null) {
      if (category.id) {
        return category.id;
      }
    }
    
    // 默认返回null
    return null;
  } catch (error) {
    console.error('获取分类ID错误:', error);
    return null;
  }
}

// 修改筛选功能
const filteredBooks = computed(() => {
  let result = [...bookStore.books]
  
  // 按分类筛选
  if (filterCategory.value) {
    result = result.filter(book => {
      // 获取书籍的分类ID进行比较
      const categoryId = getCategoryId(book.category);
      return categoryId === filterCategory.value;
    });
  }
  
  // 搜索关键词
  if (searchText.value) {
    const searchLower = searchText.value.toLowerCase()
    result = result.filter(book => 
      book.title.toLowerCase().includes(searchLower) ||
      book.author.toLowerCase().includes(searchLower) ||
      (book.publisher && book.publisher.toLowerCase().includes(searchLower)) ||
      (book.description && book.description.toLowerCase().includes(searchLower))
    )
  }
  
  // 排序
  switch (sortBy.value) {
    case 'titleAsc':
      result.sort((a, b) => a.title.localeCompare(b.title))
      break
    case 'titleDesc':
      result.sort((a, b) => b.title.localeCompare(a.title))
      break
    case 'priceAsc':
      result.sort((a, b) => a.price - b.price)
      break
    case 'priceDesc':
      result.sort((a, b) => b.price - a.price)
      break
    case 'dateDesc':
      result.sort((a, b) => {
        const dateA = a.publish_date || a.publishDate || '1970-01-01'
        const dateB = b.publish_date || b.publishDate || '1970-01-01'
        return new Date(dateB) - new Date(dateA)
      })
      break
    case 'dateAsc':
      result.sort((a, b) => {
        const dateA = a.publish_date || a.publishDate || '1970-01-01'
        const dateB = b.publish_date || b.publishDate || '1970-01-01'
        return new Date(dateA) - new Date(dateB)
      })
      break
    default: // id
      result.sort((a, b) => a.id - b.id)
  }
  
  return result
})

// 分页功能
const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredBooks.value.slice(start, end)
})

// 处理页码变化
const handleCurrentChange = (page) => {
  currentPage.value = page
}

// 处理每页条数变化
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1 // 重置到第一页
}

// 重置筛选条件
const resetFilters = () => {
  searchText.value = ''
  filterCategory.value = ''
  sortBy.value = 'id'
  currentPage.value = 1
}

// 搜索处理
const handleSearch = async () => {
  if (searchText.value) {
    try {
      const searchResults = await bookStore.searchBooks(searchText.value)
      if (searchResults.length === 0) {
        ElMessage.warning('未找到相关图书')
      }
    } catch (error) {
      console.error('搜索失败:', error)
    }
  }
}

// 获取图书封面URL - 使用统一的工具函数
const getBookCoverUrl = (id, title) => {
  return mediaUtils.getBookCoverUrl(id, title)
}

// 查看图书详情
const viewBook = async (book) => {
  selectedBook.value = book
  showViewDialog.value = true
  
  // 加载图书评论
  reviewsLoading.value = true
  try {
    reviewForm.book = book.id
    bookReviews.value = await bookStore.fetchBookReviews(book.id)
    console.log('成功加载评论:', bookReviews.value.length)
  } catch (error) {
    console.error('加载评论失败:', error)
    ElMessage.error('加载评论失败，请稍后重试')
  } finally {
    reviewsLoading.value = false
  }
}

// 查看完整图书详情页面
const viewFullBookDetail = (bookId) => {
  // 关闭对话框
  showViewDialog.value = false
  selectedBook.value = null
  
  // 清空当前路由的查询参数，以防止在详情页刷新时保留之前的状态
  router.push({
    path: '/book-detail',
    query: { id: bookId, _t: Date.now() } // 添加时间戳确保路由是唯一的
  })
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
  
  let loadingInstance = null;
  try {
    dialogLocked.value = true
    // 添加提示
    loadingInstance = ElLoading.service({
      target: '.el-dialog__body',
      text: '提交评论中...',
      background: 'rgba(255, 255, 255, 0.7)'
    });
    
    // 保存评论内容副本用于后续处理
    const reviewContent = reviewForm.content
    const reviewRating = reviewForm.rating
    
    // 添加评论前先检查是否已有评论
    const hasExistingReview = bookReviews.value.some(
      review => review.user?.id === userStore.currentUser?.id
    );
    
    if (hasExistingReview) {
      // 提示用户正在更新评论
      ElMessage({
        type: 'info',
        message: '您已评论过此书，系统将更新您的评论',
        duration: 3000
      });
    }
    
    const response = await bookStore.addReview({
      book: reviewForm.book,
      rating: reviewRating,
      content: reviewContent
    })
  
    // 重置表单
    reviewForm.content = ''
    reviewForm.rating = 5
    
    // 先完全清除缓存
    bookStore.clearBookReviews(selectedBook.value.id)
    
    // 等待一小段时间后再加载评论，让后端有时间处理
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 手动从后端获取最新评论，而不经过store的提示逻辑
    try {
      const response = await reviewApi.getBookReviews(selectedBook.value.id);
      if (response && response.data) {
        // 直接更新评论列表，不经过store处理
        if (Array.isArray(response.data)) {
          bookReviews.value = response.data;
        } else if (response.data.results && Array.isArray(response.data.results)) {
          bookReviews.value = response.data.results;
        } else {
          bookReviews.value = [];
        }
      }
    } catch (refreshError) {
      console.error('刷新评论列表失败:', refreshError);
    }
    
    // 移除成功提示，避免与store中的提示重复
  } catch (error) {
    console.error('提交评论失败:', error)
    // 根据错误类型提供更详细的反馈
    if (error.response && error.response.status === 500) {
      // 服务器错误但可能是重复评论导致的
      if (JSON.stringify(error.response.data || {}).includes('Duplicate entry')) {
        ElMessage({
          type: 'info',
          message: '您的评论正在处理中，请稍后刷新页面查看',
          duration: 5000
        });
        
        // 延迟后尝试重新加载评论
        setTimeout(async () => {
          try {
            // 清除缓存再请求
            bookStore.clearBookReviews(selectedBook.value.id)
            const response = await reviewApi.getBookReviews(selectedBook.value.id);
            if (response && response.data) {
              if (Array.isArray(response.data)) {
                bookReviews.value = response.data;
              } else if (response.data.results && Array.isArray(response.data.results)) {
                bookReviews.value = response.data.results;
              }
            }
          } catch (refreshError) {
            console.error('刷新评论失败:', refreshError);
          }
        }, 2000);
      }
    }
    // 其他错误处理已在 store 中完成
  } finally {
    dialogLocked.value = false
    if (loadingInstance) {
      try {
        loadingInstance.close()
      } catch (e) {
        console.error('关闭加载状态失败:', e)
      }
    }
  }
}
  
// 处理对话框关闭
const handleDialogClose = () => {
  showViewDialog.value = false
  selectedBook.value = null
  bookReviews.value = []
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
  if (!dateString) return '未知时间';
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  } catch (error) {
    console.error('评论时间格式化错误:', error);
    return dateString;
  }
}

// 获取用户名辅助函数
const getUserName = (review) => {
  if (!review) return '匿名用户';
  
  // 尝试从不同可能的数据结构中获取用户名
  if (review.user?.username) {
    return review.user.username;
  } else if (review.username) {
    return review.username;
  } else if (review.user_name) {
    return review.user_name;
  } else if (typeof review.user === 'string') {
    return review.user;
  } else if (review.user?.id) {
    return `用户${review.user.id}`;
  }
  
  return '匿名用户';
}

// 获取用户头像初始字母
const getUserInitial = (review) => {
  const userName = getUserName(review);
  return userName.charAt(0).toUpperCase() || 'U';
}

// 处理图片加载错误
const handleImageError = (error) => {
  console.error('图片加载失败:', error)
}
</script>

<style scoped>
.books-view {
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

/* Element Plus样式覆盖 */
:deep(.el-table) {
  border-radius: 0.5rem;
  overflow: hidden;
}

:deep(.el-tag) {
  border-radius: 4px;
}

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
</style> 