import heapq
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def read_maze(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file]
    return maze

def astar(maze, start, end):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))
    parent = {}
    g_score = {start: 0}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path
        closed_list.add(current)
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
                neighbor = (nx, ny)
                tentative_g_score = g_score[current] + 1
                if neighbor in closed_list and tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue
                if tentative_g_score < g_score.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_list]:
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, neighbor))
    return None

# Lee el laberinto desde el archivo
maze = read_maze("c:/Users/Dell/OneDrive - Universidad San Francisco de Quito/MESTRIA INTELIGENCIA ARTIFICIAL/Modulo 3 INTELIGENCIA ARTIFICIAL/Semana2/Taller 2/lab3.txt")


start = None
end = None
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if maze[i][j] == 'E':
            start = (i, j)
        elif maze[i][j] == 'S':
            end = (i, j)

if start is None or end is None:
    print("Error: Entrada (E) o salida (S) no encontrada en el laberinto.")
    exit()

# Resuelve el laberinto
start_time = time.time()
path = astar(maze, start, end)
end_time = time.time()

if path:
    # Crea una matriz para representar el laberinto
    maze_plot = np.zeros((len(maze), len(maze[0])))

    # Asigna colores a las celdas del laberinto
    colors = ListedColormap(['black', 'white', 'red', 'blue', 'green'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = plt.Normalize(0, 5)

    # Marca las paredes en la matriz
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                maze_plot[i][j] = 1

    # Marca la ruta en la matriz
    for x, y in path:
        maze_plot[x][y] = 2

    # Marca el inicio y fin en la matriz
    maze_plot[start[0]][start[1]] = 3
    maze_plot[end[0]][end[1]] = 4

    # Crea el gráfico
    plt.figure()
    plt.imshow(maze_plot, cmap=colors, norm=norm)
    plt.title('Laberinto')
    plt.show()

    print("Tiempo de ejecución:", end_time - start_time, "segundos")
    print("Pasos para la solución:", len(path) - 1)
else:
    print("No path found.")