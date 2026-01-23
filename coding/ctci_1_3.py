# URLify: Write a method to replace all spaces in a string with '%20'. You may assume that the string has sufficient 
# space at the end to hold the additional characters, and that you are given the "true" length of the string. 
# (Note: If implementing in Java, please use a character array so that you can perform this operation in place.)
#EXAMPLE
# Input: "Mr 3ohn Smith 13 
# Output: "Mr%203ohn%20Smith"

# Pythonic Solution
import unittest

def urlify(string, length):
    return string[:length].replace(" ", "%20")



def urlify_algo(string, length):
    """replace spaces with %20 and removes trailing spaces"""
    # convert to list because Python strings are immutable
    char_list = list(string)
    new_index = len(char_list)

    for i in reversed(range(length)):
        if char_list[i] == " ":
            # Replace spaces
            char_list[new_index - 3 : new_index] = "%20"
            new_index -= 3
        else:
            # Move characters
            char_list[new_index - 1] = char_list[i]
            new_index -= 1
    # convert back to string
    return "".join(char_list[new_index:])

def urlify_my(string, length):
    char_list = list(string[:length])
    for i in range(len(char_list)):
        if char_list[i] == ' ':
            char_list[i] = "%20"
    return ''.join(char_list)

def urligy_python(char_list, length):
    # Replace in-place "space" chars by "%20". In the char_list first lenght of characters are true ones.
    char_idx = length-1
    end_idx = len(char_list)-1
    while char_idx >= 0:
        if char_list[char_idx] != " ":
            char_list[end_idx] = char_list[char_idx]
            end_idx -= 1
        else:
            char_list[end_idx-2: end_idx+1] = "%20"
            end_idx -= 3
        char_idx -= 1
    return "".join(char_list[end_idx+1:])



# Examples:
# ["a", " ", "b", "c", " ", "", "", "", ""]

class Test(unittest.TestCase):
    """Test Cases"""

    test_cases = {
        ("much ado about nothing      ", 22): "much%20ado%20about%20nothing",
        ("Mr John Smith       ", 13): "Mr%20John%20Smith",
        (" a b    ", 4): "%20a%20b",
        (" a b       ", 5): "%20a%20b%20",
    }
    testable_functions = [urlify_algo, urlify, urlify_my, urligy_python]

    def test_urlify(self):
        for urlify in self.testable_functions:
            for args, expected in self.test_cases.items():
                if urlify.__name__ != "urligy_python":
                    actual = urlify(*args)
                else:
                    actual = urlify(list(args[0]), args[1])
                assert actual == expected, f"Failed {urlify.__name__} for: {[*args]}, {actual=}"


if __name__ == "__main__":
    unittest.main()