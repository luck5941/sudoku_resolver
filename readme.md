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

> git clone https://github.com/luck5941/sudoku_resolver.git \
> cd sudoku_resolver


## Uso
> python3 main.py <file with the sudoku>

La carpeta test contiene un conjunto de pruebas o sudokus a resolver organizados por dificultad 

## Author
**Lucas Elvira Martín**
 - [Profile](https://github.com/luck5941)
 - [Website](https://luck5941.github.io/curriculum/)
 
##  Support
Contributions, issues, and feature requests are welcome!

Give a :star:️ if you like this project!
