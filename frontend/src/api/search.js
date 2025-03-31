import request from '@/utils/request';

/**
 * Search novels by keywords and optional filters
 * @param {Object} params - Search parameters (keyword, category, status, page, per_page)
 * @returns {Promise}
 */
export function searchNovels(params) {
  return request({
    url: '/search/keyword',
    method: 'get',
    params
  });
} 