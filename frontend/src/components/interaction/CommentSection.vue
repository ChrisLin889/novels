<template>
  <div class="comment-section">
    <h3 class="section-title">读者评论 ({{ total }})</h3>
    
    <!-- 评论输入框 -->
    <div v-if="isAuthenticated" class="comment-form">
      <div class="user-avatar">
        <el-avatar :size="40" :src="userAvatar">
          {{ getInitials(userName) }}
        </el-avatar>
      </div>
      <div class="comment-input">
        <el-input
          v-model="commentContent"
          type="textarea"
          :rows="2"
          placeholder="分享您的想法..."
          resize="none"
          maxlength="500"
          show-word-limit
          @keydown.enter.ctrl.prevent="submitComment"
        />
        <div class="form-actions">
          <span class="hint">Ctrl + Enter 快速发布</span>
          <el-button 
            type="primary" 
            :disabled="!commentContent.trim() || submitting" 
            @click="submitComment"
          >
            发布评论
          </el-button>
        </div>
      </div>
    </div>
    
    <div v-else class="login-prompt">
      <el-alert
        title="请先登录后评论"
        type="info"
        :closable="false"
        show-icon
      >
        <template #default>
          <el-button type="primary" size="small" @click="navigateToLogin">
            去登录
          </el-button>
        </template>
      </el-alert>
    </div>

    <!-- 加载中状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
    </div>
    
    <!-- 无评论提示 -->
    <div v-else-if="comments.length === 0" class="empty-container">
      <el-empty description="暂无评论">
        <template #description>
          <p>成为第一个发表评论的人</p>
        </template>
      </el-empty>
    </div>
    
    <!-- 评论列表 -->
    <div v-else class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-avatar">
          <el-avatar :size="40" :src="comment.user.avatar">
            {{ getInitials(comment.user.username) }}
          </el-avatar>
        </div>
        <div class="comment-content">
          <div class="comment-header">
            <span class="comment-author">{{ comment.user.username }}</span>
            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>
          <div class="comment-text">{{ comment.content }}</div>
          <div class="comment-actions">
            <span class="action-btn" @click="handleReply(comment)">
              <i class="el-icon-chat-line-square"></i> 回复
            </span>
            <span v-if="isOwner && comment.user.id !== userId" class="action-btn">
              <i class="el-icon-message"></i> 私信
            </span>
          </div>
          
          <!-- 回复框 -->
          <div v-if="replyingTo === comment.id" class="reply-form">
            <el-input
              v-model="replyContent"
              type="textarea"
              :rows="1"
              placeholder="回复..."
              resize="none"
              maxlength="300"
              show-word-limit
            />
            <div class="reply-actions">
              <el-button size="small" @click="cancelReply">取消</el-button>
              <el-button 
                type="primary" 
                size="small" 
                :disabled="!replyContent.trim() || submitting" 
                @click="submitReply(comment)"
              >
                回复
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  name: 'CommentSection',
  props: {
    entityId: {
      type: Number,
      required: true
    },
    entityType: {
      type: String,
      required: true,
      validator: (value) => ['novel', 'chapter', 'user'].includes(value)
    },
    isOwner: {
      type: Boolean,
      default: false
    },
    novelId: {
      type: Number,
      default: null
    }
  },
  setup(props) {
    const store = useStore();
    const router = useRouter();
    const commentContent = ref('');
    const replyContent = ref('');
    const replyingTo = ref(null);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const submitting = ref(false);

    // 从store获取数据
    const userInfo = computed(() => store.getters['user/userInfo'] || {});
    const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
    const userId = computed(() => userInfo.value.id);
    const userName = computed(() => userInfo.value.username || '');
    const userAvatar = computed(() => userInfo.value.avatar || '');
    
    const comments = computed(() => store.getters['interaction/comments']);
    const total = computed(() => store.getters['interaction/totalComments']);
    const loading = computed(() => store.getters['interaction/commentsLoading']);

    // 获取评论列表
    const fetchComments = async () => {
      try {
        const fetchParams = {
          entityId: props.entityId,
          entityType: props.entityType,
          page: currentPage.value,
          per_page: pageSize.value
        };
        
        // 如果是章节评论并且有传入的小说ID，则直接使用它
        if (props.entityType === 'chapter' && props.novelId) {
          console.log('使用传入的小说ID获取章节评论:', props.novelId);
          fetchParams.novelId = props.novelId;
          localStorage.setItem('current_novel_id', props.novelId.toString());
        }
        
        console.log('获取评论，参数:', fetchParams);
        
        // 调用API获取评论
        const response = await store.dispatch('interaction/fetchComments', fetchParams);
        
        console.log('获取评论结果:', response);
      } catch (error) {
        console.error('获取评论失败:', error);
        ElMessage.error('获取评论失败，请稍后重试');
      }
    };

    // 提交评论
    const submitComment = async () => {
      if (!commentContent.value.trim() || submitting.value) return;
      
      submitting.value = true;
      try {
        const commentData = {
          entityId: props.entityId,
          entityType: props.entityType,
          content: commentContent.value.trim()
        };
        
        // 如果是章节评论并且有传入的小说ID，则直接使用它
        if (props.entityType === 'chapter' && props.novelId) {
          console.log('使用传入的小说ID发表章节评论:', props.novelId);
          localStorage.setItem('current_novel_id', props.novelId.toString());
          commentData.novelId = props.novelId;
        }
        
        console.log('准备提交评论，数据:', commentData);
        
        const response = await store.dispatch('interaction/postComment', commentData);
        
        console.log('提交评论结果:', response);
        
        commentContent.value = '';
        ElMessage.success('评论发表成功');
        
        // 重新获取第一页评论
        currentPage.value = 1;
        await fetchComments();
      } catch (error) {
        console.error('评论发表失败:', error);
        ElMessage.error('评论发表失败，请稍后重试');
      } finally {
        submitting.value = false;
      }
    };

    // 处理回复
    const handleReply = (comment) => {
      if (!isAuthenticated.value) {
        ElMessage.warning('请先登录后回复');
        return;
      }
      
      replyingTo.value = comment.id;
      replyContent.value = `@${comment.user.username} `;
    };

    // 取消回复
    const cancelReply = () => {
      replyingTo.value = null;
      replyContent.value = '';
    };

    // 提交回复
    const submitReply = async (comment) => {
      if (!replyContent.value.trim() || submitting.value) return;
      
      submitting.value = true;
      try {
        await store.dispatch('interaction/postComment', {
          entityId: props.entityId,
          entityType: props.entityType,
          content: replyContent.value.trim(),
          parentId: comment.id
        });
        
        replyContent.value = '';
        replyingTo.value = null;
        ElMessage.success('回复发表成功');
        
        // 重新获取当前页评论
        await fetchComments();
      } catch (error) {
        ElMessage.error('回复发表失败，请稍后重试');
      } finally {
        submitting.value = false;
      }
    };

    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page;
      fetchComments();
    };

    // 导航到登录页
    const navigateToLogin = () => {
      router.push('/login');
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
      const diffMinutes = Math.floor(diffTime / (1000 * 60));
      const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffMinutes < 60) {
        // 1小时内
        return diffMinutes === 0 ? '刚刚' : `${diffMinutes}分钟前`;
      } else if (diffHours < 24) {
        // 24小时内
        return `${diffHours}小时前`;
      } else if (diffDays < 7) {
        // 一周内
        return `${diffDays}天前`;
      } else {
        // 超过一周
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
    };

    onMounted(() => {
      fetchComments();
    });

    return {
      commentContent,
      replyContent,
      replyingTo,
      comments,
      total,
      loading,
      currentPage,
      pageSize,
      submitting,
      isAuthenticated,
      userId,
      userName,
      userAvatar,
      submitComment,
      handleReply,
      cancelReply,
      submitReply,
      handlePageChange,
      navigateToLogin,
      getInitials,
      formatTime
    };
  }
};
</script>

<style scoped>
.comment-section {
  margin: 30px 0;
}

.section-title {
  font-size: 1.5rem;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.comment-form {
  display: flex;
  margin-bottom: 25px;
}

.user-avatar {
  margin-right: 15px;
}

.comment-input {
  flex: 1;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.hint {
  font-size: 0.8rem;
  color: #909399;
}

.login-prompt {
  margin-bottom: 25px;
}

.loading-container,
.empty-container {
  padding: 30px 0;
  text-align: center;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  display: flex;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.comment-avatar {
  margin-right: 15px;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: bold;
  color: #303133;
}

.comment-time {
  font-size: 0.9rem;
  color: #909399;
}

.comment-text {
  font-size: 1rem;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 10px;
  word-break: break-word;
}

.comment-actions {
  margin-top: 10px;
}

.action-btn {
  font-size: 0.9rem;
  color: #909399;
  margin-right: 15px;
  cursor: pointer;
}

.action-btn:hover {
  color: #409eff;
}

.reply-form {
  margin-top: 15px;
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 4px;
}

.reply-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.reply-actions .el-button {
  margin-left: 10px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .comment-form {
    flex-direction: column;
  }
  
  .user-avatar {
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: flex-end;
  }
  
  .hint {
    display: none;
  }
  
  .form-actions .el-button {
    margin-top: 10px;
  }
}
</style> 