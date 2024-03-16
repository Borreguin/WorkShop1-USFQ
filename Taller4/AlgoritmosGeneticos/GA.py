from matplotlib import pyplot as plt
import numpy as np
import time
from generalSteps import *


class GA:
    def __init__(self, population, objetive, mutation_rate, n_iterations):
        self.population = population
        self.n_generation = 0
        self.n_iterations = n_iterations
        self.objetive = objetive
        self.mutation_rate = mutation_rate
        self.evaluation_type = AptitudeType.DEFAULT
        self.best_individual_selection_type = BestIndividualSelectionType.DEFAULT
        self.new_generation_type = NewGenerationType.DEFAULT

    def set_evaluation_type(self, evaluation_type: AptitudeType):
        self.evaluation_type = evaluation_type

    def set_best_individual_selection_type(self, _type:BestIndividualSelectionType):
        self.best_individual_selection_type = _type

    def set_new_generation_type(self, _type):
        self.new_generation_type = _type

    def run(self):
        success = False
        for _ in range(self.n_iterations):
            # las aptitudes son los valores que se obtienen al evaluar la función de aptitud
            aptitudes = [evaluate_aptitude(self.evaluation_type, individual, self.objetive) for individual in self.population]
            # el mejor individuo es el que tiene la mejor aptitud
            # (esto se puede elegir como maximo o minimo, depende de como se defina la aptitud)
            best_individual, best_aptitude = select_best_individual(self.best_individual_selection_type, self.population, aptitudes)
            # si el mejor individuo es igual al objetivo, se termina el algoritmo
            if best_individual == self.objetive:
                success = True
                print("Objetivo alcanzado:")
                print(f"Generación {self.n_generation}: {best_individual} - Aptitud: {best_aptitude}")
                break
            print(f"Generación {self.n_generation}: {best_individual} - población: {len(self.population)} - Aptitud: {best_aptitude}")

            # la nueva generación se obtiene a partir de la población actual, interactuando entre los individuos
            self.population = generate_new_population(self.new_generation_type, self.population, aptitudes, self.mutation_rate)
            self.n_generation += 1


        if not success:
            print(f"Objetivo no alcanzado en las iteraciones establecidas {self.n_iterations}")


class EnhancedGA(GA):
    def __init__(self, population, objetive, mutation_rate, n_iterations, elitism_rate=0.1, tournament_size=3):
        super().__init__(population, objetive, mutation_rate, n_iterations)
        self.elitism_rate = elitism_rate  # Porcentaje de individuos a mantener por elitismo
        self.tournament_size = tournament_size  # Tamaño del torneo para la selección de padres

    def tournament_selection(self, population, aptitudes):
        tournament_indices = np.random.randint(len(population), size=self.tournament_size)
        tournament_individuals = [population[i] for i in tournament_indices]
        tournament_aptitudes = [aptitudes[i] for i in tournament_indices]
        winner_index = np.argmax(tournament_aptitudes)  # Seleccionamos el mejor individuo del torneo
        return tournament_individuals[winner_index]

    def generate_new_population(self):
        new_population = []
        aptitudes = [evaluate_aptitude(self.evaluation_type, individual, self.objetive) for individual in
                     self.population]
        number_of_elites = int(len(self.population) * self.elitism_rate)

        # Elitismo: Mantener una fracción de los mejores individuos
        elites_indices = np.argsort(aptitudes)[-number_of_elites:]
        elites = [self.population[i] for i in elites_indices]
        new_population.extend(elites)

        # Generar el resto de la población mediante selección por torneo, cruce y mutación
        while len(new_population) < len(self.population):
            parent1 = self.tournament_selection(self.population, aptitudes)
            parent2 = self.tournament_selection(self.population, aptitudes)
            child1, child2 = crossover(CrossoverType.DEFAULT, parent1, parent2)
            child1 = mutate(MutationType.DEFAULT, child1, self.mutation_rate)
            child2 = mutate(MutationType.DEFAULT, child2, self.mutation_rate)
            new_population.extend([child1, child2])

        # Asegurarse de que la población no exceda su tamaño original debido al elitismo
        return new_population[:len(self.population)]

    def run(self):
        success = False
        for _ in range(self.n_iterations):
            aptitudes = [evaluate_aptitude(self.evaluation_type, individual, self.objetive) for individual in
                         self.population]
            best_individual, best_aptitude = select_best_individual(self.best_individual_selection_type,
                                                                    self.population, aptitudes)
            if best_individual == self.objetive:
                success = True
                print("Objetivo alcanzado:")
                print(f"Generación {self.n_generation}: {best_individual} - Aptitud: {best_aptitude}")
                break
            print(
                f"Generación {self.n_generation}: {best_individual} - población: {len(self.population)} - Aptitud: {best_aptitude}")
            self.population = self.generate_new_population()
            self.n_generation += 1

        if not success:
            print(f"Objetivo no alcanzado en las iteraciones establecidas {self.n_iterations}")


def case_study_1(_objetive):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 10000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

def case_study_2(_objetive):
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)
    ga.run()

def conv_elitismo(_objetive, elitism_rate = 0.1):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 10000
    ga = EnhancedGA(population, _objetive, mutation_rate, n_iterations, elitism_rate)
    ga.run()

def case_study_3(_objetive, mutation_rate):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    n_iterations = 10000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.run()
    return ga.n_generation

def case_study_4(_objetive):
    # Definición de la población inicial

    population = generate_population(700, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 10000
    ga = EnhancedGA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

# Función para medir el tiempo de ejecución
def benchmark(func, *args, repetitions=50):
    times = []
    for _ in range(repetitions):
        start_time = time.time()
        func(*args)
        times.append(time.time() - start_time)
    return np.mean(times), np.std(times)

if __name__ == "__main__":
    objetive = "GA Workshop! USFQ"
    #objetive = "Prueba Segundo CASO de la nueva distancia con una solucion absoluta"
    
    #case_study_1(objetive)
    #case_study_2(objetive)
    #case_study_4(objetive)
    #case_study_3(objetive)
    #conv_elitismo(objetive, 0.1) # Se ocupo una seleccion de elitismo

    # Corrección de la llamada a benchmark para case_study_1
    mean_time_case_study_1, std_dev_case_study_1 = benchmark(case_study_1, objetive)

    # Si necesitas pasar argumentos adicionales a conv_elitismo, asegúrate de que también se pasen correctamente.
    mean_time_conv_elitismo, std_dev_conv_elitismo = benchmark(conv_elitismo, objetive, 0.1)


    # Imprimir los resultados
    print(f"case_study_1: Tiempo promedio = {mean_time_case_study_1:.4f}s, Desviación estándar = {std_dev_case_study_1:.4f}")
    print(f"conv_elitismo: Tiempo promedio = {mean_time_conv_elitismo:.4f}s, Desviación estándar = {std_dev_conv_elitismo:.4f}")

    # Creando el gráfico
    plt.figure(figsize=(10, 6))

    # Distribuciones de los tiempos de ejecución para case_study_1
    x_case_study_1 = np.linspace(mean_time_case_study_1 - 3*std_dev_case_study_1, 
                                mean_time_case_study_1 + 3*std_dev_case_study_1, 100)
    y_case_study_1 = np.exp(-((x_case_study_1 - mean_time_case_study_1) ** 2) / (2 * std_dev_case_study_1 ** 2)) / (std_dev_case_study_1 * np.sqrt(2 * np.pi))

    # Distribuciones de los tiempos de ejecución para conv_elitismo
    x_conv_elitismo = np.linspace(mean_time_conv_elitismo - 3*std_dev_conv_elitismo, 
                                mean_time_conv_elitismo + 3*std_dev_conv_elitismo, 100)
    y_conv_elitismo = np.exp(-((x_conv_elitismo - mean_time_conv_elitismo) ** 2) / (2 * std_dev_conv_elitismo ** 2)) / (std_dev_conv_elitismo * np.sqrt(2 * np.pi))

    # Graficando las distribuciones
    plt.plot(x_case_study_1, y_case_study_1, color='blue', label='case_study_1')
    plt.fill_between(x_case_study_1, y_case_study_1, color='blue', alpha=0.5)

    plt.plot(x_conv_elitismo, y_conv_elitismo, color='red', label='conv_elitismo(objetive, 0.1)')
    plt.fill_between(x_conv_elitismo, y_conv_elitismo, color='red', alpha=0.5)

    # Añadiendo leyendas y títulos
    plt.xlabel('Tiempo de ejecución (s)')
    plt.ylabel('Densidad de probabilidad')
    plt.title('Comparación de distribuciones de tiempos de ejecución')
    plt.legend()

    plt.savefig('Images/Punto4.png')
    # Mostrar el gráfico
    plt.show()