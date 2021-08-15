from aux_structures import OrderQueue
from problem_definition import Action
from heuristics import *

class AStar:
    def __init__(self, sh = 2):
        """Constructor de A star. Define la lista abierta con una cola y la lista cerrada con una lista de python.
        La heuristica se escoge en base a una lista predefinida
        sh  en indice de la heuristica a emplear (default 2 || h(state) = 0)
        """
    
        #creacion de las listas abierta y cerrada que necesita A*. La implementacion de orderQueue se ha realizado en el fichero aux_structures.py
        
        self.open = OrderQueue()
        self.close = list()
        heuristics = (heuristic_1, heuristic_2, lambda ns : 0)
        if 0 <= sh < len(heuristics):
            self.heuristic = heuristics[sh]
        else:
            raise Exception("La heuristica debe estar en el rango [0, %s]" %len(heuristics))

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
        
        #la definicion de Action se ha realizado en el fichero problem_definition.py
        ac = Action()
        
       
        while self.open.length > 0 and not success:
            nn = self.open.dequeue()
            nodos_exp +=1


            #si ese nodo cumple las condiciones de ser un estado final (observaciones pendientes = transmisiones pendientes = 0), se finaliza
            #el algoritmo y se devuelve un exito. La logica del metodo is_complete esta explicada en el fichero problem_definition.py en la clase "State"
            if nn.state.is_complete:
                success = True
                break
                
            #si el nodo no es un nodo final, se añade a la lista cerrada
            self.close.append(nn.state)
            
            #se actualiza el estado actual al que se acaba de obtener de la lista abierta y se obtienen sus sucesores
            ac.set_state(nn.state) 
            sons = ac.get_successors()

            #para cada uno de los sucesores obtenidos, se realiza la verificacion de que no se encuentran ya en la lista cerrada y, se procede a su insercion en abierta.
            for s in sons:
                if s not in self.close:
                    s.g = nn.state.g+1
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

