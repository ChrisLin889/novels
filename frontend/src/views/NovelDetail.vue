<template>
  <div class="novel-detail-container container page-container">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="error" class="error-container">
      <el-empty description="获取小说信息失败" :image-size="200">
        <template #description>
          <p>{{ error }}</p>
        </template>
        <el-button type="primary" @click="fetchNovelDetail">重试</el-button>
      </el-empty>
    </div>
    
    <div v-else class="novel-content">
      <!-- 小说基本信息 -->
      <div class="novel-header">
        <div v-if="!novel.cover || novel.cover === ''" class="novel-cover novel-default-cover">
          <div class="novel-title-overlay">{{ novel.title }}</div>
        </div>
        <div v-else class="novel-cover">
          <img :src="novel.cover" :alt="novel.title" @error="handleImageError" />
        </div>
        
        <div class="novel-info">
          <h1 class="novel-title">{{ novel.title }}</h1>
          <div class="meta-info">
            <div class="info-item"><span class="label">作者：</span>{{ novel.author }}</div>
            <div class="info-item"><span class="label">分类：</span>{{ novel.category }}</div>
            <div class="info-item"><span class="label">状态：</span>{{ novel.status === 'ongoing' ? '连载中' : '已完结' }}</div>
            <div class="info-item"><span class="label">总章节：</span>{{ novel.chapter_count || 0 }}</div>
            <div class="info-item"><span class="label">浏览量：</span>{{ novel.view_count || 0 }}</div>
            <div class="info-item"><span class="label">收藏数：</span>{{ novel.collection_count || 0 }}</div>
            <div class="info-item"><span class="label">更新时间：</span>{{ formatDate(novel.updated_at) }}</div>
          </div>
          
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="startReading">开始阅读</el-button>
            <el-button 
              :type="isCollected ? 'success' : 'primary'" 
              plain 
              size="large" 
              :icon="isCollected ? 'Star' : 'StarFilled'"
              @click="toggleCollection"
            >{{ isCollected ? '已收藏' : '收藏' }}</el-button>
          </div>
        </div>
      </div>
      
      <!-- 小说简介 -->
      <div class="novel-intro section">
        <h2 class="section-title">作品简介</h2>
        <div class="intro-content">{{ novel.intro || '暂无简介' }}</div>
      </div>
      
      <!-- 章节列表 -->
      <div class="chapter-list section">
        <h2 class="section-title">章节列表</h2>
        <div v-if="chapters.length === 0" class="empty-chapters">
          <p>暂无章节</p>
        </div>
        <div v-else class="chapter-list">
          <div v-for="chapter in chapters" :key="chapter.id" class="chapter-item">
            <router-link :to="`/novel/${novel.id}/chapter/${chapter.id}`" class="chapter-link">
              {{ chapter.title }}
            </router-link>
            <span class="chapter-time">{{ formatDate(chapter.updated_at) }}</span>
          </div>
        </div>
        <div v-if="totalChapters > 20" class="pagination">
          <el-pagination
            v-model:currentPage="currentPage"
            :page-size="20"
            layout="prev, pager, next"
            :total="totalChapters"
            @current-change="fetchChapters"
          />
        </div>
      </div>
      
      <!-- 添加评论区组件 -->
      <div class="novel-section">
        <comment-section 
          :entity-id="novel.id" 
          entity-type="novel"
          :is-owner="isOwner"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { getNovelDetail, addToCollection, removeFromCollection, checkCollection } from '@/api/novel';
import { ElMessage } from 'element-plus';
import CommentSection from '@/components/interaction/CommentSection.vue';

export default {
  name: 'NovelDetail',
  components: {
    CommentSection
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    
    const loading = ref(true);
    const error = ref('');
    const novel = ref({});
    const chapters = ref([]);
    const currentPage = ref(1);
    const isCollected = ref(false);
    const isOwner = ref(false);
    
    const novelId = computed(() => route.params.id);
    
    // 处理图片加载错误
    const handleImageError = (e) => {
      e.target.parentNode.classList.add('novel-default-cover');
      const titleOverlay = document.createElement('div');
      titleOverlay.className = 'novel-title-overlay';
      titleOverlay.textContent = novel.value.title;
      e.target.parentNode.appendChild(titleOverlay);
      e.target.style.display = 'none';
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 获取小说详情
    const fetchNovelDetail = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await getNovelDetail(novelId.value);
        novel.value = response.novel;
        chapters.value = response.chapters || [];
        
        // 更新页面标题
        if (novel.value && novel.value.title) {
          document.title = `${novel.value.title} - 小说详情 - 科技小说网`;
        }
        
        // 检查是否已收藏
        if (store.getters['user/isAuthenticated']) {
          await checkCollectionStatus();
        }
        
        // 检查当前用户是否是小说作者
        isOwner.value = response.is_owner;
      } catch (err) {
        console.error('获取小说详情失败:', err);
        error.value = typeof err === 'string' ? err : '获取小说信息失败，请稍后重试';
      } finally {
        loading.value = false;
      }
    };
    
    // 检查收藏状态
    const checkCollectionStatus = async () => {
      try {
        const result = await checkCollection(novelId.value);
        isCollected.value = result.is_collected;
        console.log('收藏状态:', isCollected.value);
      } catch (err) {
        console.error('获取收藏状态失败:', err);
        // 回退到本地存储检查
        isCollected.value = store.getters['novel/isInBookshelf'](Number(novelId.value));
      }
    };
    
    // 开始阅读，跳转到第一章
    const startReading = () => {
      if (chapters.value.length > 0) {
        router.push(`/read/${novel.value.id}/${chapters.value[0].id}`);
      } else {
        ElMessage.info('该小说暂无章节');
      }
    };
    
    // 收藏/取消收藏
    const toggleCollection = async () => {
      if (!store.getters['user/isAuthenticated']) {
        // 未登录时跳转到登录页
        router.push({
          path: '/login',
          query: { redirect: route.fullPath }
        });
        return;
      }
      
      try {
        if (isCollected.value) {
          // 取消收藏
          await removeFromCollection(novelId.value);
          // 从本地书架移除
          store.dispatch('novel/removeFromBookshelf', Number(novelId.value));
          ElMessage.success('已从书架中移除');
        } else {
          // 添加收藏
          await addToCollection(novelId.value);
          // 添加到本地书架
          store.dispatch('novel/addToBookshelf', novel.value);
          ElMessage.success('已添加到书架');
        }
        
        // 更新收藏状态
        isCollected.value = !isCollected.value;
      } catch (err) {
        console.error('收藏操作失败:', err);
        ElMessage.error('操作失败，请稍后重试');
      }
    };
    
    // 切换章节页码
    const fetchChapters = (page) => {
      currentPage.value = page;
      // 这里应该调用获取章节列表API
    };
    
    onMounted(() => {
      fetchNovelDetail();
    });
    
    return {
      novelId,
      loading,
      error,
      novel,
      chapters,
      isCollected,
      formatDate,
      startReading,
      toggleCollection,
      fetchChapters,
      fetchNovelDetail,
      handleImageError,
      isOwner
    };
  }
};
</script>

<style scoped>
.novel-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  background-color: var(--gray-50);
  min-height: calc(100vh - 80px);
}

.loading-container, .error-container {
  padding: 40px;
  background-color: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.novel-content {
  background-color: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  padding: 30px;
}

.novel-header {
  display: flex;
  margin-bottom: 30px;
}

.novel-cover {
  width: 240px;
  height: 320px;
  margin-right: 30px;
  overflow: hidden;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-md);
  flex-shrink: 0;
  position: relative;
}

.novel-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: var(--transition-medium);
}

.novel-cover img:hover {
  transform: scale(1.05);
}

.novel-default-cover {
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  overflow: hidden !important;
  width: 240px !important;
  height: 320px !important;
  margin-right: 30px !important;
  flex-shrink: 0 !important;
  border-radius: var(--border-radius-md) !important;
  box-shadow: var(--shadow-md) !important;
}

.novel-default-cover::before {
  content: '' !important;
  position: absolute !important;
  top: -50% !important;
  left: -50% !important;
  width: 200% !important;
  height: 200% !important;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.05) 40%,
    transparent 60%
  ) !important;
  transform: rotate(30deg) !important;
  pointer-events: none !important;
}

.novel-title-overlay {
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  padding: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.novel-info {
  flex: 1;
}

.novel-title {
  font-size: var(--font-size-xxl);
  margin: 0 0 20px;
  color: var(--gray-900);
  font-weight: bold;
  line-height: 1.3;
  position: relative;
  padding-bottom: 15px;
}

.novel-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: var(--tech-gradient);
  border-radius: 3px;
}

.meta-info {
  margin-bottom: 30px;
}

.info-item {
  margin-bottom: 10px;
  font-size: var(--font-size-md);
  color: var(--gray-700);
}

.info-item .label {
  color: var(--gray-600);
  display: inline-block;
  width: 80px;
}

.action-buttons {
  margin-top: 30px;
}

.action-buttons .el-button {
  margin-right: 15px;
  transition: var(--transition-medium);
}

.action-buttons .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(63, 81, 181, 0.2);
}

.section {
  margin-bottom: 40px;
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: bold;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--gray-200);
  margin-bottom: 20px;
  color: var(--gray-900);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 40px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 3px;
}

.intro-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: var(--gray-700);
  font-size: var(--font-size-md);
}

.chapter-list {
  margin-top: 20px;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 15px;
  border-bottom: 1px solid var(--gray-200);
  transition: var(--transition-medium);
}

.chapter-item:hover {
  background-color: var(--gray-100);
}

.chapter-link {
  color: var(--gray-800);
  text-decoration: none;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: var(--transition-fast);
}

.chapter-link:hover {
  color: var(--primary-color);
}

.chapter-time {
  color: var(--gray-500);
  font-size: 0.9rem;
  white-space: nowrap;
  margin-left: 15px;
}

.empty-chapters {
  text-align: center;
  padding: 30px 0;
  color: var(--gray-500);
  background-color: var(--gray-100);
  border-radius: var(--border-radius-md);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.novel-section {
  margin-bottom: 40px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .novel-header {
    flex-direction: column;
  }
  
  .novel-cover {
    width: 100%;
    height: 400px;
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .chapters-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }
}
</style>