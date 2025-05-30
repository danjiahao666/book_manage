<template>
  <div class="profile-container">
    <div v-if="isAuthenticated" class="profile-card">
      <h2 class="profile-title">个人信息</h2>
      
      <!-- 用户信息展示区域 -->
      <div class="user-info">
        <div class="avatar-container">
          <el-avatar :size="100" :src="avatarUrl" class="user-avatar">
            {{ userInitials }}
          </el-avatar>
        </div>
        
        <div class="user-details">
          <h3 class="username">{{ username }}</h3>
          <p class="user-email">{{ userEmail }}</p>
        </div>
      </div>
      
      <!-- 统计信息 -->
      <div class="statistics">
        <div class="stat-item">
          <span class="stat-value">{{ favoriteCount }}</span>
          <span class="stat-label">收藏图书</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ reviewCount }}</span>
          <span class="stat-label">评论数量</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ lastLogin }}</span>
          <span class="stat-label">上次登录</span>
        </div>
      </div>
      
      <!-- 编辑按钮 -->
      <div class="actions">
        <el-button type="primary" @click="showEditForm = true">编辑个人信息</el-button>
        <el-button type="danger" @click="logout">退出登录</el-button>
      </div>
      
      <!-- 编辑表单对话框 -->
      <el-dialog
        title="编辑个人信息"
        v-model="showEditForm"
        width="500px"
        @close="handleDialogClose"
        :before-close="handleBeforeClose"
      >
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email" />
          </el-form-item>
          
          <el-form-item label="新密码" prop="newPassword">
            <el-input 
              v-model="form.newPassword" 
              type="password"
              placeholder="不修改请留空"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input 
              v-model="form.confirmPassword" 
              type="password"
              placeholder="不修改请留空" 
              show-password
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="handleDialogClose">取消</el-button>
            <el-button type="primary" @click="submitEdit" :loading="loading">
              保存
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>
    
    <!-- 未登录提示 -->
    <div v-else class="not-logged-in">
      <el-empty description="您尚未登录">
        <el-button type="primary" @click="$router.push('/login')">
          前往登录
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import { ElMessage } from 'element-plus';

export default {
  name: 'ProfileView',
  
  setup() {
    // 获取用户状态管理
    const userStore = useUserStore();
    // 路由
    const router = useRouter();
    // 表单引用
    const formRef = ref(null);
    // 控制编辑表单对话框显示
    const showEditForm = ref(false);
    
    // 计算属性：判断是否已登录
    const isAuthenticated = computed(() => userStore.isAuthenticated);
    // 计算属性：获取用户名
    const username = computed(() => userStore.currentUser?.username || '');
    // 计算属性：获取用户邮箱
    const userEmail = computed(() => userStore.currentUser?.email || '');
    // 计算属性：获取加载状态
    const loading = computed(() => userStore.loading);
    
    // 虚拟数据 - 实际项目中应从API获取
    const favoriteCount = ref(12);
    const reviewCount = ref(5);
    const lastLogin = ref('2023-06-15');
    
    // 计算用户头像的首字母
    const userInitials = computed(() => {
      if (!username.value) return '';
      return username.value.substring(0, 2).toUpperCase();
    });
    
    // 用户头像URL - 如果用户上传了头像则使用，否则显示首字母
    const avatarUrl = computed(() => userStore.currentUser?.avatar || '');
    
    // 编辑表单数据
    const form = reactive({
      username: '',
      email: '',
      newPassword: '',
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
      newPassword: [
        { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
      ],
      confirmPassword: [
        { 
          validator: (rule, value, callback) => {
            if (form.newPassword && value !== form.newPassword) {
              callback(new Error('两次输入的密码不一致'));
            } else {
              callback();
            }
          }, 
          trigger: 'blur' 
        }
      ]
    };
    
    // 组件挂载时初始化
    onMounted(async () => {
      // 如果已登录但没有用户信息，获取用户信息
      if (isAuthenticated.value && !userStore.currentUser) {
        await userStore.fetchCurrentUser();
      }
      
      // 如果已有用户信息，初始化编辑表单
      if (userStore.currentUser) {
        form.username = userStore.currentUser.username;
        form.email = userStore.currentUser.email;
      }
    });
    
    // 处理对话框关闭事件
    const handleDialogClose = () => {
      showEditForm.value = false;
      resetForm();
    };
    
    // 处理对话框关闭前的确认
    const handleBeforeClose = (done) => {
      resetForm();
      done();
    };
    
    // 重置表单
    const resetForm = () => {
      // 清空密码字段
      form.newPassword = '';
      form.confirmPassword = '';
      
      // 重置表单为当前用户信息
      if (userStore.currentUser) {
        form.username = userStore.currentUser.username;
        form.email = userStore.currentUser.email;
      }
      
      // 清除表单验证状态
      if (formRef.value) {
        formRef.value.clearValidate();
      }
    };
    
    // 提交编辑表单
    const submitEdit = async () => {
      try {
        // 表单验证
        await formRef.value.validate();
        
        // 构建更新数据
        const updateData = {
          username: form.username,
          email: form.email
        };
        
        // 如果有设置新密码，添加到更新数据中
        if (form.newPassword) {
          updateData.password = form.newPassword;
        }
        
        // 调用API更新用户信息 (需要在实际项目中实现)
        // const result = await userStore.updateUser(updateData);
        
        // 模拟更新成功
        ElMessage.success('个人信息更新成功');
        handleDialogClose(); // 使用handleDialogClose代替直接设置showEditForm
        
        // 刷新用户信息
        await userStore.fetchCurrentUser();
      } catch (error) {
        console.error('表单验证失败:', error);
      }
    };
    
    // 退出登录
    const logout = () => {
      userStore.logout();
      ElMessage.success('退出登录成功');
      router.push('/login');
    };
    
    return {
      isAuthenticated,
      username,
      userEmail,
      loading,
      favoriteCount,
      reviewCount,
      lastLogin,
      userInitials,
      avatarUrl,
      form,
      rules,
      formRef,
      showEditForm,
      submitEdit,
      logout,
      handleDialogClose,
      handleBeforeClose
    };
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.profile-card {
  width: 100%;
  max-width: 800px;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.profile-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.avatar-container {
  margin-right: 30px;
}

.user-avatar {
  background-color: #409eff;
  color: white;
  font-weight: bold;
}

.user-details {
  flex: 1;
}

.username {
  font-size: 24px;
  margin: 0 0 5px;
  color: #333;
}

.user-email {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.statistics {
  display: flex;
  justify-content: space-around;
  margin: 30px 0;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.not-logged-in {
  width: 100%;
  max-width: 500px;
  margin: 100px auto;
  text-align: center;
}
</style> 