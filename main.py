#!/usr/bin/env python
from sys import argv, stderr, stdout
import datetime
import problem_definition as pd
import A_star
import utils

if len(argv)< 3:
    raise Exception("Error: Missing some arguments\n")

#read the sudoku passed by parameter
i_sudoku = utils.read_sudoku(argv[1])
i_sudoku = pd.Sudoku(i_sudoku)
i_state = pd.State(i_sudoku)

start_time = datetime.datetime.now()
print(start_time)
astar = A_star.AStar(int(argv[2]))

results = astar.start(i_state)
elapsed = datetime.datetime.now() - start_time

if results[1] is not None:
    print(results[1])
    print(results[0].state.sudoku)
    print("required time: {}".format(int(elapsed.total_seconds())))
else:
    print("No solution")


