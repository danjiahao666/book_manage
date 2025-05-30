<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">用户注册</h2>
      
      <!-- 注册表单 -->
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules"
        label-position="top"
        class="register-form"
      >
        <!-- 用户名输入框 -->
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名" 
          />
        </el-form-item>
        
        <!-- 邮箱输入框 -->
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="form.email" 
            placeholder="请输入邮箱" 
          />
        </el-form-item>
        
        <!-- 密码输入框 -->
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            show-password
          />
        </el-form-item>
        
        <!-- 确认密码输入框 -->
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码" 
            show-password
          />
        </el-form-item>
        
        <!-- 注册按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="loading" 
            class="register-button" 
            @click="onSubmit"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
        
        <!-- 错误提示 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <!-- 登录链接 -->
        <div class="login-link">
          已有账号？
          <router-link to="/login">立即登录</router-link>
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
  name: 'RegisterView',
  
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
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    // 表单验证规则
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        { 
          validator: (rule, value, callback) => {
            if (value !== form.password) {
              callback(new Error('两次输入的密码不一致'));
            } else {
              callback();
            }
          }, 
          trigger: 'blur' 
        }
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
        
        // 调用注册操作
        const result = await userStore.register({
          username: form.username,
          email: form.email,
          password: form.password
        });
        
        if (result) {
          ElMessage.success('注册成功，已自动登录');
          // 注册成功，跳转到首页
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
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.register-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.register-form {
  margin-top: 20px;
}

.register-button {
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

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.login-link a {
  color: #409eff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style> 