#One Away: There are three types of edits that can be performed on strings: insert a character, remove a character, or replace a character. 
# Given two strings, write a function to check if they are one edit (or zero edits) away.
#EXAMPLE
#pale, pie -> true pales, pale -> true pale, bale -> true pale, bake -> false
import unittest

def are_one_edit_different(string_a, string_b):
    if len(string_a) < len(string_b):
        return are_one_edit_different(string_b, string_a)
    if string_a == string_b:
        return True
    elif len(string_a) == len(string_b):
        # they should differ only in one position:
        num_same_chars = 0
        for i in range(len(string_a)):
            if string_a[i] == string_b[i]:
                num_same_chars += 1
        return num_same_chars == len(string_a) - 1
    elif len(string_a) == len(string_b) + 1:
        for i in range(len(string_b)):
            if string_a[i] != string_b[i]:
                return string_a[i+1:] == string_b[i:]
        return True
    else:
        return False
            
def test_function(function, tests):
    for string_a, sting_b, answer in tests:
        assert answer == function(string_a, sting_b), f"Function {function.__name__} failed at test {string_a=}, {sting_b=}"
    print(f"All tests are passed! {function.__name__}")


class Test(unittest.TestCase):
    test_cases = [
        # no changes
        ("pale", "pale", True),
        ("", "", True),
        # one insert
        ("pale", "ple", True),
        ("ple", "pale", True),
        ("pales", "pale", True),
        ("ples", "pales", True),
        ("pale", "pkle", True),
        ("paleabc", "pleabc", True),
        ("", "d", True),
        ("d", "de", True),
        # one replace
        ("pale", "bale", True),
        ("a", "b", True),
        ("pale", "ble", False),
        # multiple replace
        ("pale", "bake", False),
        # insert and replace
        ("pale", "pse", False),
        ("pale", "pas", False),
        ("pas", "pale", False),
        ("pkle", "pable", False),
        ("pal", "palks", False),
        ("palks", "pal", False),
        # permutation with insert shouldn't match
        ("ale", "elas", False),
    ]

    testable_functions = [are_one_edit_different]

    def test_one_away(self):

        for f in self.testable_functions:
            for _ in range(100):
                for [text_a, text_b, expected] in self.test_cases:
                    assert f(text_a, text_b) == expected


if __name__ == "__main__":
    unittest.main()

# if __name__ == "__main__":
#     tests = [("pale", "pales", True), ("", "A", True), ("asv", "s", False), ("", "", True)]
#     test_function(is_one_edit, tests)
    
