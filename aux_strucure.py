class Node:
    def __init__(self, state, parent):
        self.state = state
        self.next = None
        self.parent = parent

    def __str__(self):
        return str(self.state)

class Queue:
    def __init__(self):
        self.length = 0
        self.peak = None
        self.header = current = None

    def enqueue(self, state, parent=None):
        nn = Node(state, parent)
        if self.length == 0:
            self.peak = nn
            self.header = nn
            self.current = nn
        else:
            self.peak.next = nn
            self.peak = nn

        self.length+=1
        return self.length

    def dequeue(self):
        if self.length == 0: return None
        nn = self.header
        self.header = nn.next
        self.length-=1
        return nn

    def __iter__(self):
        return self

    def __next__(self):
        if self.length > 0 and self.current != None:
            n = self.current
            self.current = self.current.next
            return n
        else:
            self.current = self.header
            raise StopIteration

class OrderQueue(Queue):
    def __init__(self):
        super(OrderQueue, self).__init__()

    def order_enqueue(self, state, parent=None, heuristic = lambda state : 0):
        nn = Node(State, parent)
        if self.length == 0:
            self.header = nn
            self.peak = nn
        else:
            last = None
            current = self.header
            f = lambda state: state.g + heuristic(state)
            evaluate_f = f(state)

            while f(current.state) < evaluate_f and current.next is not None:
                if current.state = state: return
                last = current
                current = current.next




        


