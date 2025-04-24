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
 * Get comments for a chapter
 * @param {Number} novelId - Novel ID
 * @param {Number} chapterId - Chapter ID
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getChapterComments(novelId, chapterId, params) {
  return request({
    url: `/interaction/comments/${novelId}/chapter/${chapterId}`,
    method: 'get',
    params
  });
}

/**
 * Delete a comment
 * @param {Number} commentId - Comment ID
 * @returns {Promise}
 */
export function deleteComment(commentId) {
  return request({
    url: `/interaction/comment/${commentId}`,
    method: 'delete'
  });
}

/**
 * Follow/unfollow a user
 * @param {Number} userId - User ID to follow/unfollow
 * @returns {Promise}
 */
export function toggleFollow(userId) {
  return request({
    url: '/interaction/follow',
    method: 'post',
    data: { target_user_id: userId }
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
 * Get user's comments
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getUserComments(params) {
  return request({
    url: '/interaction/user/comments',
    method: 'get',
    params
  });
}

/**
 * Add/Remove novel from collection
 * @param {Number} novelId - Novel ID 
 * @returns {Promise}
 */
export function toggleCollection(novelId) {
  return request({
    url: '/interaction/collection',
    method: 'post',
    data: { novel_id: novelId }
  });
}

/**
 * Check if novel is in user's collection
 * @param {Number} novelId - Novel ID to check
 * @returns {Promise}
 */
export function checkCollectionStatus(novelId) {
  return request({
    url: `/interaction/collection/status/${novelId}`,
    method: 'get'
  });
}

/**
 * Get user's collection/bookshelf
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getUserCollection(params) {
  return request({
    url: '/interaction/collection',
    method: 'get',
    params
  });
}

/**
 * Get reading history
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getReadingHistory(params) {
  return request({
    url: '/interaction/history',
    method: 'get',
    params
  });
}

/**
 * Get reading progress for a novel
 * @param {Number} novelId - Novel ID
 * @returns {Promise}
 */
export function getReadingProgress(novelId) {
  return request({
    url: `/interaction/progress/${novelId}`,
    method: 'get'
  });
} 