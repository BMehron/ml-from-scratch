# Is Unique: Implement an algorithm to determine if a string has all unique characters.
#  What if you cannot use additional data structures?

# 12847532

def is_unique_using_set(string):
    return len(set(string)) == len(string)

def is_unique_using_bit_vector(string):
    # here we assume that characters of the string are subset of the ASCII set
    bit_vector = 0
    for char in string:
        char_code = ord(char)
        if bit_vector & (1 << char_code):
            return False
        bit_vector |= 1 << char_code
    return True

def test_function(is_unique_funtion, tests):
    for string, answer in tests:
        assert answer == is_unique_funtion(string), f"Function {is_unique_funtion.__name__} failed at test {string}"
    print(f"All tests are passed! {is_unique_funtion.__name__}")

if __name__ == "__main__":
    tests = [("anbshbf", False), ("ajdrtf", True), ("", True), ("ashdkfjga", False)]
    test_function(is_unique_using_set, tests)
    test_function(is_unique_using_bit_vector, tests)