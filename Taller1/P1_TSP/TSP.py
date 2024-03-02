from typing import List

from P1_TSP.util import generar_ciudades_con_distancias, plotear_ruta

class CustomCityPath:
    def __init__(self, city):
        self.path = [city]
        # self.distance = 0

    def get_distance(self, distancias):
        distance = 0
        for index in range(len(self.path) - 2):
            distance = distance + distancias[(self.path[index], self.path[index + 1])]

        if self.get_actual_city() != self.get_first_city():
            distance = distance + distancias[(self.path[len(self.path) - 1], self.get_first_city())]

        return distance

    def get_actual_city(self):
        return self.path[len(self.path) - 1]

    def get_first_city(self):
        return self.path[0]

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
        custom_city_paths = []
        ciudades_as_list = list(self.ciudades)

        city_init = ciudades_as_list[0]
        custom_city_paths.append(CustomCityPath(city_init))
        ciudades_as_list.remove(city_init)
        n_iterations = 0
        custom_city = custom_city_paths[0]

        while True:
            n_iterations += 1
            if n_iterations > 5000:
                break
            if n_iterations % 100 == 0:
                print("n_iterations: ", n_iterations)
            custom_city_to_add = []
            custom_city = custom_city_paths[0]

            if len(custom_city.path) == len(self.ciudades) + 1:
                break

            if len(custom_city.path) != len(self.ciudades):
                for ciudad_in_list in ciudades_as_list:
                    if ciudad_in_list not in custom_city.path:
                        custom_city_2 = CustomCityPath(custom_city.get_first_city())
                        custom_city_2.path = custom_city.path.copy()
                        custom_city_2.path.append(ciudad_in_list)
                        custom_city_to_add.append(custom_city_2)
            else:
                ciudad_in_list = custom_city.get_first_city()
                custom_city_2 = CustomCityPath(custom_city.get_first_city())
                custom_city_2.path = custom_city.path.copy()
                custom_city_2.path.append(ciudad_in_list)
                custom_city_to_add.append(custom_city_2)

            custom_city_paths.remove(custom_city)

            for custom_city in custom_city_to_add:
                custom_city_paths.append(custom_city)

            custom_city_paths = sorted(custom_city_paths, key=lambda x: x.get_distance(self.distancias))

        custom_city.path.append(custom_city.get_first_city())
        print("distance: ", custom_city.get_distance(self.distancias))
        return custom_city.path

    def encontrar_la_ruta_mas_corta_2(self):
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