# Insertion: You are given two 32-bit numbers, N and M, and two bit positions, i and
# j. Write a method to insert M into N such that M starts at bit j and ends at bit i. You
# can assume that the bits j through i have enough space to fit all of M. That is, if
# M = 10011, you can assume that there are at least 5 bits between j and i. You would not, for
# example, have j = 3 and i = 2, because M could not fully fit between bit 3 and bit 2.

def insert(n, m, i, j):
    # My Solution
    # first let's clear bit from j to i in n
    mask = ~((1 << (j+1) - 1) ^ (1 << i - 1))
    n = n & mask
    # move m by i
    return n | (m << i)

def updateBits(n, m, i, j):
    """
    Inserts M into N such that M starts at bit j and ends at bit i.
    Assumes enough space between i and j to fit M.
    """
    # 1. Create a mask to clear the bits in N between i and j
    # This creates a sequence of all ones (e.g., ~0 or -1 in many languages)
    all_ones = ~0 
    
    # Create the left part of the mask: 1s before bit j+1, then 0s.
    # (all_ones << (j + 1)) results in 1s from bit j+1 to the end.
    left_mask = (all_ones << (j + 1))
    
    # Create the right part of the mask: 0s before bit i, then 1s.
    # (1 << i) - 1 results in 1s from bit 0 to bit i-1.
    right_mask = ((1 << i) - 1)
    
    # Combine the left and right masks to create the final mask with zeros between i and j
    mask = left_mask | right_mask
    
    # Clear the bits in N between i and j
    n_cleared = n & mask
    
    # 2. Shift M to the correct position (starting at bit i)
    m_shifted = m << i
    
    # 3. Combine the modified N and shifted M
    result = n_cleared | m_shifted
    
    return result

# Example usage:
# N = 10000000000 (binary) = 1024 (decimal)
# M = 10011 (binary) = 19 (decimal)
# i = 2
# j = 6
# Result should be 10001001100 (binary)
N = int('10000000000', 2)
M = int('10011', 2)
i = 2
j = 6

result = insert(N, M, i, j)
print(f"Original N (binary): {bin(N)}")
print(f"Original M (binary): {bin(M)}")
print(f"Result (binary): {bin(result)}")
print(f"Result (decimal): {result}")
