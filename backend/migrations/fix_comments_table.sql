-- Fix comments table to add likes column
USE novel_db;

-- Add likes column to comments table
ALTER TABLE comments ADD COLUMN likes INT DEFAULT 0; 