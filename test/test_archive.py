import unittest
from src.archive import *


class UnitTests(unittest.TestCase):

    def test_convert_to_old_reddit(self):
        self.assertEqual(
            convert_to_old_reddit("https://www.reddit.com"),
            "https://old.reddit.com",
            "Failed to modify the URL properly.",
        )

    def test_illegal_characters(self):
        self.assertEqual(
            illegal_characters("abcdefghjklmnopqrstuvwxyz", 0),
            "abcdefghjklmnopqrstuvwxyz",
        )
        self.assertEqual(
            illegal_characters("abcdefghjklmnopqrstuvwxy*", 0),
            "abcdefghjklmnopqrstuvwxy",
        )
        self.assertEqual(
            illegal_characters("abcdefghjklmnopqrstuvwxy?", 1),
            "abcdefghjklmnopqrstuvwxy-",
        )


if __name__ == "__main__":
    unittest.main()
