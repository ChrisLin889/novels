import * as adminApi from '@/api/admin';

const state = {
  dashboard: {
    userStats: {},
    contentStats: {},
    activityStats: {}
  },
  users: [],
  userActions: [],
  sensitiveWords: [],
  pendingContent: {
    novel: [],
    chapter: [],
    comment: []
  },
  crawledNovels: [],
  crawledChapters: [],
  pagination: {
    users: { total: 0, totalPages: 0, page: 1, perPage: 20 },
    userActions: { total: 0, totalPages: 0, page: 1, perPage: 20 },
    sensitiveWords: { total: 0, totalPages: 0, page: 1, perPage: 50 },
    pendingNovel: { total: 0, totalPages: 0, page: 1, perPage: 20 },
    pendingChapter: { total: 0, totalPages: 0, page: 1, perPage: 20 },
    pendingComment: { total: 0, totalPages: 0, page: 1, perPage: 20 },
    crawledNovels: { total: 0, totalPages: 0, page: 1, perPage: 20 }
  },
  loading: {
    dashboard: false,
    users: false,
    userActions: false,
    sensitiveWords: false,
    pendingContent: false,
    crawledNovels: false,
    crawledChapters: false
  },
  error: null
};

const getters = {
  isLoading: state => key => state.loading[key],
  dashboardData: state => state.dashboard,
  usersList: state => state.users,
  usersPagination: state => state.pagination.users,
  userActionsList: state => state.userActions,
  userActionsPagination: state => state.pagination.userActions,
  sensitiveWordsList: state => state.sensitiveWords,
  sensitiveWordsPagination: state => state.pagination.sensitiveWords,
  pendingContent: state => type => state.pendingContent[type] || [],
  pendingContentPagination: state => type => {
    const key = `pending${type.charAt(0).toUpperCase() + type.slice(1)}`;
    return state.pagination[key] || { total: 0, totalPages: 0, page: 1, perPage: 20 };
  },
  crawledNovelsList: state => state.crawledNovels,
  crawledNovelsPagination: state => state.pagination.crawledNovels,
  crawledChaptersList: state => state.crawledChapters,
  error: state => state.error
};

const actions = {
  // 获取仪表盘数据
  async fetchDashboard({ commit }) {
    commit('SET_LOADING', { key: 'dashboard', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getDashboardStats();
      commit('SET_DASHBOARD', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'dashboard', value: false });
    }
  },

  // 获取用户列表
  async fetchUsers({ commit }, params = {}) {
    commit('SET_LOADING', { key: 'users', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getUsers(params);
      commit('SET_USERS', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'users', value: false });
    }
  },

  // 管理用户状态
  async manageUser({ commit, dispatch }, { userId, data }) {
    commit('CLEAR_ERROR');
    try {
      const result = await adminApi.manageUser(userId, data);
      // 刷新用户列表
      dispatch('fetchUsers', { page: state.pagination.users.page });
      return result;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    }
  },

  // 获取用户操作历史
  async fetchUserActions({ commit }, params = {}) {
    commit('SET_LOADING', { key: 'userActions', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getUserActions(params);
      commit('SET_USER_ACTIONS', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'userActions', value: false });
    }
  },

  // 获取敏感词列表
  async fetchSensitiveWords({ commit }, params = {}) {
    commit('SET_LOADING', { key: 'sensitiveWords', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getSensitiveWords(params);
      commit('SET_SENSITIVE_WORDS', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'sensitiveWords', value: false });
    }
  },

  // 添加敏感词
  async addSensitiveWord({ commit, dispatch }, data) {
    commit('CLEAR_ERROR');
    try {
      const result = await adminApi.addSensitiveWord(data);
      // 刷新敏感词列表
      dispatch('fetchSensitiveWords', { page: state.pagination.sensitiveWords.page });
      return result;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    }
  },

  // 删除敏感词
  async deleteSensitiveWord({ commit, dispatch }, wordId) {
    commit('CLEAR_ERROR');
    try {
      const result = await adminApi.deleteSensitiveWord(wordId);
      // 刷新敏感词列表
      dispatch('fetchSensitiveWords', { page: state.pagination.sensitiveWords.page });
      return result;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    }
  },

  // 获取待审核内容
  async fetchPendingContent({ commit }, { contentType, params = {} }) {
    commit('SET_LOADING', { key: 'pendingContent', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getPendingContent(contentType, params);
      commit('SET_PENDING_CONTENT', { contentType, data });
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'pendingContent', value: false });
    }
  },

  // 审核内容
  async auditContent({ commit, dispatch }, { auditId, data, contentType }) {
    commit('CLEAR_ERROR');
    try {
      const result = await adminApi.auditContent(auditId, data);
      
      // 获取对应内容类型的当前页码
      const paginationKey = `pending${contentType.charAt(0).toUpperCase() + contentType.slice(1)}`;
      const currentPage = state.pagination[paginationKey].page;
      
      // 刷新待审核内容列表
      dispatch('fetchPendingContent', { 
        contentType, 
        params: { page: currentPage } 
      });
      
      return result;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    }
  },

  // 获取爬取的小说列表
  async fetchCrawledNovels({ commit }, params = {}) {
    commit('SET_LOADING', { key: 'crawledNovels', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getCrawledNovels(params);
      commit('SET_CRAWLED_NOVELS', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'crawledNovels', value: false });
    }
  },

  // 获取爬取的小说章节
  async fetchCrawledChapters({ commit }, novelId) {
    commit('SET_LOADING', { key: 'crawledChapters', value: true });
    commit('CLEAR_ERROR');
    try {
      const data = await adminApi.getCrawledChapters(novelId);
      commit('SET_CRAWLED_CHAPTERS', data);
      return data;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    } finally {
      commit('SET_LOADING', { key: 'crawledChapters', value: false });
    }
  },

  // 管理爬取的小说
  async manageCrawledNovel({ commit, dispatch }, { novelId, data }) {
    commit('CLEAR_ERROR');
    try {
      const result = await adminApi.manageCrawledNovel(novelId, data);
      // 刷新爬取的小说列表
      dispatch('fetchCrawledNovels', { page: state.pagination.crawledNovels.page });
      return result;
    } catch (error) {
      commit('SET_ERROR', error);
      throw error;
    }
  }
};

const mutations = {
  SET_LOADING(state, { key, value }) {
    state.loading[key] = value;
  },
  
  SET_ERROR(state, error) {
    state.error = error;
  },
  
  CLEAR_ERROR(state) {
    state.error = null;
  },
  
  SET_DASHBOARD(state, data) {
    state.dashboard = {
      userStats: data.user_stats || {},
      contentStats: data.content_stats || {},
      activityStats: data.activity_stats || {}
    };
  },
  
  SET_USERS(state, data) {
    state.users = data.users || [];
    state.pagination.users = {
      total: data.total || 0,
      totalPages: data.total_pages || 0,
      page: data.page || 1,
      perPage: data.per_page || 20
    };
  },
  
  SET_USER_ACTIONS(state, data) {
    state.userActions = data.actions || [];
    state.pagination.userActions = {
      total: data.total || 0,
      totalPages: data.total_pages || 0,
      page: data.page || 1,
      perPage: data.per_page || 20
    };
  },
  
  SET_SENSITIVE_WORDS(state, data) {
    state.sensitiveWords = data.words || [];
    state.pagination.sensitiveWords = {
      total: data.total || 0,
      totalPages: data.total_pages || 0,
      page: data.page || 1,
      perPage: data.per_page || 50
    };
  },
  
  SET_PENDING_CONTENT(state, { contentType, data }) {
    state.pendingContent[contentType] = data.content || [];
    
    const paginationKey = `pending${contentType.charAt(0).toUpperCase() + contentType.slice(1)}`;
    state.pagination[paginationKey] = {
      total: data.total || 0,
      totalPages: data.total_pages || 0,
      page: data.page || 1,
      perPage: data.per_page || 20
    };
  },
  
  SET_CRAWLED_NOVELS(state, data) {
    state.crawledNovels = data.novels || [];
    state.pagination.crawledNovels = {
      total: data.total || 0,
      totalPages: data.total_pages || 0,
      page: data.page || 1,
      perPage: data.per_page || 20
    };
  },
  
  SET_CRAWLED_CHAPTERS(state, data) {
    state.crawledChapters = data.chapters || [];
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}; 