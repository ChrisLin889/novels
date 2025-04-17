-- MySQL database migration script for novel_db
-- Modified version to separate users, authors and administrators into different tables

-- Disable foreign key checks to avoid constraint issues during import
SET FOREIGN_KEY_CHECKS = 0;

-- Create backup of user table (if not exists)
DROP TABLE IF EXISTS `user_backup`;
CREATE TABLE IF NOT EXISTS `user_backup` LIKE `user`;
INSERT INTO `user_backup` SELECT * FROM `user`;

-- Create new tables for authors and admins
DROP TABLE IF EXISTS `author`;
CREATE TABLE IF NOT EXISTS `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pen_name` varchar(50) DEFAULT NULL,
  `bio` text,
  `verified` tinyint(1) DEFAULT 0,
  `income_account` varchar(100) DEFAULT NULL,
  `works_count` int DEFAULT 0,
  `fans_count` int DEFAULT 0,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `author_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `admin_level` tinyint DEFAULT 1,
  `permissions` json,
  `department` varchar(50) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Migrate existing users to author and admin tables based on their role
INSERT INTO `author` (`user_id`, `pen_name`, `created_at`, `updated_at`)
SELECT `id`, `username`, `created_at`, `updated_at` FROM `user` WHERE `role` = 'author';

INSERT INTO `admin` (`user_id`, `admin_level`, `permissions`, `created_at`, `updated_at`)
SELECT `id`, 1, JSON_OBJECT('content', true, 'user', true), `created_at`, `updated_at` FROM `user` WHERE `role` = 'admin';

-- Check and drop foreign keys if they exist
SELECT constraint_name INTO @novel_fk FROM information_schema.table_constraints 
WHERE table_schema = 'novel_db' AND table_name = 'novel' 
AND constraint_type = 'FOREIGN KEY' AND constraint_name = 'novel_ibfk_1';

SET @drop_novel_fk = IF(@novel_fk IS NOT NULL, 'ALTER TABLE `novel` DROP FOREIGN KEY `novel_ibfk_1`', 'SELECT 1');
PREPARE stmt FROM @drop_novel_fk;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Update novel table to reference author table instead of user table
ALTER TABLE `novel` CHANGE COLUMN `author_id` `author_id` int NULL COMMENT 'References author.id instead of user.id';

-- Update novel relationships
UPDATE `novel` n
JOIN `user` u ON n.author_id = u.id
JOIN `author` a ON u.id = a.user_id
SET n.author_id = a.id
WHERE n.author_id IS NOT NULL;

-- Add foreign key constraint back
ALTER TABLE `novel` ADD CONSTRAINT `novel_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);

-- Update content_audit table to reference admin table
-- We don't have a content_audit_ibfk_1 foreign key, so just change the column
ALTER TABLE `content_audit` CHANGE COLUMN `audited_by` `admin_id` int NULL COMMENT 'References admin.id';

-- Update content_audit relationships
UPDATE `content_audit` ca
JOIN `user` u ON ca.admin_id = u.id  -- We just renamed audited_by to admin_id
JOIN `admin` a ON u.id = a.user_id
SET ca.admin_id = a.id
WHERE ca.admin_id IS NOT NULL;

-- Add foreign key constraint
ALTER TABLE `content_audit` ADD CONSTRAINT `content_audit_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`);

-- Remove role column from user table
ALTER TABLE `user` DROP COLUMN `role`;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Migration verification queries
-- Run these to verify the migration worked correctly
-- 
-- SELECT COUNT(*) FROM user_backup;
-- SELECT COUNT(*) FROM author;
-- SELECT COUNT(*) FROM admin;
-- 
-- SELECT u.id, u.username, a.id AS author_id, ad.id AS admin_id
-- FROM user u
-- LEFT JOIN author a ON u.id = a.user_id
-- LEFT JOIN admin ad ON u.id = ad.user_id;
-- 
-- SELECT n.id, n.title, n.author, n.author_id, a.user_id
-- FROM novel n
-- LEFT JOIN author a ON n.author_id = a.id;
--
-- SELECT ca.id, ca.content_type, ca.content_id, ca.admin_id, a.user_id
-- FROM content_audit ca
-- LEFT JOIN admin a ON ca.admin_id = a.id; 