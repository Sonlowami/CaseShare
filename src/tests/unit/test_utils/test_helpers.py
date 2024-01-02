from utils.helpers import generate_OTP
from utils.helpers import avoid_danger_in_json
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
