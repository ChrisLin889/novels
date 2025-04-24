<template>
  <div class="navbar">
    <div class="nav-container">
      <!-- 标题居中 -->
      <div class="logo-container">
        <router-link to="/">
          <h1 class="logo">小说网站</h1>
        </router-link>
      </div>
      
      <!-- 左侧用户区域 -->
      <div class="nav-left">
        <template v-if="isLoggedIn">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="user-profile">
              <el-avatar :size="32" class="user-avatar">{{ userName.charAt(0) }}</el-avatar>
              <span>{{ userName }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item v-if="isAdmin" command="admin">管理后台</el-dropdown-item>
                <el-dropdown-item v-if="isAuthor" command="author">作家中心</el-dropdown-item>
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
      
      <!-- 右侧搜索区域 -->
      <div class="nav-right">
        <div class="nav-search">
          <el-input
            v-model="searchText"
            placeholder="搜索小说标题或作者"
            @keyup.enter="handleSearch"
            clearable
            size="small"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>
    
    <!-- 下方导航区域 -->
    <div class="nav-menu">
      <div class="nav-menu-container">
        <router-link to="/" class="nav-item" :class="{ active: activeIndex === '/' }">首页</router-link>
        <router-link to="/category" class="nav-item" :class="{ active: activeIndex === '/category' }">分类</router-link>
        <router-link to="/ranking" class="nav-item" :class="{ active: activeIndex === '/ranking' }">排行榜</router-link>
        
        <!-- 登录后显示的导航项 -->
        <template v-if="isLoggedIn">
          <router-link to="/user/bookshelf" class="nav-item" :class="{ active: activeIndex === '/user/bookshelf' }">我的书架</router-link>
          <router-link to="/user/messages" class="nav-item" :class="{ active: activeIndex === '/user/messages' }">
            我的消息
            <el-badge v-if="unreadCount > 0" :value="unreadCount" class="message-badge" />
          </router-link>
          <router-link to="/user/following" class="nav-item" :class="{ active: activeIndex === '/user/following' }">我关注的</router-link>
          <router-link to="/user/followers" class="nav-item" :class="{ active: activeIndex === '/user/followers' }">我的粉丝</router-link>
          <router-link to="/user/comments" class="nav-item" :class="{ active: activeIndex === '/user/comments' }">我的评论</router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
import { Search } from '@element-plus/icons-vue';

export default {
  name: 'NavBar',
  components: {
    Search
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    
    const searchText = ref('');
    const unreadCount = ref(0);
    
    // Compute active menu item based on current route
    const activeIndex = computed(() => {
      return route.path;
    });
    
    // User auth state - 直接从 localStorage 读取
    const isLoggedIn = computed(() => {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      console.log('NavBar - 当前登录状态:', !!token && !!user);
      console.log('NavBar - localStorage token:', token);
      console.log('NavBar - localStorage user:', user);
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
    
    const userInfo = computed(() => {
      try {
        const userData = localStorage.getItem('user');
        return userData ? JSON.parse(userData) : null;
      } catch (e) {
        console.error('NavBar - 解析用户数据失败:', e);
        return null;
      }
    });
    
    const userName = computed(() => {
      return userInfo.value?.email || userInfo.value?.username || '用户';
    });
    
    const userAvatar = computed(() => userInfo.value?.avatar || '');
    const isAdmin = computed(() => userInfo.value?.role === 'admin');
    const isAuthor = computed(() => userInfo.value?.role === 'author');
    
    // 获取未读消息数量
    const fetchUnreadCount = async () => {
      if (isLoggedIn.value) {
        try {
          await store.dispatch('interaction/fetchInbox', { page: 1, per_page: 5 });
          unreadCount.value = store.getters['interaction/unreadCount'];
        } catch (error) {
          console.error('获取未读消息失败:', error);
        }
      }
    };
    
    // Methods
    const handleSearch = () => {
      if (searchText.value.trim()) {
        router.push({
          path: '/search',
          query: { keyword: searchText.value.trim() }
        });
      }
    };
    
    const goToLogin = () => {
      router.push('/login');
    };
    
    const goToRegister = () => {
      router.push('/register');
    };
    
    const handleCommand = (command) => {
      if (command === 'logout') {
        store.dispatch('user/clearUser');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        router.push('/login');
      } else if (command === 'profile') {
        router.push('/user/profile');
      } else if (command === 'admin') {
        router.push('/admin/dashboard');
      } else if (command === 'author') {
        router.push('/author/center');
      }
    };
    
    // 监听登录状态变化
    watch(() => isLoggedIn.value, (newVal) => {
      if (newVal) {
        fetchUnreadCount();
      } else {
        unreadCount.value = 0;
      }
    });
    
    onMounted(() => {
      if (isLoggedIn.value) {
        fetchUnreadCount();
      }
      
      // 定时刷新未读消息数（每5分钟）
      const intervalId = setInterval(fetchUnreadCount, 5 * 60 * 1000);
      
      // 组件销毁时清除定时器
      return () => {
        clearInterval(intervalId);
      };
    });
    
    return {
      searchText,
      activeIndex,
      isLoggedIn,
      userName,
      userAvatar,
      unreadCount,
      isAdmin,
      isAuthor,
      handleSearch,
      goToLogin,
      goToRegister,
      handleCommand
    };
  }
};
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: #fff;
}

.nav-container {
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-left {
  display: flex;
  align-items: center;
  position: absolute;
  left: 20px;
}

.logo-container {
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;
  width: max-content;
  text-align: center;
}

.logo {
  color: #409EFF;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.nav-right {
  display: flex;
  align-items: center;
  position: absolute;
  right: 20px;
}

.nav-search {
  max-width: 200px;
  margin-left: auto;
}

.nav-menu {
  background-color: #f5f7fa;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-menu-container {
  display: flex;
  justify-content: center;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-item {
  padding: 0 20px;
  height: 48px;
  line-height: 48px;
  color: #333;
  font-size: 16px;
  text-decoration: none;
  position: relative;
  transition: all 0.3s;
}

.nav-item:hover {
  color: #409EFF;
}

.nav-item.active {
  color: #409EFF;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #409EFF;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
}

.user-profile span {
  margin-left: 8px;
}

.user-avatar {
  border-radius: 50%;
  border: 2px solid var(--primary-light);
}

.mobile-only {
  display: none;
  text-decoration: none;
  color: #333;
  margin-left: 15px;
}

/* Responsive styles */
@media (max-width: 768px) {
  .logo {
    font-size: 20px;
  }
  
  .nav-menu-container {
    justify-content: space-around;
  }
  
  .nav-item {
    padding: 0 10px;
    font-size: 14px;
  }
  
  .mobile-only {
    display: block;
  }
  
  .nav-search {
    max-width: 150px;
  }
}

.message-badge {
  margin-left: 8px;
}
</style> 