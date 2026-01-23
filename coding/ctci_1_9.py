# String Rotation; Assume you have a method i s S u b s t r i n g which checks if one word is a substring of another.
#  Given two strings, si and s2, write code to check if s2 is a rotation of si using only one call to isSubst ring 
# [e.g., "waterbottle" is a rotation oP'erbottlewat"),

def string_rotation(s1, s2):
    if len(s1) != len(s2):
        return False
    return s1 in s2 + s2

import unittest
class Test(unittest.TestCase):

    test_cases = [
        ("waterbottle", "erbottlewat", True),
        ("foo", "bar", False),
        ("foo", "foofoo", False),
    ]

    def test_string_rotation(self):
        for [s1, s2, expected] in self.test_cases:
            actual = string_rotation(s1, s2)
            assert actual == expected


if __name__ == "__main__":
    unittest.main()