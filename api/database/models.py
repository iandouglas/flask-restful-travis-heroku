import bleach
from sqlalchemy import Column, String, Integer
from api import db


class User(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # unique username
    username = Column(String(80), unique=True, nullable=False)
    # unique email
    email = Column(String(100), unique=True, nullable=False)

    def __init__(self, username, email, user_id=None):
        if username is not None:
            username = bleach.clean(username).strip()
            if username == '':
                username = None

        if email is not None:
            email = bleach.clean(email).strip()
            if email == '':
                email = None

        self.username = username
        self.email = email
        if user_id is not None:
            self.id = user_id

    def insert(self):
        """
        inserts a new model into a database
        the model must have a unique username
        the model must have a unique id or null id
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        updates a new model into a database
        the model must exist in the database
        """
        db.session.commit()

    def delete(self):
        """
        deletes model from database
        the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()
