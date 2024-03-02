import matplotlib.pyplot as plt
import os, sys
from collections import deque
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from .P1_util import define_color


class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = None

    def load_Maze(self):
        _maze = []
        file_path = os.path.join(project_path, self.filename)
        print("Loading Maze from", file_path)
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

    def dijkstra(self, graph, start, end):
        queue = [(0, start, [start])]
        visited = set()

        while queue:
            distance, current_node, path = queue.pop(0)
            if current_node == end:
                return path

            if current_node not in visited:
                visited.add(current_node)
                for neighbor in graph[current_node]:
                    if neighbor not in visited:
                        queue.append((distance + 1, neighbor, path + [neighbor]))

        return None

    def bfs(self, graph, start, end):
        queue = deque([(start, [start])])
        visited = []

        while queue:
            current_node, path = queue.popleft()

            if current_node == end:
                return path

            if current_node not in visited:
                visited.append(current_node)
                for neighbor in graph[current_node]:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def paint_graph(self, path):
        for i, j in path:
            if self.maze[i][j] != "E" and self.maze[i][j] != "S":
                self.maze[i][j] = "Y"
        self.plot_maze()

    def get_graph(self):
        graph = {}
        start_node = None
        end_node = None
        rows = len(self.maze)
        cols = len(self.maze[0])
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                value = self.maze[i][j]
                if self.maze[i][j] == "E":
                    start_node = (i,j)
                elif self.maze[i][j] == "S":
                    end_node = (i,j)

                if value != "#":
                    neighbors = []
                    # Check adjacent cells
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        new_x, new_y = i + dx, j + dy
                        if 0 <= new_x < rows and 0 <= new_y < cols and self.maze[new_x][new_y] != "#":
                            neighbors.append((new_x, new_y))
                    # Add neighbors to the graph
                    graph[(i, j)] = neighbors

        if start_node and end_node:
            shortest_path_1 = self.dijkstra(graph, start_node, end_node)
            shortest_path_2 = self.bfs(graph, start_node, end_node)
            shortest_path = None
            if len(shortest_path_1) < len(shortest_path_2):
                shortest_path = shortest_path_1
                print("Dijkstra obtiene un mejor path:", len(shortest_path_1))
            else:
                shortest_path = shortest_path_2
                print("BFS obtiene un mejor path:", len(shortest_path_2))

            if shortest_path:
                self.paint_graph(shortest_path)
            else:
                print("No path found from start to end")
        else:
            print("Start or end node not found.")

        return graph
