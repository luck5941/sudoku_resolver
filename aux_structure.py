class Node:
    def __init__(self, state):
        self.state = state
        self.next = None


class Stack:
    def __init__(self):
        self.length = 0
        self.peak = None

    def __len__(self):
        return self.length

    def append(self, state):
        new_node = Node(state)
        if self.length == 0:
            self.peak = new_node
        else:
            new_node.next = self.peak
            self.peak = new_node
        self.length += 1
        return self.length

    def pop(self):
        if self.length == 0:
            return None
        new_node = self.peak
        self.peak = new_node.next
        self.length -= 1
        return new_node.state
