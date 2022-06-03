#!/usr/bin/env python3

import os
import unittest
import tempfile

from nort.note import Note

class TestNoteParsing(unittest.TestCase):
    """Test case docstring."""
    def test_missing_metadata(self):
        test_content = "# Test\n---\nsomething that is not yaml\n---\n"
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, "test.md")
            with open(path, "w+") as f:
                f.write(test_content)
            note = Note.from_file(path)

        res = note.get_section("Test")
        with open("testshit", "w+") as f:
            f.write(res)
        self.assertEqual(test_content.strip(), res.strip())

if __name__ == "__main__":
    unittest.main()
