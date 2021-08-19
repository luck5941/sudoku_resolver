#!/bin/python
import problem_definition as pd
import utils
from sys import argv

if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception("Puzzle not indicate")
        exit(-1)

    puzzle = utils.read_sudoku(argv[1])
    solution = pd.Sudoku(utils.read_sudoku("test1/solution"))
    i_sudoku = pd.Sudoku(puzzle)
    i_state = pd.State(i_sudoku)
    print(i_state)
    action = pd.Action(i_state)
    successors = action.get_successors()
    if len(successors) == 1:
        print(solution == successors[0].sudoku)
        print(solution)
    else:
        print(len(successors))




