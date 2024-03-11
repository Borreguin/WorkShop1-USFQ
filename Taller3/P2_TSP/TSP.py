import datetime as dt
from itertools import permutations
from typing import List
import pyomo.environ as pyo
import re
import random
import pandas as pd
import numpy as np
import time
import math

# Me aseguro que directorio del código siempre sea la carpeta en la que se encuentra el código ------ #
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
# --------------------------------------------------------------------------------------------------- #

# from Taller3.P2_TSP.util import generar_ciudades_con_distancias, plotear_ruta, get_min_distance, get_max_distance, \
#     get_average_distance, get_best_max_distance_for_cities, delta_time_mm_ss, get_path, calculate_path_distance
from util import generar_ciudades_con_distancias, plotear_ruta, get_min_distance, get_max_distance, \
    get_average_distance, get_best_max_distance_for_cities, delta_time_mm_ss, get_path, calculate_path_distance


class TSP:
    def __init__(self, ciudades, distancias, heuristics: List[str]):
        self.max_possible_distance = None
        self.min_possible_distance = None
        self.ciudades = ciudades
        self.distancias = distancias
        self.heuristics = heuristics
        self.min_distance = get_min_distance(distancias)
        self.max_distance = get_max_distance(distancias)
        self.average_distance = get_average_distance(distancias)
        self.average_distance_for_city = get_best_max_distance_for_cities(distancias)
        self.cal_min_max_distances()
        self.total_distance = 0.
        self.optimal_solution_found = None

    def cal_min_max_distances(self):
        # 1000 , 1500
        medium_low_distance = (self.min_distance + self.average_distance) / 2
        self.min_possible_distance = medium_low_distance * len(self.ciudades) * 0.35
        self.max_possible_distance = medium_low_distance * len(self.ciudades) * 0.50


    def print_min_max_distances(self):
        print(f"Distancia mínima entre nodos: {self.min_distance}")
        print(f"Distancia máxima entre nodos: {self.max_distance}")
        print(f"Distancia promedio entre nodos: {self.average_distance}")
        print(f"Distancia Total mínima posible: {self.min_possible_distance}")
        print(f"Distancia Total máxima posible: {self.max_possible_distance}")
        print(f"Heurísticas aplicadas: {self.heuristics}")

    def encontrar_la_ruta_mas_corta(self, tolerance, time_limit, tee):
        start_time = dt.datetime.now()

        _model = pyo.ConcreteModel()

        cities = list(self.ciudades.keys())
        n_cities = len(cities)


        # Sets to work with (conjuntos)
        _model.M = pyo.Set(initialize=self.ciudades.keys())
        _model.N = pyo.Set(initialize=self.ciudades.keys())

        # Index for the dummy variable u
        _model.U = pyo.Set(initialize=cities[1:])

        # Variables
        _model.x = pyo.Var(_model.N, _model.M, within=pyo.Binary)
        _model.u = pyo.Var(_model.N, bounds=(0, n_cities - 1))

        # Objetive Function: (función objetivo a minimizar)
        def obj_rule(model):
            return sum(self.distancias[i, j] * model.x[i, j] for i in model.N for j in model.M if i != j)

        _model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

        # Restricciones
        # Desde cada ciudad exactamente una arista
        def regla_una_entrada_una_salida_por_ciudad_desde(model, city_j):
            return sum(model.x[i, city_j]  for i in model.N if city_j != i) == 1

        _model.one_way_i_j = pyo.Constraint(_model.M, rule=regla_una_entrada_una_salida_por_ciudad_desde)

        # Hacia cada ciudad exactamente una arista
        def regla_una_entrada_una_salida_por_ciudad_hacia(model, city_i):
            return sum(model.x[city_i, j] for j in model.M if city_i != j) == 1

        _model.one_way_j_i = pyo.Constraint(_model.N, rule=regla_una_entrada_una_salida_por_ciudad_hacia)

        def rule_formando_path(model, i, j):
            if i != j:
                return model.u[i] - model.u[j] + model.x[i, j] * n_cities <= n_cities - 1
            else:
                # No se puede ir de una ciudad a la misma
                return pyo.Constraint.Skip

        _model.complete_path = pyo.Constraint(_model.U, _model.N, rule=rule_formando_path)

        def rule_asegurar_viaje(model, i, j):
            if i == j:
                return model.x[i, j] == 0
            return pyo.Constraint.Skip
        _model.no_self_travel = pyo.Constraint(_model.N, _model.M, rule=rule_asegurar_viaje)

        # Heurísticas:

        # Añadiendo limites a la función objetivo como una heurística
        if "limitar_funcion_objetivo" in self.heuristics:
            _model.obj_lower_bound = pyo.Constraint(expr=_model.obj >= self.min_possible_distance)
            _model.obj_upper_bound = pyo.Constraint(expr=_model.obj <= self.max_possible_distance)

        if "vecino_cercano" in self.heuristics:
            def rule_vecino_cercano(model, i, j):
                if i == j:
                    return pyo.Constraint.Skip
                expr = model.x[i,j] * self.distancias[i,j] <= self.average_distance_for_city[i]
                return expr
            _model.nearest_neighbor = pyo.Constraint(_model.N, _model.M, rule=rule_vecino_cercano)

        # Initialize empty set for dynamic constraints (optional)
        # _model.subtour_constraint = pyo.ConstraintList()



        # Resolver el modelo
        solver = pyo.SolverFactory('glpk')
        solver.options['mipgap'] = tolerance
        solver.options['tmlim'] = time_limit
        results = solver.solve(_model, tee=tee)

        execution_time = dt.datetime.now() - start_time
        print(f"Tiempo de ejecución: {delta_time_mm_ss(execution_time)}")
        self.print_min_max_distances()

        # Mostrar resultados
        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            print("Ruta óptima encontrada:")
            self.optimal_solution_found = True
        else:
            print("No se encontró una solución óptima, la siguiente es la mejor solución encontrada:")
            self.optimal_solution_found = False

        edges = dict()
        valid_paths = []
        for v in _model.component_data_objects(pyo.Var):
            if v.domain == pyo.Boolean and v.value is not None and v.value > 0:
                edge = re.search(r'\[(\w\d)*,(\w\d)*]', v.name)
                city1, city2 = edge.group(1), edge.group(2)
                key = f"{city1}_{city2}"
                # Esto evita caer en ciclos cerrados
                if key not in valid_paths:
                    valid_paths += [f"{city1}_{city2}", f"{city2}_{city1}"]
                    edges[city1] = city2

        initial_city = cities[0]
        path = get_path(edges, initial_city, [])
        path.append(path[0])
        distance = calculate_path_distance(self.distancias, path)
        print("Distancia total recorrida:", distance)
        self.total_distance = distance
        return path



    def plotear_resultado(self, 
                          ruta: List[str], 
                          mostrar_anotaciones: bool = True,
                          show_plot: bool = False,
                          name_plot: str = ""):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones, show_plot, name_plot)


    # Function to calculate distance between two points
    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Function to calculate total distance for a permutation
    def compute_total_distance(self, data, permutation):
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
    def generate_permutations(self, data, k, max_n = 9, max_permutations = 1_000_000):
        city_names = list(data.keys())
        if len(city_names) <= max_n:
            all_permutations = permutations(city_names, k)
        else: 
            all_permutations = self.random_permutations(city_names, max_permutations)
        return all_permutations

    # Calculate total distance for all permutations of k cities
    def calculate_all_distances(self, data, k, max_n = 9, max_permutations = 1_000_000):
        all_permutations = self.generate_permutations(data, k, max_n, max_permutations)
        distances = {}
        for perm in all_permutations:
            distances[perm] = self.compute_total_distance(data, perm)
        return distances

    # Wrap all functions together
    def encontrar_la_ruta_mas_corta_naive(self, max_n = 9, max_permutations = 1_000_000):
        distances = self.calculate_all_distances(self.ciudades, len(self.ciudades), max_n, max_permutations)
        all_perm = []
        all_dist = []
        for perm, dist in distances.items():
            all_perm.append(perm)
            all_dist.append(dist)
        df_res = pd.DataFrame({"permutation": all_perm, "cost_value": all_dist})
        best_permutation = df_res.loc[lambda x: x.cost_value == x.cost_value.min(), "cost_value"].tolist()[0]
        #best_permutation = list(best_permutation)
        return best_permutation



# def study_case_1():
#     # tal vez un loop para probar 10, 20, 30, 40, 50 ciudades?
#     n_cities = 10
#     ciudades, distancias = generar_ciudades_con_distancias(n_cities)
#     heuristics = []
#     tolerance = 0.20
#     time_limit = 30
#     tee = False
#     tsp = TSP(ciudades, distancias, heuristics)
#     ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
#     tsp.plotear_resultado(ruta)

# def study_case_2():
#     n_cities = 70
#     ciudades, distancias = generar_ciudades_con_distancias(n_cities)
#     # con heuristicas
#     heuristics = ['limitar_funcion_objetivo']
#     # sin heuristicas
#     # heuristics = []
#     tsp = TSP(ciudades, distancias, heuristics)
#     tolerance = 0.20
#     time_limit = 40
#     tee = True
#     ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
#     tsp.plotear_resultado(ruta, False)

# def study_case_3():
#     n_cities = 100
#     ciudades, distancias = generar_ciudades_con_distancias(n_cities)
#     # con heuristicas
#     heuristics = ['vecino_cercano']
#     # sin heuristicas
#     # heuristics = []
#     tsp = TSP(ciudades, distancias, heuristics)
#     tolerance = 0.1
#     time_limit = 60
#     tee = True
#     ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
#     tsp.plotear_resultado(ruta, False)

def study_case_general(n_cities = 10, 
                       heuristics = [], 
                       tolerance = 0.1, 
                       time_limit = 60,
                       tee = True,
                       show_plot = False,
                       name_plot = ""):
    random.seed(123)
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    if show_plot:
        tsp.plotear_resultado(ruta, False)
    if not show_plot:
        tsp.plotear_resultado(ruta, False, name_plot = name_plot)
    return tsp.total_distance, tsp.optimal_solution_found

def study_case_naive(n_cities = 10, 
                       heuristics = [], 
                       tolerance = 0.1, 
                       time_limit = 60,
                       tee = True,
                       show_plot = False,
                       name_plot = ""):
    random.seed(123)
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias, heuristics)
    distancia_recorrida = tsp.encontrar_la_ruta_mas_corta_naive()
    return distancia_recorrida



def problem_a():
    time_limit = 120
    cases = [10,20,30,40,50]
    elapsed_time = []
    total_distances = []
    optimal_solutions_found = []
    for case in cases:
        t0 = time.time()
        total_distance, optimal_solution_found = study_case_general(n_cities = case, 
                            heuristics = [], 
                            tolerance = 0.20, 
                            time_limit = time_limit,
                            tee = True,
                            show_plot = False,
                            name_plot = "problem_a_" + str(case))
        t1 = time.time()
        diff_time = np.round(t1-t0,2)

        total_distance = study_case_general(n_cities = case)

        elapsed_time.append(diff_time)
        total_distances.append(total_distance)
        optimal_solutions_found.append(optimal_solution_found)
    
    df_res = pd.DataFrame({"Total Ciudades": cases,
                           "Tiempo Ejecución": elapsed_time,
                           "Distancia Total": total_distances,
                           "Solución Óptima Encontrada": optimal_solutions_found})
    df_res.to_markdown("./results/problem_a.md", index=False)

    return df_res

def problem_a_naive():
    time_limit = 120
    cases = [10,20,30,40,50]
    elapsed_time = []
    total_distances = []
    optimal_solutions_found = []
    total_distances_naive = []
    elapsed_time_naive = []
    for case in cases:
        t0 = time.time()
        total_distance, optimal_solution_found = study_case_general(n_cities = case, 
                            heuristics = [], 
                            tolerance = 0.20, 
                            time_limit = time_limit,
                            tee = True,
                            show_plot = False,
                            name_plot = "problem_a_" + str(case))
        t1 = time.time()
        diff_time = np.round(t1-t0,2)
        elapsed_time.append(diff_time)
        total_distances.append(total_distance)
        optimal_solutions_found.append(optimal_solution_found)
        
        t0 = time.time()
        total_distance_naive = study_case_naive(n_cities = case)
        t1 = time.time()
        diff_time = np.round(t1-t0,2)
        total_distances_naive.append(total_distance_naive)
        elapsed_time_naive.append(diff_time)

    df_res = pd.DataFrame({"Total Ciudades": cases,
                           "Tiempo Ejecución - GLPK": elapsed_time,
                           "Distancia Total - GLPK": total_distances,
                           "Solución Óptima Encontrada - GLPK": optimal_solutions_found,
                           "Tiempo Ejecución - Naive": elapsed_time_naive,
                           "Distancia Total - Naive": total_distances_naive,
                           })
    df_res.to_markdown("./results/problem_a_naive.md", index=False)

    return df_res


def problem_c():
    time_limit = 120
    elapsed_time = []
    total_distances = []
    optimal_solutions_found = []
    cases  = []
    for h in [['limitar_funcion_objetivo'],[]]:
    #for h in [['limitar_funcion_objetivo']]:
        t0 = time.time()
        if len(h) == 0:
            h_name = "" 
        if len(h) > 0:
            h_name = "limit" 
        total_distance, optimal_solution_found = study_case_general(n_cities = 70, 
                            heuristics = h, 
                            tolerance = 0.20, 
                            time_limit = time_limit,
                            tee = True,
                            show_plot = False,
                            name_plot = "problem_c_heuristic_" + h_name)
        t1 = time.time()
        diff_time = np.round(t1-t0,2)
        elapsed_time.append(diff_time)
        total_distances.append(total_distance)
        optimal_solutions_found.append(optimal_solution_found)
        cases.append(h_name)
    
    df_res = pd.DataFrame({"Total Ciudades": cases,
                           "Tiempo Ejecución": elapsed_time,
                           "Distancia Total": total_distances,
                           "Solución Óptima Encontrada": optimal_solutions_found})
    df_res.to_markdown("./results/problem_c.md", index=False)

    return df_res

def problem_d():
    time_limit = 120
    elapsed_time = []
    total_distances = []
    optimal_solutions_found = []
    cases  = []
    for h in [['vecino_cercano'],[]]:
        t0 = time.time()
        if len(h) == 0:
            h_name = "" 
        if len(h) > 0:
            h_name = "vecino_cercano" 
        total_distance, optimal_solution_found = study_case_general(n_cities = 100, 
                            heuristics = h, 
                            tolerance = 0.10, 
                            time_limit = time_limit,
                            tee = True,
                            show_plot = False,
                            name_plot = "problem_d_heuristic_" + h_name)
        t1 = time.time()
        diff_time = np.round(t1-t0,2)
        elapsed_time.append(diff_time)
        total_distances.append(total_distance)
        optimal_solutions_found.append(optimal_solution_found)
        cases.append(h_name)
    
    df_res = pd.DataFrame({"Total Ciudades": cases,
                           "Tiempo Ejecución": elapsed_time,
                           "Distancia Total": total_distances,
                           "Solución Óptima Encontrada": optimal_solutions_found})
    df_res.to_markdown("./results/problem_d.md", index=False)

    return df_res

if __name__ == "__main__":
    # Solve the TSP problem
    print(problem_a())
    print(problem_a_naive())
    print(problem_c())
    print(problem_d())
