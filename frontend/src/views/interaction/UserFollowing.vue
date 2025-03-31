<template>
  <div class="following-page">
    <div class="page-header">
      <h1 class="page-title">我的关注</h1>
    </div>

    <div class="following-container">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="following.length === 0" class="empty-container">
        <el-empty description="暂无关注的用户">
          <template #description>
            <p>您还没有关注任何用户</p>
          </template>
        </el-empty>
      </div>

      <div v-else class="following-list">
        <el-row :gutter="20">
          <el-col v-for="user in following" :key="user.id" :xs="24" :sm="12" :md="8" :lg="6">
            <div class="user-card">
              <div class="user-card-header">
                <el-avatar :size="60" :src="user.avatar">
                  {{ getInitials(user.username) }}
                </el-avatar>
                <div class="user-info">
                  <div class="username" @click="navigateToUser(user.id)">{{ user.username }}</div>
                  <div class="user-stats">
                    <span>{{ user.novels_count || 0 }} 部作品</span>
                    <span>{{ user.followers_count || 0 }} 粉丝</span>
                  </div>
                </div>
              </div>
              <div class="user-bio" v-if="user.bio">{{ user.bio }}</div>
              <div class="user-actions">
                <el-button type="primary" size="small" @click="unfollowUser(user.id)">取消关注</el-button>
                <el-button type="default" size="small" @click="sendMessage(user.id)">发送私信</el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div v-if="totalFollowing > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next"
          :total="totalFollowing"
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
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'UserFollowing',
  setup() {
    const store = useStore();
    const router = useRouter();
    const currentPage = ref(1);
    const pageSize = ref(20);

    // 从store获取数据
    const following = computed(() => store.getters['interaction/following']);
    const totalFollowing = computed(() => store.getters['interaction/totalFollowing']);
    const loading = computed(() => store.getters['interaction/followingLoading']);

    // 获取关注列表
    const fetchFollowing = async () => {
      try {
        await store.dispatch('interaction/fetchFollowing', {
          userId: store.getters['user/userInfo'].id,
          page: currentPage.value,
          per_page: pageSize.value
        });
      } catch (error) {
        ElMessage.error('获取关注列表失败，请稍后重试');
      }
    };

    // 取消关注用户
    const unfollowUser = async (userId) => {
      try {
        await ElMessageBox.confirm(
          '确定取消关注该用户吗？',
          '取消关注',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        );
        
        const response = await store.dispatch('interaction/unfollow', { userId });
        if (!response.is_following) {
          ElMessage.success('已取消关注');
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('操作失败，请稍后重试');
        }
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
      fetchFollowing();
    };

    // 获取用户名首字母
    const getInitials = (username) => {
      if (!username) return '?';
      return username.charAt(0).toUpperCase();
    };

    onMounted(() => {
      fetchFollowing();
    });

    return {
      following,
      totalFollowing,
      loading,
      currentPage,
      pageSize,
      unfollowUser,
      sendMessage,
      navigateToUser,
      handlePageChange,
      getInitials
    };
  }
};
</script>

<style scoped>
.following-page {
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

.following-container {
  padding: 20px 0;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.following-list {
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
  .following-page {
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