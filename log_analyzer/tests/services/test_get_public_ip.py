import unittest
from unittest.mock import patch, Mock

from log_analyzer.services.get_public_ip import get_public_ip

GET_PUBLIC_IP_REQUEST_GET_MODULE = "log_analyzer.services.get_public_ip.requests.get"


class TestGetPublicIp(unittest.TestCase):

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_returns_ip_on_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"ip": "192.168.1.1"}
        mock_get.return_value = mock_response

        ip = get_public_ip()
        self.assertEqual(ip, "192.168.1.1")

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_returns_none_on_request_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection Error")
        ip = get_public_ip()
        self.assertIsNone(ip)

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_returns_none_on_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        ip = get_public_ip()
        self.assertIsNone(ip)

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_returns_none_if_ip_key_is_missing(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"something_else": "192.168.1.1"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        ip = get_public_ip()
        self.assertIsNone(ip)

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_returns_none_on_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 500 error")
        mock_get.return_value = mock_response

        ip = get_public_ip()
        self.assertIsNone(ip)

    @patch(GET_PUBLIC_IP_REQUEST_GET_MODULE)
    def test_logs_error_on_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection Error")
        with self.assertLogs(level="ERROR") as log:
            ip = get_public_ip()
            self.assertTrue(any("Failed to obtain public IP" in message for message in log.output))
