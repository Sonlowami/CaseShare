import unittest
from unittest.mock import patch, MagicMock
from api.v1.app import test_client, app

class TestPostEndpoints(unittest.TestCase):
    """Contain tests for post endpoints"""

    def setUp(self) -> None:
        """Initialize a test client"""
        self.client = test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_get_posts(self, mock_query, mock_jwt):
        """Test that a post can get all posts paginated and
        offset to page 0 by default"""
        mock_jwt.return_value = {'email': 'abc@example.com'}
        mock_query.offset.return_value = MagicMock()
        mock_limit = mock_query.offset.return_value.limit
        mock_limit.return_value = MagicMock()
        mock_all = mock_limit.return_value.all
        result = MagicMock()
        result.to_dict.return_value = {'id': 'ax2736'}
        mock_all.return_value = [result]

        response = self.client.get('/api/v1/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'id': 'ax2736'}])
        mock_query.offset.assert_called_once_with(0)
        mock_limit.assert_called_once_with(20)
        mock_all.assert_called_once()

    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_get_posts_nothing_there(self, mock_query, mock_jwt):
        """Test that get posts returns an empty list when there are no posts"""
        mock_jwt.return_value = {'email': 'abc@example.com'}
        mock_query.offset.return_value = MagicMock()
        mock_limit = mock_query.offset.return_value.limit
        mock_limit.return_value = MagicMock()
        mock_all = mock_limit.return_value.all
        mock_all.return_value = []

        response = self.client.get('/api/v1/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
        mock_query.offset.assert_called_once_with(0)
        mock_limit.assert_called_once_with(20)
        mock_all.assert_called_once()

    
    @patch('models.Post.query')
    @patch('utils.decorators.jwt.decode')
    @patch('api.v1.views.posts.jsonify')
    def test_get_post_success(self, mock_jsonify,
                              mock_jwt_decode, mock_query):
        """Test that a post can get be gotten from their id"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_query.get.return_value = MagicMock(id='6607')
        mock_query.get.return_value.to_dict.return_value = {'id': '6607'}

        response = self.client.get('/api/v1/posts/6607')
        self.assertEqual(response.status_code, 200)
        mock_query.get.assert_called_once_with('6607')
        mock_jsonify.assert_called_once()

    @patch('models.Post.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_post_not_found(self,
                              mock_jwt_decode, mock_query):
        """Test that no post can be gotten if the id doesn't exist"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_query.get.return_value = None

        response = self.client.get('/api/v1/posts/6607')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_query.get.assert_called_once_with('6607')
    
    @patch('models.User.query')
    @patch('utils.decorators.jwt.decode')
    @patch('api.v1.views.posts.jsonify')
    def test_get_post_for_user_success(self, mock_jsonify,
                                       mock_jwt_decode, mock_user):
        """Test if one can see posts for another user"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_user.get.return_value = MagicMock(id='6607')
        mock_posts = mock_user.return_value.posts
        result = MagicMock()
        result.to_dict.return_value = {'id': 'ax2736'}
        mock_posts.return_value = [result]

        response = self.client.get('/api/v1/users/6607/posts/')
        self.assertEqual(response.status_code, 200)
        mock_user.get.assert_called_once_with('6607')
        mock_jsonify.assert_called_once()

    @patch('models.User.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_post_for_user_not_found(self,
                                       mock_jwt_decode, mock_user):
        """Test that posts cannot be retrieved if a user does not exist"""
        mock_jwt_decode.return_value = {'email': 'test@example.net'}
        mock_user.get.return_value = None
        mock_posts = mock_user.return_value.posts
        result = MagicMock()
        result.to_dict.return_value = {'id': 'ax2736'}
        mock_posts.return_value = [result]

        response = self.client.get('/api/v1/users/6607/posts/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_user.get.assert_called_once_with('6607')

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('models.Post')
    def test_create_post_success(self, mock_post,
                                 mock_jwt_decode, mock_get_user_by_email):
        """Test that a post can be created"""
        mock_jwt_decode.return_value = {'email': 'test@example.com'}
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_post = mock_post.return_value
        mock_post.save.return_value = True
        contents = {
                    'user_id': '6607',
                    'title': 'test',
                    'content': 'test'
                   }
        mock_post.to_dict.return_value = contents
        response = self.client.post('/api/v1/posts',
                                    json={'title': 'test', 'content': 'test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, contents|response.json)
    
    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_create_post_no_title(self, mock_jwt_decode, mock_get_user_by_email):
        """Test that a post cannot be created without a title"""
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        response = self.client.post('/api/v1/posts', json={'content': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Title/Content must be provided'})

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_create_post_no_content(self, mock_jwt_decode, mock_get_user_by_email):
        """Test that a post cannot be created without content"""
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        response = self.client.post('/api/v1/posts', json={'title': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Title/Content must be provided'})

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_create_post_nothing(self, mock_jwt_decode, mock_get_user_by_email):
        """Test that a post cannot be created without JSON data"""
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        response = self.client.post('/api/v1/posts')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'not a JSON'})

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_edit_post_success(self, mock_query,
                               mock_jwt_decode, mock_get_user_by_email):
        """Test that a post can be created without JSON data"""
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_jwt_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.return_value = MagicMock(id='ax4832', user_id='6607',
                                                title='test', content='test')
        mock_post = mock_query.get.return_value
        mock_post.save.return_value = True
        mock_post.to_dict.return_value = {'id': 'ax4832',
                                          'title': 'hello',
                                          'content': 'world',
                                          'user_id': '6607'}
        response = self.client.put('/api/v1/posts/ax4832', json={'title': 'hello',
                                                                 'content': 'world'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_post.title, 'hello')
        self.assertEqual(mock_post.content, 'world')
        self.assertEqual(response.json, {'id': 'ax4832', 'title': 'hello',
                                         'content': 'world', 'user_id': '6607'})
        mock_query.get.assert_called_once_with('ax4832')
        mock_post.save.assert_called_once()

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    def test_edit_post_wrong_JSON(self,
                               mock_jwt_decode, mock_get_user_by_email):
        """Test that a post cannot be created without JSON data"""
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        response = self.client.put('/api/v1/posts/ax4832')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, {'error': 'not a JSON'})

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_edit_post_nothing(self, mock_query, mock_decode,
                               mock_get_user_by_email):
        """Test if nothing changes when an empty json is passed"""   
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_query.get.return_value = MagicMock(user_id='6607', id='ax4885',
                                           title='test', content='test')
        mock_post = mock_query.get.return_value
        mock_post.save.return_value = True
        mock_post.to_dict.return_value = {}

        response = self.client.put('/api/v1/posts/ax4885', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_post.title, 'test')
        self.assertEqual(mock_post.content, 'test')

    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_edit_post_content(self, mock_query, mock_decode,
                               mock_get_user_by_email):
        """Test if only content gets updated when only content changed"""   
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_query.get.return_value = MagicMock(user_id='6607', id='ax4885',
                                           title='test', content='test')
        mock_post = mock_query.get.return_value
        mock_post.save.return_value = True
        mock_post.to_dict.return_value = {}
        
        response = self.client.put('/api/v1/posts/ax4885', json={
            'content': 'hello'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_post.title, 'test')
        self.assertEqual(mock_post.content, 'hello')
        
    @patch('models.User.get_user_by_email')
    @patch('utils.decorators.jwt.decode')
    @patch('models.Post.query')
    def test_edit_post_user_not_permissioned(self, mock_query, mock_decode,
                               mock_get_user_by_email):
        """Test if update is rejected when user is not permissioned"""   
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_query.get.return_value = MagicMock(user_id='6608', id='ax4885',
                                           title='test', content='test')
        mock_post = mock_query.get.return_value
        mock_post.save.return_value = True
        mock_post.to_dict.return_value = {}
        
        response = self.client.put('/api/v1/posts/ax4885', json={
            'content': 'hello'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'forbidden'})
        self.assertEqual(mock_post.title, 'test')
        self.assertEqual(mock_post.content, 'test')
        

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_delete_post_success(self, mock_query,
                                 mock_get_user_by_email, mock_jwt_decode):
        """Test that a user can delete their post"""
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_query.get.return_value = MagicMock(id='ax4832', user_id='6607')
        mock_query.get.return_value.delete.return_value = True

        response = self.client.delete('/api/v1/posts/ax4832')
        self.assertEqual(response.status_code, 204)
        mock_get_user_by_email.assert_called_once_with('abc@example.net')
        mock_query.get.assert_called_once_with('ax4832')
        mock_query.get.return_value.delete.assert_called_once()
    
    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_delete_post_not_permitted(self, mock_query,
                                 mock_get_user_by_email, mock_jwt_decode):
        """Test that a user cannot delete another user's post"""
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_query.get.return_value = MagicMock(id='ax4832', user_id='6609')
        mock_query.get.return_value.delete.return_value = True

        response = self.client.delete('/api/v1/posts/ax4832')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'forbidden'})
        mock_get_user_by_email.assert_called_once_with('abc@example.net')
        mock_query.get.assert_called_once_with('ax4832')
        mock_query.get.return_value.delete.assert_not_called()

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_delete_post_not_found(self, mock_query,
                                 mock_get_user_by_email, mock_jwt_decode):
        """Test that a user cannot delete a post that is not there, like deleted"""
        mock_jwt_decode.return_value = {'email': 'abc@example.net'}
        mock_get_user_by_email.return_value = MagicMock(id='6607')
        mock_query.get.return_value = None

        response = self.client.delete('/api/v1/posts/ax4832')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_get_user_by_email.assert_called_once_with('abc@example.net')
        mock_query.get.assert_called_once_with('ax4832')
