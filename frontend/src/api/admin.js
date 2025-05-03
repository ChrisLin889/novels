import request from '@/utils/request';

/**
 * 获取管理员仪表盘统计数据
 * @returns {Promise}
 */
export const getDashboardStats = async () => {
  try {
    const response = await request({
      url: '/admin/dashboard',
      method: 'get'
    });
    return response;
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
 * @returns {Promise}
 */
export const getUsers = async (params = {}) => {
  try {
    const response = await request({
      url: '/admin/users',
      method: 'get',
      params
    });
    return response;
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
 * @returns {Promise}
 */
export const manageUser = async (userId, data) => {
  try {
    const response = await request({
      url: `/admin/users/${userId}`,
      method: 'post',
      data
    });
    return response;
  } catch (error) {
    console.error('管理用户状态失败:', error);
    throw error.response?.data?.error || '管理用户状态失败';
  }
};

/**
 * 更新用户角色
 * @param {number} userId - 用户ID
 * @param {string} role - 新角色
 * @returns {Promise}
 */
export const updateUserRole = async (userId, role) => {
  try {
    const response = await request({
      url: `/admin/users/${userId}/role`,
      method: 'put',
      data: { role }
    });
    return response;
  } catch (error) {
    console.error('更新用户角色失败:', error);
    throw error.response?.data?.error || '更新用户角色失败';
  }
};

/**
 * 获取用户操作历史
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {number} params.user_id - 目标用户ID（可选）
 * @returns {Promise}
 */
export const getUserActions = async (params = {}) => {
  try {
    const response = await request({
      url: '/admin/user-actions',
      method: 'get',
      params
    });
    return response;
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
 * @returns {Promise}
 */
export const getSensitiveWords = async (params = {}) => {
  try {
    const response = await request({
      url: '/admin/sensitive-words',
      method: 'get',
      params
    });
    return response;
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
 * @returns {Promise}
 */
export const addSensitiveWord = async (data) => {
  try {
    const response = await request({
      url: '/admin/sensitive-words',
      method: 'post',
      data: {
        action: 'add',
        ...data
      }
    });
    return response;
  } catch (error) {
    console.error('添加敏感词失败:', error);
    throw error.response?.data?.error || '添加敏感词失败';
  }
};

/**
 * 删除敏感词
 * @param {number} wordId - 敏感词ID
 * @returns {Promise}
 */
export const deleteSensitiveWord = async (wordId) => {
  try {
    const response = await request({
      url: '/admin/sensitive-words',
      method: 'post',
      data: {
        action: 'delete',
        word_id: wordId
      }
    });
    return response;
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
 * @returns {Promise}
 */
export const getPendingContent = async (contentType, params = {}) => {
  try {
    const response = await request({
      url: `/admin/content/${contentType}`,
      method: 'get',
      params
    });
    return response;
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
 * @returns {Promise}
 */
export const auditContent = async (auditId, data) => {
  try {
    const response = await request({
      url: `/admin/content/audit/${auditId}`,
      method: 'post',
      data
    });
    return response;
  } catch (error) {
    console.error('审核内容失败:', error);
    throw error.response?.data?.error || '审核内容失败';
  }
};

/**
 * 获取待处理作者申请
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.per_page - 每页数量
 * @param {string} params.status - 状态筛选（可选）
 * @returns {Promise}
 */
export const getAuthorApplications = async (params = {}) => {
  try {
    const response = await request({
      url: '/admin/author-applications',
      method: 'get',
      params
    });
    return response;
  } catch (error) {
    console.error('获取作者申请列表失败:', error);
    throw error.response?.data?.error || '获取作者申请列表失败';
  }
};

/**
 * 处理作者申请
 * @param {number} applicationId - 申请ID
 * @param {Object} data - 处理数据
 * @param {string} data.status - 状态：'approved' 或 'rejected'
 * @param {string} data.comment - 处理意见（可选）
 * @returns {Promise}
 */
export const processAuthorApplication = async (applicationId, data) => {
  try {
    const response = await request({
      url: `/admin/author-applications/${applicationId}`,
      method: 'post',
      data
    });
    return response;
  } catch (error) {
    console.error('处理作者申请失败:', error);
    throw error.response?.data?.error || '处理作者申请失败';
  }
};

/**
 * 触发内容敏感词扫描和替换
 * @returns {Promise}
 */
export const scanContentForSensitiveWords = async () => {
  try {
    const response = await request({
      url: '/admin/content-scan',
      method: 'post'
    });
    return response;
  } catch (error) {
    console.error('内容扫描失败:', error);
    throw error.response?.data?.error || '内容扫描失败';
  }
};

// ======= 回收站功能 =======

// 获取所有小说（用于下拉选择）
export function getAllNovels() {
  return request({
    url: '/novel/list',
    method: 'get',
    params: { per_page: 1000 }  // 获取大量小说用于选择
  });
}

// 通过小说ID获取章节列表
export function getChaptersByNovelId(novelId) {
  return request({
    url: `/novel/${novelId}/chapters`,
    method: 'get',
    params: { per_page: 1000 }  // 获取大量章节用于选择
  });
}

// 获取回收站中的小说
export function getRecycledNovels(params) {
  return request({
    url: '/admin/recycle-bin/novels',
    method: 'get',
    params
  });
}

// 获取回收站中的章节
export function getRecycledChapters(params) {
  return request({
    url: '/admin/recycle-bin/chapters',
    method: 'get',
    params
  });
}

// 获取回收站中的评论
export function getRecycledComments(params) {
  return request({
    url: '/admin/recycle-bin/comments',
    method: 'get',
    params
  });
}

// 还原小说
export function restoreNovel(novelId) {
  return request({
    url: `/admin/recycle-bin/novels/${novelId}/restore`,
    method: 'post'
  });
}

// 还原章节
export function restoreChapter(chapterId) {
  return request({
    url: `/admin/recycle-bin/chapters/${chapterId}/restore`,
    method: 'post'
  });
}

// 还原评论
export function restoreComment(commentId) {
  return request({
    url: `/admin/recycle-bin/comments/${commentId}/restore`,
    method: 'post'
  });
}

// 永久删除回收站中的小说
export function permanentlyDeleteNovel(novelId) {
  return request({
    url: `/admin/recycle-bin/novels/${novelId}/permanent`,
    method: 'delete'
  });
}

// 永久删除回收站中的章节
export function permanentlyDeleteChapter(chapterId) {
  return request({
    url: `/admin/recycle-bin/chapters/${chapterId}/permanent`,
    method: 'delete'
  });
}

// 永久删除回收站中的评论
export function permanentlyDeleteComment(commentId) {
  return request({
    url: `/admin/recycle-bin/comments/${commentId}/permanent`,
    method: 'delete'
  });
} 