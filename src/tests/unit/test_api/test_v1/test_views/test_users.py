import unittest
from unittest.mock import patch, MagicMock
from api.v1.app import test_client, app

class TestUserEndpoints(unittest.TestCase):
    """Contain tests for user endpoints"""

    def setUp(self) -> None:
        """Initialize a test client"""
        self.client = test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    @patch('utils.decorators.jwt.decode')
    @patch('models.user.User.query')
    def test_get_users(self, mock_query, mock_jwt):
        """Test that a user can get all users paginated and offset to page 0"""
        mock_jwt.return_value = {'email': 'abc@example.com'}
        mock_query.offset.return_value = MagicMock()
        mock_limit = mock_query.offset.return_value.limit
        mock_limit.return_value = MagicMock()
        mock_all = mock_limit.return_value.all
        mock_all.return_value = MagicMock()

        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        mock_query.offset.assert_called_once_with(0)
        mock_limit.assert_called_once_with(20)
        mock_all.assert_called_once()

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('api.v1.views.users.jsonify')
    def test_get_myself_success(self, mock_jsonify, mock_jwt_decode, mock_get_user_by_email):
        """Test that a user can get themselves"""
        mock_jwt_decode.return_value = {'email': 'test@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='test@example.com')

        response = self.client.get('/api/v1/users/me')
        self.assertEqual(response.status_code, 200)
        mock_get_user_by_email.assert_called_once_with('test@example.com')
        mock_jsonify.assert_called_once()

    @patch('models.User.query')
    @patch('utils.decorators.jwt.decode')
    @patch('api.v1.views.users.jsonify')
    def test_get_user_success(self, mock_jsonify, mock_jwt_decode, mock_query):
        """Test that a user can get be gotten from their id"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_query.get.return_value = MagicMock(id='6607')

        response = self.client.get('/api/v1/users/6607')
        self.assertEqual(response.status_code, 200)
        mock_query.get.assert_called_once_with('6607')
        mock_jsonify.assert_called_once()

    
    @patch('models.User.query')
    @patch('utils.decorators.jwt.decode')
    @patch('api.v1.views.users.jsonify')
    def test_get_user_failure_user_not_found(self, mock_jsonify, mock_jwt_decode, mock_query):
        """Test that getting a user by id fails if the id doesn't exist"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_query.get.return_value = None

        response = self.client.get('/api/v1/users/6607')
        self.assertEqual(response.status_code, 404)
        mock_query.get.assert_called_once_with('6607')
        mock_jsonify.assert_called_once()

    @patch('api.v1.views.users.jsonify')
    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_update_myself_success(self, mock_jwt_decode, mock_get_user_by_email, mock_jsonify):
        """Test that a user can update their information"""
        mock_jwt_decode.return_value = {'email': 'test@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='test@example.com')
        new_data = {'title': 'Programmer', 'first_name': 'John', 'last_name': 'Daniel', 'country': 'Kenya'}
        mock_get_user_by_email.return_value.to_dict.return_value = new_data
        mock_save = mock_get_user_by_email.return_value.save
        
        response = self.client.put('/api/v1/users/me', json=new_data)
        self.assertEqual(response.status_code, 200)
        mock_get_user_by_email.assert_called_once_with('test@example.com')
        mock_jsonify.assert_called_once()
        mock_save.assert_called_once()

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_update_myself_failure(self, mock_jwt_decode, mock_get_user_by_email):
        """Test that update fails when non-json data is passed"""
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='abc@example.com')
        new_data = {'title': 'Programmer', 'first_name': 'John', 'last_name': 'Daniel', 'country': 'Kenya',}
        response = self.client.put('/api/v1/users/me', data=new_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'not a JSON')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('api.v1.views.users.generate_password_hash')
    def test_change_password_success(self, mock_hash, mock_get_user_by_email, mock_jwt_decode):
        """Test that the change password feature works well when all data is supplied"""
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='abc@example.com', password='123456')
        mock_hash.return_value = '123456'
        response = self.client.put('/api/v1/users/me/change_password', json={
            'old_password': '123456', 'new_password': 'Test123456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})


    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('api.v1.views.users.generate_password_hash')
    def test_update_myself_failure_wrong_old_pwd(self, mock_hash, mock_get_user_by_email, mock_jwt_decode):
        """Test that the change password feature will not work if the old password is wrong"""
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='abc@example.com', password='123456')
        mock_hash.return_value = '12356'
        response = self.client.put('/api/v1/users/me/change_password', json={
            'old_password': '123456', 'new_password': 'Test123456'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'invalid password'})

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('api.v1.views.users.generate_password_hash')
    def test_update_myself_failure_not_json(self, mock_hash, mock_get_user_by_email, mock_jwt_decode):
        """Test that the change password feature will not work if data passed not json"""
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        mock_get_user_by_email.return_value = MagicMock(email='abc@example.com', password='123456')
        mock_hash.return_value = '123456'
        response = self.client.put('/api/v1/users/me/change_password', json='whatever')
        mock_hash.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'not a JSON'})

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    def test_delete_user_success(self, mock_get_user_by_email, mock_jwt_decode):
        """Test that a user can delete their account"""
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        mock_get_user_by_email.return_value = MagicMock(email='abc@example.com')
        mock_get_user_by_email.return_value.delete.return_value = True
        response = self.client.delete('/api/v1/users/me')
        self.assertEqual(response.status_code, 204)
        mock_get_user_by_email.assert_called_once_with('abc@example.net')