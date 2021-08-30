from typing import Union

import problem_definition as pd


class Node:
    """Class in charge of represent a Node for the Stack, queue or list used on the program

    Attributes
        state: problem_definition.State the state that is contained into the node
        next: A node with  the next node on the auxiliar structure used
    """
    def __init__(self, state: pd.State):
        """Set the state of the current node
        Args:
            state: A problem_definiotion.State
        """
        self.state = state
        self.next = None


class Stack:
    """Class in charge of represent a classic stack.
    The stack use a LiFo i/o mode. For that purpose, use a node to get access of the next element of the stack

    Attributes
        length: A int with the current length of the stack
        peak: A Node representing the peak of the stack
    """

    def __init__(self):
        self.length = 0
        self.peak = None

    def __len__(self) -> int:
        """return the length of the stack"""
        return self.length

    def append(self, state) -> int:
        """Method in charge of insert a new state into the stack. It will be converted to the new peak

        Args:
            state: The problem_definition.State that must be inserted

        Returns:
            int: the new length of the stack
        """
        new_node = Node(state)
        if self.length == 0:
            self.peak = new_node
        else:
            new_node.next = self.peak
            self.peak = new_node
        self.length += 1
        return self.length

    def pop(self) -> Union[pd.State, None]:
        """Method in charge of get the last inserted element of the stack and update the length of the stack
        If the stack is empty return None
        Returns
            The last inserted state or None if the stack is empty
        """
        if self.length == 0:
            return None
        new_node = self.peak
        self.peak = new_node.next
        self.length -= 1
        return new_node.state
