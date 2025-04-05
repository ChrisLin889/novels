<template>
  <div class="user-center container page-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="sidebar-container">
          <div class="user-info">
            <el-avatar :size="80" :src="userAvatar"></el-avatar>
            <h3>{{ userName }}</h3>
          </div>
          <el-menu
            :default-active="activeMenu"
            class="sidebar-menu"
            router
          >
            <el-menu-item index="/user/profile">
              <i class="el-icon-user"></i>
              <span>个人资料</span>
            </el-menu-item>
            <el-menu-item index="/user/bookshelf">
              <i class="el-icon-collection"></i>
              <span>我的书架</span>
            </el-menu-item>
            <el-menu-item index="/user/messages">
              <i class="el-icon-message"></i>
              <span>我的消息</span>
              <el-badge v-if="unreadCount > 0" :value="unreadCount" class="message-badge" />
            </el-menu-item>
            <el-menu-item index="/user/following">
              <i class="el-icon-star-on"></i>
              <span>我关注的</span>
            </el-menu-item>
            <el-menu-item index="/user/followers">
              <i class="el-icon-connection"></i>
              <span>我的粉丝</span>
            </el-menu-item>
            <el-menu-item index="/user/comments">
              <i class="el-icon-chat-line-round"></i>
              <span>我的评论</span>
            </el-menu-item>
            <el-menu-item v-if="isAdmin" index="/admin/dashboard">
              <i class="el-icon-setting"></i>
              <span>管理后台</span>
            </el-menu-item>
            <el-menu-item v-if="isAuthor" index="/author/center">
              <i class="el-icon-edit-outline"></i>
              <span>作家中心</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-col>
      <el-col :span="18">
        <div class="content-container">
          <router-view></router-view>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'UserCenter',
  setup() {
    const route = useRoute();
    const store = useStore();
    
    const userName = computed(() => store.getters['user/username']);
    const userAvatar = computed(() => store.getters['user/avatar']);
    const unreadCount = ref(0);
    
    // 获取用户角色
    const userInfo = computed(() => {
      try {
        const userData = localStorage.getItem('user');
        return userData ? JSON.parse(userData) : null;
      } catch (e) {
        console.error('UserCenter - 解析用户数据失败:', e);
        return null;
      }
    });
    
    const isAdmin = computed(() => userInfo.value?.role === 'admin');
    const isAuthor = computed(() => userInfo.value?.role === 'author');
    
    const activeMenu = computed(() => route.path);
    
    // 获取未读消息数量
    const fetchUnreadCount = async () => {
      try {
        await store.dispatch('interaction/fetchInbox', { page: 1, per_page: 5 });
        unreadCount.value = store.getters['interaction/unreadCount'];
      } catch (error) {
        console.error('获取未读消息失败:', error);
      }
    };
    
    onMounted(() => {
      console.log('UserCenter mounted - 用户信息:', store.getters['user/userInfo']);
      console.log('UserCenter - 用户名:', userName.value);
      console.log('UserCenter - 头像:', userAvatar.value);
      console.log('UserCenter - 用户角色:', userInfo.value?.role);
      fetchUnreadCount();
    });
    
    return {
      userName,
      userAvatar,
      activeMenu,
      isAdmin,
      isAuthor,
      unreadCount
    };
  }
};
</script>

<style scoped>
.sidebar-container {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.user-info {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}

.user-info h3 {
  margin: 10px 0 0;
  font-size: 18px;
}

.sidebar-menu {
  border-right: none;
}

.content-container {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  min-height: 500px;
}
</style> 