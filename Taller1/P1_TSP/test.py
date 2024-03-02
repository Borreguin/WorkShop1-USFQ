import itertools
import matplotlib.pyplot as plt

# Función para calcular la distancia euclidiana entre dos ciudades
def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

# Función para calcular la longitud total de una ruta
def total_distance(path, cities):
    return sum(distance(cities[path[i]], cities[path[i + 1]]) for i in range(len(path) - 1)) + distance(cities[path[-1]], cities[path[0]])

# Ciudades de ejemplo (coordenadas x, y)
cities = [(0, 0), (1, 2), (3, 1), (5, 3),(6,5),(11,3),(9,2),(8,4),(7,6),(4,7)]

# Generar todas las posibles rutas
all_paths = itertools.permutations(range(len(cities)))

# Inicializar la mejor ruta y la distancia mínima
best_path = None
min_distance = float('inf')

# Encontrar la mejor ruta por fuerza bruta
for path in all_paths:
    current_distance = total_distance(path, cities)
    if current_distance < min_distance:
        min_distance = current_distance
        best_path = path

# Crear una lista con las ciudades en el orden de la mejor ruta
best_route_cities = [cities[i] for i in best_path]
best_route_cities.append(best_route_cities[0])  # Para cerrar el ciclo

# Mostrar el gráfico
plt.figure(figsize=(8, 6))
plt.scatter(*zip(*cities), c='red', marker='o')
plt.plot(*zip(*best_route_cities), linestyle='-', marker='o')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Mejor ruta encontrada por fuerza bruta para TSP')
plt.show()

print("Mejor ruta encontrada:", best_path)
print("Distancia mínima:", min_distance)
