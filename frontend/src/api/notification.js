import request from '@/utils/request';

/**
 * 获取当前用户的通知列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @returns {Promise}
 */
export const getNotifications = async (params = {}) => {
  try {
    const response = await request({
      url: '/notification',
      method: 'get',
      params
    });
    return response;
  } catch (error) {
    console.error('获取通知列表失败:', error);
    throw error.response?.data?.error || '获取通知列表失败';
  }
};

/**
 * 将通知标记为已读
 * @param {number} notificationId - 通知ID
 * @returns {Promise}
 */
export const markNotificationRead = async (notificationId) => {
  try {
    const response = await request({
      url: `/notification/${notificationId}/read`,
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('标记通知已读失败:', error);
    throw error.response?.data?.error || '标记通知已读失败';
  }
};

/**
 * 将所有通知标记为已读
 * @returns {Promise}
 */
export const markAllNotificationsRead = async () => {
  try {
    const response = await request({
      url: '/notification/read-all',
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('标记所有通知已读失败:', error);
    throw error.response?.data?.error || '标记所有通知已读失败';
  }
}; 