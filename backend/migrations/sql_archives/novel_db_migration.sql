-- MySQL database migration script for novel_db
-- Generated for data migration

-- Disable foreign key checks to avoid constraint issues during import
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist to prevent conflicts
DROP TABLE IF EXISTS `chapter`;
DROP TABLE IF EXISTS `comments`;
DROP TABLE IF EXISTS `content_audit`;
DROP TABLE IF EXISTS `crawl_task`;
DROP TABLE IF EXISTS `crawl_temp`;
DROP TABLE IF EXISTS `crawled_chapter`;
DROP TABLE IF EXISTS `crawled_novel`;
DROP TABLE IF EXISTS `user_tips`;
DROP TABLE IF EXISTS `user_history`;
DROP TABLE IF EXISTS `user_collection`;
DROP TABLE IF EXISTS `user_following`;
DROP TABLE IF EXISTS `user_action`;
DROP TABLE IF EXISTS `private_messages`;
DROP TABLE IF EXISTS `novel_tag`;
DROP TABLE IF EXISTS `novel`;
DROP TABLE IF EXISTS `tag`;
DROP TABLE IF EXISTS `author_application`;
DROP TABLE IF EXISTS `author`;
DROP TABLE IF EXISTS `content_report`;
DROP TABLE IF EXISTS `admin`;
DROP TABLE IF EXISTS `user_backup`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `sensitive_word`;

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `novel_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
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
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `user_backup`
CREATE TABLE `user_backup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(128) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `category`
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `admin`
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `admin_level` tinyint DEFAULT '1',
  `permissions` json DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `author_application`
CREATE TABLE `author_application` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pen_name` varchar(50) NOT NULL,
  `bio` text NOT NULL,
  `reason` text NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `admin_id` int DEFAULT NULL,
  `admin_comment` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `author_application_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `author_application_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `novel`
CREATE TABLE `novel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `author_id` int DEFAULT NULL COMMENT 'References author.id instead of user.id',
  `title` varchar(100) NOT NULL,
  `author` varchar(50) NOT NULL,
  `category` varchar(30) NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `intro` text,
  `status` varchar(20) DEFAULT NULL,
  `view_count` int DEFAULT NULL,
  `collection_count` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_novel_category` (`category`),
  KEY `ix_novel_title` (`title`),
  KEY `novel_ibfk_1` (`author_id`),
  CONSTRAINT `novel_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `novel_tag`
CREATE TABLE `novel_tag` (
  `novel_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`novel_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `novel_tag_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
  CONSTRAINT `novel_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  PRIMARY KEY (`id`),
  KEY `ix_chapter_novel_id` (`novel_id`),
  CONSTRAINT `chapter_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `comments`
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `novel_id` int DEFAULT NULL,
  `chapter_id` int DEFAULT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `likes` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chapter_id` (`chapter_id`),
  KEY `ix_comments_novel_id` (`novel_id`),
  KEY `ix_comments_user_id` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`),
  CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  CONSTRAINT `user_action_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_action_ibfk_2` FOREIGN KEY (`target_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `content_report`
CREATE TABLE `content_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `target_type` varchar(20) NOT NULL,
  `target_id` int NOT NULL,
  `reason` varchar(100) NOT NULL,
  `description` text,
  `status` varchar(20) DEFAULT 'pending',
  `admin_comment` text,
  `admin_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_target` (`target_type`,`target_id`),
  CONSTRAINT `content_report_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `content_report_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='内容举报表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `content_audit`
CREATE TABLE `content_audit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content_type` varchar(20) NOT NULL,
  `content_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `admin_id` int DEFAULT NULL COMMENT 'References admin.id',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `content_audit_ibfk_1` (`admin_id`),
  CONSTRAINT `content_audit_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `user_tips`
CREATE TABLE `user_tips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipper_id` int NOT NULL,
  `author_id` int NOT NULL,
  `novel_id` int NOT NULL,
  `chapter_id` int DEFAULT NULL,
  `amount` int NOT NULL,
  `message` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chapter_id` (`chapter_id`),
  KEY `ix_user_tips_tipper_id` (`tipper_id`),
  KEY `ix_user_tips_author_id` (`author_id`),
  KEY `ix_user_tips_novel_id` (`novel_id`),
  CONSTRAINT `user_tips_ibfk_1` FOREIGN KEY (`tipper_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_tips_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_tips_ibfk_3` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`),
  CONSTRAINT `user_tips_ibfk_4` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `crawl_task`
CREATE TABLE `crawl_task` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_url` varchar(255) NOT NULL,
  `task_type` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `success_count` int DEFAULT NULL,
  `error_count` int DEFAULT NULL,
  `error_message` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `crawled_novel`
CREATE TABLE `crawled_novel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `author` varchar(50) NOT NULL, 
  `category` varchar(30) NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `intro` text,
  `status` varchar(20) DEFAULT NULL,
  `source_url` varchar(255) DEFAULT NULL,
  `source_site` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `crawled_chapter`
CREATE TABLE `crawled_chapter` (
  `id` int NOT NULL AUTO_INCREMENT,
  `novel_id` int NOT NULL,
  `chapter_number` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `source_url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `novel_id` (`novel_id`),
  CONSTRAINT `crawled_chapter_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `crawled_novel` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `crawl_temp`
CREATE TABLE `crawl_temp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `novel_title` varchar(100) DEFAULT NULL,
  `novel_author` varchar(50) DEFAULT NULL,
  `novel_category` varchar(30) DEFAULT NULL,
  `novel_intro` text DEFAULT NULL,
  `novel_cover_url` varchar(255) DEFAULT NULL,
  `chapter_title` varchar(100) DEFAULT NULL,
  `chapter_number` int DEFAULT NULL,
  `chapter_content` text DEFAULT NULL,
  `source_url` varchar(255) NOT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `is_rejected` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `crawl_temp_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `crawl_task` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Instructions for data export
-- Run the following commands to export data from the source database:
-- 
-- To export all data:
-- mysqldump -u root -p'ok123456' novel_db > novel_db_full_export.sql
--
-- To export structure only:
-- mysqldump -u root -p'ok123456' --no-data novel_db > novel_db_structure.sql
--
-- To export data only:
-- mysqldump -u root -p'ok123456' --no-create-info novel_db > novel_db_data_only.sql
--
-- To export selected tables:
-- mysqldump -u root -p'ok123456' novel_db user novel chapter > novel_db_core_tables.sql
--
-- Instructions for importing data to target database:
-- 
-- Create database if not exists:
-- mysql -u [target_username] -p -e "CREATE DATABASE IF NOT EXISTS novel_db"
--
-- Import the data:
-- mysql -u [target_username] -p novel_db < novel_db_full_export.sql
--
-- Note: Replace [target_username] with the username for your target database system