import unittest
from src.archive import *


class UnitTests(unittest.TestCase):

    def test_convert_to_old_reddit(self):
        self.assertEqual(
            convertToOldReddit("https://www.reddit.com"),
            "https://old.reddit.com",
            "Failed to modify the URL properly.",
        )


if __name__ == "__main__":
    unittest.main()
