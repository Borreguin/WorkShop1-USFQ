import datetime as dt
from typing import List
import pyomo.environ as pyo
import re
import os
#%pip3 install pyomo
from util import generar_ciudades_con_distancias, plotear_ruta, get_min_distance, get_max_distance, \
    get_average_distance, get_best_max_distance_for_cities, delta_time_mm_ss, get_path, calculate_path_distance
from pyomo.environ import SolverFactory

# Specify the path to the GLPK solver executable
glpk_path = "/Users/victorviteri/anaconda3/bin/glpsol"

# Create a solver instance and specify the solver executable
solver = SolverFactory('glpk', executable=glpk_path)

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


def study_case_1(n_cities_list):
    for n_cities in n_cities_list:
        ciudades, distancias = generar_ciudades_con_distancias(n_cities)
        heuristics = []
        tolerance = 0.20
        time_limit = 120
        tee = True
        tsp = TSP(ciudades, distancias, heuristics)
        print(f"Ejecutando caso para {n_cities} ciudades...")
        tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)

def study_case_2():
    n_cities = 70
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    # con heuristicas
    heuristics = ['limitar_funcion_objetivo']
    #sin heuristicas
    heuristics = []
    tsp = TSP(ciudades, distancias, heuristics)
    tolerance = 0.20
    time_limit = 40
    tee = False
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)

def study_case_3():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    # con heuristicas
    heuristics = ['vecino_cercano']
    # sin heuristicas
    heuristics = []
    tsp = TSP(ciudades, distancias, heuristics)
    tolerance = 0.1
    time_limit = 60
    tee = False
    ruta = tsp.encontrar_la_ruta_mas_corta(tolerance, time_limit, tee)
    tsp.plotear_resultado(ruta, False)


if __name__ == "__main__":
    os.getcwd()
    new_directory = '/Users/victorviteri/Documents/MAESTRIA/INTELIGENCIA ARTIFICIAL/Taller3_p2/'
    os.chdir(new_directory)
    print("Se ha colocado un límite de tiempo de 120 segundos para la ejecución del modelo.")

    # A. Study Case 1
    n_cities_list = [10, 20, 30, 40, 50]
    print("A. Ejecutando caso 1 para diferentes números de ciudades...")
    study_case_1(n_cities_list)
    
    """
        A. Ejecutando caso 1 para diferentes números de ciudades...
        
        Ejecutando caso para 10 ciudades...
        Tiempo de ejecución: 00:00
        Distancia mínima entre nodos: 11.20580206857144
        Distancia máxima entre nodos: 185.56249621084538
        Distancia promedio entre nodos: 104.55942429465665
        Distancia Total mínima posible: 202.58914613564914
        Distancia Total máxima posible: 289.4130659080702
        Heurísticas aplicadas: []
        No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
        Distancia total recorrida: 623.9958637928893
        
        Ejecutando caso para 20 ciudades...
        Tiempo de ejecución: 00:00
        Distancia mínima entre nodos: 2.920616373302048
        Distancia máxima entre nodos: 236.34426161851275
        Distancia promedio entre nodos: 102.06474994406953
        Distancia Total mínima posible: 349.07634300526047
        Distancia Total máxima posible: 498.680490007515
        Heurísticas aplicadas: []
        No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
        Distancia total recorrida: 724.4641682835669
        
        Ejecutando caso para 30 ciudades...
        Tiempo de ejecución: 00:18
        Distancia mínima entre nodos: 3.0066592756745814
        Distancia máxima entre nodos: 244.75293665245368
        Distancia promedio entre nodos: 109.44645540071214
        Distancia Total mínima posible: 551.0202619142949
        Distancia Total máxima posible: 787.1718027347071
        Heurísticas aplicadas: []
        No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
        Distancia total recorrida: 995.1582504415477
        
        Ejecutando caso para 40 ciudades...
        Tiempo de ejecución: 01:52
        Distancia mínima entre nodos: 5.360037313302962
        Distancia máxima entre nodos: 227.2084725532919
        Distancia promedio entre nodos: 103.69515077180543
        Distancia Total mínima posible: 725.2170007659707
        Distancia Total máxima posible: 1036.0242868085297
        Heurísticas aplicadas: []
        No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
        Distancia total recorrida: 1129.835948251177
        
        Ejecutando caso para 50 ciudades...
        Tiempo de ejecución: 02:00
        Distancia mínima entre nodos: 2.0615528128088343
        Distancia máxima entre nodos: 254.00545269737816
        Distancia promedio entre nodos: 111.39524957749006
        Distancia Total mínima posible: 953.0371400785106
        Distancia Total máxima posible: 1361.4816286835867
        Heurísticas aplicadas: []
        No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
        Distancia total recorrida: 1318.4510337557929
    
    """
    # R: Como se puede observar las soluciones obtenidas varian dependiendo
    #    del tamaño de las ciudades y la configuración específica del problema(entre mas ciudads mayor tiempo de ejecucion).
    #    En general, el TSP es un problema NP-duro, lo que significa que encontrar la solución óptima puede ser computacionalmente costoso, especialmente para un gran número de ciudades. 
    #    Sin embargo, el modelo proporciona una solución factible que en ningun caso es la optimo pero que se encuentra dentro del tiempo límite especificado.

    # B. Study Case 2
    print("\nB. Analizando el parámetro tee...")
    n_cities_list = [10, 20, 30, 40, 50]
    print("A. Ejecutando caso 1 para diferentes números de ciudades...")
    study_case_1(n_cities_list)
    
    """
    B. Analizando el parámetro tee...
    Ejecutando caso 1 para diferentes números de ciudades...
    Ejecutando caso para 10 ciudades...
    GLPSOL--GLPK LP/MIP Solver 5.0
    Parameter(s) specified in the command line:
     --mipgap 0.2 --tmlim 120 --write /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpzo14txf2.glpk.raw
     --wglp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmph442_g6w.glpk.glp
     --cpxlp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpfsgojecx.pyomo.lp
    Reading problem data from '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpfsgojecx.pyomo.lp'...
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpfsgojecx.pyomo.lp:976: warning: lower bound of variable 'x204' redefined
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpfsgojecx.pyomo.lp:976: warning: upper bound of variable 'x204' redefined
    111 rows, 110 columns, 433 non-zeros
    100 integer variables, all of which are binary
    1076 lines were read
    Writing problem data to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmph442_g6w.glpk.glp'...
    858 lines were written
    GLPK Integer Optimizer 5.0
    111 rows, 110 columns, 433 non-zeros
    100 integer variables, all of which are binary
    Preprocessing...
    101 rows, 100 columns, 423 non-zeros
    90 integer variables, all of which are binary
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  1.000e+01  ratio =  1.000e+01
    Problem data seem to be well scaled
    Constructing initial basis...
    Size of triangular part is 100
    Solving LP relaxation...
    GLPK Simplex Optimizer 5.0
    101 rows, 100 columns, 423 non-zeros
          0: obj =   1.651397278e+03 inf =   1.070e+02 (19)
         25: obj =   1.253776989e+03 inf =   3.331e-16 (0)
    *    64: obj =   2.779032596e+02 inf =   5.551e-15 (0)
    OPTIMAL LP SOLUTION FOUND
    Integer optimization begins...
    Long-step dual simplex will be used
    +    64: mip =     not found yet >=              -inf        (1; 0)
    +   126: >>>>>   4.935020560e+02 >=   2.779032596e+02  43.7% (12; 0)
    +   141: mip =   4.935020560e+02 >=   4.200379359e+02  14.9% (14; 1)
    RELATIVE MIP GAP TOLERANCE REACHED; SEARCH TERMINATED
    Time used:   0.0 secs
    Memory used: 0.3 Mb (270312 bytes)
    Writing MIP solution to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpzo14txf2.glpk.raw'...
    230 lines were written
    Tiempo de ejecución: 00:00
    Distancia mínima entre nodos: 6.9641941385920525
    Distancia máxima entre nodos: 161.10099316888147
    Distancia promedio entre nodos: 100.31183574879365
    Distancia Total mínima posible: 187.73305230292496
    Distancia Total máxima posible: 268.19007471846425
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 493.5020559873251
    
    Ejecutando caso para 20 ciudades...
    GLPSOL--GLPK LP/MIP Solver 5.0
    Parameter(s) specified in the command line:
     --mipgap 0.2 --tmlim 120 --write /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpr5d4x788.glpk.raw
     --wglp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpyfqfzs1l.glpk.glp
     --cpxlp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmptvhchilb.pyomo.lp
    Reading problem data from '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmptvhchilb.pyomo.lp'...
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmptvhchilb.pyomo.lp:3550: warning: lower bound of variable 'x726' redefined
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmptvhchilb.pyomo.lp:3550: warning: upper bound of variable 'x726' redefined
    381 rows, 380 columns, 1675 non-zeros
    361 integer variables, all of which are binary
    3911 lines were read
    Writing problem data to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpyfqfzs1l.glpk.glp'...
    3162 lines were written
    GLPK Integer Optimizer 5.0
    381 rows, 380 columns, 1675 non-zeros
    361 integer variables, all of which are binary
    Preprocessing...
    362 rows, 361 columns, 1656 non-zeros
    342 integer variables, all of which are binary
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  1.900e+01  ratio =  1.900e+01
    GM: min|aij| =  8.862e-01  max|aij| =  1.128e+00  ratio =  1.273e+00
    EQ: min|aij| =  8.271e-01  max|aij| =  1.000e+00  ratio =  1.209e+00
    2N: min|aij| =  1.000e+00  max|aij| =  1.188e+00  ratio =  1.188e+00
    Constructing initial basis...
    Size of triangular part is 361
    Solving LP relaxation...
    GLPK Simplex Optimizer 5.0
    362 rows, 361 columns, 1656 non-zeros
          0: obj =   1.913501430e+03 inf =   1.382e+02 (37)
         55: obj =   1.960743085e+03 inf =   2.220e-16 (0)
    *   147: obj =   7.079032835e+02 inf =   4.283e-15 (0) 1
    OPTIMAL LP SOLUTION FOUND
    Integer optimization begins...
    Long-step dual simplex will be used
    +   147: mip =     not found yet >=              -inf        (1; 0)
    +   489: >>>>>   1.276352639e+03 >=   7.117307775e+02  44.2% (55; 0)
    +   856: >>>>>   1.148375147e+03 >=   7.127848671e+02  37.9% (115; 1)
    +  1012: >>>>>   9.877429663e+02 >=   7.127848671e+02  27.8% (120; 24)
    +  3493: >>>>>   8.937946959e+02 >=   7.510315751e+02  16.0% (345; 129)
    +  3493: mip =   8.937946959e+02 >=   7.510315751e+02  16.0% (204; 395)
    RELATIVE MIP GAP TOLERANCE REACHED; SEARCH TERMINATED
    Time used:   0.5 secs
    Memory used: 1.2 Mb (1289061 bytes)
    Writing MIP solution to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpr5d4x788.glpk.raw'...
    770 lines were written
    Tiempo de ejecución: 00:00
    Distancia mínima entre nodos: 6.382005954243544
    Distancia máxima entre nodos: 226.23582828544204
    Distancia promedio entre nodos: 106.93309993584006
    Distancia Total mínima posible: 376.77272708452796
    Distancia Total máxima posible: 538.2467529778971
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 893.7946959027036
    
    Ejecutando caso para 30 ciudades...
    GLPSOL--GLPK LP/MIP Solver 5.0
    Parameter(s) specified in the command line:
     --mipgap 0.2 --tmlim 120 --write /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmp7wa7w8sa.glpk.raw
     --wglp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpi0uxuml3.glpk.glp
     --cpxlp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmphyqrh_as.pyomo.lp
    Reading problem data from '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmphyqrh_as.pyomo.lp'...
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmphyqrh_as.pyomo.lp:7198: warning: lower bound of variable 'x1462' redefined
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmphyqrh_as.pyomo.lp:7198: warning: upper bound of variable 'x1462' redefined
    757 rows, 756 columns, 3459 non-zeros
    729 integer variables, all of which are binary
    7927 lines were read
    Writing problem data to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpi0uxuml3.glpk.glp'...
    6434 lines were written
    GLPK Integer Optimizer 5.0
    757 rows, 756 columns, 3459 non-zeros
    729 integer variables, all of which are binary
    Preprocessing...
    730 rows, 729 columns, 3432 non-zeros
    702 integer variables, all of which are binary
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  2.700e+01  ratio =  2.700e+01
    GM: min|aij| =  8.736e-01  max|aij| =  1.145e+00  ratio =  1.310e+00
    EQ: min|aij| =  8.086e-01  max|aij| =  1.000e+00  ratio =  1.237e+00
    2N: min|aij| =  5.000e-01  max|aij| =  1.688e+00  ratio =  3.375e+00
    Constructing initial basis...
    Size of triangular part is 729
    Solving LP relaxation...
    GLPK Simplex Optimizer 5.0
    730 rows, 729 columns, 3432 non-zeros
          0: obj =   4.320590858e+03 inf =   1.877e+02 (53)
         74: obj =   2.925718984e+03 inf =   0.000e+00 (0)
    *   211: obj =   7.431583649e+02 inf =   0.000e+00 (0) 2
    OPTIMAL LP SOLUTION FOUND
    Integer optimization begins...
    Long-step dual simplex will be used
    +   211: mip =     not found yet >=              -inf        (1; 0)
    +   893: >>>>>   9.540224218e+02 >=   7.447631044e+02  21.9% (61; 1)
    +  1576: >>>>>   9.105407707e+02 >=   7.573147661e+02  16.8% (89; 46)
    +  1576: mip =   9.105407707e+02 >=   7.573147661e+02  16.8% (69; 85)
    RELATIVE MIP GAP TOLERANCE REACHED; SEARCH TERMINATED
    Time used:   0.4 secs
    Memory used: 1.6 Mb (1729719 bytes)
    Writing MIP solution to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmp7wa7w8sa.glpk.raw'...
    1522 lines were written
    Tiempo de ejecución: 00:00
    Distancia mínima entre nodos: 5.742821606144489
    Distancia máxima entre nodos: 242.8266871659703
    Distancia promedio entre nodos: 103.61645717752354
    Distancia Total mínima posible: 516.7225922528314
    Distancia Total máxima posible: 738.1751317897592
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 910.540770696015
    
    Ejecutando caso para 40 ciudades...
    GLPSOL--GLPK LP/MIP Solver 5.0
    Parameter(s) specified in the command line:
     --mipgap 0.2 --tmlim 120 --write /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpsnzwavhu.glpk.raw
     --wglp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpzzkkvqyk.glpk.glp
     --cpxlp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpobg41e6c.pyomo.lp
    Reading problem data from '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpobg41e6c.pyomo.lp'...
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpobg41e6c.pyomo.lp:12832: warning: lower bound of variable 'x2596' redefined
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpobg41e6c.pyomo.lp:12832: warning: upper bound of variable 'x2596' redefined
    1333 rows, 1332 columns, 6231 non-zeros
    1296 integer variables, all of which are binary
    14128 lines were read
    Writing problem data to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpzzkkvqyk.glpk.glp'...
    11492 lines were written
    GLPK Integer Optimizer 5.0
    1333 rows, 1332 columns, 6231 non-zeros
    1296 integer variables, all of which are binary
    Preprocessing...
    1297 rows, 1296 columns, 6195 non-zeros
    1260 integer variables, all of which are binary
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  3.600e+01  ratio =  3.600e+01
    GM: min|aij| =  8.633e-01  max|aij| =  1.158e+00  ratio =  1.342e+00
    EQ: min|aij| =  7.938e-01  max|aij| =  1.000e+00  ratio =  1.260e+00
    2N: min|aij| =  5.000e-01  max|aij| =  1.125e+00  ratio =  2.250e+00
    Constructing initial basis...
    Size of triangular part is 1296
    Solving LP relaxation...
    GLPK Simplex Optimizer 5.0
    1297 rows, 1296 columns, 6195 non-zeros
          0: obj =   5.174291692e+03 inf =   2.765e+02 (71)
        145: obj =   2.986012132e+03 inf =   6.908e-16 (0) 1
    *   420: obj =   7.624786157e+02 inf =   4.910e-15 (0) 2
    OPTIMAL LP SOLUTION FOUND
    Integer optimization begins...
    Long-step dual simplex will be used
    +   420: mip =     not found yet >=              -inf        (1; 0)
    +  1044: >>>>>   1.191029036e+03 >=   7.647585518e+02  35.8% (68; 0)
    +  5709: >>>>>   1.117773343e+03 >=   7.877137629e+02  29.5% (458; 10)
    + 11666: >>>>>   1.109682592e+03 >=   8.107870610e+02  26.9% (825; 131)
    + 12306: >>>>>   1.061479143e+03 >=   8.123266009e+02  23.5% (862; 164)
    + 14016: >>>>>   1.025995803e+03 >=   8.141670325e+02  20.6% (854; 410)
    + 14543: >>>>>   9.985681659e+02 >=   8.143567437e+02  18.4% (744; 718)
    + 14543: mip =   9.985681659e+02 >=   8.143567437e+02  18.4% (592; 1017)
    RELATIVE MIP GAP TOLERANCE REACHED; SEARCH TERMINATED
    Time used:   7.2 secs
    Memory used: 4.7 Mb (4977996 bytes)
    Writing MIP solution to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpsnzwavhu.glpk.raw'...
    2674 lines were written
    Tiempo de ejecución: 00:07
    Distancia mínima entre nodos: 2.624880949681337
    Distancia máxima entre nodos: 227.28946302017613
    Distancia promedio entre nodos: 89.40123000755095
    Distancia Total mínima posible: 579.7644990305633
    Distancia Total máxima posible: 828.2349986150906
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 998.5681658762164
    
    Ejecutando caso para 50 ciudades...
    GLPSOL--GLPK LP/MIP Solver 5.0
    Parameter(s) specified in the command line:
     --mipgap 0.2 --tmlim 120 --write /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpyz1pyy4k.glpk.raw
     --wglp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmp7w7ai1em.glpk.glp
     --cpxlp /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmppz5535le.pyomo.lp
    Reading problem data from '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmppz5535le.pyomo.lp'...
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmppz5535le.pyomo.lp:20992: warning: lower bound of variable 'x4236' redefined
    /var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmppz5535le.pyomo.lp:20992: warning: upper bound of variable 'x4236' redefined
    2163 rows, 2162 columns, 10261 non-zeros
    2116 integer variables, all of which are binary
    23108 lines were read
    Writing problem data to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmp7w7ai1em.glpk.glp'...
    18822 lines were written
    GLPK Integer Optimizer 5.0
    2163 rows, 2162 columns, 10261 non-zeros
    2116 integer variables, all of which are binary
    Preprocessing...
    2117 rows, 2116 columns, 10215 non-zeros
    2070 integer variables, all of which are binary
    Scaling...
     A: min|aij| =  1.000e+00  max|aij| =  4.600e+01  ratio =  4.600e+01
    GM: min|aij| =  8.547e-01  max|aij| =  1.170e+00  ratio =  1.369e+00
    EQ: min|aij| =  7.813e-01  max|aij| =  1.000e+00  ratio =  1.280e+00
    2N: min|aij| =  5.000e-01  max|aij| =  1.438e+00  ratio =  2.875e+00
    Constructing initial basis...
    Size of triangular part is 2116
    Solving LP relaxation...
    GLPK Simplex Optimizer 5.0
    2117 rows, 2116 columns, 10215 non-zeros
          0: obj =   7.821381746e+03 inf =   3.871e+02 (91)
        152: obj =   4.136946862e+03 inf =   2.776e-17 (0) 1
    *   456: obj =   8.069424895e+02 inf =   2.571e-15 (0) 3
    OPTIMAL LP SOLUTION FOUND
    Integer optimization begins...
    Long-step dual simplex will be used
    +   456: mip =     not found yet >=              -inf        (1; 0)
    +  2994: >>>>>   1.680513453e+03 >=   8.181105977e+02  51.3% (246; 1)
    +  5875: >>>>>   1.624669812e+03 >=   8.262062250e+02  49.1% (485; 17)
    +  7875: >>>>>   1.465238664e+03 >=   8.262198286e+02  43.6% (676; 27)
    +  8754: >>>>>   1.284204855e+03 >=   8.287654947e+02  35.5% (693; 159)
    +  9369: >>>>>   1.199505534e+03 >=   8.303047228e+02  30.8% (575; 507)
    + 14645: mip =   1.199505534e+03 >=   8.397176656e+02  30.0% (834; 734)
    + 19740: mip =   1.199505534e+03 >=   8.442817380e+02  29.6% (1239; 745)
    + 25913: mip =   1.199505534e+03 >=   8.490897735e+02  29.2% (1617; 757)
    + 31313: mip =   1.199505534e+03 >=   8.512415777e+02  29.0% (1988; 767)
    + 36980: mip =   1.199505534e+03 >=   8.539440738e+02  28.8% (2377; 779)
    + 41875: mip =   1.199505534e+03 >=   8.573901555e+02  28.5% (2739; 790)
    + 47013: mip =   1.199505534e+03 >=   8.586899326e+02  28.4% (3080; 800)
    + 52552: mip =   1.199505534e+03 >=   8.595430023e+02  28.3% (3523; 811)
    + 57667: mip =   1.199505534e+03 >=   8.611183595e+02  28.2% (3907; 822)
    + 62281: mip =   1.199505534e+03 >=   8.621826644e+02  28.1% (4233; 834)
    Time used: 60.0 secs.  Memory used: 20.1 Mb.
    + 67104: mip =   1.199505534e+03 >=   8.629965879e+02  28.1% (4549; 841)
    + 71996: mip =   1.199505534e+03 >=   8.642975759e+02  27.9% (4901; 852)
    + 76592: mip =   1.199505534e+03 >=   8.656386746e+02  27.8% (5238; 862)
    + 82407: mip =   1.199505534e+03 >=   8.666929690e+02  27.7% (5643; 874)
    + 87374: mip =   1.199505534e+03 >=   8.675718939e+02  27.7% (6025; 883)
    + 91686: mip =   1.199505534e+03 >=   8.679639701e+02  27.6% (6400; 891)
    + 96915: mip =   1.199505534e+03 >=   8.694755682e+02  27.5% (6743; 902)
    +102406: mip =   1.199505534e+03 >=   8.701209227e+02  27.5% (7122; 913)
    +107603: mip =   1.199505534e+03 >=   8.714556502e+02  27.3% (7460; 928)
    +113553: mip =   1.199505534e+03 >=   8.718380877e+02  27.3% (7906; 939)
    +118818: mip =   1.199505534e+03 >=   8.724275299e+02  27.3% (8328; 950)
    +122930: mip =   1.199505534e+03 >=   8.730053841e+02  27.2% (8672; 958)
    +124996: mip =   1.199505534e+03 >=   8.731813510e+02  27.2% (8847; 962)
    TIME LIMIT EXCEEDED; SEARCH TERMINATED
    Time used:   120.1 secs
    Memory used: 37.7 Mb (39492734 bytes)
    Writing MIP solution to '/var/folders/pn/khk4g2gd3p7fg7mp539mgph40000gp/T/tmpyz1pyy4k.glpk.raw'...
    4334 lines were written
    Tiempo de ejecución: 02:00
    Distancia mínima entre nodos: 4.085339643163096
    Distancia máxima entre nodos: 232.23341706136952
    Distancia promedio entre nodos: 97.19015980546537
    Distancia Total mínima posible: 815.2677705614591
    Distancia Total máxima posible: 1164.6682436592273
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 1199.5055343959034

    """
    #R: Se resolvio el caso A con el parametro tee=True y lo que se encontro es que el parámetro tee en el método encontrar_la_ruta_mas_corta de la clase TSP 
    #   se utiliza para controlar si se muestra la salida del solver durante la resolución del modelo de optimización. Aquí está la descripción de cómo se usa:
    #   Por ejemplo, si estableces tee=True al llamar al método encontrar_la_ruta_mas_corta, verás la salida del solver en la consola mientras se resuelve el problema de optimización. 
    #   Si estableces tee=False, la salida del solver no se mostrará en la consola. Finalmente aunque, puede ser coincidencia, cuando tee=True se obtienen rutas y tiempor de ejecucion mas cortos. 
    
    # C. Study Case 2
    print("\nC. Aplicando heurística de límites a la función objetivo...")
    study_case_2()
    
    #   A:Con huristica "limitar_funcion_objetivo"
    """
    Tiempo de ejecución: 00:41
    Distancia mínima entre nodos: 2.863564212655268
    Distancia máxima entre nodos: 244.69572942738498
    Distancia promedio entre nodos: 107.69527075294987
    Distancia Total mínima posible: 1160.8677671388537
    Distancia Total máxima posible: 1658.3825244840768
    Heurísticas aplicadas: ['limitar_funcion_objetivo']
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 1563.4615826887457
    
    """    
    # B: Sin huristica:
    """
    Tiempo de ejecución: 00:40
    Distancia mínima entre nodos: 1.0295630140986995
    Distancia máxima entre nodos: 249.97991919352242
    Distancia promedio entre nodos: 105.7341079453312
    Distancia Total mínima posible: 1139.7021874919142
    Distancia Total máxima posible: 1628.145982131306
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 2138.5108119893644
    
    """
    # R:Basándonos en los resultados proporcionados, podemos analizar las diferencias entre los dos casos:
        #Diferencia en la distancia total recorrida: En el primer caso, donde se aplicó la heurística de limitar la función objetivo, la distancia total recorrida fue de aproximadamente 1563.46. En el segundo caso, donde no se aplicó esta heurística, la distancia total recorrida fue considerablemente mayor, alrededor de 2138.51. Por lo tanto, la diferencia en la distancia total recorrida entre los dos casos es significativa.
        #Tiempo de ejecución: Aunque el tiempo de ejecución es similar en ambos casos (alrededor de 40 segundos), la diferencia en la distancia total recorrida indica que la heurística aplicada en el primer caso ayudó a encontrar una solución más óptima dentro del límite de tiempo establecido.
        #Utilidad de la heurística: La heurística de limitar la función objetivo parece ser útil en este caso específico, ya que condujo a una solución más óptima en términos de distancia total recorrida. Sin embargo, su utilidad puede depender de varios factores, como el tamaño del problema, la estructura de los datos y las características específicas del conjunto de ciudades y distancias.
        #Limitaciones de la heurística: Aunque la heurística funcionó bien en este caso particular, puede que no sea efectiva para todos los casos. Por ejemplo, en problemas con conjuntos de datos muy diferentes o con restricciones específicas, la heurística puede no proporcionar mejoras significativas o incluso puede llevar a soluciones subóptimas. Además, la efectividad de la heurística puede depender de la precisión de las estimaciones utilizadas para limitar la función objetivo.
        #En resumen, la heurística de limitar la función objetivo parece ser útil en este caso específico para mejorar la eficiencia y la calidad de la solución encontrada dentro del límite de tiempo establecido, pero su utilidad y efectividad pueden variar dependiendo de diversos factores y condiciones del problema.

    # D. Study Case 3
    print("\nD. Aplicando heurística de vecinos cercanos...")
    study_case_3()
    # A: Con huristica: Vecinos_Cercanos
    """
    Tiempo de ejecución: 01:01
    Distancia mínima entre nodos: 3.8418745424597085
    Distancia máxima entre nodos: 261.0938528575501
    Distancia promedio entre nodos: 103.69034012944502
    Distancia Total mínima posible: 1599.5416932445828
    Distancia Total máxima posible: 2285.0595617779754
    Heurísticas aplicadas: ['vecino_cercano']
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 1880.4609502141132
    """
    # B: Sin huristica: 
    """
    Tiempo de ejecución: 01:01
    Distancia mínima entre nodos: 0.9486832980505205
    Distancia máxima entre nodos: 260.2816359253952
    Distancia promedio entre nodos: 103.03220145757896
    Distancia Total mínima posible: 1455.7323865788128
    Distancia Total máxima posible: 2079.61769511259
    Heurísticas aplicadas: []
    No se encontró una solución óptima, la siguiente es la mejor solución encontrada:
    Distancia total recorrida: 1895.8307672801366
    """
    # R:
        # Basándonos en los resultados proporcionados, podemos analizar las diferencias entre los dos casos:
        # Diferencia en la distancia total recorrida: En el primer caso, donde se aplicó la heurística de vecino cercano, la distancia total recorrida fue de aproximadamente 1880.46. En el segundo caso, donde no se aplicó esta heurística, la distancia total recorrida fue de alrededor de 1895.83. Por lo tanto, la diferencia en la distancia total recorrida entre los dos casos es relativamente pequeña.
        # Tiempo de ejecución: El tiempo de ejecución es el mismo en ambos casos (alrededor de 61 segundos), lo que indica que la aplicación de la heurística de vecino cercano no tuvo un impacto significativo en el tiempo necesario para encontrar una solución.
        # Utilidad de la heurística: En este caso particular, la heurística de vecino cercano parece haber proporcionado una ligera mejora en la distancia total recorrida en comparación con el caso sin heurística. Sin embargo, la diferencia no es muy significativa. Esto sugiere que la heurística de vecino cercano puede no ser muy efectiva para este conjunto específico de ciudades y distancias.
        # Limitaciones de la heurística: Aunque la heurística de vecino cercano puede proporcionar mejoras en algunos casos, puede no ser efectiva para todos los casos. La razón podría ser que la heurística de vecino cercano no tiene en cuenta la estructura global del problema y puede quedar atrapada en mínimos locales en lugar de encontrar la solución óptima global.
        # En resumen, la heurística de vecino cercano proporcionó una ligera mejora en la distancia total recorrida en este caso particular, pero la diferencia no fue muy significativa. La efectividad de esta heurística puede variar dependiendo del conjunto específico de ciudades y distancias, y puede no ser adecuada para todos los casos.
    
