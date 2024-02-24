from typing import List

from util import generar_ciudades_con_distancias, plotear_ruta, calcular_ruta_total


class TSP:
    def __init__(self, ciudades, distancias, distanciaT=0):
        self.ciudades = ciudades
        self.distancias = distancias
        self.distanciaT = distanciaT

    def encontrar_la_ruta_mas_corta(self):
        ruta = []
        ciudades_visitadas = set()
        # Empieza en la primera ciudad (puedes elegir cualquier ciudad como punto de partida)
        ciudad_actual = list(self.ciudades.keys())[0]
        ruta.append(ciudad_actual)
        ciudades_visitadas.add(ciudad_actual)

        while len(ciudades_visitadas) < len(self.ciudades):
            distancia_minima = float('inf')
            proxima_ciudad = None
            for ciudad in self.ciudades:
                if ciudad not in ciudades_visitadas and self.distancias[(ciudad_actual, ciudad)] < distancia_minima:
                    proxima_ciudad = ciudad
                    distancia_minima = self.distancias[(ciudad_actual, ciudad)]
            ciudad_actual = proxima_ciudad
            ruta.append(ciudad_actual)
            ciudades_visitadas.add(ciudad_actual)
        return ruta


    def plotear_resultado(self, ruta: List[str], mostrar_anotaciones: bool = True):
        plotear_ruta(self.ciudades, ruta, mostrar_anotaciones,distanciaTotal=self.distanciaT)


def study_case_1():
    n_cities = 10
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    disTotal= calcular_ruta_total(ruta, distancias)
    tsp.distanciaT=disTotal
    tsp.plotear_resultado(ruta)
    print('distancia total: ',disTotal)

def study_case_2():
    n_cities = 100
    ciudades, distancias = generar_ciudades_con_distancias(n_cities)
    tsp = TSP(ciudades, distancias)
    ruta = ciudades.keys()
    ruta = tsp.encontrar_la_ruta_mas_corta()
    disTotal= calcular_ruta_total(ruta, distancias)
    tsp.distanciaT=disTotal
    tsp.plotear_resultado(ruta, False)
    print('distancia total: ',disTotal)

if __name__ == "__main__":
    # Solve the TSP problem
    study_case_2()