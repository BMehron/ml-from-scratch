#Zero Matrix: Write an algorithm such that if an element in an MxN matrix is 0, its entire row and column are set to 0.
 


def zero_matrix_inplace(matrix):
    first_row_has_zero = False
    first_col_has_zero = False

    for i in range(len(matrix)):
        if matrix[i][0] == 0:
            first_col_has_zero = True
            break

    for j in range(len(matrix[0])):
        if matrix[0][j] == 0:
            first_row_has_zero = True
            break
    
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            if matrix[i][0] == 0 or matrix[0][j]==0:
                matrix[i][j] = 0
    
    if first_row_has_zero:
        for j in range(len(matrix[0])):
            matrix[0][j] = 0
    
    if first_col_has_zero:
        for i in range(len(matrix)):
            matrix[i][0] = 0
    
    return matrix


import unittest
from copy import deepcopy

class Test(unittest.TestCase):

    test_cases = [
        (
            [
                [1, 2, 3, 4, 0],
                [6, 0, 8, 9, 10],
                [11, 12, 13, 14, 15],
                [16, 0, 18, 19, 20],
                [21, 22, 23, 24, 25],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [11, 0, 13, 14, 0],
                [0, 0, 0, 0, 0],
                [21, 0, 23, 24, 0],
            ],
        )
    ]
    testable_functions = [zero_matrix_inplace]

    def test_zero_matrix(self):
        for f in self.testable_functions:
            for [test_matrix, expected] in self.test_cases:
                test_matrix = deepcopy(test_matrix)
                assert f(test_matrix) == expected


if __name__ == "__main__":
    unittest.main()

