-- Migration: Add audit status columns to novel and chapter tables
-- Created on: $(date '+%Y-%m-%d')

-- Step 1: Add audit_status columns with default 'approved' to protect existing content if they don't exist
-- Use SHOW COLUMNS queries to check if columns exist
SET @dbname = 'novel_db';

-- Check if audit_status column exists in novel table
SET @query_novel = CONCAT('SELECT COUNT(*) INTO @novel_column_exists FROM information_schema.columns WHERE table_schema = ''', @dbname, ''' AND table_name = ''novel'' AND column_name = ''audit_status''');
PREPARE stmt FROM @query_novel;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check if audit_status column exists in chapter table
SET @query_chapter = CONCAT('SELECT COUNT(*) INTO @chapter_column_exists FROM information_schema.columns WHERE table_schema = ''', @dbname, ''' AND table_name = ''chapter'' AND column_name = ''audit_status''');
PREPARE stmt FROM @query_chapter;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check if exempt_from_audit column exists in author table
SET @query_author = CONCAT('SELECT COUNT(*) INTO @author_column_exists FROM information_schema.columns WHERE table_schema = ''', @dbname, ''' AND table_name = ''author'' AND column_name = ''exempt_from_audit''');
PREPARE stmt FROM @query_author;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add audit_status to novel table if it doesn't exist
SET @alter_novel = IF(@novel_column_exists = 0, 
    'ALTER TABLE novel ADD COLUMN audit_status ENUM(\'pending\', \'approved\', \'rejected\') DEFAULT \'approved\'',
    'SELECT \'Novel audit_status column already exists\' AS message');
PREPARE stmt FROM @alter_novel;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add audit_status to chapter table if it doesn't exist
SET @alter_chapter = IF(@chapter_column_exists = 0, 
    'ALTER TABLE chapter ADD COLUMN audit_status ENUM(\'pending\', \'approved\', \'rejected\') DEFAULT \'approved\'',
    'SELECT \'Chapter audit_status column already exists\' AS message');
PREPARE stmt FROM @alter_chapter;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Step 2: Ensure all existing content status is 'approved'
UPDATE novel SET audit_status = 'approved' WHERE 1=1;
UPDATE chapter SET audit_status = 'approved' WHERE 1=1;

-- Step 3: Change default value to 'pending' for new content
ALTER TABLE novel ALTER COLUMN audit_status SET DEFAULT 'pending';
ALTER TABLE chapter ALTER COLUMN audit_status SET DEFAULT 'pending';

-- Step 4: Add exempt_from_audit flag to author table if it doesn't exist
SET @alter_author = IF(@author_column_exists = 0, 
    'ALTER TABLE author ADD COLUMN exempt_from_audit BOOLEAN DEFAULT FALSE',
    'SELECT \'Author exempt_from_audit column already exists\' AS message');
PREPARE stmt FROM @alter_author;
EXECUTE stmt;
DEALLOCATE PREPARE stmt; 