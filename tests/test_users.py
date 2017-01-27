import unittest

from app import create_app
from models.company import Company
from models.user import User
from tests import entities
from flask import json


class UserModelTestCase(unittest.TestCase):
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

    def test_check_created_user(self):
        self.assertIsNotNone(self.company)
        self.assertIsNotNone(self.user)

    def test_success_get_by_id(self):
        res = self.client.get('api/user/get_by_id/%s' % self.user.id)
        self.assertEqual(res.status_code, 200)

    def test_fail_get_by_id(self):
        res = self.client.get('api/user/get_by_id/%s' % 99)
        self.assertEqual(res.status_code, 404)

    def test_get_list(self):
        res = self.client.get('api/user/get_list')
        self.assertEqual(res.status_code, 200)

        res_json = json.loads(res.data)
        self.assertEqual(res_json['count'], 1)
        self.assertEqual(len(res_json['data']), 1)

    def test_get_list_pagination(self):
        res = self.client.get('api/user/get_list', query_string={'page': 2})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        res_json = json.loads(res.data)
        self.assertEqual(res_json['count'], 1)
        self.assertEqual(len(res_json['data']), 0)

    def test_fail_create_user(self):
        res = self.client.post('api/user/create', data={
            'username': 'andy',
            'email': 'andy@mail.com',
            'password': '1',
            'company_id': self.company.id
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')

        res_json = json.loads(res.data)
        self.assertIsNotNone(res_json['password'])

    def test_success_create_user(self):
        res = self.client.post('api/user/create', data={
            'username': 'andy',
            'email': 'andy@mail.com',
            'password': 'password',
            'company_id': self.company.id
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')

        res_json = json.loads(res.data)
        self.assertEqual(res_json['email'], 'andy@mail.com')
