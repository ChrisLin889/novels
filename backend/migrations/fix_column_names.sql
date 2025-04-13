-- Fix column names to match model expectations
USE novel_db;

-- Fix content_audit table
ALTER TABLE content_audit CHANGE COLUMN reviewer_id audited_by INT; 