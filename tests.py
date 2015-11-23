from wsgi import application
import unittest


class KeymasterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_key_upload(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        self.assertEqual(result.status_code, 200)
