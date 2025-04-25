import request from '@/utils/request';

// 获取所有小说
export function getAllNovels(params) {
  return request({
    url: '/admin/novels',
    method: 'get',
    params
  });
}

// 获取所有章节
export function getAllChapters(params) {
  return request({
    url: '/admin/chapters',
    method: 'get',
    params
  });
}

// 获取所有评论
export function getAllComments(params) {
  return request({
    url: '/admin/comments',
    method: 'get',
    params
  });
}

// 删除小说（移至回收站）
export function deleteNovel(novelId) {
  return request({
    url: `/admin/novels/${novelId}`,
    method: 'delete'
  });
}

// 删除章节（移至回收站）
export function deleteChapter(chapterId) {
  return request({
    url: `/admin/chapters/${chapterId}`,
    method: 'delete'
  });
}

// 删除评论（移至回收站）
export function deleteComment(commentId) {
  return request({
    url: `/admin/comments/${commentId}`,
    method: 'delete'
  });
}

// ======= 回收站功能 =======

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