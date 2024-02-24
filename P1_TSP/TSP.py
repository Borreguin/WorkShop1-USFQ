from itertools import permutations
from typing import List

from P1_TSP.util import generar_ciudades_con_distancias, plotear_ruta, calcular_distancia_total


class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self):
        shortest_distance = float('inf')
        shortest_route = None

        for ruta in permutations(self.ciudades.keys()):
            distancia_total = calcular_distancia_total(ruta, self.distancias)
            if distancia_total < shortest_distance:
                shortest_distance = distancia_total
                shortest_route = ruta

        return shortest_route

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    print(distancias)
    tsp = TSP(ciudades, distancias)
    # #ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)

def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    print(distancias)
    #tsp = TSP(ciudades, distancias)
    # ruta = ciudades.keys()
    #ruta = tsp.encontrar_la_ruta_mas_corta()
    #tsp.plotear_resultado(ruta, False)


if __name__ == "__main__":
    # Solve the TSP problem
    study_case_1()