-- Fix user_action table structure
USE novel_db;

-- Drop existing user_action table and recreate with correct structure
DROP TABLE IF EXISTS user_action;

CREATE TABLE user_action (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    target_user_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    reason TEXT,
    duration INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES user(id),
    FOREIGN KEY (target_user_id) REFERENCES user(id),
    INDEX idx_target_user (target_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户操作记录表'; 