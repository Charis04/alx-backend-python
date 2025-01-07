#!/usr/bin/env python3
"""A test file to test access_nested_map"""
import unittest
from parameterized import parameterized
from typing import (
    Mapping,
    Sequence,
    Any,
)
from utils import access_nested_map


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


if __name__ == "__main__":
    unittest.main()
