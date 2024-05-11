#!/usr/bin/env python3
"""Module with a unittest python script"""
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import unittest
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock, MagicMock


class TestGithubOrgClient(unittest.TestCase):
    """Class with test methods"""
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get):
        """Method that tests test_org"""
        org_url = f"https://api.github.com/orgs/{org_name}"
        expected_result = {"org_name": org_name, "other_data": "mocked"}
        mock_get.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get.assert_called_once_with(org_url)
        self.assertEqual(result, expected_result)

    def test_public_repos_url(self):
        """Method that tests the public_repos_url"""
        org_name = "test_org"
        expected_repos_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(
                GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_repos_url}

            client = GithubOrgClient(org_name)
            result = client._public_repos_url

            self.assertEqual(result, expected_repos_url)

    @patch('client.get_json')
    @patch.object(
            GithubOrgClient, '_public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Method that tests the public_repos"""
        mock_repos_url.return_value = "https://api.github.com\
                /orgs/test_org/repos"

        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache"}},
            {"name": "repo3"}  # No license key
        ]

        org_name = "test_org"
        client = GithubOrgClient(org_name)
        repos = client.public_repos(license="mit")

        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

        self.assertEqual(repos, ["repo1"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Method that tests if has license"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Class with test methods"""

    @classmethod
    def setUpClass(cls):
        """Method that sets up a class"""
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
        """Method that tears down a class"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Method that tests public repos"""
        client = GithubOrgClient('google')
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Method that tests public repos with licesnse"""
        client = GithubOrgClient('google')
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
