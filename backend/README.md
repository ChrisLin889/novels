# 小说平台后端

这是小说平台的后端项目，基于Flask + SQLAlchemy技术栈构建。

## 项目结构

```
backend/
├── app/
│   ├── api/               # 控制器层 - API接口定义
│   │   ├── user.py        # 用户相关接口
│   │   ├── novel.py       # 小说相关接口
│   │   ├── interaction.py # 互动相关接口
│   │   ├── search.py      # 搜索相关接口
│   │   └── admin.py       # 管理相关接口
│   │
│   ├── dao/               # 数据访问层 - 数据库操作
│   │   ├── user_dao.py    # 用户数据访问
│   │   ├── novel_dao.py   # 小说数据访问
│   │   ├── interaction_dao.py # 互动数据访问
│   │   ├── search_dao.py  # 搜索数据访问
│   │   └── admin_dao.py   # 管理数据访问
│   │
│   ├── models/            # 数据模型层 - ORM定义
│   │   ├── user.py        # 用户模型
│   │   ├── novel.py       # 小说模型
│   │   ├── interaction.py # 互动模型
│   │   └── admin.py       # 管理模型
│   │
│   ├── services/          # 业务逻辑层 - 核心功能实现
│   │   ├── user_service.py    # 用户服务
│   │   ├── novel_service.py   # 小说服务
│   │   ├── interaction_service.py # 互动服务
│   │   ├── search_service.py # 搜索服务
│   │   └── admin_service.py  # 管理服务
│   │
│   ├── utils/             # 工具类
│   │   ├── auth.py        # 身份验证工具
│   │   ├── security.py    # 安全工具
│   │   └── validation.py  # 数据验证工具
│   │
│   └── tests/             # 单元测试
│       ├── test_api_endpoints.py    # API接口测试
│       ├── test_interaction_service.py # 互动服务测试
│       ├── test_search_service.py   # 搜索服务测试
│       └── test_admin_service.py    # 管理服务测试
│
├── run_all_tests.py       # 全量测试运行脚本
├── run_interaction_test.py # 互动模块测试脚本
├── run_search_test.py     # 搜索模块测试脚本
└── run_admin_test.py      # 管理模块测试脚本
```

## 已完成的模块

项目已实现以下核心模块：

1. **用户模块**：处理用户注册、登录、权限管理等功能
2. **小说模块**：管理小说元数据、章节内容、阅读记录等
3. **互动模块**：实现评论、关注、私信、打赏等社交功能
4. **搜索模块**：实现小说搜索、分类筛选、推荐功能
5. **管理模块**：提供内容审核、用户管理、敏感词过滤等功能
6. **工具模块**：包含身份验证、数据验证等通用工具

## 开发环境配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量（创建.env文件）：
```
DATABASE_URL=mysql+pymysql://user:password@localhost/novel_db
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

3. 初始化数据库：
```bash
flask db init
flask db migrate
flask db upgrade
```

4. 运行开发服务器：
```bash
flask run
```

## 测试

运行全部测试：
```bash
python run_all_tests.py
```

运行特定模块测试：
```bash
python run_interaction_test.py
python run_search_test.py
python run_admin_test.py
```

## API文档

API接口文档位于 `/doc/API接口文档.md`，详细描述了所有已实现的接口定义，包括请求方法、参数和返回值。

## 后续计划

以下模块正在规划中：
- 付费系统：实现充值和虚拟货币功能
- 推荐系统：基于用户行为的个性化推荐 