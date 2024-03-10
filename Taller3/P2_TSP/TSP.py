import datetime as dt
from typing import List

import pandas as pd
import pyomo.environ as pyo
import re



from Taller3.P2_TSP.util import generar_ciudades_con_distancias, plotear_ruta, get_min_distance, get_max_distance, \
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

    def get_statistics(self):
        return {
            "distancia_minima_nodos": self.min_distance,
            "distancia_maxima_nodos": self.max_distance,
            "distancia_promedio_nodos": self.average_distance,
            "distancia_total_minima_posible": self.min_possible_distance,
            "distancia_total_maxima_posible": self.max_possible_distance
        }
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
        return path



    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1(n_cities = 10):
    # tal vez un loop para probar 10, 20, 30, 40, 50 ciudades?
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    heuristics = []
    tolerance = 0.20
    time_limit = 30
    tee = True
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta)
    distance = calculate_path_distance(distancias, ruta)
    statistics = tsp.get_statistics()
    statistics.update({
        "n_cities": n_cities,
        "distance": distance
    })
    return statistics



def study_case_2(with_heuristics=True):
    n_cities = 70
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    heuristics = ['limitar_funcion_objetivo'] if with_heuristics else []
    tolerance = 0.20
    time_limit = 40
    tee = True
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)
    distance = calculate_path_distance(distancias, ruta)
    statistics = tsp.get_statistics()
    statistics.update({
        "n_cities": n_cities,
        "distance": distance,
        "with_heuristics": with_heuristics
    })
    return statistics

def study_case_3(with_heuristics=True):
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    # con heuristicas
    heuristics = ['vecino_cercano'] if with_heuristics else []
    # sin heuristicas
    # heuristics = []
    tsp = TSP(ciudades, distancias, heuristics)
    tolerance = 0.2
    time_limit = 120
    tee = False
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)
    distance = calculate_path_distance(distancias, ruta)
    statistics = tsp.get_statistics()
    statistics.update({
        "n_cities": n_cities,
        "distance": distance,
        "with_heuristic": with_heuristics
    })
    return statistics

def ej1():
    # CASO DE ESTUDIO 1
    results = []
    for n in [10, 20, 30, 40, 50]:
        result = study_case_1(n)
        results.append(result)

    df = pd.DataFrame(results)
    df = df[['n_cities', 'distance', 'distancia_minima_nodos', 'distancia_maxima_nodos',
                'distancia_promedio_nodos', 'distancia_total_minima_posible', 'distancia_total_maxima_posible']]
    print(df)
    print(df.to_markdown(index=True))


def ej2():
    # CASO DE ESTUDIO 2
    # Correr study_case_2 sin heurísticas
    results_without_heuristics = study_case_2(with_heuristics=False)

    # Correr study_case_2 con heurísticas
    results_with_heuristics = study_case_2(with_heuristics=True)

    # Comparar resultados
    comparison_df = pd.DataFrame([results_without_heuristics, results_with_heuristics])
    print(comparison_df.to_markdown(index=False))

    # CASO DE ESTUDIO 3
    # study_case_3()

def ej3():
    # CASO DE ESTUDIO 3
    # Ejecutar study_case_3 sin heurística
    results_without_heuristic = study_case_3(with_heuristics=False)

    # Ejecutar study_case_3 con heurística
    results_with_heuristic = study_case_3(with_heuristics=True)

    # Crear un DataFrame con los resultados para comparar
    comparison_results = [results_without_heuristic, results_with_heuristic]
    comparison_df = pd.DataFrame(comparison_results)

    # Opcional: Reordenar las columnas si es necesario
    comparison_df = comparison_df[['n_cities', 'distance', 'with_heuristic',
                                   'distancia_minima_nodos', 'distancia_maxima_nodos',
                                   'distancia_promedio_nodos', 'distancia_total_minima_posible',
                                   'distancia_total_maxima_posible']]

    print(comparison_df.to_markdown(index=False))


if __name__ == "__main__":
    print("Se ha colocado un límite de tiempo de 30 segundos para la ejecución del modelo.")
    # Solve the TSP problem
    #ej1()

    # CASO DE ESTUDIO 2
    #ej2()

    # CASO DE ESTUDIO 3
    ej3()