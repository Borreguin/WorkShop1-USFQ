import matplotlib.pyplot as plt
import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_util import define_color


class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = None

    def load_Maze(self):
        _maze = []
        file_path = os.path.join(project_path, self.filename)
        # print("Loading Maze from", file_path)
        with open(file_path, 'r') as file:
            for line in file:
                _maze.append(list(line.strip()))
        self.maze = _maze
        return self

    def plot_maze(self):
        height = len(self.maze)
        width = len(self.maze[0])

        fig = plt.figure(figsize=(width/4, height/4))  # Ajusta el tamaño de la figura según el tamaño del Maze
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                plt.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')

        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()  # Invierte el eje y para que el origen esté en la esquina inferior izquierda
        plt.xticks([])
        plt.yticks([])
        fig.tight_layout()
        plt.show()
        return self

    def get_graph(self):
        # Implementar la creación del grafo a partir del laberinto
        return None




## esto se tiene que acoplar a get_graph
# def study_case(algorithm, maze_file):
#     print(f"This is a study case using {algorithm.__name__} on {maze_file}")
#
#     # Transformación del laberinto
#     laberinto = trasnformar_laberinto(os.path.join(project_path, maze_file))
#     reduccion_laberinto = transform_maze(copy.deepcopy(laberinto))
#     # plot_maze_before_after(laberinto, reduccion_laberinto)  # Gráfico de la matriz antes y después de la transformación
#
#     # Determinación de las posiciones de inicio y fin
#     start_position = None
#     end_position = None
#     for i, row in enumerate(reduccion_laberinto):
#         for j, val in enumerate(row):
#             if val == 'E':
#                 start_position = (i, j)
#             elif val == 'S':
#                 end_position = (i, j)
#
#     if start_position is None or end_position is None:
#         print("No se encontraron posiciones de inicio o fin en el laberinto.")
#         return
#
#     # Aplicación del algoritmo para encontrar el camino
#     path = algorithm(reduccion_laberinto, start_position, end_position)
#
#     # Marcar el camino en el laberinto
#     mark_path(reduccion_laberinto, path, start_position, end_position)
#
#     plot_maze_before_after(laberinto, reduccion_laberinto, algorithm.__name__+'-'+maze_file)  # Gráfico de la matriz con el camino marcado
