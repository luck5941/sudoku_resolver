class Node:
    """Class in charge of represent a Node for the Stack, queue or list used on the program

    Attributes
    __________
    state: problem_definition.State
        the state that is contained into the node
    next: Node
        the next node on the auxiliar structure used
    """
    def __init__(self, state):
        self.state = state
        self.next = None


class Stack:
    """Class in charge of represent a classic stack.
    The stack use a LiFo i/o mode. For that purpose, use a node to get access of the next element of the stack

    Attributes
    _________
    length: int
        the length of the stack
    peak: Node
        the peak of the stack
    """

    def __init__(self):
        self.length = 0
        self.peak = None

    def __len__(self):
        """
        :rtype: int
        :return: the number of elements into the stack
        """
        return self.length

    def append(self, state):
        """Method in charge of insert a new state into the stack. It will be converted to the new peak
        :rtype: problem_definition.State
        :param problem_definition.State state: the new state to be inserted
        :return: the new length of the stack
        """
        new_node = Node(state)
        if self.length == 0:
            self.peak = new_node
        else:
            new_node.next = self.peak
            self.peak = new_node
        self.length += 1
        return self.length

    def pop(self):
        """Method in charge of get the last inserted element of the stack and update the length of the stack
        If the stack is empty return None
        :rtype: problem_definition.State
        :return: The last inserted state
        """
        if self.length == 0:
            return None
        new_node = self.peak
        self.peak = new_node.next
        self.length -= 1
        return new_node.state
