# Check Permutation: Given two strings, write a method to decide if one is a permutation of the other.

from collections import Counter 

def check_permutation_using_counter(string_a, string_b):
    string_a_counter = Counter(string_a)
    string_b_counter = Counter(string_b)
    for char in string_a:
        if string_a_counter[char] != string_b_counter[char]:
            return False
    return True

def test_function(is_unique_funtion, tests):
    for string_a, sting_b, answer in tests:
        assert answer == is_unique_funtion(string_a, sting_b), f"Function {is_unique_funtion.__name__} failed at test {string_a=}, {sting_b=}"
    print(f"All tests are passed! {is_unique_funtion.__name__}")

if __name__ == "__main__":
    tests = [("anbs", "bsna", True), ("ajdrtf", "adfg", False), ("", "", True), ("ashdkfjga", "", False)]
    test_function(check_permutation_using_counter, tests)