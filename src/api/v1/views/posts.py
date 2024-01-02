#!/usr/bin/python3
"""Define endpoints to access posts"""
from datetime import datetime
from utils.decorators import token_required
from json import JSONDecodeError
from flask import jsonify, request
from api.v1.views import api_views
from models import User
from models import Post
from utils.logger import logger

@api_views.get('/posts', strict_slashes=False)
@token_required
def get_posts(email):
    """Get all posts in the database."""
    try:
        limit, offset = 20, int(request.args.get('offset', 0))
        posts = Post.query.offset(offset).limit(limit).all()
        response = jsonify([post.to_dict() for post in posts]), 200
        logger.info(f'{len(posts)} posts retrieved successfully')
        return response
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404

@api_views.get('/posts/<string:id>', strict_slashes=False)
@token_required
def get_post(email, id):
    try:
        post = Post.query.get(id)
        result = jsonify(post.to_dict()), 200
        logger.info(f'Post {post.id} retrieved successfully')
        return result
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404

@api_views.get('/users/<string:id>/posts', strict_slashes=False)
@token_required
def get_posts_by_user(email, id):
    try:
        user = User.query.get(id)
        offset = request.args.get('offset', 0)
        limit = 20
        posts = user.posts[offset * limit: offset * limit + limit]
        response = jsonify([post.to_dict() for post in posts]), 200
        logger.info(f'{len(posts)} posts retrieved successfully')
        return response
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404

@api_views.post('/posts', strict_slashes=False)
@token_required
def post_something(email):
    try:
        user_id = User.get_user_by_email(email).id
        data = request.get_json()
        title = data['title']
        content = data['content']
        post = Post(title=title, content=content, user_id=user_id)
        post.save()
        logger.info(f'Post {post.id} created successfully')
        return jsonify(post.to_dict()), 201
    except KeyError as e:
        logger.exception(e)
        return jsonify({'error': 'Title/Content must be provided'}), 400
    except AttributeError as e:
        logger.exception(e)
        return jsonify({"error": "not Found"}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'not a JSON'}), 400

@api_views.put('/posts/<string:id>', strict_slashes=False)
@token_required
def edit_post(email, id):
    """Edit the published content"""
    try:
        user = User.get_user_by_email(email)
        data = request.get_json()
        post = Post.query.get(id)
        title = data.get('title', post.title)
        content = data.get('content', post.content)
        if post.user_id == user.id:
            post.title = title
            post.updated_at = datetime.now()
            post.content = content
            post.save()
            logger.info(f'Post {post.id} updated successfully')
            return jsonify(post.to_dict())
        else:
            logger.error(f'User {user.id} not allowed to edit post {post.id}')
            return jsonify({'error': 'forbidden'}), 403
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'Not Found'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'not a JSON'}), 400

@api_views.delete('/posts/<string:id>', strict_slashes=False)
@token_required
def delete_post(email, id):
    try:
        user = User.get_user_by_email(email)
        post = Post.query.get(id)
        if post.user_id == user.id:
            post.delete()
            logger.info(f'Post {post.id} deleted successfully')
            return jsonify({}), 204
        else:
            logger.error(f'User {user.id} not allowed to delete post {post.id}')
            return jsonify({'error': 'forbidden'}), 403
    except AttributeError as e:
        logger.exception(e)
        return jsonify({'error': 'not found'}), 404