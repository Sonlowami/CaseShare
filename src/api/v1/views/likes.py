#!/usr/bin/python3
"""Create APIs for likes"""
from flask import jsonify, request
from api.v1.views import app_views
from api.v1.views.decorators import token_required
from models.user import User
from models.like import Like
from models.post import Post

@app_views.get('/posts/<string:post_id>/likes', strict_slashes=False)
@token_required
def get_likes(email, post_id):
    """Get the number of all likes"""
    likes = Post.get(Post, post_id).likes
    try:
        return jsonify([like.to_dict() for like in likes]), 200
    except AttributeError:
        return jsonify({}), 204
    

@app_views.post('/posts/<string:post_id>/likes', strict_slashes=False)
@token_required
def create_like(email, post_id):
    """Create a new like for an object"""
    user_id = Post.get_user_by_email(email).id
    new_like = Like(user_id=user_id, post_id=post_id)
    new_like.save()
    likes = Post.get(Post, post_id).likes
    return jsonify([like.to_dict() for like in likes]), 201
