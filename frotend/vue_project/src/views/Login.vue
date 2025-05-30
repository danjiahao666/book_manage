<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">用户登录</h2>
      
      <!-- 登录表单 -->
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules"
        label-position="top"
        class="login-form"
      >
        <!-- 用户名输入框 -->
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
            @keyup.enter="onSubmit"
          />
        </el-form-item>
        
        <!-- 密码输入框 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            show-password
            @keyup.enter="onSubmit"
          />
        </el-form-item>
        
        <!-- 记住我选项 -->
        <el-form-item>
          <el-checkbox v-model="form.remember">记住我</el-checkbox>
        </el-form-item>
        
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="login-button" 
            @click="onSubmit"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
        
        <!-- 错误提示 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <!-- 注册链接 -->
        <div class="register-link">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import { ElMessage } from 'element-plus';

export default {
  name: 'LoginView',
  
  setup() {
    // 获取用户状态管理
    const userStore = useUserStore();
    // 路由
    const router = useRouter();
    // 表单引用
    const formRef = ref(null);
    
    // 表单数据
    const form = reactive({
      username: '',
      password: '',
      remember: false
    });
    
    // 表单验证规则
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
      ]
    };
    
    // 计算属性：获取加载状态
    const loading = computed(() => userStore.loading);
    // 计算属性：获取错误信息
    const error = computed(() => userStore.error);
    
    // 提交表单
    const onSubmit = async () => {
      if (!formRef.value) return;
      
      try {
        // 表单验证
        await formRef.value.validate();
        
        // 调用登录操作
        const success = await userStore.login({
          username: form.username,
          password: form.password
        });
        
        if (success) {
          ElMessage.success('登录成功');
          // 登录成功，跳转到首页
          router.push('/');
        }
      } catch (error) {
        console.error('表单验证失败:', error);
      }
    };
    
    return {
      formRef,
      form,
      rules,
      loading,
      error,
      onSubmit
    };
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
  font-size: 16px;
  height: 40px;
}

.error-message {
  color: #f56c6c;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.register-link a {
  color: #409eff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style> 