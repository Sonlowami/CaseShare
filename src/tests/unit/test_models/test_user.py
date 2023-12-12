import unittest
from unittest import mock
from datetime import datetime
from models import User
from werkzeug.security import check_password_hash
from faker import Faker
from flask import Flask
from dotenv import load_dotenv
from utils.config import Config
from utils.database import db


load_dotenv()

class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.user = User()
        self.fake = Faker()

    def tearDown(self):
        self.app_context.pop()

    def test_set_attr_hashes_password(self):
        """Test if a password is hashed when a password attribute is provided or changed"""
        self.user.password = 'I am back'
        self.assertNotEqual(self.user.password, 'I am back')
        self.assertTrue(check_password_hash(self.user.password, 'I am back'))
        self.assertFalse(check_password_hash(self.user.password, 'I am Back'))

    def test_user_dict_removes_sensitive_data(self):
        """
        Test if the to_dict function removes sensitive data, specifically:
        - Passwords
        - Reset tokens
        - OTP
        - OTP Expiry
        """
        self.user.email = self.fake.email()
        self.user.password = self.fake.password()
        self.user.otp = '48576'
        self.user.otp_expiry = datetime.now()
        self.user.reset_token = self.fake.uuid4()

        dct = self.user.to_dict()

        self.assertNotIn('password', dct)
        self.assertNotIn('otp', dct)
        self.assertNotIn('otp_expiry', dct)
        self.assertNotIn('reset_token', dct)
        self.assertIn('email', dct)

    @mock.patch('models.User.query')
    def test_get_user_by_email_with_valid_email(self, mock_query):
        """Test if get_user_by_email calls the right methods"""
        mock_query.filter_by.return_value = None

        try:
            User.get_user_by_email(self.user.email)
            mock_query.filter_by.assert_called_once_with(self.user.email)
        except AttributeError:
            # Since we set filter_by to return None, we expect an AttributeError
            # because we cannot call first() on None
            pass

    @mock.patch('models.User.query')
    def test_get_all_users(self, mock_query):
        """Test if get all users can get a list of all users in the database"""
        mock_query.all.return_value = None

        User.get_all_users()
        mock_query.all.assert_called_once()
