from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.novel import Novel, Chapter
from app import db
from datetime import datetime
import subprocess
import os
import sys

import_bp = Blueprint('import', __name__)

@import_bp.route('/novel', methods=['POST'])
@jwt_required()
def import_novel():
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    data = request.get_json()
    
    if 'title' not in data or 'author' not in data:
        return jsonify({'error': 'title and author are required'}), 400
    
    # Create a new novel
    novel = Novel(
        title=data['title'],
        author=data['author'],
        category=data.get('category', 'Other'),
        intro=data.get('intro', ''),
        cover=data.get('cover', 'default_cover.jpg'),
        status=data.get('status', 'ongoing')
    )
    
    db.session.add(novel)
    db.session.commit()
    
    return jsonify({
        'message': 'Novel imported successfully',
        'novel_id': novel.id
    }), 200

@import_bp.route('/chapter/<int:novel_id>', methods=['POST'])
@jwt_required()
def import_chapter(novel_id):
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    data = request.get_json()
    
    if 'title' not in data or 'content' not in data or 'chapter_number' not in data:
        return jsonify({'error': 'title, content, and chapter_number are required'}), 400
    
    # Check if novel exists
    novel = Novel.query.get(novel_id)
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    # Check if chapter already exists
    existing_chapter = Chapter.query.filter_by(
        novel_id=novel_id,
        chapter_number=data['chapter_number']
    ).first()
    
    if existing_chapter:
        return jsonify({'error': 'Chapter already exists'}), 409
    
    # Create new chapter
    chapter = Chapter(
        novel_id=novel_id,
        chapter_number=data['chapter_number'],
        title=data['title'],
        content=data['content'],
        word_count=len(data['content'])
    )
    
    db.session.add(chapter)
    db.session.commit()
    
    return jsonify({
        'message': 'Chapter imported successfully',
        'chapter_id': chapter.id
    }), 200

@import_bp.route('/bulk', methods=['POST'])
@jwt_required()
def bulk_import():
    # Check admin permission
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin permission required'}), 403
    
    data = request.get_json()
    
    if 'novel' not in data or 'chapters' not in data:
        return jsonify({'error': 'novel and chapters are required'}), 400
    
    novel_data = data['novel']
    chapters_data = data['chapters']
    
    if 'title' not in novel_data or 'author' not in novel_data:
        return jsonify({'error': 'novel title and author are required'}), 400
    
    # Create novel
    novel = Novel(
        title=novel_data['title'],
        author=novel_data['author'],
        category=novel_data.get('category', 'Other'),
        intro=novel_data.get('intro', ''),
        cover=novel_data.get('cover', 'default_cover.jpg'),
        status=novel_data.get('status', 'ongoing')
    )
    
    db.session.add(novel)
    db.session.flush()  # Get novel ID
    
    # Create chapters
    for chapter_data in chapters_data:
        if 'title' not in chapter_data or 'content' not in chapter_data or 'chapter_number' not in chapter_data:
            continue
        
        chapter = Chapter(
            novel_id=novel.id,
            chapter_number=chapter_data['chapter_number'],
            title=chapter_data['title'],
            content=chapter_data['content'],
            word_count=len(chapter_data['content'])
        )
        db.session.add(chapter)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Bulk import successful',
        'novel_id': novel.id,
        'chapters_count': len(chapters_data)
    }), 200 