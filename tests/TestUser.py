# -*- coding: utf-8 -*-

import unittest

from app import createApp, db
from app.Models import User, Role, Permission


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = createApp("testing")
        self.appContext = self.app.app_context()
        self.appContext.push()
        db.create_all()
        Role.insertRoles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appContext.pop()

    def testSetPassword(self):
        user = User()
        user.password = "abcabc"
        self.assertTrue(user.passwordHash is not None)

    def testVerifyPassword(self):
        user = User()
        user.password = "abcabc"
        self.assertTrue(user.verifyPassword("abcabc"))

    def testGetPassword(self):
        # 试图get会抛异常
        user = User()
        user.password = "abcabc"
        with self.assertRaises(AttributeError):
            user.password

    def testPasswordSaltsAreRandom(self):
        userA = User(password="abcabc")
        userB = User(password="abcabc")
        self.assertNotEqual(userA.passwordHash, userB.passwordHash)

    def testConfirmToken(self):
        user = User(password="abcabc")
        token = user.generateConfirmationToken()
        self.assertTrue(user.confirm(token))
        self.assertFalse(user.confirm("error"))

    def testUserPermissions(self):
        user = User(email="abc@163.com", username="nino", password="abc123")
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertFalse(user.can(Permission.ADMINISTER))

    def testAdministratorPermissions(self):
        administrator = User(
            email="superhamster@163.com", username="nino", password="abcabc")
        self.assertTrue(administrator.can(Permission.FOLLOW))
        self.assertTrue(administrator.can(Permission.ADMINISTER))

    def testIsAdministrator(self):
        administrator = User(
            email="superhamster@163.com", username="nino", password="abcabc")
        self.assertTrue(administrator.isAdministrator())

    def testResetPassword(self):
        self.assertFalse(User.resetPassword("error", "error"))

        user = User(email="abc@163.com", username="nino", password="abc123")
        db.session.add(user)
        db.session.commit()
        self.assertTrue(
            User.query.filter_by(
                email="abc@163.com").first().verifyPassword("abc123"))

        token = user.generateResetToken()
        user.resetPassword(token, "abcabca")
        self.assertFalse(
            User.query.filter_by(
                email="abc@163.com").first().verifyPassword("abc123"))
        self.assertTrue(
            User.query.filter_by(
                email="abc@163.com").first().verifyPassword("abcabca"))


def main():
    unittest.main()


if __name__ == '__main__':
    main()