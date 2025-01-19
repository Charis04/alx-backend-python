#!/usr/bin/env python3
"""Test module for Github Org Client
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        # Mock return value of get_json
        mock_get_json.return_value = {"name": org_name}

        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert that get_json was called with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the org method returns the correct value
        self.assertEqual(result, {"name": org_name})

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the expected
        result.
        """
        # Mock payload for the `org` property
        mocked_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
            }

        # Use patch as a context manager to mock the `org` property
        with patch.object(
            GithubOrgClient, 'org', new_callable=unittest.mock.PropertyMock
        ) as mock_org:
            mock_org.return_value = mocked_payload

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("test-org")

            # Access the `_public_repos_url` property
            result = client._public_repos_url

            # Assert that the result matches the expected repos_url
            self.assertEqual(result, mocked_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()
