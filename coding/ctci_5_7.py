# Draw Line: A monochrome screen is stored as a single array of bytes, allowing eight consecutive
# pixels to be stored in one byte.The screen has width w, where w is divisible by 8 (that is, no byte will
# be split across rows). The height of the screen, of course, can be derived from the length of the array
# and the width. Implement a function that draws a horizontal line from (xl, y) to (x2, y).
# The method signature should look something like:
# d r a w L i n e ( b y t e [ ] screen, i n t w i d t h , i n t x l , i n t x2, i n t y )

def drawLine(screen, width, x1, x2, y):
    byte_width = width // 8
    row_start = y*byte_width
       # Byte positions of x1 and x2
    start_idx = row_start + x1 // 8
    end_idx = row_start + x2 // 8
    
    # Bit positions within their bytes
    start_offset = x1 % 8
    end_offset = x2 % 8
    if start_idx == end_idx:
        screen[start_idx] |= ((1 << (8 - start_offset)) - 1) ^ ((1 << (7 - end_offset)) - 1)
    else:
        screen[start_idx+1:end_idx] = [(1 << 8) -1] * (end_idx - start_idx - 1)
        screen[start_idx] |= (1 << (8 - start_offset)) - 1
        screen[end_idx] |= ((1 << 8) - 1) ^ ((1 << (7 - end_offset)) - 1)
    return screen

def test_cases():
    # single pixel
    screen = drawLine([0], 8, 3, 3, 0)
    assert screen == [0b00010000], screen

    # one full byte
    screen = [0]
    drawLine(screen, 8, 0, 7, 0)
    assert screen == [0b11111111], screen

    # across byte boundary
    screen = [0, 0]
    drawLine(screen, 16, 6, 9, 0)
    assert screen == [0b00000011, 0b11000000], screen

    # multiple rows: affects only selected row
    screen = [0, 0]
    drawLine(screen, 8, 1, 6, 1)
    assert screen == [0b00000000, 0b01111110], screen

    # multi-byte span
    screen = [0, 0, 0]
    drawLine(screen, 24, 3, 20, 0)
    assert screen == [0b00011111, 0b11111111, 0b11111000], screen

if __name__ == "__main__":
   test_cases()