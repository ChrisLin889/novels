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

    <!-- 作者申请部分 -->
    <div class="author-application-section" v-if="!isAuthor && !hasPendingApplication">
      <h3>作者申请</h3>
      <p>成为作者后，您可以发布自己的小说作品。</p>
      <el-button type="primary" @click="showAuthorApplicationDialog">申请成为作者</el-button>
    </div>

    <!-- 显示申请状态 -->
    <div class="author-application-section" v-if="hasPendingApplication">
      <h3>作者申请状态</h3>
      <el-alert
        :title="'您的申请正在审核中，提交时间：' + formatDate(latestApplication.created_at)"
        type="info"
        :closable="false"
      />
      <p v-if="latestApplication.status === 'rejected'">
        <strong>申请被拒绝</strong><br>
        拒绝原因: {{ latestApplication.admin_comment || '管理员未提供原因' }}<br>
        <el-button type="primary" @click="showAuthorApplicationDialog" style="margin-top: 10px;">重新申请</el-button>
      </p>
    </div>

    <!-- 作者申请对话框 -->
    <el-dialog
      title="申请成为作者"
      v-model="authorApplicationVisible"
      width="500px"
    >
      <el-form
        ref="authorApplicationFormRef"
        :model="authorApplicationForm"
        :rules="authorApplicationRules"
        label-width="100px"
      >
        <el-form-item label="笔名" prop="pen_name">
          <el-input v-model="authorApplicationForm.pen_name" placeholder="请输入您的笔名"></el-input>
        </el-form-item>
        
        <el-form-item label="作者简介" prop="bio">
          <el-input
            v-model="authorApplicationForm.bio"
            type="textarea"
            :rows="4"
            placeholder="请简要介绍自己的创作经历和风格"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="申请理由" prop="reason">
          <el-input
            v-model="authorApplicationForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请说明您为什么想成为作者"
          ></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="authorApplicationVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAuthorApplication" :loading="submittingApplication">提交申请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';
import { getAuthorApplications } from '@/api/author';
import * as authorApi from '@/api/author';

export default {
  name: 'UserProfile',
  setup() {
    const store = useStore();
    const profileFormRef = ref(null);
    const authorApplicationFormRef = ref(null);
    const loading = ref(false);
    const submittingApplication = ref(false);
    const authorApplicationVisible = ref(false);
    const applications = ref([]);
    const hasPendingApplication = ref(false);
    const latestApplication = ref(null);
    
    const userInfo = computed(() => store.getters['user/userInfo'] || {});
    const isAuthor = computed(() => {
      const userData = localStorage.getItem('user');
      try {
        const user = userData ? JSON.parse(userData) : null;
        return user && user.role === 'author';
      } catch (e) {
        console.error('解析用户数据失败:', e);
        return false;
      }
    });
    
    const profileForm = reactive({
      username: '',
      email: '',
      phone: '',
      avatar: ''
    });
    
    const authorApplicationForm = reactive({
      pen_name: '',
      bio: '',
      reason: ''
    });
    
    const authorApplicationRules = {
      pen_name: [
        { required: true, message: '请输入笔名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      bio: [
        { required: true, message: '请输入作者简介', trigger: 'blur' },
        { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
      ],
      reason: [
        { required: true, message: '请输入申请理由', trigger: 'blur' },
        { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
      ]
    };
    
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
      
      // 获取作者申请历史
      fetchAuthorApplications();
    });
    
    // 获取作者申请历史
    const fetchAuthorApplications = async () => {
      try {
        const res = await getAuthorApplications();
        if (res && res.applications) {
          applications.value = res.applications;
          
          // 检查是否有待处理的申请
          const pendingApp = applications.value.find(app => app.status === 'pending');
          hasPendingApplication.value = !!pendingApp;
          
          // 获取最新的申请
          if (applications.value.length > 0) {
            latestApplication.value = applications.value.sort((a, b) => 
              new Date(b.created_at) - new Date(a.created_at)
            )[0];
          }
        }
      } catch (error) {
        console.error('获取作者申请历史失败:', error);
      }
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 显示作者申请对话框
    const showAuthorApplicationDialog = () => {
      authorApplicationVisible.value = true;
      // 如果有之前的申请记录，填充表单
      if (latestApplication.value) {
        authorApplicationForm.pen_name = latestApplication.value.pen_name || '';
        authorApplicationForm.bio = latestApplication.value.bio || '';
        authorApplicationForm.reason = '';  // 申请理由需要重新填写
      }
    };
    
    // 提交作者申请
    const submitAuthorApplication = async () => {
      if (!authorApplicationFormRef.value) return;
      
      await authorApplicationFormRef.value.validate(async (valid) => {
        if (!valid) return;
        
        submittingApplication.value = true;
        
        try {
          await authorApi.submitAuthorApplication(authorApplicationForm);
          
          ElMessage({
            type: 'success',
            message: '作者申请提交成功，请等待管理员审核'
          });
          
          authorApplicationVisible.value = false;
          await fetchAuthorApplications();  // 刷新申请历史
        } catch (error) {
          ElMessage({
            type: 'error',
            message: error.message || '申请提交失败，请重试'
          });
        } finally {
          submittingApplication.value = false;
        }
      });
    };
    
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
      updateProfile,
      isAuthor,
      authorApplicationForm,
      authorApplicationFormRef,
      authorApplicationRules,
      authorApplicationVisible,
      showAuthorApplicationDialog,
      submitAuthorApplication,
      submittingApplication,
      hasPendingApplication,
      latestApplication,
      formatDate
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

.author-application-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.author-application-section h3 {
  margin-bottom: 15px;
}
</style> 