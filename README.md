# WorkShop1-USFQ
## Taller 2 de inteligencia artificial

- **Nombre del grupo**: G5
- **Integrantes del grupo**:
  * Felipe Toscano
  * José Asitimbay
  * Brayan Lechón
  * Christian Hernandez

## 1. USO DE ALGORITMOS DE BÚSQUEDA
### A. Leer el laberinto y representarlo como un grafo

El objetivo de esta tarea es utilizar cualquier algoritmo de búsqueda para resolver los 3 laberintos propuestos, 
el reto es poder visualizar/representar los resultados, adicionalmente poder comparar al menos 2 algoritmos de búsqueda 
y mirar cómo se comportan para cada laberinto




### B. Aplicar algoritmos de búsqueda

#### Laberinto 1
![Maze1](/Taller2/images/laberinto1.png)

 - Solución con BFS

![Maze1BFS](/Taller2/images/laberinto1-solucion-bfs_find_path.png)

 - Solución con DFS

![Maze1BFS](/Taller2/images/laberinto1-solucion-dfs_find_path.png)

#### laberinto 2

![Maze1](/Taller2/images/laberinto2.png)

 - Solución con BFS

![Maze1BFS](/Taller2/images/laberinto2-solucion-bfs_find_path.png)

 - Solución con DFS

![Maze1BFS](/Taller2/images/laberinto2-solucion-dfs_find_path.png)

#### laberinto 3

![Maze1](/Taller2/images/laberinto3.png)

 - Solución con BFS

![Maze1BFS](/Taller2/images/laberinto3-solucion-bfs_find_path.png)

 - Solución con DFS

![Maze1BFS](/Taller2/images/laberinto3-solucion-dfs_find_path.png)

#### ¿Se puede establecer alguna métrica para evaluar los algoritmos en este problema?

Si, se puede establecer una métrica para evaluar los algoritmos en este problema, por ejemplo, el tiempo de ejecución, la longitud del camino, el número de nodos expandidos, entre otros.

| Algorithm | Maze | Path Length | Execution Time (seconds) |
|-----------|------|-------------|--------------------------|
| BFS       | 1    | 15          | 0.2178                   |
| DFS       | 1    | 31          | 0.2106                   |
| BFS       | 2    | 45          | 0.1912                   |
| DFS       | 2    | 69          | 0.2023                   |
| BFS       | 3    | 345         | 0.2606                   |
| DFS       | 3    | 453         | 0.2645                   |

Para este problema podemos observar que en tiempos de ejecución, el algoritmo BFS es más rápido que el algoritmo DFS, sin embargo, la diferencia no es muy significativa. Ademas,  el algoritmo DFS encuentra un camino más corto en todos los laberintos. 


## 2. OPTIMIZACIÓN DE COLONIAS DE HORMIGAS
### A. Correr la implementación planteada
En el repositorio, en la carpeta Taller2/P2/P2_ACO.py se plantea un ejemplo de este algoritmo, ejecutar el caso de estudio 1. Analizar el código.
### B. ¿Qué ocurre con el segundo caso de estudio?
Se plantea el caso de estudio 2, sin embargo, algo está mal en la selección del camino, ¿puedes arreglarlo? Pistas:
1. Al escoger el mejor camino una condición está faltando, ¿es suficiente elegir el camino con el menor tamaño?
2. Cambiar el número de hormigas, cambiar los parámetros: taza de evaporación, Alpha, Beta.
### C. Describir los parámetros del modelo
¿Qué propósito tiene cada parámetro en el modelo?
### D. Pregunta de investigación:
¿Será que se puede utilizar este algoritmo para resolver el Travelling Salesman Problema (TSP)?

si, se puede utilizar el algoritmo de colonia de hormigas para resolver el problema del vendedor viajero, ya que este algoritmo se basa en la búsqueda de caminos óptimos, y el problema del vendedor viajero consiste en encontrar el camino más corto que recorra todas las ciudades y regrese a la ciudad de origen.
ACO se aplica al TSP simulando el comportamiento de las hormigas que buscan caminos entre sus nidos y las fuentes de alimento. En el contexto del TSP, las "ciudades" actúan como los puntos que las hormigas necesitan visitar. Las hormigas exploran diferentes rutas entre las ciudades y depositan feromonas en su camino, marcando las rutas más cortas con mayor intensidad. Con el tiempo, la ruta con la mayor cantidad de feromonas tiende a ser la más corta, guiando a las futuras hormigas a seguir esa ruta.
A traves de iteraciones y la actualización constante de la información de las feromonas, el algoritmo converge hacia una solución óptima o cercana al óptimo.
