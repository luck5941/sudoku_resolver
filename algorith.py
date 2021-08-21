from aux_structure import Stack, Node
from aux_structure import OrderQueue
from problem_definition import Action
from heuristics import *


class DFS: 
    def __init__(self, initial_state, max_depth):
        self.stack = Stack()
        self.stack.append(initial_state)
        self.max_depth = max_depth
        self.end = False
        self.visited = []

    def start(self):
        s = None
        while len(self.stack) > 0 and not self.end:
            new_node = self.stack.pop()
            c_state = new_node.state
            if c_state.g == self.max_depth or c_state in self.visited:
                continue
            if not c_state.sudoku.is_valid:
                continue

            print(f"lista: {len(self.stack)} faltan {len(c_state.sudoku)} coste {c_state.g}")
            self.visited.append(c_state)
            action = Action(c_state)
            actions = action.get_successors()
            for p_state in actions:
                p_state.g = c_state.g + 1
                if p_state.complete:
                    self.end = True
                    s = p_state
                    break
                elif p_state not in self.visited:
                    self.stack.append(p_state)
        return s if self.end else None


class AStar:
    def __init__(self, sh):
        """Constructor de A star. Define la lista abierta con una cola y la lista cerrada con una lista de python.
        La heuristica se escoge en base a una lista predefinida
        sh  en indice de la heuristica a emplear (default 2 || h(state) = 0)
        """

        # creacion de las listas abierta y cerrada que necesita A*. La implementacion de orderQueue se ha realizado en el fichero aux_structures.py

        self.open = OrderQueue()
        self.close = list()
        heuristics = (heuristic_1, heuristic_2, heuristic_3, lambda ns: 0)
        if 0 <= sh < len(heuristics):
            self.heuristic = heuristics[sh]
        else:
            raise Exception("La heuristica debe estar en el rango [0, %s]" % len(heuristics))

    def start(self, start_node):
        """metodo encargado de ejecturar el bucle principal de A star
        :param start_node: el primer node a expandir
        :returns:
            - El nodo en el que se alcanza la solución
            - El número de nodos expandidos
        """

        nodos_exp = 0
        success = False
        self.open.order_enqueue(start_node)
        print(self.open.length)

        while self.open.length > 0 and not success:
            nn = self.open.dequeue()
            nodos_exp += 1
            print(f"{self.open.length} {len(nn.state.sudoku)}")

            # si ese nodo cumple las condiciones de ser un estado final (observaciones pendientes = transmisiones pendientes = 0), se finaliza
            # el algoritmo y se devuelve un exito. La logica del metodo is_complete esta explicada en el fichero problem_definition.py en la clase "State"
            if nn.state.complete:
                success = True
                break

            # si el nodo no es un nodo final, se añade a la lista cerrada
            self.close.append(nn.state)

            # se actualiza el estado actual al que se acaba de obtener de la lista abierta y se obtienen sus sucesores
            ac = Action(nn.state)
            sons = ac.get_successors()

            # para cada uno de los sucesores obtenidos, se realiza la verificacion de que no se encuentran ya en la lista cerrada y, se procede a su insercion en abierta.
            for s in sons:
                if s not in self.close:
                    s.g = nn.state.g + 1
                    self.open.order_enqueue(s, nn, self.heuristic)

        return (nn, nodos_exp) if success else (None, None)


def get_path(node):
    """metodo encargado de iterar por los nodos a través de los padres
    hasta alcanzar el nodo inicial (el que no tenga padre)
    :param node: El nodo solución
    :return: Una lista con los nodos que forman el camino
    """
    back_trace = []
    while node is not None:
        back_trace.append(node.state)
        node = node.parent
    return back_trace[::-1]

