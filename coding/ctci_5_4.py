# Next Number: Given a positive integer, print the next smallest and the next largest number that
# have the same number of 1 bits in their binary representation.

def get_next(num):
    c0 = 0  
    c1 = 0
    c = num
    
    while c & 1 == 0 and c:
        c0 += 1
        c >>= 1

    while c & 1 == 1:
        c1 += 1
        c >>= 1
    
    if c0 + c1 == 0 or c0 + c1 == 32:
        return -1
    
    p = c0 + c1
    # set bit p to 1
    num |= 1 << p
    # clear all bits left to 1
    num &= ~((1 << p) - 1)
    # set to c1-1 ones in suffix of num
    num |= (1 << (c1-1)) - 1
    return num

if __name__ == "__main__":
    print(get_next(5))
    print(get_next(11))

