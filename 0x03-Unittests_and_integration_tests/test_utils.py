#!/usr/bin/env python3
"""A test file to test access_nested_map"""
import unittest
from parameterized import parameterized
from typing import (
    Mapping,
    Sequence,
    Any,
)
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """a test case to test access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test method to test access_nested_map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, errmsg):
        """test exception for access nested map func"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), errmsg)


class TestGetJson(unittest.TestCase):
    """test case to test get_json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """test method to test"""
        # Set up the mock to return a Mock response with the desired payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function with the test URL
        result = get_json(test_url)

        # Assert that requests.get was called once with the test URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the function returned the expected payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """test case to test memoize"""
    def test_memoize(self):
        """a test method to test memoize"""
        class TestClass:
            """a test class"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Verify the result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method is only called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
