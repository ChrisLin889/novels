# 互动模块 API 文档

本文档详细描述了小说平台互动模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [评论功能](#1-评论功能)
   - [1.1 发表评论](#11-发表评论)
   - [1.2 获取小说评论](#12-获取小说评论)
   - [1.3 获取章节评论](#13-获取章节评论)
   - [1.4 删除评论](#14-删除评论)
   - [1.5 获取用户评论历史](#15-获取用户评论历史)
2. [关注功能](#2-关注功能)
   - [2.1 关注/取消关注用户](#21-关注取消关注用户)
   - [2.2 获取关注状态](#22-获取关注状态)
   - [2.3 获取粉丝列表](#23-获取粉丝列表)
   - [2.4 获取关注列表](#24-获取关注列表)
3. [收藏功能](#3-收藏功能)
   - [3.1 收藏/取消收藏小说](#31-收藏取消收藏小说)
   - [3.2 获取收藏状态](#32-获取收藏状态)
   - [3.3 获取收藏列表](#33-获取收藏列表)
4. [阅读功能](#4-阅读功能)
   - [4.1 获取阅读历史](#41-获取阅读历史)
   - [4.2 获取阅读进度](#42-获取阅读进度)
5. [私信功能](#5-私信功能)
   - [5.1 发送私信](#51-发送私信)
   - [5.2 获取与特定用户的对话](#52-获取与特定用户的对话)
   - [5.3 获取收件箱](#53-获取收件箱)
   - [5.4 标记消息为已读](#54-标记消息为已读)

## 1. 评论功能

### 1.1 发表评论

- **URL**: `/api/interaction/comment`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "novel_id": 6,         // 小说ID（必填）
  "content": "string",   // 评论内容（必填）
  "chapter_id": 15,      // 章节ID（可选，仅在对章节发表评论时需要）
  "parent_id": 2         // 父评论ID（可选，用于回复其他评论）
}
```

**注意事项**：
- 当发表小说级别评论时，`chapter_id`可以省略、设为null或0
- 当发表章节评论时，必须提供有效的`chapter_id`
- 系统会检查章节是否存在以及是否属于指定小说

- **成功响应** (201 Created):

```json
{
  "message": "Comment added successfully",
  "comment": {
    "id": 1,
    "content": "string",
    "created_at": "2025-04-03T14:45:51",
    "user": {
      "id": 1,
      "username": "string",
      "avatar": "string"
    }
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "Novel ID and content are required"
}
```

或

```json
{
  "error": "Invalid chapter"
}
```

### 1.2 获取小说评论

- **URL**: `/api/interaction/comments/{novel_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "comments": [
    {
      "id": 1,
      "content": "string",
      "created_at": "2025-04-03T14:45:51",
      "user": {
        "id": 1,
        "username": "string",
        "avatar": "string"
      }
    }
  ]
}
```

### 1.3 获取章节评论

- **URL**: `/api/interaction/comments/{novel_id}/chapter/{chapter_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
  - `chapter_id`: 章节ID
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK): 与获取小说评论格式相同

### 1.4 删除评论

- **URL**: `/api/interaction/comment/{comment_id}`
- **方法**: `DELETE`
- **权限**: 需要登录（用户只能删除自己的评论，管理员可删除任何评论）
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `comment_id`: 评论ID

- **成功响应** (200 OK):

```json
{
  "message": "Comment deleted successfully"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "error": "Permission denied: Cannot delete other users' comments"
}
```

### 1.5 获取用户评论历史

- **URL**: `/api/interaction/user/comments`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "comments": [
    {
      "id": 1,
      "content": "string",
      "created_at": "2025-04-03T14:45:51",
      "novel": {
        "id": 6,
        "title": "string"
      }
    }
  ]
}
```

## 2. 关注功能

### 2.1 关注/取消关注用户

- **URL**: `/api/interaction/follow`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "target_user_id": 2  // 目标用户ID
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Successfully followed the user" | "Successfully unfollowed the user",
  "is_following": true | false
}
```

### 2.2 获取关注状态

- **URL**: `/api/interaction/follow/status/{target_user_id}`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `target_user_id`: 目标用户ID

- **成功响应** (200 OK):

```json
{
  "is_following": true | false
}
```

### 2.3 获取粉丝列表

- **URL**: `/api/interaction/followers/{user_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `user_id`: 用户ID，要查看其粉丝列表的用户
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 5,
  "pages": 1,
  "current_page": 1,
  "followers": [
    {
      "id": 2,
      "username": "string",
      "avatar": "string",
      "followed_at": "2025-04-03T11:25:36"
    }
  ]
}
```

### 2.4 获取关注列表

- **URL**: `/api/interaction/following/{user_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `user_id`: 用户ID，要查看其关注列表的用户
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 3,
  "pages": 1,
  "current_page": 1,
  "following": [
    {
      "id": 3,
      "username": "string",
      "avatar": "string",
      "followed_at": "2025-04-03T12:45:22"
    }
  ]
}
```

## 3. 收藏功能

### 3.1 收藏/取消收藏小说

- **URL**: `/api/interaction/collection`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "novel_id": 6  // 小说ID
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Added to collection" | "Removed from collection",
  "is_collected": true | false
}
```

### 3.2 获取收藏状态

- **URL**: `/api/interaction/collection/status/{novel_id}`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "is_collected": true | false
}
```

### 3.3 获取收藏列表

- **URL**: `/api/interaction/collection`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：10）

- **成功响应** (200 OK):

```json
{
  "success": true,
  "total": 8,
  "pages": 1,
  "current_page": 1,
  "novels": [
    {
      "id": 6,
      "title": "string",
      "author": "string",
      "category": "string",
      "cover": "string", 
      "collection_time": "2025-04-03T15:26:12"
    }
  ]
}
```

## 4. 阅读功能

### 4.1 获取阅读历史

- **URL**: `/api/interaction/history`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 15,
  "pages": 1,
  "current_page": 1,
  "history": [
    {
      "novel_id": 6,
      "title": "string",
      "author": "string",
      "cover": "string",
      "last_read_chapter": {
        "id": 16,
        "title": "string",
        "chapter_number": 1
      },
      "last_read_at": "2025-04-03T16:45:32"
    }
  ]
}
```

### 4.2 获取阅读进度

- **URL**: `/api/interaction/progress/{novel_id}`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "novel_id": 6,
  "last_read_chapter": {
    "id": 16,
    "title": "string",
    "chapter_number": 1
  },
  "progress": 0.5,  // 阅读进度（0-1）
  "last_read_at": "2025-04-03T14:34:49"
}
```

- **错误响应** (404 Not Found):

```json
{
  "error": "No reading history found"
}
```

## 5. 私信功能

### 5.1 发送私信

- **URL**: `/api/interaction/message`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "recipient_id": 3,  // 接收者ID
  "content": "string" // 私信内容
}
```

- **成功响应** (201 Created):

```json
{
  "message": "Message sent successfully",
  "message_id": 8
}
```

### 5.2 获取与特定用户的对话

- **URL**: `/api/interaction/conversation/{user_id}`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `user_id`: 对话用户ID
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 12,
  "pages": 1,
  "current_page": 1,
  "conversation_with": {
    "id": 3,
    "username": "string",
    "avatar": "string"
  },
  "messages": [
    {
      "id": 8,
      "sender_id": 1,
      "recipient_id": 3,
      "content": "string",
      "is_read": false,
      "created_at": "2025-04-03T17:26:42"
    }
  ]
}
```

### 5.3 获取收件箱

- **URL**: `/api/interaction/inbox`
- **方法**: `GET`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 3,
  "pages": 1,
  "current_page": 1,
  "unread_count": 2,
  "conversations": [
    {
      "user": {
        "id": 3,
        "username": "string",
        "avatar": "string"
      },
      "last_message": {
        "content": "string",
        "is_read": false,
        "created_at": "2025-04-03T17:26:42"
      },
      "unread_count": 1
    }
  ]
}
```

### 5.4 标记消息为已读

- **URL**: `/api/interaction/message/{message_id}/read`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `message_id`: 消息ID

- **成功响应** (200 OK):

```json
{
  "message": "Message marked as read"
}
```

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有所需权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 