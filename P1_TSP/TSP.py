from typing import List

from P1_TSP.util import generar_ciudades_con_distancias, plotear_ruta

class CustomCityPath:
    def __init__(self, path):
        self.path = path

    def get_first_city(self):
        return self.path[0]

    def get_total_weight(self):
        total_weight = 0
        for cities, distance in self.path:
            total_weight = total_weight + distance

        return total_weight



class TSP:
    def __init__(self, ciudades, distancias):
        self.ciudades = ciudades
        self.distancias = distancias

    def get_distances_from_city_with_exclusion(self, city, removed_cities):
        distances_from_city = []
        for key, value in self.distancias.items():
            first_city, second_city = key
            if first_city == city and second_city not in removed_cities:
                distances_from_city.append({second_city: value})

        return self.sort_distances_dict(distances_from_city)

    def sort_distances_dict(self, distances_from_city):
        return sorted(distances_from_city, key=lambda x: list(x.values())[0])

    def encontrar_la_ruta_mas_corta(self):
        print(self.distancias)
        print(self.ciudades)
        path = []
        removed_cities = []

        ciudades_as_list = list(self.ciudades)
        city = ciudades_as_list[0]

        #we remove first city
        path.append(city)
        ciudades_as_list.remove(city)
        removed_cities.append(city)

        #we check the closest distance from first city
        while len(ciudades_as_list) > 0:
            custom_distances = self.get_distances_from_city_with_exclusion(city, removed_cities)
            closest_distance = custom_distances[0]
            city = list(closest_distance.keys())[0]
            path.append(city)
            ciudades_as_list.remove(city)
            removed_cities.append(city)

        return path

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