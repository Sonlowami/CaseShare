import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from utils.decorators import token_required

class TestTokenRequiredDecorator(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    @patch('jwt.decode')
    def test_token_required_valid_token(self, mock_decode):
        mock_decode.return_value = {'email': 'test@example.com'}

        @self.app.route('/')
        @token_required
        def test_route(email):
            return 'Success', 200

        response = self.client.get('/', headers={'Authorization': 'Bearer valid_token'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Success')

    @patch('jwt.decode')
    def test_token_required_invalid_token(self, mock_decode):
        mock_decode.side_effect = Exception('Invalid token')

        @self.app.route('/')
        @token_required
        def test_route(email):
            return 'Success', 200

        response = self.client.get('/', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {'error': 'invalid or missing token'})

    def test_token_required_no_token(self):
        @self.app.route('/')
        @token_required
        def test_route(email):
            return 'Success', 200

        response = self.client.get('/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {'error': 'invalid or missing token'})

if __name__ == '__main__':
    unittest.main()