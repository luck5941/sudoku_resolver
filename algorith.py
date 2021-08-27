from aux_structure import Stack
from problem_definition import Action, State


class DFS:
    def __init__(self, initial_state, max_depth):
        self.initial_state = initial_state
        self.stack = Stack()
        self.stack.append(initial_state)
        self.max_depth = max_depth
        self.end = False
        self.action = Action(initial_state)

    def start(self, slow_aproach=False, increment=1):
        if not slow_aproach:
            return self.__start(self.max_depth)
        else:
            c = increment
            result = None
            while c <= self.max_depth+1:
                result = self.__start(c)
                if result is None:
                    print(f"iter {c}")
                    c += increment 
                    self.stack.append(self.initial_state)

                else:
                    break
        return result

    def __start(self, max_depth):
        final_state = None
        while len(self.stack) > 0 and not self.end:
            current_state = self.stack.pop()
            print(f"{len(self.stack)} {len(current_state.sudoku)}")
            if current_state.g >= max_depth:
                continue

            self.action.state = current_state
            actions = self.action.get_successors()

            for posible_state in actions:
                posible_state.g += 1
                if posible_state.complete:
                    self.end = True
                    final_state = posible_state
                    break
                else:
                    self.stack.append(posible_state)
        return final_state



