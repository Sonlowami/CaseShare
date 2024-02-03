from flask_socketio import Namespace, emit
from api.v1.app import socketio
from utils.logger import logger
from utils.notifications import (get_notifications, 
                                 mark_as_read, mark_all_as_read,
                                 delete_notification,
                                 delete_all_notifications,
                                 get_unread_count) 

@socketio.on('disconnect')
def disconnect():
    """Handle disconnection"""
    emit('disconnected', 'You are disconnected')


@socketio.on('get_notifications')
def get_user_notifications(data):
    """Handle get notifications"""
    try:
        user_id = data['user_id']
        get_notifications(user_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')

@socketio.on('mark_as_read')
def mark_as_read(data):
    """Handle mark as read"""
    try:
        user_id = data['user_id']
        notification_id = data['notification_id']
        mark_as_read(user_id, notification_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')


@socketio.on('mark_all_as_read')
def mark_all_as_read(data):
    """Handle mark all as read"""
    try:
        user_id = data['user_id']
        mark_all_as_read(user_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')


@socketio.on('delete_notification')
def delete_notification(data):
    """Handle delete notification"""
    try:
        user_id = data['user_id']
        notification_id = data['notification_id']
        delete_notification(user_id, notification_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')

@socketio.on('delete_all_notifications')
def delete_all_notifications(data):
    """Handle delete all notifications"""
    try:
        user_id = data['user_id']
        delete_all_notifications(user_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')


@socketio.on('get_unread_count')
def get_unread_count(data):
    """Handle get unread count"""
    try:
        user_id = data['user_id']
        get_unread_count(user_id)
    except Exception as e:
        logger.exception(e)
        emit('error', 'Invalid request')

@socketio.on('connect')
def connect(self):
    """Handle connection"""
    try:
        emit('connect', 'You are connected')
    except Exception as e:
        logger.exception(e)
