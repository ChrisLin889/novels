-- SQLite doesn't support ALTER TABLE ADD COLUMN with NOT NULL constraint
-- So we need to create a new table and copy the data

-- Create new table with author_id
CREATE TABLE novel_new (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    cover TEXT DEFAULT 'default_cover.jpg',
    intro TEXT,
    status TEXT DEFAULT 'ongoing',
    view_count INTEGER DEFAULT 0,
    collection_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user(id)
);

-- Copy data from old table to new table
INSERT INTO novel_new (id, title, author_id, category, cover, intro, status, view_count, collection_count, created_at, updated_at)
SELECT n.id, n.title, u.id, n.category, n.cover, n.intro, n.status, n.view_count, n.collection_count, n.created_at, n.updated_at
FROM novel n
JOIN user u ON u.username = n.author;

-- Drop old table
DROP TABLE novel;

-- Rename new table to original name
ALTER TABLE novel_new RENAME TO novel;

-- Create indexes
CREATE INDEX ix_novel_author_id ON novel (author_id);
CREATE INDEX ix_novel_category ON novel (category);
CREATE INDEX ix_novel_title ON novel (title); 