import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)

from P1_MazeLoader import MazeLoader

import matplotlib.pyplot as plt
import networkx as nx
from queue import PriorityQueue
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end_time - start_time} segundos")
        return result
    return wrapper


def count_nodes(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            print(f"Número de nodos en la solución de {func.__name__}: {len(result)}")
        else:
            print(f"No se encontró una solución para {func.__name__}")
        return result
    return wrapper

def laberinto_a_grafo(laberinto):
    rows = len(laberinto)
    cols = len(laberinto[0])

    G = nx.Graph()
    start_node = None
    target_node = None

    for i in range(rows):
        for j in range(cols):
            if laberinto[i][j] != "#":  # If it's not a wall
                node = (j, rows - 1 - i)  # Swap and invert i for horizontal layout
                G.add_node(node)

                if laberinto[i][j] == "E":
                    start_node = node
                elif laberinto[i][j] == "S":
                    target_node = node

                # Connect to adjacent nodes if not walls
                if i < rows - 1 and laberinto[i + 1][j] != "#":
                    G.add_edge(node, (j, rows - 2 - i))
                if i > 0 and laberinto[i - 1][j] != "#":
                    G.add_edge(node, (j, rows - i))
                if j < cols - 1 and laberinto[i][j + 1] != "#":
                    G.add_edge(node, (j + 1, rows - 1 - i))
                if j > 0 and laberinto[i][j - 1] != "#":
                    G.add_edge(node, (j - 1, rows - 1 - i))

    if start_node is None or target_node is None:
        raise ValueError("The maze must contain a start node (E) and a target node (S)")

    return G, start_node, target_node

def dibujar_laberinto(laberinto, solution=None):
    G, start_node, target_node = laberinto_a_grafo(laberinto)

    # Node positions (already adjusted for horizontal layout in graph creation)
    pos = {node: node for node in G.nodes()}

    # Node colors
    node_colors = ['lightblue' if node != start_node and node != target_node else 'green' if node == start_node else 'red' for node in G.nodes()]

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=int(600/len(laberinto)**1.5), font_weight='bold', font_size=9)

    # Draw the solution if provided
    if solution:
        solution_edges = list(zip(solution[:-1], solution[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=solution_edges, edge_color='orange', width=2)

    plt.axis('off')
    plt.show()

    
def heuristic(node, target):
    """
    Calcula la heurística (distancia Manhattan) entre un nodo y el nodo objetivo.

    Args:
    node: Nodo actual.
    target: Nodo objetivo.

    Returns:
    int: Distancia heurística entre los nodos.
    """
    return abs(node[0] - target[0]) + abs(node[1] - target[1])

@timeit
@count_nodes
def a_star(laberinto):
    """
    Resuelve el laberinto utilizando el algoritmo A*.

    Args:
    laberinto (list of str): La representación del laberinto como una lista de cadenas.

    Returns:
    list: Lista de nodos en el camino encontrado o None si no se encuentra solución.
    """
    G, inicio, objetivo = laberinto_a_grafo(laberinto)
    queue = PriorityQueue()
    queue.put((0, inicio))
    prev = {inicio: None}
    g_score = {node: float('inf') for node in G.nodes()}
    g_score[inicio] = 0

    while not queue.empty():
        current_cost, current_node = queue.get()

        if current_node == objetivo:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = prev[current_node]
            return path[::-1]

        for neighbor in G.neighbors(current_node):
            tentative_g_score = g_score[current_node] + 1
            if tentative_g_score < g_score[neighbor]:
                prev[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, objetivo)
                queue.put((f_score, neighbor))

    return None


@timeit
@count_nodes
def dfs(laberinto):
    """
    Resuelve el laberinto utilizando el algoritmo Depth-First Search (DFS).

    Args:
    laberinto (list of str): La representación del laberinto como una lista de cadenas.

    Returns:
    list: Lista de nodos en el camino encontrado o None si no se encuentra solución.
    """
    G, inicio, objetivo = laberinto_a_grafo(laberinto)
    visited = set()

    def dfs_rec(node):
        if node == objetivo:
            return [node]

        visited.add(node)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                path = dfs_rec(neighbor)
                if path:
                    return [node] + path

        return None

    return dfs_rec(inicio)


@timeit
@count_nodes
def bfs(laberinto):
    """
    Resuelve el laberinto utilizando el algoritmo Breadth-First Search (BFS).

    Args:
    laberinto (list of str): La representación del laberinto como una lista de cadenas.

    Returns:
    list: Lista de nodos en el camino encontrado o None si no se encuentra solución.
    """
    G, inicio, objetivo = laberinto_a_grafo(laberinto)
    queue = [inicio]
    visited = {inicio: None}

    while queue:
        current_node = queue.pop(0)

        if current_node == objetivo:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = visited[current_node]
            return path[::-1]

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                visited[neighbor] = current_node
                queue.append(neighbor)

    return None

@timeit
@count_nodes
def gbfs(laberinto):
    """
    Resuelve el laberinto utilizando el algoritmo Greedy Best First Search (GBFS).

    Args:
    laberinto (list of str): La representación del laberinto como una lista de cadenas.

    Returns:
    list: Lista de nodos en el camino encontrado o None si no se encuentra solución.
    """
    G, inicio, objetivo = laberinto_a_grafo(laberinto)
    queue = PriorityQueue()
    queue.put((0, inicio))
    prev = {inicio: None}

    while not queue.empty():
        _, current_node = queue.get()

        if current_node == objetivo:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = prev[current_node]
            return path[::-1]

        for neighbor in G.neighbors(current_node):
            if neighbor not in prev:
                prev[neighbor] = current_node
                queue.put((heuristic(neighbor, objetivo), neighbor))

    return None

def study_case_1():
    print("This is study case 1")
    maze_file = 'laberinto1.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    # Aquí la implementación de la solución:
    graph = maze.maze
    dibujar_laberinto(graph)
    solution1 = a_star(graph)
    solution2 = bfs(graph)
    solution3 = dfs(graph)
    solution4 = gbfs(graph)
    dibujar_laberinto(graph, solution1)
    dibujar_laberinto(graph, solution2)
    dibujar_laberinto(graph, solution3)
    dibujar_laberinto(graph, solution4)



def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    grafico = maze.maze
    dibujar_laberinto(grafico)
    solution1 = a_star(grafico)
    solution2 = bfs(grafico)
    solution3 = dfs(grafico)
    solution4 = gbfs(grafico)
    dibujar_laberinto(grafico, solution1)
    dibujar_laberinto(grafico, solution2)
    dibujar_laberinto(grafico, solution3)
    dibujar_laberinto(grafico, solution4)


def study_case_3():
    print("This is study case 3")
    maze_file = "laberinto3.txt"
    maze = MazeLoader(maze_file).load_Maze().plot_maze()
    grafico = maze.maze
    dibujar_laberinto(grafico)
    solution1 = a_star(grafico)
    solution2 = bfs(grafico)
    solution3 = dfs(grafico)
    solution4 = gbfs(grafico)
    dibujar_laberinto(grafico, solution1)
    dibujar_laberinto(grafico, solution2)
    dibujar_laberinto(grafico, solution3)
    dibujar_laberinto(grafico, solution4)


if __name__ == '__main__':
    study_case_1()
    study_case_2()
    study_case_3()


#Para evaluar el algoritmo....
#Contar saltos que dio
#Contar celdas que visito