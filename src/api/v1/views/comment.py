#!/usr/bin/python3
"""This module implement API endpoints for accessing and manipulating comments"""
from datetime import datetime
from flask import jsonify, request
from api.v1.views import api_views
from models import Comment
from models import Post
from models import User
from utils.decorators import token_required
from utils.logger import logger

@api_views.get('/posts/<string:id>/comments', strict_slashes=False)
@token_required
def get_comments(email, id):
    """Get all comments related to a post"""
    try:
        post = Post.query.get(id)
        offset, limit = request.args.get('offset', 0), 20
        comments = post.comments[offset * limit:offset * limit + limit]
        response = jsonify([comment.to_dict() for comment in comments]), 200
        logger.info(f'{len(comments)} comments retrieved successfully')
        return response
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'unknown error occurred'}), 500
    
    
@api_views.get('/comments/<string:id>', strict_slashes=False)
@token_required
def get_comment(email, id):
    """Get a single comment and display it"""
    try:
        comment = Comment.query.get(id)
        result = jsonify(comment.to_dict()), 200
        logger.info(f'Comment {comment.id} retrieved successfully')
        return result
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'unknown error occurred'}), 500

@api_views.post('/posts/<string:post_id>/comments', strict_slashes=False)
@token_required
def post_comment(email, post_id):
    """Post a new comment to a post"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            logger.error('User did not provide a valid JSON')
            return jsonify({'error': 'not a JSON'}), 400
        post = Post.query.get(post_id)
        user_id = User.get_user_by_email(email).id
        content = data['content']
        if len(content) == 0:
            logger.error(f'Comment content on post {post.id} by user {user_id} cannot empty')
            return jsonify({'error': "empty request"}), 400
        new_comment = Comment(user_id=user_id, post_id=post.id, content=content)
        new_comment.save()
        logger.info(f'Comment {new_comment.id} created successfully')
        return jsonify(new_comment.to_dict()), 201
    except KeyError as e:
        logger.exception(e)
        return jsonify({'error': 'empty request'}), 400
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': "not found"}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'unknown error occurred'}), 500

@api_views.put('/comments/<string:id>', strict_slashes=False)
@token_required
def update_comment(email, id):
    """Update a comment"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            logger.error('User did not provide a valid JSON')
            return jsonify({'error': 'not a JSON'}), 400
        comment = Comment.query.get(id)
        user = User.get_user_by_email(email)
        if comment.user_id == user.id:
            content = data.get('content', comment.content)
            comment.content = content
            comment.updated_at = datetime.now()
            comment.save()
            logger.info(f'Comment {comment.id} updated successfully')
            return jsonify(comment.to_dict()), 200
        else:
            logger.error(f'User {user.id} does not own comment {comment.id}')
            return jsonify({'error': 'forbidden'}), 403
    except AttributeError as e:
        # The comment is not found
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        # The data passed is not a valid JSON, or other reason
        logger.exception(e)
        return jsonify({'error': 'unknown error occurred'}), 500
    
@api_views.delete('/comments/<string:id>')
@token_required
def delete_comment(email, id):
    """Delete a comment"""
    try:
        user = User.get_user_by_email(email)
        comment = Comment.query.get(id)
        if comment.user_id == user.id:
            comment.delete()
            logger.info(f'Comment {comment.id} deleted successfully')
            return jsonify({}), 204
        else:
            logger.error(f'User {user.id} not authorized to delete comment {comment.id}')
            return jsonify({'error': 'forbidden'}), 403
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'unknown error occurred'}), 500
