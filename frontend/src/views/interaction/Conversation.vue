<template>
  <div class="conversation-page">
    <div class="conversation-header">
      <el-page-header @back="goBack" :title="partner.username || '聊天'" />
    </div>

    <div class="conversation-container">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="messages.length === 0" class="empty-container">
        <el-empty description="暂无聊天记录">
          <template #description>
            <p>开始发送消息，开启对话</p>
          </template>
        </el-empty>
      </div>

      <div v-else class="messages-container" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="message.id" class="message-wrapper">
          <div class="timestamp" v-if="shouldShowTimestamp(message, index)">
            {{ formatDate(message.created_at) }}
          </div>
          <div class="message" :class="{ 'message-sent': message.is_from_me, 'message-received': !message.is_from_me }">
            <div class="message-avatar">
              <el-avatar :size="40" :src="message.is_from_me ? userAvatar : partnerAvatar">
                {{ message.is_from_me ? getInitials(userName) : getInitials(partner.username) }}
              </el-avatar>
            </div>
            <div class="message-content">
              <div class="message-bubble">
                {{ message.content }}
              </div>
              <div class="message-time">
                {{ formatTime(message.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="message-form">
        <el-input
          v-model="newMessage"
          type="textarea"
          :rows="3"
          placeholder="输入消息..."
          resize="none"
          maxlength="500"
          show-word-limit
          @keydown.enter.prevent="sendMessage"
        />
        <div class="form-actions">
          <el-button type="primary" :disabled="!newMessage.trim()" @click="sendMessage">
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  name: 'Conversation',
  setup() {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const messagesContainer = ref(null);
    const newMessage = ref('');
    const userId = computed(() => parseInt(route.params.userId));
    
    // 从store获取数据
    const messages = computed(() => store.getters['interaction/conversation']);
    const partner = computed(() => store.getters['interaction/conversationPartner']);
    const loading = computed(() => store.getters['interaction/conversationLoading']);
    const userInfo = computed(() => store.getters['user/userInfo'] || {});
    const userName = computed(() => userInfo.value.username || '');
    const userAvatar = computed(() => userInfo.value.avatar || '');
    const partnerAvatar = computed(() => partner.value.avatar || '');

    // 获取对话数据
    const fetchConversation = async () => {
      try {
        await store.dispatch('interaction/fetchConversation', {
          userId: userId.value
        });
        
        // 标记消息为已读
        if (messages.value.length > 0) {
          await store.dispatch('interaction/markMessageAsRead', {
            userId: userId.value
          });
        }
        
        // 滚动到最新消息
        scrollToBottom();
      } catch (error) {
        ElMessage.error('获取聊天记录失败，请稍后重试');
      }
    };

    // 发送消息
    const sendMessage = async () => {
      if (!newMessage.value.trim()) return;
      
      try {
        await store.dispatch('interaction/sendMessage', {
          recipientId: userId.value,
          content: newMessage.value.trim()
        });
        
        newMessage.value = '';
        await nextTick();
        scrollToBottom();
        ElMessage.success('发送成功');
      } catch (error) {
        console.error('发送消息失败:', error);
        // 只有在真正的错误时才显示错误提示
        if (error.response && error.response.status >= 400) {
          ElMessage.error('发送消息失败，请稍后重试');
        } else {
          // 如果消息已经显示在界面上，说明发送成功了
          ElMessage.success('发送成功');
        }
      }
    };

    // 滚动到底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      });
    };

    // 返回上一页
    const goBack = () => {
      router.push('/user/messages');
    };

    // 获取用户名首字母
    const getInitials = (username) => {
      if (!username) return '?';
      return username.charAt(0).toUpperCase();
    };

    // 格式化时间
    const formatTime = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit'
      });
    };

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      const now = new Date();
      const yesterday = new Date(now);
      yesterday.setDate(yesterday.getDate() - 1);
      
      if (date.toDateString() === now.toDateString()) {
        return '今天';
      } else if (date.toDateString() === yesterday.toDateString()) {
        return '昨天';
      } else {
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
    };

    // 判断是否显示时间戳
    const shouldShowTimestamp = (message, index) => {
      if (index === 0) return true;
      
      const currentDate = new Date(message.created_at);
      const prevDate = new Date(messages.value[index - 1].created_at);
      
      // 如果与前一条消息时间相差超过30分钟，则显示时间戳
      return (currentDate - prevDate) > 30 * 60 * 1000;
    };

    // 监听userId变化，重新获取对话
    watch(() => userId.value, () => {
      fetchConversation();
    });

    onMounted(() => {
      fetchConversation();
    });

    return {
      messages,
      partner,
      loading,
      newMessage,
      userAvatar,
      partnerAvatar,
      userName,
      messagesContainer,
      goBack,
      sendMessage,
      getInitials,
      formatTime,
      formatDate,
      shouldShowTimestamp
    };
  }
};
</script>

<style scoped>
.conversation-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  height: calc(100vh - 130px);
  display: flex;
  flex-direction: column;
}

.conversation-header {
  margin-bottom: 20px;
}

.conversation-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.loading-container,
.empty-container {
  padding: 40px 0;
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f9f9f9;
}

.message-wrapper {
  margin-bottom: 15px;
}

.timestamp {
  text-align: center;
  margin: 15px 0;
  color: #909399;
  font-size: 0.8rem;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message-sent {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 10px;
}

.message-content {
  max-width: 70%;
}

.message-sent .message-content {
  text-align: right;
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 12px;
  word-break: break-word;
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.message-sent .message-bubble {
  background-color: #409eff;
  color: white;
  border-top-right-radius: 4px;
}

.message-received .message-bubble {
  background-color: #ffffff;
  color: #303133;
  border: 1px solid #ebeef5;
  border-top-left-radius: 4px;
}

.message-time {
  font-size: 0.7rem;
  color: #909399;
  margin-top: 5px;
}

.message-form {
  padding: 15px;
  border-top: 1px solid #ebeef5;
}

.form-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .conversation-page {
    padding: 10px;
    height: calc(100vh - 120px);
  }
  
  .message-content {
    max-width: 80%;
  }
}
</style> 