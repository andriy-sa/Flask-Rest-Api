import unittest

from app import create_app
from models.company import Company
from models.user import User
from tests import entities
from flask import json


class AuthModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client(use_cookies=True)

        # Default seed
        self.company = Company.create(entities.company)
        user = entities.user
        user['company_id'] = self.company.id
        self.user = User.create(user)

    def tearDown(self):
        self.app_ctx.pop()
        self.company.delete()
        self.user.delete()

    def test_unautorized_me(self):
        res = self.client.get('/api/me')
        self.assertEqual(res.status_code, 401)

    def test_failed_login(self):
        res = self.client.post('/api/login', data={
            'email': 'admin@mail.com',
            'password': 'password85'
        })
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        res_json = json.loads(res.data)
        self.assertIsNotNone(res_json['email'])

    def test_success_login(self):
        res = self.client.post('/api/login', data={
            'email': 'admin@mail.com',
            'password': 'password'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        res_json = json.loads(res.data)
        self.assertEqual(res_json['email'], 'admin@mail.com')

    def test_full_process(self):
        res = self.client.post('/api/login', data={
            'email': 'admin@mail.com',
            'password': 'password'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        res_json = json.loads(res.data)
        self.assertEqual(res_json['email'], 'admin@mail.com')

        res = self.client.get('/api/me')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        res_json = json.loads(res.data)
        self.assertEqual(res_json['email'], 'admin@mail.com')

        res = self.client.get('/api/logout')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/me')
        self.assertEqual(res.status_code, 401)
