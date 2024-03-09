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

    return tsp, ruta

def study_case_3(n_cities, tolerance, time_limit, tee, heuristics):
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias, heuristics)
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)

    return tsp, ruta


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
    # tsp, ruta = study_case_2(120, 0.20, 120, True, heuristics)
    # solutions['con_heuristica'] = [tsp, ruta]
    #
    # heuristics = []
    # tsp, ruta = study_case_2(120, 0.20, 120, True, heuristics)
    # solutions['sin_heuristica'] = [tsp, ruta]
    #
    # for solution in solutions:
    #     print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
    #           f"tiempo: {solutions[solution][0].execution_time}")

    '''
    Para con_heuristica, distancia: 1558.250325102994, tiempo: 0:00:40.164015
    Para sin_heuristica, distancia: 1489.6196678078243, tiempo: 0:00:40.220753
    
    Answer: En el tiempo de ejecucion notamos que no hay diferencia entre los 
    dos algoritmos, sin embargo, la distancia si es diferente, y es mejor la distancia
    sin heuristica, por lo que podemos decir que la heuristica no es buena para este caso.
    Quiza si le aumentamos el tiempo maximo de ejecucion podriamos ver mejores resultados.
    
    Para con_heuristica, distancia: 1558.250325102994, tiempo: 0:02:00.187157
    Para sin_heuristica, distancia: 1489.6196678078243, tiempo: 0:02:00.217129
    
    Probamos poniendo un limite de 120 segundos, y nos dio el mismo resultado. Lo
    que nos da a entender que la heuristica no es buena para este problema.
    
    Probamos la heuristica con pocas ciudades, y el algoritmo no encuentra una 
    respuesta ni solucion, por lo que esta heuristica no funciona para pocas ciudades.
    
    Sin embargo, cuando probamos con mas ciudades los resultados con la heuristica
    son mejores, ya que encuentra una distancia mejor que el algoritmo sin heuristica.
    Los resultados adjuntos son para 120 ciudades.
    
    Para con_heuristica, distancia: 2064.324514299455, tiempo: 0:01:48.063817
    Para sin_heuristica, distancia: 2166.1683409945917, tiempo: 0:02:00.975900
    
    '''
    # solutions = {}
    #
    # heuristics = ['vecino_cercano']
    # tsp, ruta = study_case_3(20, 0.10, 60, True, heuristics)
    # solutions['con_heuristica'] = [tsp, ruta]
    #
    # heuristics = []
    # tsp, ruta = study_case_3(20, 0.10, 60, True, heuristics)
    # solutions['sin_heuristica'] = [tsp, ruta]
    #
    # for solution in solutions:
    #     print(f"Para {solution}, distancia: {solutions[solution][0].distance}, "
    #           f"tiempo: {solutions[solution][0].execution_time}")

    '''
    Para con_heuristica, distancia: 1860.5849359671888, tiempo: 0:01:00.385505
    Para sin_heuristica, distancia: 1896.2938227104403, tiempo: 0:01:00.616954
    
    Answer: En este caso, la heuristica si nos dio un resultado mejor, el tiempo
    de ejecucion es el mismo para los dos, sin embargo, la distancia es mejor para
    el algoritmo que usa la heuristica del vecino cercano.
    Sin embargo, esta heuristica no es buena para el problema cuando el numero de ciudades
    es menor, se intento correr el mismo algoritmo con 20 ciudades, y los resultados
    son mejores para el algoritmo sin heuristica.
    
    Para con_heuristica, distancia: 731.2632929644172, tiempo: 0:00:00.369940
    Para sin_heuristica, distancia: 698.001975055342, tiempo: 0:00:00.491536
    '''