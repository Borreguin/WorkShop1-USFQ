from typing import List

import networkx as nx
import matplotlib.pyplot as plt

from W2.e1_bidirectional_util import bfs_routine, explore


class AdjacentNode:
    def __init__(self, vertex):
        self.vertex = vertex
        self.next = None
    def repr(self):
        return f"Node({self.vertex}) -> {self.next}"

class BidirectionalSearch:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph: List[AdjacentNode] = [None] * self.vertices
        self.src_queue = list()
        self.dest_queue = list()
        self.src_visited = [False] * self.vertices
        self.dest_visited = [False] * self.vertices
        self.src_parent = [None] * self.vertices
        self.dest_parent = [None] * self.vertices
        self.iteration = 0

    def add_edge(self, _src, _dest):
        node = AdjacentNode(_dest)
        node.next = self.graph[_src]
        self.graph[_src] = node

        node = AdjacentNode(_src)
        node.next = self.graph[_dest]
        self.graph[_dest] = node

    def bfs(self, direction='forward'):
        if direction == 'forward':
            self.src_queue, self.src_visited, self.src_parent = bfs_routine(self.src_queue, self.src_visited, self.src_parent, self.graph)
            print(f"Iteration --> {self.iteration}: {self.src_queue} {self.dest_queue}")
        elif direction == 'backward':
            self.dest_queue, self.dest_visited, self.dest_parent = bfs_routine(self.dest_queue, self.dest_visited, self.dest_parent, self.graph)
            print(f"Iteration <-- {self.iteration}: {self.src_queue} {self.dest_queue}")

    def is_intersecting(self):
        for i in range(self.vertices):
            if self.src_visited[i] and self.dest_visited[i]:
                return i
        return -1

    def print_path(self, _intersecting_node, _src, _dest):
        path = list()
        path.append(_intersecting_node)
        path = explore(path, self, _intersecting_node, _src, _dest)
        path = list(map(str, path))
        print("*****Path*****")
        print(' '.join(path))

    def bidirectional_search(self, src, dest):
        self.src_queue.append(src)
        self.src_visited[src] = True
        self.src_parent[src] = -1

        self.dest_queue.append(dest)
        self.dest_visited[dest] = True
        self.dest_parent[dest] = -1

        while self.src_queue and self.dest_queue:
            self.iteration += 1
            self.bfs(direction='forward')
            self.bfs(direction='backward')

            _intersecting_node = self.is_intersecting()
            if _intersecting_node != -1:
                print(f"Iteration {self.iteration}: Intersection at {_intersecting_node}")
                self.print_path(_intersecting_node, src, dest)
                return _intersecting_node

        return -1

def visualize(graph, iterations, src, dest, intersecting_node):
    G = nx.Graph()
    for i in range(graph.vertices):
        G.add_node(i)
        temp = graph.graph[i]
        while temp:
            G.add_edge(i, temp.vertex)
            temp = temp.next
    plt.figure(figsize=(4, 3))  # Adjust figure size
    pos_ini = nx.spring_layout(G)
    pos = dict()
    for node, p in pos_ini.items():
        pos[node] = p*10
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=100)
    nx.draw_networkx_nodes(G, pos, nodelist=[src], node_color='green', node_size=100)
    nx.draw_networkx_nodes(G, pos, nodelist=[dest], node_color='red', node_size=100)
    path = list()
    if intersecting_node != -1:
        path.append(intersecting_node)
        path = explore(path, graph, intersecting_node, src, dest)
        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2)

    plt.title('Bidirectional Search Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Visited Nodes')
    plt.xticks(range(1, iterations + 1))
    plt.yticks(range(graph.vertices))
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    n = 15 # Number of vertices in graph
    src = 0
    dest = 14

    graph = BidirectionalSearch(n)
    graph.add_edge(0, 4)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(3, 5)
    graph.add_edge(4, 6)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(7, 8)
    graph.add_edge(8, 9)
    graph.add_edge(8, 10)
    graph.add_edge(9, 11)
    graph.add_edge(9, 12)
    graph.add_edge(10, 13)
    graph.add_edge(10, 14)

    intersecting_node = graph.bidirectional_search(src, dest)

    if intersecting_node == -1:
        print(f"Path does not exist between {src} and {dest}")

    visualize(graph, graph.iteration, src, dest, intersecting_node)
