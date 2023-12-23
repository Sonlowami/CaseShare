import unittest
from unittest.mock import patch, MagicMock
from api.v1.app import test_client

class TestLoginEndpoint(unittest.TestCase):


    def setUp(self):
        """Create a test client for testing requests"""
        self.client = test_client()

    @patch('models.User.get_user_by_email')
    @patch('api.v1.views.user_auth.check_password_hash')
    @patch('api.v1.views.user_auth.jwt.encode')
    @patch('api.v1.views.user_auth.make_response')
    @patch('api.v1.views.user_auth.jsonify')
    def test_successful_login(self, mock_jsonify, mock_make_response, mock_jwt_encode,
                              mock_check_password_hash, mock_get_user_by_email):
        """Test if a user can login successfully"""

        mock_get_user_by_email.return_value = MagicMock(password='hashed_password')
        mock_check_password_hash.return_value = True
        mock_jwt_encode.return_value = 'encoded_token'
        response = self.client.post('/api/v1/users/auth/login', json={
            'email': 'user@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        mock_jsonify.assert_called_once_with({'token': 'encoded_token', 'redirectUrl': '/api/v1/'})
        mock_make_response.assert_called_once_with(mock_jsonify.return_value, 200)

    @patch('api.v1.views.user_auth.jsonify')
    def test_invalid_input(self, mock_jsonify):
        """Test if the endpoint returns an error when email is not provided"""
        response = self.client.post('/api/v1/users/auth/login', json={
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'You must provide email and password'})

    @patch('api.v1.views.user_auth.jsonify')
    def test_invalid_input_password_missing(self, mock_jsonify):
        """Test if the endpoint returns an error when password is not provided"""
        response = self.client.post('/api/v1/users/auth/login', json={
            'email': 'abc@example.com'
        })
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'You must provide email and password'})

    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User')
    def test_wrong_email(self, mock_user, mock_jsonify):
        """Test if an error is raised if the user does not exist"""
        mock_user.get_user_by_email.return_value = None
        response = self.client.post('/api/v1/users/auth/login', json={
            'email': 'abc@example.com',
            'password': 'invalid'
        })
        self.assertEqual(response.status_code, 404)
        mock_jsonify.assert_called_once_with({'error': 'user doesnot exist'})

    
    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User.get_user_by_email')
    @patch('werkzeug.security.check_password_hash')
    def test_wrong_password(self, mock_hash, mock_get, mock_jsonify):
        """Test if an error is raised if the password does not exist"""
        mock_get.return_value = MagicMock(password='invalid')
        mock_hash.return_value = False
        response = self.client.post('/api/v1/users/auth/login', json={
            'email': 'abc@example.com',
            'password': 'invalid'
        })
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'invalid password'})

    @patch('api.v1.views.user_auth.jsonify')
    def test_invalid_json_data(self, mock_jsonify):
        """Test if an error code is returned if the data given is not json"""
        response = self.client.post('/api/v1/users/auth/login', json="whatever")
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'not a JSON'})
 
    @patch('api.v1.views.user_auth.jsonify')
    def test_register_invalid_json_data(self, mock_jsonify):
        """Test if register returns error code if invalid json"""
        response = self.client.post('/api/v1/users/auth/register', json="whatever")
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'not a JSON'})

    @patch('models.User.save')
    @patch('api.v1.views.user_auth.jsonify')
    def test_register_success(self, mock_jsonify, mock_save):
        """Test if register registers a new user when all the data is given"""
        mock_save.return_value = True
        response = self.client.post('/api/v1/users/auth/register', json={
            'email': 'abc@example.com',
            'password': 'I love',
            'first_name': 'John',
            'last_name': 'Doe',
            'country': 'Rwanda',
            'gender': 'male',
            'title': 'Eavesdropper at XYZ',
            'phone': '744632913'
        })
        self.assertEqual(response.status_code, 201)
        mock_save.assert_called_once()
        mock_jsonify.assert_called_once_with({'email': 'abc@example.com'})

    
    @patch('api.v1.views.user_auth.jsonify')
    def test_register_failure_missing_data(self, mock_jsonify):
        """Test if register returns an error code when some data is not provided, like the last name"""
        response = self.client.post('/api/v1/users/auth/register', json={
            'email': 'abc@example.com',
            'password': 'I love',
            'first_name': 'John',
            'country': 'Rwanda',
            'gender': 'male',
            'title': 'Eavesdropper at XYZ',
            'phone': '744632913'
        })
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'missing some data'})

    
    @patch('api.v1.views.user_auth.jsonify')
    def test_forgot_password_invalid_json_data(self, mock_jsonify):
        """Test if register returns error code if invalid json"""
        response = self.client.post('/api/v1/users/auth/forgot_password', json="whatever")
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'not a JSON'})

    
    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User')
    def test_forgot_with_wrong_email(self, mock_user, mock_jsonify):
        """Test if forgot password return error code if the user does not exist"""
        mock_user.get_user_by_email.return_value = None
        response = self.client.post('/api/v1/users/auth/forgot_password', json={
            'email': 'abc@example.com',
        })
        self.assertEqual(response.status_code, 404)
        mock_jsonify.assert_called_once_with({'error': 'user doesnot exist'})
    
    @patch('api.v1.views.user_auth.jwt.encode')
    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User.get_user_by_email')
    def test_forgot_password_with_valid_data(self, mock_get, mock_jsonify, mock_encode):
        mock_get.return_value = MagicMock(email='abc@example.com')
        mock_encode.return_value = "some string"

        response = self.client.post('/api/v1/users/auth/forgot_password', json={
            'email': 'abc@example.com'
        })
        self.assertEqual(response.status_code, 200)
        mock_jsonify.assert_called_once()
        mock_encode.assert_called_once()

    @patch('api.v1.views.user_auth.jwt.decode')
    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User.get_user_by_email')
    def test_reset_password_with_valid_data(self, mock_get, mock_jsonify, mock_decode):
        """Test if reset password works as intended if all right data is provided"""
        mock_decode.return_value = { 'email': 'abc@example.com'}
        mock_get.return_value = MagicMock(email='abc@example.com')
        mock_save = mock_get.return_value.save

        response = self.client.post('/api/v1/users/auth/reset_password/some-token', json={
            'new_password': 'randomint'
        })

        self.assertEqual(response.status_code, 200)
        mock_jsonify.assert_called_once_with({'message': "Password reset successfully"})
        mock_decode.assert_called_once()
        mock_save.assert_called_once()

    
    @patch('api.v1.views.user_auth.jwt.decode')
    @patch('api.v1.views.user_auth.jsonify')
    @patch('models.User.get_user_by_email')
    @patch('models.User.save')
    def test_reset_password_with_inexistent_user(self, mock_save, mock_get, mock_jsonify, mock_decode):
        """Test if reset password works as intended if all right data is provided"""
        mock_decode.return_value = { 'email': 'abc@example.com'}
        mock_get.return_value = None
        mock_save.return_value = True

        response = self.client.post('/api/v1/users/auth/reset_password/some-token', json={
            'new_password': 'randomint'
        })

        self.assertEqual(response.status_code, 404)
        mock_jsonify.assert_called_once_with({'error': "user doesnot exist"})
        mock_decode.assert_called_once()

    
    @patch('api.v1.views.user_auth.jsonify')
    def test_reset_password_invalid_json_data(self, mock_jsonify):
        """Test if an error code is returned if the data given is not json"""
        response = self.client.post('/api/v1/users/auth/reset_password/some-token', json="whatever")
        self.assertEqual(response.status_code, 400)
        mock_jsonify.assert_called_once_with({'error': 'not a JSON'})

if __name__ == '__main__':
    unittest.main()
