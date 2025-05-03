# 小说网站数据库结构文档

## 1. 小说表 (novel)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 小说ID |
| author_id | int | - | {FK->author.id} | 作者ID |
| title | varchar | 100 | {NOT NULL, INDEX} | 小说标题 |
| author | varchar | 50 | {NOT NULL} | 作者名称 |
| category | varchar | 30 | {NOT NULL, INDEX} | 小说分类 |
| cover | varchar | 255 | {NULL} | 封面图片URL |
| intro | text | - | {NULL} | 小说简介 |
| status | varchar | 20 | {NULL} | 小说状态 |
| view_count | int | - | {NULL} | 阅读次数 |
| collection_count | int | - | {NULL} | 收藏次数 |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |

## 2. 章节表 (chapter)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 章节ID |
| novel_id | int | - | {FK->novel.id, NOT NULL, INDEX} | 所属小说ID |
| chapter_number | int | - | {NOT NULL} | 章节序号 |
| title | varchar | 100 | {NOT NULL} | 章节标题 |
| content | text | - | {NOT NULL} | 章节内容 |
| word_count | int | - | {NULL} | 字数统计 |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |

## 3. 作者表 (author)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 作者ID |
| user_id | int | - | {FK->user.id, NOT NULL, UNIQUE} | 用户ID |
| pen_name | varchar | 50 | {NULL} | 笔名 |
| bio | text | - | {NULL} | 作者简介 |
| verified | tinyint | 1 | {NULL, DEFAULT 0} | 是否认证 |
| income_account | varchar | 100 | {NULL} | 收入账户 |
| works_count | int | - | {NULL, DEFAULT 0} | 作品数量 |
| fans_count | int | - | {NULL, DEFAULT 0} | 粉丝数量 |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |

## 4. 用户表 (user)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 用户ID |
| username | varchar | 50 | {NOT NULL} | 用户名 |
| phone | varchar | 20 | {NULL, UNIQUE} | 手机号 |
| email | varchar | 100 | {NULL, UNIQUE} | 电子邮箱 |
| password_hash | varchar | 128 | {NOT NULL} | 密码哈希 |
| avatar | varchar | 255 | {NULL} | 头像URL |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |
| status | tinyint | 1 | {NULL} | 用户状态 |

## 5. 管理员表 (admin)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 管理员ID |
| user_id | int | - | {FK->user.id, NOT NULL, UNIQUE} | 用户ID |
| admin_level | tinyint | - | {NULL, DEFAULT 1} | 管理员级别 |
| permissions | json | - | {NULL} | 权限配置 |
| department | varchar | 50 | {NULL} | 部门 |
| last_login_at | datetime | - | {NULL} | 最后登录时间 |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |

## 6. 评论表 (comments)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 评论ID |
| user_id | int | - | {FK->user.id, NOT NULL, INDEX} | 用户ID |
| novel_id | int | - | {FK->novel.id, NULL, INDEX} | 小说ID |
| chapter_id | int | - | {FK->chapter.id, NULL, INDEX} | 章节ID |
| content | text | - | {NOT NULL} | 评论内容 |
| created_at | datetime | - | {NULL} | 创建时间 |
| likes | int | - | {NULL} | 点赞数 |

## 7. 内容审核表 (content_audit)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 审核记录ID |
| content_type | varchar | 20 | {NOT NULL} | 内容类型 |
| content_id | int | - | {NOT NULL} | 内容ID |
| status | varchar | 20 | {NULL} | 审核状态 |
| reason | varchar | 255 | {NULL} | 审核原因 |
| admin_id | int | - | {FK->admin.id, NULL, INDEX} | 审核管理员ID |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |

## 8. 爬虫任务表 (crawl_task)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 任务ID |
| source_url | varchar | 255 | {NOT NULL} | 来源URL |
| task_type | varchar | 50 | {NOT NULL} | 任务类型 |
| status | varchar | 20 | {NULL} | 任务状态 |
| started_at | datetime | - | {NULL} | 开始时间 |
| completed_at | datetime | - | {NULL} | 完成时间 |
| success_count | int | - | {NULL} | 成功数量 |
| error_count | int | - | {NULL} | 错误数量 |
| error_message | text | - | {NULL} | 错误信息 |
| created_at | datetime | - | {NULL} | 创建时间 |

## 9. 爬虫临时数据表 (crawl_temp)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 记录ID |
| task_id | int | - | {FK->crawl_task.id, NOT NULL, INDEX} | 任务ID |
| novel_title | varchar | 100 | {NULL} | 小说标题 |
| novel_author | varchar | 50 | {NULL} | 小说作者 |
| novel_category | varchar | 30 | {NULL} | 小说分类 |
| novel_intro | text | - | {NULL} | 小说简介 |
| novel_cover_url | varchar | 255 | {NULL} | 小说封面URL |
| chapter_title | varchar | 100 | {NULL} | 章节标题 |
| chapter_number | int | - | {NULL} | 章节序号 |
| chapter_content | text | - | {NULL} | 章节内容 |
| source_url | varchar | 255 | {NOT NULL} | 来源URL |
| is_approved | tinyint | 1 | {NULL} | 是否通过审核 |
| is_rejected | tinyint | 1 | {NULL} | 是否被拒绝 |
| created_at | datetime | - | {NULL} | 创建时间 |
| approved_at | datetime | - | {NULL} | 审核通过时间 |

## 10. 爬取的小说表 (crawled_novel)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 小说ID |
| title | varchar | 100 | {NOT NULL, INDEX} | 小说标题 |
| author | varchar | 50 | {NOT NULL} | 作者名称 |
| category | varchar | 30 | {NOT NULL} | 小说分类 |
| cover | varchar | 255 | {NULL} | 封面图片URL |
| intro | text | - | {NULL} | 小说简介 |
| status | varchar | 20 | {NULL} | 小说状态 |
| source_url | varchar | 255 | {NULL} | 来源URL |
| source_site | varchar | 50 | {NULL} | 来源网站 |
| created_at | datetime | - | {NULL} | 创建时间 |

## 11. 爬取的章节表 (crawled_chapter)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 章节ID |
| novel_id | int | - | {FK->crawled_novel.id, NOT NULL, INDEX} | 所属小说ID |
| chapter_number | int | - | {NOT NULL} | 章节序号 |
| title | varchar | 100 | {NOT NULL} | 章节标题 |
| content | text | - | {NOT NULL} | 章节内容 |
| source_url | varchar | 255 | {NULL} | 来源URL |
| created_at | datetime | - | {NULL} | 创建时间 |

## 12. 用户操作表 (user_action)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 操作ID |
| admin_id | int | - | {FK->admin.id, NOT NULL, INDEX} | 管理员ID |
| target_user_id | int | - | {FK->user.id, NOT NULL, INDEX} | 目标用户ID |
| action_type | varchar | 20 | {NOT NULL} | 操作类型 |
| reason | varchar | 255 | {NULL} | 操作原因 |
| duration | int | - | {NULL} | 持续时间（秒） |
| created_at | datetime | - | {NULL} | 创建时间 |

## 13. 用户收藏表 (user_collection)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 收藏ID |
| user_id | int | - | {FK->user.id, NOT NULL, INDEX} | 用户ID |
| novel_id | int | - | {FK->novel.id, NOT NULL, INDEX} | 小说ID |
| created_at | datetime | - | {NULL} | 创建时间 |

## 14. 用户阅读历史表 (user_history)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 历史记录ID |
| user_id | int | - | {FK->user.id, NOT NULL, INDEX} | 用户ID |
| novel_id | int | - | {FK->novel.id, NOT NULL, INDEX} | 小说ID |
| chapter_id | int | - | {FK->chapter.id, NOT NULL, INDEX} | 章节ID |
| last_read_time | datetime | - | {NULL} | 最后阅读时间 |

## 15. 用户关注表 (user_following)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 关注记录ID |
| follower_id | int | - | {FK->user.id, NOT NULL, INDEX} | 关注者ID |
| followed_id | int | - | {FK->user.id, NOT NULL, INDEX} | 被关注者ID |
| created_at | datetime | - | {NULL} | 创建时间 |

## 16. 私信表 (private_messages)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 消息ID |
| sender_id | int | - | {FK->user.id, NOT NULL, INDEX} | 发送者ID |
| recipient_id | int | - | {FK->user.id, NOT NULL, INDEX} | 接收者ID |
| content | text | - | {NOT NULL} | 消息内容 |
| created_at | datetime | - | {NULL} | 创建时间 |
| read_at | datetime | - | {NULL} | 阅读时间 |

## 17. 敏感词表 (sensitive_word)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 敏感词ID |
| word | varchar | 50 | {NOT NULL, UNIQUE} | 敏感词 |
| level | int | - | {NULL} | 敏感级别 |
| category | varchar | 20 | {NULL} | 分类 |
| added_by | int | - | {FK->admin.id, NULL, INDEX} | 添加人ID |
| created_at | datetime | - | {NULL} | 创建时间 |

## 18. 用户打赏表 (user_tips)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 打赏ID |
| tipper_id | int | - | {FK->user.id, NOT NULL, INDEX} | 打赏者ID |
| author_id | int | - | {FK->author.id, NOT NULL, INDEX} | 作者ID |
| novel_id | int | - | {FK->novel.id, NOT NULL, INDEX} | 小说ID |
| chapter_id | int | - | {FK->chapter.id, NULL, INDEX} | 章节ID |
| amount | int | - | {NOT NULL} | 打赏金额 |
| message | varchar | 200 | {NULL} | 打赏留言 |
| created_at | datetime | - | {NULL} | 创建时间 |

## 19. 用户备份表 (user_backup)

| 字段名 | 字段类型 | 长度 | 约束 | 中文注释 |
| ------ | -------- | ---- | ---- | -------- |
| id | int | - | {PK, AUTO_INCREMENT} | 备份ID |
| username | varchar | 50 | {NOT NULL} | 用户名 |
| phone | varchar | 20 | {NULL, UNIQUE} | 手机号 |
| email | varchar | 100 | {NULL, UNIQUE} | 电子邮箱 |
| password_hash | varchar | 128 | {NOT NULL} | 密码哈希 |
| role | varchar | 20 | {NULL} | 用户角色 |
| avatar | varchar | 255 | {NULL} | 头像URL |
| created_at | datetime | - | {NULL} | 创建时间 |
| updated_at | datetime | - | {NULL} | 更新时间 |
| status | tinyint | 1 | {NULL} | 用户状态 | 