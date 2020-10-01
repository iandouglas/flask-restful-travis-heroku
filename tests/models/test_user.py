import unittest
from sqlalchemy.exc import IntegrityError

from api import create_app, db
from api.database.models import User


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        user = User(username='ian', email='ian.douglas@iandouglas.com')
        user.insert()

        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.id)
        self.assertEqual('ian', user.username)
        self.assertEqual('ian.douglas@iandouglas.com', user.email)

    def test_user_model_with_forced_id(self):
        user = User(username='ian',
                    email='ian.douglas@iandouglas.com',
                    user_id=1)
        user.insert()

        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.id)
        self.assertEqual(1, user.id)
        self.assertEqual('ian', user.username)
        self.assertEqual('ian.douglas@iandouglas.com', user.email)

    def test_user_model_trimmed_username(self):
        user = User(username=' ian ', email='ian.douglas@iandouglas.com')
        user.insert()

        self.assertEqual('ian', user.username)

    def test_user_model_trimmed_email(self):
        user = User(username='ian', email=' ian.douglas@iandouglas.com ')
        user.insert()

        self.assertEqual('ian.douglas@iandouglas.com', user.email)

    def test_user_model_unique_username(self):
        user = User(username='ian', email='ian.douglas@iandouglas.com')
        user.insert()

        try:
            user = User(username='ian', email='ian.douglas+2@iandouglas.com')
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_user_model_blank_username(self):
        try:
            user = User(username='', email='ian.douglas@iandouglas.com')
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_user_model_missing_username(self):
        try:
            user = User(username=None, email='ian.douglas@iandouglas.com')
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_user_model_unique_email(self):
        user = User(username='ian', email='ian.douglas@iandouglas.com')
        user.insert()

        try:
            user = User(username='ian2', email='ian.douglas@iandouglas.com')
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_user_model_blank_email(self):
        try:
            user = User(username='ian', email='')
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_user_model_missing_email(self):
        try:
            user = User(username='ian', email=None)
            user.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover
