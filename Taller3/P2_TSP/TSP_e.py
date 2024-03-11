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

from math import atan2

# Add this function to your TSP class
def angle_between_points(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])

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
    def __init__(self, ciudades, distancias, heuristics: List[str], angle_deviation_threshold=0.1):
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
        self.angle_deviation_threshold = angle_deviation_threshold

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
        # Heuristic to minimize crossing paths by promoting direct paths
        if "f" in self.heuristics:
            # MTZ constraints to prevent subtours
            def mtz_constraint(model, i, j):
                
                if i != j and i != cities[0] and j != cities[0]:
                    return model.u[i] - model.u[j] + model.x[i, j] * (len(model.N) - 1) <= len(model.N) - 2
                else:
                    return pyo.Constraint.Skip
                
            # Set this threshold to the level of detour you want to allow. This can be tuned.
            self.detour_threshold = 0.00000000001

            # Linear detour penalty constraint
            def detour_penalty_rule(model, i, j, k):
                if i != j and j != k and i != k:
                    dist_ij = self.distancias[i, j]
                    dist_jk = self.distancias[j, k]
                    dist_ik = self.distancias[i, k]

                    # The idea is to enforce that going from i to j to k should not be much longer than going from i to k directly
                    return model.x[i, j] + model.x[j, k] <= 2 + (dist_ij + dist_jk - dist_ik) / self.detour_threshold
                else:
                    return pyo.Constraint.Skip

            _model.detour_penalty = pyo.Constraint(_model.N, _model.N, _model.N, rule=detour_penalty_rule)
            _model.mtz_constraint = pyo.Constraint(_model.N, _model.N, rule=mtz_constraint)


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

if __name__ == "__main__":
    # Solve the TSP problem
    print(study_case_general(n_cities = 30, 
                       heuristics = ["f"], 
                       tolerance = 0.1, 
                       time_limit = 10,
                       tee = True,
                       show_plot = False,
                       name_plot = "heuristic_f_30"))
    print(study_case_general(n_cities = 40, 
                       heuristics = ["f"], 
                       tolerance = 0.1, 
                       time_limit = 10,
                       tee = True,
                       show_plot = False,
                       name_plot = "heuristic_f_40"))
    # print(study_case_general(n_cities = 100, 
    #                    heuristics = [], 
    #                    tolerance = 0.1, 
    #                    time_limit = 10,
    #                    tee = True,
    #                    show_plot = False,
    #                    name_plot = "no_heuristic_f"))