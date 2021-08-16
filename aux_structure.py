class Node:
    """Clase nodo contiene la información necesaria para poder construir el arbol de decisión
    y la cola
    :atributes:
        state: El valor asignado a cada nodo. En este problema se usa la definición de estado de problem_definition.state
        nxt: El estado que le sigue en la cola
        parent: El nodo que contiene el estado que lo ha generado
    """
    def __init__(self, state, parent):
        self.state = state
        self.nxt = None
        self.parent = parent

    def __str__(self):
        return str(self.state)

class Queue:
    """Estructura de datos basada en FIFO
    :atributes:
        length: La longitud de la cola (default 0)
        peak: El último nodo insertado (default None)
        header: El primer nodo insertado (no extraido) (default None)
        current: Nodo empleado de forma auxiliar para poder iterar con el for _ in Queue (default None)
    """
    def __init__(self):
        """Constructor de la cola
        Establece los valores por defecto de los atributos necesarios"""
        self.length = 0
        self.peak = None
        self.header = None
        self.current = None

    def enqueue(self, state, parent=None):
        """metodo para añadir elementos en una cola
        :param: state: El estado que se va añadir a la cola
        :param parent: El nodo que lo ha generado
        :return: La longitud de la cola después de la insercción
        """
        nn = Node(state, parent)
        
        if self.length == 0:
            self.peak = nn
            self.header = nn
            self.current = nn
        else:
            self.peak.nxt = nn
            self.peak = nn
        self.length +=1
        return self.length

    def dequeue(self):
        """metodo para desencolar elementos
        :return: el primer nodo de la lista
        """
        if self.length == 0: return None
        nn = self.header
        self.header = self.header.nxt
        self.length -=1
        return nn

    def __iter__(self):
        return self

    def __next__(self):
        if self.length > 0 and self.current != None:
            n = self.current
            self.current = self.current.nxt
            return n
        else: 
            self.current = self.header
            raise StopIteration

class OrderQueue(Queue):
    """Estructura de datos basada en Fifo ca"""
    def __init__(self):
        """Se emplea el constructor de Queue"""
        super(OrderQueue, self).__init__()

    def order_enqueue(self, state, parent=None, heuristic = lambda state : 0):
        """metodo encargado de insertar en la cola un estado ordenado en base a la función f(state) = g(state)+h(state) con orden ascendente
        :param state: El estado a insertar
        :param parent: El nodo que contiene al estaod que lo ha generado (default None)
        :param heuristic: La heuristica empleada para la función h
        :return: La longitud actual de la cola
        """

        nn = Node(state, parent)

        #Si la cola está vacía
        if self.length == 0:
            self.header = nn
            self.peak = nn
        else:
            last = None
            current = self.header
            f = lambda state : state.g + heuristic(state)
            evaluate_f = f(state)

            #se itera en la lista hasta encontrar la posicion en la que debemos insertar el nuevo estado o hasta encontrar un nodo
            #con el mismo estado, en cullo caso, no se inserta el nuevo estado
            while f(current.state) < evaluate_f and current.nxt is not None:
                if current.state == state:
                    return
                last = current
                current = current.nxt
             
            #una vez se llegue al final de la cola o se encuentre la posicion intermedia en la que se debe realizar la insercion, se procedera a ello
            if current.nxt is None:
                self.peak.nxt = nn
                self.peak = nn
            else:
                nn.nxt = current
                if current == self.header:
                    self.header = nn
                else:
                    last.nxt = nn

        self.length +=1
        current = nn
        #comprobamos que el estado no esté con peor f
        while current.nxt is not None:
                if current.nxt.state == state:
                        if current.nxt.nxt is None:
                            self.peak = current
                        current.nxt = current.nxt.nxt
                        self.length -=1
                        break
                current = current.nxt

        return self.length

