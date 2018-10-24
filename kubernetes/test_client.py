import sys
import unittest
from .client import Client

if sys.version_info >= (3, 3):
    from unittest import mock
else:
    import mock


class TestClient(unittest.TestCase):

    @mock.patch('requests.get')
    def test_get_stats_non_200_response_without_errors(self, mock_get):
        mock_resp = self.__mock_response(status=500)
        mock_get.return_value = mock_resp

        client = Client("stats_url", "timeout")
        self.assertRaises(Exception,
                          client.get_stats, 1,
                          msg="Invalid status code, got 500, expected 200")

    @mock.patch('requests.get')
    def test_get_stats_non_200_response_with_empty_errors(self, mock_get):
        mock_resp = self.__mock_response(status=500, json_data={'errors': []})
        mock_get.return_value = mock_resp

        client = Client("stats_url", "timeout")
        self.assertRaises(Exception,
                          client.get_stats, 1,
                          msg="Invalid status code, got 500, expected 200")

    @mock.patch('requests.get')
    def test_get_stats_non_200_response_with_errors(self, mock_get):
        mock_get.return_value = self.__mock_response(
            status=500, json_data={'errors': [
                {'code': 10, 'message': 'test'},
                {'code': 11, 'message': 'test1'}]})

        client = Client("stats_url", "timeout")
        self.assertRaises(Exception,
                          client.get_stats, 1,
                          msg="Error: 10 - test, Error 11 - test1")

    @mock.patch('requests.get')
    def test_get_stats_success(self, mock_get):
        mock_resp = self.__mock_response(status=200)
        mock_get.return_value = mock_resp

        client = Client("stats_url", "timeout")
        client.get_stats()

    def __mock_response(self, status=200, json_data=None, raise_on_json=None):
        response = mock.Mock()
        response.status_code = status
        response.json = mock.Mock()
        if json_data:
            response.json = mock.Mock(
                return_value=json_data
            )
        if raise_on_json is not None:
            response.json.side_effect = raise_on_json

        return response
