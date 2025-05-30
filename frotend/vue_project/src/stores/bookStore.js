import { defineStore } from 'pinia'
import { bookApi, categoryApi, reviewApi } from '../services/api'
import { ElMessage } from 'element-plus'

// 添加防抖函数
const debounce = (fn, delay) => {
  let timer = null
  return function(...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

export const useBookStore = defineStore('book', {
  state: () => ({
    books: [],
    categories: [],
    reviews: {},  // 使用对象缓存不同图书ID的评论
    loading: false,
    error: null,
    lastFetchTime: 0, // 上次加载数据的时间戳
    cacheExpireTime: 5 * 60 * 1000 // 缓存过期时间 (5分钟)
  }),
  
  getters: {
    // 获取所有图书
    getAllBooks() {
      return this.books
    },
    
    // 获取所有分类及其包含的图书数量
    getAllCategories() {
      return this.categories
    },
    
    // 获取图书总数
    getTotalBooks() {
      return this.books.length
    }
  },
  
  actions: {
    // 清除现有数据
    clearData() {
      this.books = []
      this.categories = []
      this.reviews = {}
      this.lastFetchTime = 0
      console.log('已清除图书和分类数据缓存')
    },
    
    // 清除特定图书的评论缓存
    clearBookReviews(bookId) {
      if (bookId) {
        if (this.reviews[bookId]) {
          delete this.reviews[bookId]
          console.log(`已清除图书ID ${bookId} 的评论缓存`)
        }
      } else {
        // 如果没有指定bookId，清除所有评论缓存
        this.reviews = {}
        console.log('已清除所有图书评论缓存')
      }
    },

    // 加载所有图书
    async fetchBooks() {
      this.loading = true
      this.error = null
      try {
        console.log('获取新的图书数据')
        // 添加时间戳参数，确保不使用缓存
        const timestamp = Date.now()
        console.log(`添加时间戳参数: ${timestamp}`)
        const response = await bookApi.getAllBooks(timestamp)
        
        // 检查和处理数据
        if (Array.isArray(response.data)) {
          console.log(`成功获取${response.data.length}本图书`)
          // 检查每本书的数据格式
          this.books = response.data.map(book => {
            // 确保价格是数字
            if (book.price !== undefined && book.price !== null) {
              book.price = parseFloat(book.price)
              if (isNaN(book.price)) book.price = 0
            } else {
              book.price = 0
            }
            return book
          })
        } else {
          console.error('获取的图书数据格式不正确:', response.data)
          if (this.books.length === 0) {
            // 只有当现有数据为空时才使用可能不完整的数据
            this.books = Array.isArray(response.data) ? response.data : []
          }
        }
        
        this.lastFetchTime = Date.now()
        return this.books
      } catch (error) {
        console.error('获取图书失败:', error)
        this.error = '获取图书失败，请稍后重试'
        ElMessage.error(this.error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 加载所有分类
    async fetchCategories() {
      this.loading = true
      this.error = null
      try {
        console.log('获取新的分类数据')
        // 添加时间戳参数，确保不使用缓存
        const timestamp = Date.now()
        console.log(`添加时间戳参数: ${timestamp}`)
        const response = await categoryApi.getAllCategories(timestamp)
        
        // 检查和处理数据
        if (Array.isArray(response.data)) {
          console.log(`成功获取${response.data.length}个分类`)
          this.categories = response.data.map(category => ({
            ...category,
            name: category.name || '未命名分类',
            count: category.book_count || 0,
            id: category.id || 0
          }))
        } else {
          console.error('获取的分类数据格式不正确:', response.data)
          if (this.categories.length === 0) {
            this.categories = []
          }
        }
        
        this.lastFetchTime = Date.now()
        return this.categories
      } catch (error) {
        console.error('获取分类失败:', error)
        this.error = '获取分类失败，请稍后重试'
        ElMessage.error(this.error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 加载图书的评论
    async fetchBookReviews(bookId) {
      // 如果已有缓存的评论，直接返回
      if (this.reviews[bookId]) {
        console.log(`使用缓存的图书ID ${bookId} 评论`)
        return this.reviews[bookId]
      }
      
      this.loading = true
      this.error = null
      try {
        const response = await reviewApi.getBookReviews(bookId)
        
        // 数据验证和处理
        let reviewsData = [];
        
        if (Array.isArray(response.data)) {
          console.log(`获取到评论数组，长度: ${response.data.length}`);
          reviewsData = response.data;
        } else if (response.data && response.data.results && Array.isArray(response.data.results)) {
          console.log(`获取到分页评论数据，长度: ${response.data.results.length}`);
          reviewsData = response.data.results;
        } else if (typeof response.data === 'object') {
          console.log('评论数据为对象，尝试提取有效数据');
          // 尝试从对象中提取可能的评论数组
          const possibleReviews = Object.values(response.data).find(val => Array.isArray(val));
          if (possibleReviews) {
            reviewsData = possibleReviews;
          } else {
            // 如果没有找到数组，将对象转为数组处理
            reviewsData = [response.data];
          }
        } else {
          console.warn('未识别的评论数据格式:', response.data);
          reviewsData = [];
        }
        
        // 确保评论数据中的每个评论对象都有必要的字段
        reviewsData = reviewsData.map(review => {
          // 基本验证，确保是对象
          if (!review || typeof review !== 'object') {
            return {
              id: Math.random().toString(36).substring(2, 10),
              content: '数据错误',
              rating: 0,
              created_at: new Date().toISOString(),
              user: { username: '未知用户' }
            };
          }
          
          // 处理可能的数据问题
          return {
            id: review.id || Math.random().toString(36).substring(2, 10),
            content: review.content || '',
            rating: Number(review.rating) || 0,
            created_at: review.created_at || review.createdAt || new Date().toISOString(),
            updated_at: review.updated_at || review.updatedAt || new Date().toISOString(),
            user: review.user || { username: '未知用户' },
            book: review.book || bookId
          };
        });
        
        // 将特定图书的评论存储在reviews对象中
        this.reviews[bookId] = reviewsData;
        return reviewsData;
      } catch (error) {
        console.error(`获取图书ID ${bookId} 的评论失败:`, error);
        this.error = '获取评论失败，请稍后重试';
        ElMessage.error(this.error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // 添加评论
    async addReview(reviewData) {
      this.loading = true
      this.error = null
      try {
        const response = await reviewApi.addReview(reviewData)
        // 更新缓存的评论
        const bookId = reviewData.book
        if (this.reviews[bookId]) {
          // 检查是否更新了已有评论
          const existingReviewIndex = this.reviews[bookId].findIndex(r => r.user?.id === response.data.user?.id);
          if (existingReviewIndex >= 0) {
            // 更新已有评论
            this.reviews[bookId][existingReviewIndex] = response.data;
            ElMessage.success('评论更新成功');
          } else {
            // 添加新评论
            this.reviews[bookId].push(response.data);
            ElMessage.success('评论添加成功');
          }
        }
        return response.data
      } catch (error) {
        console.error('评论操作失败:', error)
        
        // 检查错误类型和状态码
        if (error.response) {
          // 处理完整性错误（唯一约束冲突）
          if (error.response.status === 400 || error.response.status === 500) {
            const errorMessage = error.response?.data?.detail || '';
            const errorString = JSON.stringify(error.response?.data || {});
            
            if (errorMessage.includes('unique') || 
                errorMessage.includes('已经评论') || 
                errorString.includes('unique') || 
                errorString.includes('Duplicate entry') ||
                error.response?.data?.non_field_errors?.some(e => e.includes('已经评论'))) {
              this.error = '您已经评论过这本书，系统正在尝试更新您的评论';
              ElMessage.warning(this.error);
              
              // 尝试再次获取评论列表以刷新数据
              try {
                if (reviewData.book) {
                  await this.fetchBookReviews(reviewData.book);
                }
              } catch (refreshError) {
                console.error('刷新评论数据失败:', refreshError);
              }
            } else {
              this.error = '评论失败: ' + (errorMessage || '服务器错误');
              ElMessage.error(this.error);
            }
          } else {
            this.error = `添加评论失败 (${error.response.status}): ${error.response.statusText}`;
            ElMessage.error(this.error);
          }
        } else if (error.request) {
          // 请求发送但没有收到响应
          this.error = '服务器无响应，请检查网络连接';
          ElMessage.error(this.error);
        } else {
          // 请求设置有问题
          this.error = '添加评论失败: ' + error.message;
          ElMessage.error(this.error);
        }
        
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 搜索图书 - 使用防抖
    searchBooks: debounce(async function(query) {
      this.loading = true
      this.error = null
      try {
        const response = await bookApi.searchBooks(query)
        return response.data
      } catch (error) {
        console.error('搜索图书失败:', error)
        this.error = '搜索图书失败，请稍后重试'
        ElMessage.error(this.error)
        return []
      } finally {
        this.loading = false
      }
    }, 500),
    
    // 初始化store，加载所有必要数据
    async initialize() {
      await Promise.all([
        this.fetchBooks(),
        this.fetchCategories()
      ])
    },
    
    // 更新分类的图书数量
    async updateCategoriesBookCount() {
      try {
        console.log('开始更新分类图书数量...')
        
        // 检查是否已加载图书和分类
        if (this.books.length === 0 || this.categories.length === 0) {
          console.log('图书或分类数据不存在，先加载数据...')
          // 如果没有数据，先强制获取
          const timestamp = Date.now()
          await Promise.all([
            this.fetchBooks(),
            this.fetchCategories()
          ])
        }
        
        console.log(`当前有 ${this.books.length} 本图书和 ${this.categories.length} 个分类`)
        
        // 计算每个分类中的图书数量
        const categoryCountMap = {}
        
        // 初始化所有分类的计数为0
        this.categories.forEach(category => {
          if (category && category.id) {
            categoryCountMap[category.id] = 0
          }
        })
        
        // 统计每个分类的图书数量
        this.books.forEach(book => {
          // 处理不同格式的category字段
          let categoryId = null
          
          if (book.category) {
            if (typeof book.category === 'object' && book.category !== null) {
              categoryId = book.category.id
            } else if (typeof book.category === 'number' || typeof book.category === 'string') {
              categoryId = Number(book.category)
            }
          }
          
          if (categoryId && categoryCountMap[categoryId] !== undefined) {
            categoryCountMap[categoryId] = (categoryCountMap[categoryId] || 0) + 1
          }
        })
        
        console.log('统计的分类图书数量:', categoryCountMap)
        
        // 更新分类数量
        this.categories = this.categories.map(category => {
          if (category && category.id) {
            return {
              ...category,
              count: categoryCountMap[category.id] || 0
            }
          }
          return category
        })
        
        console.log('分类图书数量更新完成:', this.categories.map(c => `${c.name}: ${c.count}本`).join(', '))
        
        return this.categories
      } catch (error) {
        console.error('更新分类图书数量失败:', error)
        return this.categories
      }
    }
  }
}) 