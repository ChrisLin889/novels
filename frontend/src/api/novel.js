import request from '@/utils/request';

/**
 * Get novel list with optional filtering
 * @param {Object} params - Query parameters (page, per_page, category, status)
 * @returns {Promise}
 */
export function getNovelList(params) {
  return request({
    url: '/novel/list',
    method: 'get',
    params
  });
}

/**
 * Get novel detail by ID
 * @param {Number} id - Novel ID
 * @returns {Promise}
 */
export function getNovelDetail(id) {
  return request({
    url: `/novel/detail/${id}`,
    method: 'get'
  });
}

/**
 * Get chapter list for a novel
 * @param {Number} novelId - Novel ID
 * @param {Object} params - Query parameters (page, per_page)
 * @returns {Promise}
 */
export function getChapterList(novelId, params) {
  return request({
    url: `/novel/${novelId}/chapters`,
    method: 'get',
    params
  });
}

/**
 * Get chapter content
 * @param {Number} novelId - Novel ID
 * @param {Number} chapterNum - Chapter number
 * @returns {Promise}
 */
export function getChapterContent(novelId, chapterNum) {
  return request({
    url: `/novel/${novelId}/chapter/${chapterNum}`,
    method: 'get'
  });
}

/**
 * Get novels by category with filtering
 * @param {Object} params - Query parameters (category, status, sort, page, pageSize)
 * @returns {Promise}
 */
export function getNovelsByCategory(params) {
  return request({
    url: '/novel/list',
    method: 'get',
    params
  });
}

/**
 * Get rankings data
 * @param {Object} params - Query parameters (type, time, page, pageSize)
 * @returns {Promise}
 */
export function getRankings(params) {
  // 设置排行类型对应的排序字段
  let sortBy = '';
  switch(params.type) {
    case 'views':
      sortBy = 'view_count';
      break;
    case 'favorites':
      sortBy = 'collection_count';
      break;
    case 'recommends':
      sortBy = 'recommend_count';
      break;
    case 'comments':
      sortBy = 'comment_count';
      break;
    default:
      sortBy = 'view_count'; // 默认按阅读量排序
  }
  
  console.log('排行榜请求:', params.type, sortBy);
  
  const apiParams = {
    sort_by: sortBy,
    page: params.page || 1,
    per_page: params.per_page || 20,
    sort_order: 'desc' // 确保按降序排列
  };
  
  // 添加时间范围参数
  if (params.time && params.time !== 'all') {
    apiParams.time_range = params.time;
  }
  
  return request({
    url: '/novel/list',
    method: 'get',
    params: apiParams
  });
}

/**
 * Add novel to collection/bookshelf
 * @param {Number} novelId - Novel ID to add to collection
 * @returns {Promise}
 */
export function addToCollection(novelId) {
  return request({
    url: '/interaction/collection',
    method: 'post',
    data: { novel_id: novelId }
  });
}

/**
 * Remove novel from collection/bookshelf
 * @param {Number} novelId - Novel ID to remove from collection
 * @returns {Promise}
 */
export function removeFromCollection(novelId) {
  return request({
    url: '/interaction/collection',
    method: 'post',
    data: { novel_id: novelId }
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
 * Check if novel is in user's collection
 * @param {Number} novelId - Novel ID to check
 * @returns {Promise}
 */
export function checkCollection(novelId) {
  return request({
    url: `/interaction/collection/status/${novelId}`,
    method: 'get'
  });
} 