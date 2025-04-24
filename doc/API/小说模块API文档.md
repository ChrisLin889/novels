# 小说模块 API 文档

本文档详细描述了小说平台小说模块相关的API接口，包括请求方法、路径、参数和返回值。

> **注意**：本API文档已按照实际后端实现更新了"添加小说"和"更新小说"接口的参数。请特别注意以下参数名：
> - 前端需要传入 `category` 参数，与数据库字段保持一致
> - 前端需要传入 `intro` 参数，与数据库字段保持一致
> - 前端需要传入 `cover` 参数，与数据库字段保持一致
> - 新增 `tags` 数组参数
> 
> 在响应中，数据字段名称与数据库一致：`intro` 表示小说简介，`cover` 表示封面图片路径。
>
> 作者名称不再需要前端提供，系统会自动使用当前用户的笔名或用户名。
>
> **重要**：本系统的登录接口是 `/api/user/login` 而不是 `/api/auth/login`。请使用正确的路径进行认证操作。
>
> **用户与作者身份说明**：系统中用户(User)和作者(Author)是两个不同的实体，有各自的ID。API接口使用JWT返回的用户ID(user_id)进行身份验证，系统会自动查找该用户对应的作者记录(author)，并使用author.id作为author_id。前端开发者只需使用JWT认证，不需要手动处理这种映射关系。

## 目录

1. [小说管理](#1-小说管理)
   - [1.1 添加小说](#11-添加小说)
   - [1.2 更新小说信息](#12-更新小说信息)
   - [1.3 删除小说](#13-删除小说)
   - [1.4 搜索小说](#14-搜索小说)
   - [1.5 获取分类列表](#15-获取分类列表)
   - [1.6 获取分类小说](#16-获取分类小说)
   - [1.7 收藏小说功能](#17-收藏小说功能)
   - [1.8 获取作者创建的小说列表](#18-获取作者创建的小说列表)
   - [1.9 获取小说详情](#19-获取小说详情)
   - [1.10 获取热门小说](#110-获取热门小说)
   - [1.11 获取最新小说](#111-获取最新小说)
   - [1.12 获取小说章节列表](#112-获取小说章节列表)
   - [1.13 获取小说标签](#113-获取小说标签)
   - [1.14 为小说添加标签](#114-为小说添加标签)
   - [1.15 从小说中移除标签](#115-从小说中移除标签)
   - [1.16 获取所有标签列表](#116-获取所有标签列表)
2. [章节管理](#2-章节管理)
   - [2.1 添加章节](#21-添加章节)
   - [2.2 删除章节](#22-删除章节)
   - [2.3 更新章节](#23-更新章节)
   - [2.4 获取章节内容](#24-获取章节内容)
3. [相关模块文档](#3-相关模块文档)
   - [3.1 作者相关操作](#31-作者相关操作)
   - [3.2 管理员相关操作](#32-管理员相关操作)

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
  "title": "string",   // 小说标题（必填）
  "category": "string", // 小说分类ID（必填）
  "intro": "string", // 小说简介（必填）
  "cover": "string", // 封面图片路径（可选，默认为default_cover.jpg）
  "tags": ["string"]       // 小说标签（可选，数组类型）
}
```

> **重要**：系统会使用当前登录用户关联的author.id作为小说的author_id，必须确保当前用户已有author记录，否则会出现外键约束错误。由于数据库设计，novel表的author_id必须关联到author表的id。作者名称会自动使用用户的笔名或用户名。
>
> **相关流程**：需要先完成[作者申请流程](作者模块API文档.md#11-提交作者申请)并获得批准后才能添加小说。

- **成功响应** (201 Created):

```json
{
  "success": true,
  "message": "Novel added successfully",
  "novel_id": 6
}
```

- **错误响应** (400 Bad Request):

```json
{
  "success": false,
  "error": "Missing required fields"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "success": false,
  "error": "Author privileges required"
}
```

### 1.2 更新小说信息

- **URL**: `/api/novel/{novel_id}`
- **方法**: `PUT`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
- **请求参数**:

```json
{
  "title": "string",       // 可选
  "category": "string", // 可选
  "intro": "string", // 可选
  "cover": "string", // 可选
  "status": "string",      // 可选，ongoing/completed
  "tags": ["string"]       // 可选，数组类型
}
```

> **权限说明**：只有小说的原作者或管理员可以修改小说信息。系统会自动验证当前登录用户是否为小说的创建者，未经授权的修改请求将被拒绝。

- **成功响应** (200 OK):

```json
{
  "success": true, 
  "message": "Novel updated successfully"
}
```

### 1.3 删除小说

- **URL**: `/api/novel/{novel_id}/delete`
- **方法**: `DELETE`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID

> **权限说明**：只有小说的原作者或管理员可以删除小说。系统会自动验证当前登录用户是否为小说的创建者，未经授权的删除请求将被拒绝。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Novel deleted successfully"
}
```

- **错误响应** (400 Bad Request):

```json
{
  "success": false,
  "error": "Novel not found"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "success": false,
  "error": "Permission denied - only the novel author or admin can delete this novel"
}
```

### 1.4 搜索小说

> **注意**：小说搜索功能现已移至搜索模块。请使用 `/api/search/novels` 接口进行小说搜索。
>
> 详细文档请参考 [搜索模块API文档 - 小说搜索](搜索模块API文档.md#11-小说搜索)

### 1.5 获取分类列表

- **URL**: `/api/novel/categories`
- **方法**: `GET`
- **权限**: 无需登录

- **成功响应** (200 OK):

```json
{
  "success": true,
  "categories": [
    {
      "name": "Fantasy",
      "count": 12,
      "description": "奇幻小说"
    },
    {
      "name": "Science Fiction",
      "count": 8,
      "description": "科幻小说"
    },
    {
      "name": "Romance",
      "count": 15,
      "description": "言情小说"
    },
    {
      "name": "Mystery",
      "count": 10,
      "description": "悬疑小说"
    }
  ]
}
```

> **说明**：每个分类对象包含分类名称(name)、该分类下的小说数量(count)以及分类描述(description)。

### 1.6 获取分类小说

- **URL**: `/api/novel/list`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `category`: 分类名称
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：10）
  - `sort_by`: 排序方式（默认：updated_at，可选值：updated_at、view_count、collection_count）

> **说明**：sort_by参数允许按不同字段对小说列表进行排序。updated_at按更新时间排序，view_count按阅读量排序，collection_count按收藏数量排序。

- **成功响应** (200 OK):

```json
{
  "success": true,
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

### 1.7 收藏小说功能

> **重要说明**：收藏小说相关功能在交互模块中实现。请使用以下接口管理和访问收藏的小说：
> - 收藏/取消收藏小说：POST `/api/interaction/collection`
> - 获取收藏状态：GET `/api/interaction/collection/status/{novel_id}`
> - 获取收藏列表：GET `/api/interaction/collection`
>
> 详细文档请参考 [互动模块API文档 - 收藏功能](互动模块API文档.md#3-收藏功能)

### 1.8 获取作者创建的小说列表

- **URL**: `/api/novel/author/novels`
- **方法**: `GET`
- **权限**: 需要作者权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **查询参数**:
  - `page`: 页码（默认：1）
  - `per_page`: 每页数量（默认：10）

> **说明**：此接口用于作者查看自己创建的所有小说。需要作者权限，只返回作者本人创建的小说。
>
> **重要**：此接口基于JWT中的用户ID自动查找对应的作者记录，开发者无需手动处理用户ID到作者ID的映射。
> 系统会自动根据当前登录用户的user_id查找对应的author记录，并返回该作者创建的小说。

- **成功响应** (200 OK):

```json
{
  "success": true,
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
  ],
  "total": 1,
  "pages": 1,
  "current_page": 1
}
```

### 1.9 获取小说详情

- **URL**: `/api/novel/detail/{novel_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "success": true,
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
  },
  "chapters": [
    {
      "id": 16,
      "novel_id": 6,
      "chapter_number": 1,
      "title": "第一章",
      "word_count": 100,
      "created_at": "2025-04-03T14:34:49"
    }
  ]
}
```

### 1.10 获取热门小说

- **URL**: `/api/novel/popular`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `limit`: 返回小说数量（默认：10）

- **成功响应** (200 OK):

```json
{
  "success": true,
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

### 1.11 获取最新小说

- **URL**: `/api/novel/latest`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `limit`: 返回小说数量（默认：10）

- **成功响应** (200 OK):

```json
{
  "success": true,
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

### 1.12 获取小说章节列表

- **URL**: `/api/novel/{novel_id}/chapters`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID

> **说明**：此接口返回小说的所有章节，按章节编号排序。目前此接口不支持分页，会一次性返回所有章节。对于章节数量较多的小说，前端应当实现本地分页展示。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "chapters": [
    {
      "id": 16,
      "novel_id": 6,
      "chapter_number": 1,
      "title": "string",
      "content": "string",
      "word_count": 100,
      "created_at": "2025-04-03T14:34:49"
    }
  ]
}
```

### 1.13 获取小说标签

- **URL**: `/api/novel/{novel_id}/tags`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `novel_id`: 小说ID

- **成功响应** (200 OK):

```json
{
  "success": true,
  "tags": [
    {
      "id": 1,
      "name": "冒险",
      "count": 15
    },
    {
      "id": 3,
      "name": "奇幻",
      "count": 8
    }
  ]
}
```

> **说明**：每个标签对象包含标签ID(id)、标签名称(name)和使用该标签的小说数量(count)。

### 1.14 为小说添加标签

- **URL**: `/api/novel/{novel_id}/tags`
- **方法**: `POST`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
- **请求参数**:

```json
{
  "tags": ["冒险", "奇幻"]  // 标签名称数组
}
```

> **权限说明**：只有小说的原作者或管理员可以为小说添加标签。系统会验证当前登录用户是否为小说的创建者。
>
> **处理逻辑**：如果标签已存在，系统会直接使用；如果标签不存在，系统会自动创建新标签。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Tags added successfully",
  "added_tags": ["冒险", "奇幻"]
}
```

- **错误响应** (403 Forbidden):

```json
{
  "success": false,
  "error": "Permission denied - only the novel author or admin can add tags"
}
```

### 1.15 从小说中移除标签

- **URL**: `/api/novel/{novel_id}/tags/{tag_id}`
- **方法**: `DELETE`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
  - `tag_id`: 标签ID

> **权限说明**：只有小说的原作者或管理员可以从小说中移除标签。系统会验证当前登录用户是否为小说的创建者。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Tag removed successfully"
}
```

- **错误响应** (403 Forbidden):

```json
{
  "success": false,
  "error": "Permission denied - only the novel author or admin can remove tags"
}
```

- **错误响应** (404 Not Found):

```json
{
  "success": false,
  "error": "Tag not found for this novel"
}
```

### 1.16 获取所有标签列表

- **URL**: `/api/novel/tags`
- **方法**: `GET`
- **权限**: 无需登录
- **查询参数**:
  - `sort_by`: 排序方式（默认：count，可选值：name、count）
  - `order`: 排序顺序（默认：desc，可选值：asc、desc）
  - `limit`: 返回标签数量（默认：30）

> **说明**：此接口返回系统中所有的标签列表，可以按标签使用频率（count）或标签名称（name）排序。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "tags": [
    {
      "id": 1,
      "name": "冒险",
      "count": 15
    },
    {
      "id": 3,
      "name": "奇幻",
      "count": 8
    },
    {
      "id": 5,
      "name": "科幻",
      "count": 6
    }
  ]
}
```

## 2. 章节管理

### 2.1 添加章节

- **URL**: `/api/novel/{novel_id}/chapters`
- **方法**: `POST`
- **权限**: 需要作者权限（仅小说的原作者）
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `novel_id`: 小说ID
- **请求参数**:

```json
{
  "title": "string",     // 章节标题
  "content": "string",   // 章节内容
  "chapter_number": 1    // 章节编号（可选，不提供则自动分配）
}
```

> **权限说明**：只有小说的原作者可以为自己的小说添加章节。

- **成功响应** (201 Created):

```json
{
  "success": true,
  "message": "Chapter added successfully",
  "chapter_id": 16
}
```

### 2.2 删除章节

- **URL**: `/api/novel/chapters/{chapter_id}`
- **方法**: `DELETE`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `chapter_id`: 章节ID

> **权限说明**：只有小说的原作者或管理员可以删除章节。系统会验证请求用户是否为章节所属小说的作者，管理员可以删除任何小说的章节。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Chapter deleted successfully"
}
```

### 2.3 更新章节

- **URL**: `/api/novel/chapters/{chapter_id}`
- **方法**: `PUT`
- **权限**: 需要作者权限（仅小说的原作者）或管理员权限
- **请求头**:
  - `Authorization`: Bearer {token}
- **路径参数**:
  - `chapter_id`: 章节ID
- **请求参数**:

```json
{
  "title": "string",     // 章节标题（可选）
  "content": "string"    // 章节内容（可选）
}
```

> **权限说明**：只有小说的原作者或管理员可以修改章节内容。系统会自动查找用户对应的作者记录并验证该用户是否为章节所属小说的作者，管理员可以修改任何小说的章节内容。

- **成功响应** (200 OK):

```json
{
  "success": true,
  "message": "Chapter updated successfully",
  "chapter": {
    "id": 16,
    "novel_id": 6,
    "chapter_number": 1,
    "title": "更新后的章节标题",
    "content": "更新后的章节内容",
    "word_count": 120,
    "created_at": "2025-04-03T14:34:49"
  }
}
```

- **错误响应** (403 Forbidden):

```json
{
  "success": false,
  "error": "Permission denied - only the novel author or admin can update chapters"
}
```

- **错误响应** (404 Not Found):

```json
{
  "success": false,
  "error": "Chapter not found"
}
```

### 2.4 获取章节内容

- **URL**: `/api/novel/chapters/{chapter_id}`
- **方法**: `GET`
- **权限**: 无需登录
- **路径参数**:
  - `chapter_id`: 章节ID

- **成功响应** (200 OK):

```json
{
  "success": true,
  "chapter": {
    "id": 16,
    "novel_id": 6,
    "chapter_number": 1,
    "title": "章节标题",
    "content": "章节内容...",
    "word_count": 120,
    "created_at": "2025-04-03T14:34:49"
  },
  "prev_chapter": {
    "id": 15,
    "novel_id": 6,
    "chapter_number": 0,
    "title": "上一章标题",
    "word_count": 100,
    "created_at": "2025-04-03T14:34:48"
  },
  "next_chapter": {
    "id": 17,
    "novel_id": 6,
    "chapter_number": 2,
    "title": "下一章标题",
    "word_count": 110,
    "created_at": "2025-04-03T14:34:50"
  }
}
```

> **说明**：此端点会返回章节内容以及上一章和下一章的基本信息（如果存在）。阅读章节时会自动记录阅读历史并增加小说的阅读量。

## 3. 相关模块文档

### 3.1 作者相关操作

作为作者，除了管理小说和章节外，还需要了解以下作者模块功能：

- [提交作者申请](作者模块API文档.md#11-提交作者申请) - 成为作者的第一步
- [获取作者申请历史](作者模块API文档.md#12-获取作者申请历史) - 查看自己的申请记录
- [更新作者资料](作者模块API文档.md#21-作者资料更新限制) - 修改作者个人信息
- [注销作者身份](作者模块API文档.md#15-注销作者身份) - 如需放弃作者身份

### 3.2 管理员相关操作

管理员可以对小说内容进行管理，相关功能包括：

- [内容审核](管理模块API文档.md#4-内容管理) - 审核小说和章节内容
- [敏感词管理](管理模块API文档.md#3-敏感词管理) - 添加和管理内容审查的敏感词

### 2.2 获取作者统计数据

- **URL**: `/api/novel/author/stats`
- **方法**: `GET`
- **权限**: 作者
- **请求头**: `Authorization: Bearer {token}`

> **说明**：此接口提供作者作品相关的统计数据，方便作者了解自己作品的阅读情况。
>
> **重要**：此接口基于JWT中的用户ID自动查找对应的作者记录，开发者无需手动处理用户ID到作者ID的映射。
> 系统会自动根据当前登录用户的user_id查找对应的author记录，并返回该作者的统计数据。

- **成功响应** (200 OK):

```json
{
  "novel_count": 3,
  "total_chapters": 150,
  "total_words": 450000,
  "total_views": 10000,
  "total_collections": 500
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