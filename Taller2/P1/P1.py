import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from .P1_MazeLoader import MazeLoader
import networkx as nx
import matplotlib.pyplot as plt


def study_case_1():
    print("This is study case 1")
    maze_file = 'laberinto1.txt'
    maze = MazeLoader(maze_file).load_Maze()
    # Aquí la implementación de la solución:
    graph, start, goal = maze.get_graph()
    nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
    # Assuming you've called get_graph() like this:
    

    # Depth-First Search
    dfs_tree = nx.dfs_tree(graph, source=start)
    print("DFS Tree:")
    print(list(dfs_tree.edges()))

    # Breadth-First Search
    bfs_tree = nx.bfs_tree(graph, source=start)
    print("BFS Tree:")
    print(list(bfs_tree.edges()))
    
    # Find shortest path from start to goal
    path = nx.shortest_path(graph, source=start, target=goal)
    print("Path from start to goal:")
    print(path)


def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    maze = MazeLoader(maze_file).load_Maze()
    # Aquí la implementación de la solución:
    
    graph, start, goal = maze.get_graph()
    nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
    # Assuming you've called get_graph() like this:
    

    # Depth-First Search
    dfs_tree = nx.dfs_tree(graph, source=start)
    print("DFS Tree:")
    print(list(dfs_tree.edges()))

    # Breadth-First Search
    bfs_tree = nx.bfs_tree(graph, source=start)
    print("BFS Tree:")
    print(list(bfs_tree.edges()))
    
    # Find shortest path from start to goal
    path = nx.shortest_path(graph, source=start, target=goal)
    print("Path from start to goal:")
    print(path)


def study_case_3():
    print("This is study case 3")
    maze_file = 'laberinto3.txt'
    maze = MazeLoader(maze_file).load_Maze()
    # Aquí la implementación de la solución:
    graph, start, goal = maze.get_graph()
    nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
    # Assuming you've called get_graph() like this:
    

    # Depth-First Search
    dfs_tree = nx.dfs_tree(graph, source=start)
    print("DFS Tree:")
    print(list(dfs_tree.edges()))

    # Breadth-First Search
    bfs_tree = nx.bfs_tree(graph, source=start)
    print("BFS Tree:")
    print(list(bfs_tree.edges()))
    
    # Find shortest path from start to goal
    path = nx.shortest_path(graph, source=start, target=goal)
    print("Path from start to goal:")
    print(path)


if __name__ == '__main__':
    print("path",project_path)
    study_case_2()
