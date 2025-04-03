import axios from 'axios';

const API_URL = '/api/admin';

/**
 * 获取管理员仪表盘统计数据
 */
export const getDashboardStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/dashboard`);
    return response.data;
  } catch (error) {
    console.error('获取仪表盘数据失败:', error);
    throw error.response?.data?.error || '获取仪表盘数据失败';
  }
};

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {string} params.role - 角色筛选
 */
export const getUsers = async (params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/users`, { params });
    return response.data;
  } catch (error) {
    console.error('获取用户列表失败:', error);
    throw error.response?.data?.error || '获取用户列表失败';
  }
};

/**
 * 管理用户状态（禁用/启用）
 * @param {number} userId - 用户ID
 * @param {Object} data - 用户状态数据
 * @param {string} data.action - 操作类型：'ban' 或 'unban'
 * @param {string} data.reason - 操作原因
 * @param {number} data.duration - 禁用天数（仅在 ban 操作时可选）
 */
export const manageUser = async (userId, data) => {
  try {
    const response = await axios.post(`${API_URL}/users/${userId}`, data);
    return response.data;
  } catch (error) {
    console.error('管理用户状态失败:', error);
    throw error.response?.data?.error || '管理用户状态失败';
  }
};

/**
 * 获取用户操作历史
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {number} params.user_id - 目标用户ID（可选）
 */
export const getUserActions = async (params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/user-actions`, { params });
    return response.data;
  } catch (error) {
    console.error('获取用户操作历史失败:', error);
    throw error.response?.data?.error || '获取用户操作历史失败';
  }
};

/**
 * 获取敏感词列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {string} params.category - 分类筛选（可选）
 */
export const getSensitiveWords = async (params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/sensitive-words`, { params });
    return response.data;
  } catch (error) {
    console.error('获取敏感词列表失败:', error);
    throw error.response?.data?.error || '获取敏感词列表失败';
  }
};

/**
 * 添加敏感词
 * @param {Object} data - 敏感词数据
 * @param {string} data.word - 敏感词内容
 * @param {number} data.level - 敏感级别（1-3）
 * @param {string} data.category - 分类
 */
export const addSensitiveWord = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/sensitive-words`, {
      action: 'add',
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('添加敏感词失败:', error);
    throw error.response?.data?.error || '添加敏感词失败';
  }
};

/**
 * 删除敏感词
 * @param {number} wordId - 敏感词ID
 */
export const deleteSensitiveWord = async (wordId) => {
  try {
    const response = await axios.post(`${API_URL}/sensitive-words`, {
      action: 'delete',
      word_id: wordId
    });
    return response.data;
  } catch (error) {
    console.error('删除敏感词失败:', error);
    throw error.response?.data?.error || '删除敏感词失败';
  }
};

/**
 * 获取待审核内容
 * @param {string} contentType - 内容类型：'novel', 'chapter', 'comment'
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 */
export const getPendingContent = async (contentType, params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/content/${contentType}`, { params });
    return response.data;
  } catch (error) {
    console.error('获取待审核内容失败:', error);
    throw error.response?.data?.error || '获取待审核内容失败';
  }
};

/**
 * 审核内容
 * @param {number} auditId - 审核内容ID
 * @param {Object} data - 审核数据
 * @param {string} data.status - 状态：'approved' 或 'rejected'
 * @param {string} data.reason - 拒绝原因（status为rejected时必填）
 */
export const auditContent = async (auditId, data) => {
  try {
    const response = await axios.post(`${API_URL}/content/audit/${auditId}`, data);
    return response.data;
  } catch (error) {
    console.error('审核内容失败:', error);
    throw error.response?.data?.error || '审核内容失败';
  }
};

/**
 * 获取爬取的小说列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {string} params.status - 状态筛选（可选）
 */
export const getCrawledNovels = async (params = {}) => {
  try {
    const response = await axios.get(`${API_URL}/crawled-novels`, { params });
    return response.data;
  } catch (error) {
    console.error('获取爬取的小说列表失败:', error);
    throw error.response?.data?.error || '获取爬取的小说列表失败';
  }
};

/**
 * 获取爬取的小说章节
 * @param {number} novelId - 爬取的小说ID
 */
export const getCrawledChapters = async (novelId) => {
  try {
    const response = await axios.get(`${API_URL}/crawled-novels/${novelId}/chapters`);
    return response.data;
  } catch (error) {
    console.error('获取爬取的小说章节失败:', error);
    throw error.response?.data?.error || '获取爬取的小说章节失败';
  }
};

/**
 * 管理爬取的小说
 * @param {number} novelId - 爬取的小说ID
 * @param {Object} data - 管理数据
 * @param {string} data.action - 操作：'approve' 或 'reject'
 * @param {string} data.reason - 拒绝原因（action为reject时必填）
 */
export const manageCrawledNovel = async (novelId, data) => {
  try {
    const response = await axios.post(`${API_URL}/crawled-novels/${novelId}`, data);
    return response.data;
  } catch (error) {
    console.error('管理爬取的小说失败:', error);
    throw error.response?.data?.error || '管理爬取的小说失败';
  }
}; 