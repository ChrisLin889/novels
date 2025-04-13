# 数据库迁移脚本说明

本目录包含了小说网站项目的数据库迁移脚本，用于在不同设备上快速搭建完整的数据库结构。

## 文件说明

- `complete_migration.sql`：完整的 MySQL 迁移脚本，包含所有表结构和初始数据
- `complete_migration_sqlite.sql`：SQLite 版本的完整迁移脚本，适用于开发环境
- `create_tables.sql`：原始 MySQL 表结构创建脚本
- `add_author_id.sql`：添加作者ID字段的迁移脚本

## MySQL 迁移使用方法

1. 确保已安装 MySQL 服务器并已启动

2. 创建数据库和用户（如果需要）
   ```sql
   CREATE DATABASE novel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'novel_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON novel_db.* TO 'novel_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. 使用完整迁移脚本导入数据库结构和初始数据
   ```bash
   mysql -u root -p < backend/migrations/complete_migration.sql
   ```
   
   或者指定用户和数据库：
   ```bash
   mysql -u novel_user -p novel_db < backend/migrations/complete_migration.sql
   ```

## SQLite 迁移使用方法

1. 确保已安装 SQLite3

2. 创建并导入数据库
   ```bash
   sqlite3 novel.db < backend/migrations/complete_migration_sqlite.sql
   ```

3. 验证数据库结构
   ```bash
   sqlite3 novel.db
   sqlite> .tables
   sqlite> .schema user
   ```

## 数据库配置

在使用迁移脚本后，需要更新应用程序的数据库连接配置：

### MySQL 配置
修改 `.env` 文件中的数据库连接参数：
```
DATABASE_URL=mysql://username:password@localhost/novel_db
```

### SQLite 配置
修改 `.env` 文件中的数据库连接参数：
```
DATABASE_URL=sqlite:///path/to/novel.db
```

## 注意事项

1. 生产环境使用前，建议修改或移除示例数据插入部分
2. MySQL 和 SQLite 版本的脚本略有不同，主要是语法和数据类型的差异
3. 使用 SQLite 时，请确保应用程序启用了外键约束支持
4. 如需对现有数据库进行结构变更，建议先备份数据 