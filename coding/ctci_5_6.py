#PairwiseSwap: Write a program to swap odd and even bits in an integer with as few instructions as
#possible (e.g., bit 0 and bit 1 are swapped, bit 2 and bit 3 are swapped, and so on).

def swap_bits(num):
    for i in range(0, 32, 2):
        bit_i = (num & (1 << i)) >> i
        bit_i_1 = (num & (1 << (i+1))) >> (i+1)
        if bit_i != bit_i_1:
            num ^= 1 << i
            num ^= 1 << (i+1)
    return num 


if __name__ == "__main__":
   pass