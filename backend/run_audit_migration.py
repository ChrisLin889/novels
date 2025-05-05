#!/usr/bin/env python3
"""
Run the audit status migration script
"""
import os
import sys
import subprocess
from datetime import datetime

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATION_FILE = os.path.join(SCRIPT_DIR, 'migrations', 'add_audit_status.sql')

def run_migration():
    """Run the audit status migration script"""
    print(f"Running audit status migration script: {MIGRATION_FILE}")
    
    # Check if the file exists
    if not os.path.exists(MIGRATION_FILE):
        print(f"Error: Migration file not found: {MIGRATION_FILE}")
        return False
    
    # Get database connection details from environment or use defaults
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'ok123456')  # Set default password
    db_name = os.environ.get('DB_NAME', 'novel_db')
    
    # Create the mysql command
    cmd = f"mysql -h{db_host} -u{db_user}"
    if db_password:
        cmd += f" -p{db_password}"
    cmd += f" {db_name} < {MIGRATION_FILE}"
    
    # Run the command
    print(f"Executing: mysql -h{db_host} -u{db_user} -p******** {db_name} < {MIGRATION_FILE}")
    result = os.system(cmd)
    
    if result == 0:
        print(f"Migration completed successfully at {datetime.now()}")
        return True
    else:
        print(f"Migration failed with error code: {result}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1) 