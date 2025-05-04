#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to add users from sign.txt to the database
"""

import sys
import os
import json
from datetime import datetime
import bcrypt

# Add parent directory to path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.author import Author
from app.models.admin import Admin
from sqlalchemy import text

app = create_app()

def hash_password(password):
    """Generate a bcrypt hash for a password"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def add_users_from_sign():
    """Add users from sign.txt to the database"""
    with app.app_context():
        # Check if users already exist without using the model (which has banned_until field)
        # that may not be in the database
        existing_users = {}
        result = db.session.execute(text(
            "SELECT id, username FROM user WHERE username IN ('testuser', 'testauthor', 'newadmin')"
        ))
        for row in result:
            existing_users[row[1]] = row[0]  # username: id
        
        # 1. Add regular user
        if 'testuser' not in existing_users:
            print("Adding regular user 'testuser'...")
            # Use a direct SQL insert to avoid model inconsistencies
            result = db.session.execute(text(
                """
                INSERT INTO user (username, email, phone, password_hash, status, created_at, updated_at) 
                VALUES (:username, :email, :phone, :password_hash, :status, NOW(), NOW())
                """
            ), {
                'username': 'testuser',
                'email': 'updated.user@test.com',
                'phone': '12345678901',
                'password_hash': hash_password('newpassword456'),
                'status': 0
            })
            db.session.commit()
            
            # Get the new user's ID
            result = db.session.execute(text(
                "SELECT id FROM user WHERE username = 'testuser'"
            ))
            user_id = result.scalar()
            print(f"Regular user created with ID: {user_id}")
        else:
            print(f"User 'testuser' already exists with ID: {existing_users['testuser']}")
            user_id = existing_users['testuser']
        
        # 2. Add author user
        if 'testauthor' not in existing_users:
            print("Adding author user 'testauthor'...")
            # Use a direct SQL insert
            result = db.session.execute(text(
                """
                INSERT INTO user (username, email, phone, password_hash, status, created_at, updated_at) 
                VALUES (:username, :email, :phone, :password_hash, :status, NOW(), NOW())
                """
            ), {
                'username': 'testauthor',
                'email': 'author@test.com',
                'phone': '12345678902',
                'password_hash': hash_password('password123'),
                'status': 0
            })
            db.session.commit()
            
            # Get the new user's ID
            result = db.session.execute(text(
                "SELECT id FROM user WHERE username = 'testauthor'"
            ))
            author_user_id = result.scalar()
            print(f"Author user created with ID: {author_user_id}")
            
            # Add author record
            result = db.session.execute(text(
                """
                INSERT INTO author (user_id, pen_name, works_count, fans_count, created_at, updated_at)
                VALUES (:user_id, :pen_name, :works_count, :fans_count, :created_at, :created_at)
                """
            ), {
                'user_id': author_user_id,
                'pen_name': 'testauthor',
                'works_count': 0,
                'fans_count': 0,
                'created_at': '2025-04-18 19:31:41'
            })
            db.session.commit()
            
            # Get the new author's ID
            result = db.session.execute(text(
                "SELECT id FROM author WHERE user_id = :user_id"
            ), {'user_id': author_user_id})
            author_id = result.scalar()
            print(f"Author record created with ID: {author_id}")
        else:
            print(f"User 'testauthor' already exists with ID: {existing_users['testauthor']}")
        
        # 3. Add admin user
        if 'newadmin' not in existing_users:
            print("Adding admin user 'newadmin'...")
            # Use a direct SQL insert
            result = db.session.execute(text(
                """
                INSERT INTO user (username, email, phone, password_hash, status, created_at, updated_at) 
                VALUES (:username, :email, :phone, :password_hash, :status, NOW(), NOW())
                """
            ), {
                'username': 'newadmin',
                'email': 'newadmin@test.com',
                'phone': '12345678900',
                'password_hash': hash_password('password123'),
                'status': 0
            })
            db.session.commit()
            
            # Get the new user's ID
            result = db.session.execute(text(
                "SELECT id FROM user WHERE username = 'newadmin'"
            ))
            admin_user_id = result.scalar()
            print(f"Admin user created with ID: {admin_user_id}")
            
            # Add admin record
            result = db.session.execute(text(
                """
                INSERT INTO admin (user_id, admin_level, permissions, created_at, updated_at)
                VALUES (:user_id, :admin_level, :permissions, :created_at, :created_at)
                """
            ), {
                'user_id': admin_user_id,
                'admin_level': 1,
                'permissions': json.dumps({"content": True, "user": True}),
                'created_at': '2025-04-19 03:30:55'
            })
            db.session.commit()
            
            # Get the new admin's ID
            result = db.session.execute(text(
                "SELECT id FROM admin WHERE user_id = :user_id"
            ), {'user_id': admin_user_id})
            admin_id = result.scalar()
            print(f"Admin record created with ID: {admin_id}")
        else:
            print(f"User 'newadmin' already exists with ID: {existing_users['newadmin']}")
        
        print("All users added successfully!")

if __name__ == "__main__":
    add_users_from_sign() 