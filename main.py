import functions as fc
import numpy as np
import os
from termcolor import colored

os.system('cls')

def main():
    print("--- SUDOKU RESOLVER ---")
    # 4xx157x32,2xxxxxxx5,xx3xxx19x,5xxxxx9xx,xx9x31257,8xx54xx1x,xx2415xx8,x8x7634x9,xxx928x6x
    initial_sudoku = input("Introduce the numbers and Enter: ")
    if(not fc.check_input(initial_sudoku)):
        print("Invalid Input")
        return 1
    initial_matrix = fc.Matrix(initial_sudoku)
    print(initial_matrix)
    if(initial_matrix.left_to_complete() == 0):
        print("Completed Sudoku")
        return 2
    if(not initial_matrix.initial_check()):
        print("This sudoku contains errors")
        return 3
    raw_initial_matrix = "".join([digit.get_value() for digit in initial_matrix.flat_matrix()])
    alterate_matrix = fc.try_numbers(raw_initial_matrix)
    (new_mat, changes) = fc.fix_digits(alterate_matrix)
    print(new_mat)
    print("Cambios: ", changes)
    while (changes > 0):
        (new_mat, changes) = fc.fix_digits(new_mat)
        raw_new_mat = "".join([digit.get_value() for digit in new_mat.flat_matrix()])
        new_mat = fc.try_numbers(raw_new_mat)
        print(new_mat)
        print("Cambios: ", changes)


main()
