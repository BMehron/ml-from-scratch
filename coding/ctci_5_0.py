# Get Bit

def get_bit(num: int, i: int) -> int:
    return 1 if num & (1 << i) != 0 else 0

# clearBit

def clear_bit(num: int, i: int) -> int:
    return num & (~(1 << i))

def clear_bit_untill(num: int, i: int) -> int:
    return num & (1 << i - 1)

def clear_bit_after(num: int, i: int) -> int:
    mask = -1 << (i+1)
    return num & mask
# SetBit

def set_bit(num: int, i: int, value: int) -> int:
    erase_bit = num & (~(1 << i))
    return erase_bit | (value << i)

