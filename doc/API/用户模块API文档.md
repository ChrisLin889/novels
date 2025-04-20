# 用户模块 API 文档

本文档详细描述了小说平台用户模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [用户注册](#1-用户注册)
2. [用户登录](#2-用户登录)
3. [获取个人信息](#3-获取个人信息)
4. [修改个人信息](#4-修改个人信息)
5. [修改密码](#5-修改密码)
6. [用户登出](#6-用户登出)
7. [注销账户](#7-注销账户)
8. [开发中功能](#8-开发中功能)

## 1. 用户注册

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

## 2. 用户登录

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

根据用户角色不同，返回结构会有所差异：

1. **普通用户**:
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

2. **作者用户**:
```json
{
  "success": true,
  "access_token": "string", // JWT令牌
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "author",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00",
    "status": "active",
    "author": {
      "id": 1,
      "pen_name": "string",
      "bio": "string",
      "verified": true,
      "works_count": 5,
      "fans_count": 10
    }
  }
}
```

3. **管理员用户**:
```json
{
  "success": true,
  "access_token": "string", // JWT令牌
  "user": {
    "id": 1,
    "username": "string",
    "phone": "string",
    "email": "string",
    "role": "admin",
    "avatar": "string",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00",
    "status": "active"
    // 可能包含管理员特定信息
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

## 3. 获取个人信息

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

## 4. 修改个人信息

- **URL**: `/api/user/profile`
- **方法**: `PUT`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "email": "string",    // 可选
  "phone": "string",    // 可选
  "avatar": "string",   // 可选
  "password": "string"  // 可选，如提供则会更新密码
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
  "error": "错误信息" // 如：No fields to update, Email already in use, Phone already in use, Password must be at least 6 characters long
}
```

> **注意**: 当前接口支持更新avatar、email、phone和password字段，不支持更新author相关字段如pen_name和bio。作者特有信息（如笔名、简介等）目前无法通过API直接更新。

## 5. 修改密码

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

> **注意**: 前端实现中使用的是 `/user/password` 端点和 PUT 方法，但后端实际实现为 `/api/user/change-password` 和 POST 方法。在将来的版本中应统一这些差异。

## 6. 用户登出

- **URL**: `/api/user/logout`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**: 无

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

> **注意**: 由于使用的是JWT认证机制，服务器端不会实际使token失效。登出操作主要由客户端完成，通过移除本地存储的令牌实现。该API端点主要用于记录日志和维护用户会话状态。

## 7. 注销账户

- **URL**: `/api/user/deactivate`
- **方法**: `POST`
- **权限**: 用户登录
- **请求头**: `Authorization: Bearer {token}`
- **请求参数**:

```json
{
  "password": "string"  // 当前密码，用于验证身份
}
```

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Account successfully deactivated"
}
```

- **错误响应** (400 Bad Request):

```json
{
  "error": "错误信息" // 如：Password is incorrect, Admin accounts cannot be deactivated through this method
}
```

> **注意**：
> 1. 账户注销后，用户的所有数据将被删除，包括收藏、历史记录、关注关系等
> 2. 如果用户是作者，其作者信息将被删除，但已发布的作品将保留
> 3. 管理员账户不能通过此接口注销
> 4. 若要注销作者身份但保留用户账户，请使用作者模块中的 `/api/author/resign` 接口

## 8. 开发中功能

以下功能已在后端实现，但尚未提供公开的API端点。这些功能可能在未来版本中推出。

### 8.1 获取用户安全信息

此功能用于安全验证目的，例如密码重置流程中，获取经过掩码处理的用户联系方式。

- **功能名称**: `get_security_info`
- **当前状态**: 后端已实现，但尚未提供公开API端点
- **预期用途**: 密码重置，账户验证等安全流程
- **返回数据格式**:

```json
{
  "success": true,
  "email": "u***r@example.com",  // 掩码处理的邮箱
  "phone": "123****7890",        // 掩码处理的电话
  "has_email": true,             // 是否设置了邮箱
  "has_phone": true              // 是否设置了电话
}
```

> **注意**: 此功能尚未通过公开API提供，在未来版本中可能会添加"忘记密码"和"重置密码"等相关端点。

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有所需权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 