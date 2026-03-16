#Conversion: Write a function to determine the number of bits you would need to flip to convert
# integer A to integer B.

def convert_a_to_b(a, b):
    c = a ^ b
    count = 0
    while c:
        count += c & 1
        c >>= 1
    return count

def smarth_convert(a, b):
    c = a ^ b
    count = 0
    while c:
        count += 1
        c &= c-1
    return count

if __name__ == "__main__":
    print(convert_a_to_b(29, 15)) # 2
    print(convert_a_to_b(29, 4)) # 3
    print(smarth_convert(29, 15)) # 2
    print(smarth_convert(29, 4)) # 3

