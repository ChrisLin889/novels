-- Fix crawled_novel table structure
USE novel_db;

-- Add source_site column to crawled_novel table
ALTER TABLE crawled_novel ADD COLUMN source_site VARCHAR(100); 