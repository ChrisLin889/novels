from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.crawler import CrawlTask, CrawlTemp
from app.models.novel import Novel, Chapter
from app import db
from datetime import datetime
import subprocess
import os
import sys

crawler_bp = Blueprint('crawler', __name__)

@crawler_bp.route('/start', methods=['POST'])
@jwt_required()
def start_crawl():
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    data = request.get_json()
    
    if 'source_url' not in data or 'task_type' not in data:
        return jsonify({'error': 'source_url and task_type are required'}), 400
    
    # Create a new crawl task
    task = CrawlTask(
        source_url=data['source_url'],
        task_type=data['task_type'],
        status='pending'
    )
    
    db.session.add(task)
    db.session.commit()
    
    # In a real implementation, we would call Scrapy here
    # For now, we'll just simulate a successful task
    task.status = 'running'
    task.started_at = datetime.utcnow()
    db.session.commit()
    
    # This would be better handled by Celery in a real implementation
    # For now, we'll just mark it as completed
    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    task.success_count = 1
    db.session.commit()
    
    # Create a dummy crawl temp record
    temp = CrawlTemp(
        task_id=task.id,
        novel_title='Sample Novel',
        novel_author='Sample Author',
        novel_category='Fantasy',
        novel_intro='This is a sample novel intro.',
        chapter_title='Chapter 1: The Beginning',
        chapter_number=1,
        chapter_content='This is the content of the first chapter.',
        source_url=data['source_url']
    )
    
    db.session.add(temp)
    db.session.commit()
    
    return jsonify({
        'message': 'Crawl task started',
        'task_id': task.id
    }), 200

@crawler_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    tasks = CrawlTask.query.order_by(
        CrawlTask.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': page,
        'tasks': [task.to_dict() for task in tasks.items]
    }), 200

@crawler_bp.route('/review', methods=['GET'])
@jwt_required()
def get_pending_reviews():
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pending_items = CrawlTemp.query.filter_by(
        is_approved=False,
        is_rejected=False
    ).order_by(
        CrawlTemp.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': pending_items.total,
        'pages': pending_items.pages,
        'current_page': page,
        'items': [item.to_dict() for item in pending_items.items]
    }), 200

@crawler_bp.route('/approve/<int:item_id>', methods=['POST'])
@jwt_required()
def approve_item(item_id):
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    item = CrawlTemp.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    if item.is_approved or item.is_rejected:
        return jsonify({'error': 'Item already processed'}), 400
    
    # Mark as approved
    item.is_approved = True
    item.approved_at = datetime.utcnow()
    
    # Transfer to novel/chapter tables
    if item.novel_title and item.novel_author:
        # Check if novel already exists
        novel = Novel.query.filter_by(title=item.novel_title, author=item.novel_author).first()
        
        if not novel:
            # Create new novel
            novel = Novel(
                title=item.novel_title,
                author=item.novel_author,
                category=item.novel_category or 'Other',
                intro=item.novel_intro,
                cover=item.novel_cover_url or 'default_cover.jpg'
            )
            db.session.add(novel)
            db.session.flush()  # To get novel ID
        
        # Create chapter if available
        if item.chapter_title and item.chapter_content:
            # Check if chapter already exists
            existing_chapter = Chapter.query.filter_by(
                novel_id=novel.id,
                chapter_number=item.chapter_number
            ).first()
            
            if not existing_chapter:
                chapter = Chapter(
                    novel_id=novel.id,
                    chapter_number=item.chapter_number,
                    title=item.chapter_title,
                    content=item.chapter_content,
                    word_count=len(item.chapter_content)
                )
                db.session.add(chapter)
    
    db.session.commit()
    
    return jsonify({'message': 'Item approved and transferred to database'}), 200

@crawler_bp.route('/reject/<int:item_id>', methods=['POST'])
@jwt_required()
def reject_item(item_id):
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    item = CrawlTemp.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    if item.is_approved or item.is_rejected:
        return jsonify({'error': 'Item already processed'}), 400
    
    # Mark as rejected
    item.is_rejected = True
    
    db.session.commit()
    
    return jsonify({'message': 'Item rejected'}), 200 