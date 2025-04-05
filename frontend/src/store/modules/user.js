export default {
  namespaced: true,
  state: {
    user: JSON.parse(localStorage.getItem('user')) || null
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
        console.log('User state updated:', user)
      } else {
        localStorage.removeItem('user')
        console.log('User state cleared')
      }
    },
    CLEAR_USER(state) {
      state.user = null
      localStorage.removeItem('user')
      console.log('User state cleared')
    }
  },
  actions: {
    setUser({ commit }, user) {
      console.log('Setting user in store:', user)
      commit('SET_USER', user)
    },
    clearUser({ commit }) {
      console.log('Clearing user from store')
      commit('CLEAR_USER')
    },
    updateProfile({ commit, state }, profileData) {
      console.log('Updating user profile:', profileData)
      
      // 合并当前用户数据与更新的资料
      const updatedUser = {
        ...state.user,
        ...profileData
      }
      
      // 更新状态
      commit('SET_USER', updatedUser)
      
      return updatedUser
    }
  },
  getters: {
    state: state => state,
    user: state => state.user,
    userInfo: state => state.user,
    username: state => state.user?.username || state.user?.email || '用户',
    avatar: state => state.user?.avatar || '',
    isAuthor: state => state.user?.role === 'author'
  }
}; 