import json
import unittest

from api import create_app, db
from api.database.models import User
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetUsersTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


class GetAllUsersTest(GetUsersTest):
    def test_happypath_get_all_users(self):
        user_1 = User(username='zzz 1', email='email 1')
        user_1.insert()
        user_2 = User(username='aaa 1', email='email 2')
        user_2.insert()

        response = self.client.get(
            f'/api/v1/users'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'results', list)

        results = data['results']

        # we expect user 2 first to ensure we're getting results in
        # ascending alphabetical order by username
        next_result = results[0]
        assert_payload_field_type_value(
            self, next_result, 'username', str, user_2.username
        )
        assert_payload_field_type_value(
            self, next_result, 'email', str, user_2.email
        )
        user_id = next_result['id']

        assert_payload_field_type(self, next_result, 'links', dict)

        links = next_result['links']
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

        next_result = results[1]
        assert_payload_field_type_value(
            self, next_result, 'username', str, user_1.username
        )
        assert_payload_field_type_value(
            self, next_result, 'email', str, user_1.email
        )
        user_id = next_result['id']

        assert_payload_field_type(self, next_result, 'links', dict)



    def test_happypath_get_empty_users(self):
        response = self.client.get(
            f'/api/v1/users'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'results', list)
        # results list should be empty
        self.assertEqual(0, len(data['results']))
