import unittest
from unittest.mock import patch, MagicMock
from api.v1.app import test_client, app


class TestComments(unittest.TestCase):
    """ Test comments API """

    def setUp(self):
        """ Method called to prepare the test fixture """
        self.client = test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """ Method called after the test method has been called and the result recorded """
        self.app_context.pop()

    @patch('models.Post.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comments(self, mock_decode, mock_query):
        """ Test get comments """
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_query.get.return_value = MagicMock(user_id='6607',
                                                content='test',
                                                id='1443')
        result = MagicMock()
        result.to_dict.return_value = {'id': '1443', 'user_id': '6607',
                                       'content': 'test', 'post_id': 'ax3934'}
        mock_query.get.return_value.comments = [result]
        response = self.client.get('/api/v1/posts/ax3934/comments')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json[0], result.to_dict.return_value)

    @patch('models.Post.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comments_not_found(self, mock_decode, mock_query):
        """ Test get comments not found """
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.return_value = None
        response = self.client.get('/api/v1/posts/ax3934/comments')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})

    @patch('models.Post.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comments_exception(self, mock_decode, mock_query):
        """ Test get comments exception """
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.side_effect = Exception('test')
        response = self.client.get('/api/v1/posts/ax3934/comments')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'unknown error occurred'})

    @patch('models.Comment.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comment(self, mock_decode, mock_query):
        """ Test get a single comment based on id"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.return_value = MagicMock(user_id='6607',
                                                content='test',
                                                id='1443')
        mock_query.get.return_value.to_dict.return_value = {'id': '1443',
                                                            'user_id': '6607',
                                                            'content': 'test',
                                                            'post_id': 'ax3934'}
        response = self.client.get('/api/v1/comments/1443')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json,
                             mock_query.get.return_value.to_dict.return_value)
        mock_query.get.assert_called_once_with('1443')

    
    @patch('models.Comment.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comment_not_found(self, mock_decode, mock_query):
        """ Test get comment returns 404 if comment not found """
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.return_value = None

        response = self.client.get('/api/v1/comments/1443')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_query.get.assert_called_once_with('1443')

    @patch('models.Comment.query')
    @patch('utils.decorators.jwt.decode')
    def test_get_comment_error(self, mock_decode, mock_query):
        """ Test get comment returns 404 if comment not found """
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_query.get.side_effect = Exception('test')

        response = self.client.get('/api/v1/comments/1443')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'unknown error occurred'})
        mock_query.get.assert_called_once_with('1443')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_success(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment success"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.return_value = MagicMock(id='ax3934')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json={'content': 'test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['content'], 'test')
        self.assertEqual(response.json['post_id'], 'ax3934')
        self.assertEqual(response.json['user_id'], '6607')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_not_json(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment fails to non-json data"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.return_value = MagicMock(id='ax3934')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json='test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'not a JSON')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_empty_json(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment fails to empty json data"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.return_value = MagicMock(id='ax3934')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "empty request")

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_empty_content(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment fails with empty content section"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.return_value = MagicMock(id='ax3934')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json={'content': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "empty request")

    
    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_user_not_found(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment fails with an inexistent user.
        This can happen like when a token is trying to be replayed
        once the user is deleted from the database"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = None
        mock_post_q.get.return_value = MagicMock(id='ax3934')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json={'content': ''})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "not found")

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_post_not_found(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test post comment fails with an inexistent post.
        This can happen when the post is deleted from the database"""
        mock_decode.return_value = {'email': 'abc@example.com'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.return_value = None
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                    json={'content': 'Test'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "not found")

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Post.query')
    def test_post_comment_internal_error(self, mock_post_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment returns 500 if internal error occurs"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_post_q.get.side_effect = Exception('test')
        response = self.client.post('/api/v1/posts/ax3934/comments',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'unknown error occurred'})
        mock_post_q.get.assert_called_once_with('ax3934')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_success(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if a user can successfully edit a post if they wrote it"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_comment_q.get.return_value = MagicMock(id='ax3934',
                                                    content='test',
                                                    user_id='6607')
        mock_save = mock_comment_q.get.return_value.save
        mock_save.return_value = True
        mock_dict = mock_comment_q.get.return_value.to_dict
        mock_dict.return_value = {'id': 'ax3934', 'content': 'hello'}
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['content'], 'hello')
        mock_save.assert_called_once()
        mock_dict.assert_called_once()
        mock_comment_q.get.assert_called_once_with('ax3934')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_no_change(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if a post doesn't change if the user doesn't change anything
        or tries to empty everything. For deleting a post, use DELETE method"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_comment_q.get.return_value = MagicMock(id='ax3934',
                                                    content='test',
                                                    user_id='6607')
        mock_save = mock_comment_q.get.return_value.save
        mock_save.return_value = True
        mock_dict = mock_comment_q.get.return_value.to_dict
        mock_dict.return_value = {'id': 'ax3934', 'content': 'text'}
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['content'], 'text')
        mock_save.assert_called_once()
        mock_dict.assert_called_once()
        mock_comment_q.get.assert_called_once_with('ax3934')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_not_json(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment raises bad request if no json given"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_comment_q.get.return_value = MagicMock(id='ax3934',
                                                    content='test',
                                                    user_id='6607')
        mock_save = mock_comment_q.get.return_value.save
        mock_save.return_value = True
        mock_dict = mock_comment_q.get.return_value.to_dict
        mock_dict.return_value = {'id': 'ax3934', 'content': 'text'}
        response = self.client.put('/api/v1/comments/ax3934',
                                   json='yoohoo!')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'not a JSON'})
        mock_save.assert_not_called()
        mock_dict.assert_not_called()
        mock_comment_q.get.assert_not_called()

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_user_doesnot_exist(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment returns 404 if user doesnot exist"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = None
        mock_comment_q.get.return_value = MagicMock(id='ax3934',
                                                    content='test',
                                                    user_id='6607')
        mock_save = mock_comment_q.get.return_value.save
        mock_save.return_value = True
        mock_dict = mock_comment_q.get.return_value.to_dict
        mock_dict.return_value = {'id': 'ax3934', 'content': 'text'}
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_save.assert_not_called()
        mock_dict.assert_not_called()
        mock_comment_q.get.assert_called_once_with('ax3934')


    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_doesnot_exist(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment returns 404 if comment doesnot exist"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_comment_q.get.return_value = None
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'not found'})
        mock_comment_q.get.assert_called_once_with('ax3934')

    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_unauthorized(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment raises 403 if user tries to edit
        a comment that is not theirs"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6609')
        mock_comment_q.get.return_value = MagicMock(id='ax3934',
                                                    content='test',
                                                    user_id='6607')
        mock_save = mock_comment_q.get.return_value.save
        mock_save.return_value = True
        mock_dict = mock_comment_q.get.return_value.to_dict
        mock_dict.return_value = {'id': 'ax3934', 'content': 'text'}
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'forbidden'})
        mock_save.assert_not_called()
        mock_dict.assert_not_called()
        mock_comment_q.get.assert_called_once_with('ax3934')
    
    @patch('utils.decorators.jwt.decode')
    @patch('models.User.get_user_by_email')
    @patch('models.Comment.query')
    def test_update_comment_internal_error(self, mock_comment_q, 
                          mock_user_get, mock_decode):
        """ Test if edit comment returns 500 if internal error occurs"""
        mock_decode.return_value = {'email': 'abc@example.net'}
        mock_user_get.return_value = MagicMock(id='6607')
        mock_comment_q.get.side_effect = Exception('test')
        response = self.client.put('/api/v1/comments/ax3934',
                                   json={'content': 'hello'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'unknown error occurred'})
        mock_comment_q.get.assert_called_once_with('ax3934')