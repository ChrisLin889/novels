# 小说平台测试文档

本目录包含了小说平台各个模块的测试脚本，用于验证API接口的功能是否正常。

## 目录结构

```
test/
  ├── README.md                  # 本文档
  ├── test_user.py               # 用户模块测试
  ├── test_novel.py              # 小说模块测试
  ├── test_author.py             # 作者模块测试
  ├── test_interaction.py        # 互动模块测试
  ├── test_search_cache.py       # 搜索与缓存模块测试
  ├── test_admin.py              # 管理模块测试
  └── run_all_tests.py           # 运行所有测试的脚本
```

## 测试账户

测试过程使用的测试账户信息：

1. 普通用户账户
   - 用户名: testuser
   - 密码: password123
   - 邮箱: user@test.com
   - 电话: 12345678901
   - 角色: user (普通用户，已注销作者身份)
   - 用户ID: 5

2. 作者账户
   - 用户名: testauthor
   - 密码: password123
   - 邮箱: author@test.com
   - 电话: 12345678902
   - 角色: author (作者)
   - 笔名: testauthor

3. 管理员账户
   - 用户名: testadmin
   - 密码: password123
   - 邮箱: admin@test.com
   - 电话: 12345678903
   - 角色: admin (管理员)
   - 管理级别: 1
   - 权限: {"content": true, "user": true}

## 如何运行测试

### 前提条件

1. 确保后端服务正在运行
2. 确保数据库中已包含测试账户
3. 安装必要的依赖：
   ```bash
   pip install requests unittest
   ```

### 运行所有测试

```bash
python run_all_tests.py
```

### 运行单个模块测试

```bash
# 运行用户模块测试
python test_user.py

# 运行小说模块测试
python test_novel.py

# 运行作者模块测试 
python test_author.py

# 运行互动模块测试
python test_interaction.py

# 运行搜索与缓存模块测试
python test_search_cache.py

# 运行管理模块测试
python test_admin.py
```

## 测试内容说明

### 用户模块测试 (test_user.py)

- 用户注册
- 用户登录
- 获取个人信息
- 修改个人信息
- 修改密码
- 管理员用户管理功能

### 小说模块测试 (test_novel.py)

- 获取小说列表
- 获取小说详情
- 更新小说信息
- 添加章节
- 获取章节列表
- 阅读章节
- 更新章节
- 删除章节

### 作者模块测试 (test_author.py)

- 获取作者信息
- 获取作者的小说列表
- 申请成为作者
- 更新作者信息
- 获取作者统计信息
- 关注作者
- 获取粉丝列表
- 注销作者身份

### 互动模块测试 (test_interaction.py)

- 添加评论
- 获取评论列表
- 回复评论
- 点赞评论
- 收藏小说
- 获取收藏列表
- 评分小说
- 举报内容
- 删除评论

### 搜索与缓存模块测试 (test_search_cache.py)

- 搜索小说
- 搜索作者
- 标签搜索
- 热门搜索
- 搜索历史
- 搜索建议
- 缓存状态
- 清除缓存
- 缓存指标

### 管理模块测试 (test_admin.py)

- 仪表盘统计数据
- 用户管理
- 内容管理
- 举报管理
- 作者申请审批
- 系统设置
- 系统日志
- 数据备份
- 系统通知

## 测试结果解读

每个测试脚本运行后会输出测试结果，包括：

- 测试通过数量
- 测试失败数量
- 测试失败的详细信息
- 总体测试是否通过

如果发现测试失败，请根据失败信息检查相应的API实现或测试用例是否正确。 