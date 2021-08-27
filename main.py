#!/bin/python
import datetime
from sys import argv

import problem_definition as pd
import utils
import algorith

if __name__ == '__main__':
    i_sudoku = pd.Sudoku(utils.read_sudoku(argv[1]))
    print(i_sudoku)
    i_state = pd.State(i_sudoku)
    dfs = algorith.DFS(i_state, len(i_sudoku)+1)
    start_time = datetime.datetime.now()
    print(start_time)
    final_state = dfs.start(slow_aproach=False, increment=1)
    elapsed = datetime.datetime.now() - start_time
    if final_state is not None:
        print(final_state.sudoku)
        print(final_state.g)
    else:
        print("Not solution found")
    print(f"time requeired: {elapsed}")



