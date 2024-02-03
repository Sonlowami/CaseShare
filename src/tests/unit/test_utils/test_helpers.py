from utils.helpers import generate_OTP
from utils.helpers import avoid_danger_in_json, is_uuid
import unittest
from parameterized import parameterized


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""

    def test_generate_OTP(self):
        """Test generate_OTP."""
        self.assertNotEqual(generate_OTP(), generate_OTP())
        self.assertEqual(len(generate_OTP()), 8)
        self.assertIsInstance(generate_OTP(), str)

    @parameterized.expand([
        ({'name': 'John', 'email': 'alert("hello")'}, {'name': 'John', 'email': 'alerthello'}),
        ({'email': "' OR 1=1 --"}, {'email': ' OR 1=1 '}),
        ({'email': "'; DROP TABLE users; --"}, {'email': " DROP TABLE users "}),
        ({'password': 'hdbc(48--;//)'}, {'password': 'hdbc(48--;//)'}),
        ({'title': 'Hello World!'}, {'title': 'Hello World!'}),
        ({}, {}),
    ])
    def test_avoid_danger_in_json_with_hashable_json(self, kwargs, expected):
        """Test avoid_danger_in_json."""
        self.assertEqual(avoid_danger_in_json(**kwargs), expected)

    @parameterized.expand([
        ('f4c2b3b3-6f9e-4a6a-8f2d-7a7c1b5e3c5c', True),
    ])
    def test_is_uuid(self, kwargs, expected):
        """Test is_uuid."""
        self.assertEqual(is_uuid(kwargs), expected)

    @parameterized.expand([
        ('f4c2b3b3-6f9e-4a6a-8f2d-7a7c1b5e3c5', ValueError),
        ('f4c2b3b3-6f9e-4a6a-8f2d-7a7c1b5e3c5c1', ValueError),
        (123, TypeError),
        (True, TypeError),
        (None, TypeError),
        (["f4c2b3b3-6f9e-4a6a-8f2d-7a7c1b5e3c5c"], TypeError),
    ])
    def test_is_uuid_invalid_uuid(self, args, expected):
        """Test is_uuid."""
        with self.assertRaises(expected):
            is_uuid(args)
