# WorkShop1-USFQ
# Taller 1 de inteligencia artificial

- **Nombre del grupo**: Grupo-1
- **Integrantes del grupo**:
  * Loor Párraga, Ricardo
  * Muenala Terán, Kuntur
  * Villacreses Zúñiga, Diego
  * Viteri Puyol, Santiago

- **Link**: [Planificación en ClickUp](https://doc.clickup.com/9013102272/d/h/8ckj1p0-33/60b3769cbaa9388)

# Taller 2 de inteligencia artificial

- **Integrantes del grupo con descripción de sus tareas**:
  * Santiago Viteri: 
    * Elaboración de algoritmos para ejercicios 1 y 2
  * Ricardo Loor: 
    * Re factorization código y documentación ejercicio 1. 
  * Diego Villacreses: 
    * Pruebas robustez código y visualización ejercicios 1 y 2.
  * Kuntur Muenala:
    * Revisión de literatura y documentación ejercicio 2.

## Problema 1: Uso de Algoritmos de Búsqueda

Se utilizarán varios algoritmos de búsqueda no informados para la solución de laberintos. A continuación se presenta los resultados encontrados por cada algoritmo. Adicionalmente se analiza cada algoritmos bajo las siguientes métricas: tiempo de ejecución y número de nodos en la solución.

### Study Case 1


![A* Solution 1](./Taller2/images/readme/a_star_1.png)


![A* Solution 1](./Taller2/images/readme/bfs_1.png)

![A* Solution 1](./Taller2/images/readme/dfs_1.png)

![A* Solution 1](./Taller2/images/readme/gbfs_1.png)

#### Tiempos de ejecucion y numero de nodos

![A* Solution 1](./Taller2/images/readme/case_1.png)

### Study Case 2

![A* Solution 1](./Taller2/images/readme/a_star_2.png)

![A* Solution 1](./Taller2/images/readme/bfs_2.png)

![A* Solution 1](./Taller2/images/readme/dfs_2.png)

![A* Solution 1](./Taller2/images/readme/gbfs_2.png)

#### Tiempos de ejecucion y numero de nodos


![A* Solution 1](./Taller2/images/readme/case_2.png)

### Study Case 3

![A* Solution 1](./Taller2/images/readme/a_star_3.png)
![A* Solution 1](./Taller2/images/readme/bfs_3.png)
![A* Solution 1](./Taller2/images/readme/dfs_3.png)
![A* Solution 1](./Taller2/images/readme/gbfs_3.png)
![A* Solution 1](./Taller2/images/readme/case_3.png)

#### Conclusiones

Como se puede observar, los resultados obtenidos al comparar los algoritmos de búsqueda en el laberinto indican que A* exhibe tiempos de ejecución más prolongados en relación con BFS y DFS en todos los casos. Esto se debe a que A* utiliza una heurística para encontrar la solución óptima. 

Por otro lado, DFS visita más nodos en comparación con los otros algoritmos debido a su enfoque de búsqueda profunda, sin garantizar lo localización de un óptimo global (cómo es particularmente notorio en el laberinto 3). Aunque A* y BFS tienden a visitar una cantidad similar de nodos, BFS permite encontrar un óptimo global pero puede ser computacionalmente inviable, mientras que A* se destaca para encontrar óptimos locales. 

Además, Greedy Best-First Search (GBFS) muestra tiempos de ejecución más bajos que A*, pero puede no garantizar la óptima solución, lo que sugiere que es una opción viable cuando la optimización no es crítica y se necesita una solución rápida. 

En conclusión, la selección del algoritmo depende de los requisitos específicos del problema, como la necesidad de optimización, el tiempo de ejecución tolerado y los recursos computacionales disponibles.

## OPTIMIZACIÓN DE COLONIAS DE HORMIGAS

Ant Colony Optimization (ACO) es una técnica de optimización inspirada en el comportamiento de las hormigas reales cuando buscan recursos para su colonia. El propósito de este algoritmo en el campo de la IA es el de simular el comportamiento de las hormigas para encontrar el mejor camino desde el nido de la colonia a la fuente de recursos.

### A. Correr la implementación planteada
En este repositorio, en `./Taller2/P2/P2_ACO.py` se presenta una implentación de este algoritmo.

#### B. ¿Qué ocurre con el segundo caso de estudio?
1. ¿Es suficiente elegir el camino con el menor tamaño?
No es sifuciente la condicion de esocger el menor camino, si no que tambien se debe maximizar el mayor camino con pheromonas dejado por la funcion que simula el camino de las hormigas
2. Cambiar el número de hormigas, cambiar los parámetros: taza de evaporación, Alpha, Beta.
Al jugar con los parametros de número de hormigas, taza de evaporación, Alpha, Beta, podemos concluir que el camino que muestra las pheromonas es importante para escoger el camino con la menor longuited, al momento de jugar con los parametros se puede concluir que existe una correlacion entre numero de hormigas y las feromonas que traazan el camino.

#### C. Describir los parámetros del modelo
¿Qué propósito tiene cada parámetro en el modelo?

* start = Es el punto inicial (x,y) donde empieza el camino que las hormigas deben recorrer a buscar.
* end = Es la posición de destino o final (x,y) del camino que las hormigas deben alcanzar.
* obstacles = Es una lista de coordenadas que representan las posiciones de los obstáculos en el laberinto, donde las hormigas no pueden cruzar.
* grid_size = Es una tupla que especifica las dimensiones del tablero de búsqueda donde las hormigas se mueven.
* num_ants = Deterimna el numero de hormigas que el algoritmo toma para realizar la busqueda. Cuantas más hormigas haya, más exploración del espacio de búsqueda se realizará, lo que puede aumentar las posibilidades de encontrar una solución óptima.
* evaporation_rate = Representa la tasa de evaporizacion de las feromonas depositadas en el camino de las hormigas. Controla la velocidad a la que las feromonas disminuyen con cada iteracion. Por lo que este parametro afecta la capacidad del algoritmo para converger hacia una solucion optima.
* alpha = Es un parámetro que controla la influencia de las feromonas en la elección del próximo movimiento de una hormiga. Un valor más alto de alpha da más peso a las feromonas en la selección del siguiente paso.
* beta = Determina la influencia de la heurística (distancia) en la elección del próximo movimiento de una hormiga. Un valor más alto de beta prioriza la distancia en la selección del siguiente paso sobre las feromonas.
* pheromones = el valor de pheromonas que queda marcado el tablero al comienzo de la busqueda. (todas las posiciones tienen igual valor de feromona al inicio del algoritmo = 1)
best_path = Es una lista de valores de tuplas (x,y) que muestran el mejor camino marcado por las feromonas.

##### Descripcion del modelo

1. **Inicialización**: Se crea una clase llamada AntColonyOptimization que toma como entrada el punto de inicio, el punto final, los obstáculos, el tamaño de la cuadrícula, el número de hormigas, la tasa de evaporación de feromonas, y los parámetros alpha y beta.

2. **Exploración de vecindario**: La función _get_neighbors calcula los vecinos válidos de una posición dada en la cuadrícula, excluyendo los obstáculos y las posiciones fuera de la cuadrícula.

3. **Selección del próximo movimiento**: La función _select_next_position selecciona el próximo movimiento de una hormiga en función de las feromonas depositadas y una heurística que tiene en cuenta la distancia al punto final.

Esta heurística tiene como objetivo guiar a las hormigas hacia las posiciones que están más cerca del punto final en la cuadrícula, lo que ayuda a explorar y explotar el espacio de búsqueda de manera más efectiva:

$$ \text{heuristic} = \dfrac{1}{\sqrt{(x_{neighbor} - x_{end})^2 + (y_{neighbor} - y_{end})^2} + 0.1}$$

La heuristica ayuda a calcular la probabilidad de visitar la siguiente posicion vecina, de esta manera las hormigas tienen más probabilidades de seleccionar movimientos que las acercan al destino en lugar de alejarlas del destino:

$$ \text{Probabilidad} = \text{pheromone}^{\alpha} \cdot \text{heuristic}^{\beta} $$

4. **Depositar feromonas**: La función _deposit_pheromones deposita feromonas en las posiciones visitadas por una hormiga.

5. **Evaporación de feromonas**: La función _evaporate_pheromones simula la evaporación gradual de feromonas en todas las posiciones de la cuadrícula.

6. **Búsqueda de la mejor ruta**: La función find_best_path itera sobre un número especificado de iteraciones, en cada una de las cuales varias hormigas exploran el entorno y depositan feromonas. En cada iteración, se actualiza el camino óptimo encontrado hasta el momento.

7. **Visualización**: La función plot se encarga de visualizar la cuadrícula con las feromonas depositadas, el punto de inicio, el punto final y el mejor camino marcado por las feromonas de las hormigas.

#### D. Pregunta de investigación:
¿Será que se puede utilizar este algoritmo para resolver el Travelling Salesman Problema (TSP)?

Si, el agoritmo de busqueda *Ant Colony Optimization* (ACO) puede usarse para dar una solucion optima para el TSP, no seria la mejor solucion sin embargo su solucion dada seria bastante buena.

El algoritmo de busqueda deposita una cantidad de feromonas inicial en cada arista de busqueda del grafo del TSP y crea hormigas virtuales moviendose de una ciudad a otra segun las reglas de porbabilidad del algoritmo. En cada paso, la hormiga selecciona su proximo movimiento basandose en la cantidad de feromona depositada en las aristas y usa una heuristica que tiene en cuenta la distancia entre las ciudades. Despues de completar su recorrido, cada hormiga deposita feromonas en las aristas que ha recorrido, con una cantidad proporcional a la calidad de su camino solucion. En cada iteracion las feromonas se evaporan en todas las aristas para evitar el estancamiento del algoritmo y promover la exploracion del espacio de búsqueda.

El algoritmo de optimización por colonia de hormigas se puede utilizar efectivamente para buscar soluciones al Problema del Viajante, y de hecho, es ha convertido en uno de los más populares y efectivos para este problema.

Stutzle, T.,Lopez, M. Dorigo, M. (2011) *A Concise Overview of Applications of Ant Colony Optimizatio*, [link](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://lopez-ibanez.eu/doc/StuLopDor2010aco-applications.pdf)