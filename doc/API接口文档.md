# 小说平台 API 接口文档

本文档详细描述了小说平台的所有API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [用户模块](#1-用户模块)
2. [小说模块](#2-小说模块)
3. [互动模块](#3-互动模块)
4. [缓存模块](#4-缓存模块)
5. [搜索模块](#5-搜索模块)
6. [管理模块](#6-管理模块)

## 1. 用户模块

### 1.1 用户注册

- **URL**: `/api/user/register`
- **方法**: `POST`
- **权限**: 无需登录
- **请求参数**:

```json
{
  "username": "string", // 用户名
  "password": "string", // 密码
  "phone": "string",    // 手机号（可选，phone和email至少提供一个）
  "email": "string"     // 邮箱（可选，phone和email至少提供一个）
}
```

- **成功响应** (201 Created):

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "user",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "status": "active"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "错误信息" // 如：Missing required fields, Email already registered
}
```

### 1.2 用户登录

- **URL**: `/api/user/login`
- **方法**: `POST`
- **权限**: 无需登录
- **请求参数**:

```json
{
  "phone": "string",    // 手机号（和email二选一）
  "email": "string",    // 邮箱（和phone二选一）
  "password": "string"  // 密码
}
```

- **成功响应** (200 OK):

```json
{
  "access_token": "string", // JWT令牌
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "user",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "status": "active"
  }
}
```

- **错误响应** (401 Unauthorized):

```json
{
  "error": "错误信息" // 如：User not found, Invalid password
}
```

### 1.3 获取个人信息

- **URL**: `/api/user/profile`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`

- **成功响应** (200 OK):

```json
{
  "id": 1,
  "username": "string",
  "phone": "string",
  "email": "string",
  "role": "user",
  "avatar": "string",
  "created_at": "2023-01-01T00:00:00",
  "status": "active"
}
```

- **错误响应** (401 Unauthorized):

```json
{
  "error": "未授权" // Token缺失或无效
}
```

### 1.4 修改个人信息

- **URL**: `/api/user/profile`
- **方法**: `PUT`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "username": "string",  // 可选
  "avatar": "string"     // 可选
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "user",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "status": "active"
  }
}
```

### 1.5 修改密码

- **URL**: `/api/user/change-password`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "current_password": "string",  // 当前密码
  "new_password": "string"       // 新密码
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Password changed successfully"
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "错误信息" // 如：Current password is incorrect
}
```

## 2. 小说模块

### 2.1 获取小说列表

- **URL**: `/api/novel/list`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)
  - `category`: 分类 (可选)
  - `status`: 状态 (可选, 连载/完结)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "novels": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "word_count": 100000,
      "view_count": 1000,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00"
    }
  ]
}
```

### 2.2 获取小说详情

- **URL**: `/api/novel/{id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "id": 1,
  "title": "string",
  "author": "string",
  "category": "string",
  "status": "ongoing",
  "cover": "string",
  "intro": "string",
  "word_count": 100000,
  "view_count": 1000,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-02T00:00:00",
  "chapters_count": 100,
  "latest_chapter": {
    "id": 100,
    "title": "string",
    "created_at": "2023-01-02T00:00:00"
  }
}
```

### 2.3 获取章节列表

- **URL**: `/api/novel/{id}/chapters`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `id`: 小说ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 50)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 2,
  "current_page": 1,
  "chapters": [
    {
      "id": 1,
      "chapter_number": 1,
      "title": "string",
      "word_count": 2000,
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

### 2.4 获取章节内容

- **URL**: `/api/novel/{id}/chapter/{num}`
- **方法**: `GET`
- **权限**: 无需登录（VIP章节需要登录）
- **路径参数**:
  - `id`: 小说ID
  - `num`: 章节编号

- **成功响应** (200 OK):

```json
{
  "id": 1,
  "novel_id": 1,
  "chapter_number": 1,
  "title": "string",
  "content": "string",
  "word_count": 2000,
  "created_at": "2023-01-01T00:00:00",
  "prev_chapter": null,
  "next_chapter": {
    "id": 2,
    "chapter_number": 2,
    "title": "string"
  }
}
```

## 3. 互动模块

### 3.1 发表评论

- **URL**: `/api/interaction/comment`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "novel_id": 1,           // 小说ID（和chapter_id二选一）
  "chapter_id": 1,         // 章节ID（可选）
  "content": "string"      // 评论内容
}
```

- **成功响应** (201 Created):

```json
{
  "message": "Comment added successfully",
  "comment": {
    "id": 1,
    "content": "string",
    "created_at": "2023-01-01T00:00:00",
    "user": {
      "id": 1,
      "username": "string",
      "avatar": "string"
    }
  }
}
```

### 3.2 获取小说评论

- **URL**: `/api/interaction/comments/{novel_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "comments": [
    {
      "id": 1,
      "content": "string",
      "created_at": "2023-01-01T00:00:00",
      "user": {
        "id": 1,
        "username": "string",
        "avatar": "string"
      }
    }
  ]
}
```

### 3.3 获取章节评论

- **URL**: `/api/interaction/comments/{novel_id}/chapter/{chapter_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
  - `chapter_id`: 章节ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK): 与获取小说评论格式相同

### 3.4 关注/取消关注用户

- **URL**: `/api/interaction/follow`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "user_id": 1  // 要关注/取消关注的用户ID
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Following username",
  "is_following": true
}
```

或

```json
{
  "message": "Unfollowed username",
  "is_following": false
}
```

### 3.5 获取关注状态

- **URL**: `/api/interaction/follow/status/{user_id}`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `user_id`: 用户ID

- **成功响应** (200 OK):

```json
{
  "is_following": true
}
```

### 3.6 获取粉丝列表

- **URL**: `/api/interaction/followers/{user_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `user_id`: 用户ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "followers": [
    {
      "id": 1,
      "username": "string",
      "avatar": "string",
      "followed_at": "2023-01-01T00:00:00"
    }
  ]
}
```

### 3.7 获取关注列表

- **URL**: `/api/interaction/following/{user_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `user_id`: 用户ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "following": [
    {
      "id": 1,
      "username": "string",
      "avatar": "string",
      "followed_at": "2023-01-01T00:00:00"
    }
  ]
}
```

### 3.8 收藏/取消收藏小说

- **URL**: `/api/interaction/collection`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "novel_id": 1  // 小说ID
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Added to collection",
  "is_collected": true
}
```

或

```json
{
  "message": "Removed from collection",
  "is_collected": false
}
```

### 3.9 获取收藏状态

- **URL**: `/api/interaction/collection/status/{novel_id}`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "is_collected": true
}
```

### 3.10 获取收藏列表

- **URL**: `/api/interaction/collection`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 10)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "collections": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "collection_time": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00",
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

### 3.11 获取阅读历史

- **URL**: `/api/interaction/history`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 10)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "history": [
    {
      "novel_id": 1,
      "novel_title": "string",
      "chapter_id": 1,
      "chapter_title": "string",
      "read_at": "2023-01-01T00:00:00",
      "progress": 0.75
    }
  ]
}
```

### 3.12 获取阅读进度

- **URL**: `/api/interaction/progress/{novel_id}`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "success": true,
  "novel_id": 1,
  "current_chapter_id": 10,
  "current_chapter_number": 10,
  "current_chapter_title": "string",
  "progress_percentage": 0.5,
  "total_chapters": 100
}
```

### 3.13 发送私信

- **URL**: `/api/interaction/message`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "recipient_id": 1,   // 收件人ID
  "content": "string"  // 私信内容
}
```

- **成功响应** (201 Created):

```json
{
  "message": "Message sent successfully",
  "data": {
    "id": 1,
    "sender_id": 1,
    "recipient_id": 2,
    "content": "string",
    "created_at": "2023-01-01T00:00:00",
    "is_read": false,
    "read_at": null,
    "sender": {
      "id": 1,
      "username": "string",
      "avatar": "string",
      "email": "string",
      "phone": "string",
      "status": "active",
      "role": "user",
      "created_at": "2023-01-01T00:00:00"
    }
  }
}
```

### 3.14 获取与特定用户的对话

- **URL**: `/api/interaction/conversation/{user_id}`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `user_id`: 对话用户ID
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 50)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "messages": [
    {
      "id": 1,
      "sender_id": 1,
      "recipient_id": 2,
      "content": "string",
      "created_at": "2023-01-01T00:00:00",
      "is_read": true,
      "read_at": "2023-01-01T00:05:00",
      "sender": {
        "id": 1,
        "username": "string",
        "avatar": "string",
        "created_at": "2023-01-01T00:00:00",
        "email": "string",
        "phone": "string",
        "status": "active",
        "role": "user"
      }
    }
  ]
}
```

### 3.15 获取收件箱

- **URL**: `/api/interaction/inbox`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "messages": [
    {
      "id": 1,
      "sender_id": 1,
      "recipient_id": 2,
      "content": "string",
      "created_at": "2023-01-01T00:00:00",
      "is_read": false,
      "read_at": null,
      "sender": {
        "id": 1,
        "username": "string",
        "avatar": "string",
        "created_at": "2023-01-01T00:00:00",
        "email": "string",
        "phone": "string",
        "status": "active",
        "role": "user"
      }
    }
  ],
  "unread_count": 5
}
```

### 3.16 标记消息为已读

- **URL**: `/api/interaction/message/{message_id}/read`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `message_id`: 消息ID

- **成功响应** (200 OK):

```json
{
  "message": "Message marked as read"
}
```

### 3.17 删除评论

- **URL**: `/api/interaction/comment/{comment_id}`
- **方法**: `DELETE`
- **权限**: 用户登录（仅评论作者或管理员可删除）
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `comment_id`: 评论ID

- **成功响应** (200 OK):

```json
{
  "message": "Comment deleted successfully"
}
```

## 4. 缓存模块

### 4.1 刷新缓存

- **URL**: `/api/cache/refresh`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`

- **成功响应** (200 OK):

```json
{
  "message": "Cache refreshed successfully"
}
```

### 4.2 清空缓存

- **URL**: `/api/cache/clear`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`

- **成功响应** (200 OK):

```json
{
  "message": "Cache cleared successfully"
}
```

## 5. 搜索模块

### 5.1 关键词搜索

- **URL**: `/api/search/keyword`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `q`: 关键词
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "results": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "word_count": 100000,
      "view_count": 1000,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00"
    }
  ]
}
```

### 5.2 高级搜索

- **URL**: `/api/search/advanced`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `keyword`: 关键词 (可选)
  - `category`: 分类 (可选)
  - `status`: 状态 (可选)
  - `min_words`: 最小字数 (可选)
  - `max_words`: 最大字数 (可选)
  - `sort_by`: 排序字段 (可选, 更新时间/点击量)
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "results": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "word_count": 100000,
      "view_count": 1000,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00"
    }
  ]
}
```

### 5.3 热门搜索词

- **URL**: `/api/search/trending`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `limit`: 返回数量 (默认: 10)

- **成功响应** (200 OK):

```json
{
  "keywords": [
    {
      "keyword": "string",
      "count": 100
    }
  ]
}
```

### 5.4 相似小说推荐

- **URL**: `/api/search/similar/{novel_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
- **查询参数**:
  - `limit`: 返回数量 (默认: 5)

- **成功响应** (200 OK):

```json
{
  "novels": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "cover": "string",
      "similarity": 0.85
    }
  ]
}
```

## 6. 管理模块

### 6.1 获取用户列表 (管理员)

- **URL**: `/api/admin/users`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)
  - `role`: 角色筛选 (可选)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "users": [
    {
      "id": 1,
      "username": "string",
      "phone": "string",
      "email": "string",
      "role": "user",
      "avatar": "string",
      "created_at": "2023-01-01T00:00:00",
      "status": "active",
      "ban_until": null
    }
  ]
}
```

### 6.2 管理用户状态 (禁用/启用)

- **URL**: `/api/admin/users/{user_id}`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `user_id`: 用户ID
- **请求参数**:

```json
{
  "action": "ban",    // "ban" 或 "unban"
  "reason": "string", // 操作原因
  "duration": 7       // 禁用天数（仅当action为ban时需要）
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "User banned successfully",
  "user": {
    "id": 1,
    "username": "string",
    "status": "banned",
    "ban_until": "2023-01-08T00:00:00"
  }
}
```

### 6.3 敏感词管理

- **URL**: `/api/admin/sensitive-words`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "action": "add",        // "add" 或 "delete"
  "word": "string",       // 敏感词
  "level": 2,             // 敏感级别 (1-3)
  "category": "profanity" // 分类
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Sensitive word added successfully",
  "word": {
    "id": 1,
    "word": "string",
    "level": 2,
    "category": "profanity",
    "added_by": 1,
    "created_at": "2023-01-01T00:00:00"
  }
}
```

### 6.4 内容审核

- **URL**: `/api/admin/content/audit/{audit_id}`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `audit_id`: 审核内容ID
- **请求参数**:

```json
{
  "status": "approved",  // "approved" 或 "rejected"
  "reason": "string"     // 拒绝原因（status为rejected时必填）
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Content approved successfully"
}
``` 