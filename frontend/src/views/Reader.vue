<template>
  <div class="reader-container" :class="{ 'reader-dark': isDarkMode }">
    <div class="reader-header">
      <el-button @click="goBack" icon="el-icon-arrow-left">返回</el-button>
      <h1 class="chapter-title">{{ chapter.title || '加载中...' }}</h1>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="error" class="error-container">
      <el-empty description="获取章节内容失败" :image-size="200">
        <template #description>
          <p>{{ error }}</p>
        </template>
        <el-button type="primary" @click="fetchChapterContent">重试</el-button>
      </el-empty>
    </div>
    
    <div v-else class="chapter-content">
      <div v-html="formattedContent"></div>
    </div>
    
    <div class="reader-footer">
      <el-button type="primary" plain @click="prevChapter" :disabled="!prevChapterId">上一章</el-button>
      <el-dropdown trigger="click" @command="changeSettings">
        <el-button>
          设置
          <i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="toggleDarkMode">{{ isDarkMode ? '关闭' : '开启' }}夜间模式</el-dropdown-item>
            <el-dropdown-item command="increaseFont">放大字体</el-dropdown-item>
            <el-dropdown-item command="decreaseFont">缩小字体</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-button type="primary" @click="nextChapter" :disabled="!nextChapterId">下一章</el-button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'Reader',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    
    const loading = ref(true);
    const error = ref('');
    const chapter = ref({});
    const prevChapterId = ref(null);
    const nextChapterId = ref(null);
    const isDarkMode = ref(localStorage.getItem('reader_dark_mode') === 'true');
    const fontSize = ref(parseInt(localStorage.getItem('reader_font_size')) || 18);
    
    const novelId = computed(() => route.params.novelId);
    const chapterId = computed(() => route.params.chapterId);
    
    const formattedContent = computed(() => {
      if (!chapter.value || !chapter.value.content) return '';
      
      // 把章节内容按段落拆分，每段包装在<p>标签中
      return chapter.value.content
        .split('\n')
        .filter(para => para.trim().length > 0)
        .map(para => `<p>${para}</p>`)
        .join('');
    });
    
    // 获取章节内容
    const fetchChapterContent = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await store.dispatch('novel/getChapterContent', {
          novelId: novelId.value,
          chapterId: chapterId.value
        });
        
        chapter.value = response.chapter;
        prevChapterId.value = response.prev_chapter ? response.prev_chapter.id : null;
        nextChapterId.value = response.next_chapter ? response.next_chapter.id : null;
        
        // 添加到最近阅读
        if (response.chapter) {
          store.dispatch('novel/addRecentRead', {
            id: novelId.value,
            title: store.getters['novel/novelDetail']?.title || '未知小说',
            lastRead: {
              chapterId: chapterId.value,
              chapterTitle: response.chapter.title,
              timestamp: new Date().toISOString()
            }
          });
        }
        
        // 更新页面标题
        document.title = `${chapter.value.title || '阅读'} - 小说网站`;
      } catch (err) {
        console.error('获取章节内容失败:', err);
        error.value = typeof err === 'string' ? err : '获取章节内容失败，请稍后重试';
      } finally {
        loading.value = false;
      }
    };
    
    // 导航功能
    const goBack = () => {
      router.push(`/novel/${novelId.value}`);
    };
    
    const prevChapter = () => {
      if (prevChapterId.value) {
        router.push(`/read/${novelId.value}/${prevChapterId.value}`);
      }
    };
    
    const nextChapter = () => {
      if (nextChapterId.value) {
        router.push(`/read/${novelId.value}/${nextChapterId.value}`);
      }
    };
    
    // 阅读器设置
    const changeSettings = (command) => {
      if (command === 'toggleDarkMode') {
        isDarkMode.value = !isDarkMode.value;
        localStorage.setItem('reader_dark_mode', isDarkMode.value);
      } else if (command === 'increaseFont') {
        if (fontSize.value < 28) {
          fontSize.value += 2;
          localStorage.setItem('reader_font_size', fontSize.value);
          updateFontSize();
        }
      } else if (command === 'decreaseFont') {
        if (fontSize.value > 14) {
          fontSize.value -= 2;
          localStorage.setItem('reader_font_size', fontSize.value);
          updateFontSize();
        }
      }
    };
    
    // 更新字体大小
    const updateFontSize = () => {
      document.documentElement.style.setProperty('--reader-font-size', `${fontSize.value}px`);
    };
    
    // 监听路由变化，以便在章节之间导航时重新获取内容
    watch(
      () => route.params.chapterId,
      (newChapterId, oldChapterId) => {
        if (newChapterId !== oldChapterId) {
          fetchChapterContent();
        }
      }
    );
    
    onMounted(() => {
      // 初始化字体大小
      updateFontSize();
      // 获取章节内容
      fetchChapterContent();
    });
    
    return {
      novelId,
      chapterId,
      chapter,
      loading,
      error,
      prevChapterId,
      nextChapterId,
      isDarkMode,
      formattedContent,
      goBack,
      prevChapter,
      nextChapter,
      changeSettings,
      fetchChapterContent
    };
  }
};
</script>

<style>
:root {
  --reader-font-size: 18px;
}
</style>

<style scoped>
.reader-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  min-height: 80vh;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.reader-dark {
  background-color: #252525;
  color: #e0e0e0;
}

.reader-dark .reader-header,
.reader-dark .reader-footer {
  border-color: #444;
}

.loading-container, .error-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.reader-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.chapter-title {
  margin-left: 20px;
  flex-grow: 1;
  text-align: center;
  font-size: 1.5rem;
}

.chapter-content {
  font-size: var(--reader-font-size);
  line-height: 1.8;
  text-align: justify;
  margin-bottom: 40px;
}

.chapter-content p {
  margin-bottom: 1em;
  text-indent: 2em;
}

.reader-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
</style> 