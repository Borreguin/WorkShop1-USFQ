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
![Maze1](/Taller2/images/maze1.jpg)
 - Solución con BFS
![Maze1BFS](/Taller2/images/laberinto1-solucion-bfs_find_path.png)
 - Solución con DFS
![Maze1BFS](/Taller2/images/laberinto1-solucion-dfs_find_path.png)
#### laberinto 2
![Maze1](/Taller2/images/maze1.jpg)
 - Solución con BFS
![Maze1BFS](/Taller2/images/laberinto2-solucion-bfs_find_path.png)
 - Solución con DFS
![Maze1BFS](/Taller2/images/laberinto2-solucion-dfs_find_path.png)
#### laberinto 3
![Maze1](/Taller2/images/maze1.jpg)
 - Solución con BFS
![Maze1BFS](/Taller2/images/laberinto3-solucion-bfs_find_path.png)
 - Solución con DFS
![Maze1BFS](/Taller2/images/laberinto3-solucion-dfs_find_path.png)

#### ¿Se puede establecer alguna métrica para evaluar los algoritmos en este problema?


## 2. OPTIMIZACIÓN DE COLONIAS DE HORMIGAS
### A. Correr la implementación planteada
En el repositorio, en la carpeta Taller2/P2/P2_ACO.py se plantea un ejemplo de este algoritmo, ejecutar el caso de estudio 1. Analizar el código.
### B. ¿Qué ocurre con el segundo caso de estudio?
Se plantea el caso de estudio 2, sin embargo, algo está mal en la selección del camino, ¿puedes arreglarlo? Pistas:
1. Al escoger el mejor camino una condición está faltando, ¿es suficiente elegir el camino con el menor tamaño?
2. Cambiar el número de hormigas, cambiar los parámetros: taza de evaporación, Alpha, Beta.

Lo que se realizó fue ponderar la longitud del camino con la cantidad de feromonas depositadas para obtener un puntaje más equitativo.
En lugar de elegir el camino mas corto se considera el camino con mayor cantidad de feromonas depositadas. 
Esto permite que el algoritmo explore más caminos y no se quede estancado en un mínimo local.
Por lo que se define una función de evaluación que pondera la longitud del camino con la cantidad de feromonas depositadas.
Por ejemplo un camino corto con pocas feromonas puede tener un puntaje menor que un camino largo con muchas feromonas depositadas.
### C. Describir los parámetros del modelo
¿Qué propósito tiene cada parámetro en el modelo?

num_ants: Determina la cantidad de hormigas que se utilizan para explorar el espacio de soluciones, afectando la amplitud de la búsqueda.

evaporation_rate: Es la tasa a la que se evaporan las feromonas del camino, lo que afecta cuán rápidamente el algoritmo "olvida" los caminos anteriores.

alpha: Controla la importancia relativa de la traza de feromonas en la decisión del camino a seguir por las hormigas.

beta: Determina la importancia de la información heurística (distancia al objetivo) en la decisión del camino, equilibrando la exploración y la explotación.

### D. Pregunta de investigación:
¿Será que se puede utilizar este algoritmo para resolver el Travelling Salesman Problema (TSP)?

Si es adecuado para problemas de optimización combinatoria, como el TSP, ya que es capaz de encontrar soluciones cercanas al óptimo en un tiempo razonable.
 En el contexto del TSP, las "hormigas" exploran diferentes rutas entre las ciudades, depositando feromonas en los caminos que recorren, lo que guía a las hormigas subsiguientes hacia las soluciones más prometedoras basadas en la longitud de las rutas y la cantidad de feromonas depositadas.