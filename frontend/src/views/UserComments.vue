<template>
  <div class="user-comments-container">
    <h1 class="page-title">我的评论</h1>
    
    <el-card class="box-card">
      <template #header>
        <div class="clearfix">
          <span>评论列表</span>
        </div>
      </template>
      
      <div v-loading="loading" element-loading-text="加载中...">
        <div v-if="comments.length === 0 && !loading" class="empty-state">
          您还没有发表过评论
        </div>
        
        <div v-else>
          <div v-for="(comment, index) in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="novel-title">
                <router-link :to="getEntityLink(comment)">《{{ comment.entity_title || '未知作品' }}》</router-link>
              </span>
              <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
            <div class="comment-footer">
              <el-button 
                type="text" 
                size="small"
                @click="navigateToComment(comment)"
              >
                查看原文
              </el-button>
            </div>
            <el-divider v-if="index < comments.length - 1"></el-divider>
          </div>
        </div>
        
        <el-pagination
          v-if="total > 0"
          background
          layout="prev, pager, next"
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          @current-change="handlePageChange"
          class="pagination"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'UserComments',
  
  data() {
    return {
      currentPage: 1,
      pageSize: 10
    };
  },
  
  computed: {
    ...mapState('interaction', [
      'userComments',
      'totalUserComments',
      'userCommentsLoading'
    ]),
    
    comments() {
      return this.userComments;
    },
    
    total() {
      return this.totalUserComments;
    },
    
    loading() {
      return this.userCommentsLoading;
    }
  },
  
  created() {
    this.loadComments();
  },
  
  methods: {
    ...mapActions('interaction', [
      'fetchUserComments'
    ]),
    
    loadComments() {
      this.fetchUserComments({
        page: this.currentPage,
        per_page: this.pageSize
      });
    },
    
    handlePageChange(page) {
      this.currentPage = page;
      this.loadComments();
    },
    
    formatTime(timestamp) {
      if (!timestamp) return '未知时间';
      
      try {
        const date = new Date(timestamp);
        const now = new Date();
        
        // 计算时间差（毫秒）
        const diff = now - date;
        
        // 转换为相对时间
        if (diff < 60 * 1000) { // 不到1分钟
          return '刚刚';
        } else if (diff < 60 * 60 * 1000) { // 不到1小时
          const minutes = Math.floor(diff / (60 * 1000));
          return `${minutes}分钟前`;
        } else if (diff < 24 * 60 * 60 * 1000) { // 不到1天
          const hours = Math.floor(diff / (60 * 60 * 1000));
          return `${hours}小时前`;
        } else if (diff < 30 * 24 * 60 * 60 * 1000) { // 不到30天
          const days = Math.floor(diff / (24 * 60 * 60 * 1000));
          return `${days}天前`;
        } else {
          // 显示年-月-日格式
          return date.toISOString().split('T')[0];
        }
      } catch (e) {
        console.error('时间格式化错误:', e);
        return timestamp;
      }
    },
    
    getEntityLink(comment) {
      if (!comment.entity_type || !comment.entity_id) {
        return '/';
      }
      
      if (comment.entity_type === 'novel') {
        return `/novel/${comment.entity_id}`;
      }
      
      if (comment.entity_type === 'chapter') {
        return `/chapter/${comment.entity_id}`;
      }
      
      return '/';
    },
    
    navigateToComment(comment) {
      const link = this.getEntityLink(comment);
      this.$router.push(link);
    }
  }
};
</script>

<style scoped>
.user-comments-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #303133;
}

.box-card {
  margin-bottom: 20px;
}

.comment-item {
  margin-bottom: 15px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.novel-title {
  font-weight: bold;
}

.comment-time {
  color: #909399;
}

.comment-content {
  margin-bottom: 10px;
  line-height: 1.6;
  color: #606266;
  word-break: break-word;
}

.comment-footer {
  display: flex;
  justify-content: flex-end;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #909399;
  font-size: 14px;
}
</style> 