from termcolor import colored

def copy_matrix(matrix):
    return Matrix("".join([digit.get_value() for digit in matrix.flat_matrix()]))

def check_input(input):
    parts = input.split(',');
    if(len(parts) != 9):
        return False

    for i in parts:
        if(len(i) == 9):
            for j in i:
                if(not j.isnumeric() and j != 'x'):
                    return False
        else:
            return False
    return True

def get_block(row, column):
    if( row <= 2 and column <= 2):
        return 0
    elif( row <= 2 and 3 <= column < 6 ):
        return 1
    elif( row <= 2 and 6 <= column < 9 ):
        return 2
    elif( 3 <= row < 6 and column <= 2 ):
        return 3
    elif( 3 <= row < 6 and 3 <= column < 6 ):
        return 4
    elif( 3 <= row < 6 and 6 <= column < 9 ):
        return 5
    elif( row >= 6 and column <= 2 ):
        return 6
    elif( row >= 6 and 3 <= column < 6 ):
        return 7
    elif( row >= 6 and 6 <= column < 9 ):
        return 8
    else:
        return -1

def check_errors(data):
    data_without_zeros = [digit.get_value() for digit in data if digit.get_value() != "0"]
    return len(data_without_zeros) == len(set(data_without_zeros))

def check_all_errors(matrix):
    for row in range(9):
        if(not check_errors(matrix.get_row(row))):
            return False
    for column in range(9):
        if(not check_errors(matrix.get_column(column))):
            return False
    for block in range(9):
        if(not check_errors(matrix.get_block(block))):
            return False
    return True
    
def fix_digits(matrix):
    changes = 0
    for zero in matrix.get_zeros_position():
        possibilities = matrix.get_matrix()[zero[0]][zero[1]].get_possibilities()
        if(len(possibilities) == 1):
            matrix.get_matrix()[zero[0]][zero[1]].set_value(possibilities[0])
            changes += 1
    return (matrix, changes)

def try_numbers(matrix):
    alterate_matrix = Matrix(matrix)
    for zero in alterate_matrix.get_zeros_position():
        for test_digit in range(1, 10):
            alterate_matrix.get_matrix()[zero[0]][zero[1]].set_value(str(test_digit))
            if(check_all_errors(alterate_matrix)):
                alterate_matrix.get_matrix()[zero[0]][zero[1]].add_possibility(str(test_digit))
        alterate_matrix.get_matrix()[zero[0]][zero[1]].set_value("0")
        alterate_matrix.get_matrix()[zero[0]][zero[1]].set_type("p")
    return alterate_matrix

class Matrix:
    def __init__(self, input_values):
        self.input = input_values.replace("x", "0")
        self.input = self.input.replace(",", "")
        self.matrix = [[],[],[],[],[],[],[],[],[]]
        self.zeros_pos = []
        row = -1
        for index, value in enumerate(self.input):
            if((index) % 9 == 0):
                row = row +1
            self.matrix[row].append(Cell(value, row, len(self.matrix[row])))
        self.find_zeros_position()

    def __str__(self):
        result = ""
        for line in self.matrix:
            result += "\n"
            for digit in line:
                result += str(digit) + " "
        return result

    def initial_check(self):
        for row in range(9):
            if(not check_errors(self.get_row(row))):
                return False
        for column in range(9):
            if(not check_errors(self.get_column(column))):
                return False
        for block in range(9):
            if(not check_errors(self.get_block(block))):
                return False
        return True

    def flat_matrix(self):
        return [item for sublist in self.matrix for item in sublist]

    def get_matrix(self):
        return self.matrix
    
    def get_row(self, row):
        return self.matrix[row]

    def print_row(self, row):
        result = ""
        for digit in self.get_row(row):
            result += digit.get_value()
        return result

    def get_column(self, column):
        return [self.matrix[n][column] for n in range(9)]

    def print_column(self, column):
        result = ""
        for digit in self.get_column(column):
            result += digit.get_value()
        return result

    def get_block(self, block):
        return [digit for digit in self.flat_matrix() if get_block(digit.get_row(), digit.get_column()) == block]

    def print_block(self, block):
        result = ""
        for digit in self.get_block(block):
            result += digit.get_value()
        return result

    def left_to_complete(self):
        return len([digit for digit in self.flat_matrix() if digit.get_value() == "0"])

    def find_zeros_position(self):
        for row, line in enumerate(self.matrix):
            for column, digit in enumerate(line):
                if(digit.get_value() == "0"):
                    self.zeros_pos.append((row, column))

    def get_zeros_position(self):
        return self.zeros_pos



class Cell:
    def __init__(self, value, row, column):
        self.value = value
        self.posibilities = []
        self.type = "f" if self.value != "0" else "p"
        self.row = row
        self.column = column
    
    def __str__(self):
        return colored(self.value if self.type == "f" else "•", "magenta" if self.type == "f" else "blue")

    def get_type(self):
        return self.type

    def set_type(self, value):
        self.type = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.type = "f"

    def get_column(self):
        return self.column

    def get_row(self):
        return self.row

    def add_possibility(self, value):
        self.posibilities.append(value)

    def get_possibilities(self):
        return self.posibilities