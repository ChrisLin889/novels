import request from '@/utils/request'

/**
 * 获取作者统计信息
 * @returns {Promise}
 */
export function getAuthorStats() {
  return request({
    url: '/author/stats',
    method: 'get'
  })
}

/**
 * 获取作者的小说列表
 * @returns {Promise}
 */
export function getMyNovels() {
  return request({
    url: '/novel/author/novels',
    method: 'get'
  })
}

/**
 * 添加小说
 * @param {Object} data - 小说数据
 * @returns {Promise}
 */
export function addNovel(data) {
  console.log('添加小说API请求数据:', data);
  return request({
    url: '/novel/add',
    method: 'post',
    data
  })
}

/**
 * 更新小说
 * @param {Number} id - 小说ID
 * @param {Object} data - 小说更新数据
 * @returns {Promise}
 */
export function updateNovel(id, data) {
  console.log('更新小说API请求数据:', id, data);
  return request({
    url: `/novel/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除小说
 * @param {Number} id - 小说ID
 * @returns {Promise}
 */
export function deleteNovel(id) {
  return request({
    url: `/novel/${id}/delete`,
    method: 'delete'
  })
}

/**
 * 更新作者资料
 * @param {Object} data - 作者资料
 * @returns {Promise}
 */
export function updateAuthorProfile(data) {
  return request({
    url: '/author/profile',
    method: 'put',
    data
  })
}

/**
 * 提交作者申请
 * @param {Object} data - 申请数据
 * @returns {Promise}
 */
export function submitAuthorApplication(data) {
  return request({
    url: '/author/application',
    method: 'post',
    data
  })
}

/**
 * 获取作者申请历史
 * @returns {Promise}
 */
export function getAuthorApplications() {
  return request({
    url: '/author/applications',
    method: 'get'
  })
}

export function updateProfile(data) {
  return request({
    url: '/user/profile',
    method: 'put',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/user/password',
    method: 'put',
    data
  })
} 