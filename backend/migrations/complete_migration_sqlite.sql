-- Complete Migration Script for Novel Database (SQLite Version)
-- This script includes all necessary tables for the novel web application
-- Generated for use on other devices

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- User table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    phone TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    avatar TEXT DEFAULT 'default.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1
);

-- Novel table with author_id
CREATE TABLE IF NOT EXISTS novel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    author_id INTEGER,
    category TEXT NOT NULL,
    cover TEXT DEFAULT 'default_cover.jpg',
    intro TEXT,
    status TEXT DEFAULT '连载中',
    view_count INTEGER DEFAULT 0,
    collection_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user(id)
);

-- Create indexes for novel table
CREATE INDEX IF NOT EXISTS ix_novel_title ON novel (title);
CREATE INDEX IF NOT EXISTS ix_novel_category ON novel (category);
CREATE INDEX IF NOT EXISTS ix_novel_author ON novel (author);
CREATE INDEX IF NOT EXISTS ix_novel_author_id ON novel (author_id);

-- Chapter table
CREATE TABLE IF NOT EXISTS chapter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL,
    chapter_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    word_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (novel_id) REFERENCES novel(id) ON DELETE CASCADE
);

-- Create index for chapter table
CREATE INDEX IF NOT EXISTS ix_novel_chapter ON chapter (novel_id, chapter_number);

-- User collection table
CREATE TABLE IF NOT EXISTS user_collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    novel_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (novel_id) REFERENCES novel(id) ON DELETE CASCADE,
    UNIQUE (user_id, novel_id)
);

-- Create index for user_collection table
CREATE INDEX IF NOT EXISTS ix_user_collection ON user_collection (user_id);

-- User history table
CREATE TABLE IF NOT EXISTS user_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    novel_id INTEGER NOT NULL,
    chapter_id INTEGER NOT NULL,
    last_read_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (novel_id) REFERENCES novel(id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
);

-- Create index for user_history table
CREATE INDEX IF NOT EXISTS ix_user_novel_history ON user_history (user_id, novel_id);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    novel_id INTEGER,
    chapter_id INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (novel_id) REFERENCES novel(id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapter(id) ON DELETE CASCADE
);

-- Create indexes for comments table
CREATE INDEX IF NOT EXISTS ix_novel_comments ON comments (novel_id);
CREATE INDEX IF NOT EXISTS ix_chapter_comments ON comments (chapter_id);

-- Crawl task table
CREATE TABLE IF NOT EXISTS crawl_task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT NOT NULL,
    task_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    success_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for crawl_task table
CREATE INDEX IF NOT EXISTS ix_task_status ON crawl_task (status);

-- Crawl temp table
CREATE TABLE IF NOT EXISTS crawl_temp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    novel_title TEXT,
    novel_author TEXT,
    novel_category TEXT,
    novel_intro TEXT,
    novel_cover_url TEXT,
    chapter_title TEXT,
    chapter_number INTEGER,
    chapter_content TEXT,
    source_url TEXT NOT NULL,
    is_approved INTEGER DEFAULT 0,
    is_rejected INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES crawl_task(id) ON DELETE CASCADE
);

-- Create index for crawl_temp table
CREATE INDEX IF NOT EXISTS ix_task_approval ON crawl_temp (task_id, is_approved, is_rejected);

-- Sensitive word table
CREATE TABLE IF NOT EXISTS sensitive_word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE,
    level INTEGER DEFAULT 1,
    category TEXT,
    added_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (added_by) REFERENCES user(id)
);

-- Create index for sensitive_word table
CREATE INDEX IF NOT EXISTS ix_word ON sensitive_word (word);

-- Content audit table
CREATE TABLE IF NOT EXISTS content_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type TEXT NOT NULL,
    content_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    reason TEXT,
    audited_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (audited_by) REFERENCES user(id)
);

-- Create indexes for content_audit table
CREATE INDEX IF NOT EXISTS ix_content ON content_audit (content_type, content_id);
CREATE INDEX IF NOT EXISTS ix_status ON content_audit (status);

-- User action table
CREATE TABLE IF NOT EXISTS user_action (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    target_user_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    reason TEXT,
    duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES user(id),
    FOREIGN KEY (target_user_id) REFERENCES user(id)
);

-- Create index for user_action table
CREATE INDEX IF NOT EXISTS ix_target_user ON user_action (target_user_id);

-- Crawled novel table
CREATE TABLE IF NOT EXISTS crawled_novel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    cover TEXT,
    intro TEXT,
    status TEXT DEFAULT 'pending',
    source_url TEXT,
    source_site TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for crawled_novel table
CREATE INDEX IF NOT EXISTS ix_crawled_title ON crawled_novel (title);
CREATE INDEX IF NOT EXISTS ix_crawled_status ON crawled_novel (status);

-- Crawled chapter table
CREATE TABLE IF NOT EXISTS crawled_chapter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL,
    chapter_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (novel_id) REFERENCES crawled_novel(id) ON DELETE CASCADE
);

-- Create index for crawled_chapter table
CREATE INDEX IF NOT EXISTS ix_crawled_chapter ON crawled_chapter (novel_id, chapter_number);

-- Insert admin user (password: Admin123)
INSERT INTO user (username, email, password_hash, role)
VALUES ('管理员', 'admin@example.com', '$2b$12$SQEr/bj4/fYBjUfuHZzVIuQwE8pyQOUAuEf8aqfBe5TJ/YrGwDKpK', '管理员');

-- Insert sample novel data (optional - comment out if not needed for production)
INSERT INTO novel (title, author, category, intro, status)
VALUES 
('最后的英雄', '张明', '奇幻', '这是一个关于最后一位英雄对抗黑暗势力的故事。', '连载中'),
('永恒之爱', '李芳', '言情', '一个跨越几个世纪的爱情故事。', '连载中'),
('太空探索者', '王伟', '科幻', '人类冒险探索未知太空区域的故事。', '已完结');

-- Insert sample chapters (optional - comment out if not needed for production)
INSERT INTO chapter (novel_id, chapter_number, title, content, word_count)
VALUES 
(1, 1, '开始', '这是我们故事的开始。英雄在一个陌生的世界中醒来...', 100),
(1, 2, '旅程', '我们的英雄开始穿越危险的土地...', 120),
(2, 1, '初次相遇', '她在拥挤的房间里看到了他，知道她的生活将不再一样...', 110),
(3, 1, '发射日', '船员们准备进行这次将带领人类前往星空的历史性发射...', 150); 