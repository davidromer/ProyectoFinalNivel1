import tempfile
import unittest
from pathlib import Path

from user_management import UserManager, UserNotFoundError, ValidationError


class UserManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "usuarios.txt"
        self.manager = UserManager(str(self.file_path))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_list_user(self) -> None:
        self.manager.add_user(1, "Ana", "ana@example.com", 25)
        users = self.manager.list_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "Ana")

    def test_reject_invalid_email(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "Ana", "invalid-email", 25)

    def test_reject_duplicate_id(self) -> None:
        self.manager.add_user(1, "Ana", "ana@example.com", 25)
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "Ana2", "ana2@example.com", 30)

    def test_reject_invalid_age(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "Ana", "ana@example.com", -1)
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "Ana", "ana@example.com", 121)

    def test_reject_invalid_name(self) -> None:
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "   ", "ana@example.com", 25)
        with self.assertRaises(ValidationError):
            self.manager.add_user(1, "Ana|Ruiz", "ana@example.com", 25)

    def test_find_and_delete_user(self) -> None:
        self.manager.add_user(1, "Ana", "ana@example.com", 25)
        found = self.manager.find_user(1)
        self.assertEqual(found["email"], "ana@example.com")

        self.manager.delete_user(1)
        with self.assertRaises(UserNotFoundError):
            self.manager.find_user(1)


if __name__ == "__main__":
    unittest.main()
