import numpy as np
import matplotlib.pyplot as plt
# np.random.seed(124)
from matplotlib.colors import LinearSegmentedColormap


class AntColonyOptimization:
    def __init__(self, start, end, obstacles, grid_size=(10, 10), num_ants=10, evaporation_rate=0.1, alpha=0.1,
                 beta=15):
        self.start = start
        self.end = end
        self.obstacles = obstacles
        self.grid_size = grid_size
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromones = np.ones(grid_size)
        self.best_path = None

    def _get_neighbors(self, position):
        pos_x, pos_y = position
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_x, new_y = pos_x + i, pos_y + j
                if (0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1] and
                        (new_x, new_y) != position and (new_x, new_y) not in self.obstacles):
                    neighbors.append((new_x, new_y))
        return neighbors

    def _select_next_position(self, position, visited):
        neighbors = self._get_neighbors(position)
        probabilities = []
        total = 0
        for neighbor in neighbors:
            if neighbor not in visited:
                pheromone = self.pheromones[neighbor[1], neighbor[0]]
                heuristic = 1 / (np.linalg.norm(np.array(neighbor) - np.array(self.end)) + 0.1)
                probabilities.append((neighbor, pheromone ** self.alpha * heuristic ** self.beta))
                total += pheromone ** self.alpha * heuristic ** self.beta
        if not probabilities:
            return None
        probabilities = [(pos, prob / total) for pos, prob in probabilities]
        selected = np.random.choice(len(probabilities), p=[prob for pos, prob in probabilities])
        return probabilities[selected][0]

    def _evaporate_pheromones(self):
        self.pheromones *= (1 - self.evaporation_rate)

    def _deposit_pheromones(self, path):
        for position in path:
            self.pheromones[position[1], position[0]] += 1

    def find_best_path(self, num_iterations, problem):
        for _ in range(num_iterations):
            all_paths = []
            for _ in range(self.num_ants):
                current_position = self.start
                path = [current_position]
                while current_position != self.end:
                    next_position = self._select_next_position(current_position, path)
                    if next_position is None:
                        break
                    path.append(next_position)
                    current_position = next_position
                    all_paths.append(path)

            # Escoger el mejor camino por la cantidad de feromonas depositadas
            # --------------------------------------------------------------
            # if problem == "B":

            best_path = None
            best_path_pheromones = 0
            for path in all_paths:
                path_pheromones = sum(self.pheromones[pos[1], pos[0]] for pos in path)
                if best_path is None or path_pheromones > best_path_pheromones:
                    best_path = path
                    best_path_pheromones = path_pheromones
                    # --------------------------------------------------------------

            self._evaporate_pheromones()
            self._deposit_pheromones(best_path)

            if self.best_path is None or len(best_path) <= len(self.best_path) and best_path[-1] == self.end:
                self.best_path = best_path

            # else:

            #     all_paths.sort(key=lambda x: len(x))
            #     best_path = all_paths[0]

            #     self._evaporate_pheromones()
            #     self._deposit_pheromones(best_path)

            #     if self.best_path is None or len(best_path) <= len(self.best_path) and best_path[-1] == self.end:
            #         self.best_path = best_path

    def plot(self):
        cmap = LinearSegmentedColormap.from_list('pheromone', ['white', 'green', 'red'])
        plt.figure(figsize=(8, 8))
        plt.imshow(self.pheromones, cmap=cmap, vmin=np.min(self.pheromones), vmax=np.max(self.pheromones))
        plt.colorbar(label='Pheromone intensity')
        plt.scatter(self.start[0], self.start[1], color='orange', label='Start', s=100)
        plt.scatter(self.end[0], self.end[1], color='magenta', label='End', s=100)
        for obstacle in self.obstacles:
            plt.scatter(obstacle[0], obstacle[1], color='gray', s=900, marker='s')
        if self.best_path:
            path_x, path_y = zip(*self.best_path)
            plt.plot(path_x, path_y, color='blue', label='Best Path', linewidth=3)
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.title('Ant Colony Optimization')
        plt.legend()
        plt.grid(True)
        plt.show()


def study_case_1():
    print("Start of Ant Colony Optimization - First Study Case")
    start = (0, 0)
    end = (4, 7)
    obstacles = [(1, 2), (2, 2), (3, 2)]
    aco = AntColonyOptimization(start, end, obstacles)
    aco.find_best_path(100, "A")
    aco.plot()
    print("End of Ant Colony Optimization")
    print("Best path: ", aco.best_path)


def study_case_2():
    print("Start of Ant Colony Optimization - Second Study Case")
    start = (0, 0)
    end = (4, 7)
    obstacles = [(0, 2), (1, 2), (2, 2), (3, 2)]
    aco = AntColonyOptimization(start, end, obstacles)
    aco.find_best_path(100, "B")
    aco.plot()
    print("End of Ant Colony Optimization")
    print("Best path: ", aco.best_path)


if __name__ == '__main__':
    study_case_1()

    """
    A. El caso de estudio 1 simula un escenario donde se encuentra el camino más corto desde un punto de inicio hasta un punto final en un laberinto, 
    evitando obstáculos situados en las coordenadas (1, 2), (2, 2) y (3, 2). 
    El algoritmo ACO busca encontrar esta ruta óptima utilizando una serie de hormigas virtuales que depositan feromonas en el camino, 
    lo que guía a otras hormigas a seguir rutas más cortas basadas en la intensidad de las feromonas. 
    El paso óptimo del algoritmo se relaciona con la cantidad de feromonas depositadas en la cuadrícula, 
    donde las rutas con mayores concentraciones de feromonas tienen una mayor probabilidad de ser seleccionadas por las hormigas. Hecho que se lo puede observar en su 
    grafica ya que la ruta encontrada esta marcada por un rango de color de cafe a rojo que denota una densidad de feromonas alta.

    """
    study_case_2()

    """
    B. En el segundo caso de estudio, inicialmente, no se encontraba una solución al considerar únicamente el tamaño del camino para seleccionar la mejor ruta.
    A pesar de intentar incrementar el número de iteraciones para abordar este problema utilizando el enfoque inicial, el resultado seguía siendo el mismo. 
    Sin embargo, al modificar el código para seleccionar el mejor camino basado en la cantidad de feromonas depositadas a lo largo del camino, se logró resolver este problema. 
    Este cambio permitió al algoritmo ACO encontrar una solución más efectiva al guiar a las hormigas virtuales hacia caminos más prometedores basados en la intensidad de las feromonas.

    Aqui se muestra el bloque de codigo que se modifico: 
        def find_best_path(self, num_iterations,problem):

            ...
            if problem == "B":

                best_path = None
                best_path_pheromones = 0
                for path in all_paths:
                    path_pheromones = sum(self.pheromones[pos[1], pos[0]] for pos in path)
                    if best_path is None or path_pheromones > best_path_pheromones:
                        best_path = path
                        best_path_pheromones = path_pheromones
            ...

    """
    """
    C. 
        1. start: Representa la posición de inicio del camino que las hormigas virtuales deben recorrer. Este parámetro establece el punto de partida para la búsqueda de la ruta óptima.
        2. end: Indica la posición de destino o final del camino que las hormigas deben alcanzar. Define el objetivo que el algoritmo intenta alcanzar al encontrar la ruta más corta desde el punto de inicio hasta este punto final.
        3. obstacles: Es una lista de coordenadas que representan las posiciones de los obstáculos en el laberinto. Estos obstáculos son áreas en el camino que las hormigas deben evitar al buscar la ruta óptima.
        4. grid_size: Es una tupla que especifica las dimensiones del laberinto o área de búsqueda donde las hormigas se mueven. Define el tamaño del espacio en el que se busca la ruta óptima.
        5. num_ants: Determina el número de hormigas virtuales que participan en la búsqueda de la ruta óptima. Cuantas más hormigas haya, más exploración del espacio de búsqueda se realizará, lo que puede aumentar las posibilidades de encontrar una solución óptima.
        6. evaporation_rate: Representa la tasa de evaporación de las feromonas depositadas en el camino por las hormigas. Controla la velocidad a la que las feromonas disminuyen con el tiempo, lo que afecta la capacidad del algoritmo para converger hacia una solución óptima.
        7. alpha: Es un parámetro que controla la influencia de las feromonas en la elección del próximo movimiento de una hormiga. Un valor más alto de alpha da más peso a las feromonas en la selección del siguiente paso.
        8. beta: Determina la influencia de la heurística (distancia) en la elección del próximo movimiento de una hormiga. Un valor más alto de beta prioriza la distancia en la selección del siguiente paso sobre las feromonas.

    """
    """
    D. ¿Será que se puede utilizar este algoritmo para resolver el Travelling Salesman Problema (TSP)?

    Si, ya que segun un estudio realizado por la Universidad de Sevilla se demostro como el algoritmo de Optimización por Colonias de Hormigas (ACO) se puede utilizar para resolver el Problema del Viajante (TSP) 
    Como se conoce, el TSP es un problema clásico en la optimización combinatoria, que busca encontrar la ruta más corta que visita un conjunto de ciudades exactamente una vez y regresa al punto de partida. 
    Sin embargo, debido a su complejidad computacional, encontrar la solución óptima para el TSP es difícil, especialmente para un gran número de ciudades.

    El algoritmo ACO se inspira en el comportamiento colectivo de las hormigas en la naturaleza para encontrar soluciones aproximadas al TSP y los investigadores describen su funcionalidad de la siguiente manera:

        1. Inicialmente, se deposita una cantidad de feromona en todas las aristas del grafo.
        2. Se crean varias "hormigas" virtuales que construyen soluciones moviéndose de una ciudad a otra siguiendo reglas probabilísticas.
        3. Cada hormiga construye su recorrido basándose en la cantidad de feromona depositada en las aristas y en una medida de la "visibilidad" de cada arista (inversa de la distancia).
        4. Después de completar su recorrido, cada hormiga deposita feromona en las aristas que ha recorrido, con una cantidad proporcional a la calidad de su solución.
        5. Se evapora la feromona en todas las aristas para evitar el estancamiento del algoritmo.
        6. Se repiten los pasos 2 a 5 durante un número fijo de iteraciones o hasta que se cumpla algún criterio de parada.

    Los resultados obtenidos mostraron que el algoritmo ACO fue efectivo para encontrar soluciones aproximadas al TSP y otros problemas de optimización combinatoria.
    Además, tambien se han desarollado variantes, que otorgan soluciones efectivas, del algoritmo, como el Sistema de Colonia de Hormigas (ACS), el Sistema de Hormigas Max-Min (MMAS), entre otros,
    que se adaptan a diferentes contextos y condiciones específicas del problema.

    En resumen, segun el estudio proporcionado se demuestra cómo el comportamiento de las hormigas en la naturaleza puede inspirar soluciones eficientes
    para problemas difíciles como el TSP mediante el uso de algoritmos de optimización por colonias de hormigas.

    Referencia:

        Universidad de Sevilla. "Algoritmos de Hormigas y el Problema del Viajante (TSP)." Disponible en: https://www.cs.us.es/~fsancho/Blog/posts/ACO_TSP.md

    """