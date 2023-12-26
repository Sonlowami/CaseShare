#!/usr/bin/python3
"""This module implement API endpoints for accessing and manipulating comments"""
from datetime import datetime
from flask import jsonify, request
from api.v1.views import api_views
from models.comment import Comment
from models.post import Post
from models.user import User
from utils.decorators import token_required

@api_views.get('/posts/<string:id>/comments', strict_slashes=False)
def get_comments(id):
    """Get all comments related to a post"""
    post = Post.get(Post, id)
    try:
        comments = post.comments
        return jsonify([comment.to_dict() for comment in comments]), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    
@api_views.get('/comments/<string:id>', strict_slashes=False)
def get_comment(id):
    """Get a single comment and display it"""
    comment = Comment.get(Comment, id)
    try:
        return jsonify(comment.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404

@api_views.post('/posts/<string:post_id>/comments', strict_slashes=False)
@token_required
def post_comment(email, post_id):
    """Post a new comment to a post"""
    try:
        data = request.get_json()
        user_id = User.get_user_by_email(email).id
        content = data['content']
        if len(content) == 0:
            return jsonify({'error': "Can't save empty content"}), 400
        new_comment = Comment(user_id=user_id, post_id=post_id, content=content)
        new_comment.save()
        return jsonify(new_comment.to_dict()), 201
    except AttributeError:
        return jsonify({'error': "Request data missing 'content' attribute"}), 400
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.put('/comments/<string:id>', strict_slashes=False)
@token_required
def update_comment(email, id):
    """Update a comment"""
    try:
        data = request.get_json()
        comment = Comment.get(Comment, id)
        user = User.get_user_by_email(email)
        if comment.user_id == user.id:
            content = data['content']
            comment.content = content
            comment.updated_at = datetime.now()
            comment.save()
            return jsonify(comment.to_dict()), 200
        else:
            # The user is not found, or not own the comment
            return jsonify({'error': 'Forbidden'}), 403
    except AttributeError:
        # The comment is not found
        return jsonify({'error': 'Not Found'}), 404
    except KeyError:
        # data object does not contain key 'content'
        return jsonify({'error': 'request data must have key: content'}), 400
    except Exception:
        # The data passed is not a valid JSON, or other reason
        return jsonify({'error': 'Not a JSON'}), 400
    
@api_views.delete('/comments/<string:id>')
@token_required
def delete_comment(email, id):
    """Delete a comment"""
    try:
        user = User.get_user_by_email(email)
        comment = Comment.get(Comment, id)
        if comment.user_id == user.id:
            Comment.delete(comment)
            Comment.save()
            return jsonify({}), 204
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404