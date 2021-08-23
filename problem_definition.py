def get_sub_matrix(ii, jj):
    return 3*(ii//3) + jj//3


class Sudoku:
    def __init__(self, matrix):
        self.matrix = [[x for x in row] for row in matrix]

    def __setitem__(self, key, value):
        i, k = key
        if self.valid_position(i, k, value):
            self.matrix[i][k] = value
        else:
            raise Exception("Invalid value")


    def __eq__(self, other):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __copy__(self):
        return Sudoku(self.matrix)

    def __str__(self):
        return "\n".join(["|".join([str(x) for x in row]) for row in self.matrix])

    def __len__(self):
        return len(list(self.empty_position))

    def __hash__(self):
        return hash((tuple(x) for x in self.matrix))

    def valid_position(self, i, j, value):
        for ii in range(len(self.matrix)):
            for jj in range(len(self.matrix[ii])):
                if i == ii and value == self.matrix[ii][jj]:
                    return False
                elif j == jj and value == self.matrix[ii][jj]:
                    return False
                elif get_sub_matrix(ii, jj) == get_sub_matrix(i, j) and value == self.matrix[ii][jj]:
                    return False
        return True

    @property
    def empty_position(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    yield i, j
    @property
    def available(self):
        availables = []
        for position in self.empty_position:
            i, j = position
            availables.append(((i, j), set()))
            for k in range(1, 10):
                if self.valid_position(i, j, k):
                    availables[-1][1].add(k)
        availables = sorted(availables, key=lambda x: len(x[1]), reverse=True)
        return availables

    def remove_trivial_solution_l1(self, posibles=False):
        if not posibles:
            posibles = self.available
        for posible in posibles:
            if len(posible[1]) == 1:
                try:
                    self[posible[0]] = posible[1].pop()
                except:
                    return None
            else:
                continue
        return self

    def remove_trivial_solution(self):
        posibles = self.available
        old = len(posibles)
        new = -1
        while old != new:
            if self.remove_trivial_solution_l1(posibles) is None:
                return None
            posibles = self.available
            old = new
            new = len(posibles)
        return self


class State:
    def __init__(self, sudoku, g=0, h=0):
        self.sudoku = sudoku
        self.g = g
        self.h = h

    def __eq__(self, other):
        return self.sudoku == other.sudoku

    def __copy__(self):
        return State(self.sudoku, self.g, self.h)

    def __hash__(self):
        return hash(self.sudoku)
    @property
    def complete(self):
        return len(self.sudoku) == 0

    def set_sudoku(self, sudoku):
        self.sudoku = sudoku


class Action:
    def __init__(self, state):
        self.state = state

    def get_successors(self):
        new_sudoku = self.state.sudoku.__copy__()
        new_state = self.state.__copy__()
        new_sudoku = new_sudoku.remove_trivial_solution()
        if new_sudoku is None:
            return []
        new_state.set_sudoku(new_sudoku)
        movements = [new_state]
        for tmp in new_sudoku.available:
            if len(tmp[1]) == 0:
                return []
            for p in tmp[1]:
                i, j = tmp[0]
                tmp_sudoku = new_sudoku.__copy__()
                tmp_sudoku[i, j] = p
                tmp_state = self.state.__copy__()
                tmp_state.set_sudoku(tmp_sudoku)
                movements.append(tmp_state)

        return movements
