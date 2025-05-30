// api.js - 与后端API通信的服务

import axios from 'axios';

// API配置
export const API_CONFIG = {
  // 后端API基础URL
  BASE_URL: 'http://localhost:8000/api',
  // 媒体文件基础URL
  MEDIA_URL: 'http://localhost:8000/media',
  // API超时时间 (毫秒)
  TIMEOUT: 15000
}

// 创建axios实例
const apiClient = axios.create({
  // 设置基础URL，指向Django后端
  baseURL: API_CONFIG.BASE_URL,
  // 设置请求超时
  timeout: API_CONFIG.TIMEOUT,
  // 请求头
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 重试配置
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000; // 毫秒

// 请求计数和缓存
const pendingRequests = new Map();
const responseCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 缓存持续时间，5分钟

// 请求拦截器 - 添加认证令牌和缓存处理
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      // 确保Token格式正确 - Django REST Framework需要"Token "前缀
      config.headers['Authorization'] = `Token ${token}`;
    }
    
    // 对GET请求进行缓存处理
    if (config.method === 'get' && !config.params?.noCache) {
      const cacheKey = `${config.url}${JSON.stringify(config.params || {})}`;
      const cachedResponse = responseCache.get(cacheKey);
      
      if (cachedResponse && (Date.now() - cachedResponse.timestamp) < CACHE_DURATION) {
        // 使用缓存的响应
        console.log(`[API] 使用缓存数据: ${cacheKey}`);
        config.adapter = () => {
          return Promise.resolve({
            data: cachedResponse.data,
            status: 200,
            statusText: 'OK',
            headers: cachedResponse.headers,
            config,
            request: {}
          });
        };
      }
    }
    
    return config;
  },
  error => {
    console.error('请求拦截器错误:', error);
    return Promise.reject(error);
  }
);

// 添加响应拦截器
apiClient.interceptors.response.use(
  response => {
    // 缓存GET请求的响应
    if (response.config.method === 'get' && !response.config.params?.noCache) {
      const cacheKey = `${response.config.url}${JSON.stringify(response.config.params || {})}`;
      responseCache.set(cacheKey, {
        data: response.data,
        headers: response.headers,
        timestamp: Date.now()
      });
    }
    
    return response;
  },
  async error => {
    const originalRequest = error.config;
    
    // 初始化重试计数
    if (originalRequest._retryCount === undefined) {
      originalRequest._retryCount = 0;
    }
    
    // 处理请求超时或网络错误，尝试重试
    if ((error.code === 'ECONNABORTED' || 
         error.message?.includes('timeout') || 
         error.message?.includes('Network Error')) && 
        originalRequest._retryCount < MAX_RETRIES) {
        
      console.warn(`请求超时或网络错误，准备重试 (${originalRequest._retryCount + 1}/${MAX_RETRIES}):`, originalRequest.url);
      
      // 增加重试计数
      originalRequest._retryCount++;
      
      // 延迟一段时间后重试
      await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
      
      console.log(`正在重试请求 (${originalRequest._retryCount}/${MAX_RETRIES}):`, originalRequest.url);
      return apiClient(originalRequest);
    }
    
    if (error.response) {
      // 服务器响应了但状态码不在2xx范围
      console.error('API请求失败:', {
        status: error.response.status,
        data: error.response.data,
        url: error.config.url
      });
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('API请求无响应:', {
        url: error.config.url,
        method: error.config.method,
        timeout: error.config.timeout,
        retryCount: originalRequest._retryCount || 0
      });
    } else {
      // 请求设置有问题
      console.error('API请求配置错误:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// 用户相关API
export const userApi = {
  // 用户登录
  login(credentials) {
    return apiClient.post('/users/token-auth/', credentials);
  },
  
  // 用户注册
  register(userData) {
    return apiClient.post('/users/users/', userData);
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return apiClient.get('/users/users/me/');
  },
  
  // 更新用户信息
  updateUser(userId, userData) {
    return apiClient.put(`/users/users/${userId}/`, userData);
  }
};

// 图书相关API
export const bookApi = {
  // 获取所有图书
  getAllBooks(timestamp) {
    console.log('正在请求所有图书数据...')
    return apiClient.get('/books/books/', { 
      params: { 
        noCache: true,
        // 添加时间戳参数确保不使用缓存
        t: timestamp || Date.now(),
        page_size: 100,  // 设置分页大小为100
        no_page: true    // 完全禁用分页
      } 
    }).then(response => {
      // 处理分页响应
      if (response.data && response.data.results) {
        console.log(`获取到分页图书数据: ${response.data.results.length}本`)
        return { ...response, data: response.data.results };
      }
      // 如果是直接返回的数组
      if (Array.isArray(response.data)) {
        console.log(`获取到图书数组数据: ${response.data.length}本`)
        return response;
      }
      // 其他情况尝试提取有用数据
      console.log('图书数据格式不是预期的分页或数组格式:', response.data)
      const extractedData = response.data.books || response.data.results || [];
      return { ...response, data: extractedData };
    }).catch(error => {
      console.error('获取图书数据失败:', error)
      // 返回失败的Promise以便外部处理错误
      return Promise.reject(error)
    });
  },
  
  // 获取单本图书详情
  getBook(bookId) {
    return apiClient.get(`/books/books/${bookId}/`);
  },
  
  // 搜索图书
  searchBooks(query) {
    // 搜索请求不应该被缓存
    return apiClient.get(`/books/books/search/?q=${query}`, { params: { noCache: true } });
  }
};

// 分类相关API
export const categoryApi = {
  // 获取所有分类
  getAllCategories(timestamp) {
    console.log('正在请求所有分类数据...')
    return apiClient.get('/books/categories/', { 
      params: { 
        noCache: true,
        // 如果提供了时间戳，则使用它
        t: timestamp || Date.now()  // 添加时间戳参数确保不使用缓存
      } 
    }).then(response => {
      // 处理分页响应
      if (response.data && response.data.results) {
        console.log(`获取到分页分类数据: ${response.data.results.length}个`)
        return { ...response, data: response.data.results };
      }
      // 如果是直接返回的数组
      if (Array.isArray(response.data)) {
        console.log(`获取到分类数组数据: ${response.data.length}个`)
        return response;
      }
      // 其他情况尝试提取有用数据
      console.log('分类数据格式不是预期的分页或数组格式:', response.data)
      const extractedData = response.data.categories || response.data.results || [];
      return { ...response, data: extractedData };
    }).catch(error => {
      console.error('获取分类数据失败:', error)
      // 返回失败的Promise以便外部处理错误
      return Promise.reject(error)
    });
  },
  
  // 获取单个分类详情
  getCategory(categoryId) {
    return apiClient.get(`/books/categories/${categoryId}/`);
  },
  
  // 获取分类下的所有图书
  getCategoryBooks(categoryId) {
    return apiClient.get(`/books/categories/${categoryId}/books/`);
  }
};

// 评论相关API
export const reviewApi = {
  // 获取图书的所有评论
  getBookReviews(bookId) {
    console.log(`正在获取图书ID=${bookId}的评论...`);
    return apiClient.get(`/books/books/${bookId}/reviews/`, { params: { noCache: true } }).then(response => {
      // 处理响应数据
      console.log(`获取到图书评论:`, response.data);
      
      // 调试日志：查看评论数据格式
      if (Array.isArray(response.data)) {
        console.log(`评论数据是数组，长度: ${response.data.length}`);
        // 查看第一条评论的结构（如果存在）
        if (response.data.length > 0) {
          console.log('第一条评论结构:', JSON.stringify(response.data[0], null, 2));
        }
      } else if (response.data && response.data.results) {
        console.log(`评论数据是分页对象，结果长度: ${response.data.results.length}`);
        if (response.data.results.length > 0) {
          console.log('第一条评论结构:', JSON.stringify(response.data.results[0], null, 2));
        }
      } else {
        console.log('评论数据格式不是数组或分页对象:', response.data);
      }
      
      // 处理分页响应
      if (response.data && response.data.results) {
        return { ...response, data: response.data.results };
      }
      
      // 如果是数组，直接返回
      if (Array.isArray(response.data)) {
        return { ...response, data: response.data };
      }
      
      return response;
    }).catch(error => {
      console.error(`获取图书ID=${bookId}评论失败:`, error);
      return Promise.reject(error);
    });
  },
  
  // 添加评论
  addReview(reviewData) {
    console.log('添加评论数据:', reviewData);
    return apiClient.post('/books/comments/', reviewData)
      .then(response => {
        console.log('评论添加成功，响应数据:', response.data);
        return response;
      })
      .catch(error => {
        console.error('评论添加失败:', error);
        console.error('错误详情:', error.response?.data || error.message);
        return Promise.reject(error);
      });
  },
  
  // 更新评论 (只有自己发表的评论才能更新)
  updateReview(reviewId, reviewData) {
    console.log(`更新评论ID=${reviewId}:`, reviewData);
    return apiClient.put(`/books/comments/${reviewId}/`, reviewData)
      .then(response => {
        console.log('评论更新成功，响应数据:', response.data);
        return response;
      })
      .catch(error => {
        console.error(`更新评论ID=${reviewId}失败:`, error);
        return Promise.reject(error);
      });
  },
  
  // 删除评论 (只有自己发表的评论才能删除)
  deleteReview(reviewId) {
    return apiClient.delete(`/books/comments/${reviewId}/`);
  }
};

// 清除API缓存的方法
export const clearApiCache = () => {
  responseCache.clear();
  console.log('[API] 缓存已清除');
};

// 媒体文件工具函数
export const mediaUtils = {
  /**
   * 获取图书封面URL
   * @param {number} id - 图书ID
   * @param {string} title - 图书标题
   * @returns {string} 图书封面完整URL
   */
  getBookCoverUrl(id, title) {
    // 数据库ID与文件名已对齐，直接使用原始ID
    const safeTitle = title ? title.replace(/[\\/:*?"<>|]/g, '_') : 'unknown'
    const imageUrl = `${API_CONFIG.MEDIA_URL}/covers/${id}_${safeTitle}.jpg`
    
    return imageUrl
  },
  
  /**
   * 获取默认图书封面URL
   * @returns {string} 默认图书封面URL
   */
  getDefaultCoverUrl() {
    return `${API_CONFIG.MEDIA_URL}/covers/default.jpg`
  }
}

// 导出API对象
export default {
  user: userApi,
  book: bookApi,
  category: categoryApi,
  review: reviewApi,
  clearCache: clearApiCache,
  mediaUtils,
  config: API_CONFIG
}; 