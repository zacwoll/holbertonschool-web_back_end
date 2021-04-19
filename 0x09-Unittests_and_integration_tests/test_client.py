#!/usr/bin/env python
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import Mock, patch, PropertyMock
from urllib.error import HTTPError
from utils import memoize


class TestGithubOrgClient(unittest.TestCase):
    """ Test GitHub Org Client """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org, mock_request):
        """ Test that GithubOrgClient.org returns the correct value """
        client = GithubOrgClient(org)
        self.assertEqual(client.org, mock_request.return_value)
        mock_request.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self):
        """ test _public_repos_url private method """
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value={"repos_url": "google"}) as mock_get:
            json = {"repos_url": "google"}
            client = GithubOrgClient(json.get("repos_url"))
            repos_url = client._public_repos_url
            mock_get.assert_called_once()
            self.assertEqual(repos_url, mock_get.return_value.get("repos_url"))

    @patch('client.get_json', return_value=[{"name": "google"}])
    def test_public_repos(self, mock_get_json):
        """ test public_repos method """
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/") as mock_url:
            client = GithubOrgClient("google")
            public_repos = client.public_repos()
            self.assertEqual(public_repos, ["google"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_return):
        """ test has_license """
        client = GithubOrgClient("google")
        has_license = client.has_license(repo, license_key)
        self.assertEqual(has_license, expected_return)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Test Integration with fixtures TEST_PAYLOAD """

    @classmethod
    def setUpClass(cls):
        """ Set up a requests.patch for all tests"""

        # Since it's not obvious, org_payload has to move down the list
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ Destroy the setUpCls """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ test public_repos method of GitHubClient """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ test public repos with licenses """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()
