-- Fix sensitive_word table structure
USE novel_db;

-- Add missing columns to sensitive_word table
ALTER TABLE sensitive_word 
ADD COLUMN level INT DEFAULT 1,
ADD COLUMN added_by INT,
ADD FOREIGN KEY (added_by) REFERENCES user(id); 