import unittest
from unittest import mock
from models.base_model import BaseModel
from models import Post
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

        self.base_model = BaseModel()
        self.post = Post()
        self.fake = Faker()

    def tearDown(self):
        self.app_context.pop()

    def test_init_with_no_kwargs(self):
        """Test if the model is initialized without passing keyword arguments"""
        self.assertIn('id', self.base_model.__dict__)
        
    def test_init_with_kwargs(self):
        """Test if a BaseModel object is initialized when passed kwargs"""
        self.base_model = BaseModel(name="France", sex='malish')

        self.assertIn('name', self.base_model.__dict__)
        self.assertIn('sex', self.base_model.__dict__)
        self.assertEqual(self.base_model.name, 'France')
        self.assertEqual(self.base_model.sex, "malish")

    def test_repr(self):
        """
        Test if a BaseModel instance is represented in the below format:
        Class: <Id>
        """
        self.assertRegex(str(self.base_model), '([A-Z])\w+ <[a-z0-9-]+>')

    def test_to_dict(self):
        """
        Test if BaseModel.to_dict return a dictionary of values, _sa_instance_state excluded.
        Because BaseModel class is not mapped, we use Post class to test this functionality. 
        """
        dct = self.post.to_dict()
        self.assertIsInstance(dct, dict)
        self.assertIn('id', dct)
        self.assertIn('create_at', dct)
        self.assertIn('update_at', dct)

    @mock.patch('utils.database.db.session')
    def test_save_success(self, mock_session):
        # Mock the necessary dependencies
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        # Call the save() function
        result = self.base_model.save()

        # Assert that the necessary methods were called
        mock_session.add.assert_called_once_with(self.base_model)
        mock_session.commit.assert_called_once()

        # Assert the result
        self.assertTrue(result)

    @mock.patch('utils.database.db.session')
    def test_save_failure(self, mock_session):
        # Mock the necessary dependencies
        mock_session.add.return_value = None
        mock_session.commit.side_effect = Exception('code failed')

        # Call the save() function
        result = self.base_model.save()

        # Assert that the necessary methods were called
        mock_session.add.assert_called_once_with(self.base_model)
        mock_session.commit.assert_called_once()

        # Assert the result
        self.assertFalse(result)

    @mock.patch('utils.database.db.session')
    def test_update_object(self, mock_session):
        """Test if the update functionality updates the object if column exists"""
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        old_times = self.post.update_at
        result = self.post.update(title='New title')

        # Assert that the necessary methods were called
        self.assertTrue(result)
        mock_session.add.assert_called_once_with(self.post)
        mock_session.commit.assert_called_once()
        self.assertNotEqual(self.post.update_at, old_times)
        self.assertEqual(self.post.title, 'New title')

    @mock.patch('utils.database.db.session')
    def test_update_rejects_new_attribute(self, mock_session):
        """Test if update function rejects an attribute that does not have a matching column"""
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        old_times = self.post.update_at
        result = self.post.update(name="Impossible")

        self.assertTrue(result)
        self.assertEqual(self.post.update_at, old_times)
        mock_session.add.assert_called_once_with(self.post)
        mock_session.commit.assert_called_once()

    
    @mock.patch('utils.database.db.session')
    def test_update_fails(self, mock_session):
        """Test if update function rejects an attribute that does not have a matching column"""
        mock_session.add.return_value = None
        mock_session.commit.side_effect = Exception()

        result = self.post.update()

        self.assertFalse(result)
        mock_session.add.assert_called_once_with(self.post)
        mock_session.commit.assert_called_once()

    @mock.patch('utils.database.db.session')
    def test_delete_success(self, mock_session):
        # Mock the necessary dependencies
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        # Call the delete() function
        result = self.base_model.delete()

        # Assert that the necessary methods were called
        mock_session.delete.assert_called_once_with(self.base_model)
        mock_session.commit.assert_called_once()

        # Assert the result
        self.assertTrue(result)

    @mock.patch('utils.database.db.session')
    def test_delete_failure(self, mock_session):
        # Mock the necessary dependencies
        mock_session.delete.return_value = None
        mock_session.commit.side_effect = Exception('test')

        # Call the delete() function
        result = self.base_model.delete()

        # Assert that the necessary methods were called
        mock_session.delete.assert_called_once_with(self.base_model)
        mock_session.commit.assert_called_once()

        # Assert the result
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main()