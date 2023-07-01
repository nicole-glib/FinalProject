import bcrypt
from pymongo import MongoClient




client = MongoClient('localhost', 27017)

db = client.ElinoysDB

users_col = db.Users

class User:
    def __init__(self, username, hashed_password):
        self._username = username
        self._hashed_password = hashed_password
        self._is_admin = False

    @property
    def username(self):
        return self._username

    @property
    def hashed_password(self):
        return self._hashed_password

    @property
    def is_admin(self):
        return self._is_admin

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @hashed_password.setter
    def hashed_password(self, new_password):
        self._hashed_password = new_password

    @is_admin.setter
    def is_admin(self, is_admin):
        self._is_admin = is_admin

    def correct_password(self,password):
        if bcrypt.checkpw(password.encode('utf-8'), self._hashed_password):
            return True
        return False

    def to_db_format(self):
        return {
            'username': self._username,
            'hashed_password': self._hashed_password,
            'is_admin': self._is_admin
        }
    def signup(self):
        users_col.insert_one(self.to_db_format())


