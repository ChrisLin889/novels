<template>
  <div class="reading-history">
    <h2>阅读历史</h2>
    
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="false"
      class="mb-20"
    />
    
    <div class="loading-container" v-if="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="historyList.length === 0" class="empty-content">
      <i class="el-icon-document"></i>
      <p>暂无阅读历史</p>
      <el-button type="primary" @click="$router.push('/')">去看看有哪些好书</el-button>
    </div>
    
    <div v-else class="history-list">
      <el-card v-for="item in historyList" :key="item.novel.id" class="history-item">
        <div class="history-content">
          <div class="book-cover">
            <img :src="item.novel.cover || '/placeholder.png'" :alt="item.novel.title" />
          </div>
          <div class="book-info">
            <h3>{{ item.novel.title }}</h3>
            <p class="author">作者: {{ item.novel.author }}</p>
            <p class="last-chapter">
              上次阅读: {{ item.chapter.title }}
              <span class="chapter-number">(第{{ item.chapter.chapter_number }}章)</span>
            </p>
            <p class="read-time">{{ formatDate(item.last_read_time) }}</p>
          </div>
        </div>
        <div class="operation">
          <el-button 
            type="primary" 
            size="small" 
            @click="continueReading(item.novel.id, item.chapter.id)"
          >
            继续阅读
          </el-button>
          <el-button 
            type="info" 
            size="small" 
            @click="$router.push(`/novel/${item.novel.id}`)"
          >
            查看详情
          </el-button>
        </div>
      </el-card>
    </div>
    
    <el-pagination
      v-if="totalItems > 0"
      background
      layout="prev, pager, next"
      :total="totalItems"
      :page-size="pageSize"
      v-model:current-page="currentPage"
      @current-change="handlePageChange"
      class="pagination"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getReadingHistory } from '@/api/interaction';

export default {
  name: 'UserReadingHistory',
  
  setup() {
    const router = useRouter();
    const historyList = ref([]);
    const loading = ref(false);
    const error = ref('');
    const currentPage = ref(1);
    const pageSize = ref(10);
    const totalItems = ref(0);
    
    const loadReadingHistory = async (page = 1) => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('开始加载阅读历史...');
        const response = await getReadingHistory({
          page,
          per_page: pageSize.value
        });
        
        console.log('阅读历史API响应:', response);
        console.log('阅读历史数据结构:', JSON.stringify(response.history || [], null, 2));
        
        historyList.value = response.history || [];
        totalItems.value = response.total || 0;
        
        console.log('处理后的historyList:', historyList.value);
      } catch (err) {
        console.error('Failed to load reading history:', err);
        error.value = '获取阅读历史失败，请稍后重试';
        ElMessage.error('获取阅读历史失败');
      } finally {
        loading.value = false;
      }
    };
    
    const handlePageChange = (page) => {
      currentPage.value = page;
      loadReadingHistory(page);
    };
    
    const continueReading = (novelId, chapterId) => {
      router.push(`/read/${novelId}/${chapterId}`);
    };
    
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      
      // 一天内显示为几小时前/几分钟前
      if (diff < 86400000) { // 24小时内
        const hours = Math.floor(diff / 3600000);
        if (hours > 0) {
          return `${hours}小时前`;
        }
        const minutes = Math.floor(diff / 60000);
        if (minutes > 0) {
          return `${minutes}分钟前`;
        }
        return '刚刚';
      }
      
      // 七天内显示为周几
      if (diff < 604800000) { // 7天内
        const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        return dayNames[date.getDay()];
      }
      
      // 其他情况显示具体日期
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    };
    
    onMounted(() => {
      loadReadingHistory();
    });
    
    return {
      historyList,
      loading,
      error,
      currentPage,
      pageSize,
      totalItems,
      handlePageChange,
      continueReading,
      formatDate
    };
  }
};
</script>

<style scoped>
.reading-history {
  padding: 0 10px;
}

.loading-container {
  padding: 20px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
  color: #909399;
}

.empty-content i {
  font-size: 48px;
  margin-bottom: 20px;
}

.history-list {
  margin-top: 20px;
}

.history-item {
  margin-bottom: 15px;
  transition: all 0.3s;
}

.history-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.history-content {
  display: flex;
}

.book-cover {
  width: 80px;
  height: 120px;
  overflow: hidden;
  margin-right: 15px;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.book-info {
  flex: 1;
}

.book-info h3 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 16px;
}

.author, .last-chapter, .read-time {
  margin: 5px 0;
  font-size: 14px;
  color: #606266;
}

.chapter-number {
  color: #909399;
  font-size: 13px;
}

.operation {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.mb-20 {
  margin-bottom: 20px;
}
</style> 