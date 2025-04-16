# 小说平台 API 接口文档

本文档详细描述了小说平台的所有API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [用户模块](#1-用户模块)
2. [小说模块](#2-小说模块)
3. [互动模块](#3-互动模块)
   - [3.1 发表评论](#31-发表评论)
   - [3.2 获取小说评论](#32-获取小说评论)
   - [3.3 获取章节评论](#33-获取章节评论)
   - [3.4 关注/取消关注用户](#34-关注取消关注用户)
   - [3.5 获取关注状态](#35-获取关注状态)
   - [3.6 获取粉丝列表](#36-获取粉丝列表)
   - [3.7 获取关注列表](#37-获取关注列表)
   - [3.8 收藏/取消收藏小说](#38-收藏取消收藏小说)
   - [3.9 获取收藏状态](#39-获取收藏状态)
   - [3.10 获取收藏列表](#310-获取收藏列表)
   - [3.11 获取阅读历史](#311-获取阅读历史)
   - [3.12 获取阅读进度](#312-获取阅读进度)
   - [3.13 发送私信](#313-发送私信)
   - [3.14 获取与特定用户的对话](#314-获取与特定用户的对话)
   - [3.15 获取收件箱](#315-获取收件箱)
   - [3.16 标记消息为已读](#316-标记消息为已读)
   - [3.17 删除评论](#317-删除评论)
   - [3.18 打赏作者](#318-打赏作者)
   - [3.19 获取收到的打赏](#319-获取收到的打赏)
   - [3.20 获取发出的打赏](#320-获取发出的打赏)
   - [3.21 获取用户评论历史](#321-获取用户评论历史)
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
  "username": "string", // 用户名（必填）
  "password": "string", // 密码（必填）
  "phone": "string",    // 手机号（可选，phone和email至少提供一个）
  "email": "string"     // 邮箱（可选，phone和email至少提供一个）
}
```

- **成功响应** (201 Created):

```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "created_at": "2023-01-01T00:00:00"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "错误信息" // 如：Username already exists, Email already exists, Password must be at least 6 characters long
}
```

### 1.2 用户登录

- **URL**: `/api/user/login`
- **方法**: `POST`
- **权限**: 无需登录
- **请求参数**:

```json
{
  // 以下三个至少提供一个
  "username": "string", // 用户名
  "phone": "string",    // 手机号
  "email": "string",    // 邮箱
  
  "password": "string"  // 密码（必填）
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "access_token": "string", // JWT令牌
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "user",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00",
    "status": "active"
  }
}
```

- **错误响应** (401 Unauthorized):

```json
{
  "success": false,
  "error": "错误信息" // 如：User not found, Invalid password, Your account is disabled
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
  "status": "active",
  "stats": {
    "collection_count": 0,
    "followers_count": 0,
    "following_count": 0
  }
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
  "email": "string",    // 可选
  "phone": "string",    // 可选
  "avatar": "string"    // 可选
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "user",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "status": "active",
    "stats": {
      "collection_count": 0,
      "followers_count": 0,
      "following_count": 0
    }
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "错误信息" // 如：No fields to update, Email already in use, Phone already in use
}
```

### 1.5 修改密码

> **注意: 此接口目前尚未实现，后端缺少 UserService.change_password 方法**

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

- **错误响应** (500 Internal Server Error):

```json
{
  // 当前会返回服务器错误，因为此方法尚未实现
  "error": "AttributeError: type object 'UserService' has no attribute 'change_password'"
}
```

### 1.6 管理员查看用户列表

- **URL**: `/api/user/admin/users`
- **方法**: `GET`
- **权限**: 管理员
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
  "users": [
    {
      // 用户信息
    }
  ]
}
```

- **错误响应** (403 Forbidden):

```json
{
  "error": "Admin privileges required"
}
```

### 1.7 管理员修改用户状态

- **URL**: `/api/user/admin/users/{target_user_id}/status`
- **方法**: `PUT`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `target_user_id`: 目标用户ID
- **请求参数**:

```json
{
  "status": true  // true为启用账户，false为禁用账户
}
```

- **成功响应** (200 OK):

```json
{
  "message": "User account enabled successfully", // 或 "User account disabled successfully"
  "user": {
    // 用户信息
  }
}
```

- **错误响应** (403 Forbidden):

```json
{
  "error": "Admin privileges required"
}
```

### 1.8 管理员修改用户角色

- **URL**: `/api/user/admin/users/{target_user_id}/role`
- **方法**: `PUT`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `target_user_id`: 目标用户ID
- **请求参数**:

```json
{
  "role": "string"  // 可选值: "user", "author", "admin"
}
```

- **成功响应** (200 OK):

```json
{
  "message": "User role updated successfully",
  "user": {
    // 用户信息
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "Invalid role" // 角色必须是 user, author 或 admin
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
      "novel_cover": "string",
      "novel_author": "string",
      "chapter_id": 1,
      "chapter_title": "string",
      "chapter_number": 5,
      "last_read_time": "2023-01-01T00:00:00",
      "progress": 0.75
    }
  ]
}
```

- **错误响应** (401 Unauthorized):

```json
{
  "error": "未授权" // Token缺失或无效
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
  "novel_title": "string",
  "current_chapter_id": 10,
  "current_chapter_number": 10,
  "current_chapter_title": "string",
  "progress_percentage": 0.5,
  "total_chapters": 100,
  "last_read_time": "2023-01-01T00:00:00"
}
```

- **错误响应** (404 Not Found):

```json
{
  "success": false,
  "error": "Novel not found"
}
```

或

```json
{
  "success": false,
  "error": "No reading history for this novel"
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

- **限制条件**:
  - 消息内容不能为空
  - 消息内容长度不能超过1000个字符
  - 不能给自己发送私信
  - **重要**：只有当接收者关注了发送者或发送者是管理员时，才能发送私信

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

- **错误响应** (400 Bad Request):

```json
{
  "error": "Message cannot be empty"
}
```

或

```json
{
  "error": "Message is too long (maximum 1000 characters)"
}
```

或

```json
{
  "error": "Cannot send message to yourself"
}
```

或

```json
{
  "error": "This user is not following you and cannot receive your messages"
}
```

或

```json
{
  "error": "User not found"
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

- **特性说明**:
  - 获取对话时，当前用户收到的未读消息会自动标记为已读

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

- **错误响应** (404 Not Found):

```json
{
  "error": "User not found"
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

### 3.18 打赏作者

- **URL**: `/api/interaction/tip`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "author_id": 1,      // 作者ID
  "novel_id": 1,       // 小说ID
  "amount": 100,       // 打赏金额（单位：分）
  "message": "string", // 打赏留言（可选）
  "chapter_id": 1      // 章节ID（可选）
}
```

- **限制条件**:
  - 打赏金额必须为正数
  - 留言长度不能超过200个字符
  - 小说必须存在且属于指定作者
  - 如果提供了章节ID，章节必须存在且属于指定小说

- **成功响应** (201 Created):

```json
{
  "message": "Successfully sent 1.00 to username",
  "tip": {
    "id": 1,
    "tipper_id": 2,
    "author_id": 1,
    "novel_id": 1,
    "chapter_id": 1,
    "amount": 100,
    "message": "string",
    "created_at": "2023-01-01T00:00:00"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "Author ID, novel ID, and amount are required"
}
```

或

```json
{
  "error": "Tip amount must be positive"
}
```

或

```json
{
  "error": "Message is too long (maximum 200 characters)"
}
```

或

```json
{
  "error": "Novel not found or does not belong to this author"
}
```

或

```json
{
  "error": "Chapter not found or does not belong to this novel"
}
```

### 3.19 获取收到的打赏

- **URL**: `/api/interaction/tips/received`
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
  "tips": [
    {
      "id": 1,
      "tipper_id": 2,
      "author_id": 1,
      "novel_id": 1,
      "chapter_id": 1,
      "amount": 100,
      "message": "string",
      "created_at": "2023-01-01T00:00:00",
      "tipper": {
        "id": 2,
        "username": "string",
        "avatar": "string"
      },
      "novel": {
        "id": 1,
        "title": "string"
      },
      "chapter": {
        "id": 1,
        "title": "string"
      }
    }
  ],
  "total_amount": 5000
}
```

### 3.20 获取发出的打赏

- **URL**: `/api/interaction/tips/sent`
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
  "tips": [
    {
      "id": 1,
      "tipper_id": 2,
      "author_id": 1,
      "novel_id": 1,
      "chapter_id": 1,
      "amount": 100,
      "message": "string",
      "created_at": "2023-01-01T00:00:00",
      "author": {
        "id": 1,
        "username": "string",
        "avatar": "string"
      },
      "novel": {
        "id": 1,
        "title": "string"
      },
      "chapter": {
        "id": 1,
        "title": "string"
      }
    }
  ],
  "total_amount": 5000
}
```

### 3.21 获取用户评论历史

- **URL**: `/api/interaction/user-comments`
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
  "comments": [
    {
      "id": 1,
      "user_id": 1,
      "novel_id": 1,
      "chapter_id": 5,
      "content": "string",
      "created_at": "2023-01-01T00:00:00",
      "likes": 10,
      "novel": {
        "id": 1,
        "title": "string",
        "cover": "string" 
      },
      "chapter": {
        "id": 5,
        "title": "string",
        "chapter_number": 5
      }
    }
  ]
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

### 5.1 小说搜索

- **URL**: `/api/search/novels`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `q`: 搜索关键词（标题或作者）
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 50)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "page": 1,
  "per_page": 20,
  "total_pages": 5,
  "results": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "view_count": 1000,
      "collection_count": 100,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00"
    }
  ]
}
```

### 5.2 标签搜索

- **URL**: `/api/search/novels/tag/{tag}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `tag`: 标签名称
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 50)

- **成功响应** (200 OK): 与小说搜索格式相同

### 5.3 相似小说推荐

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
      "view_count": 1000,
      "collection_count": 100,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00"
    }
  ]
}
```

## 6. 管理模块

本模块提供管理员使用的API接口，包括用户管理、内容审核、敏感词管理和数据统计等功能。

### 6.1 仪表盘统计

- **URL**: `/api/admin/dashboard`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **描述**: 获取管理员仪表盘统计数据，包括用户统计、内容统计和活动统计。

- **成功响应** (200 OK):

```json
{
  "user_stats": {
    "total_users": 100,
    "new_users_today": 5,
    "active_users_today": 30,
    "banned_users": 2
  },
  "content_stats": {
    "total_novels": 50,
    "total_chapters": 1500,
    "pending_moderation": 10,
    "rejected_content": 5
  },
  "activity_stats": {
    "comments_today": 25,
    "readings_today": 300,
    "tips_today": 10
  }
}
```

- **错误响应** (401 Unauthorized):

```json
{
  "error": "未授权操作"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "error": "需要管理员权限"
}
```

### 6.2 用户管理

#### 6.2.1 获取用户列表

- **URL**: `/api/admin/users`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)
  - `role`: 角色筛选 (可选，如：admin, user, author)

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "total_pages": 5,
  "page": 1,
  "per_page": 20,
  "users": [
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
  ]
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "无效的分页参数"
}
```

#### 6.2.2 管理用户状态

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
  "reason": "string", // 操作原因（必填）
  "duration": 7       // 禁用天数（仅当action为ban时可选，不提供则永久禁用）
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "User 5 has been banned", // 或 "User 5 has been unbanned"
  "action_id": 3 // 用户操作记录ID
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "缺少必要参数" // 或其他错误信息
}
```

#### 6.2.3 获取用户操作历史

- **URL**: `/api/admin/user-actions`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `user_id`: 目标用户ID（可选，用于筛选特定用户的操作记录）
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)

- **成功响应** (200 OK):

```json
{
  "total": 10,
  "total_pages": 1,
  "page": 1,
  "per_page": 20,
  "actions": [
    {
      "id": 1,
      "admin_id": 7,
      "target_user_id": 5,
      "action_type": "ban",
      "reason": "违反社区规则",
      "duration": 7,
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

### 6.3 敏感词管理

#### 6.3.1 获取敏感词列表

- **URL**: `/api/admin/sensitive-words`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `category`: 分类筛选（可选）
  - `page`: 页码（默认: 1）
  - `per_page`: 每页数量（默认: 50，最大: 200）

- **成功响应** (200 OK):

```json
{
  "total": 100,
  "total_pages": 2,
  "page": 1,
  "per_page": 50,
  "words": [
    {
      "id": 1,
      "word": "string",
      "level": 2,
      "category": "profanity",
      "added_by": 1,
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

#### 6.3.2 管理敏感词

- **URL**: `/api/admin/sensitive-words`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **描述**: 添加或删除敏感词

- **添加敏感词请求参数**:

```json
{
  "action": "add",        // 固定为 "add"
  "word": "string",       // 敏感词内容（必填）
  "level": 2,             // 敏感级别 (1-3)（必填）
  "category": "profanity" // 分类（必填）
}
```

- **删除敏感词请求参数**:

```json
{
  "action": "delete",  // 固定为 "delete"
  "word_id": 25        // 敏感词ID（必填）
}
```

- **成功响应-添加** (200 OK):

```json
{
  "success": true,
  "message": "Word 'test_sensitive_word' added to sensitive words list",
  "word": {
    "id": 25,
    "word": "test_sensitive_word",
    "level": 2,
    "category": "profanity",
    "added_by": 7,
    "created_at": "2023-01-01T00:00:00"
  }
}
```

- **成功响应-删除** (200 OK):

```json
{
  "success": true,
  "message": "Word deleted"
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "缺少必要参数" // 或其他错误信息，如"无效的敏感级别"
}
```

### 6.4 内容管理

#### 6.4.1 获取待审核内容

- **URL**: `/api/admin/content/{content_type}`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `content_type`: 内容类型，可选值："novel", "chapter", "comment"
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 50)

- **成功响应** (200 OK):

```json
{
  "total": 10,
  "total_pages": 1,
  "page": 1,
  "per_page": 20,
  "content_type": "novel",
  "content": [
    {
      "id": 1,
      "content_type": "novel",
      "content_id": 5,
      "title": "小说标题",
      "submitter_id": 3,
      "submitter_name": "作者用户名",
      "created_at": "2023-01-01T00:00:00",
      "content_summary": "内容摘要..."
    }
  ]
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "无效的内容类型: blog" // 不支持的content_type
}
```

#### 6.4.2 审核内容

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
  "message": "Content 5 has been approved", // 或 "Content 5 has been rejected"
  "audit": {
    "id": 3,
    "content_type": "novel",
    "content_id": 5,
    "status": "approved",
    "reason": null,
    "audited_by": 7,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-02T00:00:00"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "无效的状态" // 或 "拒绝时必须提供原因"
}
```

### 6.5 爬虫内容管理

#### 6.5.1 获取爬取的小说列表

- **URL**: `/api/admin/crawled-novels`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `status`: 状态筛选（可选，如：pending, approved, rejected）
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20)

- **成功响应** (200 OK):

```json
{
  "total": 10,
  "total_pages": 1,
  "page": 1,
  "per_page": 20,
  "novels": [
    {
      "id": 1,
      "title": "小说标题",
      "author": "作者名",
      "category": "科幻",
      "status": "pending",
      "chapter_count": 20,
      "source_site": "来源网站",
      "created_at": "2023-01-01T00:00:00"
    }
  ]
}
```

#### 6.5.2 获取爬取的小说章节

- **URL**: `/api/admin/crawled-novels/{novel_id}/chapters`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `novel_id`: 爬取的小说ID

- **成功响应** (200 OK):

```json
{
  "total": 20,
  "novel": {
    "id": 1,
    "title": "小说标题",
    "status": "pending"
  },
  "chapters": [
    {
      "id": 1,
      "novel_id": 1,
      "chapter_number": 1,
      "title": "第一章 标题",
      "content_length": 2500,
      "source_url": "http://example.com/chapter1"
    }
  ]
}
```

#### 6.5.3 管理爬取的小说

- **URL**: `/api/admin/crawled-novels/{novel_id}`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `novel_id`: 爬取的小说ID
- **请求参数**:

```json
{
  "action": "approve",  // "approve" 或 "reject"
  "reason": "string"    // 拒绝原因（action为reject时必填）
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Novel approved and moved to production" // 或 "Novel rejected"
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "无效的操作" // 或 "拒绝时必须提供原因"
}
```

### 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有管理员权限               |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     |

### 敏感词级别说明

| 级别 | 说明                                               | 处理方式                                             |
|------|----------------------------------------------------|----------------------------------------------------|
| 1    | 轻度敏感，一般为轻微不良词汇                       | 系统自动替换为星号                                   |
| 2    | 中度敏感，涉及政治、暴力等内容                     | 需人工审核，默认不通过审核                           |
| 3    | 高度敏感，严重违法违规内容                         | 内容直接拒绝，同时记录用户违规行为                   | 