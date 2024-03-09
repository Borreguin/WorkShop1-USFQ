import random
import string
import math
from typing import List
import datetime as dt

from matplotlib import pyplot as plt

random.seed(123) # This fixes the seed for reproducibility

def generar_ciudades(n_cities: int):
    ciudades = {}
    for i in range(n_cities):
        ciudad = f"{random.choice(string.ascii_uppercase)}{random.randint(0,9)}"
        x = round(random.uniform(-100, 100) ,1) # Coordenada x aleatoria entre -100 y 100
        y = round(random.uniform(-100, 100), 1)  # Coordenada y aleatoria entre -100 y 100
        ciudades[ciudad] = (x, y)
    return ciudades

def calcular_distancia(ciudad1, ciudad2):
    x1, y1 = ciudad1
    x2, y2 = ciudad2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def generar_distancias(ciudades):
    distancias = {}
    for ciudad1, coord1 in ciudades.items():
        for ciudad2, coord2 in ciudades.items():
            if ciudad1 != ciudad2:
                distancia = calcular_distancia(coord1, coord2)
                distancias[(ciudad1, ciudad2)] = distancia
    return distancias

def generar_ciudades_con_distancias(n_cities: int):
    ciudades = generar_ciudades(n_cities)
    distancias = generar_distancias(ciudades)
    return ciudades, distancias

def plotear_ruta(ciudades, ruta, mostrar_anotaciones=True):
    if None in ruta:
        print("La ruta contiene valores nulos, no se encontró una solución válida.")
        return
    # Extraer coordenadas de las ciudades
    coordenadas_x = [ciudades[ciudad][0] for ciudad in ruta]
    coordenadas_y = [ciudades[ciudad][1] for ciudad in ruta]

    # Agregar la primera ciudad al final para cerrar el ciclo
    coordenadas_x.append(coordenadas_x[0])
    coordenadas_y.append(coordenadas_y[0])

    # Trama de las ubicaciones de las ciudades
    plt.figure(figsize=(8, 6))
    plt.scatter(coordenadas_x, coordenadas_y, color='blue', label='Ciudades')

    # Trama del mejor camino encontrado
    plt.plot(coordenadas_x, coordenadas_y, linestyle='-', marker='o', color='red', label='Mejor Ruta')

    if mostrar_anotaciones:
        # Anotar las letras de las ciudades
        for i, ciudad in enumerate(ruta):
            plt.text(coordenadas_x[i], coordenadas_y[i], ciudad)

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Ubicaciones de las Ciudades y Mejor Ruta')
    plt.legend()
    plt.grid(True)
    plt.show()

def get_path(edges: dict, initial_city: str, path: List[str]):
    next_node = edges.get(initial_city, None)
    if next_node is None:
        return [next_node]
    elif next_node in path:
        return path
    path.append(next_node)
    return get_path(edges, next_node, path)

def calculate_path_distance(distances: dict, path: List[str]):
    distance = 0
    for i in range(len(path) - 1):
        if path[i] is not None and path[i+1] is not None:
            distance += distances[(path[i], path[i+1])]
    return distance

def delta_time_mm_ss(delta_time: dt.timedelta):
    minutes, seconds = divmod(delta_time.seconds, 60)
    return f"{0 if minutes < 10 else ''}{minutes}:{0 if seconds < 10 else ''}{seconds}"

def get_min_distance(distances: dict):
    min_distance = min(distances.values())
    return min_distance

def get_max_distance(distances: dict):
    max_distance = max(distances.values())
    return max_distance

def get_average_distance(distances: dict):
    avg_distance = sum(distances.values()) / len(distances)
    return avg_distance

def get_best_max_distance_for_city(city:str, distances: dict):
    acc_distances = 0
    max_distance = 0
    for k, v in distances.items():
        if city in k:
            acc_distances += v
            max_distance = max(max_distance, v)
    avg_distance = acc_distances / len(distances)
    return (avg_distance + max_distance) / 2

def get_best_max_distance_for_cities(distances: dict):
    cities = list(set([city for k in distances.keys() for city in k]))
    best_max_distances = {}
    for city in cities:
        best_max_distances[city] = get_best_max_distance_for_city(city, distances)
    return best_max_distances
