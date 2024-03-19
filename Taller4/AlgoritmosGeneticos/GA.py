from generalSteps import *
import pandas as pd

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

    # -------codigo incluido----
    # Métodos setter para los nuevos atributos
    def set_parent_selection_type(self, _type: ParentSelectionType):
        self.parent_selection_type = _type

    def set_crossover_type(self, _type: CrossoverType):
        self.crossover_type = _type
    #---------

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
            #print(f"Generación {self.n_generation}: {best_individual} - población: {len(self.population)} - Aptitud: {best_aptitude}")

            # la nueva generación se obtiene a partir de la población actual, interactuando entre los individuos
            self.population = generate_new_population(self.new_generation_type, self.population, aptitudes, self.mutation_rate)
            self.n_generation += 1

        if not success:
            print(f"Objetivo no alcanzado en las iteraciones establecidas {self.n_iterations}")


def case_study_1(_objetive):
    # Definición de la población inicial
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
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


def case_study_2_1(_objetive):
    population = generate_population(100, len(_objetive))
    mutation_rate = 0.01
    n_iterations = 1000
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)
       # Configurar los nuevos tipos de selección de padres y cruzamiento
    ga.set_parent_selection_type(ParentSelectionType.RANK)
    ga.set_crossover_type(CrossoverType.TWO_POINT)
    ga.run()


def case_study_3(_objetive):
    n_iterations = 1000
    # Mover la creación de la población inicial dentro del bucle para reiniciarla en cada prueba
    for mutation_rate in [0.001, 0.01, 0.05, 0.1, 0.2]:
        print(f"Probando con tasa de mutación: {mutation_rate}")
        population = generate_population(100, len(_objetive))  # Crear una nueva población para cada tasa
        ga = GA(population, _objetive, mutation_rate, n_iterations)

        # Establecemos las configuraciones optimizadas basadas en las recomendaciones
        ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
        ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
        ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)

        # Ejecutamos el GA
        ga.run()


def case_study_4(_objetive):
    n_iterations = 1000
    mutation_rate = 0.01  # Usar una tasa de mutación constante
    population_sizes = [50, 100, 200, 500, 1000]  # Diferentes tamaños de población para probar

    for size in population_sizes:
        print(f"\nProbando con tamaño de población: {size}")
        population = generate_population(size, len(_objetive))  # Crear una nueva población para cada tamaño
        ga = GA(population, _objetive, mutation_rate, n_iterations)

        # Establecer configuraciones optimizadas
        ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
        ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
        ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)

        # Ejecutar el GA
        ga.run()

def case_study_5(_objetive):
    population = generate_population(1000, len(_objetive))
    mutation_rate = 0.1 #mejor tasa de mutacion probada
    n_iterations = 1000 # mejor tamaño de poblacion probado
    ga = GA(population, _objetive, mutation_rate, n_iterations)
    ga.set_evaluation_type(AptitudeType.BY_DISTANCE)
    ga.set_best_individual_selection_type(BestIndividualSelectionType.MIN_DISTANCE)
    ga.set_new_generation_type(NewGenerationType.MIN_DISTANCE)
       # Aplicando nuevos tipos de selección de padres y de cruzamiento
    ga.set_parent_selection_type(ParentSelectionType.RANK)
    ga.set_crossover_type(CrossoverType.TWO_POINT)
    ga.run()



if __name__ == "__main__":
    objetive = "GA Workshop! USFQ"
    #case_study_1(objetive)
    #case_study_2(objetive)
    #case_study_3(objetive)
    #case_study_4(objetive)
    case_study_5(objetive)