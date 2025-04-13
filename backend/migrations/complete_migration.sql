-- Complete Migration Script for Novel Database
-- This script includes all necessary tables for the novel web application
-- Generated for use on other devices

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS novel_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE novel_db;

-- User table
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL,
    `phone` VARCHAR(20) UNIQUE,
    `email` VARCHAR(100) UNIQUE,
    `password_hash` VARCHAR(128) NOT NULL,
    `role` VARCHAR(20) DEFAULT 'user',
    `avatar` VARCHAR(255) DEFAULT 'default.jpg',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `status` BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- Novel table with author_id
CREATE TABLE IF NOT EXISTS `novel` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `author` VARCHAR(50) NOT NULL,
    `author_id` INT,
    `category` VARCHAR(30) NOT NULL,
    `cover` VARCHAR(255) DEFAULT 'default_cover.jpg',
    `intro` TEXT,
    `status` VARCHAR(20) DEFAULT '连载中',
    `view_count` INT DEFAULT 0,
    `collection_count` INT DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
    INDEX `idx_title` (`title`),
    INDEX `idx_category` (`category`),
    INDEX `idx_author` (`author`),
    INDEX `idx_author_id` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小说表';

-- Chapter table
CREATE TABLE IF NOT EXISTS `chapter` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `novel_id` INT NOT NULL,
    `chapter_number` INT NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `content` TEXT NOT NULL,
    `word_count` INT DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
    INDEX `idx_novel_chapter` (`novel_id`, `chapter_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='章节表';

-- User collection table
CREATE TABLE IF NOT EXISTS `user_collection` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `novel_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uix_user_novel_collection` (`user_id`, `novel_id`),
    INDEX `idx_user_collection` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';

-- User history table
CREATE TABLE IF NOT EXISTS `user_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `novel_id` INT NOT NULL,
    `chapter_id` INT NOT NULL,
    `last_read_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE,
    INDEX `idx_user_novel_history` (`user_id`, `novel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户阅读历史表';

-- Comments table
CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `novel_id` INT,
    `chapter_id` INT,
    `content` TEXT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `likes` INT DEFAULT 0,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE,
    INDEX `idx_novel_comments` (`novel_id`),
    INDEX `idx_chapter_comments` (`chapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- Crawl task table
CREATE TABLE IF NOT EXISTS `crawl_task` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `source_url` VARCHAR(255) NOT NULL,
    `task_type` VARCHAR(50) NOT NULL,
    `status` VARCHAR(20) DEFAULT 'pending',
    `started_at` DATETIME,
    `completed_at` DATETIME,
    `success_count` INT DEFAULT 0,
    `error_count` INT DEFAULT 0,
    `error_message` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_task_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬虫任务表';

-- Crawl temp table
CREATE TABLE IF NOT EXISTS `crawl_temp` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `task_id` INT NOT NULL,
    `novel_title` VARCHAR(100),
    `novel_author` VARCHAR(50),
    `novel_category` VARCHAR(30),
    `novel_intro` TEXT,
    `novel_cover_url` VARCHAR(255),
    `chapter_title` VARCHAR(100),
    `chapter_number` INT,
    `chapter_content` TEXT,
    `source_url` VARCHAR(255) NOT NULL,
    `is_approved` BOOLEAN DEFAULT FALSE,
    `is_rejected` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `approved_at` DATETIME,
    FOREIGN KEY (`task_id`) REFERENCES `crawl_task` (`id`) ON DELETE CASCADE,
    INDEX `idx_task_approval` (`task_id`, `is_approved`, `is_rejected`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬虫临时数据表';

-- Sensitive word table
CREATE TABLE IF NOT EXISTS `sensitive_word` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `word` VARCHAR(50) NOT NULL UNIQUE,
    `level` INT DEFAULT 1,
    `category` VARCHAR(20),
    `added_by` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`added_by`) REFERENCES `user` (`id`),
    INDEX `idx_word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='敏感词表';

-- Content audit table
CREATE TABLE IF NOT EXISTS `content_audit` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content_type` VARCHAR(20) NOT NULL,
    `content_id` INT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'pending',
    `reason` VARCHAR(255),
    `audited_by` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`audited_by`) REFERENCES `user` (`id`),
    INDEX `idx_content` (`content_type`, `content_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='内容审核表';

-- User action table
CREATE TABLE IF NOT EXISTS `user_action` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_id` INT NOT NULL,
    `target_user_id` INT NOT NULL,
    `action_type` VARCHAR(20) NOT NULL,
    `reason` VARCHAR(255),
    `duration` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`),
    FOREIGN KEY (`target_user_id`) REFERENCES `user` (`id`),
    INDEX `idx_target_user` (`target_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户操作日志表';

-- Crawled novel table
CREATE TABLE IF NOT EXISTS `crawled_novel` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `author` VARCHAR(50) NOT NULL,
    `category` VARCHAR(30) NOT NULL,
    `cover` VARCHAR(255),
    `intro` TEXT,
    `status` VARCHAR(20) DEFAULT 'pending',
    `source_url` VARCHAR(255),
    `source_site` VARCHAR(50),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_crawled_title` (`title`),
    INDEX `idx_crawled_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬取小说表';

-- Crawled chapter table
CREATE TABLE IF NOT EXISTS `crawled_chapter` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `novel_id` INT NOT NULL,
    `chapter_number` INT NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `content` TEXT NOT NULL,
    `source_url` VARCHAR(255),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`novel_id`) REFERENCES `crawled_novel` (`id`) ON DELETE CASCADE,
    INDEX `idx_crawled_chapter` (`novel_id`, `chapter_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬取章节表';

-- Insert admin user (password: Admin123)
INSERT INTO `user` (`username`, `email`, `password_hash`, `role`)
VALUES ('管理员', 'admin@example.com', '$2b$12$SQEr/bj4/fYBjUfuHZzVIuQwE8pyQOUAuEf8aqfBe5TJ/YrGwDKpK', '管理员');

-- Insert sample novel data (optional - comment out if not needed for production)
INSERT INTO `novel` (`title`, `author`, `category`, `intro`, `status`)
VALUES 
('最后的英雄', '张明', '奇幻', '这是一个关于最后一位英雄对抗黑暗势力的故事。', '连载中'),
('永恒之爱', '李芳', '言情', '一个跨越几个世纪的爱情故事。', '连载中'),
('太空探索者', '王伟', '科幻', '人类冒险探索未知太空区域的故事。', '已完结');

-- Insert sample chapters (optional - comment out if not needed for production)
INSERT INTO `chapter` (`novel_id`, `chapter_number`, `title`, `content`, `word_count`)
VALUES 
(1, 1, '开始', '这是我们故事的开始。英雄在一个陌生的世界中醒来...', 100),
(1, 2, '旅程', '我们的英雄开始穿越危险的土地...', 120),
(2, 1, '初次相遇', '她在拥挤的房间里看到了他，知道她的生活将不再一样...', 110),
(3, 1, '发射日', '船员们准备进行这次将带领人类前往星空的历史性发射...', 150); 