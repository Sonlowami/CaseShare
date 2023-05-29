#!/usr/bin/python3
"""Define endpoints to access posts"""
from datetime import datetime
from api.v1.views.decorators import token_required
from json import JSONDecodeError
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.user import User
from models.post import Post
from models import storage

@api_views.get('/posts', strict_slashes=False)
def get_posts():
    """Get all posts in the database."""
    posts =  storage.all(Post)
    try:
        return jsonify([post.to_dict() for post in posts]), 200
    except AttributeError:
        pass

@api_views.get('/posts/<string:id>', strict_slashes=False)
def get_post(id):
    post = storage.get(Post, id)
    try:
        return jsonify(post.to_dict()), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404

@api_views.get('/users/<string:email>/posts', strict_slashes=False)
@token_required
def get_posts_by_user(email):
    user = storage.get(User, email)
    try:
        posts = user.posts
        return jsonify([post.to_dict() for post in posts]), 200
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404

@api_views.post('/posts', strict_slashes=False)
@token_required
def post_something(email):
    try:
        user_id = storage.get_user_by_email(email).id
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        post = Post(title=title, content=content, user_id=user_id)
        post.save()
        return jsonify(post.to_dict()), 201
    except KeyError:
        return jsonify({'error': 'Title/Content cannot be null'}), 400
    except AttributeError:
        return jsonify({"error": "Not Found"}), 404
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.put('/posts/<string:id>', strict_slashes=False)
@token_required
def edit_post(email, id):
    """Edit the published content"""
    try:
        user = storage.get_user_by_email(email)
        data = request.get_json()
        post = storage.get(Post, id)
        title = data.get('title')
        content = data.get('content')
        if post.user == user:
            post.title = title
            post.updated_at = datetime.now()
            post.content = content
            post.save()
            return jsonify(post.to_dict())
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404
    except JSONDecodeError:
        return jsonify({'error': 'Not a JSON'}), 400

@api_views.delete('/posts/<string:id>', strict_slashes=False)
@token_required
def delete_post(email, id):
    user = storage.get(User, email)
    post = storage.get(Post, id)
    try:
        if post.user == user:
            post.delete()
            return jsonify({}), 204
    except AttributeError:
        return jsonify({'error': 'Not Found'}), 404