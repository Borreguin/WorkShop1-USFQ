import datetime as dt
from typing import List
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
        if "sin_cruces" in self.heuristics:
            def rule_sin_cruces(model, i, j):
                if i == j:
                    return pyo.Constraint.Skip
                for k in model.N:
                    if k != i and k != j:
                        expr = model.x[i, j] + model.x[j, k] <= 1
                        return expr
                return pyo.Constraint.Skip

            _model.no_cross = pyo.Constraint(_model.N, _model.M, rule=rule_sin_cruces)

            def subtour_elimination_rule(model, i, j):
                if i != j:
                    return model.u[i] - model.u[j] + n_cities * model.x[i, j] <= n_cities - 1
                else:
                    return pyo.Constraint.Skip

            _model.subtour_elimination = pyo.Constraint(_model.U, _model.N, rule=subtour_elimination_rule)

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

        self.execution_time = dt.datetime.now() - start_time
        print(f"Tiempo de ejecución: {delta_time_mm_ss(self.execution_time)}")
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
        self.distance = calculate_path_distance(self.distancias, path)
        print("Distancia total recorrida:", self.distance)
        return path



    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1(n_cities, tolerance, time_limit, tee):
    # tal vez un loop para probar 10, 20, 30, 40, 50 ciudades?
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    heuristics = []
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta)

    return tsp, ruta


def study_case_2(n_cities, tolerance, time_limit, tee, heuristics):
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)

    tsp_sin = TSP(ciudades, distancias, [])
    ruta_sin = tsp_sin.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp_sin.plotear_resultado(ruta_sin, False)

    return tsp, ruta, tsp_sin, ruta_sin

def study_case_3(n_cities, tolerance, time_limit, tee, heuristics):
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)

    tsp_sin = TSP(ciudades, distancias, [])
    ruta_sin = tsp_sin.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp_sin.plotear_resultado(ruta_sin, False)

    return tsp, ruta, tsp_sin, ruta_sin


if __name__ == "__main__":
    print("Se ha colocado un límite de tiempo de 30 segundos para la ejecución del modelo.")
    # Solve the TSP problem
    # n_cities = [10, 20, 30, 40, 50]
    # solutions = {}
    # for n_city in n_cities:
    #     tsp, ruta = study_case_1(n_cities=n_city, tolerance=0.20, time_limit=120, tee=False)
    #     solutions[n_city] = [tsp, ruta]
    #
    # for solution in solutions:
    #     print(f"Para {solution} ciudades, tiempo: ", end='')
    #     print(solutions[solution][0].execution_time)

    '''
    Para 10 ciudades, tiempo: 0:00:00.039944
    Para 20 ciudades, tiempo: 0:00:00.404346
    Para 30 ciudades, tiempo: 0:00:05.750724
    Para 40 ciudades, tiempo: 0:00:19.522744
    Para 50 ciudades, tiempo: 0:02:00.116622
    
    Answer: Para menos de 50 ciudades, los tiempos estan bien, sin embargo
    cuando las ciudades pasan los 40, el algoritmo no logra encontrar una 
    respuesta en el tiempo marcado.
    Para estos algoritmos las rutas que marco muestran una buena aproximacion
    sin embargo, no es la solucion correcta ya que a simple vista se puede ver
    que hay mejores rutas, sin embargo las soluciones son muy buenas, 
    con respecto al tiempo de computo.
    '''

    # n_cities = [10]
    # solutions = {}
    # for n_city in n_cities:
    #     tsp, ruta = study_case_1(n_cities=n_city, tolerance=0.20, time_limit=120, tee=True)
    #     solutions[n_city] = [tsp, ruta]
    #
    # for solution in solutions:
    #     print(f"Para {solution} ciudades, tiempo: ", end='')
    #     print(solutions[solution][0].execution_time)

    '''
    Para 50 ciudades, tiempo: 0:02:00.127389

    Answer: Este parametro se utiliza para imprimir el progreso del algoritmo
    en consola mientras se ejecuta, muestra el numero de iteracion en la que va,
    el valor objetivo al que se quiere llegar, el valor actual y el gap que se
    tiene con el valor objetivo.
    Si realizamos el mismo analisis con 10 ciudades, el gap es minimo de aproximadamente
    un 15.6%, lo cual lo considera alcanzado porque esta menor a la tolerancia aplicada
    y termina la ejecucion del mismo.
    '''
    # solutions = {}
    #
    # heuristics = ['limitar_funcion_objetivo']
    # tsp, ruta, tsp_sin, ruta_sin = study_case_2(20, 0.20, 120, True, heuristics)
    # solutions['con_heuristica'] = [tsp, ruta]
    # solutions['sin_heuristica'] = [tsp_sin, ruta_sin]
    #
    # for solution in solutions:
    #     print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
    #           f"tiempo: {solutions[solution][0].execution_time}")

    '''
    Para con_heuristica, distancia: 1558.250325102994, tiempo: 0:00:40.194639
    Para sin_heuristica, distancia: 1563.6203758773668, tiempo: 0:00:40.250727
    
    Answer: En el tiempo de ejecucion notamos que no hay diferencia entre los 
    dos algoritmos, sin embargo, la distancia si es diferente, y es mejor la distancia
    con heuristica.
    
    Si le aumentamos el tiempo de computo a 120 segundos, el resultado es:
    
    Para con_heuristica, distancia: 1558.250325102994, tiempo: 0:02:00.263367
    Para sin_heuristica, distancia: 1446.9146529109034, tiempo: 0:02:00.204524
    
    Por lo que la heuristica es buena para sacar resultados mas rapidos, pero
    pierde eficacia cuando se le da mas tiempo para hacer calculos.
    
    Probamos la heuristica con pocas ciudades, y el algoritmo no encuentra una 
    respuesta ni solucion, por lo que esta heuristica no funciona para pocas ciudades.
    
    Para con_heuristica, distancia: 0, tiempo: 0:00:00.064021
    Para sin_heuristica, distancia: 771.3699844082084, tiempo: 0:00:00.346119
    
    Sin embargo, cuando probamos con mas ciudades los resultados con la heuristica
    no son tann buenos, ya que sin heuristica encuentra distancias menores.
    Los resultados adjuntos son para el calculo de 120 ciudades.
    
    Para con_heuristica, distancia: 2064.324514299455, tiempo: 0:01:59.198407
    Para sin_heuristica, distancia: 1836.8987616272466, tiempo: 0:02:00.848938
    
    '''
    # solutions = {}
    #
    # heuristics = ['vecino_cercano']
    # tsp, ruta, tsp_sin, ruta_sin = study_case_3(60, 0.10, 30, True, heuristics)
    # solutions['con_heuristica'] = [tsp, ruta]
    # solutions['sin_heuristica'] = [tsp_sin, ruta_sin]
    #
    # for solution in solutions:
    #     print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
    #           f"tiempo: {solutions[solution][0].execution_time}")

    '''
    Para con_heuristica, distancia: 1860.5849359671888, tiempo: 0:01:00.402269
    Para sin_heuristica, distancia: 1843.3138822726253, tiempo: 0:01:00.522899
    
    Answer: En este caso, el algoritmo funciona mejor sin el uso de la heuristica
    ya que encuentra una distancia menor en el mismo tiempo de ejecucion.
    
    Probamos para 120 ciudades a ver si hay una mejora, y encontramos que esta heuristica
    funciona mejor para mas ciudades ya que encuentra una distancia menor.
    
    Para con_heuristica, distancia: 1881.8523466910974, tiempo: 0:01:00.487912
    Para sin_heuristica, distancia: 2048.256820321997, tiempo: 0:01:00.893955

    Probamos para un menor tiempo de ejecucion (30 segundos) y los resultados
    son mejores, por ende llegamos a la conclusion que tuvimos con la heuristica 
    anterior, para ejecuciones mas rapidos, esta heuristica da mejores resultados.
    
    Para con_heuristica, distancia: 1399.359166137796, tiempo: 0:00:30.200888
    Para sin_heuristica, distancia: 1457.7855368285611, tiempo: 0:00:30.175974
    
    Sin embargo, esta heuristica no es buena para el problema cuando el numero de ciudades
    es menor, se intento correr el mismo algoritmo con 20 ciudades, y los resultados
    son mejores para el algoritmo sin heuristica.
    
    Para con_heuristica, distancia: 731.2632929644172, tiempo: 0:00:00.328847
    Para sin_heuristica, distancia: 726.901149719755, tiempo: 0:00:00.954094
    '''

    # solutions = {}
    #
    # heuristics = ['sin_cruces']
    # tsp, ruta, tsp_sin, ruta_sin = study_case_3(10, 0.10, 60, True, heuristics)
    # solutions['con_heuristica'] = [tsp, ruta]
    # solutions['sin_heuristica'] = [tsp_sin, ruta_sin]
    #
    # for solution in solutions:
    #     print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
    #             f"tiempo: {solutions[solution][0].execution_time}")