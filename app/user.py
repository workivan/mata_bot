class User(object):
    def __init__(self, nickname, login, imporved=False, banned=False, subscription=True, is_admin=False):
        self.nickname = nickname
        self.login = login
        self.is_admin = is_admin
        self.subscription = subscription
        self.improved = imporved
        self.banned = banned
