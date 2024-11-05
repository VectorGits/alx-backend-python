#!/usr/bin/env python3
"""
Test the Client class in client.py
"""

import unittest
from typing import Dict
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError
from utils import access_nested_map, get_json, memoize


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json):
        """
        Test the org method
        """
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that the _public_repos_url method
        returns the correct value
        """
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "test"}
            test_class = GithubOrgClient("google")
            self.assertEqual(test_class._public_repos_url, "test")
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock):
        """
        Test that GithubOrgClient.public_repos returns the correct value
        """
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "test"
            mock_get_json.return_value = [{"name": "test"}]
            test_class = GithubOrgClient("google")
            self.assertEqual(test_class.public_repos(), ["test"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("test")

        @parameterized.expand([
            ({"license": {"key": "my_license"}}, "my_license"),
            ({"license": {"key": "other_license"}}, "other_license")
        ])
        def test_has_license(self, repo: Dict[str, Dict], license_key: str):
            """
            Test that GithubOrgClient.has_license returns the correct value
            """
            test_class = GithubOrgClient("google")
            self.assertEqual(test_class.has_license(repo, license_key), True)


if __name__ == '__main__':
    unittest.main()
