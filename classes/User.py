class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
        self.is_admin = False