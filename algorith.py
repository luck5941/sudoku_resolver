from aux_structure import Stack
import problem_definition as pd


class DFS:
    """Class in charge of build de Deep First Search algorithm to resolve the problem you indicate
    For that we use a custom stack but can be change for other one.

    Attributes:
        initial_state: A problem_definition.State. The state in which the problem start
        stack: aux_structure.Stack The stack in which all the generate states are stored
        max_depth: int the max cost of the state that can has the result of the problem
    """
    def __init__(self, initial_state: pd.State, max_depth: int):
        """
        Args:
            initial_state: problem_definition.State. the state in which the problem start
            max_depth: A int with the max cost of the state that can has the result of the problem

        Raises:
            ValueError: if the max_depth is invalid or if the initial state not match with the api especificate into problem_definition
        """
        self.initial_state = initial_state
        self.max_depth = max_depth
        if not isinstance(max_depth, int) or max_depth <= 0:
            raise ValueError("The max depth parameter must be positive number")
        if not isinstance(initial_state, pd.State):
            raise ValueError("The initial state must be type of state")
        self.stack = Stack()
        self.stack.append(initial_state)

        self._end = False
        self._action = pd.Action(initial_state)

    def start(self, slow_approach: bool = False, increment: int = 1) -> pd.State:
        """Method in charge of start the algorithm.
        If slow_approach is set as True, the algorithm take a iterative DFS with increment parameter
        representing increase of the max_depth in each iteration
        Args:
            slow_approach: A bool. If True, then the algorithm is incremental DFS.
            increment: A int with the steps of increase the max_depth.

        Returns:
            The final state with the solution or None in case of not found it
        """
        if not slow_approach:
            return self.__start(self.max_depth)
        else:
            c = increment
            result = None
            while c <= self.max_depth+1:
                result = self.__start(c)
                if result is None:
                    c += increment 
                    self.stack.append(self.initial_state)
                else:
                    break
        return result

    def __start(self, max_depth: int) -> pd.State:
        """Private method with the logic of the DFS algorithm

        Args:
            max_depth: A int with the max cost of the search, representing the deep of the graph generate
        Returns:
            The final state with the solution or None in case of not found it
        """

        final_state = None
        while len(self.stack) > 0 and not self._end:
            current_state = self.stack.pop()
            if current_state.g >= max_depth:
                continue

            self._action.state = current_state
            actions = self._action.get_successors()

            for posible_state in actions:
                posible_state.g += 1
                if posible_state.complete:
                    self._end = True
                    final_state = posible_state
                    break
                else:
                    self.stack.append(posible_state)

        return final_state



