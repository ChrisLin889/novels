<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'is-collapsed': isCollapsed }">
      <div class="sidebar-header">
        <div class="logo-container">
          <h1 v-if="!isCollapsed" class="logo-text">Novel<span>Admin</span></h1>
          <h1 v-else class="logo-icon">N</h1>
        </div>
      </div>
      
      <el-menu
        class="sidebar-menu"
        :collapse="isCollapsed"
        :default-active="activeMenu"
        :router="true"
        background-color="#1e293b"
        text-color="#e2e8f0"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        
        <el-sub-menu index="users">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/admin/users">
            <el-icon><UserFilled /></el-icon>
            <span>用户列表</span>
          </el-menu-item>
          <el-menu-item index="/admin/user-actions">
            <el-icon><List /></el-icon>
            <span>用户行为</span>
          </el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="content">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>内容管理</span>
          </template>
          <el-menu-item index="/admin/sensitive-words">
            <el-icon><Warning /></el-icon>
            <span>敏感词管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/content">
            <el-icon><Reading /></el-icon>
            <span>内容审核</span>
          </el-menu-item>
          <el-menu-item index="/admin/crawled-novels">
            <el-icon><Download /></el-icon>
            <span>爬取小说</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
      <!-- Header -->
      <div class="header">
        <div class="left-section">
          <el-button 
            type="text" 
            @click="toggleSidebar" 
            class="sidebar-toggle"
          >
            <el-icon v-if="isCollapsed"><Expand /></el-icon>
            <el-icon v-else><Fold /></el-icon>
          </el-button>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">管理后台</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="right-section">
          <el-dropdown @command="handleNotification" class="notification-dropdown">
            <el-badge :value="3" class="notification-badge">
              <el-button type="text" class="notification-button">
                <el-icon><Bell /></el-icon>
              </el-button>
            </el-badge>
            <template #dropdown>
              <el-dropdown-menu>
                <div class="notification-header">
                  <span>通知</span>
                  <el-button type="text" size="small">标记全部已读</el-button>
                </div>
                <div class="empty-notifications" v-if="!hasNotifications">
                  暂无通知
                </div>
                <template v-else>
                  <el-dropdown-item>新的用户注册</el-dropdown-item>
                  <el-dropdown-item>新的内容待审核</el-dropdown-item>
                </template>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <el-dropdown @command="handleCommand" class="user-dropdown">
            <div class="user-info">
              <el-avatar size="small" :src="userAvatar" class="user-avatar">
                {{ username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username" v-if="!isCollapsed">{{ username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="settings">设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- Page Content -->
      <div class="page-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import { 
  Document, 
  UserFilled, 
  User, 
  Reading, 
  Warning, 
  Download, 
  Fold, 
  Expand, 
  Bell, 
  DataLine,
  List,
  ArrowDown
} from '@element-plus/icons-vue';
import { ElMessageBox } from 'element-plus';

export default {
  name: 'AdminLayout',
  components: {
    Document, 
    UserFilled, 
    User, 
    Reading, 
    Warning, 
    Download, 
    Fold, 
    Expand, 
    Bell, 
    DataLine,
    List,
    ArrowDown
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    
    const isCollapsed = ref(false);
    const hasNotifications = ref(false);
    
    // 获取当前激活的菜单项
    const activeMenu = computed(() => {
      return route.path;
    });
    
    // 获取当前页面标题
    const currentPageTitle = computed(() => {
      const routePath = route.path;
      
      if (routePath.includes('/admin/dashboard')) return '仪表盘';
      if (routePath.includes('/admin/users')) return '用户列表';
      if (routePath.includes('/admin/user-actions')) return '用户行为';
      if (routePath.includes('/admin/sensitive-words')) return '敏感词管理';
      if (routePath.includes('/admin/content')) return '内容审核';
      if (routePath.includes('/admin/crawled-novels')) return '爬取小说';
      
      return '管理后台';
    });
    
    // 获取用户名
    const username = computed(() => {
      return store.getters['user/username'] || '管理员';
    });
    
    // 获取用户头像
    const userAvatar = computed(() => {
      return store.getters['user/avatar'] || '';
    });
    
    // 切换侧边栏
    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value;
    };
    
    // 处理通知点击
    const handleNotification = (command) => {
      // 处理通知点击
      console.log('Notification clicked:', command);
    };
    
    // 处理下拉菜单命令
    const handleCommand = (command) => {
      if (command === 'profile') {
        router.push('/profile');
      } else if (command === 'settings') {
        router.push('/admin/settings');
      } else if (command === 'logout') {
        ElMessageBox.confirm('确定要退出登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.dispatch('user/logout');
          router.push('/login');
        }).catch(() => {});
      }
    };
    
    return {
      isCollapsed,
      hasNotifications,
      activeMenu,
      currentPageTitle,
      username,
      userAvatar,
      toggleSidebar,
      handleNotification,
      handleCommand
    };
  }
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f0f2f5;
}

/* Sidebar Styles */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 240px;
  background-color: #1e293b;
  transition: width 0.3s ease;
  z-index: 1000;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar.is-collapsed {
  width: 64px;
}

.sidebar-header {
  height: 60px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.logo-text span {
  color: #6366f1;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #6366f1;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(99, 102, 241, 0.1);
  border-radius: 8px;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu :deep(.el-menu-item),
.sidebar-menu :deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: #334155;
}

.sidebar-menu :deep(.el-sub-menu__title:hover),
.sidebar-menu :deep(.el-menu-item:hover) {
  background-color: #334155;
}

.sidebar-menu :deep(.el-menu-item .el-icon),
.sidebar-menu :deep(.el-sub-menu__title .el-icon) {
  margin-right: 12px;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  margin-left: 240px;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
  max-width: 100%;
}

.sidebar.is-collapsed ~ .main-content {
  margin-left: 64px;
}

/* Header Styles */
.header {
  height: 60px;
  background-color: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 999;
}

.left-section {
  display: flex;
  align-items: center;
}

.sidebar-toggle {
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  color: #64748b;
}

.sidebar-toggle:hover {
  color: #334155;
  background-color: #f1f5f9;
  border-radius: 6px;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* Dropdown Styles */
.notification-dropdown {
  margin-right: 8px;
}

.notification-button {
  height: 40px;
  width: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.notification-button:hover {
  color: #334155;
  background-color: #f1f5f9;
  border-radius: 6px;
}

.notification-badge :deep(.el-badge__content) {
  background-color: #6366f1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.notification-header span {
  font-weight: 600;
  color: #334155;
}

.empty-notifications {
  padding: 16px;
  text-align: center;
  color: #94a3b8;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: #f1f5f9;
}

.user-avatar {
  background-color: #6366f1;
  color: white;
  font-weight: 600;
}

.username {
  font-size: 14px;
  color: #334155;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Page Content Styles */
.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style> 