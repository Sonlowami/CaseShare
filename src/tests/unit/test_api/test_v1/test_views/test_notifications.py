import unittest
from unittest.mock import patch, MagicMock
from api.v1.app import socketio, app
from models import Notification
from uuid import uuid4 as uuid
class TestNotificationNamespace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = socketio.test_client(app, namespace='/notifications')
        cls.client.connect()

    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()

    def test_be_connected(self):
        """Test that the client is connected to the namespace"""
        self.assertTrue(self.client.is_connected())
        received = self.client.get_received()
        self.assertGreater(len(received), 0)
        self.assertEqual(received[0]['name'], 'connect')

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_get_notifications(self, mock_is_uuid, mock_query):
        """Test get notifications gets notificaions if everything is valid"""
        mock_is_uuid.return_value = True
        mock_query.filter_by.return_value.all.return_value = MagicMock(user_id=str(uuid()))
        data = {'user_id': 1}
        self.client.emit('get_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        response = received[0]
        self.assertEqual(response['name'], 'all_notifications')
        mock_is_uuid.assert_called_once_with(1)

    @patch('utils.notifications.is_uuid')
    def test_get_notifications_invalid_uuid(self, mock_is_uuid):
        """Test get notifications fail if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1}
        self.client.emit('get_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_get_notifications_internal_error(self, mock_is_uuid, mock_query):
        """Test get notifications fail if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.filter_by.side_effect = Exception('Internal error')
        data = {'user_id': 1}
        self.client.emit('get_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')

    def test_get_notifications_no_user_id_passed(self):
        """Test get notifications fail if no user_id passed"""
        data = {'username': 1}
        self.client.emit('get_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')

    @patch('models.Notification.query')
    @patch('models.Notification.save')
    @patch('utils.notifications.is_uuid')
    def test_mark_as_read(self, mock_is_uuid, mock_save, mock_query):
        """Test mark as read marks a notification as read"""
        user_id = str(uuid())
        notification_id = str(uuid())
        mock_is_uuid.return_value = True
        mock_query.get.return_value = MagicMock(user_id=user_id,
                                                notification_id=notification_id,
                                                read=False)
        result = mock_query.get.return_value
        result.to_dict.return_value = {'user_id': user_id,
                                       'notification_id': notification_id, 'read': True}
        mock_save.return_value = True
        data = {'user_id': user_id, 'notification_id': notification_id}
        self.client.emit('mark_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        mock_is_uuid.assert_called_with(notification_id)
        self.assertEqual(response['name'], 'read_notification')
        self.assertTrue(result.read)

    @patch('utils.notifications.is_uuid')
    def test_mark_as_read_invalid_uuid(self, mock_is_uuid):
        """Test mark as read fails if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1, 'notification_id': 1}
        self.client.emit('mark_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_mark_as_read_internal_error(self, mock_is_uuid, mock_query):
        """Test mark as read fails if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.get.side_effect = Exception('Internal error')
        data = {'user_id': 1, 'notification_id': 1}
        self.client.emit('mark_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'Something went wrong'})
    
    
    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_mark_as_read_unpermitted_user(self, mock_is_uuid, mock_query):
        """Test mark as read fail if user is not permitted"""
        mock_is_uuid.return_value = True
        user_id = str(uuid())
        notification_id = str(uuid())
        mock_query.get.return_value = MagicMock(user_id=str(uuid()))
        data = {'user_id': user_id, 'notification_id': notification_id}
        self.client.emit('mark_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})
    
    def test_mark_as_read_no_user_id_passed(self):
        """Test mark as read fails if no user_id passed"""
        data = {'username': 1}
        self.client.emit('mark_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid request'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_mark_all_as_read(self, mock_is_uuid, mock_query):
        """Test mark all as read marks all notifications as read"""
        user_id = str(uuid())
        mock_is_uuid.return_value = True
        mock_query.filter_by.return_value.all.return_value = [
            MagicMock(user_id=user_id, message='hi', read=False),
            MagicMock(user_id=user_id, message='hi', read=False)]
        result = mock_query.filter_by.return_value.all.return_value
        for item in result:
            item.to_dict.return_value = {'user_id': item.user_id, 'read': item.read}
        data = {'user_id': user_id}
        self.client.emit('mark_all_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'all_read')
        self.assertTrue(all(n.read for n in result))

    @patch('utils.notifications.is_uuid')
    def test_mark_all_as_read_invalid_uuid(self, mock_is_uuid):
        """Test mark all as read fails if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1}
        self.client.emit('mark_all_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})
    
    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_mark_all_as_read_internal_error(self, mock_is_uuid, mock_query):
        """Test mark all as read fails if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.filter_by.side_effect = Exception('Internal error')
        data = {'user_id': 1}
        self.client.emit('mark_all_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'Something went wrong'})

    def test_mark_all_as_read_no_user_id_passed(self):
        """Test mark all as read fails if no user_id passed"""
        data = {'username': 1}
        self.client.emit('mark_all_as_read', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid request'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_delete_notification(self, mock_is_uuid, mock_query):
        """Test delete notification deletes a notification"""
        user_id = str(uuid())
        notification_id = str(uuid())
        mock_is_uuid.return_value = True
        mock_query.get.return_value = MagicMock(user_id=user_id,
                                                notification_id=notification_id)
        data = {'user_id': user_id, 'notification_id': notification_id}
        self.client.emit('delete_notification', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'notification_deleted')
        self.assertEqual(response['args'][0], notification_id)

    @patch('utils.notifications.is_uuid')
    def test_delete_notification_invalid_uuid(self, mock_is_uuid):
        """Test delete notification fails if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1, 'notification_id': 1}
        self.client.emit('delete_notification', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_delete_notification_internal_error(self, mock_is_uuid, mock_query):
        """Test delete notification fails if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.get.side_effect = Exception('Internal error')
        data = {'user_id': 1, 'notification_id': 1}
        self.client.emit('delete_notification', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'Something went wrong'})


    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_delete_notification_unpermitted_user(self, mock_is_uuid, mock_query):
        """Test delete notification fails if user is not permitted"""
        mock_is_uuid.return_value = True
        user_id = str(uuid())
        notification_id = str(uuid())
        mock_query.get.return_value = MagicMock(user_id=str(uuid()))
        data = {'user_id': user_id, 'notification_id': notification_id}
        self.client.emit('delete_notification', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})

    def test_delete_notification_no_user_id_passed(self):
        """Test delete notification fails if no user_id passed"""
        data = {'username': 1}
        self.client.emit('delete_notification', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid request'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_delete_all_notifications(self, mock_is_uuid, mock_query):
        """Test delete all notifications deletes all notifications"""
        user_id = str(uuid())
        mock_is_uuid.return_value = True
        mock_query.filter_by.return_value.all.return_value = [
            MagicMock(user_id=user_id, message='hi'),
            MagicMock(user_id=user_id, message='hi')]
        data = {'user_id': user_id}
        self.client.emit('delete_all_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'all_deleted')

    @patch('utils.notifications.is_uuid')
    def test_delete_all_notifications_invalid_uuid(self, mock_is_uuid):
        """Test delete all notifications fails if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1}
        self.client.emit('delete_all_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_delete_all_notifications_internal_error(self, mock_is_uuid, mock_query):
        """Test delete all notifications fails if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.filter_by.side_effect = Exception('Internal error')
        data = {'user_id': 1}
        self.client.emit('delete_all_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'Something went wrong'})

    def test_delete_all_notifications_no_user_id_passed(self):
        """Test delete all notifications fails if no user_id passed"""
        data = {'username': 1}
        self.client.emit('delete_all_notifications', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid request'})

    @patch('utils.notifications.is_uuid')
    @patch('models.Notification.query')
    def test_get_unread_count(self, mock_query, mock_is_uuid):
        """Test get unread count gets the unread count"""
        user_id = str(uuid())
        mock_is_uuid.return_value = True
        mock_query.filter_by.return_value.all.return_value = [
            MagicMock(user_id=user_id, message='hi', read=False),
            MagicMock(user_id=user_id, message='hi', read=False)]
        result = mock_query.filter_by.return_value.all.return_value
        data = {'user_id': user_id}
        self.client.emit('get_unread_count', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'unread_count')
        self.assertEqual(response['args'][0], 2)

    @patch('utils.notifications.is_uuid')
    def test_get_unread_count_invalid_uuid(self, mock_is_uuid):
        """Test get unread count fails if no uuid passed"""
        mock_is_uuid.side_effect = ValueError('Invalid UUID')
        data = {'user_id': 1}
        self.client.emit('get_unread_count', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid user ID'})

    @patch('models.Notification.query')
    @patch('utils.notifications.is_uuid')
    def test_get_unread_count_internal_error(self, mock_is_uuid, mock_query):
        """Test get unread count fails if an internal error occurs"""
        mock_is_uuid.return_value = True
        mock_query.filter_by.side_effect = Exception('Internal error')
        data = {'user_id': 1}
        self.client.emit('get_unread_count', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'Something went wrong'})

    def test_get_unread_count_no_user_id_passed(self):
        """Test get unread count fails if no user_id passed"""
        data = {'username': 1}
        self.client.emit('get_unread_count', data)
        received = self.client.get_received()

        # Check that we received a response
        self.assertGreater(len(received), 0)

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'error')
        self.assertEqual(response['args'][0], {'error': 'invalid request'})


if __name__ == '__main__':
    unittest.main()
