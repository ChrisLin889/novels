import request from '@/utils/request';

export default {
  namespaced: true,
  state: {
    novelList: [],
    novelDetail: null,
    chapterList: [],
    chapterContent: null,
    recentRead: JSON.parse(localStorage.getItem('recentRead')) || [],
    bookshelf: JSON.parse(localStorage.getItem('bookshelf')) || [],
    readingProgress: {}
  },
  mutations: {
    SET_NOVEL_LIST(state, novelList) {
      state.novelList = novelList;
    },
    SET_NOVEL_DETAIL(state, novelDetail) {
      state.novelDetail = novelDetail;
    },
    SET_CHAPTER_LIST(state, chapterList) {
      state.chapterList = chapterList;
    },
    SET_CHAPTER_CONTENT(state, chapterContent) {
      state.chapterContent = chapterContent;
    },
    ADD_RECENT_READ(state, novel) {
      // Update recent read list (avoid duplicates)
      const index = state.recentRead.findIndex(item => item.id === novel.id);
      if (index !== -1) {
        state.recentRead.splice(index, 1);
      }
      state.recentRead.unshift(novel);
      // Keep only the most recent 10 items
      state.recentRead = state.recentRead.slice(0, 10);
      localStorage.setItem('recentRead', JSON.stringify(state.recentRead));
    },
    ADD_TO_BOOKSHELF(state, novel) {
      // Check if already in bookshelf
      const exists = state.bookshelf.some(item => item.id === novel.id);
      if (!exists) {
        state.bookshelf.unshift(novel);
        localStorage.setItem('bookshelf', JSON.stringify(state.bookshelf));
      }
    },
    REMOVE_FROM_BOOKSHELF(state, novelId) {
      state.bookshelf = state.bookshelf.filter(item => item.id !== novelId);
      localStorage.setItem('bookshelf', JSON.stringify(state.bookshelf));
    },
    SET_READING_PROGRESS(state, { novelId, chapterId, progress }) {
      state.readingProgress[novelId] = { chapterId, progress };
    }
  },
  actions: {
    // Get novel list
    async getNovelList({ commit }, params) {
      try {
        const response = await request({
          url: '/novel/list',
          method: 'get',
          params
        });
        commit('SET_NOVEL_LIST', response.novels);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Get novel detail
    async getNovelDetail({ commit }, id) {
      try {
        const response = await request({
          url: `/novel/detail/${id}`,
          method: 'get'
        });
        commit('SET_NOVEL_DETAIL', response);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Get chapter list
    async getChapterList({ commit }, novelId) {
      try {
        const response = await request({
          url: `/novel/${novelId}/chapters`,
          method: 'get'
        });
        commit('SET_CHAPTER_LIST', response.chapters);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Get chapter content
    async getChapterContent({ commit }, { chapterId }) {
      try {
        const response = await request({
          url: `/novel/chapters/${chapterId}`,
          method: 'get'
        });
        commit('SET_CHAPTER_CONTENT', response);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Add to recent read
    addRecentRead({ commit }, novel) {
      commit('ADD_RECENT_READ', novel);
    },
    
    // Add to bookshelf
    addToBookshelf({ commit }, novel) {
      commit('ADD_TO_BOOKSHELF', novel);
    },
    
    // Remove from bookshelf
    removeFromBookshelf({ commit }, novelId) {
      commit('REMOVE_FROM_BOOKSHELF', novelId);
    },
    
    async updateReadingProgress({ commit }, payload) {
      try {
        // 从payload中解构所需参数
        const { novelId, chapterId, progress } = payload;
        
        console.log(`更新小说 ${novelId} 的阅读进度`);
        
        // 创建存储键
        const storageKey = `reading_progress_${novelId}`;
        
        // 创建进度数据对象
        const progressData = { chapterId, progress, timestamp: Date.now() };
        
        // 保存到本地存储
        localStorage.setItem(storageKey, JSON.stringify(progressData));
        
        // 提交到state
        commit('SET_READING_PROGRESS', { novelId, chapterId, progress });
        
        return Promise.resolve();
      } catch (error) {
        console.error('Failed to update reading progress:', error);
        return Promise.reject(error);
      }
    }
  },
  getters: {
    novelList: state => state.novelList,
    novelDetail: state => state.novelDetail,
    chapterList: state => state.chapterList,
    chapterContent: state => state.chapterContent,
    recentRead: state => state.recentRead,
    bookshelf: state => state.bookshelf,
    isInBookshelf: state => novelId => {
      return state.bookshelf.some(item => item.id === novelId);
    },
    readingProgress: state => state.readingProgress
  }
}; 