<template>
  <div class="messages-page">
    <div class="page-header">
      <h1 class="page-title">我的私信</h1>
    </div>

    <div class="messages-container">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="inbox.length === 0" class="empty-container">
        <el-empty description="暂无私信记录">
          <template #description>
            <p>您的收件箱是空的，暂无任何私信</p>
          </template>
        </el-empty>
      </div>

      <div v-else class="inbox-list">
        <el-list>
          <el-list-item
            v-for="conversation in inbox"
            :key="conversation.user.id"
            class="conversation-item"
            :class="{ 'has-unread': conversation.unread_count > 0 }"
            @click="navigateToConversation(conversation.user.id)"
          >
            <div class="conversation-avatar">
              <el-badge v-if="conversation.unread_count > 0" :value="conversation.unread_count" type="danger">
                <el-avatar :src="conversation.user.avatar" :size="50">
                  {{ getInitials(conversation.user.username) }}
                </el-avatar>
              </el-badge>
              <el-avatar v-else :src="conversation.user.avatar" :size="50">
                {{ getInitials(conversation.user.username) }}
              </el-avatar>
            </div>

            <div class="conversation-info">
              <div class="conversation-header">
                <span class="conversation-name">{{ conversation.user.username }}</span>
                <span class="conversation-time">{{ formatTime(conversation.last_message.created_at) }}</span>
              </div>
              <div class="conversation-last-message" :class="{ 'unread': conversation.unread_count > 0 }">
                <span v-if="conversation.last_message.is_from_me">我: </span>
                {{ conversation.last_message.content }}
              </div>
            </div>
          </el-list-item>
        </el-list>
      </div>

      <div v-if="totalMessages > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next"
          :total="totalMessages"
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
  name: 'Messages',
  setup() {
    const store = useStore();
    const router = useRouter();
    const currentPage = ref(1);
    const pageSize = ref(20);

    // 从store获取数据
    const inbox = computed(() => store.getters['interaction/inbox']);
    const totalMessages = computed(() => store.getters['interaction/totalMessages']);
    const loading = computed(() => store.getters['interaction/inboxLoading']);

    // 获取收件箱数据
    const fetchInbox = async () => {
      try {
        await store.dispatch('interaction/fetchInbox', {
          page: currentPage.value,
          per_page: pageSize.value
        });
      } catch (error) {
        ElMessage.error('获取私信列表失败，请稍后重试');
      }
    };

    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page;
      fetchInbox();
    };

    // 导航到对话界面
    const navigateToConversation = (userId) => {
      router.push(`/user/conversation/${userId}`);
    };

    // 获取用户名首字母
    const getInitials = (username) => {
      if (!username) return '?';
      return username.charAt(0).toUpperCase();
    };

    // 格式化时间
    const formatTime = (dateString) => {
      if (!dateString) return '';
      
      const now = new Date();
      const date = new Date(dateString);
      const diffTime = Math.abs(now - date);
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        // 今天
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
      } else if (diffDays === 1) {
        // 昨天
        return '昨天';
      } else if (diffDays < 7) {
        // 一周内
        return `${diffDays}天前`;
      } else {
        // 超过一周
        return date.toLocaleDateString('zh-CN', {
          month: '2-digit',
          day: '2-digit'
        });
      }
    };

    onMounted(() => {
      fetchInbox();
    });

    return {
      inbox,
      totalMessages,
      loading,
      currentPage,
      pageSize,
      handlePageChange,
      navigateToConversation,
      getInitials,
      formatTime
    };
  }
};
</script>

<style scoped>
.messages-page {
  max-width: 1000px;
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

.messages-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
}

.conversation-item {
  display: flex;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.conversation-item:hover {
  background-color: #f5f7fa;
}

.has-unread {
  background-color: #ecf5ff;
}

.has-unread:hover {
  background-color: #e3f0ff;
}

.conversation-avatar {
  margin-right: 15px;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.conversation-name {
  font-weight: bold;
  color: #303133;
  margin-right: 10px;
}

.conversation-time {
  font-size: 0.8rem;
  color: #909399;
  white-space: nowrap;
}

.conversation-last-message {
  color: #606266;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.9rem;
}

.unread {
  color: #303133;
  font-weight: 500;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 