<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>注册账号</h2>
        <p>加入我们，开始您的阅读之旅</p>
      </div>
      
      <el-form 
        ref="registerFormRef"
        :model="registerForm" 
        :rules="rules" 
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="registerForm.username" 
            placeholder="请输入用户名" 
          ></el-input>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="registerForm.email" 
            placeholder="请输入邮箱" 
          ></el-input>
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input 
            v-model="registerForm.phone" 
            placeholder="请输入手机号" 
          ></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码" 
            show-password
          ></el-input>
          <div class="password-requirements">
            <p>密码要求：至少8个字符，包含至少1个数字和1个大写字母</p>
          </div>
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码" 
            show-password
          ></el-input>
        </el-form-item>
        
        <div class="agreement">
          <el-checkbox v-model="agreeTerms">我已阅读并同意</el-checkbox>
          <el-link type="primary" href="#">《用户协议》</el-link>和
          <el-link type="primary" href="#">《隐私政策》</el-link>
        </div>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            class="register-button" 
            :loading="loading"
            :disabled="!agreeTerms"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-link">
        已有账号? <router-link to="/login">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

export default {
  name: 'Register',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    const registerForm = reactive({
      username: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: ''
    });
    
    // Form validation rules
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length < 8) {
        callback(new Error('密码长度至少为 8 个字符'));
      } else if (!/\d/.test(value)) {
        callback(new Error('密码必须包含至少1个数字'));
      } else if (!/[A-Z]/.test(value)) {
        callback(new Error('密码必须包含至少1个大写字母'));
      } else {
        if (registerForm.confirmPassword !== '') {
          // Force validate the confirmation password field when the password changes
          registerFormRef.value?.validateField('confirmPassword');
        }
        callback();
      }
    };
    
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== registerForm.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    
    const validateEmail = (rule, value, callback) => {
      if (value === '' && registerForm.phone === '') {
        callback(new Error('邮箱和手机号必须至少填写一项'));
      } else if (value !== '' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        callback(new Error('请输入正确的邮箱格式'));
      } else {
        callback();
      }
    };
    
    const validatePhone = (rule, value, callback) => {
      if (value === '' && registerForm.email === '') {
        callback(new Error('邮箱和手机号必须至少填写一项'));
      } else if (value !== '' && !/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号格式'));
      } else {
        callback();
      }
    };
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { validator: validateEmail, trigger: 'blur' }
      ],
      phone: [
        { validator: validatePhone, trigger: 'blur' }
      ],
      password: [
        { validator: validatePass, trigger: 'blur' }
      ],
      confirmPassword: [
        { validator: validatePass2, trigger: 'blur' }
      ]
    };
    
    const registerFormRef = ref(null);
    const loading = ref(false);
    const agreeTerms = ref(false);
    
    const handleRegister = async () => {
      if (!registerFormRef.value) return;
      
      await registerFormRef.value.validate(async (valid) => {
        if (!valid) return;
        
        if (!agreeTerms.value) {
          ElMessage({
            type: 'warning',
            message: '请先阅读并同意用户协议和隐私政策'
          });
          return;
        }
        
        loading.value = true;
        
        try {
          // Create registration data object
          const registerData = {
            username: registerForm.username,
            password: registerForm.password
          };
          
          // Add email or phone if provided
          if (registerForm.email) {
            registerData.email = registerForm.email;
          }
          
          if (registerForm.phone) {
            registerData.phone = registerForm.phone;
          }
          
          // Call the registration API
          await store.dispatch('user/register', registerData);
          
          ElMessage({
            type: 'success',
            message: '注册成功，请登录'
          });
          
          // Redirect to login page
          router.push('/login');
        } catch (error) {
          ElMessage({
            type: 'error',
            message: error || '注册失败，请重试'
          });
        } finally {
          loading.value = false;
        }
      });
    };
    
    return {
      registerForm,
      registerFormRef,
      rules,
      loading,
      agreeTerms,
      handleRegister
    };
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 500px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 10px;
}

.register-header p {
  color: #909399;
  font-size: 14px;
}

.agreement {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
  font-size: 14px;
  color: #606266;
}

.register-button {
  width: 100%;
  padding: 12px 0;
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.login-link a {
  color: #409EFF;
  text-decoration: none;
}

.password-requirements {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}
</style> 