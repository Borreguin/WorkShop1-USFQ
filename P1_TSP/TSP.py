from itertools import permutations
from typing import List

from P1_TSP.util import generar_ciudades_con_distancias, plotear_ruta, calcular_distancia_total


class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self):
        shotest_distance = float('inf')
        shortest_route =None
        for route in permutations(self.ciudades.keys()):
            distance = calcular_distancia_total(route, self.distancias)
            if distance < shotest_distance:
                shotest_distance = distance
                shortest_route = route
        return shortest_route


        # implementación aquí

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    #ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)

def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    #ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta, False)


if __name__ == "__main__":
    # Solve the TSP problem
    study_case_1()
    #study_case_2()