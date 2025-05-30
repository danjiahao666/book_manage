// userStore.js - 用户状态管理
import { defineStore } from 'pinia';
import { userApi } from '../services/api';

export const useUserStore = defineStore('user', {
  state: () => ({
    // 用户信息
    currentUser: null,
    // 登录状态
    isLoggedIn: false,
    // 登录令牌
    token: localStorage.getItem('token') || null,
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    // 获取用户名
    username: (state) => state.currentUser?.username || '',
    // 判断是否已登录
    isAuthenticated: (state) => !!state.token && state.isLoggedIn,
    // 获取用户ID
    userId: (state) => state.currentUser?.id || null,
  },
  
  actions: {
    // 登录操作
    async login(credentials) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('登录请求数据:', credentials);
        
        // 调用登录API
        const response = await userApi.login(credentials);
        console.log('登录响应数据:', response.data);
        
        // 处理不同格式的响应
        let token, user;
        
        if (response.data.token) {
          // 直接返回token的情况
          if (typeof response.data.user === 'object') {
            // 格式 { token: '...', user: {...} }
            token = response.data.token;
            user = response.data.user;
          } else {
            // 格式 { token: '...', ... } 其余字段是用户信息
            token = response.data.token;
            user = { ...response.data };
            delete user.token;
          }
        } else if (response.data.key) {
          // DRF的dj-rest-auth格式 { key: '...' }
          token = response.data.key;
          // 需要单独获取用户信息
          await this.fetchCurrentUser();
          return true;
        } else {
          console.error('未知的响应格式:', response.data);
          this.error = '服务器返回了未知格式的数据';
          return false;
        }
        
        // 保存令牌到本地存储和状态
        console.log('保存token:', token);
        localStorage.setItem('token', token);
        this.token = token;
        this.isLoggedIn = true;
        
        // 设置用户信息
        if (user) {
          this.currentUser = user;
          console.log('设置用户信息:', user);
        } else {
          console.log('没有用户信息，尝试获取');
          // 如果没有用户信息，尝试获取
          await this.fetchCurrentUser();
        }
        
        return true;
      } catch (error) {
        console.error('登录失败:', error);
        let errorMsg = '登录失败，请检查用户名和密码';
        
        if (error.response) {
          // 处理服务器返回的错误
          if (error.response.data) {
            if (error.response.data.detail) {
              errorMsg = error.response.data.detail;
            } else if (typeof error.response.data === 'string') {
              errorMsg = error.response.data;
            } else if (typeof error.response.data === 'object') {
              // 处理表单验证错误
              errorMsg = Object.values(error.response.data)
                .map(errors => Array.isArray(errors) ? errors.join(', ') : errors)
                .join('; ');
            }
          }
        }
        
        this.error = errorMsg;
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // 获取当前用户信息
    async fetchCurrentUser() {
      if (!this.token) {
        console.log('没有令牌，无法获取用户信息');
        return null;
      }
      
      this.loading = true;
      console.log('尝试获取当前用户信息');
      
      try {
        const response = await userApi.getCurrentUser();
        console.log('获取用户信息成功:', response.data);
        this.currentUser = response.data;
        this.isLoggedIn = true;
        return this.currentUser;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        
        // 尝试解析错误
        let errorDetail = '未知错误';
        if (error.response) {
          console.log('错误状态码:', error.response.status);
          console.log('错误数据:', error.response.data);
          
          if (error.response.status === 401) {
            console.log('未授权错误，可能是令牌无效或过期');
            this.logout();
            this.error = '登录已过期，请重新登录';
          } else {
            errorDetail = error.response.data?.detail || error.response.statusText || '服务器错误';
            this.error = `获取用户信息失败: ${errorDetail}`;
          }
        } else if (error.request) {
          console.log('没有收到响应:', error.request);
          this.error = '服务器没有响应，请检查网络连接';
        } else {
          console.log('请求配置错误:', error.message);
          this.error = `请求错误: ${error.message}`;
        }
        
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // 注册操作
    async register(userData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await userApi.register(userData);
        // 注册成功后自动登录
        await this.login({
          username: userData.username,
          password: userData.password
        });
        return response.data;
      } catch (error) {
        console.error('注册失败:', error);
        this.error = error.response?.data || '注册失败，请稍后再试';
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // 退出登录
    logout() {
      // 清除本地存储中的令牌
      localStorage.removeItem('token');
      
      // 重置状态
      this.token = null;
      this.currentUser = null;
      this.isLoggedIn = false;
      this.error = null;
    },
    
    // 初始化用户状态 (应用启动时调用)
    async initialize() {
      if (this.token) {
        return await this.fetchCurrentUser();
      }
      return null;
    }
  }
}); 