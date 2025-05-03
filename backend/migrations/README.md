# Database Migration Strategy

This directory contains the database migration files for the Novel application.

## Migration System

We use Alembic for database migrations. All database schema changes should be done through Alembic migrations to keep track of the database state.

## File Structure

- `versions/`: Contains all Alembic migration scripts
- `env.py`: Alembic environment configuration
- `alembic.ini`: Alembic configuration file
- `script.py.mako`: Template for new migration files

## Migration Workflow

1. To create a new migration:
   ```
   alembic revision -m "description of changes"
   ```

2. To upgrade the database to the latest version:
   ```
   alembic upgrade head
   ```

3. To downgrade the database:
   ```
   alembic downgrade -1
   ```

## Current Database State

The current database schema is maintained by the Alembic migration system. The latest version is `20251001002`, which includes all necessary tables, constraints, and indexes.

For reference, a consolidated SQL file is available at `backend/consolidated_migration.sql` which represents the complete database schema and can be used for fresh installations.

## History

- Original schema defined in `/novel_db_migration.sql`
- Recycle bin fields added in `/migrations/add_recycle_bin_fields.sql`
- Category table added in Alembic migration `20251001001`
- All migrations consolidated in `consolidated_migration.sql`

## Notes

- Always use Alembic for future database changes
- Keep the `consolidated_migration.sql` file updated when major changes are made
- The SQL files in this directory are for reference purposes only, not for direct execution 