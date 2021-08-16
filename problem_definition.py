class Sudoku:
    def __init__(self, matrix):
        self.matrix = [[x for x in row] for row in matrix]
        self.transverse = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
        self.squads = [[] for _ in range(len(matrix))]
        self.missing = 0
        self.last_action = (-1, -1)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.squads[i//3+j//3].append(matrix[i][j])
                if matrix[i][j] == 0: self.missing+=1

    def available(self, n, i, j):
        if n in self.matrix[i] or n in self.transverse[j] or n in self.squads[i//3+j//3]:
            return None
        else:
            matrix = [[self.matrix[ii][jj] if i != ii or j != jj else n for jj in range(len(self.matrix[i]))] for ii in range(len(self.matrix)) ]
            return Sudoku(matrix)

    @property
    def get_missing(self):
        return self.missing

    @property
    def get_last_action(self):
        return self.last_action

    @property
    def set_last_action(self, positions):
       i, j = positions
       if 0<= i < len(self.matrix) and 0<= j < len(self.matrix[0]):
           self.last_action = (i, j)

    @property
    def decompose(self):
        return self.matrix, self.transverse, self.squads

    def __str__(self):
        s = ""
        for row in self.matrix:
            for number in row:
                s +=f"{number}|"
            s+="\n"
        return s

    def __copy__(self):
        return Sudoku(self.matrix)

    def __eq__(self,sudoku):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != sudoku.matrix[i][j]: return False
        return True



class State:
    def __init__(self, sudoku):
        self.g = 0
        self.h = 0
        self.sudoku = sudoku.__copy__()

    @property
    def is_complete(self):
        return self.sudoku.get_missing == 0


    def __eq__(self, state2):
        if  not isinstance(state2, State):
            raise Exception("state2 must be a State")
        return self.sudoku == state2.sudoku

    def __copy__(self):
        ns = State(self.sudoky)
        return ns

class Action:
    def __init__(self):
        self.state = None

    def set_state(self,state):
        self.state = state

    def get_successors(self):
        """
        method in charge of generate all the posibles succesors of the current state
        for that create a list with all the posibles new states of the the sudoku
        """
        successors = []
        print("Para este estado podemos rellenar {} huecos".format(self.state.sudoku.get_missing))
        for i in range(len(self.state.sudoku.matrix)):
            for j in range(len(self.state.sudoku.matrix[i])):
                if self.state.sudoku.matrix[i][j] == 0:
                    print(f"i vale {i} j vale {j}")
                    for n in range(1,10):
                        s = self.state.sudoku.available(n, i, j)
                        if s is not None:
                            print(s== self.state.sudoku)
                            successors.append(State(s))
        print(len(successors))
        return successors
                            

    
