 # 作者功能 API 文档

本文档详细描述了小说平台作者功能相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [小说管理](#1-小说管理)
2. [章节管理](#2-章节管理)
3. [互动功能](#3-互动功能)

## 1. 小说管理

### 1.1 添加小说

- **URL**: `/api/novel/add`
- **方法**: `POST`
- **权限**: 需要作者权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "title": "string",     // 小说标题
  "category": "string",  // 小说分类
  "intro": "string"      // 小说简介
}
```

- **成功响应** (201 Created):

```json
{
  "message": "Novel added successfully",
  "novel": {
    "id": 6,
    "title": "string",
    "author": "string",
    "category": "string",
    "status": "ongoing",
    "cover": "string",
    "intro": "string",
    "word_count": 0,
    "view_count": 0,
    "created_at": "2025-04-03T14:33:56",
    "updated_at": "2025-04-03T14:33:56"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "Missing required fields"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "error": "Author privileges required"
}
```

### 1.2 更新小说信息

- **URL**: `/api/novel/{novel_id}/update`
- **方法**: `PUT`
- **权限**: 需要作者权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
- **请求参数**:

```json
{
  "title": "string",     // 可选
  "category": "string",  // 可选
  "intro": "string",     // 可选
  "status": "string"     // 可选，ongoing/completed
}
```

- **成功响应** (200 OK):

```json
{
  "message": "Novel updated successfully",
  "novel": {
    "id": 6,
    "title": "string",
    "author": "string",
    "category": "string",
    "status": "ongoing",
    "cover": "string",
    "intro": "string",
    "word_count": 100,
    "view_count": 0,
    "created_at": "2025-04-03T14:33:56",
    "updated_at": "2025-04-03T14:41:49"
  }
}
```

### 1.3 搜索小说

- **URL**: `/api/novel/search`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `keyword`: 搜索关键词（标题或作者）
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "novels": [
    {
      "id": 6,
      "title": "string",
      "author": "string",
      "category": "string",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "word_count": 100,
      "view_count": 0,
      "created_at": "2025-04-03T14:33:56",
      "updated_at": "2025-04-03T14:41:49"
    }
  ]
}
```

### 1.4 获取分类列表

- **URL**: `/api/novel/categories`
- **方法**: `GET`
- **权限**: 无需登录

- **成功响应** (200 OK):

```json
{
  "categories": [
    "Fantasy",
    "Science Fiction",
    "Romance",
    "Mystery",
    "Horror",
    "Adventure",
    "Historical",
    "Contemporary"
  ]
}
```

### 1.5 获取分类小说

- **URL**: `/api/novel/list`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `category`: 分类名称
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：20）

- **成功响应** (200 OK):

```json
{
  "total": 1,
  "pages": 1,
  "current_page": 1,
  "novels": [
    {
      "id": 6,
      "title": "string",
      "author": "string",
      "category": "Fantasy",
      "status": "ongoing",
      "cover": "string",
      "intro": "string",
      "word_count": 100,
      "view_count": 0,
      "created_at": "2025-04-03T14:33:56",
      "updated_at": "2025-04-03T14:41:49"
    }
  ]
}
```

## 2. 章节管理

### 2.1 添加章节

- **URL**: `/api/novel/{novel_id}/chapter/add`
- **方法**: `POST`
- **权限**: 需要作者权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
- **请求参数**:

```json
{
  "title": "string",     // 章节标题
  "content": "string",   // 章节内容
  "chapter_number": 1    // 章节编号
}
```

- **成功响应** (201 Created):

```json
{
  "message": "Chapter added successfully",
  "chapter": {
    "id": 16,
    "novel_id": 6,
    "chapter_number": 1,
    "title": "string",
    "content": "string",
    "word_count": 100,
    "created_at": "2025-04-03T14:34:49"
  }
}
```

### 2.2 删除章节

- **URL**: `/api/novel/chapter/{chapter_id}/delete`
- **方法**: `DELETE`
- **权限**: 需要作者权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `chapter_id`: 章节ID

- **成功响应** (200 OK):

```json
{
  "message": "Chapter deleted successfully"
}
```

## 3. 互动功能

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

### 3.3 添加评论

- **URL**: `/api/interaction/comment`
- **方法**: `POST`
- **权限**: 需要登录
- **请求头**:
  - `Authorization`: Bearer {token}
- **请求参数**:

```json
{
  "novel_id": 6,     // 小说ID
  "content": "string" // 评论内容
}
```

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

### 3.4 获取评论列表

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

### 3.5 获取阅读进度

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

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有作者权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 422      | 参数验证失败               | 检查请求参数是否符合格式要求                 |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     |