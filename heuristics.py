def heuristic_1(state):
    i, j = state.sudoku.get_last_action
    #matrix, transverse, squads = state.sudoku.decompose
    state.h = sum((matrix[i].count(0), transverse[j].count(0), squads[i//3+j//3].count(0)))
    return state.h


def heuristic_2(state):
    i, j = state.sudoku.get_last_action
    #matrix, transverse, squads = state.sudoku.decompose
    state.h = min((matrix[i].count(0), transverse[j].count(0), squads[i//3+j//3].count(0)))
    return state.h


def heuristic_3(state):
    h = 0
    for x in state.sudoku:
        if len(x[1]) == 0:
            h += len(state.sudoku.matrix)**2
        else:
            h += len(x[1])
    state.h = h
    return state.h
