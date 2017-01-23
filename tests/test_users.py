import unittest
from app import create_app


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

    def tearDown(self):
        self.app_ctx.pop()

    def test_test(self):
        self.assertTrue(True)