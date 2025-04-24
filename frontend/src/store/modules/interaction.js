import { 
  postComment, 
  getNovelComments, 
  getChapterComments,
  toggleFollow, 
  getFollowers, 
  getFollowing, 
  sendMessage, 
  getInbox,
  getConversation,
  markMessageAsRead,
  getUserComments,
  checkFollowStatus
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
    async fetchComments({ commit }, { entityId, entityType, page = 1, per_page = 10, novelId }) {
      commit('SET_COMMENTS_LOADING', true);
      try {
        let response;
        if (entityType === 'novel') {
          response = await getNovelComments(entityId, { page, per_page });
        } else if (entityType === 'chapter') {
          // 优先使用传入的novelId参数
          if (novelId) {
            console.log('使用传入的小说ID获取章节评论:', novelId, '章节ID:', entityId);
            response = await getChapterComments(novelId, entityId, { page, per_page });
          } else {
            // 尝试从localStorage获取
            const localNovelId = localStorage.getItem('current_novel_id');
            
            // 添加调试日志
            console.log('从localStorage获取小说ID:', localNovelId, '章节ID:', entityId);
            
            if (!localNovelId || localNovelId === 'undefined' || localNovelId === 'null') {
              console.error('获取小说ID失败，localStorage中没有小说ID');
              // 尝试从URL中获取小说ID
              const path = window.location.pathname;
              const matches = path.match(/\/read\/(\d+)\//);
              if (matches && matches[1]) {
                const novelIdFromUrl = matches[1];
                console.log('从URL获取小说ID:', novelIdFromUrl);
                localStorage.setItem('current_novel_id', novelIdFromUrl);
                response = await getChapterComments(novelIdFromUrl, entityId, { page, per_page });
              } else {
                throw new Error('无法获取小说ID，无法加载评论');
              }
            } else {
              response = await getChapterComments(localNovelId, entityId, { page, per_page });
            }
          }
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
    async postComment({ commit }, { entityId, entityType, content, parentId, novelId }) {
      try {
        let data = {
          content,
          parent_id: parentId
        };
        
        if (entityType === 'novel') {
          data.novel_id = entityId;
        } else if (entityType === 'chapter') {
          // 优先使用传入的novelId参数
          if (novelId) {
            data.novel_id = parseInt(novelId);
            data.chapter_id = entityId;
            console.log('使用传入的novelId发表章节评论:', data);
          } else {
            // 从localStorage获取小说ID作为备选
            const localNovelId = localStorage.getItem('current_novel_id');
            
            // 添加调试日志
            console.log('从localStorage获取小说ID:', localNovelId);
            
            if (!localNovelId || localNovelId === 'undefined' || localNovelId === 'null') {
              console.error('获取小说ID失败，localStorage中没有小说ID');
              // 尝试从URL中获取小说ID
              const path = window.location.pathname;
              const matches = path.match(/\/read\/(\d+)\//);
              if (matches && matches[1]) {
                const novelIdFromUrl = matches[1];
                console.log('从URL获取小说ID:', novelIdFromUrl);
                localStorage.setItem('current_novel_id', novelIdFromUrl);
                data.novel_id = parseInt(novelIdFromUrl);
              } else {
                throw new Error('无法获取小说ID，无法发表评论');
              }
            } else {
              data.novel_id = parseInt(localNovelId);
            }
            
            data.chapter_id = entityId;
          }
        }
        
        console.log('最终发表评论数据:', data);
        
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
        const response = await toggleFollow(userId);
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
        const response = await toggleFollow(userId);
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
        console.log('获取收件箱响应:', response);
        
        // 适配API响应格式 - 根据实际返回值结构调整
        let conversations = [];
        let totalCount = 0;
        let unreadCount = 0;
        
        if (response.conversations) {
          // 标准格式
          conversations = response.conversations;
          totalCount = response.total || 0;
          unreadCount = response.unread_count || 0;
        } else if (Array.isArray(response)) {
          // 可能直接返回数组
          conversations = response.map(message => {
            return {
              user: message.sender || message.user || {},
              last_message: {
                content: message.content || '',
                created_at: message.created_at || new Date().toISOString(),
                is_from_me: message.is_from_me || false
              },
              unread_count: message.is_read ? 0 : 1
            };
          });
          totalCount = conversations.length;
        } else if (response.messages) {
          // 另一种可能的格式
          conversations = response.messages.map(message => {
            return {
              user: message.sender || message.user || {},
              last_message: {
                content: message.content || '',
                created_at: message.created_at || new Date().toISOString(),
                is_from_me: message.is_from_me || false
              },
              unread_count: message.is_read ? 0 : 1
            };
          });
          totalCount = response.total || conversations.length;
          unreadCount = response.unread_count || 0;
        }
        
        commit('SET_INBOX', { 
          inbox: conversations, 
          total: totalCount,
          unreadCount: unreadCount
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
        console.log('获取对话响应:', response);
        
        // 处理不同的响应格式
        let messages = [];
        let partner = {};
        
        if (response.messages && Array.isArray(response.messages)) {
          // 标准格式
          messages = response.messages.map(message => {
            // 确保消息有is_from_me字段，根据发送者ID判断
            return {
              ...message,
              is_from_me: message.sender_id !== parseInt(userId),
              created_at: message.created_at || new Date().toISOString()
            };
          });
        } else if (response.conversation && Array.isArray(response.conversation)) {
          // 可能的另一种格式
          messages = response.conversation.map(message => {
            return {
              ...message,
              is_from_me: message.sender_id !== parseInt(userId),
              created_at: message.created_at || new Date().toISOString()
            };
          });
        } else if (Array.isArray(response)) {
          // 直接返回消息数组
          messages = response.map(message => {
            return {
              ...message,
              is_from_me: message.sender_id !== parseInt(userId),
              created_at: message.created_at || new Date().toISOString()
            };
          });
        }
        
        // 按时间排序
        messages.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
        
        // 获取对话伙伴信息
        if (response.conversation_with) {
          partner = response.conversation_with;
        } else {
          // 尝试从消息中获取伙伴信息
          const partnerMessage = messages.find(m => !m.is_from_me);
          if (partnerMessage) {
            partner = partnerMessage.sender || {};
            if (!partner.id) {
              partner.id = userId;
            }
          } else {
            // 如果没有消息或找不到伙伴信息，使用默认值
            partner = { id: userId, username: '用户' + userId };
          }
        }
        
        commit('SET_CONVERSATION', { 
          messages,
          user: userId
        });
        
        // 保存对话伙伴信息
        commit('SET_CONVERSATION_PARTNER', partner);
        
        // 标记为已读
        if (messages.length > 0) {
          commit('MARK_CONVERSATION_READ', userId);
        }
        
        return Promise.resolve(response);
      } catch (error) {
        console.error('获取对话失败:', error);
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
          ...(response.data || response), // 处理不同的响应格式
          is_from_me: true,
          sender_id: rootState.user.userInfo.id,
          recipient_id: recipientId,
          created_at: new Date().toISOString()
        };
        
        commit('ADD_MESSAGE', messageWithInfo);
        return Promise.resolve(response);
      } catch (error) {
        console.error('发送消息失败:', error);
        return Promise.reject(error);
      }
    },
    
    // 标记消息为已读
    async markAsRead({ commit }, { messageId, userId }) {
      try {
        if (messageId) {
          await markMessageAsRead(messageId);
        } else if (userId) {
          // 即使没有具体消息ID，也标记整个对话为已读
          console.log('标记用户对话为已读:', userId);
        }
        
        if (userId) {
          commit('MARK_CONVERSATION_READ', userId);
        }
        
        return Promise.resolve();
      } catch (error) {
        console.error('标记消息已读失败:', error);
        // 即使API调用失败，也尝试在前端标记为已读，提升用户体验
        if (userId) {
          commit('MARK_CONVERSATION_READ', userId);
        }
        return Promise.reject(error);
      }
    },
    
    // 检查关注状态
    async checkFollowStatus(_, { userId }) {
      try {
        const response = await checkFollowStatus(userId);
        return response;
      } catch (error) {
        console.error('获取关注状态失败:', error);
        return { is_following: false };
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