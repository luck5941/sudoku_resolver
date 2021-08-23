#!/bin/python
import datetime
from sys import argv

import problem_definition as pd
import utils
import algorith



"""
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


puzzle = utils.read_sudoku(argv[1])
i_sudoku = pd.Sudoku(puzzle)
ll = i_sudoku.available
old = len(ll)
print(old)
for l in ll:
    print(l)
i_sudoku.remove_trivial_solution()
print("-----------------------------------")
new = -1
while new != old:
    i_sudoku.remove_trivial_solution()
    ll = i_sudoku.available
    old = new
    new = len(ll)

print(new)
for l in ll:
    print(l)

"""

if __name__ == '__main__':
    i_sudoku = pd.Sudoku(utils.read_sudoku(argv[1]))
    print(i_sudoku)
    i_sudoku.remove_trivial_solution()
    i_state = pd.State(i_sudoku)
    dfs = algorith.DFS(i_state, len(i_sudoku)+1)
    start_time = datetime.datetime.now()
    print(start_time)
    final_state = dfs.start()
    elapsed = datetime.datetime.now() - start_time
    if final_state is not None:
        print(final_state.sudoku)
    else:
        print("Not solution found")
    print(f"time requeired: {elapsed}")



