import request from '@/utils/request';

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || null
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
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
    }
  },
  actions: {
    // Login action
    async login({ commit }, credentials) {
      try {
        const response = await request({
          url: '/user/login',
          method: 'post',
          data: credentials
        });
        
        commit('SET_TOKEN', response.access_token);
        commit('SET_USER_INFO', response.user);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
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
    token: state => state.token
  }
}; 