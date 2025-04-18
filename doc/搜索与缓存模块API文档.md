# 搜索与缓存模块 API 文档

本文档详细描述了小说平台搜索和缓存模块相关的API接口，包括请求方法、路径、参数和返回值。

## 目录

1. [搜索功能](#1-搜索功能)
   - [1.1 小说搜索](#11-小说搜索)
   - [1.2 标签搜索](#12-标签搜索)
   - [1.3 相似小说推荐](#13-相似小说推荐)
   - [1.4 获取热门标签](#14-获取热门标签)
2. [缓存管理](#2-缓存管理)
   - [2.1 刷新缓存](#21-刷新缓存)
   - [2.2 清空缓存](#22-清空缓存)

## 1. 搜索功能

### 1.1 小说搜索

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
      "updated_at": "2023-01-02T00:00:00",
      "chapter_count": 20,
      "tags": [
        {
          "id": 1,
          "name": "玄幻",
          "category_id": 1,
          "category_name": "类型",
          "description": null
        }
      ]
    }
  ]
}
```

### 1.2 标签搜索

- **URL**: `/api/search/novels/tag/{tag}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `tag`: 标签名称
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `per_page`: 每页数量 (默认: 20，最大: 50)
- **说明**: 该接口用于查找拥有特定标签的小说。系统将优先查找完全匹配的标签，若无法找到，将尝试模糊匹配。

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
      "updated_at": "2023-01-02T00:00:00",
      "chapter_count": 20,
      "tags": [
        {
          "id": 1,
          "name": "玄幻",
          "category_id": 1,
          "category_name": "类型",
          "description": null
        }
      ]
    }
  ]
}
```

### 1.3 相似小说推荐

- **URL**: `/api/search/similar/{novel_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID
- **查询参数**:
  - `limit`: 返回数量 (默认: 5)
- **说明**: 该接口基于标签相似度进行推荐，优先返回与目标小说拥有相同标签的作品，按共同标签数量排序。若目标小说无标签，则返回同一类别下的热门小说。

- **成功响应** (200 OK):

```json
{
  "similar_novels": [
    {
      "id": 1,
      "title": "string",
      "author": "string",
      "category": "string",
      "cover": "string",
      "view_count": 1000,
      "collection_count": 100,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": "2023-01-02T00:00:00",
      "chapter_count": 20,
      "tags": [
        {
          "id": 1,
          "name": "玄幻",
          "category_id": 1,
          "category_name": "类型",
          "description": null
        }
      ]
    }
  ]
}
```

### 1.4 获取热门标签

- **URL**: `/api/search/tags/hot`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `limit`: 返回数量 (默认: 20)
  - `category_id`: 分类ID (可选，若提供则只返回该分类下的标签)

- **成功响应** (200 OK):

```json
{
  "tags": [
    {
      "id": 1,
      "name": "玄幻",
      "category_id": 1,
      "category_name": "类型",
      "description": null,
      "novel_count": 125
    }
  ]
}
```

## 2. 缓存管理

### 2.1 刷新缓存

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

- **错误响应** (403 Forbidden):

```json
{
  "error": "需要管理员权限"
}
```

### 2.2 清空缓存

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

- **错误响应** (403 Forbidden):

```json
{
  "error": "需要管理员权限"
}
```

## 附录: 错误代码及说明

| 错误代码 | 描述                       | 解决方案                                     |
|----------|----------------------------|----------------------------------------------|
| 400      | 请求参数错误               | 检查请求参数是否符合要求                     |
| 401      | 未授权（未登录）           | 确保请求中包含有效的授权令牌                 |
| 403      | 权限不足                   | 确认当前用户是否具有管理员权限               |
| 404      | 资源不存在                 | 检查请求的资源ID是否存在                     |
| 500      | 服务器内部错误             | 请联系管理员，并提供错误发生时的详细信息     | 