import os, sys
import copy
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_MazeLoader import MazeLoader
from P1_util import trasnformar_laberinto, transform_maze, plot_maze_before_after, bfs_find_path, mark_path

def study_case_1():
    print("This is study case 2")
    maze_file = 'laberinto1.txt'
    
    # Algoritmo de Nayfeth
    laberinto = trasnformar_laberinto(os.path.join(project_path, maze_file))
    reduccion_laberinto = transform_maze(copy.deepcopy(laberinto))
    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz

    # Aplicación de BFS sobre el laberinto reducido
    start_position = None
    end_position = None
    for i, row in enumerate(reduccion_laberinto):
        for j, val in enumerate(row):
            if val == 'E':
                start_position = (i, j)
            elif val == 'S':
                end_position = (i, j)

    # Apply BFS to find the shortest path
    path = bfs_find_path(reduccion_laberinto, start_position, end_position)

    # Mark the path in the maze
    mark_path(reduccion_laberinto, path, start_position, end_position) 

    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz


    #maze = MazeLoader(maze_file).load_Maze().plot_maze()
    #graph = maze.get_graph()



def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    
    
    # Algoritmo de Nayfeth
    laberinto = trasnformar_laberinto(os.path.join(project_path, maze_file))
    reduccion_laberinto = transform_maze(copy.deepcopy(laberinto))
    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz

    # Aplicación de BFS sobre el laberinto reducido
    start_position = None
    end_position = None
    for i, row in enumerate(reduccion_laberinto):
        for j, val in enumerate(row):
            if val == 'E':
                start_position = (i, j)
            elif val == 'S':
                end_position = (i, j)

    # Apply BFS to find the shortest path
    path = bfs_find_path(reduccion_laberinto, start_position, end_position)

    # Mark the path in the maze
    mark_path(reduccion_laberinto, path, start_position, end_position)

    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz


    #maze = MazeLoader(maze_file).load_Maze().plot_maze()
    #graph = maze.get_graph()


def study_case_3():
    print("This is study case 2")
    maze_file = 'laberinto3.txt'
    
    # Algoritmo de Nayfeth
    laberinto = trasnformar_laberinto(os.path.join(project_path, maze_file))
    reduccion_laberinto = transform_maze(copy.deepcopy(laberinto))
    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz

    # Aplicación de BFS sobre el laberinto reducido
    start_position = None
    end_position = None
    for i, row in enumerate(reduccion_laberinto):
        for j, val in enumerate(row):
            if val == 'E':
                start_position = (i, j)
            elif val == 'S':
                end_position = (i, j)

    # Apply BFS to find the shortest path
    path = bfs_find_path(reduccion_laberinto, start_position, end_position)

    # Mark the path in the maze
    mark_path(reduccion_laberinto, path, start_position, end_position)

    plot_maze_before_after(laberinto, reduccion_laberinto) # Gráfico de la matriz


    #maze = MazeLoader(maze_file).load_Maze().plot_maze()
    #graph = maze.get_graph()


if __name__ == '__main__':
    study_case_3()
