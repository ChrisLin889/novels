# 修复 deactivate_account 方法，正确获取用户角色

@staticmethod
def deactivate_account(user_id: int, password: str) -> Dict:
    """
    Deactivate a user account. This will completely delete the user record.
    
    Args:
        user_id: User ID
        password: Password for verification
        
    Returns:
        Dict with success status and message
    """
    user = User.query.get(user_id)
    if not user:
        return {
            'success': False,
            'error': 'User not found'
        }
    
    # Verify password
    if not user.check_password(password):
        return {
            'success': False,
            'error': 'Password is incorrect'
        }
    
    # 正确获取用户角色，使用 PermissionService 而不是直接访问 user.role
    from app.services.permission_service import PermissionService
    user_role = PermissionService.get_user_role(user.id)
    
    # Check if user is an admin (cannot deactivate admin accounts through this method)
    if user_role == 'admin':
        return {
            'success': False,
            'error': 'Admin accounts cannot be deactivated through this method'
        }
        
    # Check if user is an author
    if user_role == 'author':
        # 注意：如果只想注销作者身份但保留用户账户，应使用作者模块的 /api/author/resign API
        # 这里的操作会完全删除用户账户
        author = Author.query.filter_by(user_id=user_id).first()
        if author:
            # Clear author relationship but keep the novels
            db.session.delete(author)
    
    # Delete user interactions (collections, history, following)
    UserCollection.query.filter_by(user_id=user_id).delete()
    UserHistory.query.filter_by(user_id=user_id).delete()
    UserFollowing.query.filter_by(follower_id=user_id).delete()
    UserFollowing.query.filter_by(author_id=user_id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Account successfully deactivated'
    } 