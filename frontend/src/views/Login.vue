<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>登录</h2>
        <p>欢迎回来，请登录您的账号</p>
      </div>
      
      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="rules" 
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="邮箱/手机号" prop="account">
          <el-input 
            v-model="loginForm.account" 
            placeholder="请输入邮箱或手机号" 
            prefix-icon="el-icon-message"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="el-icon-lock"
            show-password
          ></el-input>
        </el-form-item>
        
        <div class="form-actions">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" href="#">忘记密码?</el-link>
        </div>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            class="login-button" 
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-link">
        还没有账号? <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import request from '@/utils/request';

export default {
  name: 'Login',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    const loginForm = reactive({
      account: '',
      password: ''
    });
    
    const rules = {
      account: [
        { required: true, message: '请输入邮箱或手机号', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
      ]
    };
    
    const loginFormRef = ref(null);
    const loading = ref(false);
    const rememberMe = ref(false);
    
    const handleLogin = async () => {
      try {
        await loginFormRef.value.validate()
        console.log('使用邮箱登录:', loginForm.account)
        
        try {
          // 将 account 转换为 email
          const loginData = {
            email: loginForm.account,
            password: loginForm.password
          }
          
          console.log('发送登录请求:', loginData)
          const response = await request.post('/user/login', loginData);
          console.log('登录成功，响应数据:', response)
          
          if (response && response.access_token && response.user) {
            // 先明确设置token
            const token = response.access_token;
            localStorage.setItem('token', token);
            store.commit('SET_TOKEN', token);
            
            // 确保用户对象格式正确并包含必要信息
            const userData = {
              ...response.user,
              id: response.user.id,
              username: response.user.username || '用户' + response.user.id,
              email: response.user.email,
              role: response.user.role,
              avatar: response.user.avatar || 'default.jpg'
            };
            
            console.log('处理后的用户数据:', userData);
            
            // 额外保存一些关键信息便于访问
            localStorage.setItem('userRole', userData.role);
            localStorage.setItem('userId', userData.id);
            
            // 保存用户信息到Vuex模块
            await store.dispatch('user/setUser', userData);
            
            console.log('保存完成的用户信息:', store.getters['user/userInfo']);
            console.log('认证状态:', store.getters['user/isAuthenticated']);
            
            // 根据用户角色设置重定向路径
            let redirectPath = '/'
            if (userData.role === 'author') {
              redirectPath = '/author/center'
              console.log('用户是作者，重定向到:', redirectPath)
            } else if (userData.role === 'admin') {
              redirectPath = '/admin/dashboard'
              console.log('用户是管理员，重定向到:', redirectPath)
            } else {
              console.log('普通用户，重定向到:', redirectPath)
            }
            
            console.log('最终重定向到:', redirectPath)
            router.push(redirectPath)
          } else {
            throw new Error('登录响应格式错误：缺少token或用户信息')
          }
        } catch (error) {
          console.error('登录失败:', error)
          const errorMessage = error.response?.data?.message || error.message || '登录失败，请重试'
          ElMessage.error(errorMessage)
        }
      } catch (error) {
        console.error('表单验证失败:', error)
        return false
      }
    };
    
    return {
      loginForm,
      loginFormRef,
      rules,
      loading,
      rememberMe,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 10px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.register-link a {
  color: #409EFF;
  text-decoration: none;
}
</style> 