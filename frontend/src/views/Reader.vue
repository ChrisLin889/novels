<template>
  <div class="reader-container" :class="{ 'reader-dark': isDarkMode }" :style="{ backgroundColor: bgColor }">
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
            <el-dropdown-item command="showBgColorDialog" divided>背景颜色</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-button type="primary" @click="nextChapter" :disabled="!nextChapterId">下一章</el-button>
    </div>
    
    <!-- 背景颜色选择面板 -->
    <div v-if="bgColorDialogVisible" class="color-picker-overlay" @click.self="bgColorDialogVisible = false">
      <div class="color-picker-panel">
        <div class="color-picker-header">
          <h3>选择背景颜色</h3>
          <button class="close-btn" @click="bgColorDialogVisible = false">
            <i class="el-icon-close"></i>
          </button>
        </div>
        <div class="color-options">
          <div class="color-option" 
            v-for="option in bgColorOptions" 
            :key="option.value"
            :style="{ backgroundColor: option.color }"
            @click="selectBgColor(option.value)"
          >
            <span>{{ option.label }}</span>
            <i v-if="bgColor === option.color" class="el-icon-check"></i>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加章节评论区 -->
    <div v-if="!loading && !error" class="chapter-comments">
      <comment-section 
        :entity-id="Number(chapterId)" 
        entity-type="chapter" 
        :is-owner="false"
        :novel-id="Number(novelId)"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import CommentSection from '@/components/interaction/CommentSection.vue';

export default {
  name: 'Reader',
  components: {
    CommentSection
  },
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
    const bgColor = ref(localStorage.getItem('reader_bg_color') || '#fff');
    const bgColorDialogVisible = ref(false);
    
    const bgColorOptions = [
      { label: '默认', value: 'bgDefault', color: isDarkMode.value ? '#252525' : '#fff' },
      { label: '米色', value: 'bgBeige', color: '#f8f2e4' },
      { label: '护眼绿', value: 'bgGreen', color: '#e3f1e1' },
      { label: '淡蓝', value: 'bgBlue', color: '#e9f5f9' },
      { label: '淡粉', value: 'bgPink', color: '#fbeef2' }
    ];
    
    const novelId = computed(() => route.params.novelId);
    const chapterId = computed(() => route.params.chapterId);
    
    // 增强存储当前小说ID的逻辑
    const storeNovelId = (id) => {
      if (id) {
        console.log('正在存储小说ID到localStorage:', id);
        localStorage.setItem('current_novel_id', id);
        return true;
      }
      return false;
    };
    
    // 存储当前小说ID，供评论系统使用
    watch(novelId, (newNovelId) => {
      if (newNovelId) {
        storeNovelId(newNovelId);
      }
    }, { immediate: true });
    
    // 确保章节加载成功后也保存小说ID
    watch(() => chapter.value, (newChapter) => {
      if (newChapter && newChapter.novel_id) {
        console.log('章节加载后存储小说ID:', newChapter.novel_id);
        storeNovelId(newChapter.novel_id);
      }
    });
    
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
      
      // 检查登录状态和token
      const token = localStorage.getItem('token');
      console.log('读取章节时检查token:', token ? `${token.substring(0, 15)}...` : '无token');
      console.log('章节ID:', chapterId.value);
      console.log('用户身份:', store.getters['user/userInfo']);
      
      try {
        // 添加重试逻辑
        let attempts = 0;
        const maxAttempts = 3;
        let response;
        
        while (attempts < maxAttempts) {
          try {
            console.log(`尝试获取章节内容: 第${attempts + 1}次尝试`);
            response = await store.dispatch('novel/getChapterContent', {
              novelId: novelId.value,
              chapterId: chapterId.value
            });
            console.log('章节内容API响应:', response);
            // 成功获取数据，跳出循环
            break;
          } catch (err) {
            console.error(`章节内容获取失败 (尝试 ${attempts + 1}/${maxAttempts}):`, err);
            attempts++;
            if (attempts >= maxAttempts) {
              // 所有尝试都失败，抛出最后一个错误
              throw err;
            }
            // 等待一段时间后重试
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        if (!response) {
          throw new Error('获取章节内容失败');
        }
        
        chapter.value = response.chapter;
        prevChapterId.value = response.prev_chapter ? response.prev_chapter.id : null;
        nextChapterId.value = response.next_chapter ? response.next_chapter.id : null;
        
        // 如果章节内容中包含小说ID，确保存储它
        if (response.chapter && response.chapter.novel_id) {
          storeNovelId(response.chapter.novel_id);
        } else {
          // 否则使用路由参数中的小说ID
          storeNovelId(novelId.value);
        }
        
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
        // 更详细的错误信息
        if (err.response && err.response.status) {
          const status = err.response.status;
          if (status === 404) {
            error.value = '章节不存在，可能已被删除';
          } else if (status >= 500) {
            error.value = '服务器错误，请稍后重试';
          } else {
            error.value = `请求错误 (${status})，请稍后重试`;
          }
        } else if (err.message && err.message.includes('Network Error')) {
          error.value = '网络连接失败，请检查网络后重试';
        } else {
          error.value = typeof err === 'string' ? err : '获取章节内容失败，请稍后重试';
        }
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
    
    // 选择背景颜色
    const selectBgColor = (command) => {
      if (command === 'bgDefault') {
        bgColor.value = isDarkMode.value ? '#252525' : '#fff';
      } else if (command === 'bgBeige') {
        bgColor.value = '#f8f2e4';
      } else if (command === 'bgGreen') {
        bgColor.value = '#e3f1e1';
      } else if (command === 'bgBlue') {
        bgColor.value = '#e9f5f9';
      } else if (command === 'bgPink') {
        bgColor.value = '#fbeef2';
      }
      
      localStorage.setItem('reader_bg_color', bgColor.value);
      bgColorDialogVisible.value = false;
    };
    
    // 阅读器设置
    const changeSettings = (command) => {
      if (command === 'toggleDarkMode') {
        isDarkMode.value = !isDarkMode.value;
        localStorage.setItem('reader_dark_mode', isDarkMode.value);
        
        // 更新默认背景色选项的颜色
        bgColorOptions[0].color = isDarkMode.value ? '#252525' : '#fff';
        
        // 如果用户正在使用默认背景色，则随夜间模式切换背景色
        if (bgColor.value === '#fff' || bgColor.value === '#252525') {
          bgColor.value = isDarkMode.value ? '#252525' : '#fff';
          localStorage.setItem('reader_bg_color', bgColor.value);
        }
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
      } else if (command === 'showBgColorDialog') {
        bgColorDialogVisible.value = true;
      }
    };
    
    // 更新字体大小
    const updateFontSize = () => {
      document.documentElement.style.setProperty('--reader-font-size', `${fontSize.value}px`);
    };
    
    // 监听夜间模式变化，更新背景色
    watch(isDarkMode, (newValue) => {
      // 更新默认背景色选项的颜色
      bgColorOptions[0].color = newValue ? '#252525' : '#fff';
      
      // 如果用户没有设置自定义背景色，则随夜间模式切换默认背景色
      if (bgColor.value === '#fff' || bgColor.value === '#252525') {
        bgColor.value = newValue ? '#252525' : '#fff';
        localStorage.setItem('reader_bg_color', bgColor.value);
      }
    });
    
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
      bgColor,
      bgColorDialogVisible,
      bgColorOptions,
      formattedContent,
      goBack,
      prevChapter,
      nextChapter,
      changeSettings,
      selectBgColor,
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
  background-color: #fff; /* 默认颜色现在由内联样式控制 */
  min-height: 80vh;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
  position: relative;
}

.reader-dark {
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
  margin-bottom: 30px;
}

.chapter-comments {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

/* 背景颜色选择面板样式 */
.color-picker-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.color-picker-panel {
  background-color: white;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.color-picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.color-picker-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.close-btn:hover {
  color: #409EFF;
}

.color-options {
  display: flex;
  flex-direction: column;
  padding: 15px;
  gap: 15px;
}

.color-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  color: #303133;
}

.color-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* 在夜间模式下调整面板颜色 */
.reader-dark .color-picker-panel {
  background-color: #2d2d2d;
  border-color: #444;
}

.reader-dark .color-picker-header {
  border-color: #444;
}

.reader-dark .color-picker-header h3 {
  color: #e0e0e0;
}

.reader-dark .close-btn {
  color: #909399;
}

.reader-dark .color-option {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.reader-dark .color-option span {
  color: #303133;  /* 保持文字颜色便于阅读 */
}
</style> 