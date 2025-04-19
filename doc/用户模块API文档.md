# 用户模块 API 文档

本文档详细描述了小说平台用户模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [用户注册](#1-用户注册)
2. [用户登录](#2-用户登录)
3. [获取个人信息](#3-获取个人信息)
4. [修改个人信息](#4-修改个人信息)
5. [修改密码](#5-修改密码)
6. [注销账户](#6-注销账户)
7. [管理员功能](#7-管理员功能)
   - [7.1 查看用户列表](#71-查看用户列表)
   - [7.2 修改用户状态](#72-修改用户状态)
   - [7.3 修改用户角色](#73-修改用户角色)

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

> **注意**: 当前接口仅支持更新avatar、email、phone字段，不支持更新author相关字段如pen_name和bio。作者特有信息（如笔名、简介等）目前无法通过API直接更新。

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

## 6. 注销账户

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

## 7. 管理员功能

### 7.1 查看用户列表

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

### 7.2 修改用户状态

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

### 7.3 修改用户角色

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

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有所需权限                 |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 