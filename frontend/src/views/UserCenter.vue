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
            <el-menu-item index="/user/history">
              <i class="el-icon-time"></i>
              <span>阅读历史</span>
            </el-menu-item>
            <el-menu-item index="/user/comments">
              <i class="el-icon-chat-line-round"></i>
              <span>我的评论</span>
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
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'UserCenter',
  setup() {
    const route = useRoute();
    const store = useStore();
    
    const userInfo = computed(() => store.getters['user/userInfo']);
    const userName = computed(() => userInfo.value?.username || '用户');
    const userAvatar = computed(() => userInfo.value?.avatar || '');
    
    const activeMenu = computed(() => route.path);
    
    return {
      userName,
      userAvatar,
      activeMenu
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