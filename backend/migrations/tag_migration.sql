-- 标签和小说标签关系的迁移脚本

-- 1. 创建标签表（如果不存在）
CREATE TABLE IF NOT EXISTS `tag` (
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

-- 2. 创建小说标签关联表（如果不存在）
CREATE TABLE IF NOT EXISTS `novel_tag` (
  `novel_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`novel_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `novel_tag_ibfk_1` FOREIGN KEY (`novel_id`) REFERENCES `novel` (`id`) ON DELETE CASCADE,
  CONSTRAINT `novel_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3. 添加示例标签数据
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

-- 注意：请确保执行此脚本前数据库中已存在category表 