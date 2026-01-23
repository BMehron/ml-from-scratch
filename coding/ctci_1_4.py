# Palindrome Permutation: Given a string, write a function to check if it is a permutation of a palin- drome.
#  A palindrome is a word or phrase that is the same forwards and backwards. 
# A permutation is a rearrangement of letters. The palindrome does not need to be limited to just dictionary words.

from collections import Counter 
import unittest

def is_palindrome_permutation(string):
    counter = Counter(string)
    num_odd_letters = 0
    for value in counter.values():
        if value % 2 == 1:
            num_odd_letters += 1
    print(string, num_odd_letters)
    return num_odd_letters < 2

def is_palindrome_permutation_pythonic(phrase):
    """function checks if a string is a permutation of a palindrome or not"""
    counter = Counter(clean_phrase(phrase))
    return sum(val % 2 for val in counter.values()) <= 1

class Test(unittest.TestCase):
    test_cases = [
        ("aba", True),
        ("aab", True),
        ("abba", True),
        ("aabb", True),
        ("a-bba", True),
        ("a-bba!", True),
        ("Tact Coa", True),
        ("jhsabckuj ahjsbckj", True),
        ("Able was I ere I saw Elba", True),
        ("So patient a nurse to nurse a patient so", False),
        ("Random Words", False),
        ("Not a Palindrome", False),
        ("no x in nixon", True),
        ("azAZ", True),
    ]
    testable_functions = [
        is_palindrome_permutation,
    ]

    def test_pal_perm(self):
        for f in self.testable_functions:
            for [test_string, expected] in self.test_cases:
                assert f(test_string) == expected, f"{test_string=}, {f(test_string)=}"


if __name__ == "__main__":
    unittest.main()