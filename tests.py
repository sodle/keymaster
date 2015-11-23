from keymaster import application
import unittest
from urlparse import urljoin


class KeymasterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        application.config["TESTING"] = True
        application.config["DEBUG"] = True
        self.app = application.test_client()

    def tearDown(self):
        pass

    def test_key_upload_success(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        self.assertEqual(result.status_code, 200)

    def test_key_upload_returns_url(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        self.assertTrue('http' in result.data)

    def test_key_retrieval(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        result2 = self.app.get(result.data)
        self.assertEqual(result2.status_code, 200)

    def test_raw_key_retrieval(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        result2 = self.app.get(result.data + '/key')
        self.assertEqual(result2.status_code, 200)

    def test_key_extension(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        extend_url = result.data + '/extend'
        result2 = self.app.post(extend_url)
        self.assertEqual(result2.status_code, 302)

    def test_key_expiration(self):
        result = self.app.post('/k', data=dict(public_key="test key"))
        expire_url = result.data + '/expire'
        result2 = self.app.post(expire_url)
        self.assertEqual(result2.status_code, 302)
