import datetime as dt
from typing import List
import pyomo.environ as pyo
import re
import pandas as pd
import time

from util import generar_ciudades_con_distancias, plotear_ruta, get_min_distance, get_max_distance, \
    get_average_distance, get_best_max_distance_for_cities, delta_time_mm_ss, get_path, calculate_path_distance, calcular_distancia


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

        execution_time = delta_time_mm_ss(dt.datetime.now() - start_time)
        print(f"Tiempo de ejecución: {execution_time}")
        self.print_min_max_distances()

        # Mostrar resultados
        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            print("Ruta óptima encontrada:")
        else:
            print("No se encontró una solución óptima, la siguiente es la mejor solución encontrada:")

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
        return path, execution_time, distance

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)

    def dos_opt(self, ruta):
        """Implementación del algoritmo 2-opt para mejorar una ruta del TSP."""
        mejora = True
        while mejora:
            mejora = False
            for i in range(1, len(ruta) - 2):
                for j in range(i + 1, len(ruta)):
                    if j - i == 1: continue  # No se intercambia con aristas adyacentes
                    nueva_ruta = ruta[:i] + ruta[i:j][::-1] + ruta[j:]
                    distancia_nueva_ruta = calculate_path_distance(self.distancias, nueva_ruta)
                    distancia_ruta =calculate_path_distance(self.distancias, ruta)
                    if distancia_nueva_ruta < calculate_path_distance(self.distancias, ruta):
                        ruta = nueva_ruta
                        mejora = True
            break  # Si no hay mejora, termina el loop
        return ruta, min(distancia_nueva_ruta, distancia_ruta)
    

from matplotlib import pyplot as plt
def study_case_1():
    # tal vez un loop para probar 10, 20, 30, 40, 50 ciudades?

    # Lista para almacenar los resultados
    resultados = pd.DataFrame(columns=['Ciudades', 'Tiempo de ejecucion', 'Distancia recorrida',  'Distancia nueva ruta', 'Distancia nueva ruta (x2)'])

    for i, cities in enumerate([10, 20, 30, 40, 50, 100]):
        # Configurando el tamaño de la figura para los gráficos
    

        n_cities = cities
        ciudades, distancias = generar_ciudades_con_distancias(n_cities)
        heuristics = []
        tolerance = 0.20
        time_limit = 120
        tee = False
        tsp = TSP(ciudades, distancias, heuristics)
        ruta, tiempo_ejecucion, recorrido = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
        tsp.plotear_resultado(ruta)
        ruta_mejorada, distancia_nueva_ruta = tsp.dos_opt(ruta)
        ruta_mejorada2, distancia_nueva_ruta2 = tsp.dos_opt(ruta_mejorada)
        
        tsp.plotear_resultado(ruta_mejorada2)
        
        # Añade los resultados al DataFrame
        resultados.loc[len(resultados)] = {'Ciudades': cities, 'Tiempo de ejecucion': tiempo_ejecucion, 'Distancia recorrida': recorrido, 'Distancia nueva ruta': distancia_nueva_ruta, 'Distancia nueva ruta (x2)': distancia_nueva_ruta2}

    print(resultados)
    resultados.to_excel('resultado_A.xlsx', index=False)


def study_case_tee():
    # tee = True
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    heuristics = []
    tolerance = 0.20
    time_limit = 120
    tee = True
    tsp = TSP(ciudades, distancias, heuristics)
    ruta, tiempo_ejecucion, recorrido = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta)
    
def study_case_2():
    n_cities = 70
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)

    # Lista para almacenar los resultados
    resultados = pd.DataFrame(columns=['Heurística', 'Tiempo de ejecucion', 'Distancia recorrida'])

    for heuristica in ['limitar_funcion_objetivo', 'limitar_funcion_objetivo']:
        heuristics = [heuristica]
        tsp = TSP(ciudades, distancias, heuristics)
        tolerance = 0.20
        time_limit = 40
        tee = False
        ruta, tiempo_ejecucion, recorrido = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
        tsp.plotear_resultado(ruta, False)

        # Añade los resultados al DataFrame
        resultados.loc[len(resultados)] = {'Heurística': heuristica, 'Tiempo de ejecucion': tiempo_ejecucion, 'Distancia recorrida': recorrido}
    print(resultados)
    resultados.to_excel('resultado_C.xlsx', index=False) 


def study_case_3():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    
    # Lista para almacenar los resultados
    resultados = pd.DataFrame(columns=['Heurística', 'Tiempo de ejecucion', 'Distancia recorrida'])
    for heuristica in ['vecino_cercano', '']:
        heuristics = [heuristica]
    
        tsp = TSP(ciudades, distancias, heuristics)
        tolerance = 0.1
        time_limit = 60
        tee = True
        ruta, tiempo_ejecucion, recorrido = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
        tsp.plotear_resultado(ruta, False)

        # Añade los resultados al DataFrame
        resultados.loc[len(resultados)] = {'Heurística': heuristica, 'Tiempo de ejecucion': tiempo_ejecucion, 'Distancia recorrida': recorrido}
    print(resultados)
    resultados.to_excel('resultado_D.xlsx', index=False) 


if __name__ == "__main__":
    #print("Se ha colocado un límite de tiempo de 30 segundos para la ejecución del modelo.")
    # Solve the TSP problem
    study_case_1() #Tiempo limite 120 segundos y tolerancia 0.2 para 10, 20, 30, 40, 50, 100 ciudades y opcional
    #study_case_tee() #Prueba parámetro tee
    #study_case_2() #Prueba heuristica limitar_funcion_objetivo: restricciones que las rutas entre nodos deben estar en un intervalo
    #study_case_3() #Heuristica 2