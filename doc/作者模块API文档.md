# 作者模块 API 文档

本文档详细描述了小说平台作者模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [作者申请](#1-作者申请)
   - [1.1 提交作者申请](#11-提交作者申请)
   - [1.2 获取作者申请历史](#12-获取作者申请历史)
   - [1.3 获取待处理作者申请](#13-获取待处理作者申请)
   - [1.4 处理作者申请](#14-处理作者申请)
   - [1.5 注销作者身份](#15-注销作者身份)
2. [功能限制说明](#2-功能限制说明)
   - [2.1 作者资料更新限制](#21-作者资料更新限制)
   - [2.2 数据库关系说明](#22-数据库关系说明)

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

**注意**: 此功能允许作者自行注销身份，不需要管理员批准。注销后，用户将变为普通用户，所有作者相关信息将被移除，但已发布的小说和章节不会被删除。如需恢复作者身份，需重新提交作者申请并经过管理员审核。

## 2. 功能限制说明

### 2.1 作者资料更新限制

当前API实现不支持直接更新作者特有信息：

- **pen_name (笔名)**：无法通过现有API更新
- **bio (作者简介)**：无法通过现有API更新

### 2.2 数据库关系说明

平台采用三层关系结构：

1. **user表**：存储基本用户信息（id、username、email等）
2. **author表**：存储作者特有信息，通过user_id外键与user表关联
3. **novel表**：存储小说信息，通过author_id外键与author表关联

这种设计导致添加小说时必须确保正确的author记录存在，否则会出现外键约束错误。当一个用户被设置为作者角色时，系统应该自动创建对应的author记录。

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有所需权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 