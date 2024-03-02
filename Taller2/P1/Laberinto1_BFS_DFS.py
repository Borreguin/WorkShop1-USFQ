import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time

# Transformar el laberinto en un grafo (lista de adyacencia)
def laberinto_a_grafo(laberinto):
    graph = {}
    rows = len(laberinto)
    cols = len(laberinto[0])
    
    for i in range(rows):
        for j in range(cols):
            if laberinto[i][j] == 0:
                neighbors = []
                if i > 0 and laberinto[i-1][j] == 0:
                    neighbors.append((i-1, j))
                if i < rows-1 and laberinto[i+1][j] == 0:
                    neighbors.append((i+1, j))
                if j > 0 and laberinto[i][j-1] == 0:
                    neighbors.append((i, j-1))
                if j < cols-1 and laberinto[i][j+1] == 0:
                    neighbors.append((i, j+1))
                graph[(i, j)] = neighbors
    
    return graph

# Búsqueda en anchura
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                queue.append((neighbor, path + [neighbor]))
    
    return None

# Búsqueda en profundidad
def dfs(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start == goal:
        return [start]
    for next_node in graph[start]:
        if next_node not in visited:
            path = dfs(graph, next_node, goal, visited)
            if path:
                return [start] + path
    return None

# Visualización del laberinto y los caminos encontrados
def dibujar_laberinto(laberinto, path=None):
    img = np.array(laberinto)
    plt.imshow(img, cmap='binary')
    if path:
        path = np.array(path)
        plt.plot(path[:, 1], path[:, 0], marker='o', color='r')
    plt.show()

import time

# Función para medir el tiempo de ejecución de un algoritmo
def medir_tiempo(algoritmo, *args):
    inicio = time.time()
    resultado = algoritmo(*args)
    tiempo_transcurrido = time.time() - inicio
    return resultado, tiempo_transcurrido

# Ejemplo de uso
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

graph = laberinto_a_grafo(laberinto)
start = (1, 1)
goal = (7, 9)
print("Laberinto:")
dibujar_laberinto(laberinto)
print("Búsqueda en anchura:")
path_bfs = bfs(graph, start, goal)
dibujar_laberinto(laberinto, path_bfs)
print("Búsqueda en profundidad:")
path_dfs = dfs(graph, start, goal)
dibujar_laberinto(laberinto, path_dfs)

# Medir el tiempo de ejecución de BFS
path_bfs, tiempo_bfs = medir_tiempo(bfs, graph, start, goal)
print(f"Tiempo de ejecución de BFS: {tiempo_bfs:.6f} segundos")
dibujar_laberinto(laberinto, path_bfs)

# Medir el tiempo de ejecución de DFS
path_dfs, tiempo_dfs = medir_tiempo(dfs, graph, start, goal)
print(f"Tiempo de ejecución de DFS: {tiempo_dfs:.6f} segundos")
dibujar_laberinto(laberinto, path_dfs)

# Calcula la distancia recorrida en el camino encontrado por BFS
distancia_bfs = len(path_bfs) - 1  # Restamos 1 porque la longitud del camino es el número de nodos visitados - 1
print(f"Distancia recorrida por BFS: {distancia_bfs}")

# Calcula la distancia recorrida en el camino encontrado por DFS
distancia_dfs = len(path_dfs) - 1  # Restamos 1 porque la longitud del camino es el número de nodos visitados - 1
print(f"Distancia recorrida por DFS: {distancia_dfs}")