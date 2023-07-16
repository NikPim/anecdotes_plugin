import unittest
from dummy_api_client import DummyAPIClient, InvalidTokenError, ServerDoesNotRespondError
from config import read_config

class DummyAPIClientTestCase(unittest.TestCase):
    def setUp(self):
        config = read_config()
        token = config.get("API", "token")

        self.correct_token = token
        self.incorrect_token = "incorrect token"
        self.correct_url = "https://dummyapi.io/data/v1/"
        self.incorrect_url = "https://dummyapi.io/data/v111"
        self.client = DummyAPIClient(self.correct_url, self.correct_token)

    def test_check_connection_with_correct_url(self):
        """
        Test to ensure that connection succeeds with correct URL
        """
        self.assertIsNone(self.client.check_connection())

    def test_check_connection_with_incorrect_url(self):
        """
        Test to ensure that connection raises ServerDoesNotRespondError with incorrect URL
        """
        self.client.home_url = self.incorrect_url
        with self.assertRaises(ServerDoesNotRespondError) as cm:
            self.client.check_connection()

        self.assertEqual(str(cm.exception), "Server does not respond")

    def test_check_connection_with_correct_token(self):
        """
        Test to ensure that connection succeeds with correct token
        """
        self.assertIsNone(self.client.check_connection())

    def test_check_connection_with_incorrect_token(self):
        """
        Test to ensure that connection raises InvalidTokenError with incorrect token
        """
        self.client.headers["app-id"] = self.incorrect_token
        with self.assertRaises(InvalidTokenError):
            self.client.check_connection()

if __name__ == "__main__":
    unittest.main()
