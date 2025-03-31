<template>
  <div class="followers-page">
    <div class="page-header">
      <h1 class="page-title">我的粉丝</h1>
    </div>

    <div class="followers-container">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="followers.length === 0" class="empty-container">
        <el-empty description="暂无粉丝">
          <template #description>
            <p>还没有用户关注您</p>
          </template>
        </el-empty>
      </div>

      <div v-else class="followers-list">
        <el-row :gutter="20">
          <el-col v-for="user in followers" :key="user.id" :xs="24" :sm="12" :md="8" :lg="6">
            <div class="user-card">
              <div class="user-card-header">
                <el-avatar :size="60" :src="user.avatar">
                  {{ getInitials(user.username) }}
                </el-avatar>
                <div class="user-info">
                  <div class="username" @click="navigateToUser(user.id)">{{ user.username }}</div>
                  <div class="user-stats">
                    <span>{{ user.novels_count || 0 }} 部作品</span>
                    <span>{{ user.following_count || 0 }} 关注</span>
                  </div>
                </div>
              </div>
              <div class="user-bio" v-if="user.bio">{{ user.bio }}</div>
              <div class="user-actions">
                <el-button 
                  :type="user.is_following ? 'default' : 'primary'" 
                  size="small" 
                  @click="toggleFollow(user)"
                >
                  {{ user.is_following ? '已关注' : '关注' }}
                </el-button>
                <el-button type="default" size="small" @click="sendMessage(user.id)">发送私信</el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div v-if="totalFollowers > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next"
          :total="totalFollowers"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  name: 'UserFollowers',
  setup() {
    const store = useStore();
    const router = useRouter();
    const currentPage = ref(1);
    const pageSize = ref(20);

    // 从store获取数据
    const followers = computed(() => store.getters['interaction/followers']);
    const totalFollowers = computed(() => store.getters['interaction/totalFollowers']);
    const loading = computed(() => store.getters['interaction/followersLoading']);

    // 获取粉丝列表
    const fetchFollowers = async () => {
      try {
        await store.dispatch('interaction/fetchFollowers', {
          userId: store.getters['user/userInfo'].id,
          page: currentPage.value,
          per_page: pageSize.value
        });
      } catch (error) {
        ElMessage.error('获取粉丝列表失败，请稍后重试');
      }
    };

    // 切换关注状态
    const toggleFollow = async (user) => {
      try {
        if (user.is_following) {
          const response = await store.dispatch('interaction/unfollow', { userId: user.id });
          if (!response.is_following) {
            user.is_following = false;
            ElMessage.success('已取消关注');
          }
        } else {
          const response = await store.dispatch('interaction/follow', { 
            userId: user.id,
            userData: user
          });
          if (response.is_following) {
            user.is_following = true;
            ElMessage.success('关注成功');
          }
        }
      } catch (error) {
        ElMessage.error('操作失败，请稍后重试');
      }
    };

    // 发送私信
    const sendMessage = (userId) => {
      router.push(`/user/conversation/${userId}`);
    };

    // 查看用户主页
    const navigateToUser = (userId) => {
      router.push(`/user/${userId}`);
    };

    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page;
      fetchFollowers();
    };

    // 获取用户名首字母
    const getInitials = (username) => {
      if (!username) return '?';
      return username.charAt(0).toUpperCase();
    };

    onMounted(() => {
      fetchFollowers();
    });

    return {
      followers,
      totalFollowers,
      loading,
      currentPage,
      pageSize,
      toggleFollow,
      sendMessage,
      navigateToUser,
      handlePageChange,
      getInitials
    };
  }
};
</script>

<style scoped>
.followers-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}

.page-title {
  font-size: 1.8rem;
  color: #303133;
  margin: 0;
}

.followers-container {
  padding: 20px 0;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.followers-list {
  margin-bottom: 20px;
}

.user-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
}

.user-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-info {
  margin-left: 15px;
  flex: 1;
}

.username {
  font-weight: bold;
  font-size: 1.1rem;
  color: #303133;
  margin-bottom: 5px;
  cursor: pointer;
}

.username:hover {
  color: #409eff;
  text-decoration: underline;
}

.user-stats {
  font-size: 0.9rem;
  color: #606266;
}

.user-stats span {
  margin-right: 10px;
}

.user-bio {
  font-size: 0.9rem;
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.user-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.user-actions .el-button {
  flex: 1;
  margin: 0 5px;
}

.user-actions .el-button:first-child {
  margin-left: 0;
}

.user-actions .el-button:last-child {
  margin-right: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .followers-page {
    padding: 10px;
  }
  
  .user-card {
    padding: 15px;
  }
  
  .user-actions {
    flex-direction: column;
  }
  
  .user-actions .el-button {
    margin: 5px 0;
  }
}
</style> 