-- 为小说表添加回收站字段
ALTER TABLE `novel` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `novel` ADD COLUMN `deleted_at` DATETIME NULL;

-- 为章节表添加回收站字段
ALTER TABLE `chapter` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `chapter` ADD COLUMN `deleted_at` DATETIME NULL;

-- 为评论表添加回收站字段
ALTER TABLE `comments` ADD COLUMN `is_deleted` TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE `comments` ADD COLUMN `deleted_at` DATETIME NULL;

-- 为现有数据添加默认值
UPDATE `novel` SET `is_deleted` = 0 WHERE `is_deleted` IS NULL;
UPDATE `chapter` SET `is_deleted` = 0 WHERE `is_deleted` IS NULL;
UPDATE `comments` SET `is_deleted` = 0 WHERE `is_deleted` IS NULL;

-- 添加索引以优化查询性能
CREATE INDEX idx_novel_is_deleted ON `novel` (`is_deleted`);
CREATE INDEX idx_chapter_is_deleted ON `chapter` (`is_deleted`);
CREATE INDEX idx_comments_is_deleted ON `comments` (`is_deleted`); 