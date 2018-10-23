import unittest
from app import app


class UserReportTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # print('setup')

    # def setUpClass(cls):
    #     print('setupClass')

    def tearDown(self):
        print('tearDown')

    # def tearDownClass(cls):
    #     print('tearDownClass')

    def register(self, nickname, password):
        return self.app.post('/api/v1/seller/register/', data={'username':nickname, 'password':password}, follow_redirects=True)

    def login(self, nickname, password):
        return self.app.post('/login/', data={'username':nickname, 'password':password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/')

    def test_reg_logout_login(self):
        assert self.register('hello', 'world').status_code == 200
        assert b'-hello' in self.app.open('/').data
        self.logout()
        assert b'-hello' not in self.app.open('/').data
        self.login('hello', 'world')
        assert b'-hello' in self.app.open('/').data

    def test_profile(self):
        r = self.app.open('/profile/3/', follow_redirects=True)
        assert r.status_code == 200
        assert b'password' in r.data
        self.register('hello2', 'world')
        assert b'hello2' in self.app.open('/profile/1/', follow_redirects=True).data

