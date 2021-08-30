from typing import Generator, Union


def get_sub_matrix(ii, jj):
    """function in charge of return the sub matrix of the current cell
    Args:
        ii: A int with the number of the row
        jj: A int with the number of the column

    Returns:
        A int with the sub matrix's number

    Raises:
        IndexError: If get invalid range of value

    """
    if 0 <= ii < 9 or 0 <= jj < 9:
        return 3*(ii//3) + jj//3
    else:
        raise IndexError("The column and the row must be in the range [0,8]")


class Sudoku:
    """Class in charge of represent a sudoku. It has the matrix with the numbers.

    Attributes
            matrix: A list[list[int]] with the matrix with the problem. The empty cells are represented as 0
    """

    def __init__(self, matrix: list[list[int]]):
        """Default constructor. Create a copy of the matrix passed by parameter

        Args:
            matrix: A list[list[int]] with the board of the game.

        Raises:
            ValueError: If the board is not a square or If detect invalid number into the board.
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

    def __getitem__(self, key: tuple[int, int]) -> int:
        """Method in charge of return the value into the cell especificate into the key parameter of the board

        Args:
            key: The position that want to know

        Returns:
            The value of this position

        Raises:
            IndexError: If get invalid cell or if the key does not have two position.
        """
        if len(key) != 2:
            raise IndexError("Invalid cell selected")
        i, j = key
        if 0 <= i < 9 and 0 <= j < 9:
            return self.matrix[i][j]
        else:
            raise IndexError("Invalid cell selected")

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """Method in charge of update the matrix
        Args:
            key: The position of the matrix that want to know. It must be a tuple of two position
            value: The new value of this position
        raises:
            ValueError: If cant set this value on this position
            IndexError If get invalid cell or if the key does not have two position.
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

    def __eq__(self, other: 'Sudoku') -> bool:
        """Method in charge of compare two sudokus. For that compare all the cells of both boards
        Args:
            other: Other instance of Sudoku's class  to be compared
        Returns:
            True if are equals otherwise False
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __copy__(self) -> 'Sudoku':
        """Method in charge of return a copy of the current sudoku
        Returns:
            The copy of the current sudoku
        """
        return Sudoku(self.matrix)

    def __str__(self) -> str:
        """Method in charge of represent as string the sudoku

        Returns:
            The sudoku representation
        """
        return "\n".join(["|".join([str(x) for x in row]) for row in self.matrix])

    def __len__(self) -> int:
        """
        Returns:
            The number of empty cells of the board
        """
        return len(list(self.empty_position))

    def __hash__(self) -> int:
        """Overwrite the original method hash to allow store a Sudoku into a set

        Returns:
            The hash value of the board

        """
        return hash((tuple(x) for x in self.matrix))

    def valid_position(self, i: int, j: int, value: int) -> bool:
        """Method in charge of check if the value can be set into the cell selected

        Args:
            i: the row to be check
            j: the column to be check
            value: the new value that want to update
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
    def empty_position(self) -> Generator[tuple[int, int], None, None]:
        """Generator of the empty cells for the board
        Returns:
            All the empty cells
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    yield i, j

    @property
    def available(self) -> list[tuple[tuple[int, int], set]]:
        """bidimensional tuple with the positions free and the availables values of that position
        order by the number of availables options on each cell

        Returns:
             The list with all the availables positions and his posibles values
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

    def _remove_trivial_solution_l1(self, posibles: list[tuple[tuple[int, int], set]] = ()) -> int:
        """Method in charge of set all the cells that only has one option available

        Args:
            posibles: the list with the cells and theirs options. If is empty, use the the list of the Sudoku
        Returns:
            A int indicate if there was some error or any changes on the matrix:
                0 -> Not changes
                1 -> changes
                2 -> Invalid sudoku
        """
        error = 0

        if not posibles:
            posibles = self.available

        for posible in posibles:
            # break the for when the number of options are more than one
            if len(posible[1]) == 1:
                try:
                    self[posible[0]] = posible[1].pop()
                    error = 1
                # If can not set the value, the current sudoku is invalid so return None to indicate that
                except ValueError:
                    error = 2
                    break
            else:
                break
        return error

    def _remove_trivial_solution_l2(self, matrix: list[list[int]]) -> bool:
        """Method in charge of set all the cell on that a value has its unique option to be set

        Args:
            matrix: the matrix to be update
        Returns:
            if the method change some cell
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

    def remove_trivial_solution(self) -> Union['Sudoku', None]:
        """Method in charge of remove trivial solution trying to reduce the empty cells of the board.
        For that use the private method _remove_trivial_solution_l2 and _remove_trivial_solution_l1 and call it while
        there are some changes on the matrix

        Returns:
            The current sudoku after update it
        """
        posibles = tuple(self.available)
        old = len(posibles)
        new = -1
        while old != new:
            l2 = self._remove_trivial_solution_l2(self.matrix)
            transverse = [[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))]
            l3 = self._remove_trivial_solution_l2(transverse)
            l1 = self._remove_trivial_solution_l1(posibles)
            if l1 == 2 and not l2 and not l3:
                return None
            posibles = self.available
            old = new
            new = len(posibles)
        return self


class State:
    """Class in charge of represent a state of the problem. It is prepare for its use in informed and uninformed search.
    Because that, it has a attribute h representing it heuristic.

    Attributes
        sudoku Each state has a problem. In this case, the problem is a Sudoku instance
        g: A int with the cost of the state
        h: A int with the result of the heuristic function used for this state
    """

    def __init__(self, sudoku: Sudoku, g: int = 0, h: int = 0):
        """
        Args:
            sudoku: The sudoku of the state
            g: the cost of this state
            h: the heuristic of this state
        """
        self._sudoku = sudoku
        self.g = g
        self.h = h

    def __eq__(self, other: 'State') -> bool:
        """method in charge of compare two state by theirs sudokus

        Args:
            other: the other state to compare

        Returns:
            If both state have the same sudoku
        """
        return self._sudoku == other.sudoku

    def __copy__(self) -> 'State':
        """Create a copy of the current state

        Returns:
            the copy of the state
        """
        return State(self._sudoku, self.g, self.h)

    def __hash__(self):
        """Overwrite the original method hash to allow store a State into a set. For that we use the hash of its sudoku

        Returns:
            The hash value of the board

        """
        return hash(self._sudoku)

    @property
    def complete(self) -> bool:
        """
        Returns:
            if the current state is final or not. For that check if the empty cells of the sudoku are 0
        """
        return len(self.sudoku) == 0

    @property
    def sudoku(self) -> Sudoku:
        """Getter of the Sudoku instance of the state

        Returns:
            the sudoku of the state
        """
        return self._sudoku

    @sudoku.setter
    def sudoku(self, sudoku: Sudoku):
        """setter to update the sudoku

        Args:
            sudoku: the new sudoku
        """
        self.sudoku = sudoku


class Action:
    """Class in charge of represent all the actions availables for one state
    Attributes:
        state: the state that can do the actions
    """
    def __init__(self, state: State):
        self._state = state

    @property
    def state(self):
        """Getter of the state property
        Returns: The state of the action
        """
        return self._state

    @state.setter
    def state(self, state: State):
        """
        Setter of the state property. Update the current state of the action instance
        Args:
            state: The new state
        """
        self._state = state

    def get_successors(self):
        """Method in charge of return all the new state availbles from the current state. Only make changes into the cell
        with less values availables.

        Returns:
            A list with the posibles news state for the first position free of the sudoku

        """
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


