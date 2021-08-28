from sys import stderr


def perror(string):
    """
    Function in charge of write a message into the error system output
    :param str string: the message to be display
    """
    stderr.write("Error:\n\t" + string)


def read_sudoku(file):
    """
    Function in charge of read a file and return it as a matrix of number
    :rtype: list[list[int]]
    :param str file: the path of the file
    :return: the matrix with the sudoku
    """
    with open(file, "r") as f:
        puzzle = f.read().split("\n")
    if len(puzzle[-1]) == 0:
        puzzle = puzzle[:-1]
    try:
        puzzle = [[int(n) for n in list(line)] for line in puzzle]
    except ValueError:
        perror("The file must be formated as list of numbers,  separate the rows by _end-line")
        exit(-1)
    return puzzle

