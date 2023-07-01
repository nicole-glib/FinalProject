import bcrypt
from pymongo import MongoClient




client = MongoClient('localhost', 27017)

db = client.ElinoysDB

users_col = db.Users

class User:
    def __init__(self, *args):
        if len(args) == 2:
            self.username = args[0]
            self.hashed_password = args[1]
            self.is_admin = False
        elif len(args) == 1:
            self.__dict__.update(args[0])
        else:
            pass

    def correct_password(self,password):
        if bcrypt.checkpw(password.encode('utf-8'), self.hashed_password):
            return True
        return False

    def signup(self):
        users_col.insert_one(self.__dict__)


