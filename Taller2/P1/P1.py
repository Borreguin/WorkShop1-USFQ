import os, sys
project_path = os.path.dirname(__file__)
import copy
sys.path.append(project_path)
from P1_MazeLoader import MazeLoader
from P1_util import trasnformar_laberinto, transform_maze, plot_maze_before_after, bfs_find_path, mark_path


def study_case(algorithm, maze_file):
    print(f"This is a study case using {algorithm.__name__} on {maze_file}")

    # Transformación del laberinto
    laberinto = trasnformar_laberinto(os.path.join(project_path, maze_file))
    reduccion_laberinto = transform_maze(copy.deepcopy(laberinto))
    # plot_maze_before_after(laberinto, reduccion_laberinto)  # Gráfico de la matriz antes y después de la transformación

    # Determinación de las posiciones de inicio y fin
    start_position = None
    end_position = None
    for i, row in enumerate(reduccion_laberinto):
        for j, val in enumerate(row):
            if val == 'E':
                start_position = (i, j)
            elif val == 'S':
                end_position = (i, j)

    if start_position is None or end_position is None:
        print("No se encontraron posiciones de inicio o fin en el laberinto.")
        return

    # Aplicación del algoritmo para encontrar el camino
    path = algorithm(reduccion_laberinto, start_position, end_position)

    # Marcar el camino en el laberinto
    mark_path(reduccion_laberinto, path, start_position, end_position)

    plot_maze_before_after(laberinto, reduccion_laberinto, algorithm.__name__+'-'+maze_file)  # Gráfico de la matriz con el camino marcado


if __name__ == '__main__':
    # print((Path(project_path)/'../images').isdir())
    # study_case_3()
    mazes = ['laberinto1.txt', 'laberinto2.txt', 'laberinto3.txt']
    for maze_file in mazes:
        maze = MazeLoader(maze_file).load_Maze().plot_maze()
        # graph = maze.get_graph()
        study_case(bfs_find_path, maze_file)
