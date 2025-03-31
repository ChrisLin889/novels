import { createStore } from 'vuex';
import user from './modules/user';
import novel from './modules/novel';
import interaction from './modules/interaction';

export default createStore({
  modules: {
    user,
    novel,
    interaction
  },
  // Global state
  state: {
    isLoading: false,
    darkMode: localStorage.getItem('darkMode') === 'true',
    errorMessage: null,
    successMessage: null
  },
  // Synchronous state mutations
  mutations: {
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading;
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
    SET_ERROR(state, message) {
      state.errorMessage = message;
    },
    SET_SUCCESS(state, message) {
      state.successMessage = message;
    },
    CLEAR_MESSAGES(state) {
      state.errorMessage = null;
      state.successMessage = null;
    }
  },
  // Actions that can be asynchronous
  actions: {
    toggleDarkMode({ commit, state }) {
      commit('SET_DARK_MODE', !state.darkMode);
    },
    setError({ commit }, message) {
      commit('SET_ERROR', message);
      setTimeout(() => {
        commit('CLEAR_MESSAGES');
      }, 3000);
    },
    setSuccess({ commit }, message) {
      commit('SET_SUCCESS', message);
      setTimeout(() => {
        commit('CLEAR_MESSAGES');
      }, 3000);
    }
  },
  // Computed properties for the state
  getters: {
    isLoading: state => state.isLoading,
    errorMessage: state => state.errorMessage,
    successMessage: state => state.successMessage
  }
}); 