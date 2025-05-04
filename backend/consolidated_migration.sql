-- Consolidated Database Migration Script for novel_db
-- This file represents the current state of the database structure
-- Generated on: $(date '+%Y-%m-%d')

-- Disable foreign key checks to avoid constraint issues during import
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist to prevent conflicts
DROP TABLE IF EXISTS `chapter`;
DROP TABLE IF EXISTS `comments`;
DROP TABLE IF EXISTS `content_audit`;
DROP TABLE IF EXISTS `user_collection`;
DROP TABLE IF EXISTS `user_following`;
DROP TABLE IF EXISTS `user_history`;
DROP TABLE IF EXISTS `private_messages`;
DROP TABLE IF EXISTS `novel_tag`;
DROP TABLE IF EXISTS `novel`;
DROP TABLE IF EXISTS `tag`;
DROP TABLE IF EXISTS `author_application`;
DROP TABLE IF EXISTS `author`;
DROP TABLE IF EXISTS `admin`;
DROP TABLE IF EXISTS `user_action`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `sensitive_word`;
DROP TABLE IF EXISTS `alembic_version`;

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `novel_db` DEFAULT CHARACTER SET utf8mb4 COLLATE=utf8mb4_unicode_ci;
USE `novel_db`;

-- Table structure for table `user`
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(128) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` int DEFAULT NULL,
  `banned_until` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `category`
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL,
  `description` text,
  `parent_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `tag`
CREATE TABLE `tag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `category_id` int DEFAULT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `admin`
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `admin_level` int DEFAULT NULL,
  `permissions` json DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `author`
CREATE TABLE `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pen_name` varchar(50) DEFAULT NULL,
  `bio` text,
  `verified` tinyint(1) DEFAULT '0',
  `income_account` varchar(100) DEFAULT NULL,
  `works_count` int DEFAULT '0',
  `fans_count` int DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `author_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `author_application`
CREATE TABLE `author_application` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pen_name` varchar(50) NOT NULL,
  `bio` text NOT NULL,
  `reason` text NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `admin_comment` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `author_application_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `author_application_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `novel`
CREATE TABLE `novel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `author` varchar(50) NOT NULL,
  `author_id` int DEFAULT NULL,
  `category` varchar(30) NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `intro` text,
  `status` varchar(20) DEFAULT NULL,
  `view_count` int DEFAULT NULL,
  `collection_count` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_novel_category` (`category`),
  KEY `ix_novel_title` (`title`),
  KEY `novel_ibfk_1` (`author_id`),
  CONSTRAINT `novel_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `novel_tag`
CREATE TABLE `novel_tag` (
  `novel_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`novel_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `novel_tag_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
  CONSTRAINT `novel_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `chapter`
CREATE TABLE `chapter` (
  `id` int NOT NULL AUTO_INCREMENT,
  `novel_id` int NOT NULL,
  `chapter_number` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `word_count` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_chapter_novel_id` (`novel_id`),
  CONSTRAINT `chapter_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `comments`
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `novel_id` int DEFAULT NULL,
  `chapter_id` int DEFAULT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `likes` int DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chapter_id` (`chapter_id`),
  KEY `ix_comments_user_id` (`user_id`),
  KEY `ix_comments_novel_id` (`novel_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`),
  CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `user_collection`
CREATE TABLE `user_collection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `novel_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_user_novel_collection` (`user_id`,`novel_id`),
  KEY `ix_user_collection_user_id` (`user_id`),
  KEY `ix_user_collection_novel_id` (`novel_id`),
  CONSTRAINT `user_collection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_collection_ibfk_2` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `user_history`
CREATE TABLE `user_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `novel_id` int NOT NULL,
  `chapter_id` int NOT NULL,
  `last_read_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chapter_id` (`chapter_id`),
  KEY `ix_user_history_user_id` (`user_id`),
  KEY `ix_user_history_novel_id` (`novel_id`),
  KEY `idx_user_novel_history` (`user_id`,`novel_id`),
  CONSTRAINT `user_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_history_ibfk_2` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`),
  CONSTRAINT `user_history_ibfk_3` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `user_following`
CREATE TABLE `user_following` (
  `id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int NOT NULL,
  `followed_id` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_follower_followed` (`follower_id`,`followed_id`),
  KEY `ix_user_following_follower_id` (`follower_id`),
  KEY `ix_user_following_followed_id` (`followed_id`),
  CONSTRAINT `user_following_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_following_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `private_messages`
CREATE TABLE `private_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `recipient_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `read_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_sender_recipient` (`sender_id`,`recipient_id`),
  KEY `ix_private_messages_recipient_id` (`recipient_id`),
  KEY `ix_private_messages_sender_id` (`sender_id`),
  KEY `idx_recipient_read` (`recipient_id`,`read_at`),
  CONSTRAINT `private_messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`),
  CONSTRAINT `private_messages_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `user_action`
CREATE TABLE `user_action` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `target_user_id` int NOT NULL,
  `action_type` varchar(20) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `target_user_id` (`target_user_id`),
  CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`),
  CONSTRAINT `user_action_ibfk_2` FOREIGN KEY (`target_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `content_audit`
CREATE TABLE `content_audit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content_type` varchar(20) NOT NULL,
  `content_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `content_audit_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `sensitive_word`
CREATE TABLE `sensitive_word` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(50) NOT NULL,
  `level` int DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `added_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sensitive_word_word` (`word`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `sensitive_word_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table structure for table `alembic_version`
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Insert initial data for category table (from Alembic migration)
INSERT INTO `category` (`id`, `name`, `type`, `description`, `parent_id`, `created_at`, `updated_at`) VALUES
(1, 'Fantasy', 'novel', '奇幻小说', NULL, NOW(), NOW()),
(2, 'Science Fiction', 'novel', '科幻小说', NULL, NOW(), NOW()),
(3, 'Romance', 'novel', '言情小说', NULL, NOW(), NOW()),
(4, 'Mystery', 'novel', '悬疑小说', NULL, NOW(), NOW()),
(5, '情节', 'tag', '与情节相关的标签', NULL, NOW(), NOW()),
(6, '角色', 'tag', '与角色相关的标签', NULL, NOW(), NOW()),
(7, '风格', 'tag', '与写作风格相关的标签', NULL, NOW(), NOW())
ON DUPLICATE KEY UPDATE `type`=VALUES(`type`), `description`=VALUES(`description`);

-- Insert initial tags (from tag_migration.sql)
INSERT IGNORE INTO `tag` (`name`, `description`) VALUES
('奇幻', '包含魔法、超自然能力或其他奇幻元素的故事'),
('科幻', '基于科学和技术发展的虚构故事'),
('冒险', '主角踏上冒险旅程的故事'),
('恋爱', '以爱情为主题的故事'),
('校园', '以学校为背景的故事'),
('悬疑', '充满谜团和悬念的故事'),
('历史', '以历史时期为背景的故事'),
('武侠', '描写武术家和侠客的故事'),
('仙侠', '具有道教神话元素的武侠故事'),
('玄幻', '充满东方神话和幻想元素的故事'),
('都市', '以现代城市为背景的故事'),
('游戏', '与游戏相关的故事'),
('体育', '与体育运动相关的故事'),
('轻小说', '面向年轻读者的轻松文学作品');

-- Insert Alembic version data
INSERT INTO `alembic_version` (`version_num`) VALUES ('20251001002')
ON DUPLICATE KEY UPDATE `version_num`='20251001002'; 