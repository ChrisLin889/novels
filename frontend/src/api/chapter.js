import request from '@/utils/request'

export function getChapters(novelId) {
  return request({
    url: `/novel/${novelId}/chapters`,
    method: 'get'
  })
}

export function getChapterDetail(chapterId) {
  return request({
    url: `/novel/chapters/${chapterId}`,
    method: 'get'
  })
}

export function addChapter(novelId, data) {
  return request({
    url: `/novel/${novelId}/chapters`,
    method: 'post',
    data
  })
}

export function updateChapter(chapterId, data) {
  return request({
    url: `/novel/chapters/${chapterId}`,
    method: 'put',
    data
  })
}

export function deleteChapter(chapterId) {
  return request({
    url: `/novel/chapters/${chapterId}`,
    method: 'delete'
  })
} 