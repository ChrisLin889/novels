<template>
  <div class="nav-bar">
    <div class="nav-left">
      <router-link to="/" class="logo">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img">
        <span class="logo-text">小说阅读</span>
      </router-link>
    </div>
    
    <div class="nav-center">
      <el-menu mode="horizontal" :router="true">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/novels">小说列表</el-menu-item>
        <el-menu-item index="/about">关于我们</el-menu-item>
        <!-- 登录后显示的导航项 -->
        <template v-if="isLoggedIn">
          <el-menu-item index="/user/bookshelf">我的书架</el-menu-item>
          <el-menu-item index="/user/following">我关注的</el-menu-item>
          <el-menu-item index="/user/followers">我的粉丝</el-menu-item>
          <el-menu-item index="/user/comments">我的评论</el-menu-item>
        </template>
      </el-menu>
    </div>
    
    <div class="nav-right">
      <user-menu />
    </div>
  </div>
</template>

<script>
import UserMenu from './UserMenu.vue';
import { computed } from 'vue';

export default {
  name: 'NavBar',
  components: {
    UserMenu
  },
  setup() {
    // 判断用户是否登录
    const isLoggedIn = computed(() => {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      return !!token && !!user;
    });

    return {
      isLoggedIn
    };
  }
};
</script>

<style scoped>
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--primary-color);
}

.logo-img {
  height: 32px;
  margin-right: 8px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
}

.nav-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

:deep(.el-menu) {
  border-bottom: none;
}

:deep(.el-menu-item) {
  height: 60px;
  line-height: 60px;
}
</style> 