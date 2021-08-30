# Sudoku resolver

Programa escrito en python3 encargado de resolver sudokus aplicando diversos enfoques para tratar de optimizar
la obtención del resultado esperado. Entre los diversos enfoques se encuentran:
1. Reducir el número de espacios en blanco resolviendo en un solo paso todas aquellas 
casillas que solo tengan una opción o valores que solo se puedan situar en una celda 
para una columna o fila.
2. Tratar de colocar siempre la celda que menos opciones tenga, de forma que haya más
opciones de acertar con la correcta
3. Finalmente se ha empleado un algoritmo basado en backtracking para resolver el problema
cuando las opciones 1 y 2 no resultan suficiente

## Instalación
Para poder probar el programa, solo hace falta descargar el respositorio,
el cual viene con algunos ejemplos de sudokus

```console
$ git clone https://github.com/luck5941/sudoku_resolver.git
$ cd sudoku_resolver
```

## Uso
```console
$ python3 main.py <file with the sudoku>
```

La carpeta test contiene un conjunto de pruebas o sudokus a resolver organizados por dificultad 

## Ejemplo de uso

```python
#!/usr/bin/env python

#import external libraries
from sys import argv

#import internal libraries
import problem_definition as pd
import utils
import algorithm

if __name__ == '__main__':
    if len(argv) < 2:
        name = argv[0]
        s = f"Error: use {name} <fileName> where fileName is the file with the sudoku you want to resolve\n"
        utils.p_error(s)
        exit(-1)

    #prepare the problem
    i_sudoku = pd.Sudoku(utils.read_sudoku(argv[1]))
    i_state = pd.State(i_sudoku)
    print(i_sudoku)
    
    #create a instance of the algorithm used to resolve the problem
    dfs = algorithm.DFS(i_state, len(i_sudoku) + 1)    
    final_state = dfs.start(slow_approach=False, increment=1)
    
    if final_state is not None:
        print("--------------")
        print(final_state.sudoku)
        print(final_state.g)
    else:
        print("Not solution found")
```
## Author
**Lucas Elvira Martín**
 - [Profile](https://github.com/luck5941)
 - [Website](https://luck5941.github.io/curriculum/)
 
##  Support
Contributions, issues, and feature requests are welcome!

Give a :star:️ if you like this project!
