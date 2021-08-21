#!/bin/python
import problem_definition as pd
import utils
from sys import argv
from algorith import AStar, get_path

if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception("Puzzle not indicate")
        exit(-1)

    puzzle = utils.read_sudoku(argv[1])
    i_sudoku = pd.Sudoku(puzzle)
    i_state = pd.State(i_sudoku)
    print(i_state)

    a_start = AStar(2)
    result = a_start.start(i_state)
    print(result[0].state.sudoku)





