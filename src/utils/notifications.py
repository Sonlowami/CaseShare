from api.v1.app import socketio
from flask_socketio import emit
from models import Notification


def create_notification(user_id, message, link):
    """Create and emit a notification when a notification"""
    notification = Notification(user_id=user_id, message=message, link=link)
    notification.save()

    emit('new_notification', notification.to_dict(),
                  namespace='/notifications', room=user_id)


def get_notifications(user_id):
    """Get all notifications for a user"""
    notifications = Notification.query.filter_by(user_id=user_id).all()
    emit('all_notifications', [n.to_dict() for n in notifications],
                  namespace='/notifications', room=user_id)
    
def mark_as_read(user_id, notification_id):
    """Mark a notification as read"""
    notification = Notification.query.get(notification_id)
    if notification.user_id == user_id:
        notification.read = True
        notification.save()
        emit('read_notification', notification.to_dict(),
             namespace='/notifications', room=user_id)
        
def mark_all_as_read(user_id):
    """Mark all notifications as read"""
    notifications = Notification.query.filter_by(user_id=user_id).all()
    for notification in notifications:
        notification.read = True
        notification.save()
    emit('all_read', namespace='/notifications', room=user_id)

def delete_notification(user_id, notification_id):
    """Delete a notification"""
    notification = Notification.query.get(notification_id)
    if notification.user_id == user_id:
        notification.delete()
        emit('delete_notification', notification_id,
             namespace='/notifications', room=user_id)
        
def delete_all_notifications(user_id):
    """Delete all notifications"""
    notifications = Notification.query.filter_by(user_id=user_id).all()
    for notification in notifications:
        notification.delete()
    emit('all_deleted', namespace='/notifications', room=user_id)

def get_unread_count(user_id):
    """Get the number of unread notifications"""
    notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
    emit('unread_count', len(notifications), namespace='/notifications', room=user_id)