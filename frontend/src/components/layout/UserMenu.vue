<template>
  <div class="user-menu">
    <template v-if="isLoggedIn">
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="user-profile">
          <el-avatar :size="32" class="user-avatar">{{ displayName.charAt(0) }}</el-avatar>
          <span class="username">{{ displayName }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item v-if="isAuthor" command="author">作者中心</el-dropdown-item>
            <el-dropdown-item v-if="isAdmin" command="admin">管理后台</el-dropdown-item>
            <el-dropdown-item command="bookshelf">我的书架</el-dropdown-item>
            <el-dropdown-item command="following">我关注的</el-dropdown-item>
            <el-dropdown-item command="followers">我的粉丝</el-dropdown-item>
            <el-dropdown-item command="comments">我的评论</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </template>
    <template v-else>
      <el-button type="text" @click="goToLogin">登录</el-button>
      <el-button type="primary" @click="goToRegister">注册</el-button>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'UserMenu',
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // 登录状态 - 直接从 localStorage 读取
    const isLoggedIn = computed(() => {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      const userRole = localStorage.getItem('userRole');
      console.log('UserMenu - 当前登录状态:', !!token && !!user, '用户角色:', userRole);
      
      // 刷新用户状态到 store
      if (token && user) {
        try {
          const userData = JSON.parse(user);
          store.dispatch('user/setUser', userData);
          return true;
        } catch (e) {
          console.error('解析用户数据失败:', e);
          return false;
        }
      }
      return false;
    });
    
    // 用户信息从 localStorage 读取
    const userInfo = computed(() => {
      try {
        const userData = localStorage.getItem('user');
        const parsedData = userData ? JSON.parse(userData) : null;
        console.log('UserMenu - 用户信息:', parsedData);
        return parsedData;
      } catch (e) {
        console.error('UserMenu - 解析用户数据失败:', e);
        return null;
      }
    });
    
    // 角色判断
    const isAdmin = computed(() => {
      const role = userInfo.value?.role;
      const directRole = localStorage.getItem('userRole');
      console.log('UserMenu - 是否管理员:', role === 'admin', '直接角色:', directRole);
      return role === 'admin' || directRole === 'admin';
    });
    
    const isAuthor = computed(() => {
      const role = userInfo.value?.role;
      const directRole = localStorage.getItem('userRole');
      console.log('UserMenu - 是否作者:', role === 'author', '直接角色:', directRole);
      return role === 'author' || directRole === 'author';
    });
    
    // 显示名称
    const displayName = computed(() => {
      return userInfo.value?.email || userInfo.value?.username || '用户';
    });
    
    // 导航方法
    const goToLogin = () => router.push('/login');
    const goToRegister = () => router.push('/register');
    
    // 菜单命令处理
    const handleCommand = (command) => {
      if (command === 'logout') {
        // 清除用户状态
        store.dispatch('user/clearUser');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('userRole');
        router.push('/login');
      } else if (command === 'profile') {
        router.push('/user/profile');
      } else if (command === 'admin') {
        console.log('点击了管理后台，即将导航到 /admin/dashboard');
        router.push('/admin/dashboard');
      } else if (command === 'author') {
        console.log('点击了作者中心，即将导航到 /author');
        router.push('/author');
      } else if (command === 'bookshelf') {
        router.push('/user/bookshelf');
      } else if (command === 'following') {
        router.push('/user/following');
      } else if (command === 'followers') {
        router.push('/user/followers');
      } else if (command === 'comments') {
        router.push('/user/comments');
      }
    };
    
    // 组件挂载时检查登录状态
    onMounted(() => {
      console.log('UserMenu 组件挂载 - 检查登录状态');
    });
    
    return {
      isLoggedIn,
      userInfo,
      displayName,
      isAdmin,
      isAuthor,
      goToLogin,
      goToRegister,
      handleCommand
    };
  }
};
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 8px;
}

.username {
  margin-left: 8px;
  font-size: 14px;
}

.user-avatar {
  border: 2px solid var(--el-color-primary-light-3);
}
</style> 