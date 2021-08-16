def read_sudoku(file):
    with open(file, "r") as f:
        puzzle = f.read().split("\n")[:-1]
    puzzle = [[int(n) for n in list(line)] for line in puzzle]
    return puzzle

