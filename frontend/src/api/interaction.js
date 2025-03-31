import request from '@/utils/request';

/**
 * Post a comment
 * @param {Object} data - Comment data (novel_id, chapter_id, content, parent_id)
 * @returns {Promise}
 */
export function postComment(data) {
  return request({
    url: '/interaction/comment',
    method: 'post',
    data
  });
}

/**
 * Get comments for a novel
 * @param {Number} novelId - Novel ID
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getNovelComments(novelId, params) {
  return request({
    url: `/interaction/comments/${novelId}`,
    method: 'get',
    params
  });
}

/**
 * Follow a user/author
 * @param {Number} userId - User ID to follow
 * @returns {Promise}
 */
export function followUser(userId) {
  return request({
    url: '/interaction/follow',
    method: 'post',
    data: { user_id: userId }
  });
}

/**
 * Unfollow a user/author
 * @param {Number} userId - User ID to unfollow
 * @returns {Promise}
 */
export function unfollowUser(userId) {
  return request({
    url: '/interaction/follow',
    method: 'post',
    data: { user_id: userId }
  });
}

/**
 * Get followers list for a user
 * @param {Number} userId - User ID to get followers for
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getFollowers(userId, params) {
  return request({
    url: `/interaction/followers/${userId}`,
    method: 'get',
    params
  });
}

/**
 * Get following list for a user
 * @param {Number} userId - User ID to get following for
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getFollowing(userId, params) {
  return request({
    url: `/interaction/following/${userId}`,
    method: 'get',
    params
  });
}

/**
 * Send a private message to another user
 * @param {Object} data - Message data (recipient_id, content)
 * @returns {Promise}
 */
export function sendMessage(data) {
  return request({
    url: '/interaction/message',
    method: 'post',
    data
  });
}

/**
 * Get inbox with conversations
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getInbox(params) {
  return request({
    url: '/interaction/inbox',
    method: 'get',
    params
  });
}

/**
 * Get conversation messages with a specific user
 * @param {Number} userId - The user ID to get conversation with
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getConversation(userId, params) {
  return request({
    url: `/interaction/conversation/${userId}`,
    method: 'get',
    params
  });
}

/**
 * Mark message as read
 * @param {Number} messageId - The message ID to mark as read
 * @returns {Promise}
 */
export function markMessageAsRead(messageId) {
  return request({
    url: `/interaction/message/${messageId}/read`,
    method: 'post'
  });
}

/**
 * Check if user is following another user
 * @param {Number} userId - User ID to check
 * @returns {Promise}
 */
export function checkFollowStatus(userId) {
  return request({
    url: `/interaction/follow/status/${userId}`,
    method: 'get'
  });
}

/**
 * Get user's comments
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getUserComments(params) {
  return request({
    url: '/interaction/user-comments',
    method: 'get',
    params
  });
} 