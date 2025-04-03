import { createStore } from 'vuex';
import user from './modules/user';
import novel from './modules/novel';
import interaction from './modules/interaction';
import admin from './modules/admin';

// HTTP拦截器
import axios from 'axios';

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    // 获取token
    const token = localStorage.getItem('token');
    // 如果有token，则添加到header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response && error.response.status === 401) {
      // 如果返回401，可能是token过期，清除token并跳转到登录页
      localStorage.removeItem('token');
      window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    }
    return Promise.reject(error);
  }
);

export default createStore({
  modules: {
    user,
    novel,
    interaction,
    admin
  },
  // Global state
  state: {
    loading: false,
    darkMode: localStorage.getItem('darkMode') === 'true',
    globalError: null,
    successMessage: null,
    notifications: []
  },
  // Synchronous state mutations
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value;
    },
    SET_DARK_MODE(state, isDark) {
      state.darkMode = isDark;
      localStorage.setItem('darkMode', isDark);
      if (isDark) {
        document.documentElement.classList.add('dark-mode');
      } else {
        document.documentElement.classList.remove('dark-mode');
      }
    },
    SET_GLOBAL_ERROR(state, error) {
      state.globalError = error;
    },
    SET_SUCCESS(state, message) {
      state.successMessage = message;
    },
    CLEAR_MESSAGES(state) {
      state.globalError = null;
      state.successMessage = null;
    },
    ADD_NOTIFICATION(state, notification) {
      state.notifications.push(notification);
    },
    REMOVE_NOTIFICATION(state, id) {
      state.notifications = state.notifications.filter(n => n.id !== id);
    }
  },
  // Actions that can be asynchronous
  actions: {
    toggleDarkMode({ commit, state }) {
      commit('SET_DARK_MODE', !state.darkMode);
    },
    setGlobalError({ commit }, error) {
      commit('SET_GLOBAL_ERROR', error);
    },
    setSuccess({ commit }, message) {
      commit('SET_SUCCESS', message);
      setTimeout(() => {
        commit('CLEAR_MESSAGES');
      }, 3000);
    },
    showNotification({ commit }, { message, type = 'info', duration = 3000 }) {
      const id = Date.now();
      commit('ADD_NOTIFICATION', { id, message, type });
      
      // 自动清除通知
      setTimeout(() => {
        commit('REMOVE_NOTIFICATION', id);
      }, duration);
    }
  },
  // Computed properties for the state
  getters: {
    isLoading: state => state.loading,
    globalError: state => state.globalError,
    successMessage: state => state.successMessage,
    notifications: state => state.notifications
  }
}); 