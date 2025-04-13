-- Add missing admin tables and columns
USE novel_db;

-- Add sensitive_word table if not exists
CREATE TABLE IF NOT EXISTS `sensitive_word` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `word` VARCHAR(100) NOT NULL UNIQUE,
    `level` INT DEFAULT 1,
    `category` VARCHAR(50),
    `added_by` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`added_by`) REFERENCES `user` (`id`),
    INDEX `idx_word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='敏感词表';

-- Add content_audit table if not exists
CREATE TABLE IF NOT EXISTS `content_audit` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `content_type` VARCHAR(50) NOT NULL,
    `content_id` INT NOT NULL,
    `status` VARCHAR(20) DEFAULT 'pending',
    `reason` TEXT,
    `audited_by` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`audited_by`) REFERENCES `user` (`id`),
    INDEX `idx_content` (`content_type`, `content_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='内容审核表';

-- Add user_action table if not exists
CREATE TABLE IF NOT EXISTS `user_action` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_id` INT NOT NULL,
    `target_user_id` INT NOT NULL,
    `action_type` VARCHAR(50) NOT NULL,
    `reason` TEXT,
    `duration` INT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`),
    FOREIGN KEY (`target_user_id`) REFERENCES `user` (`id`),
    INDEX `idx_target_user` (`target_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户操作记录表';

-- Add crawled_novel table if not exists
CREATE TABLE IF NOT EXISTS `crawled_novel` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(100) NOT NULL,
    `author` VARCHAR(50) NOT NULL,
    `category` VARCHAR(30) NOT NULL,
    `cover` VARCHAR(255),
    `intro` TEXT,
    `status` VARCHAR(20) DEFAULT 'pending',
    `source_url` VARCHAR(255),
    `source_site` VARCHAR(100),
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_crawled_title` (`title`),
    INDEX `idx_crawled_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬取小说表';

-- Add crawled_chapter table if not exists
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