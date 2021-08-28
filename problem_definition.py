
def get_sub_matrix(ii, jj):
    """function in charge of return the sub matrix of the current cell
    :rtype: int
    :param int ii: the number of the row
    :param int jj: the number of the column
    :return: the sub matrix number
    :raise IndexError: If get invalid range of value
    """
    if 0 <= ii < 9 or 0 <= jj < 9:
        return 3*(ii//3) + jj//3
    else:
        raise IndexError("The column and the row must be in the range [0,8]")


class Sudoku:
    """Class in charge of represent a sudoku. It has the matrix with the numbers.

    Attributes
    __________
    matrix: list[list[int]]
        the matrix with the problem. The empty cells are represented as 0
    """

    def __init__(self, matrix):
        """Default constructor. Create a copy of the matrix passed by parameter
        :param list[list[int]] matrix: the board of the game.
        :raises ValueError: If the board is not a square or If detect invalid number into the board.
        """
        self.matrix = []
        for row in matrix:
            if len(row) != len(matrix):
                raise ValueError("The board must be a square")
            self.matrix.append([])
            for x in row:
                if 0 <= x <= len(matrix):
                    self.matrix[-1].append(x)
                else:
                    raise ValueError("The values must be a positive number fewer of the length of the board")

    def __getitem__(self, key):
        """Method in charge of return the value into the cell especificate into the key parameter of the board
        :rtype: int
        :param tuple[int] key: The position of the matrix that want to know. It must be a tuple of two position
        :return: The content of the cell
        :raises IndexError: If get invalid cell or if the key does not have two position.
        """
        if len(key) != 2:
            raise IndexError("Invalid cell selected")
        i, j = key
        if 0 <= i < 9 and 0 <= j < 9:
            return self.matrix[i][j]
        else:
            raise IndexError("Invalid cell selected")

    def __setitem__(self, key, value):
        """Method in charge of update the matrix
        :param tuple[int] key: The position of the matrix that want to know. It must be a tuple of two position
        :param value: The new value of this position
        :raises ValueError: If cant set this value on this position
        :raises IndexError If get invalid cell or if the key does not have two position.
        """
        if len(key) != 2:
            raise IndexError("Invalid cell selected")
        i, k = key
        if 0 <= i < 9 and 0 <= k < 9:
            if self.valid_position(i, k, value):
                self.matrix[i][k] = value
            else:
                s = f"Can not update the matrix with {value} on cell {(i, k)}"
                raise ValueError(s)
        else:
            raise IndexError("Invalid cell selected")

    def __eq__(self, other):
        """Method in charge of compare two sudokus. For that compare all the cells of both boards
        :rtype: bool
        :param Sudoku other: The sudoku to be compared
        :return: True if are equals otherwise False
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __copy__(self):
        """Method in charge of return a copy of the current sudoku
        :rtype Sudoku
        :return: The copy of the sudoku
        """
        return Sudoku(self.matrix)

    def __str__(self):
        """Method in charge of represent as string the sudoku
        :rtype: str
        :return: The sudoku representation
        """
        return "\n".join(["|".join([str(x) for x in row]) for row in self.matrix])

    def __len__(self):
        """
        :rtype: int
        :return: the number of empty cells of the board
        """
        return len(list(self.empty_position))

    def __hash__(self):
        return hash((tuple(x) for x in self.matrix))

    def valid_position(self, i, j, value):
        """Method in charge of check if the value can be set into the cell selected
        :rtype bool
        :param int i: the row of the board
        :param int j: the column of the board
        :param int value: the new value
        :return: If is a valid position
        """
        if self.matrix[i][j] != 0:
            return False
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
        """Generator of the empty cells for the board
        :rtype Generator[tuple[int, int], None, None]
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    yield i, j

    @property
    def available(self):
        """
        Property with a bideimensional tuple with the positions free and the availables values of that position
        order by the number of availables options on each cell
        :rtype: list[tuple[tuple[int, int], set]]
        :return: the list
        """
        availables = []
        for position in self.empty_position:
            i, j = position
            availables.append(((i, j), set()))
            for k in range(1, 10):
                if self.valid_position(i, j, k):
                    availables[-1][1].add(k)
        availables = sorted(availables, key=lambda x: len(x[1]))
        return availables

    def _remove_trivial_solution_l1(self, posibles=()):
        """
        Method in charge of set all the cells that only has one option available
        :param tuple[int] posibles: the list with the cells and theirs options.
        :return: The same sudoku after update it
        :rtype: Sudoku
        """
        if not posibles:
            posibles = self.available
        for posible in posibles:
            # break the for when the number of options are more than one
            if len(posible[1]) == 1:
                try:
                    self[posible[0]] = posible[1].pop()
                # If can not set the value, the current sudoku is invalid so return None to indicate that
                except ValueError:
                    return None
            else:
                break
        return self

    def _remove_trivial_solution_l2(self, matrix):
        """
        Method in charge of set all the cell on that a value has its unique option to be set
        :param list[list[int]] matrix: the matrix to be update
        :return: if the method change some cell
        :rtype: bool
        """
        diff = False
        for value in range(1, len(matrix)):
            # iter over all valid values
            for i in range(len(matrix)):
                # iter over the rows and check if the value is missing
                if value not in matrix[i]:
                    posibles = set()
                    # iter over all the rows of the i cell and check if the value is valid
                    for j in range(len(matrix[i])):
                        if self.valid_position(i, j, value):
                            posibles.add(j)
                    # if in this row, there is only one valid position for the value, it must be correct and set it
                    if len(posibles) == 1:
                        j = posibles.pop()
                        self[i, j] = value
                        diff = True
        return diff

    def remove_trivial_solution(self):
        """
        Method in charge of remove trivial solution trying to reduce the empty cells of the board.
        For that use the private method _remove_trivial_solution_l2 and _remove_trivial_solution_l1 and call it while
        there are some changes on the matrix
        :return: the current sudoku
        :rtype: Sudoku
        """
        posibles = tuple(self.available)
        old = len(posibles)
        new = -1
        while old != new:
            transverse = [[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))]
            l2 = self._remove_trivial_solution_l2(self.matrix)
            l3 = self._remove_trivial_solution_l2(transverse)
            l1 = self._remove_trivial_solution_l1(posibles)
            if l1 is None and not l2 and not l3:
                return None
            posibles = self.available
            old = new
            new = len(posibles)
        return self


class State:
    """Class in charge of represent a state of the problem. It is prepare for its use in informed and uninformed search.
    Because that, it has a attribute h representing it heuristic.

    Attributes
    _________
    sudoku Sudoku:
        Each state has a problem. In this case, the problem is a sudoku
    g: int
        The cost of the state
    h: int
        The result of the heuristic function used for this state
    """

    def __init__(self, sudoku, g=0, h=0):
        """Default contructor
        :param Sudoku sudoku: The sudoku of the state
        :param g: the cost of this state
        :param h: the heuristic of this state
        """
        self._sudoku = sudoku
        self.g = g
        self.h = h

    def __eq__(self, other: 'State') -> bool:
        """method in charge of compare two state by theirs sudokus
        :param State other: the other sudoku
        :return: if their are equals
        :rtype: bool
        """
        return self._sudoku == other.sudoku

    def __copy__(self):
        """
        Create a copy of the current state
        :return: the copy of the state
        :rtype: State
        """
        return State(self._sudoku, self.g, self.h)

    def __hash__(self):
        return hash(self._sudoku)

    @property
    def complete(self):
        """
        :return: if the current state is final or not. For that check if the empty cells of the sudoku are 0
        :rtype: bool
        """
        return len(self.sudoku) == 0

    @property
    def sudoku(self):
        """
        :return: the sudoku of the state
        :rtype: Sudoku
        """
        return self._sudoku

    @sudoku.setter
    def sudoku(self, sudoku:Sudoku) ->None:
        """
        setter to update the sudoku

        :param Sudoku sudoku: the new sudoku
        """
        self.sudoku = sudoku


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
        new_sudoku = self._state.sudoku.__copy__()

        new_sudoku = new_sudoku.remove_trivial_solution()
        new_state = State(new_sudoku, self._state.g)

        if new_sudoku is None:
            return []
        elif new_sudoku != self._state.sudoku:
            return [new_state]

        availables = new_sudoku.available
        movements = []
        pos = availables[0][0]
        for p in availables[0][1]:
            tmp_sudoku = new_sudoku.__copy__()
            tmp_sudoku[pos] = p
            tmp_state = State(tmp_sudoku, self._state.g)
            movements.append(tmp_state)

        return movements


