from flask_socketio import Namespace, emit
from api.v1.app import socketio
from utils.logger import logger
from utils.notifications import (get_notifications, 
                                 mark_as_read, mark_all_as_read,
                                 delete_notification,
                                 delete_all_notifications,
                                 get_unread_count) 

class NotificationNameSpace(Namespace):
    """Define event handlers for notification namespace"""

    def on_connect(self):
        """Handle connection"""
        emit('connected', 'You are connected', namespace='/notifications')

    def on_disconnect(self):
        """Handle disconnection"""
        emit('disconnected', 'You are disconnected', namespace='/notifications')

    def on_get_notifications(self, data):
        """Handle get notifications"""
        try:
            user_id = data['user_id']
            get_notifications(user_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

    def on_mark_as_read(self, data):
        """Handle mark as read"""
        try:
            user_id = data['user_id']
            notification_id = data['notification_id']
            mark_as_read(user_id, notification_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

    def on_mark_all_as_read(self, data):
        """Handle mark all as read"""
        try:
            user_id = data['user_id']
            mark_all_as_read(user_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

    def on_delete_notification(self, data):
        """Handle delete notification"""
        try:
            user_id = data['user_id']
            notification_id = data['notification_id']
            delete_notification(user_id, notification_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

    def on_delete_all_notifications(self, data):
        """Handle delete all notifications"""
        try:
            user_id = data['user_id']
            delete_all_notifications(user_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

    def on_get_unread_count(self, data):
        """Handle get unread count"""
        try:
            user_id = data['user_id']
            get_unread_count(user_id)
        except Exception as e:
            logger.exception(e)
            emit('error', 'Invalid request', namespace='/notifications')

socketio.on_namespace(NotificationNameSpace('/notifications'))