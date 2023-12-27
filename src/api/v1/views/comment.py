#!/usr/bin/python3
"""This module implement API endpoints for accessing and manipulating comments"""
from datetime import datetime
from flask import jsonify, request
from api.v1.views import api_views
from models import Comment
from models import Post
from models import User
from utils.decorators import token_required

@api_views.get('/posts/<string:id>/comments', strict_slashes=False)
@token_required
def get_comments(email, id):
    """Get all comments related to a post"""
    try:
        post = Post.query.get(id)
        offset, limit = request.args.get('offset', 0), 20
        comments = post.comments[offset * limit:offset * limit + limit]
        return jsonify([comment.to_dict() for comment in comments]), 200
    except AttributeError:
        return jsonify({'error': 'not found'}), 404
    except Exception:
        return jsonify({'error': 'unknown error occurred'}), 500
    
    
@api_views.get('/comments/<string:id>', strict_slashes=False)
@token_required
def get_comment(email, id):
    """Get a single comment and display it"""
    try:
        comment = Comment.query.get(id)
        return jsonify(comment.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'not found'}), 404
    except Exception:
        return jsonify({'error': 'unknown error occurred'}), 500

@api_views.post('/posts/<string:post_id>/comments', strict_slashes=False)
@token_required
def post_comment(email, post_id):
    """Post a new comment to a post"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'not a JSON'}), 400
        post = Post.query.get(post_id)
        user_id = User.get_user_by_email(email).id
        content = data['content']
        if len(content) == 0:
            return jsonify({'error': "empty request"}), 400
        new_comment = Comment(user_id=user_id, post_id=post.id, content=content)
        new_comment.save()
        return jsonify(new_comment.to_dict()), 201
    except KeyError:
        return jsonify({'error': 'empty request'}), 400
    except AttributeError:
        return jsonify({'error': "not found"}), 404
    except Exception:
        return jsonify({'error': 'unknown error occurred'}), 500

@api_views.put('/comments/<string:id>', strict_slashes=False)
@token_required
def update_comment(email, id):
    """Update a comment"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'not a JSON'}), 400
        comment = Comment.query.get(id)
        user = User.get_user_by_email(email)
        if comment.user_id == user.id:
            content = data.get('content', comment.content)
            comment.content = content
            comment.updated_at = datetime.now()
            comment.save()
            return jsonify(comment.to_dict()), 200
        else:
            # The user is not found, or not own the comment
            return jsonify({'error': 'forbidden'}), 403
    except AttributeError:
        # The comment is not found
        return jsonify({'error': 'not found'}), 404
    except Exception:
        # The data passed is not a valid JSON, or other reason
        return jsonify({'error': 'unknown error occurred'}), 500
    
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