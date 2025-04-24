<template>
  <div class="user-bookshelf">
    <h2>我的书架</h2>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="error" class="error-message">
      <el-alert
        :title="error"
        type="warning"
        description="使用本地存储的书架数据显示"
        show-icon
      />
    </div>
    
    <div v-else-if="bookshelf.length > 0">
      <el-row :gutter="20">
        <el-col 
          v-for="novel in bookshelf" 
          :key="novel.id" 
          :xs="12" 
          :sm="8" 
          :md="6" 
          :lg="6" 
          :xl="4"
        >
          <div class="bookshelf-item tech-card">
            <div class="novel-cover" 
                 :class="{'novel-default-cover': !novel.cover || novel.cover === ''}" 
                 :style="novel.cover && novel.cover !== '' ? { backgroundImage: `url(${novel.cover})` } : {}">
              <div v-if="!novel.cover || novel.cover === ''" class="novel-title-overlay">{{ novel.title }}</div>
              <img v-else :src="novel.cover" style="display:none" @error="handleImageError(novel)" />
              <div class="remove-button" @click.stop="removeFromBookshelf(novel.id)">
                <el-icon><Close /></el-icon>
              </div>
            </div>
            <div class="novel-info" @click="navigateToNovel(novel.id)">
              <h3 class="novel-title text-ellipsis">{{ novel.title }}</h3>
              <p class="novel-author text-ellipsis">{{ novel.author }}</p>
              <p class="reading-progress">
                <span>阅读至: {{ novel.lastRead?.chapterTitle || '未开始阅读' }}</span>
              </p>
            </div>
            <div class="novel-actions">
              <el-button 
                type="primary" 
                size="small" 
                @click="continueReading(novel)"
              >
                继续阅读
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <div v-else class="empty-bookshelf">
      <el-empty description="您的书架还没有书哦，快去添加吧！">
        <el-button type="primary" @click="navigateToHome">去首页看看</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { ElMessageBox, ElMessage } from 'element-plus';
import { Close } from '@element-plus/icons-vue';
import { getUserCollection } from '@/api/novel';
import { toggleCollection } from '@/api/interaction';

export default {
  name: 'UserBookshelf',
  components: {
    Close
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // 从Vuex获取书架数据，也可以作为备用数据源
    const localBookshelf = computed(() => store.getters['novel/bookshelf']);
    
    // 用来存储从API获取的书架数据
    const bookshelf = ref([]);
    const loading = ref(true);
    const error = ref('');
    
    // 从API获取书架数据
    const fetchBookshelf = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        if (!store.getters['user/isAuthenticated']) {
          // 如果用户未登录，使用本地存储的数据
          bookshelf.value = localBookshelf.value;
          return;
        }
        
        const response = await getUserCollection();
        console.log('获取书架数据:', response);
        
        if (response && response.collections) {
          bookshelf.value = response.collections;
          
          // 将API获取的数据同步到本地存储
          bookshelf.value.forEach(novel => {
            if (!store.getters['novel/isInBookshelf'](novel.id)) {
              store.dispatch('novel/addToBookshelf', novel);
            }
          });
        } else {
          // 回退到本地存储
          bookshelf.value = localBookshelf.value;
        }
      } catch (err) {
        console.error('获取书架失败:', err);
        error.value = typeof err === 'string' ? err : '获取书架数据失败，使用本地数据';
        // 出错时回退到本地存储
        bookshelf.value = localBookshelf.value;
      } finally {
        loading.value = false;
      }
    };
    
    // Navigate to novel detail page
    const navigateToNovel = (id) => {
      router.push(`/novel/${id}`);
    };
    
    // Navigate to home page
    const navigateToHome = () => {
      router.push('/');
    };
    
    // Remove novel from bookshelf
    const removeFromBookshelf = (id) => {
      ElMessageBox.confirm(
        '确定要从书架中移除这本书吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          if (store.getters['user/isAuthenticated']) {
            // 调用API从远程书架移除
            await toggleCollection(id);
          }
          
          // 从本地书架移除
          store.dispatch('novel/removeFromBookshelf', id);
          
          // 更新当前页面显示
          bookshelf.value = bookshelf.value.filter(item => item.id !== id);
          
          ElMessage({
            type: 'success',
            message: '已从书架中移除'
          });
        } catch (err) {
          console.error('移除书架项目失败:', err);
          ElMessage.error('操作失败，请稍后重试');
        }
      }).catch(() => {});
    };
    
    // Continue reading from last chapter
    const continueReading = (novel) => {
      if (novel.lastRead && novel.lastRead.chapterId) {
        router.push(`/read/${novel.id}/${novel.lastRead.chapterId}`);
      } else {
        // If no reading history, start from first chapter
        router.push(`/novel/${novel.id}`);
      }
    };
    
    // 处理图片加载错误
    const handleImageError = (novel) => (e) => {
      // 获取父元素
      const coverElement = e.target.parentNode;
      
      // 移除背景图片样式
      coverElement.style.backgroundImage = 'none';
      
      // 添加默认封面类
      coverElement.classList.add('novel-default-cover');
      
      // 如果没有标题覆盖层，创建一个
      if (!coverElement.querySelector('.novel-title-overlay')) {
        const titleOverlay = document.createElement('div');
        titleOverlay.className = 'novel-title-overlay';
        titleOverlay.textContent = novel.title;
        coverElement.appendChild(titleOverlay);
      }
      
      // 隐藏图片元素
      e.target.style.display = 'none';
    };
    
    // 初始化
    onMounted(() => {
      fetchBookshelf();
    });
    
    return {
      bookshelf,
      loading,
      error,
      navigateToNovel,
      navigateToHome,
      removeFromBookshelf,
      continueReading,
      handleImageError
    };
  }
};
</script>

<style scoped>
.user-bookshelf {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--gray-50);
  min-height: calc(100vh - 80px);
}

.user-bookshelf h2 {
  font-size: var(--font-size-xxl);
  margin-bottom: 20px;
  padding-bottom: 15px;
  color: var(--gray-900);
  text-align: center;
  font-weight: bold;
  position: relative;
}

.user-bookshelf h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 80px;
  height: 3px;
  background: var(--tech-gradient);
  transform: translateX(-50%);
  border-radius: 3px;
}

.loading, .error-message {
  padding: 20px;
  margin-bottom: 20px;
  background-color: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.bookshelf-item {
  background-color: #fff;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  margin-bottom: 20px;
  position: relative;
  transition: var(--transition-medium);
  border: 1px solid var(--gray-200);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.bookshelf-item:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-5px);
  border-color: var(--primary-light);
}

.novel-cover {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
  cursor: pointer;
}

.novel-cover.novel-default-cover {
  background: linear-gradient(135deg, #3f51b5 0%, #00bcd4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.novel-cover.novel-default-cover::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.05) 40%,
    transparent 60%
  );
  transform: rotate(30deg);
  pointer-events: none;
}

.novel-title-overlay {
  color: white;
  text-align: center;
  padding: 10px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  font-size: 16px;
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

.remove-button {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 28px;
  height: 28px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-medium);
  z-index: 5;
  backdrop-filter: blur(4px);
}

.remove-button:hover {
  background-color: rgba(220, 53, 69, 0.9);
  box-shadow: 0 2px 8px rgba(220, 53, 69, 0.4);
  transform: scale(1.1);
}

.novel-info {
  padding: 15px;
  cursor: pointer;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.novel-title {
  font-size: var(--font-size-md);
  margin: 0 0 8px;
  color: var(--gray-900);
  font-weight: bold;
}

.novel-author {
  font-size: var(--font-size-sm);
  color: var(--gray-700);
  margin: 0 0 10px;
}

.reading-progress {
  font-size: var(--font-size-sm);
  color: var(--gray-600);
  margin: 0;
  background-color: rgba(var(--el-color-primary-rgb), 0.05);
  padding: 5px 10px;
  border-radius: var(--border-radius-sm);
  margin-top: auto;
}

.novel-actions {
  padding: 0 15px 15px;
  display: flex;
  justify-content: flex-end;
}

.novel-actions .el-button {
  background: var(--primary-color);
  border-color: var(--primary-color);
  transition: var(--transition-medium);
}

.novel-actions .el-button:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
  box-shadow: 0 2px 8px rgba(63, 81, 181, 0.3);
}

.empty-bookshelf {
  padding: 40px 0;
  background-color: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 