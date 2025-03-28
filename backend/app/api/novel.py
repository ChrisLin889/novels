from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.novel import Novel, Chapter
from app.models.interaction import UserCollection, UserHistory, Comment
from app import db
from sqlalchemy import desc

novel_bp = Blueprint('novel', __name__)

@novel_bp.route('/list', methods=['GET'])
def get_novel_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    
    query = Novel.query
    
    if category:
        query = query.filter_by(category=category)
    
    novels = query.order_by(desc(Novel.updated_at)).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': novels.total,
        'pages': novels.pages,
        'current_page': page,
        'novels': [novel.to_dict() for novel in novels.items]
    }), 200

@novel_bp.route('/detail/<int:novel_id>', methods=['GET'])
def get_novel_detail(novel_id):
    novel = Novel.query.get(novel_id)
    
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    # Increment view count
    novel.view_count += 1
    db.session.commit()
    
    novel_dict = novel.to_dict()
    
    # Get first 20 chapters
    chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number).limit(20).all()
    novel_dict['chapters'] = [chapter.to_dict() for chapter in chapters]
    
    return jsonify(novel_dict), 200

@novel_bp.route('/chapter/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    # Get previous and next chapter
    prev_chapter = Chapter.query.filter_by(
        novel_id=chapter.novel_id
    ).filter(Chapter.chapter_number < chapter.chapter_number).order_by(
        desc(Chapter.chapter_number)
    ).first()
    
    next_chapter = Chapter.query.filter_by(
        novel_id=chapter.novel_id
    ).filter(Chapter.chapter_number > chapter.chapter_number).order_by(
        Chapter.chapter_number
    ).first()
    
    result = chapter.to_dict(include_content=True)
    result['prev_chapter'] = prev_chapter.to_dict() if prev_chapter else None
    result['next_chapter'] = next_chapter.to_dict() if next_chapter else None
    
    # Update reading history if user is logged in
    user_id = get_jwt_identity() if request.headers.get('Authorization') else None
    if user_id:
        history = UserHistory.query.filter_by(
            user_id=user_id,
            novel_id=chapter.novel_id
        ).first()
        
        if history:
            history.chapter_id = chapter.id
        else:
            history = UserHistory(
                user_id=user_id,
                novel_id=chapter.novel_id,
                chapter_id=chapter.id
            )
            db.session.add(history)
        
        db.session.commit()
    
    return jsonify(result), 200

@novel_bp.route('/collection', methods=['POST'])
@jwt_required()
def toggle_collection():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'novel_id' not in data:
        return jsonify({'error': 'Novel ID is required'}), 400
    
    novel_id = data['novel_id']
    
    # Check if novel exists
    novel = Novel.query.get(novel_id)
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    collection = UserCollection.query.filter_by(
        user_id=user_id,
        novel_id=novel_id
    ).first()
    
    if collection:
        # Remove from collection
        db.session.delete(collection)
        novel.collection_count = max(0, novel.collection_count - 1)
        message = 'Removed from collection'
        is_collected = False
    else:
        # Add to collection
        collection = UserCollection(user_id=user_id, novel_id=novel_id)
        db.session.add(collection)
        novel.collection_count += 1
        message = 'Added to collection'
        is_collected = True
    
    db.session.commit()
    
    return jsonify({
        'message': message,
        'is_collected': is_collected
    }), 200

@novel_bp.route('/collection', methods=['GET'])
@jwt_required()
def get_collections():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    collections = UserCollection.query.filter_by(
        user_id=user_id
    ).order_by(
        desc(UserCollection.created_at)
    ).paginate(page=page, per_page=per_page)
    
    # Get novel details for each collection
    result = []
    for collection in collections.items:
        novel = Novel.query.get(collection.novel_id)
        if novel:
            novel_dict = novel.to_dict()
            novel_dict['collection_time'] = collection.created_at.isoformat()
            result.append(novel_dict)
    
    return jsonify({
        'total': collections.total,
        'pages': collections.pages,
        'current_page': page,
        'collections': result
    }), 200

@novel_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    history_records = UserHistory.query.filter_by(
        user_id=user_id
    ).order_by(
        desc(UserHistory.last_read_time)
    ).paginate(page=page, per_page=per_page)
    
    # Get novel and chapter details for each history record
    result = []
    for history in history_records.items:
        novel = Novel.query.get(history.novel_id)
        chapter = Chapter.query.get(history.chapter_id)
        
        if novel and chapter:
            record = {
                'novel': novel.to_dict(),
                'chapter': chapter.to_dict(),
                'last_read_time': history.last_read_time.isoformat()
            }
            result.append(record)
    
    return jsonify({
        'total': history_records.total,
        'pages': history_records.pages,
        'current_page': page,
        'history': result
    }), 200 