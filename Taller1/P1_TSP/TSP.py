from typing import List
import itertools
from util import generar_ciudades_con_distancias, plotear_ruta,calcular_distancia_total



class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def encontrar_la_ruta_mas_corta(self):
        mejor_ruta = None
        mejor_distancia = float('inf')
        for ruta in itertools.permutations(self.ciudades.keys()):
            distancia_actual=calcular_distancia_total(ruta, self.distancias)
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_ruta = ruta
        return list(mejor_ruta)

    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta)

def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = tsp.encontrar_la_ruta_mas_corta()
    tsp.plotear_resultado(ruta, False)


if __name__ == "__main__":
    # Solve the TSP problem
    study_case_1()
