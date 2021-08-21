class Sudoku:
    """Class in charge of represent the sudoku
    puzzle. It has a 9*9 matrix with the initial state
    of the puzzle and a 9*9 matrix with the sudoku's solution
    """

    def __init__(self, matrix):
        """ constructor of the sudoku
        Parameters:
        -----------
        matrix: int[9][9]
            the matrix with the puzzle
        """
        self.matrix = [[x for x in row] for row in matrix]
        self.availables = self.update_availables()
        self.last_update = ()

    def __iter__(self):
        """method in charge of start the iter process on the
        free position of the puzzle"""
        self.position = 0
        return self

    def __next__(self):
        """method in charge of iter over all the free position
        of the puzzle"""
        if self.position < len(self.availables):
            p = self.availables[self.position]
            self.position += 1
            return p
        else:
            raise StopIteration

    def __len__(self):
        """method in charge of return the number of free position"""
        return sum([row.count(0) for row in self.matrix])

    def __getitem__(self, key):
        """method in charge of return the availables number on one specific
        position
        Parameters:
        ----------
        key: (int, int)
            a tuple with the position to ask
        """
        for p in self.availables:
            if p[0][0] == key[0] and p[0][1] == key[1]:
                return p[1]

    def __setitem__(self, key, value):
        i, j = key
        if not self.available(value, i, j):
            raise Exception("Invalid update")
        for missing in self.availables:
            ii, jj = missing[0]
            if ii == i and jj == j:
                self.matrix[i][j] = value
                self.last_update = (i, j, value)
                if value in missing[1]:
                    missing[1].remove(value)
                break

    def __str__(self):
        s = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                s += f"{self.matrix[i][j]}|"
            s += "\n"
        return s

    def __eq__(self, other):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def clone(self):
        return Sudoku(matrix=self.matrix)

    def update_availables(self):
        _missing = [(i // 9, i % 9) for i in range(9 ** 2) if self.matrix[i // 9][i % 9] == 0]
        availables = [(p, set(self.get_availables(p[0], p[1]))) for p in _missing]
        availables = sorted(availables, key=lambda x: len(x[1]))
        self.availables = availables
        return availables

    def available(self, n, i, j):
        """Method in charge of check if key can be set into the position i, j
        of the puzzle
        Parameters:
        -----------
        key: int
            number between 1 and 9 for check if is available on the selected position
        i: int
            number between 0 and 8 representing the row
        j: int
            number between 0 and 8 representing the column
        """

        if not 0 < n < 10:
            raise Exception(str(n) + " Number not valid")
        if not 0 <= i < 9:
            raise IndexError(f"i {i} must be between 0 and 9")
        if not 0 <= j < 9:
            raise IndexError(f"j {j} must be between 0 and 9")

        if (n in self.matrix[i] or
                n in [row[j] for row in self.matrix] or
                n in [self.matrix[ii // 9][ii % 9] for ii in range(9 ** 2) if
                      3 * ((ii // 9) // 3) + (ii % 9) // 3 == 3 * (i // 3) + j // 3]):
            return False
        else:
            return True

    def get_availables(self, i, j):
        """Method in charge of return the list of posibles values into the position i, j of the puzzle
        Parameters:
        -----------
        i: int
            number between 0 and 8 representing the row
        j: int
            number between 0 and 8 representing the column
        """
        for n in range(1, 10):
            if self.available(n, i, j) is True:
                yield n

    @property
    def is_valid(self):
        for x in self.availables:
            if len(x[1]) == 0:
                return False
        return True

class State:
    def __init__(self, sudoku, g=0, h=0):
        self.sudoku = sudoku
        self.g = g
        self.h = h

    def __eq__(self, state2):
        return self.sudoku == state2.sudoku

    def __str__(self):
        return f"g: {self.g} h: {self.h}: missing:  {len(self.sudoku)}"

    @property
    def complete(self):
        return len(self.sudoku) == 0

    def clone(self):
        return State(self.sudoku, self.g, self.h)


def reduce_list(sudoku):
    cont = 0
    nodes_possibles = sudoku.availables
    
    for node in nodes_possibles:
        i, j = node[0]
        if len(node[1]) == 1:
            cont += 1
            sudoku[i, j] = node[1].pop()
        else:
            break
    sudoku.update_availables()
    return cont


class Action:
    def __init__(self, state):
        self._state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def get_successors(self):
        new_sudoku = self._state.sudoku.clone()
        pos = -1
        while pos != 0:
            pos = reduce_list(new_sudoku)

        successors = [State(new_sudoku)]
        for tmp in new_sudoku.availables:
            if len(tmp[1]) == 0:
                return []
            for p in tmp[1]:
                i, j = tmp[0]
                tmp_sudoku = new_sudoku.clone()
                tmp_sudoku[i, j] = p
                successors.append(State(tmp_sudoku))
        return successors
