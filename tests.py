import unittest
from unittest.mock import patch, MagicMock
from main import get_ping, notify


class TestMain(unittest.TestCase):

    @patch('main.speedtest')
    def test_get_ping(self, mock_speedtest):
        # Set up mock results
        mock_results = {'ping': 5}
        mock_speedtest.Speedtest.return_value.results.ping = mock_results['ping']

        # Call function and check result
        result = get_ping()
        self.assertEqual(result, mock_results)

    @patch('main.get_ping')
    def test_notify(self, mock_get_ping):
        # Set up mock results
        mock_results = {'ping': 5}
        mock_get_ping.return_value = mock_results

        # Call function and check result
        result = notify()
        self.assertIsNone(result)  # This function doesn't return anything, so just check for None


if __name__ == '__main__':
    unittest.main()
