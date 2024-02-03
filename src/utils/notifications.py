from api.v1.app import socketio
from flask_socketio import emit
from models import Notification
from utils.logger import logger
from utils.helpers import is_uuid


def create_notification(user_id, message, link):
    """Create and emit a notification when a notification"""
    try:
        is_uuid(user_id)
        notification = Notification(user_id=user_id, message=message, link=link)
        notification.save()
        emit('new_notification', notification.to_dict())
    except ValueError as e:
        logger.exception(e)
        emit('new_notification', {'error': 'Invalid user ID'})
    except Exception as e:
        logger.exception(e)
        emit('new_notification', {'error': 'Something went wrong'})


def get_notifications(user_id):
    """Get all notifications for a user"""
    try:
        is_uuid(user_id)
        notifications = Notification.query.filter_by(user_id=user_id).all()
        emit('all_notifications', [n.to_dict() for n in notifications])
    except ValueError as e:
        logger.exception(e)
        emit('error', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('error', {'error': 'Something went wrong'}
             )


def mark_as_read(user_id, notification_id):
    """Mark a notification as read"""
    try:
        is_uuid(user_id)
        is_uuid(notification_id)
        notification = Notification.query.get(notification_id)
        if notification.user_id == user_id:
            notification.read = True
            notification.save()
            emit('read_notification', notification.to_dict(),
                )
    except ValueError as e:
        logger.exception(e)
        emit('read_notification', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('read_notification', {'error': 'Something went wrong'}
             )

        
def mark_all_as_read(user_id):
    """Mark all notifications as read"""
    try:
        is_uuid(user_id)
        notifications = Notification.query.filter_by(user_id=user_id).all()
        for notification in notifications:
            notification.read = True
            notification.save()
        emit('all_read', )
    except ValueError as e:
        logger.exception(e)
        emit('all_read', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('all_read', {'error': 'Something went wrong'}
             )


def delete_notification(user_id, notification_id):
    """Delete a notification"""
    try:
        is_uuid(user_id)
        is_uuid(notification_id)
        notification = Notification.query.get(notification_id)
        if notification.user_id == user_id:
            notification.delete()
            emit('delete_notification', notification_id,
                 )
    except ValueError as e:
        logger.exception(e)
        emit('delete_notification', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('delete_notification', {'error': 'Something went wrong'}
             )

    
def delete_all_notifications(user_id):
    """Delete all notifications"""
    try:
        is_uuid(user_id)
        notifications = Notification.query.filter_by(user_id=user_id).all()
        for notification in notifications:
            notification.delete()
        emit('all_deleted', )
    except ValueError as e:
        logger.exception(e)
        emit('all_deleted', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('all_deleted', {'error': 'Something went wrong'}
             )
        

def get_unread_count(user_id):
    """Get the number of unread notifications"""
    try:
        is_uuid(user_id)
        notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
        emit('unread_count', len(notifications), )
    except ValueError as e:
        logger.exception(e)
        emit('unread_count', {'error': 'Invalid user ID'}
             )
    except Exception as e:
        logger.exception(e)
        emit('unread_count', {'error': 'Something went wrong'}
             )
