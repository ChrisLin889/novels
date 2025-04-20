# 作者模块 API 文档

本文档详细描述了小说平台作者模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [作者申请](#1-作者申请)
   - [1.1 提交作者申请](#11-提交作者申请)
   - [1.2 获取作者申请历史](#12-获取作者申请历史)
   - [1.3 获取待处理作者申请](#13-获取待处理作者申请)
   - [1.4 处理作者申请](#14-处理作者申请)
   - [1.5 注销作者身份](#15-注销作者身份)
2. [作者管理](#2-作者管理)
   - [2.1 更新作者资料](#21-更新作者资料)
   - [2.2 获取作者统计数据](#22-获取作者统计数据)
3. [相关模块文档](#3-相关模块文档)
   - [3.1 小说管理相关操作](#31-小说管理相关操作)
   - [3.2 管理员相关操作](#32-管理员相关操作)

## 1. 作者申请

### 1.1 提交作者申请

- **URL**: `/api/author/application`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "pen_name": "string",    // 笔名（必填）
  "bio": "string",         // 作者简介（必填）
  "reason": "string"       // 申请理由（必填）
}
```

> **说明**: 成为作者是发布小说的前提条件。申请通过后，作者可以使用[小说模块](小说模块API文档.md)的功能创建和管理小说。

- **成功响应** (201 Created):

```json
{
  "message": "作者申请提交成功，请等待管理员审核",
  "application": {
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
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "笔名、简介和申请理由为必填项"
}
```

或

```json
{
  "error": "您已经是作者，无需再次申请"
}
```

或

```json
{
  "error": "您已有一个正在处理的申请，请等待审核结果"
}
```

### 1.2 获取作者申请历史

- **URL**: `/api/author/applications`
- **方法**: `GET`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`

- **成功响应** (200 OK):

```json
{
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
    },
    {
      "id": 2,
      "user_id": 5,
      "user_name": "用户名",
      "pen_name": "新笔名", 
      "bio": "更新的作者简介",
      "reason": "新的申请理由",
      "status": "rejected",
      "admin_id": 1,
      "admin_comment": "拒绝原因",
      "created_at": "2023-01-10T00:00:00",
      "updated_at": "2023-01-15T00:00:00"
    }
  ]
}
```

### 1.3 获取待处理作者申请

- **URL**: `/api/author/admin/applications`
- **方法**: `GET`
- **权限**: 管理员
- **请求头**: `Authorization: Bearer {token}`
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 100)

> **说明**: 此接口用于管理员查看待处理的作者申请，与[管理模块-内容管理](管理模块API文档.md#4-内容管理)类似。

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

- **错误响应** (403 Forbidden):

```json
{
  "error": "需要管理员权限"
}
```

### 1.4 处理作者申请

- **URL**: `/api/author/admin/applications/{application_id}`
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

### 1.5 注销作者身份

- **URL**: `/api/author/resign`
- **方法**: `POST`
- **权限**: 作者
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**: 无

> **重要说明**：如果作者有发布的小说，需要先处理这些小说。系统会检查是否有关联的小说，如果有则不允许注销作者身份。

- **成功响应** (200 OK):

```json
{
  "message": "您已成功注销作者身份，恢复为普通用户",
  "success": true
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "您不是作者，无需注销作者身份"
}
```

或

```json
{
  "error": "作者记录不存在"
}
```

或

```json
{
  "error": "您有正在连载的作品，请先处理您的作品"
}
```

**注意**: 此功能允许作者自行注销身份，不需要管理员批准。注销后，用户将变为普通用户，所有作者相关信息将被移除，但已发布的小说和章节不会被删除。如需恢复作者身份，需重新提交作者申请并经过管理员审核。

## 2. 作者管理

### 2.1 更新作者资料

- **URL**: `/api/author/profile`
- **方法**: `PUT`
- **权限**: 作者
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "pen_name": "string",     // 笔名（可选）
  "bio": "string",          // 作者简介（可选）
  "contact_email": "string" // 联系邮箱（可选）
}
```

> **说明**：此接口用于作者更新个人资料信息，包括笔名、简介等。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "作者资料更新成功",
  "author": {
    "id": 1,
    "user_id": 5,
    "pen_name": "新笔名",
    "bio": "更新后的作者简介",
    "contact_email": "author@example.com",
    "verified": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-15T00:00:00"
  }
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "没有提供有效的更新数据"
}
```

或

```json
{
  "error": "只有作者才能更新作者资料"
}
```

### 2.2 获取作者统计数据

- **URL**: `/api/novel/author/stats`
- **方法**: `GET`
- **权限**: 作者
- **请求头**: `Authorization: Bearer {token}`

> **说明**：此接口提供作者作品相关的统计数据，方便作者了解自己作品的阅读情况。详细信息可以参考[小说模块-获取作者统计数据](小说模块API文档.md#获取作者统计数据)。

- **成功响应** (200 OK):

```json
{
  "total_novels": 3,
  "total_chapters": 150,
  "total_words": 450000,
  "total_views": 10000,
  "total_collections": 500,
  "popular_novels": [
    {
      "id": 1,
      "title": "小说标题",
      "view_count": 5000
    }
  ]
}
```

## 3. 相关模块文档

### 3.1 小说管理相关操作

作者通过申请审核后，可以使用小说模块的功能进行创作：

- [添加小说](小说模块API文档.md#11-添加小说) - 创建新的小说作品
- [更新小说信息](小说模块API文档.md#12-更新小说信息) - 修改小说标题、分类、简介等
- [删除小说](小说模块API文档.md#13-删除小说) - 删除已发布的小说
- [添加章节](小说模块API文档.md#21-添加章节) - 为小说添加新章节
- [更新章节](小说模块API文档.md#23-更新章节) - 修改已发布章节的内容
- [删除章节](小说模块API文档.md#22-删除章节) - 删除已发布的章节
- [获取作者小说列表](小说模块API文档.md#17-获取作者小说列表) - 查看自己的所有小说

### 3.2 管理员相关操作

管理员对作者和作品进行管理的相关功能：

- [处理作者申请](#14-处理作者申请) - 审核作者申请
- [内容审核](管理模块API文档.md#4-内容管理) - 审核小说和章节内容

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有所需权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 