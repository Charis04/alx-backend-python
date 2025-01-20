#!/usr/bin/env python3
"""Test module for Github Org Client
"""
import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json")
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
            GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock
        ) as mock_org:
            mock_org.return_value = mocked_payload

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("test-org")

            # Access the `_public_repos_url` property
            result = client._public_repos_url

            # Assert that the result matches the expected repos_url
            self.assertEqual(result, mocked_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mocked_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected result.
        """
        # Mock payload for the `repos_payload` property
        mocked_payload = [
            {"name": "test-repo1", "license": {"key": "mit"}},
            {"name": "test-repo2", "license": {"key": "apache-2.0"}},
            {"name": "test-repo3", "license": {"key": "mit"}},
        ]

        mocked_get_json.return_value = mocked_payload

        mocked_public_repos_url = "https://api.github.com/orgs/test-org/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=unittest.mock.PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = mocked_public_repos_url

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("test-org")

            # Call the `public_repos` method
            result = client.public_repos(license="mit")

            mocked_get_json.assert_called_once_with(mocked_public_repos_url)
            mocked_get_json.assert_called_once()

            # Assert that the result matches the expected list of repo names
            self.assertEqual(result, ["test-repo1", "test-repo3"])

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False)
        ]
    )
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that GithubOrgClient.has_license returns the expected result.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mock the JSON responses for different URLs
        def side_effect(url, *args, **kwargs):
            # Create a mock Response object
            mock_response = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test the public_repos method with a license argument"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
