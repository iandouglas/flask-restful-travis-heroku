import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from api import create_app, db
from api.database.models import User
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class PatchuserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user_1 = User(username='zzz 1', email='e1')
        self.user_1.insert()

        # adding extra padding in here to ensure we strip() it off later
        self.payload = {
            'username': ' new_username ',
            'email': ' new_email ',
        }

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_happypath_patch_a_user(self):
        payload = deepcopy(self.payload)

        response = self.client.patch(
            f'/api/v1/users/{self.user_1.id}',
            json=payload,
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

        assert_payload_field_type_value(
            self, data, 'username', str, payload['username'].strip()
        )
        assert_payload_field_type_value(
            self, data, 'email', str, payload['email'].strip()
        )

        user_id = data['id']
        assert_payload_field_type(self, data, 'links', dict)
        links = data['links']
        assert_payload_field_type_value(
            self, links, 'get', str, f'/api/v1/users/{user_id}'
        )
        assert_payload_field_type_value(
            self, links, 'patch', str, f'/api/v1/users/{user_id}'
        )
        assert_payload_field_type_value(
            self, links, 'delete', str, f'/api/v1/users/{user_id}'
        )
        assert_payload_field_type_value(
            self, links, 'index', str, '/api/v1/users'
        )

    def test_sadpath_patch_blank_username(self):
        payload = deepcopy(self.payload)
        payload['username'] = ''

        response = self.client.patch(
            f'/api/v1/users/{self.user_1.id}',
            json=payload,
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'username' parameter is blank"]
        )

    def test_sadpath_patch_blank_email(self):
        payload = deepcopy(self.payload)
        payload['email'] = ''
        response = self.client.patch(
            f'/api/v1/users/{self.user_1.id}',
            json=payload,
            content_type='application/json'
        )
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'email' parameter is blank"]
        )

    def test_sadpath_patch_user_bad_id(self):
        response = self.client.patch(
            f'/api/v1/users/9999999'
        )
        self.assertEqual(404, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'message', str, 'resource not found'
        )
