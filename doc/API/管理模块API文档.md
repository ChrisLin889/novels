# 管理模块 API 文档

本文档详细描述了小说平台管理模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [仪表盘统计](#1-仪表盘统计)
2. [用户管理](#2-用户管理)
   - [2.1 获取用户列表](#21-获取用户列表)
   - [2.2 管理用户状态](#22-管理用户状态)
   - [2.3 获取用户操作历史](#23-获取用户操作历史)
3. [敏感词管理](#3-敏感词管理)
   - [3.1 获取敏感词列表](#31-获取敏感词列表)
   - [3.2 管理敏感词](#32-管理敏感词)
4. [内容管理](#4-内容管理)
   - [4.1 获取待审核内容](#41-获取待审核内容)
   - [4.2 审核内容](#42-审核内容)
5. [作者管理](#5-作者管理)
   - [5.1 获取待处理作者申请](#51-获取待处理作者申请)
   - [5.2 处理作者申请](#52-处理作者申请)
6. [相关模块文档](#6-相关模块文档)
   - [6.1 作者相关管理](#61-作者相关管理)
   - [6.2 小说相关管理](#62-小说相关管理)
7. [附录：敏感词级别说明](#7-附录敏感词级别说明)

## 1. 仪表盘统计

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

## 2. 用户管理

### 2.1 获取用户列表

- **URL**: `/api/admin/users`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)
  - `role`: 角色筛选 (可选，如：admin, user, author)

> **说明**：通过指定`role=author`可以筛选出作者用户，方便与[作者模块](作者模块API文档.md)中的功能结合使用。

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

### 2.2 管理用户状态

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

> **注意**：如果被禁用的用户是作者，其作者权限将被暂停，但相关作品不会被删除。详情请参考[作者模块](作者模块API文档.md)。

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

### 2.3 获取用户操作历史

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

## 3. 敏感词管理

### 3.1 获取敏感词列表

- **URL**: `/api/admin/sensitive-words`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `category`: 分类筛选（可选）
  - `page`: 页码（默认: 1）
  - `per_page`: 每页数量（默认: 50，最大: 200）

> **说明**：敏感词管理对[小说模块](小说模块API文档.md)内容审核十分重要，系统会自动检查小说和章节内容中的敏感词。

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

### 3.2 管理敏感词

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

## 4. 内容管理

### 4.1 获取待审核内容

- **URL**: `/api/admin/content/{content_type}`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `content_type`: 内容类型，可选值："novel", "chapter", "comment"
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 50)

> **说明**：此接口用于获取需要审核的内容。`novel`和`chapter`类型的内容与[小说模块](小说模块API文档.md)相关，管理员通过此接口可以审核作者提交的小说和章节。

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

### 4.2 审核内容

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

> **说明**：审核结果会影响作者作品的可见性。如果内容被拒绝，作者可以在[小说模块](小说模块API文档.md)查看拒绝原因并修改后重新提交。

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

## 5. 作者管理

### 5.1 获取待处理作者申请

- **URL**: `/api/admin/author-applications`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)

> **说明**: 此接口用于管理员查看待处理的作者申请，与[内容管理](#4-内容管理)类似。

- **成功响应** (200 OK):

```json
{
  "total": 10,
  "pages": 1,
  "current_page": 1,
  "applications": [
    {
      "id": 1,
      "user_id": 5,
      "user_name": "用户名",
      "pen_name": "笔名",
      "bio": "作者简介",
      "reason": "申请理由",
      "status": "pending",
      "admin_id": null,
      "admin_comment": null,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-01T00:00:00"
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

- **错误响应** (403 Forbidden):

```json
{
  "error": "需要管理员权限"
}
```

### 5.2 处理作者申请

- **URL**: `/api/admin/author-applications/{application_id}`
- **方法**: `POST`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **路径参数**:
  - `application_id`: 申请ID
- **请求参数**:

```json
{
  "action": "approve",    // "approve" 或 "reject"
  "comment": "string"     // 管理员批注（拒绝时必填）
}
```

> **审核结果**：如果申请被批准，用户将获得作者权限，可以使用[小说模块](小说模块API文档.md)中的功能创建和管理小说。

- **成功响应** (200 OK):

```json
{
  "message": "申请已批准，用户已成为作者",
  "application": {
    "id": 1,
    "user_id": 5,
    "user_name": "用户名",
    "pen_name": "笔名",
    "bio": "作者简介",
    "reason": "申请理由",
    "status": "approved",
    "admin_id": 1,
    "admin_comment": "批准评语",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-02T00:00:00"
  }
}
```

或

```json
{
  "message": "申请已拒绝",
  "application": {
    "id": 1,
    "user_id": 5,
    "user_name": "用户名",
    "pen_name": "笔名",
    "bio": "作者简介",
    "reason": "申请理由",
    "status": "rejected",
    "admin_id": 1,
    "admin_comment": "拒绝原因",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-02T00:00:00"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "无效的操作，必须是 approve 或 reject"
}
```

或

```json
{
  "error": "拒绝申请时必须提供原因"
}
```

或

```json
{
  "error": "申请记录不存在"
}
```

或

```json
{
  "error": "该申请已被处理，无法再次处理"
}
```

## 6. 相关模块文档

### 6.1 作者相关管理

管理员负责审核和管理作者相关功能：

- [获取待处理作者申请](#51-获取待处理作者申请) - 查看用户的作者申请
- [处理作者申请](#52-处理作者申请) - 审核作者申请
- [获取作者小说列表](小说模块API文档.md#16-获取作者小说列表) - 查看特定作者的作品

### 6.2 小说相关管理

管理员对小说和章节内容的管理功能：

- [删除小说](小说模块API文档.md#13-删除小说) - 管理员可以删除违规小说
- [审核内容](#42-审核内容) - 审核小说和章节内容
- [敏感词管理](#3-敏感词管理) - 管理内容审核的敏感词列表

## 7. 附录：敏感词级别说明

| 级别 | 说明                                               | 处理方式                                             |
|------|----------------------------------------------------|----------------------------------------------------|
| 1    | 轻度敏感，一般为轻微不良词汇                       | 系统自动替换为星号                                   |
| 2    | 中度敏感，涉及政治、暴力等内容                     | 需人工审核，默认不通过审核                           |
| 3    | 高度敏感，严重违法违规内容                         | 内容直接拒绝，同时记录用户违规行为                   |

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有管理员权限               |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 