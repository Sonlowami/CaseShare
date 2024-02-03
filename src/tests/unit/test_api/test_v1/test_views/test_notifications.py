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

        # Check that the response has the expected data
        response = received[0]
        self.assertEqual(response['name'], 'connect')
        response = received[1]
        self.assertEqual(response['name'], 'all_notifications')

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

if __name__ == '__main__':
    unittest.main()
