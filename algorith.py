from aux_structure import Stack
from problem_definition import Action, State


class DFS:
    def __init__(self, initial_state, max_depth):
        self.initial_state = initial_state
        self.stack = Stack()
        self.stack.append(initial_state)
        self.max_depth = max_depth
        self.end = False
        self.visited = set()

    def start(self, slow_aproach=False):
        if not slow_aproach:
            return self.__start(self.max_depth)
        else:
            c = 1
            result = None
            while c <= self.max_depth+1:
                result = self.__start(c)
                if result is None:
                    print(f"iter {c}")
                    c += 1
                    self.stack.append(self.initial_state)

                else:
                    break
        return result

    def __start(self, max_depth):
        final_state = None

        while len(self.stack) > 0 and not self.end:
            current_state = self.stack.pop()

            if current_state.complete:
                self.end = True
                final_state = current_state
                break
            if current_state.g >= max_depth:
                continue

            self.visited.add(current_state)
            action = Action(current_state)
            actions = action.get_successors()

            for posible_state in actions:
                posible_state.g = current_state.g + 1
                if posible_state not in self.visited:
                    self.stack.append(posible_state)
        return final_state



