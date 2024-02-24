# Factorial function using recursion
import random

#
# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n - 1)
#
# print(factorial(5))
#
# # Fibonacci series using recursion
# def fibonacci(n):
#     if n <= 1:
#         return n
#     else:
#         return fibonacci(n - 1) + fibonacci(n - 2)
#
# print(fibonacci(10))
#
#
# # plot parabola y = x^2
# import matplotlib.pyplot as plt
# import numpy as np
#
# def plot_parabola():
#     x = np.linspace(-10, 10, 100)
#     y = x ** 2
#     plt.plot(x, y)
#     plt.show()
# plot_parabola()
#
# # show nodes and vertices of a graph using networkx
# import networkx as nx
#
# def show_graph():
#     G = nx.Graph()
#     G.add_node(1)
#     G.add_node(2)
#     G.add_node(3)
#     G.add_node(4)
#     G.add_edge(1, 2)
#     G.add_edge(2, 3)
#     G.add_edge(3, 1)
#     G.add_edge(1, 4)
#     nx.draw(G, with_labels=True)
#     plt.show()
#
# show_graph()

# show graph with gray edges
# import networkx as nx
def plot_graph():
    G = nx.Graph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    G.add_edge(1, 4)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()


# example of TSP using networkx
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

random.seed(123)

def add_random_nodes(G, n):
    for i in range(n):
        G.add_node(i, pos=(random.random() * 10, random.random() * 10))
    return G

def calculate_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def add_edges_with_distance(G):
    for i in G.nodes():
        for j in G.nodes():
            if i != j:
                G.add_edge(i, j, weight=calculate_distance(G.nodes[i]['pos'], G.nodes[j]['pos']))
    return G

def show_path(G, path):
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        plt.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], 'r')
    plt.show()


def tsp():
    G = nx.Graph()
    G = add_random_nodes(G, 6)
    G = add_edges_with_distance(G)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True)
    plt.show()
    nodes = list(G.nodes())
    min_cost = float('inf')
    min_path = None
    n_iteration = 0
    for path in permutations(nodes):
        cost = 0
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            if G.has_edge(a, b):
                cost += G[a][b]['weight']
        if G.has_edge(path[-1], path[0]):
            cost += G[path[-1]][path[0]]['weight']
        if cost < min_cost:
            min_cost = cost
            min_path = path
        n_iteration += 1
        if n_iteration >10000:
            break
    print(min_path, min_cost)
    round_trip = min_path + (min_path[0],)
    return G, round_trip, min_cost

G, min_path, min_cost = tsp()
show_path(G, min_path)