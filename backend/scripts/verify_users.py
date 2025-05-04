#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to verify users in the database
"""

import sys
import os
import json

# Add parent directory to path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import text

app = create_app()

def verify_users():
    """Print information about users, authors, and admins in the database"""
    with app.app_context():
        # Check users
        print("Users:")
        result = db.session.execute(text("SELECT id, username, email, phone, status FROM user"))
        for row in result:
            print(f"  ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, Phone: {row[3]}, Status: {row[4]}")
        
        # Check authors
        print("\nAuthors:")
        result = db.session.execute(text("SELECT id, user_id, pen_name, works_count, fans_count, created_at FROM author"))
        for row in result:
            print(f"  ID: {row[0]}, User ID: {row[1]}, Pen Name: {row[2]}, Works: {row[3]}, Fans: {row[4]}, Created: {row[5]}")
        
        # Check admins
        print("\nAdmins:")
        result = db.session.execute(text("SELECT id, user_id, admin_level, permissions, created_at FROM admin"))
        for row in result:
            print(f"  ID: {row[0]}, User ID: {row[1]}, Level: {row[2]}, Permissions: {row[3]}, Created: {row[4]}")

if __name__ == "__main__":
    verify_users() 