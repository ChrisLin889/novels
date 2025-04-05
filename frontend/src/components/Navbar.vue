<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :router="true"
    @select="handleSelect"
  >
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/novels">小说列表</el-menu-item>
    <el-menu-item index="/rankings">排行榜</el-menu-item>
    
    <div class="flex-grow"></div>
    
    <template v-if="isLoggedIn">
      <el-sub-menu>
        <template #title>
          <el-avatar :size="32" :src="user?.avatar || defaultAvatar">
            {{ user?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <span class="username">
            {{ user?.username }}
            <el-tag v-if="isAuthor" size="small" type="success">作者</el-tag>
          </span>
        </template>
        <el-menu-item v-if="isAuthor" index="/author/center">作者中心</el-menu-item>
        <el-menu-item index="/user/profile">个人中心</el-menu-item>
        <el-menu-item @click="handleLogout">退出登录</el-menu-item>
      </el-sub-menu>
    </template>
    
    <template v-else>
      <el-menu-item index="/login">登录</el-menu-item>
      <el-menu-item index="/register">注册</el-menu-item>
    </template>
  </el-menu>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import defaultAvatar from '@/assets/default-avatar.png'

export default {
  name: 'Navbar',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isLoggedIn = computed(() => store.state.isLoggedIn)
    const user = computed(() => store.state.user?.user)
    const isAuthor = computed(() => store.getters.isAuthor)
    
    console.log('Navbar state:', {
      isLoggedIn: isLoggedIn.value,
      user: user.value,
      isAuthor: isAuthor.value
    })
    
    const handleLogout = async () => {
      try {
        await store.dispatch('logout')
        router.push('/login')
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
    
    return {
      isLoggedIn,
      user,
      isAuthor,
      defaultAvatar,
      handleLogout
    }
  }
}
</script>

<style scoped>
.el-menu-demo {
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.flex-grow {
  flex-grow: 1;
}

.username {
  margin-left: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-avatar {
  margin-right: 8px;
}
</style> 