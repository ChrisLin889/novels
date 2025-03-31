import { 
  postComment, 
  getNovelComments, 
  followUser, 
  unfollowUser, 
  getFollowers, 
  getFollowing, 
  sendMessage, 
  getInbox,
  getConversation,
  markMessageAsRead,
  getUserComments
} from '@/api/interaction';

export default {
  namespaced: true,
  state: {
    // 评论相关
    comments: [],
    totalComments: 0,
    commentsLoading: false,
    
    // 用户评论
    userComments: [],
    totalUserComments: 0,
    userCommentsLoading: false,
    
    // 关注相关
    followers: [],
    following: [],
    totalFollowers: 0,
    totalFollowing: 0,
    followersLoading: false,
    followingLoading: false,
    
    // 私信相关
    inbox: [],
    conversation: [],
    totalMessages: 0,
    inboxLoading: false,
    conversationLoading: false,
    currentConversationUser: null,
    unreadCount: 0,
    conversationPartner: {}
  },
  
  mutations: {
    // 评论相关
    SET_COMMENTS(state, { comments, total }) {
      state.comments = comments;
      state.totalComments = total;
    },
    SET_COMMENTS_LOADING(state, loading) {
      state.commentsLoading = loading;
    },
    ADD_COMMENT(state, comment) {
      state.comments.unshift(comment);
      state.totalComments++;
    },
    
    // 用户评论相关
    SET_USER_COMMENTS(state, { comments, total }) {
      state.userComments = comments;
      state.totalUserComments = total;
    },
    SET_USER_COMMENTS_LOADING(state, loading) {
      state.userCommentsLoading = loading;
    },
    
    // 关注相关
    SET_FOLLOWERS(state, { followers, total }) {
      state.followers = followers;
      state.totalFollowers = total;
    },
    SET_FOLLOWING(state, { following, total }) {
      state.following = following;
      state.totalFollowing = total;
    },
    SET_FOLLOWERS_LOADING(state, loading) {
      state.followersLoading = loading;
    },
    SET_FOLLOWING_LOADING(state, loading) {
      state.followingLoading = loading;
    },
    ADD_FOLLOWING(state, user) {
      if (!state.following.some(u => u.id === user.id)) {
        state.following.push(user);
        state.totalFollowing++;
      }
    },
    REMOVE_FOLLOWING(state, userId) {
      state.following = state.following.filter(u => u.id !== userId);
      state.totalFollowing--;
    },
    
    // 私信相关
    SET_INBOX(state, { inbox, total, unreadCount }) {
      state.inbox = inbox;
      state.totalMessages = total;
      state.unreadCount = unreadCount;
    },
    SET_CONVERSATION(state, { messages, user }) {
      state.conversation = messages;
      state.currentConversationUser = user;
    },
    SET_INBOX_LOADING(state, loading) {
      state.inboxLoading = loading;
    },
    SET_CONVERSATION_LOADING(state, loading) {
      state.conversationLoading = loading;
    },
    ADD_MESSAGE(state, message) {
      // 添加到当前对话
      state.conversation.push(message);
      
      // 更新收件箱中对应的最后一条消息
      const existingConversation = state.inbox.find(c => 
        c.user.id === (message.is_from_me ? message.recipient_id : message.sender_id)
      );
      
      if (existingConversation) {
        existingConversation.last_message = {
          content: message.content,
          created_at: message.created_at,
          is_from_me: message.is_from_me
        };
      }
    },
    MARK_CONVERSATION_READ(state, userId) {
      const conversation = state.inbox.find(c => c.user.id === userId);
      if (conversation) {
        // 更新未读计数
        state.unreadCount -= conversation.unread_count || 0;
        conversation.unread_count = 0;
      }
    },
    SET_CONVERSATION_PARTNER(state, partner) {
      state.conversationPartner = partner;
    }
  },
  
  actions: {
    // 获取评论
    async fetchComments({ commit }, { entityId, entityType, page = 1, per_page = 10 }) {
      commit('SET_COMMENTS_LOADING', true);
      try {
        let response;
        if (entityType === 'novel') {
          response = await getNovelComments(entityId, { page, per_page });
        } else if (entityType === 'chapter') {
          // 这里应添加章节评论接口
          response = { comments: [], total: 0 };
        }
        
        commit('SET_COMMENTS', { 
          comments: response.comments || [], 
          total: response.total || 0
        });
        return response;
      } catch (error) {
        console.error('获取评论失败:', error);
        return Promise.reject(error);
      } finally {
        commit('SET_COMMENTS_LOADING', false);
      }
    },
    
    // 发表评论
    async postComment({ commit }, { entityId, entityType, content, parentId }) {
      try {
        const data = {
          novel_id: entityType === 'novel' ? entityId : undefined,
          chapter_id: entityType === 'chapter' ? entityId : undefined,
          content,
          parent_id: parentId
        };
        
        const response = await postComment(data);
        
        if (response && response.comment) {
          commit('ADD_COMMENT', response.comment);
        }
        
        return response;
      } catch (error) {
        console.error('发表评论失败:', error);
        return Promise.reject(error);
      }
    },
    
    // 获取用户评论
    async fetchUserComments({ commit }, { page = 1, per_page = 20 } = {}) {
      commit('SET_USER_COMMENTS_LOADING', true);
      try {
        const response = await getUserComments({ page, per_page });
        
        commit('SET_USER_COMMENTS', { 
          comments: response.comments || [], 
          total: response.total || 0
        });
        
        return response;
      } catch (error) {
        console.error('获取用户评论失败:', error);
        return Promise.reject(error);
      } finally {
        commit('SET_USER_COMMENTS_LOADING', false);
      }
    },
    
    // 获取粉丝列表
    async fetchFollowers({ commit }, { userId, page = 1, per_page = 20 }) {
      commit('SET_FOLLOWERS_LOADING', true);
      try {
        const response = await getFollowers(userId, { page, per_page });
        commit('SET_FOLLOWERS', { 
          followers: response.followers, 
          total: response.total 
        });
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      } finally {
        commit('SET_FOLLOWERS_LOADING', false);
      }
    },
    
    // 获取关注列表
    async fetchFollowing({ commit }, { userId, page = 1, per_page = 20 }) {
      commit('SET_FOLLOWING_LOADING', true);
      try {
        const response = await getFollowing(userId, { page, per_page });
        commit('SET_FOLLOWING', { 
          following: response.following, 
          total: response.total 
        });
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      } finally {
        commit('SET_FOLLOWING_LOADING', false);
      }
    },
    
    // 关注用户
    async follow({ commit }, { userId, userData }) {
      try {
        const response = await followUser(userId);
        // 只有在实际关注时才添加到following列表
        if (response.is_following) {
          commit('ADD_FOLLOWING', userData);
        }
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // 取消关注
    async unfollow({ commit }, { userId }) {
      try {
        const response = await unfollowUser(userId);
        // 只有在实际取消关注时才从following列表中移除
        if (!response.is_following) {
          commit('REMOVE_FOLLOWING', userId);
        }
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // 获取收件箱
    async fetchInbox({ commit }, { page = 1, per_page = 20 } = {}) {
      commit('SET_INBOX_LOADING', true);
      try {
        const response = await getInbox({ page, per_page });
        
        // 适配API响应格式
        const conversations = (response.messages || []).map(message => {
          return {
            user: message.sender,
            last_message: {
              content: message.content,
              created_at: message.created_at,
              is_from_me: false
            },
            unread_count: message.is_read ? 0 : 1
          };
        });
        
        commit('SET_INBOX', { 
          inbox: conversations, 
          total: response.total || 0,
          unreadCount: response.unread_count || 0
        });
        return response;
      } catch (error) {
        console.error('获取收件箱失败:', error);
        throw error;
      } finally {
        commit('SET_INBOX_LOADING', false);
      }
    },
    
    // 获取与某用户的对话
    async fetchConversation({ commit }, { userId, params }) {
      commit('SET_CONVERSATION_LOADING', true);
      try {
        const response = await getConversation(userId, params);
        
        // 添加 is_from_me 标志
        const messages = (response.messages || []).map(message => {
          return {
            ...message,
            is_from_me: message.sender_id === userId ? false : true
          };
        });
        
        // 确保有伙伴信息，如果没有提供则构建一个基本对象
        let partner = {};
        if (messages.length > 0) {
          const partnerMessage = messages.find(m => m.sender_id === userId);
          if (partnerMessage && partnerMessage.sender) {
            partner = partnerMessage.sender;
          }
        }
        
        commit('SET_CONVERSATION', { 
          messages,
          user: userId
        });
        
        // 保存对话伙伴信息
        commit('SET_CONVERSATION_PARTNER', partner);
        
        // 标记为已读
        commit('MARK_CONVERSATION_READ', userId);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      } finally {
        commit('SET_CONVERSATION_LOADING', false);
      }
    },
    
    // 发送私信
    async sendMessage({ commit, rootState }, { recipientId, content }) {
      try {
        const response = await sendMessage({ recipient_id: recipientId, content });
        
        // 添加发送者信息，因为API返回的消息可能没有
        const messageWithInfo = {
          ...response.data,
          is_from_me: true,
          sender_id: rootState.user.userInfo.id,
          recipient_id: recipientId
        };
        
        commit('ADD_MESSAGE', messageWithInfo);
        return Promise.resolve(response);
      } catch (error) {
        return Promise.reject(error);
      }
    },
    
    // 标记消息为已读
    async markAsRead({ commit }, { messageId, userId }) {
      try {
        await markMessageAsRead(messageId);
        if (userId) {
          commit('MARK_CONVERSATION_READ', userId);
        }
        return Promise.resolve();
      } catch (error) {
        return Promise.reject(error);
      }
    }
  },
  
  getters: {
    comments: state => state.comments,
    totalComments: state => state.totalComments,
    commentsLoading: state => state.commentsLoading,
    
    userComments: state => state.userComments,
    totalUserComments: state => state.totalUserComments,
    userCommentsLoading: state => state.userCommentsLoading,
    
    followers: state => state.followers,
    following: state => state.following,
    totalFollowers: state => state.totalFollowers,
    totalFollowing: state => state.totalFollowing,
    followersLoading: state => state.followersLoading,
    followingLoading: state => state.followingLoading,
    
    inbox: state => state.inbox,
    conversation: state => state.conversation,
    currentConversationUser: state => state.currentConversationUser,
    totalMessages: state => state.totalMessages,
    inboxLoading: state => state.inboxLoading,
    conversationLoading: state => state.conversationLoading,
    unreadCount: state => state.unreadCount,
    conversationPartner: state => state.conversationPartner
  }
}; 