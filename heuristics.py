def heuristic_1(state):
    i, j = state.sudoku.get_last_action
    matrix, transverse, squads = state.sudoku.decompose
    state.h = sum((matrix[i].count(0), transverse[j].count(0), squads[i//3+j//3].count(0)))
    return state.h


def heuristic_2(state):
    i, j = state.sudoku.get_last_action
    matrix, transverse, squads = state.sudoku.decompose
    state.h = min((matrix[i].count(0), transverse[j].count(0), squads[i//3+j//3].count(0)))
    return state.h

def heuristic_3(state):
    state.h = state.sudoku.get_missing
    return state.h
