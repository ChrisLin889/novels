# 小说网站 - Novel Website

基于 Flask + Vue 的小说网站毕业设计项目

## 项目架构

- 前端：Vue3 + Vue Router + Axios + Element Plus
- 后端：Flask + SQLAlchemy + JWT
- 数据库：MySQL 8.0 + Redis
- 爬虫：Scrapy

## 目录结构

```
project/
├── backend/               # Flask 后端
│   ├── app/               # 应用代码
│   │   ├── api/           # API 路由
│   │   ├── models/        # 数据库模型
│   │   ├── services/      # 业务逻辑
│   │   ├── utils/         # 工具函数
│   │   └── config/        # 配置
│   ├── migrations/        # 数据库迁移
│   ├── tests/             # 测试
│   ├── .env               # 环境变量
│   ├── requirements.txt   # Python 依赖
│   └── run.py             # 入口文件
├── frontend/              # Vue 前端
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   └── package.json       # 前端依赖
└── doc/                   # 文档
```

## 第一阶段：环境搭建

这个阶段完成了基础开发环境的搭建：

1. 后端 Flask 项目结构
   - 用户模块：注册、登录、个人信息管理
   - 小说模块：小说列表、详情、章节内容、阅读历史
   - 爬虫模块：基础爬虫任务管理

2. 数据库设计
   - 用户、小说、章节、收藏、历史记录等表结构

## 如何运行

### 后端

1. 安装依赖
   ```
   cd backend
   pip install -r requirements.txt
   ```

2. 设置环境变量
   在 `.env` 文件中配置数据库连接

3. 创建数据库
   使用 `migrations/create_tables.sql` 创建数据库和表

4. 运行服务器
   ```
   flask run
   ```

### 前端 (下一阶段完成)

1. 安装依赖
   ```
   cd frontend
   npm install
   ```

2. 运行开发服务器
   ```
   npm run serve
   ```

## 测试账号

- 管理员：
  - 邮箱：admin@example.com
  - 密码：Admin123 