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
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';

export default {
  name: 'Login',
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    
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
      if (!loginFormRef.value) return;
      
      await loginFormRef.value.validate(async (valid) => {
        if (!valid) {
          console.error('表单验证失败');
          return;
        }
        
        loading.value = true;
        
        try {
          // Determine if account is email or phone
          const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(loginForm.account);
          
          const loginData = {
            password: loginForm.password
          };
          
          if (isEmail) {
            loginData.email = loginForm.account;
            console.log('使用邮箱登录:', loginData.email);
          } else {
            loginData.phone = loginForm.account;
            console.log('使用手机号登录:', loginData.phone);
          }
          
          console.log('发送登录请求:', JSON.stringify(loginData));
          
          const result = await store.dispatch('user/login', loginData);
          console.log('登录成功，用户信息:', result);
          
          ElMessage({
            type: 'success',
            message: '登录成功'
          });
          
          // 验证用户角色是否保存
          const savedRole = localStorage.getItem('userRole');
          console.log('保存的用户角色:', savedRole);
          
          // Redirect to intended page or home
          const redirectPath = route.query.redirect || '/';
          
          // 如果是管理员用户，则重定向到管理仪表盘
          if (savedRole === 'admin') {
            console.log('检测到管理员用户，重定向到管理页面');
            router.push('/admin/dashboard');
          } else {
            console.log('重定向到:', redirectPath);
            router.push(redirectPath);
          }
        } catch (error) {
          console.error('登录错误:', error);
          ElMessage({
            type: 'error',
            message: typeof error === 'string' ? error : '登录失败，请重试'
          });
        } finally {
          loading.value = false;
        }
      });
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