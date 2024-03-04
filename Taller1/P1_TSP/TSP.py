from typing import List
from itertools import permutations
import math
import pandas as pd
import random

from util import generar_ciudades_con_distancias, plotear_ruta


class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    # Function to calculate distance between two points
    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Function to calculate total distance for a permutation
    def total_distance(self, data, permutation):
        total = 0
        for i in range(len(permutation) - 1):
            total += self.distance(data[permutation[i]], data[permutation[i+1]])
        return total
    
    # Function to generate m random permutations
    def random_permutations(self, input_list:list, m:int)->list:
        permutations = []
        list_length = len(input_list)
        # To avoid duplicates, we'll shuffle the list once and then sample from it
        random.shuffle(input_list)
        
        for _ in range(m):
            permutation = random.sample(input_list, list_length)
            permutations.append(tuple(permutation))
        
        return permutations
    
    # Function to generate all permutations of k cities
    def generate_permutations(self, data, k, max_n = 10, max_permutations = 100_000):
        city_names = list(data.keys())
        if len(city_names) <= max_n:
            all_permutations = permutations(city_names, k)
        else: 
            all_permutations = self.random_permutations(city_names, max_permutations)
        return all_permutations

    # Calculate total distance for all permutations of k cities
    def calculate_all_distances(self, data, k, max_n = 10, max_permutations = 100_000):
        all_permutations = self.generate_permutations(data, k, max_n, max_permutations)
        distances = {}
        for perm in all_permutations:
            distances[perm] = self.total_distance(data, perm)
        return distances

    # Wrap all functions together
    def encontrar_la_ruta_mas_corta(self, max_n = 10, max_permutations = 100_000):
        distances = self.calculate_all_distances(self.ciudades, len(self.ciudades), max_n, max_permutations)
        all_perm = []
        all_dist = []
        for perm, dist in distances.items():
            all_perm.append(perm)
            all_dist.append(dist)
        df_res = pd.DataFrame({"permutation": all_perm, "cost_value": all_dist})
        best_permutation = df_res.loc[lambda x: x.cost_value == x.cost_value.min(), "permutation"].tolist()[0]
        best_permutation = list(best_permutation)
        return best_permutation

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)
    print("Ruta original:", ciudades.keys())
    print("Mejor ruta:", ruta)


def study_case_n(n_cities = 100, max_n = 10, max_permutations = 100_000):
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    #ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta(max_n,max_permutations)
    tsp.plotear_resultado(ruta, False)
    print("Ruta original:", ciudades.keys())
    print("Mejor ruta:", ruta)

if __name__ == "__main__":
    # # Solve the TSP problem
    # print("Results for TSP of 10 cities")
    # study_case_1()

    # print()
    # print("Results for TSP of 100 cities")
    # print("Since 100! is not computable feasible we introduce a user defined max")
    # print("number of cities (n_cities), when we have more than that max, we also set a user defined value")
    # print("of how many permutations the user knows his/her computer can compute (max_permutations).")
    # print("The best permutation then is computed from max_permutations random permutations.")
    # study_case_n(n_cities =100, max_n = 10, max_permutations = 200_000)

    # print()
    # print("For curiosity lets compute best routes for 15 and cities")
    # print("Results for TSP of 15 cities")
    # study_case_n(n_cities =15, max_n = 10, max_permutations = 200_000)
    # print("Results for TSP of 25 cities")
    study_case_n(n_cities =1_000, max_n = 10, max_permutations = 400_000)