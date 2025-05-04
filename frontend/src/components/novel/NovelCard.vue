<template>
  <div class="novel-card tech-card" @click="navigateToDetail">
    <div v-if="!novel.cover || novel.cover === ''" class="novel-cover novel-default-cover">
      <div class="novel-title-overlay">{{ novel.title }}</div>
      <div class="novel-status" v-if="novel.status">{{ statusText }}</div>
    </div>
    <div v-else class="novel-cover">
      <img :src="processedCoverUrl" :alt="novel.title" class="novel-cover" @error="handleImageError">
      <div class="novel-status" v-if="novel.status">{{ statusText }}</div>
    </div>
    <div class="novel-info">
      <h3 class="novel-title text-ellipsis" :title="novel.title">{{ novel.title }}</h3>
      <div class="novel-author text-ellipsis">
        <el-icon><User /></el-icon>
        <span>{{ novel.author }}</span>
      </div>
      <div class="novel-category">
        <el-tag size="small" effect="plain" type="info">{{ novel.category }}</el-tag>
      </div>
      <div class="novel-stats">
        <span class="stats-item">
          <el-icon><Reading /></el-icon>
          {{ formatCount(novel.view_count) }}
        </span>
        <span class="stats-item">
          <el-icon><Document /></el-icon>
          {{ formatWordCount(novel.word_count) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { User, Reading, Document } from '@element-plus/icons-vue';
import { processCoverUrl } from '@/utils/image';

export default {
  name: 'NovelCard',
  components: {
    User,
    Reading,
    Document
  },
  props: {
    novel: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter();
    
    // 处理封面URL，确保中文字符正确编码
    const processedCoverUrl = computed(() => {
      return processCoverUrl(props.novel.cover);
    });
    
    // Compute cover image style with fallback
    const coverStyle = computed(() => {
      if (!props.novel.cover) {
        return {}; // 使用CSS定义的默认渐变
      }
      return {
        backgroundImage: `url(${processedCoverUrl.value})`
      };
    });
    
    // 处理图片加载错误
    const handleImageError = (e) => {
      console.log('图片加载失败，使用默认图片');
      e.target.src = '/images/default_cover.jpg';
      e.target.onerror = null; // 防止循环触发错误
    };
    
    // Compute status text based on novel status
    const statusText = computed(() => {
      return props.novel.status === 'ongoing' ? '连载中' : '已完结';
    });
    
    // Format view count with K/M suffix for large numbers
    const formatCount = (count) => {
      if (!count) return '0';
      if (count >= 1000000) {
        return (count / 1000000).toFixed(1) + 'M';
      }
      if (count >= 1000) {
        return (count / 1000).toFixed(1) + 'K';
      }
      return count.toString();
    };
    
    // Format word count to show in K/M
    const formatWordCount = (count) => {
      if (!count) return '0字';
      if (count >= 10000) {
        return (count / 10000).toFixed(1) + '万字';
      }
      return count + '字';
    };
    
    // Navigate to novel detail page
    const navigateToDetail = () => {
      router.push(`/novel/${props.novel.id}`);
    };
    
    return {
      coverStyle,
      statusText,
      formatCount,
      formatWordCount,
      navigateToDetail,
      handleImageError,
      processedCoverUrl
    };
  }
};
</script>

<style scoped>
.novel-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  transition: var(--transition-medium);
}

.novel-card:hover {
  transform: translateY(-5px);
}

.novel-cover {
  width: 100%;
  height: 0;
  padding-bottom: 133%; /* 3:4 aspect ratio for book covers */
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
}

.novel-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.novel-card:hover .novel-cover img {
  transform: scale(1.05);
}

.novel-cover.novel-default-cover {
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  overflow: hidden !important;
  width: 100% !important;
  height: 0 !important;
  padding-bottom: 133% !important; /* 3:4 aspect ratio for book covers */
  background-size: cover !important;
  background-position: center !important;
}

.novel-cover.novel-default-cover::before {
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
  text-align: center;
  padding: 10px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  font-size: 14px;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.novel-status {
  position: absolute;
  top: 10px;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 2px 8px;
  font-size: var(--font-size-xs);
  border-radius: var(--border-radius-sm) 0 0 var(--border-radius-sm);
  backdrop-filter: blur(4px);
}

.novel-info {
  padding: 12px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.novel-title {
  margin: 0 0 8px;
  font-size: var(--font-size-md);
  font-weight: bold;
  color: var(--gray-900);
}

.novel-author {
  display: flex;
  align-items: center;
  font-size: var(--font-size-sm);
  color: var(--gray-700);
  margin-bottom: 8px;
}

.novel-author .el-icon {
  margin-right: 4px;
  font-size: var(--font-size-xs);
  color: var(--primary-color);
}

.novel-category {
  margin-bottom: 12px;
}

.novel-category .el-tag {
  background-color: rgba(var(--el-color-primary-rgb), 0.1);
  color: var(--primary-color);
  border-color: transparent;
}

.novel-stats {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--gray-600);
}

.stats-item {
  display: flex;
  align-items: center;
}

.stats-item .el-icon {
  margin-right: 4px;
  font-size: var(--font-size-xs);
  color: var(--primary-color);
}
</style> 