import unittest
from AccountManagement.account_management import register_user, deregister_user


class TestAccountManagement(unittest.TestCase):

    def test_register(self):
        deregister_user("govn0001")
        self.assertEqual(register_user("govn0001", "Abcde12345", "Government Agency"), 1)   # OK
        self.assertEqual(register_user("govn000", "Abcde12345", "Government Agency"), 0)    # username violation
        self.assertEqual(register_user("govn0001", "45", "Government Agency"), 2)           # password violation
        self.assertEqual(register_user("govn0001", "Abcde12345", "Government Agency"), 3)   # exception occur (not unique)

    def test_deregister(self):
        register_user("temp0001", "Abcde12345", "Government Agency")
        self.assertTrue(deregister_user("temp0001"))                                        # OK
        self.assertFalse(deregister_user("asda"))                                           # user not exist


if __name__ == '__main__':
    unittest.main()
