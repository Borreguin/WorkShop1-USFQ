import numpy as np

from Taller4.AlgoritmosGeneticos.generalSteps import *


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

def conv_elitismo(_objetive):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 10000
    ga = EnhancedGA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

def case_study_3(_objetive):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.004
    n_iterations = 10000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

def case_study_4(_objetive):
    # Definición de la población inicial
    population = generate_population(700, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 10000
    ga = EnhancedGA(population, _objetive, mutation_rate, n_iterations)
    ga.run()

if __name__ == "__main__":
    objetive = "GA Workshop! USFQ"
    #objetive = "Prueba Segundo CASO de la nueva distancia con una solucion absoluta"
    #
    #case_study_1(objetive)
    #case_study_2(objetive)
    #case_study_4(objetive)
    case_study_3(objetive)