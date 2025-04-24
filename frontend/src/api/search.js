import request from '@/utils/request';

/**
 * Search novels by keywords
 * @param {Object} params - Search parameters (q, page, per_page)
 * @returns {Promise}
 */
export function searchNovels(params) {
  return request({
    url: '/search/novels',
    method: 'get',
    params: {
      q: params.q,
      page: params.page || 1,
      per_page: params.per_page || 20
    }
  });
}

/**
 * Search novels by tag
 * @param {Object} params - Search parameters (tag, page, per_page)
 * @returns {Promise}
 */
export function searchByTag(params) {
  return request({
    url: `/search/novels/tag/${params.tag}`,
    method: 'get',
    params: {
      page: params.page || 1,
      per_page: params.per_page || 20
    }
  });
}

/**
 * Get similar novels
 * @param {Object} params - Search parameters (novel_id, limit)
 * @returns {Promise}
 */
export function getSimilarNovels(params) {
  return request({
    url: `/search/similar/${params.novel_id}`,
    method: 'get',
    params: {
      limit: params.limit || 5
    }
  });
}

/**
 * Get hot tags
 * @param {Object} params - Query parameters (limit, category_id)
 * @returns {Promise}
 */
export function getHotTags(params = {}) {
  return request({
    url: '/search/tags/hot',
    method: 'get',
    params: {
      limit: params.limit || 20,
      category_id: params.category_id
    }
  });
} 