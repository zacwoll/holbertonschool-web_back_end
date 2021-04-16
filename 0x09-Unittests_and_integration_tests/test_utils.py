#!/usr/bin/env python3
""" Unittesting for utils.py """
import json
from parameterized import parameterized
import requests
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """ Tests access_nested_map method from utils """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ tests access_nested_map function using parameterized tests """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ tests that access_nested_map raises a KeyError when necessary """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Tests the get_json method from utils """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, payload):
        """ Tests that get_json works properly """

        mock_response = Mock()
        mock_response.json.return_value = payload

        with patch('requests.get', return_value=mock_response):
            response = get_json(url)
            self.assertEqual(response, payload)
            mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """ Tests the memoize method from utils """
    def test_memoize(self):
        """ test the memoize method """
        class TestClass:
            """ Basic Class to test functionality """

            def a_method(self):
                """ Simply return 42 when called """
                return 42

            @memoize
            def a_property(self):
                """ calls a_method to test memoization """
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            test_memo = test_class.a_property
            test_memo = test_class.a_property
            mock_method.assert_called_once()
