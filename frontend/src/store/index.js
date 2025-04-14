import { createStore } from 'vuex';
import user from './modules/user';
import novel from './modules/novel';
import interaction from './modules/interaction';
import admin from './modules/admin';
import { login, register, updateProfile, changePassword } from '@/api/user';

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
    notifications: [],
    isLoggedIn: !!localStorage.getItem('token'),
    token: localStorage.getItem('token') || ''
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
    },
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    SET_LOGIN_STATUS(state, status) {
      state.isLoggedIn = status;
    },
    CLEAR_AUTH(state) {
      state.token = '';
      state.isLoggedIn = false;
      localStorage.removeItem('token');
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
    },
    async login({ commit, dispatch }, userData) {
      try {
        console.log('开始登录请求:', userData);
        const response = await login(userData);
        console.log('登录响应:', response);
        
        if (response && response.access_token && response.user) {
          const { access_token, user } = response;
          console.log('解析的token:', access_token);
          console.log('解析的用户信息:', user);
          
          // 保存 token
          commit('SET_TOKEN', access_token);
          commit('SET_LOGIN_STATUS', true);
          
          // 保存用户信息
          await dispatch('user/setUser', user, { root: true });
          
          return { token: access_token, user };
        } else {
          console.error('响应数据格式错误:', response);
          throw new Error('登录响应格式错误：缺少 token 或用户信息');
        }
      } catch (error) {
        console.error('登录失败:', error);
        commit('SET_TOKEN', '');
        commit('SET_LOGIN_STATUS', false);
        throw error;
      }
    },
    // eslint-disable-next-line no-unused-vars
    async register(_, userData) {
      return await register(userData);
    },
    logout({ commit, dispatch }) {
      commit('SET_TOKEN', '');
      commit('SET_LOGIN_STATUS', false);
      dispatch('user/clearUser', null, { root: true });
    },
    // eslint-disable-next-line no-unused-vars
    async updateProfile({ dispatch }, profileData) {
      const response = await updateProfile(profileData);
      if (response && response.data) {
        await dispatch('user/setUser', response.data, { root: true });
      }
      return response;
    },
    // eslint-disable-next-line no-unused-vars
    async changePassword(_, passwordData) {
      return await changePassword(passwordData);
    }
  },
  // Computed properties for the state
  getters: {
    state: state => state,
    isLoading: state => state.loading,
    globalError: state => state.globalError,
    successMessage: state => state.successMessage,
    notifications: state => state.notifications,
    isLoggedIn: state => state.isLoggedIn || !!localStorage.getItem('token'),
    isAuthenticated: state => state.user?.isAuthenticated || !!localStorage.getItem('token'),
    user: state => state.user?.user || null,
    isAuthor: state => state.user?.user?.role === 'author',
    token: state => state.token || localStorage.getItem('token')
  }
}); 