# String Compression: Implement a method to perform basic string compression using the counts of repeated characters. 
# For example, the string aabcccccaaa would become a2blc5a3, If the "compressed" string would not become smaller than 
# the original string, your method should return the original string.
#  You can assume the string has only uppercase and lowercase letters (a - z).

# def compress_string(string_list: list):
#     if len(string_list) <= 1:
#         return ''.join(string_list)
#     original_string = ''.join(string_list)
#     end_idx = 1
#     cur_counter = 1
#     for i in range(1, len(string_list)):
#         if string_list[i] == string_list[i-1]:
#             cur_counter += 1
#             continue
#         if cur_counter > 1:
#             string_list[end_idx] = str(cur_counter)
#             end_idx += 1
        
#         string_list[end_idx] = string_list[i]
#         end_idx += 1
#         cur_counter = 1
    
#     if cur_counter > 1:
#         string_list[end_idx] = str(cur_counter)
#         end_idx += 1
    
#     if end_idx == len(string_list):
#         return original_string
#     return ''.join(string_list[:end_idx])
        

def compress_string_a(string):  
    compressed = []
    curr_count = 0
    for i in range(len(string)):
        if i != 0 and string[i] != string[i-1]:
            compressed_part
            compressed.append(f"{string[i-1]}{curr_count}")
            curr_count = 0
        curr_count += 1
    compressed.append(f"{string[-1]}{curr_count}")
    return min(string, ''.join(compressed), key=len)

def test_function(function, tests):
    for string, answer in tests:
        assert answer == function(list(string)), f"Function {function.__name__} failed at test {string}, {function(list(string))=}"
    print(f"All tests are passed! {function.__name__}")

if __name__ == "__main__":
    tests = [("aabcccccaaa", "a2bc5a3"), ("ajdrtf", "ajdrtf"), ("aa", "aa")]
    test_function(compress_string_a, tests)