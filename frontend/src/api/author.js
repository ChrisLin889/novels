import request from '@/utils/request'

// 获取作者统计信息
export function getAuthorStats() {
  return request({
    url: '/novel/author/stats',
    method: 'get'
  })
}

// 获取作者的小说列表
export function getMyNovels() {
  return request({
    url: '/novel/my',
    method: 'get'
  })
}

// 添加小说
export function addNovel(data) {
  console.log('添加小说API请求数据:', data);
  return request({
    url: '/novel/add',
    method: 'post',
    data
  })
}

// 更新小说
export function updateNovel(id, data) {
  console.log('更新小说API请求数据:', id, data);
  return request({
    url: `/novel/${id}`,
    method: 'put',
    data
  })
}

// 删除小说
export function deleteNovel(id) {
  return request({
    url: `/novel/${id}/delete`,
    method: 'delete'
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