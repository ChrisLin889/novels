<template>
  <div class="user-profile">
    <h2>个人资料</h2>
    
    <el-form 
      ref="profileFormRef"
      :model="profileForm" 
      :rules="rules" 
      label-width="100px"
      @submit.prevent="updateProfile"
    >
      <el-form-item label="用户名" prop="username">
        <el-input v-model="profileForm.username"></el-input>
      </el-form-item>
      
      <el-form-item label="邮箱">
        <el-input v-model="profileForm.email" disabled></el-input>
      </el-form-item>
      
      <el-form-item label="手机号">
        <el-input v-model="profileForm.phone" disabled></el-input>
      </el-form-item>
      
      <el-form-item label="头像">
        <el-upload
          class="avatar-uploader"
          action="#"
          :show-file-list="false"
          :auto-upload="false"
          :on-change="onAvatarChange"
        >
          <img v-if="avatarUrl" :src="avatarUrl" class="avatar" />
          <el-button v-else type="primary">点击上传</el-button>
        </el-upload>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  name: 'UserProfile',
  setup() {
    const store = useStore();
    const profileFormRef = ref(null);
    const loading = ref(false);
    
    const userInfo = computed(() => store.getters['user/userInfo'] || {});
    
    const profileForm = reactive({
      username: '',
      email: '',
      phone: '',
      avatar: ''
    });
    
    const avatarUrl = ref('');
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ]
    };
    
    // Initialize form with user data
    onMounted(() => {
      console.log('UserProfile mounted - store中的用户信息:', userInfo.value);
      
      // 尝试直接从localStorage获取用户信息
      try {
        const localUserData = localStorage.getItem('user');
        if (localUserData) {
          const userData = JSON.parse(localUserData);
          console.log('UserProfile - localStorage中的用户信息:', userData);
          
          // 使用localStorage的用户数据初始化表单
          profileForm.username = userData.username || '';
          profileForm.email = userData.email || '';
          profileForm.phone = userData.phone || '';
          profileForm.avatar = userData.avatar || '';
          avatarUrl.value = userData.avatar || '';
          
          // 确保store中也有这些数据
          store.dispatch('user/setUser', userData);
        } else {
          console.log('UserProfile - localStorage中没有用户数据');
          
          // 回退到使用store中的数据
          if (userInfo.value) {
            profileForm.username = userInfo.value.username || '';
            profileForm.email = userInfo.value.email || '';
            profileForm.phone = userInfo.value.phone || '';
            profileForm.avatar = userInfo.value.avatar || '';
            avatarUrl.value = userInfo.value.avatar || '';
          }
        }
      } catch (e) {
        console.error('UserProfile - 解析localStorage用户数据失败:', e);
        
        // 回退到使用store中的数据
        if (userInfo.value) {
          profileForm.username = userInfo.value.username || '';
          profileForm.email = userInfo.value.email || '';
          profileForm.phone = userInfo.value.phone || '';
          profileForm.avatar = userInfo.value.avatar || '';
          avatarUrl.value = userInfo.value.avatar || '';
        }
      }
    });
    
    // Avatar upload handler
    const onAvatarChange = (file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarUrl.value = e.target.result;
        profileForm.avatar = e.target.result;
      };
      reader.readAsDataURL(file.raw);
    };
    
    // Update profile handler
    const updateProfile = async () => {
      if (!profileFormRef.value) return;
      
      await profileFormRef.value.validate(async (valid) => {
        if (!valid) return;
        
        loading.value = true;
        
        try {
          await store.dispatch('user/updateProfile', {
            username: profileForm.username,
            avatar: profileForm.avatar
          });
          
          ElMessage({
            type: 'success',
            message: '个人资料更新成功'
          });
        } catch (error) {
          ElMessage({
            type: 'error',
            message: error || '更新失败，请重试'
          });
        } finally {
          loading.value = false;
        }
      });
    };
    
    return {
      profileForm,
      profileFormRef,
      rules,
      loading,
      avatarUrl,
      onAvatarChange,
      updateProfile
    };
  }
};
</script>

<style scoped>
.user-profile h2 {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.avatar-uploader {
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style> 