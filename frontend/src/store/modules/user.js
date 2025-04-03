import request from '@/utils/request';

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || null,
    userRole: localStorage.getItem('userRole') || null,
    isAuthenticated: false,
    loading: false
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo;
      localStorage.setItem('userInfo', JSON.stringify(userInfo));
    },
    LOGOUT(state) {
      state.token = null;
      state.userInfo = null;
      state.userRole = null;
      state.isAuthenticated = false;
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
      localStorage.removeItem('userRole');
    },
    SET_AUTH(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    }
  },
  actions: {
    // Login action
    async login({ commit }, credentials) {
      commit('SET_LOADING', true);
      try {
        const response = await request({
          url: '/user/login',
          method: 'post',
          data: credentials
        });
        
        // 保存token和用户信息
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('userRole', response.user.role);
        
        commit('SET_TOKEN', response.access_token);
        commit('SET_USER_INFO', response.user);
        commit('SET_AUTH', true);
        commit('SET_LOADING', false);
        
        return response.user;
      } catch (error) {
        commit('SET_LOADING', false);
        console.error('登录失败:', error);
        throw error;
      }
    },
    
    // Register action
    async register(_, userData) {
      try {
        const response = await request({
          url: '/user/register',
          method: 'post',
          data: userData
        });
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Get user profile
    async getProfile({ commit }) {
      try {
        const response = await request({
          url: '/user/profile',
          method: 'get'
        });
        
        commit('SET_USER_INFO', response);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Update user profile
    async updateProfile({ commit }, profileData) {
      try {
        const response = await request({
          url: '/user/profile',
          method: 'put',
          data: profileData
        });
        
        commit('SET_USER_INFO', response.user);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // Logout action
    logout({ commit }) {
      commit('LOGOUT');
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    userInfo: state => state.userInfo,
    token: state => state.token,
    userRole: state => state.userRole,
    loading: state => state.loading
  }
}; 