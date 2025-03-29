# tests/test_utils.py
import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.utils import extract_icon_number, format_icon_path, sanitize_filename

class TestUtils(unittest.TestCase):

    def test_extract_icon_number(self):
        path = "/i/065000/065123.png"
        self.assertEqual(extract_icon_number(path), "065123")

    def test_format_icon_path(self):
        path = "/i/065000/065123.png"
        expected = "https://xivapi.com/i/065000/065123.png"
        self.assertEqual(format_icon_path(path), expected)

    def test_sanitize_filename(self):
        name = r"Invalid:/\\Name*?"
        self.assertEqual(sanitize_filename(name), "Invalid___Name__")

if __name__ == '__main__':
    unittest.main()
