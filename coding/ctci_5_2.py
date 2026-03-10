# Binary to String: Given a reai number between 0 and 1 (e.g., 0.72) that is passed in as a double, print
# the binary representation. If the number cannot be represented accurately in binary with at most 32
# characters, print "ERROR."

def binary_to_strint(x):
    answer = []
    while x > 0 and len(answer) < 32:
        x *= 2
        if x >= 1:
            answer.append("1")
            x -= 1
        else:
            answer.append("0")
    if x > 0:
        print("ERROR")
    else:
        print("0." + "".join(answer))
    return 

        
if __name__ == "__main__":
    binary_to_strint(0.625)
    binary_to_strint(0.63)