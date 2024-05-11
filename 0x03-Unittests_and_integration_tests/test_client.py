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


@parameterized_class((
    'org_payload', 'repos_payload',
    'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Class with test methods"""
    @classmethod
    def setUpClass(cls):
        """Method that sets up the class"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = cls.mock_response

    @classmethod
    def tearDownClass(cls):
        """Method that tears down the class"""
        cls.get_patcher.stop()

    @staticmethod
    def mock_response(url):
        """Method that mock the response"""
        if url == 'https://api.github.com/orgs/google':
            return MockResponse(
                    200, TestIntegrationGithubOrgClient.org_payload)
        elif url == 'https://api.github.com/orgs/google/repos':
            return MockResponse(
                    200, TestIntegrationGithubOrgClient.repos_payload)
        else:
            return MockResponse(404, {})


class MockResponse:
    """Class with methods"""
    def __init__(self, status_code, json_data):
        """Method that initializes the class"""
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        """Method that returns json_data"""
        return self.json_data


if __name__ == '__main__':
    unittest.main()
